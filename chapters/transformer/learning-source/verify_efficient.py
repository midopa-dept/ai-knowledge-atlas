"""별도 스칼라/유리수 기준, 그래프 열거, 비용, 거부 조건과 변경 대조."""
import json
from pathlib import Path
from fractions import Fraction
import numpy as np
from efficient import *
from reference_efficient import decimal_attention, fraction_kernel, enumerated_paths
from demo_efficient import examples


def close(a,b):
    np.testing.assert_allclose(a,b,rtol=4e-12,atol=4e-12)


def run():
    rng=np.random.default_rng(570)
    cases=0
    for case in range(120):
        n=int(rng.integers(1,8)); dk=int(rng.integers(1,5)); dv=int(rng.integers(1,4)); r=int(rng.integers(1,5))
        q,k,v=rng.normal(size=(n,dk)),rng.normal(size=(n,dk)),rng.normal(size=(n,dv))
        originals=[x.copy() for x in (q,k,v)]
        p=np.arange(1,n+1); width=int(rng.integers(1,n+3))
        b=causal_mask(p,p,width)
        actual=sparse_attention(q,k,v,b)
        reference=decimal_attention(q.tolist(),k.tolist(),v.tolist(),b.tolist())
        for a,e in zip(actual,reference): close(a,e)
        for a,e in zip((q,k,v),originals): np.testing.assert_array_equal(a,e)
        qf,kf=rng.integers(1,6,size=(n,r)).astype(float),rng.integers(1,6,size=(n,r)).astype(float)
        vint=rng.integers(-5,6,size=(n,dv)).astype(float)
        direct=kernel_direct(qf,kf,vint)[2]
        s,z,factor=kernel_factorized(qf,kf,vint)
        close(direct,factor)
        close(direct,[[float(x) for x in row] for row in fraction_kernel(qf.tolist(),kf.tolist(),vint.tolist(),np.ones((n,n),bool))])
        states,prefix=kernel_prefix(qf,kf,vint)
        close(prefix,kernel_direct(qf,kf,vint,causal_mask(p,p))[2])
        for i,(si,zi) in enumerate(states):
            # 상태의 모든 원소를 명시적 좌표 반복으로 별도 검산한다.
            expected_s=[[sum(Fraction(int(kf[j,t]))*Fraction(int(vint[j,c])) for j in range(i+1)) for c in range(dv)] for t in range(r)]
            close(si,[[float(x) for x in row] for row in expected_s])
            close(zi,[sum(kf[j,t] for j in range(i+1)) for t in range(r)])
        if n>1:
            future=vint.copy(); future[-1]+=10
            close(kernel_prefix(qf,kf,future)[1][:-1],prefix[:-1])
            assert not np.allclose(kernel_factorized(qf,kf,future)[2][0],factor[0])
        # 제공 열 재배열은 원위치 Mask와 함께 적용해야 한다.
        order=rng.permutation(n)
        reordered=sparse_attention(q,k[order],v[order],causal_mask(p,p[order],width))
        close(reordered[2],actual[2]); close(reordered[1][:,np.argsort(order)],actual[1])
        masks=[]
        for layer in range(3):
            m=rng.random((n,n))<.3; np.fill_diagonal(m,True); masks.append(m)
        history=reachability(masks)
        for depth in range(1,4):
            for source in range(1,n+1):
                expected=enumerated_paths([m.tolist() for m in masks[:depth]],source)
                observed={i+1 for i,deps in enumerate(history[depth]) if source in deps}
                assert observed==expected
        costs=interaction_cost(n,dk,dv,width,r)
        assert costs['local_pairs']==sum(min(i,width) for i in range(1,n+1))==int(b.sum())
        assert costs['factor_multiplications']==n*r*dv+n*r*dv+n*r
        cases+=1
    ex=examples()
    assert ex['full_mask'].sum()==10 and ex['local_mask'].sum()==7 and ex['minimum_1_to_4']==3
    close(ex['full_output'],[[1],[5/3],[7/3],[3]])
    close(ex['local_output'],[[1],[5/3],[13/5],[25/7]])
    assert not np.isclose(ex['full_output'][-1],ex['local_output'][-1])
    close(ex['kernel_output'][-1],[3]); close(ex['same_scores_softmax'],[[3.732991837837875]])
    close(ex['prefix_output'],[[1],[2],[9/4],[3]])
    close(ex['future40_prefix'][:3],ex['prefix_output'][:3])
    close(ex['future40_global'],[[21],[15],[129/7],[213/11]])
    close(ex['past10_prefix'],[[10],[2],[9/2],[51/11]])
    b=local_global_mask(); assert b.sum()==11 and minimum_steps(b,1,5)==2
    close(ex['global_output'],[[2],[3],[14/3],[12],[56/3]])
    assert all(j<=i for i,row in enumerate(b) for j,yes in enumerate(row) if yes)
    # 잘못된 global의 미래5→위치3→위치4 누출을 두 층 값으로 확인한다.
    bad=b.copy(); bad[2,:]=True
    zero=np.zeros((5,1)); v=np.array([[2.],[4.],[8.],[16.],[32.]])
    changed=v.copy(); changed[-1]=320
    def two(mask,value):
        first=sparse_attention(zero,zero,value,mask)[2]
        return sparse_attention(zero,zero,first,b)[2]
    close(two(b,v)[:4],two(b,changed)[:4])
    assert not np.isclose(two(bad,v)[3,0],two(bad,changed)[3,0])
    assert 5 in reachability([bad,b])[2][3]
    # 출력 우연 일치가 같은 연산의 보장은 아니다.
    phi=np.array([[1.,0.],[0.,1.],[1.,1.],[2.,1.]])
    states,prefix=kernel_prefix(phi,phi,np.arange(1,5)[:,None])
    close(states[-1][0],[[12],[9]]); close(states[-1][1],[4,3])
    constant=np.ones((4,1))*7
    close(sparse_attention(np.ones((4,1)),np.zeros((4,1)),constant,causal_mask([1,2,3,4],[1,2,3,4],2))[2],constant)
    close(kernel_factorized(phi,phi,constant)[2],constant)
    # 자기 Edge가 없어도 Query의 생성원은 출력에 영향을 줄 수 있다.
    no_self=np.array([[False,True,True],[False,True,False],[False,False,True]])
    assert reachability([no_self])[1][0]=={1,2,3}
    h=np.array([[1.],[0.],[1.]])
    changed_h=h.copy(); changed_h[0]=2
    first=sparse_attention(h,h,h,no_self)[2][0]
    second=sparse_attention(changed_h,changed_h,changed_h,no_self)[2][0]
    assert not np.allclose(first,second)
    # unsigned 원위치라도 아래 경계가 wrap되지 않아야 한다.
    unsigned=np.array([1,2],dtype=np.uint64)
    np.testing.assert_array_equal(causal_mask(unsigned,unsigned,3),[[True,False],[True,True]])
    largest=np.array([np.iinfo(np.int64).max],dtype=np.int64)
    np.testing.assert_array_equal(causal_mask(largest,largest,10**30),[[True]])
    # 거부 검사는 계약 위반별로 구별한다.
    rejected=0
    def reject(fn):
        nonlocal rejected
        try: fn()
        except ValueError: rejected+=1
        else: raise AssertionError('계약 위반을 거부하지 않음')
    reject(lambda: causal_mask([1,1],[1]))
    reject(lambda: causal_mask([1.],[1]))
    reject(lambda: causal_mask([1],[1],0))
    reject(lambda: causal_mask([0],[1]))
    reject(lambda: causal_mask([-1],[1]))
    reject(lambda: causal_mask(np.array([2**63],dtype=np.uint64),[1]))
    reject(lambda: local_global_mask(global_position=3.0))
    reject(lambda: local_global_mask(global_position=True))
    reject(lambda: sparse_attention([[1]],[[1,2]],[[1]],[[True]]))
    reject(lambda: sparse_attention([[1]],[[1]],[[1],[2]],[[True]]))
    reject(lambda: sparse_attention([[1]],[[1]],[[1]],[[1]]))
    reject(lambda: sparse_attention([[1]],[[1]],[[1]],np.zeros((1,1),bool)))
    reject(lambda: sparse_attention([[np.nan]],[[1]],[[1]],np.ones((1,1),bool)))
    reject(lambda: kernel_direct([[-1]],[[1]],[[1]]))
    reject(lambda: kernel_direct([[0]],[[1]],[[1]]))
    reject(lambda: kernel_direct([[1,0]],[[0,1]],[[1]]))
    reject(lambda: kernel_factorized([[1,2]],[[1]],[[1]]))
    reject(lambda: kernel_factorized([[1]],[[np.inf]],[[1]]))
    reject(lambda: kernel_prefix([[1],[2]],[[1]],[[1]]))
    reject(lambda: interaction_cost(4,1,1,2,0))
    reject(lambda: interaction_cost(4,1,1,2,1.0))
    with np.errstate(over='ignore',invalid='ignore'):
        reject(lambda: kernel_factorized([[1],[1]],[[1],[1]],[[1e308],[1e308]]))
        reject(lambda: kernel_prefix([[1],[1]],[[1],[1]],[[1e308],[1e308]]))
        reject(lambda: kernel_factorized([[1e308]],[[1]],[[2]]))
    report={'상태':'작성자 검증 통과','스칼라·유리수생성 사례':cases,'계약 위반 거부':rejected,
            '그래프':'각 생성 사례3층·모든 초기 위치의 경로 열거 대조',
            '명시검사':['10/7쌍','1→4 최소3단계','Global11쌍/1→5 두 단계','Softmax 재정규화',
                       'Kernel 직접/인자 분해','모든 Prefix S/z','미래 불변/과거 양성 대조',
                       '잘못된 Global 두 층 누출','제공 열 재배열','비제자리','조건별 비용'],
            '한계':'유한 사례의 계산 검증이다. 독립 심사·인간 승인·일반 증명과 다르다.'}
    out=Path(__file__).with_name('EFFICIENT_CHECKS.json')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__': run()
