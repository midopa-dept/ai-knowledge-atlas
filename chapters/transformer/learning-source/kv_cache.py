"""두 레이어 Decoder의 전체·증분 계산. 기본 Cache에는 K/V만 저장한다."""
from copy import deepcopy
import hashlib
import json
import numpy as np


def norm(u, gamma, beta, eps):
    """각 행의 특징 좌표만 정규화한다. Working의 좁은 N 인터페이스다."""
    mean = u.mean(axis=-1, keepdims=True)
    variance = ((u - mean) ** 2).mean(axis=-1, keepdims=True)
    return (u - mean) / np.sqrt(variance + eps) * gamma + beta


def feed(u, b1, b2, bias1, bias2):
    """Working의 F 인터페이스. 입력 선택과 Residual 덧셈은 호출자가 한다."""
    activation = np.maximum(u @ b1 + bias1, 0)
    return activation, activation @ b2 + bias2


def positions_mask(query_positions, key_positions, valid):
    """배열 행 번호가 아니라 원래 위치와 Key 유효성으로 허용 관계를 만든다."""
    return (np.asarray(key_positions)[None, :] <=
            np.asarray(query_positions)[:, None]) & np.asarray(valid)[None, :]


def rotate(x, positions, theta):
    """행벡터를 좌표쌍별 반시계로 회전한다. V에는 적용하지 않는다."""
    if x.shape[1] % 2:
        raise ValueError("RoPE 비교 폭은 짝수여야 한다")
    angle = np.asarray(positions)[:, None] * np.asarray(theta)[None, :]
    c, s = np.cos(angle), np.sin(angle)
    out = x.copy()
    out[:, 0::2] = x[:, 0::2] * c - x[:, 1::2] * s
    out[:, 1::2] = x[:, 0::2] * s + x[:, 1::2] * c
    return out


def attention(q, k, v, allowed, active):
    """비활성 요청은 집계0, 활성 요청의 빈 허용 집합은 오류로 처리한다."""
    if allowed.dtype != bool or allowed.shape != (len(q), len(k)):
        raise ValueError("Mask의 축 또는 Boolean dtype이 다르다")
    if np.any(np.asarray(active) & ~allowed.any(axis=1)):
        raise ValueError("활성 요청에 허용 Key가 없다")
    scores = q @ k.T / np.sqrt(q.shape[1])
    weights = np.zeros_like(scores)
    for i in range(len(q)):
        if active[i]:
            row = scores[i, allowed[i]]
            exp = np.exp(row - row.max())
            weights[i, allowed[i]] = exp / exp.sum()
    return scores, weights, weights @ v


def layer(h, pos, block, old=None, allowed=None, active=None):
    """새 표현의 투영→과거 결합→Attention→두 Residual을 순서대로 계산한다."""
    active = np.ones(len(h), dtype=bool) if active is None else active
    z = norm(h, block["g1"], block["n1"], block["eps"])
    keys_pos = list(pos) if old is None else old["positions"] + list(pos)
    valid = list(active) if old is None else old["valid"] + list(active)
    if allowed is None:
        allowed = positions_mask(pos, keys_pos, valid)
    records, cache_heads = [], []
    for r, head in enumerate(block["heads"]):
        q, raw_k, v = [z @ head[name] for name in ("q", "k", "v")]
        k = raw_k
        if "theta" in head:
            q, k = rotate(q, pos, head["theta"]), rotate(k, pos, head["theta"])
        old_head = None if old is None else old["heads"][r]
        all_k = k if old_head is None else np.concatenate((old_head["k"], k))
        all_v = v if old_head is None else np.concatenate((old_head["v"], v))
        scores, weights, out = attention(q, all_k, all_v, allowed, active)
        records.append(dict(q=q, raw_k=raw_k, k=k, v=v, scores=scores,
                            weights=weights, out=out))
        cache_heads.append(dict(head=r, k=all_k.copy(), v=all_v.copy()))
    joined = np.concatenate([item["out"] for item in records], axis=1)
    mixed = joined @ block["wo"]
    residual = h + mixed
    u = norm(residual, block["g2"], block["n2"], block["eps"])
    activation, f = feed(u, block["b1"], block["b2"], block["bias1"], block["bias2"])
    result = residual + f
    cache = dict(positions=keys_pos, valid=valid, heads=cache_heads)
    trace = dict(h=h.copy(), z=z, heads=records, joined=joined, mixed=mixed,
                 residual=residual, u=u, activation=activation, f=f, result=result)
    return result, cache, trace


