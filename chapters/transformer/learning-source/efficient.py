"""비용·연결·정규화의 교육용 CPU 구현. 투영/특징 생성은 입력 계약 밖이다."""
import numpy as np


def matrix(x, name):
    """행은 위치, 열은 좌표다. 빈 폭과 비유한 값은 계산 전에 거부한다."""
    a = np.array(x, dtype=np.float64, copy=True)
    if a.ndim != 2 or min(a.shape) < 1 or not np.isfinite(a).all():
        raise ValueError(f'{name}: 유한한 비어 있지 않은 행렬 필요')
    return a


def positions(p):
    a = np.asarray(p)
    if a.ndim != 1 or len(a) < 1 or a.dtype.kind not in 'iu' or len(set(a.tolist())) != len(a):
        raise ValueError('원위치는 중복 없는 정수 벡터여야 한다')
    if any(int(x)<1 or int(x)>np.iinfo(np.int64).max for x in a):
        raise ValueError('원위치는 signed int64 범위의 양의 정수여야 한다')
    return a.astype(np.int64, copy=True)


def causal_mask(query_positions, key_positions, width=None):
    """원위치를 1부터 센다. 배열이 재배열돼도 원위치의 허용 관계를 쓴다."""
    qp, kp = positions(query_positions), positions(key_positions)
    if width is not None and (type(width) is not int or width < 1):
        raise ValueError('현재 위치를 포함하는 양의 정수 폭 필요')
    allowed = kp[None, :] <= qp[:, None]
    if width is not None:
        # Python 정수로 경계를 만들어 unsigned wrap와 signed overflow를 피한다.
        lower = np.array([max(1, int(i)-width+1) for i in qp], dtype=np.int64)
        allowed &= kp[None, :] >= lower[:, None]
    return allowed


def checked_mask(mask, shape):
    b = np.asarray(mask)
    if b.dtype != np.bool_ or b.shape != shape or not b.any(axis=1).all():
        raise ValueError('정확한 shape의 Boolean Mask와 행별 허용 Key 필요')
    return b.copy()


def sparse_attention(q, k, v, mask):
    """허용 쌍만 점수 계산. 반환 A는 관찰용 Dense 배열이며 실무 희소 저장이 아니다."""
    q, k, v = matrix(q, 'Q'), matrix(k, 'K'), matrix(v, 'V')
    if q.shape[1] != k.shape[1] or len(k) != len(v):
        raise ValueError('비교 폭 및 K/V 제공 행 수 불일치')
    b = checked_mask(mask, (len(q), len(k)))
    scores = np.full(b.shape, -np.inf)
    weights = np.zeros(b.shape)
    output = np.empty((len(q), v.shape[1]))
    for i in range(len(q)):
        js = np.flatnonzero(b[i])  # 배열 열 번호이며 원위치 자체는 아니다.
        s = k[js] @ q[i] / np.sqrt(q.shape[1])
        if not np.isfinite(s).all():
            raise ValueError('점수 산술의 비유한 결과')
        e = np.exp(s - s.max())
        a = e / e.sum()  # 금지 열을 뺀 뒤 새로운 분모로 정규화한다.
        scores[i, js], weights[i, js] = s, a
        output[i] = a @ v[js]
    return scores, weights, matrix(output, 'Softmax 출력')


def full_causal_attention(q, k, v, query_positions, key_positions):
    return sparse_attention(q, k, v, causal_mask(query_positions, key_positions))


def reachability(masks):
    """각 층에서 가능한 초기 입력 의존 집합. 실제 비영 기여를 보장하지 않는다."""
    first = np.asarray(masks[0])
    if first.ndim != 2 or first.shape[0] != first.shape[1]:
        raise ValueError('동일 위치 집합의 정사각 Mask 필요')
    n = len(first)
    previous = [{i + 1} for i in range(n)]
    history = [previous]
    for mask in masks:
        b = checked_mask(mask, (n, n))
        current = []
        for i in range(n):
            # Q_i의 생성원 및 Residual의 자기 경로를 포함한다.
            deps = set(previous[i])
            for j in np.flatnonzero(b[i]):
                deps.update(previous[j])
            current.append(deps)
        history.append(current)
        previous = current  # 이전 층 전체를 읽은 뒤 갱신한다.
    return history


