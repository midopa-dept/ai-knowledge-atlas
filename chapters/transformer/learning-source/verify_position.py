"""독립 Decimal 스칼라/Taylor·고정 유리수·기하학 기준으로 위치 계산 검산."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from pathlib import Path
import contextlib, io, json, math
import numpy as np
from position import (positions, frequencies, sinusoidal, add_absolute, absolute_attention,
                      relative_bias, biased_attention, rope, rotary_attention, comparison_inputs)
from sources import project
from masking import masked_attention, causal_allowed
with contextlib.redirect_stdout(io.StringIO()):
    from solution_position import split_half

PI = D("3.141592653589793238462643383279502884197169399375105820974944592307816406286")


def decimal(x):
    return x if isinstance(x, D) else D(str(float(x)))


def trig(angle):
    """NumPy/math 삼각함수를 호출하지 않는 축소 각도의 Taylor 합."""
    with localcontext() as ctx:
        ctx.prec = 75
        x = angle % (2*PI)
        if x > PI:
            x -= 2*PI
        if x < -PI:
            x += 2*PI
        sine, cosine, st, ct = x, D(1), x, D(1)
        for n in range(1, 180):
            st *= -x*x / D((2*n)*(2*n+1))
            ct *= -x*x / D((2*n-1)*(2*n))
            sine += st
            cosine += ct
            if abs(st) + abs(ct) < D("1e-72"):
                break
        else:
            raise AssertionError("Taylor 합의 수렴 조건 실패")
        return sine, cosine


def scalar_rotate(rows, pos, theta):
    out = []
    for row, p in zip(rows, pos):
        result = []
        for r, t in enumerate(theta):
            sn, cs = trig(D(int(p))*decimal(t))
            a, b = decimal(row[2*r]), decimal(row[2*r+1])
            result.extend([cs*a-sn*b, sn*a+cs*b])
        out.append(result)
    return out


def scalar_project(rows, weights, encoding=None):
    result = []
    for i, row in enumerate(rows):
        coords = [decimal(x) + (decimal(encoding[i][t]) if encoding is not None else 0)
                  for t, x in enumerate(row)]
        result.append([sum(coords[t]*decimal(weights[t][r]) for t in range(len(row)))
                       for r in range(len(weights[0]))])
    return result


def scalar_attention(q, k, v, allowed, active, bias=None):
    """중첩 스칼라 합·Decimal 지수/제곱근으로 S/A/O를 만든다."""
    width, value_width = len(q[0]), len(v[0])
    scores, weights, outputs = [], [], []
    for i, row in enumerate(q):
        s = [sum(decimal(a)*decimal(b) for a, b in zip(row, key))/D(width).sqrt()
             + (decimal(bias[i][j]) if bias is not None else 0) for j, key in enumerate(k)]
        a = [D(0)] * len(k)
        if active[i]:
            cols = [j for j in range(len(k)) if allowed[i][j]]
            high = max(s[j] for j in cols)
            ex = [(s[j]-high).exp() for j in cols]
            total = sum(ex)
            for j, e in zip(cols, ex):
                a[j] = e/total
        o = [sum(a[j]*decimal(v[j][r]) for j in range(len(k))) for r in range(value_width)]
        scores.append(s); weights.append(a); outputs.append(o)
    return scores, weights, outputs


def close(actual, expected, tol=3e-12):
    np.testing.assert_allclose(actual, np.array(expected, dtype=float), rtol=tol, atol=tol)


def rational_rows(values):
    return [[float(F(x)) for x in row] for row in values]


with localcontext() as ctx:
    ctx.prec = 70
    x, wq, wk, wv, e, p, table = comparison_inputs()
    q, k, v = project(x, wq), project(x, wk), project(x, wv)
    b = np.ones((3, 3), dtype=bool); active = np.ones(3, dtype=bool)
    absolute = absolute_attention(x, x, e, e, wq, wk, wv, b)
    bias_result = biased_attention(q, k, v, p, p, table, b)
    rotary = rotary_attention(q, k, v, p, p, [math.pi/2], b)
    # 고정 유리수 기준은 실행 함수의 출력에서 만들지 않는다.
    expected_absolute = rational_rows([["1/4","1/4","1/2"],
                                       ["1/5","2/5","2/5"],
                                       ["1/6","1/6","2/3"]])
    expected_bias = rational_rows([["2/7","4/7","1/7"],
                                   ["1/2","1/6","1/3"],
                                   ["1/13","9/13","3/13"]])
    expected_rope = rational_rows([["4/7","2/7","1/7"],
                                   ["1/4","1/2","1/4"],
                                   ["1/7","2/7","4/7"]])
    close(absolute[4], expected_absolute); close(absolute[5], [[23/4],[28/5],[13/2]])
    close(bias_result[3], expected_bias); close(bias_result[4], [[32/7],[9/2],[71/13]])
    close(rotary[3], expected_rope); close(rotary[4], [[26/7],[5],[44/7]])
    close(rope([[2,1],[2,1],[2,1]], [0,1,2], [math.pi/2]), [[2,1],[-1,2],[-2,-1]])
    close(rope([[3,-2]], [-1], [math.pi/2]), [[-2,-3]])
    # 직교성·길이·상대 내적은 고정 좌표와 별도 행렬곱으로도 확인한다.
    def rotation(a):
        return np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
    for angle in [0., math.pi/2, math.pi, -.73]:
        r = rotation(angle)
        close(r.T @ r, np.eye(2))
        z = np.array([2.,-3.]); close(np.dot(r@z, r@z), 13)
    close(rotation(.31).T @ rotation(-.77), rotation(-1.08))
    # 4차원 고정 정답과 상대 블록식. 여러 좌표의 scaling은 sqrt4다.
    q4, k4 = [[1,0,0,2]], [[0,1,1,0]]
    theta4 = [math.pi/2, math.pi/4]
    q4r, k4r = rope(q4,[1],theta4), rope(k4,[2],theta4)
    close(q4r, [[0,1,-math.sqrt(2),math.sqrt(2)]])
    close(k4r, [[0,-1,0,1]])
    close((q4r @ k4r.T)/2, [[(-1+math.sqrt(2))/2]])
    # 앞 절 국소 보강의 유리수/스칼라 기준도 새 위치 코드와 독립이다.
    assert F(2,9)*1+F(2,9)*4 == F(10,9)
    assert F(1,3)*(-1)+F(1,9)*3 == 0
    close(math.sqrt(2)*math.log(2)/math.sqrt(2), math.log(2))
    close(math.sqrt(3)*math.log(3)/math.sqrt(3), math.log(3))
    # 본문의 Sinusoidal 표는 math 스칼라와 별도로 대조한다.
    got = sinusoidal([0,1,2,3], 4)
    wanted = [[math.sin(i),math.cos(i),math.sin(.01*i),math.cos(.01*i)] for i in range(4)]
    close(got, wanted)
    for a, t in [(0,1),(2,3)]:
        close(np.dot(sinusoidal([a],4)[0],sinusoidal([t],4)[0]),
              math.cos(a-t)+math.cos(.01*(a-t)))
    assert math.cos(3) < math.cos(4)
    # 부호 오류가 드러나는 q/k: cos항만 시험하면 놓칠 수 있다.
    wrong_sign = np.array([1.,0.]) @ rotation(-math.pi/2) @ np.array([0.,1.])
    right_sign = np.array([1.,0.]) @ rotation(math.pi/2) @ np.array([0.,1.])
    close(wrong_sign,1); close(right_sign,-1)
    # 실제 위치 재배열·Causal과 결합: 같은 출력의 우연한 오류도 진단한다.
    order=np.array([2,0,1]); allow=causal_allowed(p,p,np.ones(3,dtype=bool))
    original=rotary_attention(q,k,v,p,p,[math.pi/2],allow)
    ordered=rotary_attention(q,k[order],v[order],p,p[order],[math.pi/2],allow[:,order])
    for a,c in [(0,0),(1,1)]:
        close(ordered[a], original[c] if a==0 else original[c][order])
    close(ordered[2],original[2][:,order]); close(ordered[3],original[3][:,order])
    close(ordered[4],original[4]); close(original[4],[[2],[4],[44/7]])
    wrong=rotary_attention(q,k[order],v[order],p,p,[math.pi/2],allow[:,order])
    close(wrong[4][1], [3])
    twice_wrong=rotary_attention(q,k[order],v[order],p,p,[math.pi/2],allow)
    close(twice_wrong[4][1], [4]); assert twice_wrong[3][1,0] > 0
    # 새 문항 p07/p12/p24의 유리수 기준과 가산/값 변화.
    qp=[1,3]; kp=[0,2,3]; tq={d:d*math.log(2) for d in range(-5,6)}
    kk=np.array([[math.sqrt(2)*math.log(2),0],[0,0],[-math.sqrt(2)*math.log(2),0]])
    new=biased_attention([[1,0],[1,0]],kk,[[1],[4],[10]],qp,kp,tq,np.ones((2,3),bool))
    close(new[3],[[32/37,4/37,1/37]]*2);close(new[4],[[58/37]]*2)
    new=rotary_attention([[1,1]],[[math.sqrt(2)*math.log(2),0]]*2,
                         [[1],[7]],[1],[0,2],[math.pi/2],np.ones((1,2),bool))
    close(new[3],[[1/5,4/5]]);close(new[4],[[29/5]])
    ev=e.copy();ev[1,2]=1
    abs_v=absolute_attention(x,x,ev,ev,wq,wk,wv,b)
    close(abs_v[3],absolute[3]);close(abs_v[5],[[6],[6],[20/3]])
    def cross_case(shift):
        h=[[1,0]]; z=[[1,0],[1,0]]; eh=[[0,1+shift]]; ez=[[0,shift],[0,2+shift]]
        q1,k1,_,s1,a1,_=absolute_attention(h,z,eh,ez,np.eye(2),
            math.sqrt(2)*math.log(2)*np.eye(2),np.eye(2),np.ones((1,2),bool))
        return s1,a1,a1@np.array([[2.],[8.]])
    close(cross_case(0)[1],[[1/5,4/5]]);close(cross_case(0)[2],[[34/5]])
    close(cross_case(1)[1],[[1/17,16/17]]);close(cross_case(1)[2],[[130/17]])
    # seed를 고정해 길이·짝수 폭·값 폭·위치·Mask·비활성을 바꾼다.
    rng=np.random.default_rng(1060567)
    scalar_cases=100
    for case in range(scalar_cases):
        m,n,d,dv=int(rng.integers(1,5)),int(rng.integers(1,6)),2*int(rng.integers(1,4)),int(rng.integers(1,4))
        qr,kr,vr=rng.normal(size=(m,d)),rng.normal(size=(n,d)),rng.normal(size=(n,dv))
        qp,kp=rng.integers(-7,8,m),rng.integers(-7,8,n)
        theta=rng.uniform(-1.2,1.2,d//2)
        allowed=rng.random((m,n))>.3;allowed[:,0]=True
        active=rng.random(m)>.15
        rotated=rotary_attention(qr,kr,vr,qp,kp,theta,allowed,active)
        sq,sk=scalar_rotate(qr,qp,theta),scalar_rotate(kr,kp,theta)
        close(rotated[0],sq);close(rotated[1],sk)
        ss,sa,so=scalar_attention(sq,sk,vr,allowed,active)
        close(rotated[2],ss);close(rotated[3],sa);close(rotated[4],so)
        # 각 q/k쌍의 원래 내용에서 상대각만 써 계산한 별도 분자.
        relative=[]
        for i in range(m):
            row=[]
            for j in range(n):
                total=D(0)
                for r,t in enumerate(theta):
                    sn,cs=trig(D(int(kp[j])-int(qp[i]))*decimal(t))
                    a,bb,c,dd=map(decimal,[qr[i,2*r],qr[i,2*r+1],kr[j,2*r],kr[j,2*r+1]])
                    total+=(a*c+bb*dd)*cs+(bb*c-a*dd)*sn
                row.append(total/D(d).sqrt())
            relative.append(row)
        close(rotated[2],relative)
        close(np.sum(rotated[0]**2,axis=1),np.sum(qr**2,axis=1))
        shifted=rotary_attention(qr,kr,vr,qp+11,kp+11,theta,allowed,active)
        for a,c in zip(rotated[2:],shifted[2:]):close(a,c)
        perm=rng.permutation(n)
        moved=rotary_attention(qr,kr[perm],vr[perm],qp,kp[perm],theta,allowed[:,perm],active)
        close(moved[2],rotated[2][:,perm]);close(moved[3],rotated[3][:,perm]);close(moved[4],rotated[4])
        # 편향 표를 스칼라 기준에서 따로 조회한다.
        tab={delta:float(rng.normal()) for delta in range(-14,15)}
        tr=biased_attention(qr,kr,vr,qp,kp,tab,allowed,active)
        scalar_bias=[[tab[int(qp[i])-int(kp[j])] for j in range(n)] for i in range(m)]
        close(tr[1],scalar_bias)
        ss,sa,so=scalar_attention(qr,kr,vr,allowed,active,scalar_bias)
        close(tr[2],ss);close(tr[3],sa);close(tr[4],so)
        shift_b=biased_attention(qr,kr,vr,qp+11,kp+11,tab,allowed,active)
        for a,c in zip(tr,shift_b):close(a,c)
        # 다른 길이/입력 폭의 absolute 투영을 중첩 스칼라 합으로 확인한다.
        ih,iz=int(rng.integers(1,5)),int(rng.integers(1,5))
        h,z=rng.normal(size=(m,ih)),rng.normal(size=(n,iz))
        eh,ez=rng.normal(size=h.shape),rng.normal(size=z.shape)
        wqq,wkk,wvv=rng.normal(size=(ih,d)),rng.normal(size=(iz,d)),rng.normal(size=(iz,dv))
        ar=absolute_attention(h,z,eh,ez,wqq,wkk,wvv,allowed,active)
        aq,ak,av=scalar_project(h,wqq,eh),scalar_project(z,wkk,ez),scalar_project(z,wvv,ez)
        for a,c in zip(ar[:3],[aq,ak,av]):close(a,c)
        for a,c in zip(ar[3:],scalar_attention(aq,ak,av,allowed,active)):close(a,c)
        # 같은 수학적 쌍의 저장 순서를 검사한다.
        to_split=np.r_[np.arange(0,d,2),np.arange(1,d,2)]
        sr=split_half(qr[:,to_split],qp,theta)
        close(sr,rotated[0][:,to_split])
        assert np.all(rotated[3][~allowed]==0)
        close(rotated[3][active].sum(axis=1),np.ones(active.sum()))
        assert np.all(rotated[4][~active]==0)
        # 회전은 입력 배열을 직접 바꾸지 않는다.
        before=qr.copy();rope(qr,qp,theta);np.testing.assert_array_equal(qr,before)

    rejections=[
        lambda:rope([[1,2,3]],[0],[1]),
        lambda:rope([[1,2]],[0,1],[1]),
        lambda:rope([[1,2]],[.5],[1]),
        lambda:rope([[1,2]],[True],[1]),
        lambda:rope([[1,2]],[2**31],[1]),
        lambda:rope([[1,2]],[0],[1,2]),
        lambda:rope([[1,2]],[0],[math.inf]),
        lambda:rope([[math.nan,2]],[0],[1]),
        lambda:rope([[1,2]],[2],[1e308]),
        lambda:sinusoidal([0],3),
        lambda:sinusoidal([0],4,1),
        lambda:sinusoidal([],4),
        lambda:add_absolute([[1,2]],[[1]]),
        lambda:add_absolute([[1e308]],[[1e308]]),
        lambda:relative_bias([0],[1],{0:0}),
        lambda:relative_bias([0],[0],{0:math.inf}),
        lambda:relative_bias([0],[0],{False:0}),
        lambda:biased_attention([[1,0]],[[1,0]],[[1]],[0,1],[0],{0:0,1:0},[[True]]),
        lambda:rotary_attention([[1,0]],[[1,0]],[[1]],[0],[0],[1],[[False]]),
        lambda:rotary_attention([[1,0]],[[1,0]],[[1]],[0],[0],[1],[[1]]),
        lambda:split_half([[1,2,3]],[0],[1]),
    ]
    for call in rejections:
        try:call()
        except ValueError:pass
        else:raise AssertionError("잘못된 입력을 거부하지 않았다")
    report={'독립 Decimal 정밀도':70,'Taylor 삼각함수 정밀도':75,
            '생성 사례':scalar_cases,'각 사례의 세 경로 S/A/O':'통과',
            '직접 회전/상대식·길이·동시 이동·재배열·Split-half':'통과',
            '고정 Fraction/90도/180도/4차원/문항 정답':'통과',
            '잘못된 입력 거부':len(rejections),'비교 허용오차':'rtol/atol 3e-12',
            '범위':'유한 CPU float64 시험이며 본문 증명·독립 심사·학습효과 실증과 별개'}
    (Path(__file__).parent/'NUMERICAL_POSITION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
