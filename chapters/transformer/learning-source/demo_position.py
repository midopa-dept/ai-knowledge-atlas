"""세 방식을 같은 내용에서 비교한다."""
import numpy as np
from sources import project
from masking import masked_attention, causal_allowed
from position import (comparison_inputs, absolute_attention, biased_attention,
                      rotary_attention, sinusoidal)

np.set_printoptions(precision=9, suppress=True)
x, wq, wk, wv, e, p, table = comparison_inputs()
q, k, v = project(x, wq), project(x, wk), project(x, wv)
b = np.ones((3, 3), dtype=bool)
print("기본 Q/K/V", q, k, v, sep="\n")
print("Sinusoidal 폭4, 위치0/1/2", sinusoidal(p, 4), sep="\n")
for title, result, names in [
    ("위치 없음", masked_attention(q, k, v, b), ["S", "A", "O"]),
    ("Absolute", absolute_attention(x, x, e, e, wq, wk, wv, b),
     ["Q", "K", "V", "S", "A", "O"]),
    ("Relative", biased_attention(q, k, v, p, p, table, b),
     ["원점수", "편향", "S", "A", "O"]),
    ("RoPE", rotary_attention(q, k, v, p, p, [np.pi/2], b),
     ["회전 Q", "회전 K", "S", "A", "O"]),
    ("RoPE+Causal", rotary_attention(q, k, v, p, p, [np.pi/2],
                                    causal_allowed(p, p, np.ones(3, dtype=bool))),
     ["회전 Q", "회전 K", "S", "A", "O"]),
]:
    print(title)
    for name, value in zip(names, result):
        print(name, value.shape, value, sep="\n")
