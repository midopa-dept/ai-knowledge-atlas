"""본문과 다른 특징·값 폭의 독립 계산. CPU에서 직접 합과 인자 합을 대조한다."""
import numpy as np
from efficient import kernel_direct, kernel_factorized, kernel_prefix, causal_mask


def solve_example():
    qf = np.array([[1., 2.], [2., 1.], [1., 1.]])
    kf = np.array([[1., 1.], [2., 0.], [0., 3.]])
    v = np.array([[2., -1.], [0., 4.], [3., 2.]])
    weights, a, direct = kernel_direct(qf, kf, v)
    s, z, factor = kernel_factorized(qf, kf, v)
    assert np.allclose(direct, factor)
    states, prefix = kernel_prefix(qf, kf, v)
    mask = causal_mask([1, 2, 3], [1, 2, 3])
    assert np.allclose(prefix, kernel_direct(qf, kf, v, mask)[2])
    return weights, s, z, direct, prefix


if __name__ == '__main__':
    weights, s, z, direct, prefix = solve_example()
    print('특징 내적', weights.tolist())
    print('S', s.tolist(), 'z', z.tolist())
    print('직접 합과 인자 분해 합', direct.tolist())
    print('Prefix', prefix.tolist())
