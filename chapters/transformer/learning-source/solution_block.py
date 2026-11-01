"""독립 연습의 새 입력/매개변수. 상세 손계산은 별도 해설에 있다."""
import numpy as np
from block import post_ln, pre_ln


def exercise_inputs(number):
    if number == 1:
        x = np.array([[2.,1.,0.],[0.,1.,2.]])
        head = (np.array([[1.],[0.],[0.]]),
                np.array([[np.log(2.)],[0.],[0.]]),
                np.array([[1.,0.],[0.,1.],[0.,1.]]))
        wo = np.array([[.5,0.,-.5],[0.,.5,.5]])
        ffn = (np.array([[1.,-1.],[0.,1.],[1.,0.]]),
               np.array([-.5,.25]), wo.copy(), np.array([0.,.1,-.1]))
        ln = (np.ones(3),np.zeros(3),.04)
    elif number == 2:
        x = np.array([[1.,3.],[2.,0.]])
        head = (np.array([[1.],[0.]]),
                np.array([[0.],[np.log(2.)]]),np.eye(2))
        wo = .5*np.eye(2)
        ffn = (np.array([[1.,-1.],[1.,1.]]), np.array([-.5,.25]),
               np.array([[1.,0.],[0.,-1.]]),np.array([.2,-.1]))
        ln = (np.array([1.,2.]),np.array([.5,0.]),.25)
    else:
        raise ValueError("예제 번호는 1 또는 2다")
    return x,[head],wo,ffn,ln,ln


if __name__ == "__main__":
    np.set_printoptions(precision=6,suppress=True)
    for num in (1,2):
        for mode,fn in [("post",post_ln),("pre",pre_ln)]:
            _,t=fn(*exercise_inputs(num))
            print("연습",num,mode)
            for key in ("attention_input","heads","attention","first_sum",
                        "norm1","u","ffn_input","ffn_linear","activated",
                        "ffn","second_sum","norm2","y"):
                print(key,t[key],sep="\n")


def diagnose_missing_ln():
    """연습22: 새로운 입력으로 정상 두 trace와 LN₂ 생략을 대조한다."""
    from block import example_inputs, feed_forward, residual
    inputs = list(example_inputs())
    inputs[0] = np.array([[-.5, 2., 1.], [3., -1., .25]])
    post, pt = post_ln(*inputs)
    pre, rt = pre_ln(*inputs)
    wrong_update, wrong_ffn = feed_forward(rt["u"], *inputs[3])
    wrong = residual(rt["u"], wrong_update)
    print("연습22 Post 반환", post, sep="\n")
    print("연습22 Pre 반환", pre, sep="\n")
    print("오류 FFN 입력", rt["u"], sep="\n")
    print("오류 첫 선형", wrong_ffn["linear"], sep="\n")
    print("오류 반환", wrong, sep="\n")
    assert not np.allclose(rt["ffn_input"], rt["u"])
    assert not np.allclose(pre, wrong)
    return pt, rt, wrong


if __name__ == "__main__":
    diagnose_missing_ln()
