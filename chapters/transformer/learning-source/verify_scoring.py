"""Decimal 스칼라 기준·완전열거·조건 변형으로 본문과 해설을 검산한다."""
import itertools
import json
import platform
from decimal import Decimal, localcontext
from pathlib import Path
import numpy as np
from scoring import scaled_dot_product, softmax_rows
from solution_scoring import with_contributions, queries_for_odds

checks = {}


def reference(q, k, v):
    # NumPy @나 구현의 최대값 이동을 사용하지 않는 70자리 스칼라 계산.
    with localcontext() as ctx:
        ctx.prec = 70
        q, k, v = [[[Decimal(str(x)) for x in row] for row in matrix]
                   for matrix in (q, k, v)]
        dots = [[sum(x*y for x, y in zip(qi, kj)) for kj in k] for qi in q]
        scores = [[x / Decimal(len(q[0])).sqrt() for x in row] for row in dots]
        exps = [[x.exp() for x in row] for row in scores]
        a = [[x/sum(row) for x in row] for row in exps]
        o = [[sum(a[i][j]*v[j][t] for j in range(len(k)))
              for t in range(len(v[0]))] for i in range(len(q))]
        return [np.array(x, dtype=float) for x in (dots, scores, a, o)]


def case(name, q, k, v, output=None):
    actual = scaled_dot_product(q, k, v)
    for got, expected in zip(actual, reference(q, k, v)):
        np.testing.assert_allclose(got, expected, rtol=2e-13, atol=2e-13)
    if output is not None:
        np.testing.assert_allclose(actual[-1], output, rtol=2e-13, atol=2e-13)
    checks[name] = {label: x.tolist() for label, x in zip(('D', 'S', 'A', 'O'), actual)}
    return actual


q = [[1., 0.], [0., 1.]]
k = [[1., 0.], [0., 1.], [1., 1.]]
v = [[2., 0.], [0., 4.], [2., 4.]]
case('전체 예제', q, k, v)
case('내적 유제', [[2, -1], [1, 1]], [[1, 2], [-1, 0], [2, 1]], [[1], [2], [3]])
c = np.sqrt(2.)*np.log(2.)
full = case('전체 유제', q, [[c, 0], [0, c]], [[3, 0, 6], [0, 9, 3]], [[2, 3, 5], [1, 6, 4]])
case('독립01', [[1, -2, 3]], [[2, 1, 0], [0, -1, 2]], [[4], [10]])
case('독립02', [[1], [-1]], [[0], [np.log(2)], [np.log(4)]], [[7, 0], [0, 7], [7, 7]], [[5, 6], [5, 3]])
case('독립14', [[1]], [[0], [np.log(3)]], [[10, 0], [0, 2]], [[2.5, 1.5]])
case('독립15 정상', [[1]], [[0], [np.log(3)]], [[2], [10]], [[8]])
case('독립15 키만 순열', [[1]], [[np.log(3)], [0]], [[2], [10]], [[4]])
case('독립15 대응 순열', [[1]], [[np.log(3)], [0]], [[10], [2]], [[8]])
queries = queries_for_odds([[2, 1], [1, 3]])
case('독립19', queries, [[1, 0], [0, 1], [0, 0]], [[10], [20], [40]], [[20], [22]])
qc = [[1, 0], [0, 1]]
kc = [[0, 0], [np.sqrt(2)*np.log(3), 0]]
vc = [[2, 0, 4], [10, 8, 0]]
case('독립20', qc, kc, vc, [[8, 6, 1], [6, 4, 2]])

# 문제의 정확한 지수 비·원소·수치 조건을 별도로 확인한다.
np.testing.assert_allclose(softmax_rows([[0, np.log(2), np.log(3)]]), [[1/6, 1/3, 1/2]])
np.testing.assert_allclose(softmax_rows([[0, np.log(4), np.log(3)]]), [[1/8, 1/2, 3/8]])
np.testing.assert_allclose(with_contributions(q, [[c, 0], [0, c]], [[3, 0, 6], [0, 9, 3]])[3][1, :, 2], [2, 2])
np.testing.assert_allclose(12/(1+np.sqrt(3)), 4.392304845413264)
checks['비율과 scale 수치'] = {
    '폭4 비율 전': softmax_rows([[4, 0]]).tolist(),
    '폭4 비율 후': softmax_rows([[2, 0]]).tolist(),
    '유제 scale 출력 전': float(8-6/(1+np.exp(-3))),
    '유제 scale 출력 후': float(8-6/(1+np.exp(-1))),
    '독립04 오분모 출력': float(12/(1+np.sqrt(3))),
    '독립18 M 경계': float(np.log(999)),
}