def minimum_steps(mask, source, target):
    """정적 그래프에서 제공 source→요청 target의 최단 Attention 단계 수."""
    b = np.asarray(mask)
    b = checked_mask(b, b.shape)
    if b.shape[0] != b.shape[1] or not 1 <= source <= len(b) or not 1 <= target <= len(b):
        raise ValueError('정사각 그래프와 유효한 원위치 필요')
    reached = {source}
    for step in range(len(b) + 1):
        if target in reached:
            return step
        reached = reached | {i + 1 for i in range(len(b))
                             if any(b[i, j - 1] for j in reached)}
    return None


def local_global_mask(n=5, width=2, global_position=3):
    """교육용 Causal global: g는 자기 과거를 읽고 현재/미래 요청만 g를 읽는다."""
    if (type(n) is not int or n < 1 or type(global_position) is not int
            or not 1 <= global_position <= n):
        raise ValueError('길이와 global 원위치 오류')
    p = np.arange(1, n + 1)
    b = causal_mask(p, p, width)
    b[global_position - 1, :global_position] = True
    b[global_position - 1:, global_position - 1] = True
    return b


def feature_inputs(qf, kf, v):
    """좌표별 비음수를 충분조건으로 택한다. 일반 Kernel의 필요조건은 더 약하다."""
    qf, kf, v = matrix(qf, 'Query 특징'), matrix(kf, 'Key 특징'), matrix(v, 'V')
    if qf.shape[1] != kf.shape[1] or len(kf) != len(v):
        raise ValueError('특징 폭 또는 제공 길이 불일치')
    if (qf < 0).any() or (kf < 0).any():
        raise ValueError('이 구현의 특징 계약은 좌표별 비음수다')
    return qf, kf, v


def positive_denominator(d):
    if not np.isfinite(d).all() or (d <= 0).any():
        raise ValueError('유한한 양의 Kernel 분모 필요')


def kernel_direct(qf, kf, v, mask=None):
    qf, kf, v = feature_inputs(qf, kf, v)
    weights = qf @ kf.T  # 지수를 취하지 않은 특징 내적이다.
    if mask is not None:
        weights = np.where(checked_mask(mask, weights.shape), weights, 0.)
    d = weights.sum(axis=1)
    positive_denominator(d)
    a = weights / d[:, None]
    return weights, a, matrix(a @ v, '직접 Kernel 출력')


def kernel_factorized(qf, kf, v):
    qf, kf, v = feature_inputs(qf, kf, v)
    state = matrix(kf.T @ v, 'Kernel 누적 상태')  # (r,n)@(n,d_v) -> (r,d_v)
    z = kf.sum(axis=0)  # Key의 행(제공 위치)을 합하고 특징 좌표는 남긴다.
    d = qf @ z
    positive_denominator(d)
    return state, z, matrix((qf @ state) / d[:, None], '인자 Kernel 출력')


def kernel_prefix(qf, kf, v):
    qf, kf, v = feature_inputs(qf, kf, v)
    if len(qf) != len(kf):
        raise ValueError('Prefix 계산은 같은 순서의 Query/Key 행이 필요하다')
    state = np.zeros((qf.shape[1], v.shape[1]))
    z = np.zeros(qf.shape[1])
    outputs, states = [], []
    for i in range(len(qf)):
        # 현재 입력을 읽은 뒤 현재 K/V를 추가하고 그 다음 현재 요청을 계산한다.
        state = matrix(state + np.outer(kf[i], v[i]), 'Prefix 누적 상태')
        z = z + kf[i]
        d = qf[i] @ z
        positive_denominator(np.asarray(d))
        outputs.append(qf[i] @ state / d)
        states.append((state.copy(), z.copy()))
    return states, matrix(outputs, 'Prefix 출력')


def interaction_cost(n, dk, dv, width, r):
    """곱셈만 센다. scale/division/지수/덧셈/특징 생성/투영/출력 저장은 제외."""
    if any(type(x) is not int or x < 1 for x in (n, dk, dv, width, r)):
        raise ValueError('모든 크기는 양의 정수여야 한다')
    m = min(n, width)
    full, local = n * (n + 1) // 2, n * m - m * (m - 1) // 2
    return {'full_pairs': full, 'local_pairs': local, 'dense_cells': n*n,
            'full_multiplications': full*(dk+dv),
            'local_multiplications': local*(dk+dv),
            'factor_multiplications': 2*n*r*dv+n*r,
            'state_scalars': r*dv+r, 'kv_scalars': n*(dk+dv)}
