"""Head별 투영·집계·Concat·출력 변환. 배치·편향·dropout은 생략한다."""
import numpy as np
from sources import matrix, project
from masking import masked_attention


def multi_head(h, z, projections, wo, masks=None, active=None):
    """H가 요청, Z가 제공. Self에서는 같은 배열을 두 번 전달한다."""
    h, z, wo = matrix(h), matrix(z), matrix(wo)
    if not projections:
        raise ValueError("Head가 하나 이상 필요하다")
    if masks is None:
        masks = [np.ones((len(h), len(z)), dtype=bool)
                 for _ in projections]
    if len(masks) != len(projections):
        raise ValueError("각 Head에 하나의 Mask를 명시해야 한다")
    traces, outputs = [], []
    for (wq, wk, wv), allowed in zip(projections, masks):
        # 입력의 모든 좌표에서 Head별로 다른 학습 투영을 만든다.
        q = project(h, wq)
        k = project(z, wk)
        v = project(z, wv)
        # 비교 폭 검사·scaling·허용 열 Softmax·AV는 앞 절 함수다.
        s, a, o = masked_attention(q, k, v, allowed, active)
        traces.append(dict(q=q, k=k, v=v, s=s, a=a, o=o))
        outputs.append(o)
    # 행은 같은 요청 위치다. Head의 값 좌표들을 마지막 축에 잇는다.
    c = np.concatenate(outputs, axis=1)
    if wo.shape[0] != c.shape[1]:
        raise ValueError("W_O의 입력 폭은 Concat 폭과 같아야 한다")
    y = project(c, wo)
    return traces, c, y


def example_inputs():
    """본문 대표 예제. 투영은 학습 결과가 아닌 교육용 수치다."""
    x = np.array([[1., 0.], [0., 1.], [1., -1.]])
    head1 = (np.array([[1.], [0.]]),
             np.array([[np.log(2.)], [0.]]), np.array([[2.], [1.]]))
    head2 = (np.array([[0.], [1.]]),
             np.array([[0.], [np.log(3.)]]), np.array([[-1.], [3.]]))
    wo = np.array([[1., 2.], [-1., 1.]])
    return x, [head1, head2], wo
