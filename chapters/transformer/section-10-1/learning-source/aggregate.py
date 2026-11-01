"""교육용 행 합 규칙과 값 집계. 실제 학습 매개변수를 사용하지 않는다."""

import numpy as np



def normalize_rows(scores):
    """비음수 점수를 각 요청의 제공 위치 합으로 나눈다."""
    scores = np.asarray(scores, dtype=float)
    if scores.ndim != 2 or scores.shape[1] == 0:
        raise ValueError("점수는 제공 위치가 있는 2차원 배열이어야 한다")
    if not np.isfinite(scores).all() or (scores < 0).any():
        raise ValueError("이 규칙에는 유한한 비음수 점수가 필요하다")
    totals = scores.sum(axis=1, keepdims=True)
    if (totals <= 0).any() or not np.isfinite(totals).all():
        raise ValueError("각 요청의 점수 합은 유한한 양수여야 한다")
    return scores / totals


def aggregate(weights, values):
    """가중치 열과 값 행은 같은 제공 위치 순서여야 한다."""
    a = np.asarray(weights, dtype=float)
    v = np.asarray(values, dtype=float)
    if a.ndim != 2 or v.ndim != 2 or a.shape[1] != v.shape[0]:
        raise ValueError("가중치 열 수와 값 행 수가 같아야 한다")
    if a.shape[1] == 0 or v.shape[1] == 0:
        raise ValueError("제공 위치와 값 좌표가 필요하다")
    if not np.isfinite(a).all() or not np.isfinite(v).all():
        raise ValueError("입력은 유한해야 한다")
    if (a < 0).any() or not np.allclose(a.sum(axis=1), 1):
        raise ValueError("비율은 비음수이고 각 행의 합이 1이어야 한다")
    # 요청마다 같은 값 행을 자기 비율로 곱해 위치 축에서 더한다.
    return a @ v


def contributions(weights, values):
    """요청·제공 위치·값 좌표의 세 축을 보존한다."""
    expected = aggregate(weights, values)
    a = np.asarray(weights, dtype=float)
    v = np.asarray(values, dtype=float)
    parts = a[:, :, None] * v[None, :, :]
    # 가운데 축은 제공 위치다. 좌표 축을 합하지 않는다.
    assert np.allclose(parts.sum(axis=1), expected)
    return parts


def move_weight(weights, source, target, amount):
    """0부터 시작하는 두 출처 인덱스 사이에서 비율을 옮긴다."""
    a = np.asarray(weights, dtype=float).copy()
    if a.ndim != 1 or not np.isfinite(a).all() or (a < 0).any():
        raise ValueError("비율 행은 유한한 비음수 1차원 배열이어야 한다")
    if not np.isclose(a.sum(), 1):
        raise ValueError("비율 행의 합은 1이어야 한다")
    if not 0 <= source < len(a) or not 0 <= target < len(a):
        raise ValueError("출처 인덱스가 범위를 벗어났다")
    if source == target or not np.isfinite(amount):
        raise ValueError("서로 다른 출처와 유한한 이동량이 필요하다")
    if not 0 <= amount <= a[source]:
        raise ValueError("옮기는 양은 출발 비율 이하의 비음수여야 한다")
    a[source] -= amount
    a[target] += amount
    return a


def reorder_sources(weights, values, order):
    """가중치 열과 값 행을 같은 순열로 옮긴다."""
    aggregate(weights, values)
    order = np.asarray(order)
    n = np.asarray(values).shape[0]
    if order.ndim != 1 or not np.array_equal(np.sort(order), np.arange(n)):
        raise ValueError("순열은 모든 제공 위치를 한 번씩 포함해야 한다")
    return np.asarray(weights)[:, order], np.asarray(values)[order]
