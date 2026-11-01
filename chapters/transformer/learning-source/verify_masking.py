"""독립 Decimal 스칼라 기준·정책 목록·누출/보존·경계 계약 검증."""
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import json
import numpy as np
from masking import causal_allowed, masked_attention, masked_softmax
from solution_masking import diagnose_and_repair


def reference(q, k, v, mask, active):
    # NumPy 내적/Softmax를 호출하지 않는 70자리 스칼라 기준이다.
    with localcontext() as ctx:
        ctx.prec = 70
        d = lambda x: Decimal(str(float(x)))
        s, a, o = [], [], []
        scale = Decimal(len(q[0])).sqrt()
        for i in range(len(q)):
            row = [sum(d(q[i][r])*d(k[j][r]) for r in range(len(q[i])))/scale
                   for j in range(len(k))]
            s.append(row)
            allowed = [j for j in range(len(k)) if mask[i][j]]
            coeff = [Decimal(0)]*len(k)
            if active[i]:
                assert allowed
                maximum = max(row[j] for j in allowed)
                weights = [(row[j]-maximum).exp() for j in allowed]
                total = sum(weights)
                for j, w in zip(allowed, weights):
                    coeff[j] = w/total
            a.append(coeff)
            o.append([sum(coeff[j]*d(v[j][t]) for j in range(len(k)))
                      for t in range(len(v[0]))])
        return [np.array(x, dtype=float) for x in (s, a, o)]


report = {"명시 사례": {}, "위치 변형": 0, "계약 거부": 0}


def check(name, q, k, v, mask, active=None, expected=None):
    if active is None:
        active = np.ones(len(q), bool)
    actual = masked_attention(q, k, v, mask, active)
    independent = reference(q, k, v, mask, active)
    for x, y in zip(actual, independent):
        np.testing.assert_allclose(x, y, rtol=2e-13, atol=2e-13)
    np.testing.assert_allclose(actual[1].sum(axis=1), active.astype(float), atol=2e-15)
    assert np.all(actual[1][~mask] == 0)
    if expected is not None:
        np.testing.assert_allclose(actual[2], expected, atol=2e-13)
    report["명시 사례"][name] = {key: val.tolist() for key,val in zip(["S","A","O"],actual)}
    return actual


q = np.ones((3,1)); k = np.array([[0.],[np.log(2)],[np.log(3)]])
v = np.array([[2.,0],[0,6],[12,12]])
mask = causal_allowed([0,1,2],[0,1,2],[True]*3)
check("대표 차단 전",q,k,v,np.ones((3,3),bool),expected=[[19/3,8]]*3)
_,a,o = check("대표 차단 후",q,k,v,mask,expected=[[2,0],[2/3,4],[19/3,8]])
for padding_value in [100,0]:
    check(f"패딩{padding_value} 차단 전",[[1]],[[0],[np.log(3)],[np.log(4)]],
          [[2],[10],[padding_value]],np.ones((1,3),bool),expected=[[4+padding_value/2]])
    check(f"패딩{padding_value} 차단 후",[[1]],[[0],[np.log(3)],[np.log(4)]],
          [[2],[10],[padding_value]],np.array([[True,True,False]]),expected=[[8]])
check("왼쪽 패딩",np.zeros((3,1)),np.zeros((3,1)),[[99],[2],[6]],
      causal_allowed([-1,0,1],[-1,0,1],[False,True,True]),np.array([False,True,True]),[[0],[2],[4]])
