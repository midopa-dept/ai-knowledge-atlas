"""입력 출처를 보존하는 단일 Head·2차원 Self/Cross Attention."""
import numpy as np
from masking import masked_attention


def matrix(x):
    """비어 있지 않은 유한 실수 행렬로 변환한다."""
    a = np.asarray(x, dtype=np.float64)
    if a.ndim != 2 or 0 in a.shape or not np.isfinite(a).all():
        raise ValueError("입력은 비어 있지 않은 유한 행렬이어야 한다")
    return a


def project(x, w):
    """행의 개수는 유지하고 마지막 좌표 축을 투영한다."""
    x, w = matrix(x), matrix(w)
    if x.shape[1] != w.shape[0]:
        raise ValueError("입력 폭과 투영 행렬의 첫 축이 다르다")
    with np.errstate(over="ignore", invalid="ignore"):
        result = x @ w
    return matrix(result)


def cross_attention(h, z, wq, wk, wv, allowed=None, active=None):
    """H가 요청하고 Z가 제공한다. 입력 배열은 직접 변경하지 않는다."""
    h, z = matrix(h), matrix(z)
    q, k, v = project(h, wq), project(z, wk), project(z, wv)
    if allowed is None:
        allowed = np.ones((len(h), len(z)), dtype=bool)
    s, a, o = masked_attention(q, k, v, allowed, active)
    return q, k, v, s, a, o


def self_attention(x, wq, wk, wv, allowed=None, active=None):
    """세 출처에 같은 X를 배정한다."""
    return cross_attention(x, x, wq, wk, wv, allowed, active)


def example_inputs():
    """본문의 교육용 배열. 학습된 벡터가 아니다."""
    x = np.array([[1., 0.], [0., 1.], [1., 1.]])
    h = np.array([[1., 0., 1.], [0., 1., 1.]])
    wq = np.eye(2)
    wk = np.sqrt(2.) * np.diag(np.log([2., 3.]))
    wv = np.diag([2., 3.])
    uq = np.array([[1., 0.], [0., 1.], [0., 0.]])
    r = np.array([[1., 0., 1.], [0., 1., -1.]])
    return x, h, wq, wk, wv, uq, r
