"""출처·접근·반환 계약과 별도 스칼라 계산의 실제 대조."""
import json
from pathlib import Path
from decimal import localcontext
import numpy as np
from architectures import *
from masking import causal_allowed
from sources import cross_attention
from reference_architectures import decoder, attention, array, reference, mm

checks = []


def close(actual, expected):
    if isinstance(expected, dict):
        for k in expected: close(actual[k], expected[k])
    elif isinstance(expected, list) and expected and isinstance(expected[0], dict):
        for a, e in zip(actual, expected): close(a, e)
    else: np.testing.assert_allclose(np.asarray(actual, float), np.asarray(expected, float), rtol=5e-12, atol=5e-12)


def require_change(a, b):
    if np.allclose(a, b, rtol=1e-10, atol=1e-10): raise AssertionError("양성 대조가 반응하지 않았다")


def main():
    p, wo, fp, ln = parameters()
    sw = (*p, wo)
    cw = (np.array([[1.,0.],[0.,1.],[0.,0.]]),
          np.sqrt(2.)*np.array([[np.log(2.),0.],[0.,np.log(3.)],[0.,0.]]),
          np.array([[1.,0.],[0.,1.],[1.,-1.]]), np.array([[1.,0.,.5],[0.,1.,-.5]]))
    t = integrated(); sm, cm = t['self_mask'], t['cross_mask']
    er = reference((t['z'], [p], wo, fp, ln, ln), 'post')
    close(t['encoder'], er)
    dr = decoder(t['d'], er['y'], sw, cw, fp, [ln]*3, sm, cm)
    close(t['decoder'], dr)
    with localcontext() as ctx:
        ctx.prec = 70
        lr = mm([dr['y'][-1]], array([[1.,0.,-1.],[0.,1.,0.],[.5,0.,1.]]))[0]
    close(t['logits'], lr); checks.append('실제 Encoder E부터 Decoder 전 중간값/Readout Decimal70')
    rng = np.random.default_rng(569)
    for case in range(100):
        m, n, dd, de, dk, dv = [int(rng.integers(1,5)) for _ in range(6)]
        d, e = rng.normal(size=(m,dd)), rng.normal(size=(n,de))
        sk = int(rng.integers(1,4)); sv = int(rng.integers(1,4)); ff = int(rng.integers(1,5))
        swr = (rng.normal(size=(dd,sk)),rng.normal(size=(dd,sk)),rng.normal(size=(dd,sv)),rng.normal(size=(sv,dd)))
        cwr = (rng.normal(size=(dd,dk)),rng.normal(size=(de,dk)),rng.normal(size=(de,dv)),rng.normal(size=(dv,dd)))
        fpr = (rng.normal(size=(dd,ff)),rng.normal(size=ff),rng.normal(size=(ff,dd)),rng.normal(size=dd))
        ns = [(rng.normal(size=dd),rng.normal(size=dd),float(rng.uniform(.05,.3))) for _ in range(3)]
        sm = causal_allowed(np.arange(m),np.arange(m),np.ones(m,dtype=bool))
        cm = rng.random((m,n))>.4; cm[:,0]=True
        active = rng.random(m)>.2
        y, dt = decoder_post(d,e,swr,cwr,fpr,ns,sm,cm,active)
        ref = decoder(d,array(e),swr,cwr,fpr,ns,sm,cm,active)
        close(dt,ref)
        assert y.shape == (m,dd)
    checks.append('생성100사례: 길이/입력 폭/비교 폭/값 폭/FFN/γβ/Mask/active 전 중간값')
    h,e,wq,wk,wv,mask=exact_cross()
    exact = cross_attention(h,e,wq,wk,wv,mask)
    close(exact[-2], [[2/5,1/5,2/5],[1/7,4/7,2/7]])
    close(exact[-1], [[8/5,4/5],[6/7,10/7]])
    wrong=cross_attention(h,e,wq,wk,wv,np.tri(2,3,dtype=bool))[-1]
    close(wrong,[[2,0],[.4,1.6]])
    perm=np.array([2,0,1])
    reordered=cross_attention(h,e[perm],wq,wk,wv,mask[:,perm])
    close(reordered[-1],exact[-1]); close(reordered[-2],exact[-2][:,perm])
    checks.append('직사각형 Cross Fraction 정답/불필요 tril/키 순열 대응')
    x=t['z']; cm=causal_allowed(np.arange(3),np.arange(3),np.ones(3,dtype=bool))
    def run(a,mask=cm): return post_ln(a,[p],wo,fp,ln,ln,[mask])[0]
    baseline=run(x); future=x.copy();future[2]=[7.,-3.,5.]
    close(run(future)[:2],baseline[:2])
    past=x.copy();past[0]=[-2.,1.,4.]
    require_change(run(past)[1],baseline[1])
    # 두 층에도 같은 초기정보/행별 함수 조건을 적용한다.
    close(run(run(future))[:2],run(baseline)[:2])
    require_change(run(future,np.ones((3,3),dtype=bool))[0],run(x,np.ones((3,3),dtype=bool))[0])
    require_change(run(x+x.mean(axis=0))[0],run(future+future.mean(axis=0))[0])
    zero=np.zeros_like(baseline)
    try: require_change(zero,zero)
    except AssertionError: checks.append('상수0 결함 양성 대조에서 거부')
    else: raise AssertionError('상수0 결함을 허용했다')
    checks.append('Decoder-only 미래 불변/과거 양성/두 층/전역 입력 오염 누출')
    d2=t['d'].copy();d2[1]=[4.,-2.,3.]
    close(integrated(prefix=d2)['decoder']['y'][0],t['decoder']['y'][0])
    z2=t['z'].copy();z2[2]=[5.,2.,-1.]
    require_change(integrated(source=z2)['decoder']['y'],t['decoder']['y'])
    require_change(integrated(prefix=np.array([[3.,1.,0.],[0.,1.,2.]]))['decoder']['y'][1],t['decoder']['y'][1])
    checks.append('통합 미래 Prefix 불변/조건 원문·허용 과거 양성')
    pad=np.array([True,True,False]);pm=full_allowed(2,pad)
    before=cross_attention(h,e,wq,wk,wv,pm)[-1]
    ep=e.copy();ep[2]=[9.,-8.]
    close(cross_attention(h,ep,wq,wk,wv,pm)[-1],before)
    active=np.array([True,False]);empty=pm.copy();empty[1]=False
    at=cross_attention(h,e,wq,wk,wv,empty,active)
    close(at[-1][1],[0,0])
    # 비활성 Attention만0이고 Residual/LN/FFN의 최종은 일반적으로 비영이다.
    sm=np.array([[True,False],[True,True]])
    y,_=decoder_post(t['d'],t['e'],sw,cw,fp,[ln]*3,sm,full_allowed(2,pad),active)
    require_change(y[1],np.zeros(3))
    # 스트리밍: Cross에서1열만 열어도 미리 전체로 인코딩된 E1은 미래 원문에 반응한다.
    one=full_allowed(2,np.array([True,False,False]))
    u=cross_attention(t['decoder']['h'],t['e'],*cw[:3],one)[-1]
    v=cross_attention(t['decoder']['h'],integrated(source=z2)['e'],*cw[:3],one)[-1]
    require_change(u,v); checks.append('Padding/비활성 요청/스트리밍 Encoder 간접 누출')
    enc_pad=full_allowed(3,np.array([True,True,False]))
    base_enc=post_ln(t['z'],[p],wo,fp,ln,ln,[enc_pad],np.array([True,True,False]))[0]
    change_enc=post_ln(z2,[p],wo,fp,ln,ln,[enc_pad],np.array([True,True,False]))[0]
    close(base_enc[:2],change_enc[:2])
    checks.append('Encoder 패딩 제공자 변경: 활성 두 행 Block 반환 불변')
    from solution_architectures import problem_cross
    from fractions import Fraction as F
    new = problem_cross()
    frac_a = [[F(1,4),F(1,4),F(1,2)],[F(1,9),F(4,9),F(4,9)]]
    frac_v = [[-1,1],[1,2],[0,3]]
    frac_o = [[sum(frac_a[i][j]*frac_v[j][k] for j in range(3)) for k in range(2)] for i in range(2)]
    assert frac_o == [[F(0),F(9,4)],[F(1,3),F(7,3)]]
    close(new['전체']['a'],frac_a); close(new['전체']['o'],frac_o)
    close(new['전체']['u'],[[-9/np.sqrt(97),9/np.sqrt(97)],[0,0]])
    close(new['잘못된_삼각형']['o'],[[-1,1],[3/5,9/5]])
    with localcontext() as ctx:
        ctx.prec=70
        nr,_=attention(array([[1,1],[2,0]]),array([[0,1],[1,0],[1,1]]),
                       (np.eye(2),np.sqrt(2)*np.log(2)*np.eye(2),np.array([[1,2],[-1,1]]),np.eye(2)),
                       [[True]*3]*2,[True,True])
    close({k:new['전체'][k] for k in nr},nr)
    checks.append('독립 문제10/11 새 Cross 전 중간값/분수/LN 정답')
    rejected=0
    def reject(fn):
        nonlocal rejected
        try: fn()
        except (ValueError,TypeError): rejected+=1
        else: raise AssertionError('잘못된 입력을 허용했다')
    reject(lambda:full_allowed(0,pad));reject(lambda:full_allowed(True,pad))
    reject(lambda:full_allowed(2,[1,1,0]));reject(lambda:full_allowed(2,[]))
    reject(lambda:full_allowed(2,pad,np.ones((3,2),bool)))
    reject(lambda:shifted_inputs([],0));reject(lambda:shifted_inputs([1.,2.],0))
    reject(lambda:shifted_inputs([1,2],True));reject(lambda:shifted_inputs(np.array([1,2],dtype=np.uint8),300))
    reject(lambda:check_shift([1,2],[1,2],0))
    reject(lambda:cross_attention(h,e,wq,wk,wv,np.zeros((2,3),bool)))
    reject(lambda:cross_attention(h,e,wq,wk,wv,np.ones((3,2),bool)))
    reject(lambda:cross_attention(h,e,wq,wk,wv,np.ones((2,3),int)))
    reject(lambda:cross_attention(h,e,wq,wk,wv,mask,[1,0]))
    reject(lambda:decoder_post(t['d'][None],t['e'],sw,cw,fp,[ln]*3,sm,mask))
    reject(lambda:decoder_post(t['d'].astype(complex),t['e'],sw,cw,fp,[ln]*3,sm,mask))
    reject(lambda:decoder_post(t['d'],t['e'],sw,cw,fp,[ln]*2,sm,mask))
    bad=(cw[0],cw[1][:,:1],cw[2],cw[3])
    reject(lambda:decoder_post(t['d'],t['e'],sw,bad,fp,[ln]*3,sm,mask))
    reject(lambda:decoder_post(t['d'],t['e'],sw,(*cw[:3],np.ones((2,1))),fp,[ln]*3,sm,mask))
    reject(lambda:decoder_post(t['d'],t['e'],sw,cw,fp,[(ln[0],ln[1],0)]*3,sm,mask))
    reject(lambda:decoder_post(np.full((2,3),np.nan),t['e'],sw,cw,fp,[ln]*3,sm,mask))
    original=t['d'].copy(); eo=t['e'].copy()
    decoder_post(t['d'],t['e'],sw,cw,fp,[ln]*3,sm,mask)
    assert np.array_equal(original,t['d']) and np.array_equal(eo,t['e'])
    i,ta=shifted_inputs([11,12,13],0); assert check_shift(i,ta,0)
    assert list(i)==[0,11,12] and list(ta)==[11,12,13]
    qp=np.array([0,1,2]);kp=np.array([2,0,1]);km=causal_allowed(qp,kp,np.ones(3,bool))
    close(km,cm[:,[2,0,1]])
    checks.append(f'입력/Target 이동·원래 위치·비제자리·거부{rejected}')
    result=dict(상태='검사 통과',독립계산='Decimal70/rtol=atol=5e-12',생성사례=100,거부조건=rejected,검사=checks,
                한계='유한 수치·작성자 자체 검증. 독립 심사/학습/독자 실증은 미실시.')
    Path(__file__).with_name('ARCHITECTURE_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
