"""본문 대표 계산과 제공자 변경 실험을 재현한다."""
import numpy as np
from sources import example_inputs, self_attention, cross_attention, project
np.set_printoptions(precision=6, suppress=True)
x, h, wq, wk, wv, uq, r = example_inputs()
self_result = self_attention(x, wq, wk, wv)
cross_result = cross_attention(h, x, uq, wk, wv)
for title, result in [("Self", self_result), ("Cross", cross_result)]:
    print(title)
    for name, value in zip(["Q", "K", "V", "S", "A", "O"], result):
        print(name, "=", value)
print("Self의 예시 반환 X+O =", x + self_result[-1])
print("Cross의 예시 반환 H+OR =", h + project(cross_result[-1], r))
z_changed = x.copy()
z_changed[2] = [2., 1.]
changed = cross_attention(h, z_changed, uq, wk, wv)
print("Z의 행2 변경 후 Cross O =", changed[-1])
mask = np.array([[True, True, False], [True, True, False]])
masked = cross_attention(h, x, uq, wk, wv, mask)
print("Z의 행2 차단 후 Cross O =", masked[-1])
