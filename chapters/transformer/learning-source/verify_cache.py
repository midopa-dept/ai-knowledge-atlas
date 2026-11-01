"""전 중간값 독립 검산·생성원 변경·고의 Cache 오류를 CPU에서 검사한다."""
from copy import deepcopy
from pathlib import Path
import json
import numpy as np
from kv_cache import (example_model, transfer_model, rope_model, full_prefix, incremental,
                      serial, layer, positions_mask, attention, rotate)
from reference_cache import reference
from cache_validity import validity_matrix

root = Path(__file__).resolve().parent
checks = []


def close(x, y):
    np.testing.assert_allclose(np.asarray(x, dtype=float), np.asarray(y, dtype=float), rtol=6e-12, atol=6e-12)


def different(x, y):
    assert np.max(np.abs(np.asarray(x) - np.asarray(y))) > 1e-7


def compare_trace(a, b):
    for name in ("h", "z", "joined", "mixed", "residual", "u", "activation", "f", "result"):
        close(a[name], b[name])
    for x, y in zip(a["heads"], b["heads"]):
        for name in x:
            close(x[name], y[name])


def last(trace):
    return {key: [{k: v[-1:] for k, v in head.items()} for head in value]
            if key == "heads" else value[-1:] for key, value in trace.items()}


rng = np.random.default_rng(91)
for case in range(103):
    model = [example_model, transfer_model, rope_model][case % 3]()
    tokens = [0, 1, 2] if case == 0 else [2, 0, 1]
    pos = [0, 1, 2] if case == 0 else [1, 3, 4]
    if case >= 3:
        model["embedding"] += rng.normal(0, .3, model["embedding"].shape)
        for b in model["blocks"]:
            for head in b["heads"]:
                for name in ("q", "k", "v"):
                    head[name] += rng.normal(0, .2, head[name].shape)
            b["g1"] += rng.normal(0, .1, 2)
            b["n2"] += rng.normal(0, .1, 2)
            b["eps"] = float(rng.uniform(.2, 1.5))
    h, logits, cache, trace = full_prefix(model, tokens, pos)
    rh, rl, rt = reference(model, tokens, pos)
    close(h, rh); close(logits, rl)
    for a, b in zip(trace, rt): compare_trace(a, b)
    ph, _, old, _ = full_prefix(model, tokens[:-1], pos[:-1])
    before = deepcopy(serial(old))
    ih, il, updated, it = incremental(model, tokens[:-1], pos[:-1], tokens[-1], pos[-1], old)
    close(ih, h[-1:]); close(il, logits[-1:]); close(ph, h[:-1])
    assert serial(old) == before
    for index, (a, b) in enumerate(zip(trace, it)):
        compare_trace(last(a), b)
        for r in range(len(a["heads"])):
            for kind in ("k", "v"):
                close(updated["layers"][index]["heads"][r][kind], cache["layers"][index]["heads"][r][kind])
                assert np.array_equal(old["layers"][index]["heads"][r][kind], updated["layers"][index]["heads"][r][kind][:-1])
checks.append("명시3+생성100사례 Decimal70·전 중간값·Full/Incremental·과거 값 보존")

m = example_model(); tokens = [0, 1, 2]; pos = [0, 1, 2]
h, logits, base, trace = full_prefix(m, tokens, pos)
_, _, old, _ = full_prefix(m, tokens[:2], pos[:2])
changed_model = deepcopy(m); changed_model["embedding"][1] = [.1, 2.]
h2, _, changed, _ = full_prefix(changed_model, tokens, pos)
for r in range(2):
    for kind in ("k", "v"):
        for p in (0, 2): close(base["layers"][0]["heads"][r][kind][p], changed["layers"][0]["heads"][r][kind][p])
        close(base["layers"][1]["heads"][r][kind][0], changed["layers"][1]["heads"][r][kind][0])
        different(base["layers"][1]["heads"][r][kind][1:], changed["layers"][1]["heads"][r][kind][1:])
# 미래를 바꿔도 과거 반환 불변. 허용된 과거를 바꾸면 실제 반응한다.
future = deepcopy(m); future["embedding"][2] += [2., -1.]
hf, _, _, _ = full_prefix(future, tokens, pos)
close(hf[:2], h[:2]); different(h2[2], h[2])
checks.append("토큰 변경의 첫/둘째 레이어 반례·미래 불변·허용 과거 반응")

