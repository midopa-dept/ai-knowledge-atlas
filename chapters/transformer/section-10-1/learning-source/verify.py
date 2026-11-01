"""스칼라 유리수 기준·독립 예상값·NumPy·조건과 반례를 대조한다."""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from aggregate import aggregate, normalize_rows, contributions, move_weight, reorder_sources
from solution_code import with_contributions


def scalar(weights, values):
    # 배열 연산을 사용하지 않는 독립 기준. 문자열 변환으로 소수를 유리수로 읽는다.
    return [[float(sum(F(str(a)) * F(str(v[r])) for a, v in zip(row, values)))
             for r in range(len(values[0]))] for row in weights]


cases = [
    ('예제 언어·두 요청', [[.2,.6,.2],[.2,.2,.6]], [[2,0],[0,4],[2,4]], [[.8,3.2],[1.6,3.2]]),
    ('예제 값 변경', [[.2,.6,.2]], [[2,0],[1,3],[2,4]], [[1.4,2.6]]),
    ('예제 비율 이동', [[.3,.5,.2]], [[2,0],[0,4],[2,4]], [[1,2.8]]),
    ('예제 역문제', [[.25,.25,.5]], [[0,0],[2,0],[0,2]], [[.5,1]]),
    ('유제 규칙', [[.5,0,.5]], [[2,0],[0,4],[2,4]], [[2,2]]),
    ('유제 값 변경', [[.2,.6,.2]], [[7,0],[0,4],[2,4]], [[1.8,3.2]]),
    ('유제 가능', [[.5,.5]], [[1,3],[5,1]], [[3,2]]),
    ('유제 대응', [[.1,.7,.2]], [[1,0],[0,2],[3,1]], [[.7,1.6]]),
    ('연습 기여', [[.6,.3,.1]], [[1,4],[5,0],[-2,2]], [[1.9,2.6]]),
    ('연습 규칙', [[0,.25,.75],[.75,.25,0]], [[2,1],[0,3],[4,-1]], [[3,0],[1.5,1.5]]),
    ('연습 변화 원형', [[.5,.25,.25]], [[2,2],[6,0],[0,4]], [[2.5,2]]),
    ('연습 변화 결과', [[.5,.25,.25]], [[2,2],[8,-2],[0,4]], [[3,1.5]]),
    ('연습 이동 원형', [[.4,.4,.2]], [[1,5],[4,5],[2,-1]], [[2.4,3.8]]),
    ('연습 이동 결과', [[.3,.5,.2]], [[1,5],[4,5],[2,-1]], [[2.7,3.8]]),
    ('연습 폭', [[.5,.5,0],[0,.25,.75]], [[1,0,2],[3,4,0],[0,2,6]], [[2,2,1],[.75,2.5,4.5]]),
    ('연습 역문제', [[.25,.25,.5]], [[0,0],[4,0],[0,2]], [[1,1]]),
    ('연습 출처', [[.2,.5,.3]], [[10],[20],[100]], [[42]]),
    ('연습 NumPy', [[.25,.75],[.5,.5]], [[2,0],[0,4]], [[.5,3],[1,2]]),
    ('연습 비유일', [[0,1,0],[.5,0,.5]], [[0],[1],[2]], [[1],[1]]),
    ('연습 손실 첫쌍', [[.25,.75]], [[0],[4]], [[3]]),
    ('연습 손실 둘째쌍', [[.25,.75]], [[6],[2]], [[3]]),
    ('연습 해석', [[.9,.1]], [[0,0],[10,0]], [[1,0]]),
    ('연습 센서', [[.75,.25,0],[0,.25,.75],[0,.5,.5]], [[10,1],[20,0],[30,1]], [[12.5,.75],[27.5,.75],[25,.5]]),
    ('심화 복원', [[.75,.25],[.25,.75]], [[1],[5]], [[2],[4]]),
]
report = {}
for name, a, v, expected in cases:
    ref = scalar(a,v)
    actual = aggregate(a,v)
    np.testing.assert_allclose(ref, expected, rtol=0, atol=1e-12)
    np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-12)
    np.testing.assert_allclose(contributions(a,v).sum(axis=1), actual, atol=1e-12)
    report[name] = actual.tolist()
