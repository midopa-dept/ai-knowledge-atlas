"""출처별 기여를 반환하는 독립 연습의 한 풀이."""
import numpy as np
from aggregate import aggregate


def with_contributions(weights, values):
    # 입력 검사를 재사용하고, 출처별 중간값을 별도로 만든다.
    expected = aggregate(weights, values)
    weights = np.asarray(weights, dtype=float)
    values = np.asarray(values, dtype=float)
    parts = weights[:, :, None] * values[None, :, :]
    output = parts.sum(axis=1)
    assert np.allclose(output, expected)
    return parts, output
