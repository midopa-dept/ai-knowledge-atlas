"""Full/Incremental 전 중간값·별도 Attention 기준·정보 접근을 검사한다."""
import json
from pathlib import Path
import torch
from torch.nn import functional as F
from integrated_transformer import train, generate, dataset, EncoderDecoder, Attention


def close(a, b):
    torch.testing.assert_close(a, b, rtol=2e-11, atol=2e-11)
    return float((a-b).abs().max())


def check_reference(attention, block):
    """관찰 Head 반환을 PyTorch의 별도 SDPA와 직접 스칼라 합으로 대조한다."""
    t = block['attention']
    reference = F.scaled_dot_product_attention(t['q'], t['k'], t['v'],
                                               attn_mask=t['allowed'][:, None], dropout_p=0.)
    close(reference, t['heads'])
    # 첫 batch/Head의 모든 요청을 별도 좌표 내적·지수·합으로 계산한다.
    rows = []
    for q, allowed in zip(t['q'][0, 0], t['allowed'][0]):
        scores = torch.stack([sum(q[d]*key[d] for d in range(len(q)))
                              / len(q)**.5 for key in t['k'][0, 0]])
        exps = torch.where(allowed, (scores-scores[allowed].max()).exp(), 0.)
        weights = exps/exps.sum()
        rows.append(torch.stack([sum(weights[j]*t['v'][0, 0, j, d]
                                     for j in range(len(weights))) for d in range(q.shape[-1])]))
    close(torch.stack(rows), t['heads'][0, 0])
    # nn.Linear는 행벡터 수식의 W를 weight.T로 저장한다.
    close(t['mixed'], t['joined'] @ attention.out.weight.T)