def serial(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer, np.bool_)):
        return value.item()
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(item) for item in value]
    return value


def digest(value):
    data = json.dumps(serial(value), sort_keys=True, allow_nan=False).encode()
    return hashlib.sha256(data).hexdigest()


def validate_model(model):
    """이 소스는 두 개 이상 레이어와 Head별 독립된 폭을 허용한다."""
    width = model["embedding"].shape[1]
    if len(model["blocks"]) < 2:
        raise ValueError("이 실습에는 두 개 이상 레이어가 필요하다")
    # 수치 계약을 확인하고 NaN·복소수·Residual 폭 불일치를 거부한다.
    for b in model["blocks"]:
        if b["eps"] <= 0 or not np.isfinite(b["eps"]):
            raise ValueError("epsilon은 양의 유한값이어야 한다")
        total = 0
        for head in b["heads"]:
            if head["q"].shape != head["k"].shape or head["q"].shape[0] != width:
                raise ValueError("Q/K 투영 폭 불일치")
            if head["v"].shape[0] != width or head["q"].shape[1] < 1:
                raise ValueError("Head 입력/비교 폭 불일치")
            total += head["v"].shape[1]
            if "theta" in head and (head["q"].shape[1] != 2 * len(head["theta"])):
                raise ValueError("RoPE 좌표쌍과 주파수 불일치")
        if b["wo"].shape != (total, width):
            raise ValueError("출력 투영과 Residual 폭 불일치")
        for name in ("g1", "n1", "g2", "n2", "bias2"):
            if b[name].shape != (width,):
                raise ValueError("정규화/FFN 출력 폭 불일치")
        if b["b1"].shape[0] != width or b["b2"].shape != (b["b1"].shape[1], width):
            raise ValueError("FFN 투영 폭 불일치")
    if model["readout"].shape[0] != width:
        raise ValueError("Readout 입력 폭 불일치")
    def check(x):
        if isinstance(x, dict):
            for y in x.values(): check(y)
        elif isinstance(x, list):
            for y in x: check(y)
        elif isinstance(x, np.ndarray) and (np.iscomplexobj(x) or not np.isfinite(x).all()):
            raise ValueError("모델에 비실수/비유한값이 있다")
    check(model)


def initial(model, tokens, pos):
    validate_model(model)
    tok, p = np.asarray(tokens), np.asarray(pos)
    if tok.ndim != 1 or p.ndim != 1 or len(tok) != len(p) or not len(tok):
        raise ValueError("Token/위치는 같은 길이의 비어 있지 않은 1차원 배열")
    if tok.dtype.kind not in "iu" or p.dtype.kind not in "iu":
        raise ValueError("Token/위치에는 정수가 필요하다")
    if np.any(tok < 0) or np.any(tok >= len(model["embedding"])) or np.any(p < 0):
        raise ValueError("Token/위치 범위 밖")
    if len(set(pos)) != len(pos):
        raise ValueError("이 실습에서는 원래 위치가 서로 달라야 한다")
    return model["embedding"][tok] + p[:, None] * model["position_step"]


def full_prefix(model, tokens, pos, allowed=None, active=None):
    """모든 입력 위치를 처음부터 계산해 레이어별 K/V와 전 중간값을 반환한다."""
    h = initial(model, tokens, pos)
    caches, traces = [], []
    for index, b in enumerate(model["blocks"]):
        mask = None if allowed is None else allowed[index]
        h, c, trace = layer(h, pos, b, allowed=mask, active=active)
        c["layer"] = index
        caches.append(c); traces.append(trace)
    contract = dict(model=digest(model), tokens=list(tokens), positions=list(pos),
                    policy=digest(allowed), active=serial(active))
    cache = dict(layers=caches, contract=contract)
    cache["seal"] = digest(cache)
    return h, h @ model["readout"], cache, traces


