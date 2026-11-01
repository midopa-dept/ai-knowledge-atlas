"""대표 두 Head의 모든 중간값과 순서·Mask 변형을 출력한다."""
import numpy as np
from heads import multi_head, example_inputs
np.set_printoptions(precision=6, suppress=True)
x, heads, wo = example_inputs()
traces, c, y = multi_head(x, x, heads, wo)
for r, t in enumerate(traces, 1):
    print(f"Head {r}")
    for key, value in t.items():
        if key == "s":
            d = t["q"] @ t["k"].T
            print(f"d {d.shape} =\n{d}")
        print(f"{key} {value.shape} =\n{value}")
print("Concat =\n", c, sep="")
print("최종 Y =\n", y, sep="")
print("Head만 교환 =\n", multi_head(x, x, heads[::-1], wo)[2], sep="")
print("Head와 W_O 대응 교환 =\n",
      multi_head(x, x, heads[::-1], wo[::-1])[2], sep="")
b = np.tril(np.ones((3, 3), dtype=bool))
print("두 Head 모두 Causal Y =\n",
      multi_head(x, x, heads, wo, [b, b])[2], sep="")
