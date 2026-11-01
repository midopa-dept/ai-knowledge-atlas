"""출처 투영부터 집계까지 독립 Decimal 기준과 성질을 대조한다."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np
from sources import (example_inputs, self_attention, cross_attention, project)
from solution_sources import compare_providers, permute_provider


def scalar_reference(h, z, wq, wk, wv, mask, active):
    """NumPy 곱·지수·Softmax 없이 스칼라 중첩 합으로 계산한다."""
    def convert(x):
        return [[D(str(float(v))) for v in row] for row in x]
    def multiply(a, b):
        return [[sum((a[i][t]*b[t][j] for t in range(len(b))), D(0))
                 for j in range(len(b[0]))] for i in range(len(a))]
    with localcontext() as ctx:
        ctx.prec = 70
        hh, zz, uq, uk, uv = map(convert, [h, z, wq, wk, wv])
        q, k, v = multiply(hh, uq), multiply(zz, uk), multiply(zz, uv)
        m, n, dk, dv = len(q), len(k), len(q[0]), len(v[0])
        s = [[sum((q[i][t]*k[j][t] for t in range(dk)), D(0))
              / D(dk).sqrt() for j in range(n)] for i in range(m)]
        a = [[D(0)]*n for _ in range(m)]
        for i in range(m):
            if not active[i]:
                continue
            cols = [j for j in range(n) if mask[i, j]]
            maximum = max(s[i][j] for j in cols)
            e = [(s[i][j]-maximum).exp() for j in cols]
            denom = sum(e)
            for j, value in zip(cols, e):
                a[i][j] = value/denom
        o = multiply(a, v)
        return [np.array([[float(t) for t in row] for row in mat])
                for mat in [q, k, v, s, a, o]]


count = 0

def check(h, z, wq, wk, wv, mask=None, active=None):
    global count
    if mask is None:
        mask = np.ones((len(h), len(z)), dtype=bool)
    if active is None:
        active = np.ones(len(h), dtype=bool)
    actual = cross_attention(h, z, wq, wk, wv, mask, active)
    ref = scalar_reference(h, z, wq, wk, wv, mask, active)
    for a, b in zip(actual, ref):
        np.testing.assert_allclose(a, b, rtol=2e-12, atol=2e-12)
    np.testing.assert_allclose(actual[-2].sum(1), active.astype(float))
    assert np.all(actual[-2][~mask] == 0)
    count += 1
    return actual


x, h, wq, wk, wv, uq, r = example_inputs()
original = [a.copy() for a in [x, h, wq, wk, wv, uq]]
s = check(x, x, wq, wk, wv)
c = check(h, x, uq, wk, wv)
expected_a = [[F(2, 5), F(1, 5), F(2, 5)],
              [F(1, 7), F(3, 7), F(3, 7)],
              [F(2, 11), F(3, 11), F(6, 11)]]
expected_o = [[sum(expected_a[i][j]*F(int(s[2][j, t]))
                   for j in range(3)) for t in range(2)] for i in range(3)]
np.testing.assert_allclose(s[-2], np.array(expected_a, float), atol=2e-13)
np.testing.assert_allclose(s[-1], np.array(expected_o, float), atol=2e-13)
for left, right in zip([s[0][:2], *s[1:3], *[a[:2] for a in s[3:]]], c):
    np.testing.assert_array_equal(left, right)
np.testing.assert_allclose(x+s[-1], [[13/5, 9/5], [8/7, 25/7], [27/11, 38/11]])
np.testing.assert_allclose(h+project(c[-1], r), [[13/5, 9/5, 4/5], [8/7, 25/7, -3/7]])
for before, after in zip(original, [x, h, wq, wk, wv, uq]):
    np.testing.assert_array_equal(before, after)
# Causal·패딩 정책은 출처와 별도로 지정한다.
causal = check(x, x, wq, wk, wv, np.tri(3, dtype=bool))
np.testing.assert_allclose(causal[-1], [[2, 0], [1/2, 9/4], [16/11, 27/11]])
mask = np.array([[1, 1, 0], [1, 1, 0]], dtype=bool)
masked = check(h, x, uq, wk, wv, mask)
np.testing.assert_allclose(masked[-1], [[4/3, 1], [1/2, 9/4]])
inactive = check(h, x, uq, wk, wv, mask, np.array([True, False]))
np.testing.assert_array_equal(inactive[-1][1], [0, 0])
z_new = x.copy(); z_new[2] = [2, 1]
changed = check(h, z_new, uq, wk, wv)
np.testing.assert_allclose(changed[-1], [[20/7, 15/7], [2, 18/7]])
np.testing.assert_array_equal(c[-2][1], changed[-2][1])
np.testing.assert_array_equal(masked[-1], check(h, z_new, uq, wk, wv, mask)[-1])
comparison = compare_providers(h, x, z_new, uq, wk, wv, mask)
np.testing.assert_array_equal(*comparison['O'])
# 독립 문제의 기대값도 직접 검사한다.
p03 = check(np.array([[1.], [2.], [0.]]), np.array([[1.], [2.], [0.]]),
            [[1.]], [[np.log(2)]], [[3.]])
np.testing.assert_allclose(p03[-1].ravel(), [30/7, 36/7, 3])
p08 = check(np.array([[1.], [2.]]), np.array([[0.], [1.], [2.]]),
            [[1.]], [[np.log(2)]], [[4.]])
np.testing.assert_allclose(p08[-1].ravel(), [40/7, 48/7])
order = [2, 0, 1]
permuted = permute_provider(h, x, uq, wk, wv, mask, order)
np.testing.assert_allclose(masked[-1], permuted[-1])
np.testing.assert_allclose(permuted[-2], [[0, 2/3, 1/3], [0, 1/4, 3/4]])
np.testing.assert_allclose(c[-2][0] @ s[2][order], [6/5, 12/5])
# 고정 A에서의 값 변화와 원래 Z 변경을 구별한다.
for t, delta in [(2, [5., -5.]), (1, [7., -7.])]:
    v = c[2].copy(); v[t] += delta
    np.testing.assert_allclose(c[-2]@v-c[-1], c[-2][:, t, None]*delta)
# 제공자 출처를 틀리면 동일 shape라도 실패하는 분리 실험이다.
hh = np.eye(2); zz = hh[::-1].copy()
right = check(hh, zz, np.eye(2), np.eye(2), np.diag([2., 3.]))
assert not np.array_equal(right[1], project(hh, np.eye(2)))
assert not np.array_equal(right[2], project(hh, np.diag([2., 3.])))
# 심화: 비율 변화와 값 변화의 두 경로를 중심차분으로 대조한다.
e = np.array([[.2, -.1], [.1, .3], [-.2, .4]])
dk, dv = e@wk, e@wv
ds = c[0]@dk.T/np.sqrt(2)
da = c[-2]*(ds-(c[-2]*ds).sum(1, keepdims=True))
dot = da@c[2]+c[-2]@dv
step = 1e-5
plus = cross_attention(h, x+step*e, uq, wk, wv)[-1]
minus = cross_attention(h, x-step*e, uq, wk, wv)[-1]
np.testing.assert_allclose((plus-minus)/(2*step), dot, rtol=1e-8, atol=1e-9)
assert np.linalg.norm(da@c[2]) > 0 and np.linalg.norm(c[-2]@dv) > 0
# 서로 다른 길이/폭·Mask·순열을 생성해 스칼라 기준과 대조한다.
rng = np.random.default_rng(104)
for _ in range(100):
    m, n, dh, dz, dk, dv = rng.integers(1, 6, size=6)
    h0, z0 = rng.normal(size=(m, dh)), rng.normal(size=(n, dz))
    ws = [rng.normal(size=shape) for shape in [(dh, dk), (dz, dk), (dz, dv)]]
    b = rng.random((m, n)) > .35
    b[:, 0] = True
    active = rng.random(m) > .2
    result = check(h0, z0, *ws, b, active)
    p = rng.permutation(n)
    moved = cross_attention(h0, z0[p], *ws, b[:, p], active)
    np.testing.assert_allclose(result[-1], moved[-1], rtol=2e-12, atol=2e-12)
    p = rng.permutation(m)
    moved = cross_attention(h0[p], z0, *ws, b[p], active[p])
    np.testing.assert_allclose(result[-1][p], moved[-1], rtol=2e-12, atol=2e-12)
    # Self는 요청/제공 위치와 Mask의 두 축을 함께 옮긴다.
    xx = rng.normal(size=(n, dh))
    ww = [rng.normal(size=shape) for shape in [(dh, dk), (dh, dk), (dh, dv)]]
    bb = rng.random((n, n)) > .35; bb[:, 0] = True
    p = rng.permutation(n)
    left = self_attention(xx, *ww, bb)[-1]
    right = self_attention(xx[p], *ww, bb[p][:, p])[-1]
    np.testing.assert_allclose(left[p], right, rtol=2e-12, atol=2e-12)
# 인터페이스 오류를 조용히 통과시키지 않는다.
invalid = [
    lambda: cross_attention([], x, uq, wk, wv),
    lambda: cross_attention(h, [], uq, wk, wv),
    lambda: cross_attention(h, x, np.eye(2), wk, wv),
    lambda: cross_attention(h, x, uq, np.ones((3, 2)), wv),
    lambda: cross_attention(h, x, uq, wk, np.ones((3, 2))),
    lambda: cross_attention(h, x, np.ones((3, 3)), wk, wv),
    lambda: cross_attention(h, x, uq, wk, wv, np.ones((3, 2), bool)),
    lambda: cross_attention(h, x, uq, wk, wv, np.ones((2, 3), int)),
    lambda: cross_attention(h, x, uq, wk, wv, np.zeros((2, 3), bool)),
    lambda: cross_attention(h, x, uq, wk, wv, active=np.array([True])),
    lambda: cross_attention(h*np.nan, x, uq, wk, wv),
    lambda: project([[1e308]], [[1e308]]),
]
for test in invalid:
    try:
        test()
    except ValueError:
        pass
    else:
        raise AssertionError("잘못된 입력이 거부되지 않았다")
report = {'환경': {'NumPy': np.__version__, '장치': 'CPU'},
          '독립 Decimal 스칼라 대조 사례': count,
          '무작위 길이·폭·접근·양쪽 순열 변형': 100,
          '잘못된 입력 거부': len(invalid),
          'Fraction 대표 비율·집계': '통과',
          'Self/Cross 동일 수치·반환·입력 보존': '통과',
          '차단 불변·허용 변경 양성 대조': '통과',
          '두 미분 경로와 중심차분': '통과'}
Path(__file__).with_name('NUMERICAL_SOURCES.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
