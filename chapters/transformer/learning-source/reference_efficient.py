"""NumPy 행렬곱을 사용하지 않는 별도 계산 경로. Decimal70과 명시적 좌표 합으로 검산한다."""
from decimal import Decimal, localcontext
from fractions import Fraction


def decimal_attention(q, k, v, mask):
    with localcontext() as ctx:
        ctx.prec = 70
        q, k, v = [[[Decimal(str(x)) for x in row] for row in a] for a in (q, k, v)]
        score, weight, output = [], [], []
        for i, qi in enumerate(q):
            js = [j for j, yes in enumerate(mask[i]) if yes]
            s = {j: sum(qi[t]*k[j][t] for t in range(len(qi)))/Decimal(len(qi)).sqrt() for j in js}
            e = {j: (s[j]-max(s.values())).exp() for j in js}
            a = {j: e[j]/sum(e.values()) for j in js}
            score.append([float(s[j]) if j in s else float('-inf') for j in range(len(k))])
            weight.append([float(a.get(j, 0)) for j in range(len(k))])
            output.append([float(sum(a[j]*v[j][t] for j in js)) for t in range(len(v[0]))])
        return score, weight, output


def fraction_kernel(qf, kf, v, mask):
    qf, kf, v = [[[Fraction(str(x)) for x in row] for row in a] for a in (qf, kf, v)]
    out = []
    for i, qi in enumerate(qf):
        w = [sum(x*y for x, y in zip(qi, kj)) if mask[i][j] else Fraction(0)
             for j, kj in enumerate(kf)]
        d = sum(w)
        if d <= 0:
            raise ValueError('양의 분모 필요')
        out.append([sum(w[j]*v[j][t] for j in range(len(v)))/d for t in range(len(v[0]))])
    return out


def enumerated_paths(masks, source):
    """초기 source에서 시간 확장 그래프의 가능한 경로를 실제로 열거한다."""
    paths = [(source,)]
    for b in masks:
        paths = [path+(i+1,) for path in paths for i in range(len(b))
                 if b[i][path[-1]-1] or i+1 == path[-1]]
    return {path[-1] for path in paths}
