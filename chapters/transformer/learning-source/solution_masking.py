"""독립 연습의 누출 진단과 미래 차단·과거 보존 수정."""
import numpy as np
from masking import causal_allowed


def diagnose_and_repair(query_pos, key_pos, key_valid, wrong):
    correct = causal_allowed(query_pos, key_pos, key_valid)
    wrong = np.asarray(wrong)
    if wrong.dtype != np.bool_ or wrong.shape != correct.shape:
        raise ValueError("검사할 Mask의 규약/크기가 다르다")
    # 잘못 연 경로와 놓친 과거를 각각 (질의 배열 행, 키 배열 열)로 반환한다.
    extra = np.argwhere(wrong & ~correct)
    missing = np.argwhere(correct & ~wrong)
    return extra, missing, correct
