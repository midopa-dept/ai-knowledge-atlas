"""두 배치 순서의 전 중간값을 CPU에서 출력한다."""
import numpy as np
from block import example_inputs, post_ln, pre_ln
np.set_printoptions(precision=6, suppress=True)
inputs = example_inputs()
print("입력", inputs[0], sep="\n")
for name, fn in [("Post-LN", post_ln), ("Pre-LN", pre_ln)]:
    y, trace = fn(*inputs)
    print(name)
    for key, value in trace.items():
        if key == "heads":
            for i, head in enumerate(value, 1):
                for subkey, array in head.items():
                    print(f"Head{i} {subkey}", array, sep="\n")
        elif isinstance(value, dict):
            for subkey, array in value.items():
                print(f"{key} {subkey}", array, sep="\n")
        else:
            print(key, value, sep="\n")
