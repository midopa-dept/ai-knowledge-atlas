"""정보 출처와 접근 정책을 드러내는 단일 시퀀스 Post-LN 예제."""
import numpy as np
from block import real_array, residual, layer_norm, feed_forward, post_ln
from sources import cross_attention, project
from masking import causal_allowed


def valid_vector(x, n):
    """위치별 Boolean. 숫자 0/1을 자동 허용하지 않는다."""
    a = np.asarray(x)
    if a.dtype != np.bool_ or a.shape != (n,):
        raise ValueError("위치별 Boolean 벡터가 필요하다")
    return a


def full_allowed(query_count, key_valid, restriction=None):
    """행=요청, 열=제공. 완성 입력 또는 Cross의 허용 키 관계."""
    if isinstance(query_count, bool) or not isinstance(query_count, int) or query_count < 1:
        raise ValueError("요청 수는 양의 정수여야 한다")
    raw = np.asarray(key_valid)
    if raw.ndim != 1 or raw.size == 0:
        raise ValueError("제공 위치가 필요하다")
    valid = valid_vector(raw, len(raw))
    allowed = np.broadcast_to(valid, (query_count, len(valid))).copy()
    if restriction is not None:
        r = np.asarray(restriction)
        if r.dtype != np.bool_ or r.shape != allowed.shape:
            raise ValueError("접근 제한은 같은 shape의 Boolean이어야 한다")
        allowed &= r
    return allowed


def shifted_inputs(targets, bos):
    """비어 있지 않은 정수 Target 벡터에서 [BOS,y1,...]을 만든다."""
    t = np.asarray(targets)
    if t.ndim != 1 or t.size == 0 or t.dtype.kind not in "iu":
        raise ValueError("Target은 비어 있지 않은 정수 벡터여야 한다")
    if isinstance(bos, bool) or not isinstance(bos, (int, np.integer)):
        raise ValueError("BOS는 정수 Token 식별자여야 한다")
    # dtype 축소로 BOS가 변형되는 것을 막는다.
    if not np.iinfo(t.dtype).min <= bos <= np.iinfo(t.dtype).max:
        raise ValueError("BOS가 Target dtype의 표현 범위를 벗어났다")
    return np.concatenate((np.array([bos], dtype=t.dtype), t[:-1])), t.copy()


def check_shift(inputs, targets, bos):
    """데이터 이동 계약만 검사한다. 표현 오염까지 증명하지 않는다."""
    expected, _ = shifted_inputs(targets, bos)
    i = np.asarray(inputs)
    if i.dtype.kind not in "iu" or i.shape != expected.shape or not np.array_equal(i, expected):
        raise ValueError("입력은 [BOS, Target[:-1]]이어야 한다")
    return True


def decoder_post(d, e, self_weights, cross_weights, ffn, norms,
                 self_mask, cross_mask, active=None):
    """D:(m,dD), E:(n,dE). Self→Cross→FFN, 각 합 뒤 LN."""
    d, e = real_array(d, 2), real_array(e, 2)
    if len(norms) != 3:
        raise ValueError("Decoder에는 세 LN 매개변수가 필요하다")
    sq, sk, sv, so = [real_array(w, 2) for w in self_weights]
    cq, ck, cv, co = [real_array(w, 2) for w in cross_weights]
    # 출처가 같은 Self와 출처가 다른 Cross를 별도로 호출한다.
    st = cross_attention(d, d, sq, sk, sv, self_mask, active)
    sm = project(st[-1], so)
    r1 = residual(d, sm)
    h, n1 = layer_norm(r1, *norms[0])
    ct = cross_attention(h, e, cq, ck, cv, cross_mask, active)
    cm = project(ct[-1], co)
    r2 = residual(h, cm)
    u, n2 = layer_norm(r2, *norms[1])
    f, ft = feed_forward(u, *ffn)
    r3 = residual(u, f)
    y, n3 = layer_norm(r3, *norms[2])
    trace = dict(self=dict(zip(("q", "k", "v", "s", "a", "o"), st)),
                 self_update=sm, r1=r1, norm1=n1, h=h,
                 cross=dict(zip(("q", "k", "v", "s", "a", "o"), ct)),
                 cross_update=cm, r2=r2, norm2=n2, u=u,
                 ffn_linear=ft["linear"], activated=ft["activated"],
                 ffn=f, r3=r3, norm3=n3, y=y)
    return y, trace


def parameters(d=3):
    """손계산용 한 Head: 비교 폭1, 값/반환 폭d, 비영 FFN."""
    q = np.zeros((d, 1)); q[0, 0] = 1.
    k = np.log(2.) * q
    v = np.eye(d); wo = .5 * np.eye(d)
    ffn = (np.eye(d), np.zeros(d), .25*np.eye(d), np.zeros(d))
    ln = (np.ones(d), np.zeros(d), .1)
    return (q, k, v), wo, ffn, ln


def integrated(source=None, prefix=None):
    """원문3행→Encoder E3×3, Prefix2행→Decoder Y2×3."""
    content = np.array([[1., 0., 1.], [0., 1., 1.], [1., 1., 0.]])
    position = np.array([[0., 0., 1.], [0., 1., 0.], [1., 0., 0.]])
    z = content + position if source is None else real_array(source, 2)
    d = np.array([[1., 0., 1.], [0., 1., 2.]]) if prefix is None else real_array(prefix, 2)
    p, wo, ffn, ln = parameters()
    enc_mask = full_allowed(len(z), np.ones(len(z), dtype=bool))
    e, et = post_ln(z, [p], wo, ffn, ln, ln, [enc_mask])
    self_mask = causal_allowed(np.arange(len(d)), np.arange(len(d)), np.ones(len(d), dtype=bool))
    cross_mask = full_allowed(len(d), np.ones(len(e), dtype=bool))
    wq = np.array([[1., 0.], [0., 1.], [0., 0.]])
    wk = np.sqrt(2.) * np.array([[np.log(2.), 0.], [0., np.log(3.)], [0., 0.]])
    wv = np.array([[1., 0.], [0., 1.], [1., -1.]])
    cw = (wq, wk, wv, np.array([[1., 0., .5], [0., 1., -.5]]))
    y, dt = decoder_post(d, e, (*p, wo), cw, ffn, [ln]*3, self_mask, cross_mask)
    readout = np.array([[1., 0., -1.], [0., 1., 0.], [.5, 0., 1.]])
    logits = y[-1] @ readout
    return dict(content=content, position=position, z=z, encoder=et, e=e,
                d=d, decoder=dt, logits=logits, self_mask=self_mask, cross_mask=cross_mask)


def exact_cross():
    """Encoder 출력 E가 주어진 축약 예제. 원문 Embedding이 아니다."""
    h = np.array([[1., 0., 2.], [0., 1., 1.]])
    e = np.array([[1., 0.], [0., 2.], [1., 1.]])
    wq = np.array([[1., 0.], [0., 1.], [0., 0.]])
    wk = np.sqrt(2.) * np.log(2.) * np.eye(2)
    wv = np.diag([2., 1.])
    mask = full_allowed(2, np.ones(3, dtype=bool))
    return h, e, wq, wk, wv, mask