def validate_cache(model, cache, prefix, old_pos):
    """계약 변경은 재평가를 요구한다. 항목별 최소 재계산 판정과 다른 보수적 검사다."""
    core = {key: value for key, value in cache.items() if key != "seal"}
    if digest(core) != cache["seal"]:
        raise ValueError("Cache의 Layer/Head/위치/K-V 대응 또는 값이 변경됐다")
    con = cache["contract"]
    if con["model"] != digest(model) or con["tokens"] != list(prefix) or con["positions"] != list(old_pos):
        raise ValueError("모델/Prefix/위치 계약 변경. 항목별 재평가가 필요하다")
    if con["policy"] != digest(None) or con["active"] is not None:
        raise ValueError("이 증분 인터페이스는 기본 Causal 활성 Prefix만 받는다")
    if len(cache["layers"]) != len(model["blocks"]):
        raise ValueError("레이어 수 불일치")
    for index, (b, c) in enumerate(zip(model["blocks"], cache["layers"])):
        if c["layer"] != index or c["positions"] != list(old_pos):
            raise ValueError("레이어/원래 위치 불일치")
        if len(c["heads"]) != len(b["heads"]):
            raise ValueError("Head 수 불일치")
        for r, (head, stored) in enumerate(zip(b["heads"], c["heads"])):
            if stored["head"] != r or stored["k"].shape != (len(prefix), head["k"].shape[1]):
                raise ValueError("Head/Key shape 불일치")
            if stored["v"].shape != (len(prefix), head["v"].shape[1]):
                raise ValueError("Value shape 불일치")


def incremental(model, prefix, old_pos, token, position, cache):
    """과거 K/V를 재사용하고 새 한 위치만 레이어마다 순서대로 전달한다."""
    validate_cache(model, cache, prefix, old_pos)
    if old_pos and position <= max(old_pos):
        raise ValueError("새 위치는 기존 Causal Prefix 뒤에 있어야 한다")
    h = initial(model, [token], [position])
    caches, traces = [], []
    for index, b in enumerate(model["blocks"]):
        h, c, trace = layer(h, [position], b, old=cache["layers"][index])
        c["layer"] = index
        caches.append(c); traces.append(trace)
    contract = dict(model=digest(model), tokens=list(prefix) + [token],
                    positions=list(old_pos) + [position], policy=digest(None), active=None)
    updated = dict(layers=caches, contract=contract)
    updated["seal"] = digest(updated)
    return h, h @ model["readout"], updated, traces


def example_model():
    """기존 설계의 인공 수치를 유지한다. 위치 가산·epsilon1은 교육용 선택이다."""
    eye = np.eye(2)
    heads = [dict(q=eye[:, :1], k=eye[:, :1], v=2 * eye[:, :1]),
             dict(q=eye[:, 1:], k=eye[:, 1:], v=4 * eye[:, 1:])]
    b = dict(heads=heads, wo=np.array([[1., 1.], [0., 1.]]),
             g1=np.ones(2), n1=np.zeros(2), g2=np.ones(2), n2=np.zeros(2),
             eps=1., b1=np.diag([1., -1.]), b2=np.diag([.5, .25]),
             bias1=np.zeros(2), bias2=np.array([.1, -.1]))
    return dict(embedding=np.array([[1., 0.], [0., 1.], [1., 1.], [2., 0.]]),
                position_step=np.array([.1, 0.]), blocks=[deepcopy(b), deepcopy(b)],
                readout=np.array([[1., 0., -1.], [0., 1., 1.]]))


def transfer_model():
    """새 통합 과제: Head 비교 폭2/1·값 폭1/2와 서로 다른 레이어를 사용한다."""
    m = example_model()
    m["embedding"] = np.array([[0., 1.], [1., -1.], [-1., .5], [1., 1.]])
    m["position_step"] = np.array([0., .2])
    for i, b in enumerate(m["blocks"]):
        b["heads"] = [dict(q=np.array([[1., .5], [0., 1.]]),
                            k=np.array([[.5, 0.], [1., 1.]]), v=np.array([[1.], [-1.]])),
                      dict(q=np.array([[.5], [1.]]), k=np.array([[1.], [-.5]]),
                           v=np.array([[1., 0.], [.5, 1.]]))]
        b["wo"] = np.array([[1., 0.], [0., .5], [.5, 1.]]) * (1 if i == 0 else .7)
        b["b1"] = np.array([[1., 0., -1.], [0., 1., 1.]])
        b["b2"] = np.array([[.2, 0.], [0., .3], [-.1, .1]])
        b["bias1"] = np.zeros(3)
        b["bias2"] = np.array([0., .05])
        b["g1"] = np.array([1., .8]) if i == 0 else np.array([.9, 1.])
    return m


def rope_model():
    m = transfer_model()
    m["position_step"] = np.zeros(2)
    for b in m["blocks"]:
        b["heads"] = [b["heads"][0]]
        b["heads"][0]["theta"] = np.array([.7])
        b["wo"] = np.array([[1., -.5]])
    return m
