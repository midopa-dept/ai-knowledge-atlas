"""Decimal70 스칼라 독립 경로. NumPy/집필 구현을 호출하지 않는다."""
from decimal import localcontext
from reference_block import D, array, mm, add, ln, ffn, reference


def attention(h, e, weights, mask, active):
    wq, wk, wv, wo = weights
    q = mm(h, array(wq)); k = mm(e, array(wk)); v = mm(e, array(wv))
    s = [[sum(qi[t]*kj[t] for t in range(len(qi)))/D(len(qi)).sqrt()
          for kj in k] for qi in q]
    a = []
    for i, row in enumerate(s):
        if not active[i]: a.append([D(0)]*len(row)); continue
        selected = [j for j in range(len(row)) if mask[i][j]]
        if not selected: raise ValueError("유효 빈행")
        top = max(row[j] for j in selected)
        exp = [(row[j]-top).exp() if j in selected else D(0) for j in range(len(row))]
        a.append([x/sum(exp) for x in exp])
    o = mm(a, v)
    return dict(q=q, k=k, v=v, s=s, a=a, o=o), mm(o, array(wo))


def decoder(d, e, sw, cw, fp, norms, sm, cm, active=None):
    with localcontext() as ctx:
        ctx.prec = 70
        # E는 독립 Encoder 경로에서 만들어진 Decimal을 그대로 받는다.
        d = array(d); active = [True]*len(d) if active is None else active
        st, su = attention(d, d, sw, sm, active)
        r1 = add(d, su); h, n1 = ln(r1, norms[0])
        ct, cu = attention(h, e, cw, cm, active)
        r2 = add(h, cu); u, n2 = ln(r2, norms[1])
        f, linear, act = ffn(u, fp); r3 = add(u, f); y, n3 = ln(r3, norms[2])
        return dict(self=st, self_update=su, r1=r1, norm1=n1, h=h,
                    cross=ct, cross_update=cu, r2=r2, norm2=n2, u=u,
                    ffn_linear=linear, activated=act, ffn=f, r3=r3, norm3=n3, y=y)
