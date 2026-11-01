"""독립 연습의 재배열: K/V와 실제 위치를 같은 순서로 옮긴다."""
import numpy as np
from position import comparison_inputs, rotary_attention
from sources import project
from masking import causal_allowed

x, wq, wk, wv, _, p, _ = comparison_inputs()
q, k, v = project(x, wq), project(x, wk), project(x, wv)
order = np.array([2, 0, 1])
allowed = causal_allowed(p, p[order], np.ones(3, dtype=bool))
_, _, scores, weights, output = rotary_attention(
    q, k[order], v[order], p, p[order], [np.pi/2], allowed)
print("재배열된 키의 원래 위치", p[order])
print("비율", weights)
print("출력", output)


def split_half(x, p, theta):
    """Split-half 저장 순서를 인접 쌍으로 옮겨 기존 회전을 재사용한다."""
    from position import rope
    from sources import matrix
    x = matrix(x)
    d = x.shape[1]
    if d % 2:
        raise ValueError("Split-half의 전체 회전 폭은 짝수여야 한다")
    order = np.array([i for r in range(d//2) for i in (r, r+d//2)])
    inverse = np.argsort(order)
    return rope(x[:, order], p, theta)[:, inverse]
