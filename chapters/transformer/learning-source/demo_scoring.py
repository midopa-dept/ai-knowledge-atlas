"""직접 정한 두 요청·세 출처의 본문 수치와 조건 변형을 출력한다."""
import numpy as np
from scoring import scaled_dot_product, softmax_rows

np.set_printoptions(precision=6, suppress=True)
Q = np.array([[1., 0.], [0., 1.]])
K = np.array([[1., 0.], [0., 1.], [1., 1.]])
V = np.array([[2., 0.], [0., 4.], [2., 4.]])
for name, x in zip(("내적", "조정 점수", "가중치", "출력"),
                   scaled_dot_product(Q, K, V)):
    print(name, x.shape)
    print(x)
print("조정 없음", softmax_rows(Q @ K.T))
print("큰 점수의 안정 계산", softmax_rows([[1000., 1001., 999.]]))
print("폭4 비교", softmax_rows([[4., 0.]]), softmax_rows([[2., 0.]]))
