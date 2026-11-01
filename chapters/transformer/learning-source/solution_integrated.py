"""새 종합 문제의 수치 해설. 문제 본문에는 완성 결과를 먼저 제공하지 않는다."""
from pathlib import Path
import json
import numpy as np
from kv_cache import example_model, full_prefix, incremental, norm, feed, serial


def solve():
    x = np.array([[2., 0.], [0., 1.], [1., 2.]])
    wo = np.array([[1., -1.], [.5, 1.]])
    heads = []
    for coord, scale in [(0, 2.), (1, 3.)]:
        q = x[:, coord:coord+1]; k = q.copy(); v = scale*q
        s = q @ k.T
        e = np.exp(s-s.max(axis=1, keepdims=True)); a = e/e.sum(axis=1, keepdims=True)
        heads.append(dict(q=q, k=k, v=v, s=s, a=a, o=a@v))
    joined = np.concatenate([h['o'] for h in heads], axis=1)
    h = np.array([[1., -1.]])
    mixed = np.array([[.5, .25]])
    r = h + mixed
    u = norm(r, np.ones(2), np.zeros(2), 1.)
    active, f = feed(u, np.diag([1., -1.]), np.diag([.25, .5]), np.zeros(2), np.zeros(2))
    model = example_model()
    model['embedding'] = np.array([[.8, .2], [-.2, 1.1], [1.4, .3]])
    old_h, old_g, past, old_trace = full_prefix(model, [0, 1], [0, 1])
    returned, logits, updated, inc = incremental(model, [0, 1], [0, 1], 2, 2, past)
    full_h, full_g, full_cache, full_trace = full_prefix(model, [0, 1, 2], [0, 1, 2])
    assert np.allclose(returned[0], full_h[-1], rtol=1e-13, atol=1e-13)
    assert np.allclose(logits[0], full_g[-1], rtol=1e-13, atol=1e-13)
    result = dict(heads=heads, joined=joined, mixed=joined@wo,
                  block=dict(h=h, mixed=mixed, r=r, u=u, active=active, f=f, returned=r+f),
                  cache=dict(past=past, old_trace=old_trace, incremental=inc,
                             returned=returned, logits=logits, updated=updated))
    (Path(__file__).resolve().parent/'SOLUTIONS_INTEGRATED.json').write_text(
        json.dumps(serial(result), ensure_ascii=False, indent=2)+'\n')
    print('새 Head 결합:', result['mixed'])
    print('새 Pre-LN 반환:', r+f)
    print('새 두 레이어 반환/Logit:', returned, logits)
    for i, c in enumerate(past['layers']):
        print('과거 층',i+1,[(h['k'].ravel().tolist(),h['v'].ravel().tolist()) for h in c['heads']])
    for i, t in enumerate(inc):
        print('새 층',i+1,'z',t['z'],'반환',t['result'],'가중치',[h['weights'] for h in t['heads']])
    return result


if __name__ == '__main__':
    solve()
