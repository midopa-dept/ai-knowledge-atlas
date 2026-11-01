"""마지막 특징 축 LN/FFN과 단일 시퀀스 Transformer 블록. 입력 비변경."""
import numpy as np
from heads import multi_head


def real_array(x, ndim=None):
    """비어 있지 않은 유한 실수 float64 배열. 복소수는 허용하지 않는다."""
    raw = np.asarray(x)
    if raw.dtype.kind not in "iuf" or raw.size == 0:
        raise ValueError("비어 있지 않은 실수 배열이 필요하다")
    a = np.asarray(raw, dtype=np.float64)
    if not np.isfinite(a).all() or (ndim is not None and a.ndim != ndim):
        raise ValueError("유한 실수와 올바른 축 수가 필요하다")
    return a


def layer_norm(x, gamma, beta, epsilon=1e-5):
    """(..., d) → 같은 shape. 각 마지막 축만 평균/분산, ddof=0."""
    x = real_array(x)
    if x.ndim < 1 or 0 in x.shape:
        raise ValueError("마지막 특징 축이 필요하다")
    gamma, beta = real_array(gamma, 1), real_array(beta, 1)
    if gamma.shape != (x.shape[-1],) or beta.shape != gamma.shape:
        raise ValueError("gamma/beta는 특징 폭의 벡터여야 한다")
    e = real_array(epsilon, 0)
    if e <= 0:
        raise ValueError("epsilon은 양의 유한 스칼라여야 한다")
    # keepdims로 각 행/배치의 통계가 해당 특징 좌표에만 방송된다.
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        mean = x.mean(axis=-1, keepdims=True)
        centered = x - mean
        variance = (centered * centered).mean(axis=-1, keepdims=True)
        normalized = centered / np.sqrt(variance + e)
        output = normalized * gamma + beta
    for a in (mean, variance, normalized, output):
        real_array(a)
    return output, dict(mean=mean, variance=variance, normalized=normalized)


def feed_forward(x, w1, b1, w2, b2):
    """(..., d) → (..., d). 공유 매개변수·ReLU·위치 간 직접 혼합 없음."""
    x = real_array(x)
    w1, w2 = real_array(w1, 2), real_array(w2, 2)
    b1, b2 = real_array(b1, 1), real_array(b2, 1)
    if x.ndim < 1 or 0 in x.shape:
        raise ValueError("특징 축이 필요하다")
    d = x.shape[-1]
    if w1.shape[0] != d or b1.shape != (w1.shape[1],):
        raise ValueError("첫 변환의 폭이 다르다")
    if w2.shape != (w1.shape[1], d) or b2.shape != (d,):
        raise ValueError("둘째 변환은 모델 폭으로 반환해야 한다")
    with np.errstate(over="ignore", invalid="ignore"):
        linear = x @ w1 + b1
        activated = np.maximum(linear, 0.)
        output = activated @ w2 + b2
    for a in (linear, activated, output):
        real_array(a)
    return output, dict(linear=linear, activated=activated)


def residual(x, update):
    """방송을 허용하지 않고 대응 위치·좌표끼리 더한다."""
    x, update = real_array(x), real_array(update)
    if x.shape != update.shape:
        raise ValueError("Residual 두 배열의 shape가 같아야 한다")
    with np.errstate(over="ignore", invalid="ignore"):
        y = x + update
    return real_array(y)


def transformer_block(x, projections, wo, ffn, ln1, ln2,
                      mode="post", masks=None, active=None):
    """X:(n,d). 두 LN은 (gamma,beta,epsilon), FFN은 (W1,b1,W2,b2)."""
    x = real_array(x, 2)
    if mode not in ("post", "pre"):
        raise ValueError("mode는 post 또는 pre다")
    # 기존 MHA는 단일 시퀀스만 지원한다. Batch는 외부 반복이 필요하다.
    projections = [tuple(real_array(w, 2) for w in head)
                   for head in projections]
    wo = real_array(wo, 2)
    attention_input = x
    if mode == "pre":
        attention_input, norm1 = layer_norm(x, *ln1)
    heads, concat, attention = multi_head(
        attention_input, attention_input, projections, wo, masks, active)
    first_sum = residual(x, attention)
    if mode == "post":
        u, norm1 = layer_norm(first_sum, *ln1)
        ffn_input = u
    else:
        u = first_sum
        ffn_input, norm2 = layer_norm(u, *ln2)
    update, ftrace = feed_forward(ffn_input, *ffn)
    second_sum = residual(u, update)
    if mode == "post":
        y, norm2 = layer_norm(second_sum, *ln2)
    else:
        y = second_sum
    trace = dict(attention_input=attention_input.copy(), heads=heads,
                 concat=concat, attention=attention, first_sum=first_sum,
                 norm1=norm1, u=u, ffn_input=ffn_input,
                 ffn_linear=ftrace["linear"], activated=ftrace["activated"],
                 ffn=update, second_sum=second_sum, norm2=norm2, y=y)
    return y, trace


def post_ln(x, projections, wo, ffn, ln1, ln2, masks=None, active=None):
    """LN(X+MHA(X)) → LN(U+FFN(U))."""
    return transformer_block(x, projections, wo, ffn, ln1, ln2,
                             "post", masks, active)


def pre_ln(x, projections, wo, ffn, ln1, ln2, masks=None, active=None):
    """X+MHA(LN(X)) → U+FFN(LN(U)). 마지막의 추가 LN은 없다."""
    return transformer_block(x, projections, wo, ffn, ln1, ln2,
                             "pre", masks, active)


def example_inputs():
    """본문의 두 위치·폭3·두 Head·중간 폭4 교육용 매개변수."""
    x = np.array([[1., 0., 2.], [0., 2., 1.]])
    h1 = (np.array([[1.], [0.], [0.]]),
          np.array([[np.log(2.)], [0.], [0.]]),
          np.array([[0.], [0.], [1.]]))
    h2 = (np.array([[0.], [1.], [0.]]),
          np.array([[0.], [np.log(2.)], [0.]]),
          np.array([[1.], [0.], [0.]]))
    wo = np.array([[1., 0., 1.], [0., 1., -1.]])
    w1 = np.array([[1., 0., -1., 1.],
                   [0., 1., 1., -1.], [1., -1., 0., 0.]])
    b1 = np.array([0., .5, 0., -.5])
    w2 = np.array([[.5, 0., -.5], [0., .5, .5],
                   [.5, -.5, 0.], [-.5, 0., .5]])
    b2 = np.array([.1, -.2, .3])
    ln = (np.ones(3), np.zeros(3), .01)
    return x, [h1, h2], wo, (w1, b1, w2, b2), ln, ln