@torch.no_grad()
def validate():
    # 학습은 별도 활성 gradient 문맥에서 실제로 실행한다.
    with torch.enable_grad():
        model, learning = train()
    assert learning['steps'] == 80 and learning['final_loss'] < learning['initial_loss']
    assert learning['update_norm'] > 0
    inputs, targets = dataset()
    assert torch.equal(inputs[:, 1:], targets[:, :-1])
    errors, cases = [], []
    for tokens in [torch.tensor([[0, 1, 2, 3, 0]]),
                   torch.tensor([[2, 0, 3, 1, 2], [1, 3, 2, 0, 1]])]:
        full_logits, full_cache, full = model(tokens, use_cache=True, trace=True)
        cache = None
        for i in range(tokens.shape[1]):
            logit, new_cache, inc = model(tokens[:, i:i+1], past=cache, use_cache=True, trace=True)
            errors.append(close(logit, full_logits[:, i:i+1]))
            for key in ['embedding', 'position', 'initial', 'returned', 'final', 'logits']:
                errors.append(close(inc[key], full[key][:, i:i+1]))
            for layer, (one, all_rows) in enumerate(zip(inc['blocks'], full['blocks'])):
                for key in ['input', 'z', 'r', 'u', 'f', 'returned']:
                    errors.append(close(one[key], all_rows[key][:, i:i+1]))
                a, fa = one['attention'], all_rows['attention']
                for key in ['q', 'new_k', 'new_v', 'heads']:
                    errors.append(close(a[key], fa[key][:, :, i:i+1]))
                for key in ['k', 'v']:
                    errors.append(close(a[key], fa[key][:, :, :i+1]))
                errors.append(close(a['scores'], fa['scores'][:, :, i:i+1, :i+1]))
                errors.append(close(a['weights'], fa['weights'][:, :, i:i+1, :i+1]))
                for key in ['joined', 'mixed']:
                    errors.append(close(a[key], fa[key][:, i:i+1]))
                if cache is not None:
                    for old, new in zip(cache.layers[layer], new_cache.layers[layer]):
                        assert torch.equal(old, new[:, :, :i])
                check_reference(model.blocks[layer].attention, one)
            assert new_cache.positions.tolist() == list(range(i+1))
            assert torch.equal(new_cache.tokens, tokens[:, :i+1])
            cache = new_cache
        for one, all_rows in zip(cache.layers, full_cache.layers):
            for a, b in zip(one, all_rows):
                errors.append(close(a, b))
        cases.append(dict(batch=tokens.shape[0], length=tokens.shape[1],
                          cache_shapes=[list(k.shape) for k, v in cache.layers]))
    # 미래 차단은 앞쪽 Logit뿐 아니라 앞쪽 레이어별 K/V와 반환도 검사한다.
    x = torch.tensor([[0, 1, 2, 3]])
    changed = torch.tensor([[0, 1, 3, 0]])
    a, ca, ta = model(x, use_cache=True, trace=True)
    b, cb, tb = model(changed, use_cache=True, trace=True)
    close(a[:, :2], b[:, :2])
    for ka, kb in zip(ca.layers, cb.layers):
        for va, vb in zip(ka, kb):
            close(va[:, :, :2], vb[:, :, :2])
    for ra, rb in zip(ta['blocks'], tb['blocks']):
        close(ra['returned'][:, :2], rb['returned'][:, :2])
    past_change = model(torch.tensor([[3, 1, 2, 3]]))[0]
    positive = float((past_change[:, 1]-a[:, 1]).abs().max())
    assert positive > 1e-6
    # 같은 Token도 위치표의 다른 행을 읽는다.
    close(ta['initial'][:, 2], model.token(x[:, 2])+model.position(torch.tensor([2])))
    assert not torch.equal(model.position(torch.tensor([0])), model.position(torch.tensor([2])))
    # 같은 shape라도 둘째 레이어 K는 첫째 레이어 K의 복사본이 아니다.
    assert not torch.allclose(ca.layers[0][0], ca.layers[1][0])
    sequence, gc, history = generate(model, torch.tensor([[0, 1]]))
    assert sequence == [0, 1, 2, 3, 0, 1, 2, 3]
    assert gc.tokens.tolist()[0] == sequence[:-1] and gc.positions.tolist() == list(range(7))
    assert history[0]['processed_positions'] == [0, 1]
    rejected = []
    def refuse(name, call):
        try:
            call()
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    refuse('빈 입력', lambda: model(torch.empty(1, 0, dtype=torch.long)))
    with torch.enable_grad():
        refuse('gradient 활성 Cache', lambda: model(x, use_cache=True))
    model.train()
    refuse('학습 중 Cache', lambda: model(x, use_cache=True))
    model.eval()
    with torch.no_grad():
        model.blocks[0].attention.q.weight.add_(.01)
    refuse('매개변수 변경 후 Cache', lambda: model(x[:, :1], past=ca, use_cache=True))
    refuse('위치표 범위 초과', lambda: model(torch.zeros(1, 33, dtype=torch.long)))
    att = Attention(8, 2).double()
    h = torch.randn(1, 2, 8, dtype=torch.float64)
    mask = torch.tensor([[[True, False], [True, False]]])
    _, _, mt = att(h, h, mask, trace=True)
    assert torch.equal(mt['weights'][:, :, :, 1], torch.zeros(1, 2, 2))
    refuse('빈 허용 행', lambda: att(h, h, torch.zeros(1, 2, 2, dtype=torch.bool)))
    torch.manual_seed(23)
    ed = EncoderDecoder().double().eval()
    source, prefix = torch.tensor([[0, 2, 1]]), torch.tensor([[0, 1]])
    el, et = ed(source, prefix, trace=True)
    future, ft = ed(source, torch.tensor([[0, 3]]), trace=True)
    close(el[:, :1], future[:, :1])
    source_changed = ed(torch.tensor([[3, 2, 1]]), prefix)[0]
    source_positive = float((el-source_changed).abs().max())
    assert source_positive > 1e-6
    assert et['cross_attention']['q'].shape == (1, 2, 2, 4)
    assert et['cross_attention']['k'].shape == (1, 2, 3, 4)
    assert el.shape == (1, 2, 4)
    for attention, record in [(ed.encoder.attention, et['encoder']),
                              (ed.self_attention, {'attention': et['self_attention']}),
                              (ed.cross, {'attention': et['cross_attention']})]:
        check_reference(attention, record)
    result = dict(full_incremental_max_abs_error=max(errors), compared_tensors=len(errors),
                  cases=cases, causal_future_unchanged=True, past_positive_max_change=positive,
                  encoder_source_positive_max_change=source_positive,
                  generated=sequence, processed_positions=gc.positions.tolist(),
                  reference='PyTorch SDPA와 별도 좌표별 내적·지수·가중합', rejected=rejected,
                  learning=learning)
    p = Path(__file__).resolve().parent/'INTEGRATED_CHECKS.json'
    p.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('Full/Incremental 최대 절대오차:', max(errors), '비교 수:', len(errors))
    print('미래 불변/과거 변경/원문 변경/두 층 K/V/별도 계산: 확인')
    print('거부 계약:', rejected)


if __name__ == '__main__':
    validate()
