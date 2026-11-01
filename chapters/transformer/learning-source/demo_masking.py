"""본문의 대표 계산·패딩·재배열 누출·수정 후 변화 실험."""
import numpy as np
from masking import causal_allowed, masked_attention, masked_softmax

np.set_printoptions(precision=6, suppress=True)
q = np.ones((3, 1))
k = np.array([[0.0], [np.log(2)], [np.log(3)]])
v = np.array([[2.0, 0], [0, 6], [12, 12]])
mask = causal_allowed([0, 1, 2], [0, 1, 2], [True]*3)
_, unmasked_a, unmasked_o = masked_attention(q, k, v, np.ones((3, 3), bool))
_, a, o = masked_attention(q, k, v, mask)
print("차단 전 A/O:", unmasked_a, unmasked_o, sep="\n")
print("Causal 허용/A/O:", mask.astype(int), a, o, sep="\n")
print("패딩 전/후 비율:")
print(masked_softmax([[0, np.log(3), np.log(4)]], [[True]*3]))
print(masked_softmax([[0, np.log(3), np.log(4)]], [[True, True, False]]))
# 키·값·원래 위치를 함께 옮긴다. tril은 배열 번호만 비교해 틀린다.
order = np.array([2, 0, 1])
kp, kr, vr = np.arange(3)[order], k[order], v[order]
wrong = np.tril(np.ones((3, 3), bool))
fixed = causal_allowed([0, 1, 2], kp, [True]*3)
_, _, bad_o = masked_attention(q, kr, vr, wrong)
_, fixed_a, fixed_o = masked_attention(q, kr, vr, fixed)
print("재배열 키 위치/잘못된 출력/수정 A/O:", kp, bad_o, fixed_a, fixed_o, sep="\n")
# 원래 위치2(y2)를 바꾼다. y1/y2를 예측하는 질의0/1에는 닿으면 안 된다.
changed_k, changed_v = kr.copy(), vr.copy()
changed_k[0, 0], changed_v[0] = np.log(30), [120, -12]
_, _, changed_bad = masked_attention(q, changed_k, changed_v, wrong)
_, _, changed_fixed = masked_attention(q, changed_k, changed_v, fixed)
print("미래 변경 뒤 잘못된/수정 출력:", changed_bad, changed_fixed, sep="\n")
np.testing.assert_array_equal(fixed_o[:2], changed_fixed[:2])
print("허용된 질의0/1의 출력 보존:", np.array_equal(fixed_o[:2], changed_fixed[:2]))