# 비대칭 축 반례는 정상·전체·열별·잘못된 이동을 실제 비교한다.
s = np.array([[0., np.log(3)], [0., 0.]])
e = np.exp(s)
a = softmax_rows(s)
b, column = e/e.sum(), e/e.sum(axis=0, keepdims=True)
wrong_shift = softmax_rows(s-s.max(axis=0, keepdims=True))
np.testing.assert_allclose(a, [[.25, .75], [.5, .5]])
np.testing.assert_allclose(wrong_shift, [[.5, .5], [.75, .25]])
np.testing.assert_allclose(b @ [[2], [10]], [[16/3], [2]])
np.testing.assert_allclose(column @ vc, [[8.5, 6, 2], [3.5, 2, 2]])
checks['축 오류'] = {'전체': b.tolist(), '열': column.tolist(), '잘못된 최대값 이동': wrong_shift.tolist()}

# 확률 모형은 표본 추정 대신 모든 부호 조합의 정확한 평균/분산을 센다.
independent = [x[0]*x[2]+x[1]*x[3] for x in itertools.product([-1, 1], repeat=4)]
correlated = [2*u*w for u, w in itertools.product([-1, 1], repeat=2)]
assert sum(independent) == 0 and sum(x*x for x in independent)/16 == 2
assert sum(correlated) == 0 and sum(x*x for x in correlated)/4 == 4
assert all(u*u == 1 for u in [-1, 1])
checks['확률 완전열거'] = {'독립16경우 분산': 2, '반복좌표4경우 분산': 4, '쌍 의존 내적': 1, '쌍 의존 분산': 0, '독립07 분산': 49}

rng = np.random.default_rng(560)
for iteration in range(100):
    qr, kr, vr = rng.normal(size=(3, 4)), rng.normal(size=(5, 4)), rng.normal(size=(5, 2))
    d, s, a, o = scaled_dot_product(qr, kr, vr)
    for got, expected in zip((d,s,a,o), reference(qr,kr,vr)):
        np.testing.assert_allclose(got,expected,rtol=2e-12,atol=2e-12)
    np.testing.assert_allclose(a.sum(axis=1), 1)
    np.testing.assert_allclose(softmax_rows(s+rng.normal(size=(3,1))), a, atol=3e-15)
    offset = rng.normal(size=(1,4))
    np.testing.assert_allclose(scaled_dot_product(qr,kr+offset,vr)[2], a, atol=3e-15)
    p = rng.permutation(5)
    np.testing.assert_allclose(scaled_dot_product(qr,kr[p],vr[p])[-1], o, atol=3e-15)
    changed = qr.copy(); changed[1] *= 2
    np.testing.assert_allclose(scaled_dot_product(changed,kr,vr)[-1][[0,2]],o[[0,2]])
    # 심화02의 미분은 중앙차분과 대조한다. 증명 대체로 사용하지 않는다.
    eps=1e-5; t=2
    plus=s.copy(); minus=s.copy(); plus[0,t]+=eps; minus[0,t]-=eps
    derivative=((softmax_rows(plus) @ vr)-(softmax_rows(minus) @ vr))[0]/(2*eps)
    np.testing.assert_allclose(derivative,a[0,t]*(vr[t]-o[0]),rtol=2e-8,atol=2e-10)
checks['변형100회'] = 'Decimal 대조·행이동·키이동·대응순열·질의행 독립·미분 중앙차분'

# 수치 안정성과 정의역을 실제 실패 경로로 검사한다.
with np.errstate(over='ignore',under='ignore',invalid='ignore'):
    raw=np.exp([[1000.,1001.,999.]])
    assert not np.isfinite(raw/raw.sum()).all()
    assert np.exp(-1000.) == 0.
np.testing.assert_allclose(softmax_rows([[1000,1001,999]]), softmax_rows([[0,1,-1]]))
np.testing.assert_allclose(softmax_rows([[-1000,-1001,-1002]]), softmax_rows([[0,-1,-2]]))
bad=[([],[[1]],[[1]]),([[1,2]],[[1]],[[1]]),([[1]],[[1],[2]],[[1]]),([[np.nan]],[[1]],[[1]]),([[1]],[[np.inf]],[[1]]),([[1]],[[1]],[[np.inf]])]
for args in bad:
    try: scaled_dot_product(*args)
    except ValueError: pass
    else: raise AssertionError('잘못된 입력을 수용했다')
for args in ([], [[np.inf]], [[-np.inf]], [[np.nan]]):
    try: softmax_rows(args)
    except ValueError: pass
    else: raise AssertionError('유한 점수 조건이 누락됐다')
checks['잘못된 입력10개'] = '거부 확인'

report={'환경':{'Python':platform.python_version(),'NumPy':np.__version__},'사례':checks,'한계':'증명·독립 교육 심사·독자 실증을 수치 테스트로 대체하지 않는다'}
Path('NUMERICAL_SCORING.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('수치 대조·확률 완전열거·변형100회·잘못된 입력10개 확인 완료')
print('독립01 가중치와 출력:', checks['독립01']['A'], checks['독립01']['O'])