np.testing.assert_allclose(normalize_rows([[0,2,6],[3,1,0]]), [[0,.25,.75],[.75,.25,0]])
# 본문의 실패 사례를 별도 스칼라 기준으로 확인한다.
np.testing.assert_allclose(scalar([[.6,.2,.2]], [[2,0],[0,4],[2,4]]), [[1.6,1.6]])
np.testing.assert_allclose(scalar([[.1,.7,.2]], [[3,1],[1,0],[0,2]]), [[1,.5]])
np.testing.assert_allclose(scalar([[.2,.5,.3]], [[100],[10],[20]]), [[31]])
np.testing.assert_allclose(scalar([[.125,.375],[.375,.125]], [[2],[6]]), [[2.5],[1.5]])
assert scalar([[-1,2]], [[0],[2]]) == [[4.0]]
assert scalar([[1,1]], [[1],[2]]) == [[3.0]]
np.testing.assert_allclose(np.array([[.25,.75],[.5,.5]]) * [[2,0],[0,4]], [[.5,0],[0,2]])
parts, out = with_contributions([[.2,.6,.2],[.2,.2,.6]], [[2,0],[0,4],[2,4]])
np.testing.assert_allclose(parts[1,2], [1.2,2.4])
np.testing.assert_allclose(out[1], [1.6,3.2])
# 목표 출력의 연립 조건을 유리수로 검산한다.
assert 1-F(3,4)-F(1,2) == F(-1,4)
assert 1-F(3,4)-F(3,4) == F(-1,2)
# 고정 난수로 특정 예제 밖에서도 증명의 조건을 확인한다.
rng = np.random.default_rng(13)
for _ in range(100):
    a = normalize_rows(rng.random((3,5)))
    v = rng.normal(size=(5,4))
    o = aggregate(a,v)
    assert (o >= v.min(axis=0)-1e-12).all() and (o <= v.max(axis=0)+1e-12).all()
    order = rng.permutation(5)
    ap, vp = reorder_sources(a,v,order)
    np.testing.assert_allclose(aggregate(ap,vp),o, atol=1e-12)
    c = rng.normal(size=4)
    np.testing.assert_allclose(aggregate(a,v+c),o+c, atol=1e-12)
    moved = move_weight(a[0],0,1,a[0,0]/2)
    np.testing.assert_allclose(aggregate([moved],v)[0]-o[0],a[0,0]/2*(v[1]-v[0]),atol=1e-12)
    h = rng.normal(size=4)
    changed = v.copy()
    changed[0] += h
    changed[1] -= a[0,0]/a[0,1]*h
    np.testing.assert_allclose(aggregate(a[:1],changed),o[:1],atol=1e-12)
    b = normalize_rows(rng.random((1,5)))[0]
    s = v[:,0]
    eps = np.abs(a[0]-b).sum()/2
    assert abs((a[0]-b)@s) <= eps*(s.max()-s.min())+1e-12
# 입력 검사의 거부 조건을 실행한다.
rejects = [lambda:normalize_rows([[-1,2,-1]]),lambda:normalize_rows([[0,0]]),
           lambda:aggregate([[.5,.5]], [[1]]),lambda:aggregate([[1,1]], [[1],[2]]),
           lambda:aggregate([[-1,2]], [[1],[2]]),lambda:move_weight([.4,.6],0,1,.5),
           lambda:reorder_sources([[.5,.5]],[[1],[2]],[0,0])]
for fn in rejects:
    try:
        fn()
    except ValueError:
        pass
    else:
        raise AssertionError('잘못된 입력을 거부하지 않음')
(Path(__file__).parent/'NUMERICAL_OUTPUT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f'독립 유리수/NumPy 예상값 {len(cases)}사례, 증명 조건 100변형, 입력 거부 {len(rejects)}조건 확인')
