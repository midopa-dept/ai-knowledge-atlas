"""독립 검산: Decimal 70자리·스칼라 반복. 본문 계산 함수를 호출하지 않는다."""
from decimal import Decimal, localcontext
D = lambda x: Decimal(str(x))


def array(x):
    return [[D(v) for v in row] for row in x]


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), D(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[u+v for u,v in zip(ar,br)] for ar,br in zip(a,b)]


def ln(x, params):
    gamma, beta, epsilon = params
    g, b, e = [D(v) for v in gamma], [D(v) for v in beta], D(epsilon)
    means, variances, normalized, out = [], [], [], []
    for row in x:
        mu = sum(row)/D(len(row)); var = sum((v-mu)**2 for v in row)/D(len(row))
        z = [(v-mu)/(var+e).sqrt() for v in row]
        means.append([mu]); variances.append([var]); normalized.append(z)
        out.append([z[t]*g[t]+b[t] for t in range(len(row))])
    return out, dict(mean=means, variance=variances, normalized=normalized)


def ffn(x, params):
    w1,b1,w2,b2 = params
    z = [[v+D(b1[t]) for t,v in enumerate(row)] for row in mm(x,array(w1))]
    h = [[max(D(0),v) for v in row] for row in z]
    out = [[v+D(b2[t]) for t,v in enumerate(row)] for row in mm(h,array(w2))]
    return out, z, h


def mha(x, projections, wo, masks, active):
    heads = []; concat = [[] for _ in x]
    for (wq,wk,wv), mask in zip(projections, masks):
        q,k,v = [mm(x,array(w)) for w in (wq,wk,wv)]
        s = [[sum(qi[t]*kj[t] for t in range(len(qi)))/D(len(qi)).sqrt()
              for kj in k] for qi in q]
        a = []
        for i,row in enumerate(s):
            if not active[i]: a.append([D(0)]*len(row)); continue
            selected = [j for j in range(len(row)) if mask[i][j]]
            top = max(row[j] for j in selected)
            e = [(row[j]-top).exp() if j in selected else D(0) for j in range(len(row))]
            a.append([v/sum(e) for v in e])
        o = mm(a,v)
        for c, row in zip(concat,o): c.extend(row)
        heads.append(dict(q=q,k=k,v=v,s=s,a=a,o=o))
    return heads,concat,mm(concat,array(wo))


def reference(inputs, mode, masks=None, active=None):
    """검산용 경로는 float64 결과를 입력받지 않고 원 매개변수에서 재계산한다."""
    x, projections, wo, fparams, ln1, ln2 = inputs
    x = array(x); n=len(x)
    masks = masks if masks is not None else [[[True]*n for _ in range(n)] for _ in projections]
    active = active if active is not None else [True]*n
    with localcontext() as ctx:
        ctx.prec=70
        attention_input=x
        if mode=='pre': attention_input,norm1=ln(x,ln1)
        heads,c,attention=mha(attention_input,projections,wo,masks,active)
        first=add(x,attention)
        if mode=='post': u,norm1=ln(first,ln1); f_input=u
        else: u=first; f_input,norm2=ln(u,ln2)
        update,z,h=ffn(f_input,fparams); second=add(u,update)
        if mode=='post': y,norm2=ln(second,ln2)
        else: y=second
        return dict(attention_input=attention_input,heads=heads,concat=c,
                    attention=attention,first_sum=first,norm1=norm1,u=u,
                    ffn_input=f_input,ffn_linear=z,activated=h,ffn=update,
                    second_sum=second,norm2=norm2,y=y)
