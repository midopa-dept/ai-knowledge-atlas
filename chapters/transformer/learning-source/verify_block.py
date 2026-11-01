"""전 중간값 독립 Decimal 대조와 축·순서·접근·경계 변형 검사."""
import json
from pathlib import Path
import numpy as np
from block import (example_inputs, post_ln, pre_ln, layer_norm,
                   feed_forward, residual, transformer_block)
from reference_block import reference
from solution_block import exercise_inputs
RTOL = ATOL = 4e-12


def compare(actual, expected):
    if isinstance(actual, dict):
        assert actual.keys() == expected.keys()
        for k in actual: compare(actual[k], expected[k])
    elif isinstance(actual, list):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): compare(a,b)
    else:
        np.testing.assert_allclose(actual,np.array(expected,dtype=float),rtol=RTOL,atol=ATOL)


def check(inputs, masks=None, active=None):
    snapshots = [a.copy() for a in [inputs[0],inputs[2],*inputs[3],*inputs[4][:2],*inputs[5][:2]]]
    for mode,fn in [('post',post_ln),('pre',pre_ln)]:
        _,t=fn(*inputs,masks=masks,active=active)
        compare(t,reference(inputs,mode,masks,active))
    for old,new in zip(snapshots,[inputs[0],inputs[2],*inputs[3],*inputs[4][:2],*inputs[5][:2]]):
        np.testing.assert_array_equal(old,new)


rng=np.random.default_rng(568)
check(example_inputs()); check(exercise_inputs(1)); check(exercise_inputs(2))
new = list(example_inputs()); new[0] = np.array([[-.5,2.,1.],[3.,-1.,.25]])
check(tuple(new))
for case in range(100):
    n=1+case%5; d=1+case%5; h=1+case%3; mid=1+case%7
    x=rng.normal(size=(n,d)); projections=[]; total=0; masks=[]
    active=np.ones(n,dtype=bool)
    if n>1 and case%4==0: active[-1]=False
    for head in range(h):
        dk=1+(head+case)%3; dv=1+(head+case)%4; total+=dv
        projections.append(tuple(rng.normal(size=(d,w))*.6 for w in (dk,dk,dv)))
        mask=rng.random((n,n))>.4; np.fill_diagonal(mask,True); masks.append(mask)
    wo=rng.normal(size=(total,d))*.5
    ffn=(rng.normal(size=(d,mid)),rng.normal(size=mid),
         rng.normal(size=(mid,d))*.5,rng.normal(size=d))
    ln1=(rng.uniform(-2,2,d),rng.normal(size=d),10.**(-1-case%5))
    ln2=(rng.uniform(-2,2,d),rng.normal(size=d),10.**(-1-(case+2)%5))
    check((x,projections,wo,ffn,ln1,ln2),masks,active)
# 분산0·폭1·epsilon·gamma/beta는 공식으로 별도 대조한다.
for d in (1,3,5):
    g=np.arange(1,d+1,dtype=float); b=np.arange(d,dtype=float)-2
    for e in (1e-5,.25,4.):
        y,t=layer_norm(np.full((2,d),7.),g,b,e)
        np.testing.assert_array_equal(y,np.broadcast_to(b,(2,d)))
        assert np.all(t['variance']==0)
x=np.array([[1.,3.],[10.,14.]])
y,_=layer_norm(x,np.ones(2),np.zeros(2),.25)
wrong=(x-x.mean(axis=0))/np.sqrt(x.var(axis=0)+.25)
assert not np.allclose(y,wrong)
batched=np.stack([x,x+3])
by,_=layer_norm(batched,np.ones(2),np.zeros(2),.25)
np.testing.assert_allclose(by[0],by[1],atol=1e-14)
params=(np.array([[1.,-1.],[1.,1.]]),np.zeros(2),np.eye(2),np.zeros(2))
fy,_=feed_forward(batched,*params)
for i in range(2):
    for j in range(2): np.testing.assert_allclose(fy[i,j],feed_forward(batched[i,j],*params)[0])
# 두 층 causal: 미래를 바꾸어도 과거 반환이 같다. 양성 대조도 함께 둔다.
inputs=example_inputs(); mask=np.tril(np.ones((2,2),dtype=bool)); masks=[mask,mask]
for fn in (post_ln,pre_ln):
    original,_=fn(*inputs,masks=masks)
    changed=inputs[0].copy(); changed[1]=[8,-4,6]
    altered,_=fn(changed,*inputs[1:],masks=masks)
    np.testing.assert_allclose(original[0],altered[0],rtol=0,atol=1e-14)
    second,_=fn(original,*inputs[1:],masks=masks)
    other,_=fn(altered,*inputs[1:],masks=masks)
    np.testing.assert_allclose(second[0],other[0],rtol=0,atol=1e-14)
    full,_=fn(*inputs); full2,_=fn(changed,*inputs[1:]); assert not np.allclose(full[0],full2[0])
    leaked=inputs[0].copy(); leaked[0,0]+=changed[1,0]
    bad,_=fn(leaked,*inputs[1:],masks=masks); assert not np.allclose(original[0],bad[0])
# 비활성 Attention 행은 후속 Block에서 자동0이 아니다.
y,t=pre_ln(*inputs,active=np.array([True,False]))
assert np.all(t['attention'][1]==0) and not np.all(y[1]==0)
post,pt=post_ln(*inputs); pre,rt=pre_ln(*inputs)
assert not np.allclose(pt['attention'],rt['attention'])
assert not np.allclose(pt['ffn_input'],rt['ffn_input'])
assert not np.allclose(post,pre)
rejected=0

def reject(fn):
    global rejected
    try: fn()
    except (ValueError,TypeError): rejected+=1
    else: raise AssertionError('잘못된 입력을 허용했다')
for bad in ([np.nan,1,2],[np.inf,1,2],[1+2j,0,0],[],[[1,2],[3,4]]):
    reject(lambda bad=bad:layer_norm(bad,np.ones(3),np.zeros(3)))
for e in (0,-1,np.nan,np.inf,[.1]): reject(lambda e=e:layer_norm([1,2,3],np.ones(3),np.zeros(3),e))
reject(lambda:layer_norm([1,2,3],[1,2],[0,0]))
reject(lambda:layer_norm([1e308,-1e308],np.ones(2),np.zeros(2)))
reject(lambda:residual(np.ones((2,3)),np.ones(3)))
reject(lambda:residual(np.full(2,1e308),np.full(2,1e308)))
reject(lambda:feed_forward([1,2],np.ones((2,3)),np.zeros(3),np.ones((3,4)),np.zeros(4)))
reject(lambda:feed_forward([np.inf,2],*params))
reject(lambda:post_ln(np.ones((1,2,3)),*inputs[1:]))
reject(lambda:post_ln(inputs[0],inputs[1],np.ones((2,4)),*inputs[3:]))
reject(lambda:pre_ln(*inputs,masks=[np.ones((2,2))]*2))
reject(lambda:pre_ln(*inputs,masks=[np.zeros((2,2),dtype=bool)]*2))
reject(lambda:transformer_block(*inputs,mode='other'))
reject(lambda:post_ln(*inputs,active=np.ones(3,dtype=bool)))
report={'독립_기준':'Decimal70 스칼라 전 중간값','명시_사례':4,'생성_사례':100,
        '두_순서_대조':208,'rtol':RTOL,'atol':ATOL,'거부_조건':rejected,
        '축_배치_위치별_FFN_확인':True,'두_층_causal_및_누출_양성대조':True,
        '비제자리_확인':True,'라이브러리_비교':'미실시'}
Path(__file__).with_name('NUMERICAL_BLOCK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
