"""학습 모델 첫 Head의 같은 Q/K/V에서 Full·Local·별도 Kernel을 비교한다."""
import json
from pathlib import Path
import numpy as np
import torch
from integrated_transformer import train
from efficient import sparse_attention, causal_mask
from kv_cache import serial


def run():
    model, _ = train()
    with torch.no_grad():
        _, _, trace = model(torch.tensor([[0, 1, 2, 3, 0]]), trace=True)
    a = trace['blocks'][0]['attention']
    q, k, v = [a[name][0, 0].numpy() for name in ('q', 'k', 'v')]
    p = np.arange(1, 6)
    full_mask, local_mask = causal_mask(p, p), causal_mask(p, p, 2)
    full = sparse_attention(q, k, v, full_mask)
    local = sparse_attention(q, k, v, local_mask)
    # r=2의 별도 특징맵이다. Softmax 근사 보장은 부여하지 않는다.
    pq = np.column_stack((np.ones(5), np.maximum(q[:, 0], 0)))
    pk = np.column_stack((np.ones(5), np.maximum(k[:, 0], 0)))
    direct, factor, states, weights = [], [], [], []
    s, z = np.zeros((2, 4)), np.zeros(2)
    for i in range(5):
        coefficients = pq[i] @ pk[:i+1].T
        weights.append(coefficients/coefficients.sum())
        direct.append((coefficients @ v[:i+1])/coefficients.sum())
        s = s + pk[i, :, None]*v[i, None, :]
        z = z + pk[i]
        factor.append(pq[i] @ s / (pq[i] @ z))
        states.append(dict(s=s.copy(), z=z.copy()))
    assert np.allclose(direct, factor, rtol=1e-13, atol=1e-13)
    assert np.allclose(full[2], a['heads'][0, 0].numpy(), rtol=1e-12, atol=1e-12)
    result = dict(q=q, k=k, v=v, full_mask=full_mask, local_mask=local_mask,
                  full=dict(scores=full[0], weights=full[1], output=full[2]),
                  local=dict(scores=local[0], weights=local[1], output=local[2]),
                  phi_q=pq, phi_k=pk, kernel_weights=weights,
                  kernel_direct=np.array(direct), kernel_factor=np.array(factor), states=states,
                  allowed_pairs=dict(full=15, local=9, kernel=15),
                  coordinate_multiplications=dict(full=120, local=72, factor=90),
                  scope='점수/Value 또는 특징 상태 생성·읽기만 포함. 투영·특징 생성·지수·나눗셈·FFN 제외.')
    # 금지 점수는 JSON 표준의 null로 기록한다.
    data=serial(result)
    for kind in ('full', 'local'):
        data[kind]['scores']=[[None if not np.isfinite(x) else x for x in row]
                              for row in result[kind]['scores']]
    (Path(__file__).resolve().parent/'COMPARISON_INTEGRATED.json').write_text(
        json.dumps(data, ensure_ascii=False, allow_nan=False, indent=2)+'\n')
    for name, out in [('Full', full[2]), ('Local', local[2]), ('Kernel', np.array(factor))]:
        print(name, '마지막 Head 반환:', out[-1])
    print('허용 쌍 Full15/Local9/Kernel15; 좌표 곱셈120/72/90; 실행 시간 실측 없음')
    return result


if __name__ == '__main__':
    run()