order=np.array([2,0,1]); kp=np.arange(3)[order]; kr=k[order]; vr=v[order]
wrong=np.tril(np.ones((3,3),bool)); fixed=causal_allowed([0,1,2],kp,[True]*3)
check("재배열 오류",q,kr,vr,wrong,expected=[[12,12],[9.5,9],[19/3,8]])
_,_,fixed_o=check("재배열 수정",q,kr,vr,fixed,expected=o)
ck,cv=kr.copy(),vr.copy(); ck[0,0]=np.log(30); cv[0]=[120,-12]
check("미래 변경 오류",q,ck,cv,wrong,expected=[[120,-12],[3602/31,-360/31],[3602/33,-348/33]])
_,_,changed=check("미래 변경 수정",q,ck,cv,fixed,expected=[[2,0],[2/3,4],[3602/33,-348/33]])
np.testing.assert_array_equal(changed[:2],fixed_o[:2])
cv=vr.copy(); cv[2]=[0,9]
check("과거 양성 대조",q,kr,cv,fixed,expected=[[2,0],[2/3,6],[19/3,9]])
extra,missing,correct=diagnose_and_repair([0,1,2],kp,[True]*3,wrong)
assert extra.tolist()==[[0,0],[1,0]] and missing.tolist()==[[0,1],[1,2]]
np.testing.assert_array_equal(correct,fixed)
# 독립 연습의 계산도 유리수로 대조한다.
assert sum([Fraction(1,10)*3,Fraction(2,10)*9,Fraction(7,10)*90])==Fraction(651,10)
assert Fraction(1,3)*3+Fraction(2,3)*9==7
assert Fraction(1,4)*3+Fraction(1,8)*9+Fraction(5,8)*30==Fraction(165,8)
np.testing.assert_allclose(masked_softmax([[0,1,1e6]],[[True,True,False]]),
                           [[1/(1+np.e),np.e/(1+np.e),0]])
# 각 후보를 Python 비교로 판정하여 위치 벡터화와 별도로 대조한다.
rng=np.random.default_rng(561562)
for trial in range(100):
    n=int(rng.integers(3,9)); m=int(rng.integers(1,6)); width=int(rng.integers(1,5))
    kp=rng.permutation(n); qp=rng.integers(0,n,size=m)
    valid=rng.random(n)>.3; valid[kp==0]=True
    b=causal_allowed(qp,kp,valid)
    lists=[[bool(valid[j]) and int(kp[j])<=int(qp[i]) for j in range(n)] for i in range(m)]
    np.testing.assert_array_equal(b,lists)
    tq=rng.normal(size=(m,width)); tk=rng.normal(size=(n,width)); tv=rng.normal(size=(n,2))
    actual=masked_attention(tq,tk,tv,b)
    for x,y in zip(actual,reference(tq,tk,tv,lists,[True]*m)):
        np.testing.assert_allclose(x,y,rtol=2e-12,atol=2e-12)
    perm=rng.permutation(n)
    for index,(x,y) in enumerate(zip(actual[1:],masked_attention(tq,tk[perm],tv[perm],b[:,perm])[1:])):
        # 계수 열만 원래 순서로 돌린다. 출력 행의 요청 순서는 같다.
        if index==0:
            y=y[:,np.argsort(perm)]
        np.testing.assert_allclose(x,y,rtol=2e-12,atol=2e-12)
    for i in range(m):
        blocked=~b[i]; ck=tk.copy(); cv=tv.copy()
        ck[blocked]=rng.normal(size=ck[blocked].shape)*10
        cv[blocked]=rng.normal(size=cv[blocked].shape)*100
        updated=masked_attention(tq,ck,cv,b)
        np.testing.assert_array_equal(actual[1][i],updated[1][i])
        np.testing.assert_array_equal(actual[2][i],updated[2][i])
    report["위치 변형"]+=1


# 유제·독립 연습의 정책/출력은 직접 작성한 기대 배열과 대조한다.
policy_cases = [
    ([1,0],[1,2,0],[True]*3,[[1,0,1],[0,0,1]]),
    ([4,1],[3,0,5,1],[True]*4,[[1,1,0,1],[0,1,0,1]]),
    ([0,2],[-1,2,0,1],[False,True,True,True],[[0,0,1,0],[0,1,1,1]]),
    ([3,0],[2,0,4,1],[True,True,True,False],[[1,1,0,0],[0,1,0,0]]),
]
for qp,kp,valid,expected in policy_cases:
    np.testing.assert_array_equal(causal_allowed(qp,kp,valid),expected)
check("유제 정규화 전",[[1]],[[np.log(2)],[0],[np.log(5)]],[[3],[9],[30]],
      np.ones((1,3),bool),expected=[[165/8]])
