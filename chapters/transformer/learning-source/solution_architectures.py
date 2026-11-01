"""새 독립 Cross/Encoder 변형의 수치 풀이를 재현한다."""
import numpy as np
from architectures import full_allowed, exact_cross, parameters
from sources import cross_attention, project
from block import layer_norm, residual


def problem_cross():
    """독립 문제10/11: 주어진 E, 두 요청·세 제공, LN까지."""
    h = np.array([[1.,1.],[2.,0.]])
    e = np.array([[0.,1.],[1.,0.],[1.,1.]])
    wq = np.eye(2); wk = np.sqrt(2.)*np.log(2.)*np.eye(2)
    wv = np.array([[1.,2.],[-1.,1.]])
    results = {}
    for name, mask in [("전체",full_allowed(2,np.ones(3,bool))),
                       ("잘못된_삼각형",np.tri(2,3,dtype=bool))]:
        trace = cross_attention(h,e,wq,wk,wv,mask)
        r = residual(h,trace[-1])
        u, norm = layer_norm(r,np.ones(2),np.zeros(2),.25)
        results[name] = dict(q=trace[0],k=trace[1],v=trace[2],s=trace[3],a=trace[4],o=trace[5],r=r,u=u,norm=norm)
    return results


def main():
    np.set_printoptions(precision=6,suppress=True)
    for name, trace in problem_cross().items():
        print(name)
        for k,v in trace.items():print(k,v,sep='\n')
    x=np.array([[1.,0.,2.],[0.,2.,1.],[2.,1.,0.]])
    p,wo,_,ln=parameters()
    mask=np.array([[True,False,True],[True,True,True],[True,True,True]])
    t=cross_attention(x,x,*p,mask)
    r=x+project(t[-1],wo)
    print('독립 문제3 첫 요청\n',t[-2][0],t[-1][0],r[0],layer_norm(r,*ln)[0][0])
    h,e,q,k,v,mask=exact_cross()
    mask[:,2]=False
    t=cross_attention(h,e,q,k,v,mask,np.array([True,False]))
    print('독립 문제15 A/O',t[-2],t[-1],sep='\n')


if __name__=='__main__':main()
