"""단일 시퀀스·단일 Head·2차원 배열. True는 읽기 허용이다."""
import numpy as np


def causal_allowed(query_pos, key_pos, key_valid):
    """배열 순서 대신 원래 위치를 비교하고 패딩 키를 제외한다."""
    qp, kp = np.asarray(query_pos), np.asarray(key_pos)
    valid = np.asarray(key_valid)
    if any(x.ndim != 1 or x.size == 0 for x in (qp, kp, valid)):
        raise ValueError("위치와 유효성은 비어 있지 않은 벡터여야 한다")
    if any(x.dtype.kind not in "iu" for x in (qp, kp)):
        raise ValueError("원래 위치는 정수여야 한다")
    if valid.dtype != np.bool_ or valid.shape != kp.shape:
        raise ValueError("key_valid는 키별 Boolean이어야 한다")
    # (m,1)과 (1,n)의 비교 결과는 (m,n)이다.
    return (kp[None, :] <= qp[:, None]) & valid[None, :]


def masked_softmax(scores, allowed, active=None):
    """유효 질의의 빈 허용 집합은 오류, 비활성 질의는 계수0."""
    s = np.asarray(scores, dtype=np.float64)
    mask = np.asarray(allowed)
    if s.ndim != 2 or 0 in s.shape or not np.isfinite(s).all():
        raise ValueError("점수는 비어 있지 않은 유한 실수 행렬이어야 한다")
    if mask.dtype != np.bool_ or mask.shape != s.shape:
        raise ValueError("allowed는 점수와 같은 크기의 Boolean이어야 한다")
    active = np.ones(s.shape[0], dtype=bool) if active is None else np.asarray(active)
    if active.dtype != np.bool_ or active.shape != (s.shape[0],):
        raise ValueError("active는 질의별 Boolean이어야 한다")
    a = np.zeros_like(s)
    for i in range(s.shape[0]):
        if not active[i]:
            continue  # 패딩 질의: 확률분포를 만들지 않는 별도 계약이다.
        cols = np.flatnonzero(mask[i])
        if cols.size == 0:
            raise ValueError(f"유효 질의 {i}의 모든 키가 차단되었다")
        # 허용된 점수만 최대값·지수·분모에 참여한다.
        row = s[i, cols]
        with np.errstate(over="ignore", under="ignore"):
            weights = np.exp(row - row.max())
        a[i, cols] = weights / weights.sum()
    return a


def masked_attention(q, k, v, allowed, active=None):
    """S·A·O를 반환한다. Mask 정책은 호출자가 구성한다."""
    q, k, v = [np.asarray(x, dtype=np.float64) for x in (q, k, v)]
    if any(x.ndim != 2 or 0 in x.shape for x in (q, k, v)):
        raise ValueError("Q/K/V는 비어 있지 않은 2차원 배열이어야 한다")
    if q.shape[1] != k.shape[1] or k.shape[0] != v.shape[0]:
        raise ValueError("비교 폭 또는 키·값의 제공 위치 수가 다르다")
    if not all(np.isfinite(x).all() for x in (q, k, v)):
        raise ValueError("차단된 위치도 포함해 Q/K/V는 유한해야 한다")
    with np.errstate(over="ignore", invalid="ignore"):
        s = (q @ k.T) / np.sqrt(q.shape[1])
    a = masked_softmax(s, allowed, active)
    with np.errstate(over="ignore", invalid="ignore"):
        o = a @ v
    if not np.isfinite(o).all():
        raise ValueError("출력의 표현 범위를 벗어났다")
    return s, a, o
