"""독립70자리 Decimal·Fraction·축/순서/Mask/출력 변환 검산."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from numpy.testing import assert_allclose as close
from heads import multi_head, example_inputs
from solution_heads import reorder


def scalar_mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Decimal(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def dec(a):
    return [[Decimal(str(float(x))) for x in row] for row in a]


def reference(h, z, heads, wo, masks, active):
    # NumPy의 곱셈·exp·Softmax·Concat을 호출하지 않는 스칼라 경로다.
    with localcontext() as ctx:
        ctx.prec = 70
        traces = []
        for (wq, wk, wv), b in zip(heads, masks):
            q, k, v = (scalar_mm(dec(h), dec(wq)),
                       scalar_mm(dec(z), dec(wk)), scalar_mm(dec(z), dec(wv)))
            s = [[sum((u*t for u, t in zip(qi, kj)), Decimal(0)) /
                  Decimal(len(qi)).sqrt() for kj in k] for qi in q]
            a = []
            for i, row in enumerate(s):
                allowed = [j for j in range(len(z)) if b[i, j]]
                ar = [Decimal(0)]*len(z)
                if active[i]:
                    maximum = max(row[j] for j in allowed)
                    e = [(row[j]-maximum).exp() for j in allowed]
                    total = sum(e)
                    for j, val in zip(allowed, e): ar[j] = val/total
                a.append(ar)
            o = scalar_mm(a, v)
            traces.append(dict(q=q, k=k, v=v, s=s, a=a, o=o))
        c = [sum((t['o'][i] for t in traces), []) for i in range(len(h))]
        return traces, c, scalar_mm(c, dec(wo))


def compare(h, z, heads, wo, masks, active):
    got = multi_head(h, z, heads, wo, masks, active)
    want = reference(h, z, heads, wo, masks, active)
    for g, w in zip(got[0], want[0]):
        for key in g: close(g[key], np.array(w[key], float), rtol=3e-12, atol=3e-12)
    for g, w in zip(got[1:], want[1:]):
        close(g, np.array(w, float), rtol=3e-12, atol=3e-12)
    return got


x, heads, wo = example_inputs()
full = [np.ones((3, 3), bool)]*2
active = np.ones(3, bool)
t, c, y = compare(x, x, heads, wo, full, active)
a1 = [[F(2,5), F(1,5), F(2,5)], [F(1,3)]*3, [F(2,5), F(1,5), F(2,5)]]
a2 = [[F(1,3)]*3, [F(3,13),F(9,13),F(1,13)], [F(3,13),F(1,13),F(9,13)]]
for r, (a, values) in enumerate([(a1,[2,1,1]), (a2,[-1,3,-4])]):
    exact_o = [[sum(p*v for p,v in zip(row,values))] for row in a]
    close(t[r]['a'], np.array(a,float), atol=2e-14)
    close(t[r]['o'], np.array(exact_o,float), atol=2e-14)
exact_y = [[F(31,15),F(32,15)], [F(-8,39),F(164,39)], [F(271,65),F(2,65)]]
close(y, np.array(exact_y,float), atol=2e-14)
wrong = multi_head(x,x,heads[::-1],wo)[2]
close(wrong, [[-31/15,1/15],[8/39,172/39],[-271/65,-269/65]])
assert not np.allclose(wrong,y)
close(multi_head(x,x,heads[::-1],wo[::-1])[2],y)
# 잘못된 Concat/stack 축과 평균은 원래 연산이 아니다.
assert np.concatenate([u['o'] for u in t],axis=0).shape==(6,1)
assert np.stack([u['o'] for u in t]).shape==(2,3,1)
assert not np.allclose((t[0]['o']+t[1]['o'])/2,y)
b = np.tril(np.ones((3,3),bool))
causal = compare(x,x,heads,wo,[b,b],active)[2]
close(causal, [[3,3],[-1/2,5],[271/65,2/65]])
changed=x.copy(); changed[2]=[4.,2.]
for masks in [[b,b],[b,full[1]]]:
    before=multi_head(x,x,heads,wo,masks)[2]
    after=multi_head(changed,changed,heads,wo,masks)[2]
    if masks[1] is b: close(after[0],before[0],atol=0,rtol=0)
    else: assert not np.allclose(after[0],before[0])
# Cross의 다른 입력 폭·반환 폭: 대표 첫 두 요청을 재사용한다.
h=np.array([[1.,0.,1.],[0.,1.,1.]])
cross_heads=[(np.vstack([wq,[[0.]]]),wk,wv) for wq,wk,wv in heads]
wo3=np.array([[1.,2.,0.],[-1.,1.,1.]])
cross=compare(h,x,cross_heads,wo3,[np.ones((2,3),bool)]*2,np.ones(2,bool))[2]
close(cross[:,:2],y[:2]);close(cross[:,2],t[1]['o'][:2,0])
# 두 Head의 비교 폭2로 바꾸되 점수는 보존: K에 sqrt(2)를 곱한다.
extended=[(np.column_stack([wq,np.zeros(2)]),
           np.column_stack([wk*np.sqrt(2),np.zeros(2)]),wv) for wq,wk,wv in heads]
close(multi_head(x,x,extended,wo)[2],y)
# 새로운 독립 문제 수치도 대표 예제와 별도로 검산한다.
u=np.array([[1.],[0.]])
newheads=[(np.ones((1,1)),np.array([[np.log(2.)]]),np.array([[3.]])),
          (-np.ones((1,1)),np.array([[np.log(2.)]]),np.array([[6.]]))]
new=compare(u,u,newheads,np.array([[2.,-1.],[1.,1.]]),
            [np.ones((2,2),bool)]*2,np.ones(2,bool))[2]
close(new,[[6.,0.],[6.,1.5]],atol=2e-14)
# 서로 다른 A라도 상수 V이면 같은 Head 출력을 만들 수 있다.
const_z=np.array([[1.,0.],[1.,1.],[1.,2.]])
const_heads=[(np.array([[1.]]),np.array([[0.],[1.]]),np.array([[5.],[0.]])),
             (np.array([[-1.]]),np.array([[0.],[1.]]),np.array([[5.],[0.]]))]
ct,_,_=multi_head(np.array([[1.]]),const_z,const_heads,np.ones((2,1)))
assert not np.allclose(ct[0]['a'],ct[1]['a']);close(ct[0]['o'],ct[1]['o'])

# Head별 투영을 잘못 공유한 변형은 최종 shape로 잡히지 않는다.
shared=multi_head(x,x,[heads[0],heads[0]],wo)[2]
close(shared,np.column_stack([np.zeros(3),3*t[0]['o'][:,0]]))
assert shared.shape==y.shape and not np.allclose(shared,y)
# 서로 다른 값 폭·실제 도착 시각/패딩을 포함한 독립21 인터페이스.
interface_rng=np.random.default_rng(210566)
ih=interface_rng.normal(size=(2,7))*.3
iz=interface_rng.normal(size=(5,4))*.3
interface_heads=[tuple(interface_rng.normal(size=sh)*.3 for sh in
                       [(7,dk),(4,dk),(4,dv)]) for dk,dv in [(3,2),(1,3)]]
interface_wo=interface_rng.normal(size=(5,7))
interface_mask=np.array([[1,1,0,0,0],[1,1,1,1,0]],bool)
it,ic,iy=compare(ih,iz,interface_heads,interface_wo,
                 [interface_mask]*2,np.ones(2,bool))
assert ic.shape==(2,5) and iy.shape==(2,7)
padding_changed=iz.copy();padding_changed[4]=[9.,8.,7.,6.]
close(multi_head(ih,padding_changed,interface_heads,interface_wo,
                 [interface_mask]*2)[2],iy,atol=0,rtol=0)
late_changed=iz.copy();late_changed[2]+=1.
late_y=multi_head(ih,late_changed,interface_heads,interface_wo,
                  [interface_mask]*2)[2]
close(late_y[0],iy[0],atol=0,rtol=0)
assert not np.allclose(late_y[1],iy[1])

rng=np.random.default_rng(1050566)
for trial in range(100):
    m,n,dh,dz=(int(rng.integers(1,6)) for _ in range(4))
    hh=int(rng.integers(1,5)); dout=int(rng.integers(1,6))
    ih=rng.normal(size=(m,dh))*.5; iz=rng.normal(size=(n,dz))*.5
    hs=[]
    for _ in range(hh):
        dk,dv=int(rng.integers(1,5)),int(rng.integers(1,4))
        hs.append(tuple(rng.normal(size=s)*.5 for s in [(dh,dk),(dz,dk),(dz,dv)]))
    outw=rng.normal(size=(sum(t[2].shape[1] for t in hs),dout))
    bs=[rng.random((m,n))>.4 for _ in hs]
    for bb in bs: bb[:,0]=True
    act=rng.random(m)>.2
    before_h,before_z=ih.copy(),iz.copy()
    ts,cc,yy=compare(ih,iz,hs,outw,bs,act)
    close(ih,before_h,atol=0,rtol=0);close(iz,before_z,atol=0,rtol=0)
    assert cc.shape==(m,outw.shape[0]) and yy.shape==(m,dout)
    assert (yy[~act]==0).all()
    for tt,bb in zip(ts,bs):
        close(tt['a'].sum(1),act.astype(float));assert (tt['a'][~bb]==0).all()
    order=rng.permutation(hh).tolist()
    hs2,bs2,w2=reorder(hs,bs,outw,order)
    close(multi_head(ih,iz,hs2,w2,bs2,act)[2],yy,atol=2e-12)
    # 제공자·요청 순열과 Head 순열은 서로 다른 축이다.
    pq,pk=rng.permutation(m),rng.permutation(n)
    close(multi_head(ih[pq],iz[pk],hs,outw,[bb[pq][:,pk] for bb in bs],
                     act[pq])[2],yy[pq],atol=2e-12)
    # W_O 블록 합 분해를 다른 값 폭에서도 검산한다.
    offsets=np.cumsum([0]+[tt['o'].shape[1] for tt in ts])
    total=sum(tt['o']@outw[offsets[r]:offsets[r+1]] for r,tt in enumerate(ts))
    close(total,yy,atol=2e-12)

bad=[lambda:multi_head(x,x,[],wo),
     lambda:multi_head(x,x,heads,wo,full[:1]),
     lambda:multi_head(x,x,heads,np.ones((3,2))),
     lambda:multi_head(x,x,[(np.ones((3,1)),heads[0][1],heads[0][2])],wo),
     lambda:multi_head(x,x,[(np.ones((2,2)),heads[0][1],heads[0][2])],np.ones((1,2))),
     lambda:multi_head(x,x,heads,wo,[np.ones((2,3),bool)]*2),
     lambda:multi_head(x,x,heads,wo,[np.ones((3,3),int)]*2),
     lambda:multi_head(x,x,heads,wo,[np.zeros((3,3),bool)]*2),
     lambda:multi_head(x,x,heads,wo,active=np.ones(2,bool)),
     lambda:multi_head(x,x,heads,np.full((2,2),np.nan)),
     lambda:multi_head(x.reshape(1,3,2),x,heads,wo),
     lambda:multi_head(x[:0],x,heads,wo),
     lambda:multi_head(x,x,heads,wo.T[:,:0]),
     lambda:reorder(heads,full,wo,[0,0])]
for f in bad:
    try: f()
    except ValueError: pass
    else: raise AssertionError("잘못된 입력을 거부하지 않았다")
result={'독립 Decimal 정밀도':70,'명시 스칼라 대조 사례':5,'생성 대조 사례':100,
        'Head·제공자·요청 순열 및 블록 분해 변형':100,'거부 조건':len(bad),
        'Fraction 최종 Y':[[str(v) for v in row] for row in exact_y],
        'Head만 교환':wrong.tolist(),'Causal Y':causal.tolist(),
        '새 독립 문제 Y':new.tolist(),'실행':'통과'}
Path(__file__).with_name('NUMERICAL_HEADS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
