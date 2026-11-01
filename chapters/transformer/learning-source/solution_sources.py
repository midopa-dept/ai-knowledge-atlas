"""독립 연습의 출처/순열/조건 변경 실험."""
import numpy as np
from sources import cross_attention


def compare_providers(h, z, z_new, wq, wk, wv, allowed):
    """같은 요청·정책에서 제공자만 바꾸어 중간값을 비교한다."""
    before = cross_attention(h, z, wq, wk, wv, allowed)
    after = cross_attention(h, z_new, wq, wk, wv, allowed)
    return {name: (a, b) for name, a, b in
            zip(["Q", "K", "V", "S", "A", "O"], before, after)}


def permute_provider(h, z, wq, wk, wv, allowed, order):
    """Z와 그 열의 허용 관계를 함께 옮긴다."""
    order = np.asarray(order)
    if sorted(order.tolist()) != list(range(len(z))):
        raise ValueError("모든 제공 위치를 한 번씩 포함해야 한다")
    return cross_attention(h, z[order], wq, wk, wv, allowed[:, order])