check("유제 정규화 후",[[1]],[[np.log(2)],[0],[np.log(5)]],[[3],[9],[30]],
      np.array([[True,True,False]]),expected=[[5]])
check("독립05 차단 전",[[1]],[[0],[np.log(2)],[np.log(7)]],[[3],[9],[90]],
      np.ones((1,3),bool),expected=[[651/10]])
check("독립05 차단 후",[[1]],[[0],[np.log(2)],[np.log(7)]],[[3],[9],[90]],
      np.array([[True,True,False]]),expected=[[7]])
combined=causal_allowed([0,1,2,3],[0,1,2,3],[True,True,False,False])
check("유제 패딩 결합",np.zeros((4,1)),np.zeros((4,1)),[[4],[12],[80],[90]],combined,
      expected=[[4],[8],[8],[8]])
check("유제 패딩 질의 생략",np.zeros((4,1)),np.zeros((4,1)),[[4],[12],[80],[90]],combined,
      np.array([True,True,False,False]),[[4],[8],[0],[0]])
local=np.array([[p-1<=r<=p for r in range(5)] for p in range(5)])
check("독립19 두 입력",np.zeros((5,1)),np.zeros((5,1)),[[2],[4],[8],[16],[32]],local,
      expected=[[2],[3],[6],[12],[24]])
packed=np.array([[1,0,0,0],[1,1,0,0],[0,0,1,0],[0,0,1,1]],bool)
check("독립20 시퀀스 격리",np.zeros((4,1)),np.zeros((4,1)),[[2],[6],[100],[200]],packed,
      expected=[[2],[4],[100],[150]])
# 허용 계수만 뽑아 재정규화하는 대안은 underflow를 복구하지 못한다.
with np.errstate(under="ignore",invalid="ignore"):
    bad_weights=np.exp(np.array([0.,1.])-1e6)
    assert bad_weights.sum()==0
    assert np.isnan(bad_weights/bad_weights.sum()).all()
# 마지막 층의 위치0 V 자체가 미래에 의존하는 우회 반례.
for future in [5.,9.]:
    _,_,leaked=masked_attention([[0]],[[0]],[[future]],[[True]])
    assert leaked[0,0]==future


bad_calls=[
    lambda: masked_softmax([[0,1]],[[False,False]]),
    lambda: masked_softmax([[0,np.inf]],[[True,False]]),
    lambda: masked_softmax([[0,1]],[[1,0]]),
    lambda: masked_softmax([[0,1]],[True,False]),
    lambda: masked_softmax([[0,1]],[[True,False]],[True,False]),
    lambda: masked_softmax([[0,1]],[[True,False]],[1]),
    lambda: causal_allowed([.5],[0],[True]),
    lambda: causal_allowed([0],[0],[1]),
    lambda: causal_allowed([0],[0,1],[True]),
    lambda: masked_attention([[1]],[[0],[1]],[[2],[np.nan]],[[True,False]]),
    lambda: masked_attention([[1,2]],[[0]],[[2]],[[True]]),
    lambda: masked_attention([[1e308]],[[1e308]],[[2]],[[True]]),
    lambda: masked_attention([[0]],[[0]],[[2],[3]],[[True]]),
    lambda: masked_softmax([],[]),
]
for call in bad_calls:
    try:
        call()
    except ValueError:
        report["계약 거부"]+=1
    else:
        raise AssertionError("잘못된 입력을 거부하지 않았다")
np.testing.assert_array_equal(masked_softmax([[0,1]],[[False,False]],[False]),[[0,0]])
np.testing.assert_array_equal(masked_softmax([[1e308,-1e308]],[[True,True]]),[[1,0]])
# 같은 유한 음수는 균등분포다. 모든 위치 차단이 아니다.
np.testing.assert_array_equal(masked_softmax([[-1e9,-1e9]],[[True,True]]),[[.5,.5]])
Path('NUMERICAL_MASKING.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f"독립 수치{len(report['명시 사례'])}·위치 변형{report['위치 변형']}·잘못된 입력{report['계약 거부']} 검증 완료")
