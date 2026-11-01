"""본문의 두 요청을 실행한다."""
import numpy as np
from aggregate import aggregate, normalize_rows

scores = np.array([[1, 3, 1], [1, 1, 3]], dtype=float)
values = np.array([[2, 0], [0, 4], [2, 4]], dtype=float)
weights = normalize_rows(scores)
print("가중치")
print(weights)
print("출력")
print(aggregate(weights, values))