mutations = {}
for name in ("W_Q", "W_K", "W_V", "W_O", "FFN", "LN1", "LN2", "Readout", "Absolute", "기존Mask"):
    mm = deepcopy(m); positions = pos; allowed = None
    if name in {"W_Q", "W_K", "W_V"}:
        mm["blocks"][0]["heads"][0][{"W_Q":"q", "W_K":"k", "W_V":"v"}[name]] *= 1.7
    elif name == "W_O": mm["blocks"][0]["wo"] *= 1.2
    elif name == "FFN": mm["blocks"][0]["bias2"] += [.2, -.1]
    elif name == "LN1": mm["blocks"][0]["g1"] *= 1.3
    elif name == "LN2": mm["blocks"][0]["g2"] *= 1.3
    elif name == "Readout": mm["readout"] *= 1.5
    elif name == "Absolute": positions = [0, 1, 3]
    else:
        allowed = [positions_mask(pos, pos, [True]*3)] * 2
        allowed = deepcopy(allowed); allowed[0][2, 1] = False
    mh, ml, mc, mt = full_prefix(mm, tokens, positions, allowed)
    rrh, rrl, rrt = reference(mm, tokens, positions, allowed)
    close(mh, rrh); close(ml, rrl)
    for a,b in zip(mt,rrt): compare_trace(a,b)
    mutations[name] = dict(h=mh, cache=mc, changed=[
        dict(layer=l+1, head=r+1, kind=kind, positions=[p for p in range(3)
             if not np.allclose(base["layers"][l]["heads"][r][kind][p], mc["layers"][l]["heads"][r][kind][p], rtol=1e-10, atol=1e-10)])
        for l in range(2) for r in range(2) for kind in ("k", "v")])
    if name in {"W_Q", "W_O", "FFN", "LN2", "Readout", "기존Mask"}:
        for r in range(2):
            for kind in ("k", "v"): close(base["layers"][0]["heads"][r][kind], mc["layers"][0]["heads"][r][kind])
    if name in {"W_Q", "W_K"}:
        close(base["layers"][1]["heads"][0]["k"][0], mc["layers"][1]["heads"][0]["k"][0])
    if name == "Readout":
        close(h, mh); different(logits, ml)
checks.append("매개변수·위치·기존Mask 변경10안의 생성원 및 Decimal 대조")

failures = []
def rejected(name, fn):
    try: fn()
    except (ValueError, KeyError, IndexError): failures.append(name)
    else: raise AssertionError(name)

rejected("다른 Prefix", lambda: incremental(m,[0,0],[0,1],2,2,old))
rejected("다른 위치 계약", lambda: incremental(m,[0,1],[1,2],2,3,old))
rejected("위치0 재시작", lambda: incremental(m,[0,1],[0,1],2,0,old))
rejected("매개변수 변경 후 무재판정", lambda: incremental(changed_model,[0,1],[0,1],2,2,old))
for name in ("레이어 교환", "Head 교환", "K/V 위치 불일치", "Query를 기본 Cache에 혼입"):
    wrong = deepcopy(old)
    if name == "레이어 교환": wrong["layers"].reverse()
    elif name == "Head 교환": wrong["layers"][0]["heads"].reverse()
    elif name == "K/V 위치 불일치": wrong["layers"][0]["heads"][0]["v"] = wrong["layers"][0]["heads"][0]["v"][::-1]
    else: wrong["queries"] = trace[0]["heads"][0]["q"]
    rejected(name, lambda: incremental(m,[0,1],[0,1],2,2,wrong))
rejected("활성 빈행", lambda: attention(np.ones((1,1)),np.ones((3,1)),np.ones((3,1)),np.zeros((1,3),bool),[True]))
rejected("Mask 축", lambda: attention(np.ones((1,1)),np.ones((3,1)),np.ones((3,1)),np.ones((3,1),bool),[True]))
rejected("Token 실수", lambda: full_prefix(m,[0.,1.],[0,1]))
rejected("중복 원위치", lambda: full_prefix(m,[0,1],[0,0]))
bad = deepcopy(m); bad["blocks"][0]["wo"] = np.ones((2,3))
rejected("Residual 폭", lambda: full_prefix(bad,tokens,pos))
bad = deepcopy(m); bad["blocks"][0]["eps"] = 0
rejected("epsilon0", lambda: full_prefix(bad,tokens,pos))
bad = deepcopy(m); bad["embedding"][0,0] = np.nan
rejected("NaN", lambda: full_prefix(bad,tokens,pos))

