"""위치 가산·점수 편향·인접 좌표 쌍 회전. CPU·단일 Head·행 배열."""
import numpy as np
from sources import matrix, project
from masking import masked_attention, masked_softmax


def positions(p, length):
    """배열 행과 대응하는 실제 정수 위치. 안전한 차/각도 계산 범위를 둔다."""
    a = np.asarray(p)
    if length <= 0 or a.shape != (length,) or a.dtype.kind not in "iu":
        raise ValueError("위치는 각 행에 대응하는 정수 벡터여야 한다")
    if any(abs(int(x)) > 2**31 - 1 for x in a):
        raise ValueError("교육용 위치 범위는 절댓값 2**31-1 이하이다")
    return a.astype(np.int64)


def frequencies(theta, pairs):
    """좌표 쌍마다 한 개의 유한 주파수, 단위는 rad/위치다."""
    t = np.asarray(theta, dtype=np.float64)
    if t.shape != (pairs,) or not np.isfinite(t).all():
        raise ValueError("각 좌표 쌍에 유한한 주파수 하나가 필요하다")
    return t


def sinusoidal(p, width, base=10000.):
    """0기반 좌표 (2r,2r+1)에 sin/cos를 배치한다. 여기서는 짝수 폭."""
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0 or width % 2:
        raise ValueError("이 구현의 Sinusoidal 폭은 양의 짝수여야 한다")
    if not np.isscalar(base) or not np.isfinite(base) or base <= 1:
        raise ValueError("base는 1보다 큰 유한 실수여야 한다")
    p = positions(p, len(p))
    omega = base ** (-2 * np.arange(width // 2, dtype=float) / width)
    angle = p[:, None] * omega[None, :]
    result = np.empty((len(p), width))
    result[:, 0::2], result[:, 1::2] = np.sin(angle), np.cos(angle)
    return result


def add_absolute(x, encoding):
    """가산 뒤의 같은 표현이 Q/K/V 모두에 사용될 수 있다."""
    x, e = matrix(x), matrix(encoding)
    if x.shape != e.shape:
        raise ValueError("내용과 위치 표현의 행/폭이 같아야 한다")
    with np.errstate(over="ignore", invalid="ignore"):
        return matrix(x + e)


def absolute_attention(h, z, eh, ez, wq, wk, wv, allowed, active=None):
    """각 출처에 위치를 더한 뒤 투영한다. Cross/Self 모두 사용 가능."""
    hp, zp = add_absolute(h, eh), add_absolute(z, ez)
    q, k, v = project(hp, wq), project(zp, wk), project(zp, wv)
    s, a, o = masked_attention(q, k, v, allowed, active)
    return q, k, v, s, a, o


def relative_bias(query_pos, key_pos, table):
    """delta=pQ-pK. 양수는 키가 과거, 음수는 키가 미래다."""
    qp, kp = positions(query_pos, len(query_pos)), positions(key_pos, len(key_pos))
    delta = qp[:, None] - kp[None, :]
    if not isinstance(table, dict) or not table:
        raise ValueError("명시적인 정수 상대 위치 편향 표가 필요하다")
    if any(not isinstance(k, (int, np.integer)) or isinstance(k, (bool, np.bool_))
           for k in table):
        raise ValueError("편향 표의 상대 위치는 정수여야 한다")
    if any(not np.isscalar(v) or not np.isfinite(v) for v in table.values()):
        raise ValueError("편향은 유한 스칼라여야 한다")
    if any(int(d) not in table for d in delta.flat):
        raise ValueError("사용한 상대 위치가 편향 표에 없다")
    return np.array([[table[int(d)] for d in row] for row in delta], dtype=float)


def biased_attention(q, k, v, query_pos, key_pos, table, allowed, active=None):
    """기존 scale/검사를 재사용하고, 편향을 scale 뒤 Softmax 전에 더한다."""
    s0, _, _ = masked_attention(q, k, v, allowed, active)
    bias = relative_bias(query_pos, key_pos, table)
    if bias.shape != s0.shape:
        raise ValueError("위치 목록과 Q/K의 행 수가 다르다")
    with np.errstate(over="ignore", invalid="ignore"):
        s = s0 + bias
    a = masked_softmax(s, allowed, active)
    with np.errstate(over="ignore", invalid="ignore"):
        o = matrix(a @ matrix(v))
    return s0, bias, s, a, o


def rope(x, p, theta):
    """(0,1),(2,3),…를 회전한다. 열벡터 R x의 좌표를 행에 저장한다."""
    x = matrix(x)
    if x.shape[1] % 2:
        raise ValueError("전체 회전 폭은 짝수여야 한다")
    p = positions(p, len(x))
    theta = frequencies(theta, x.shape[1] // 2)
    with np.errstate(over="ignore", invalid="ignore"):
        angle = p[:, None] * theta[None, :]
    if not np.isfinite(angle).all():
        raise ValueError("회전 각도의 표현 범위를 벗어났다")
    c, s = np.cos(angle), np.sin(angle)
    even, odd = x[:, 0::2], x[:, 1::2]
    out = np.empty_like(x)
    # 입력의 두 좌표를 동시에 참조하므로 제자리 갱신에 의한 오염이 없다.
    with np.errstate(over="ignore", invalid="ignore"):
        out[:, 0::2] = c * even - s * odd
        out[:, 1::2] = s * even + c * odd
    return matrix(out)


def rotary_attention(q, k, v, query_pos, key_pos, theta, allowed, active=None):
    """Q/K만 위치 회전하고, V와 허용 관계는 호출자가 제공한 것을 쓴다."""
    qr, kr = rope(q, query_pos, theta), rope(k, key_pos, theta)
    s, a, o = masked_attention(qr, kr, v, allowed, active)
    return qr, kr, s, a, o


def comparison_inputs():
    """본문의 인공 수치. 비교 투영은 세 번째 내용 좌표를 사용하지 않는다."""
    x = np.array([[1., 0., 2.], [1., 0., 5.], [1., 0., 8.]])
    wq = np.array([[1., 0.], [0., 1.], [0., 0.]])
    wk, wv = np.sqrt(2.) * np.log(2.) * wq, np.array([[0.], [0.], [1.]])
    e = np.array([[0., 0., 0.], [0., 1., 0.], [1., 0., 0.]])
    p = np.array([0, 1, 2])
    table = {-2: -np.log(2.), -1: np.log(2.), 0: 0.,
             1: np.log(3.), 2: -np.log(3.)}
    return x, wq, wk, wv, e, p, table
