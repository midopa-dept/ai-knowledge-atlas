"""독립 문제의 좌표별 기여와 두 확률비 요구를 구현한다."""
import numpy as np
from scoring import scaled_dot_product


def with_contributions(q, k, v):
    dots, scores, a, o = scaled_dot_product(q, k, v)
    # 질의·제공 위치·값 좌표의 세 축을 남긴다.
    c = a[:, :, None] * np.asarray(v)[None, :, :]
    return dots, scores, a, c, o


def queries_for_odds(ratios):
    """키가 단위축일 때 a1/a3와 a2/a3를 지정한다."""
    ratios = np.asarray(ratios, dtype=np.float64)
    if ratios.ndim != 2 or ratios.shape[1] != 2:
        raise ValueError("비율 쌍을 행으로 제공한다")
    if not np.isfinite(ratios).all() or np.any(ratios <= 0):
        raise ValueError("비율은 양의 유한수여야 한다")
    return np.sqrt(2.) * np.log(ratios)
