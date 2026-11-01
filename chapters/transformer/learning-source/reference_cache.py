"""NumPy 함수와 독립된 Decimal70 스칼라 전체 Decoder 기준. 행렬곱을 공유하지 않는다."""
from decimal import Decimal as D, localcontext


def dec(x):
    return D(str(float(x)))


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def project(row, matrix):
    return [sum((x * dec(matrix[k][j]) for k, x in enumerate(row)), D(0))
            for j in range(len(matrix[0]))]


def normalize(row, gamma, beta, eps):
    mean = sum(row) / len(row)
    variance = sum((x - mean) ** 2 for x in row) / len(row)
    return [(x - mean) / (variance + dec(eps)).sqrt() * dec(g) + dec(b)
            for x, g, b in zip(row, gamma, beta)]


def trig(x):
    # 삼각함수도 NumPy를 쓰지 않고 Taylor 급수로 계산한다.
    pi = D("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
    x %= 2 * pi
    if x > pi: x -= 2 * pi
    if x < -pi: x += 2 * pi
    s, c, st, ct = x, D(1), x, D(1)
    for n in range(1, 110):
        st *= -x * x / ((2 * n) * (2 * n + 1))
        ct *= -x * x / ((2 * n - 1) * (2 * n))
        s += st; c += ct
    return c, s


def rotary(row, p, theta):
    out = []
    for i, frequency in enumerate(theta):
        c, s = trig(D(int(p)) * dec(frequency))
        x, y = row[2 * i:2 * i + 2]
        out.extend([x * c - y * s, x * s + y * c])
    return out


def reference(model, tokens, positions, masks=None, active=None):
    with localcontext() as ctx:
        ctx.prec = 70
        h = [[dec(x) + D(int(p)) * dec(step) for x, step in
              zip(model["embedding"][t], model["position_step"])]
             for t, p in zip(tokens, positions)]
        traces = []
        for layer_index, block in enumerate(model["blocks"]):
            z = [normalize(row, block["g1"], block["n1"], block["eps"]) for row in h]
            heads = []
            for head in block["heads"]:
                q, raw_k, v = [[project(row, head[name]) for row in z]
                               for name in ("q", "k", "v")]
                k = raw_k
                if "theta" in head:
                    q = [rotary(row, p, head["theta"]) for row, p in zip(q, positions)]
                    k = [rotary(row, p, head["theta"]) for row, p in zip(k, positions)]
                scores, weights, outputs = [], [], []
                for i, query in enumerate(q):
                    s = [sum(x * y for x, y in zip(query, key)) / D(len(query)).sqrt() for key in k]
                    allowed = [positions[j] <= positions[i] and (active is None or active[j])
                               for j in range(len(k))] if masks is None else masks[layer_index][i]
                    a = [D(0)] * len(k)
                    if active is None or active[i]:
                        maximum = max(x for x, ok in zip(s, allowed) if ok)
                        exps = [(x - maximum).exp() if ok else D(0) for x, ok in zip(s, allowed)]
                        a = [x / sum(exps) for x in exps]
                    out = [sum(a[j] * v[j][d] for j in range(len(v))) for d in range(len(v[0]))]
                    scores.append(s); weights.append(a); outputs.append(out)
                heads.append(dict(q=q, raw_k=raw_k, k=k, v=v, scores=scores, weights=weights, out=outputs))
            joined = [sum((head["out"][i] for head in heads), []) for i in range(len(h))]
            mixed = [project(row, block["wo"]) for row in joined]
            residual = [add(x, y) for x, y in zip(h, mixed)]
            u = [normalize(row, block["g2"], block["n2"], block["eps"]) for row in residual]
            activation = [[max(x + dec(b), D(0)) for x, b in zip(project(row, block["b1"]), block["bias1"])] for row in u]
            f = [add(project(row, block["b2"]), [dec(x) for x in block["bias2"]]) for row in activation]
            result = [add(x, y) for x, y in zip(residual, f)]
            traces.append(dict(h=h, z=z, heads=heads, joined=joined, mixed=mixed,
                               residual=residual, u=u, activation=activation, f=f, result=result))
            h = result
        logits = [project(row, model["readout"]) for row in h]
        return h, logits, traces