# 검사를 우회해 실제 잘못된 계산의 차이도 확인한다.
for name in ("레이어", "Head", "V위치", "삼각Mask"):
    past = deepcopy(old["layers"][0]); mask = None
    if name == "레이어": past = old["layers"][1]
    elif name == "Head": past["heads"].reverse()
    elif name == "V위치": past["heads"][0]["v"] = past["heads"][0]["v"][::-1]
    else: mask = np.tril(np.ones((1,3),dtype=bool))
    wrong_h, _, _ = layer(np.array([[1.2,1.]]), [2], m["blocks"][0], past, mask)
    different(wrong_h, trace[0]["result"][-1:])
# 이전 Query를 새 Query로 사용하면 새 행이 달라진다. 과거 Query의 저장 자체는 오류가 아니다.
head = trace[0]["heads"][0]
_, _, wrong_q = attention(head["q"][:1], head["k"], head["v"], np.ones((1,3),bool),[True])
different(wrong_q, head["out"][-1:])
checks.append("거부15조건·오류 우회4안·과거Query를 새 요청에 재사용하는 반례")

# K/V와 원위치를 함께 순열하면 출력이 같다. 패딩과 비활성은 별도로 검사한다.
q,k,v=np.array([[1.,2.]]),np.array([[1.,0.],[0.,1.],[2.,1.]]),np.array([[1.],[3.],[9.]])
mask=positions_mask([3],[1,3,5],[True]*3)
s,a,o=attention(q,k,v,mask,[True]); order=[2,0,1]
close(attention(q,k[order],v[order],mask[:,order],[True])[2],o)
assert mask.tolist()==[[True,True,False]]
close(attention(q,k,v,np.zeros((1,3),bool),[False])[2],[[0.]])
active=np.array([True,False,True]); hp,_,_,tp=full_prefix(m,tokens,pos,active=active)
pad=deepcopy(m); pad["embedding"][1] += [100.,-100.]
hpp,_,_,_=full_prefix(pad,tokens,pos,active=active)
close(hp[[0,2]],hpp[[0,2]])
# 다른 정밀도·비결정 함수·시퀀스 통계는 동등성 정리의 가정을 충족하지 않는다.
dropout1 = trace[0]["result"][-1:] * np.array([[0., 2.]])
dropout2 = trace[0]["result"][-1:] * np.array([[2., 0.]])
different(dropout1, dropout2)
quant=np.asarray(h,dtype=np.float16).astype(float)
assert not np.array_equal(quant,h)
whole=np.array([[1.,0.],[.1,1.],[1.2,1.]])
assert not np.allclose((whole-whole.mean(axis=0))[:2],(whole[:2]-whole[:2].mean(axis=0)))

rm=rope_model(); rh,_,rc,rt=full_prefix(rm,[2,0,1],[1,3,4])
_,_,rshift,_=full_prefix(rm,[2,0,1],[2,4,5])
for l in range(2):
    close(rc["layers"][l]["heads"][0]["v"],rshift["layers"][l]["heads"][0]["v"])
    different(rc["layers"][l]["heads"][0]["k"],rshift["layers"][l]["heads"][0]["k"])
raw=rt[0]["heads"][0]["raw_k"]
close(rotate(raw,[1,3,4],[.7]),rc["layers"][0]["heads"][0]["k"])
_,_,rone,_=full_prefix(rm,[2,0,1],[1,2,4])
close(rc["layers"][0]["heads"][0]["v"],rone["layers"][0]["heads"][0]["v"])
different(rc["layers"][1]["heads"][0]["v"][1:],rone["layers"][1]["heads"][0]["v"][1:])
checks.append("원위치 순열·미래 차단·패딩/비활성·정밀도/비결정/시퀀스정규화 반례·RoPE 회전전후/동시이동/국소변경")

# 큰 위치도 각도 축약한 독립 삼각 기준으로 대조한다.
large_h, large_l, _, large_t = full_prefix(rm,[2,0,1],[1000,1002,1003])
large_rh, large_rl, large_rt = reference(rm,[2,0,1],[1000,1002,1003])
close(large_h,large_rh); close(large_l,large_rl)
for x,y in zip(large_t,large_rt): compare_trace(x,y)
checks.append("RoPE 원위치1000의 각도 축약 Decimal 대조")

report=dict(checks=checks,rejected=failures,mutations=mutations,validity={
    name:validity_matrix(name, changed_position=2 if name in {"Absolute","기존Mask"} else 1) for name in ("추가","토큰","Absolute","RoPE","W_Q","W_K","W_V","W_O","FFN","LN1","LN2","기존Mask","새QueryMask","Readout","다른Prefix")})
(root/"CACHE_CHECKS.json").write_text(json.dumps(serial(report),ensure_ascii=False,indent=2)+"\n")
for item in checks: print(item)
print("유한 수치 시험 완료. 일반 증명·독립 심사·독자 실증과 별개다.")
