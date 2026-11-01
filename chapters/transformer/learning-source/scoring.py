"""행렬의 행은 질의 또는 제공 위치다. 유한한 실수·비차단 입력을 받는다."""
import numpy as np


def softmax_rows(scores):
    """각 질의의 제공 위치 축을 따로 정규화한다."""
    scores = np.asarray(scores, dtype=np.float64)
    if scores.ndim != 2 or 0 in scores.shape:
        raise ValueError("점수는 비어 있지 않은 2차원 배열이어야 한다")
    if not np.isfinite(scores).all():
        raise ValueError("이 함수는 유한 점수만 받는다")
    # 최대값을 빼면 적어도 한 지수는 1, 나머지는 1 이하다.
    shifted = scores - scores.max(axis=1, keepdims=True)
    weights = np.exp(shifted)
    return weights / weights.sum(axis=1, keepdims=True)


def scaled_dot_product(q, k, v):
    """내적·scale·행별 비율·집계 출력을 순서대로 반환한다."""
    q, k, v = [np.asarray(x, dtype=np.float64) for x in (q, k, v)]
    if any(x.ndim != 2 or 0 in x.shape for x in (q, k, v)):
        raise ValueError("Q/K/V는 비어 있지 않은 행렬이어야 한다")
    if q.shape[1] != k.shape[1] or k.shape[0] != v.shape[0]:
        raise ValueError("비교 폭 또는 키/값의 제공 위치 수가 다르다")
    if not all(np.isfinite(x).all() for x in (q, k, v)):
        raise ValueError("Q/K/V의 원소는 유한해야 한다")
    # 두 합 축을 구별한다: 여기서는 비교 좌표, 마지막에는 제공 위치.
    dots = q @ k.T
    scores = dots / np.sqrt(q.shape[1])
    a = softmax_rows(scores)
    o = a @ v
    if not np.isfinite(o).all():
        raise ValueError("출력의 표현 범위를 벗어났다")
    return dots, scores, a, o
