"""대표 두 레이어의 구조상 항목 판정. 숫자 우연 일치를 계약상 보장으로 바꾸지 않는다."""


def validity_matrix(change, n=3, changed_position=1, changed_head=0):
    """동일 위치 순서·위치별 입력·기본 Causal을 전제로 생성원 영향 범위를 반환한다."""
    supported = {"추가", "토큰", "Absolute", "RoPE", "W_Q", "W_K", "W_V", "W_O",
                 "FFN", "LN1", "LN2", "기존Mask", "새QueryMask", "Readout", "다른Prefix"}
    if change not in supported:
        raise ValueError("알려지지 않은 변경안")
    rows = []
    for layer in range(2):
        for head in range(2):
            for p in range(n):
                for kind in ("K", "V"):
                    state, why = "재사용", "생성원과 투영 계약 유지"
                    if change == "다른Prefix":
                        state, why = "추가 확인", "공통 Token·위치·모델·접근 경로 확인 필요"
                    elif layer == 0:
                        direct = ((change in {"토큰", "Absolute"} and p == changed_position) or
                                  change == "LN1" or
                                  (change == "RoPE" and p == changed_position and kind == "K") or
                                  (change == "W_" + kind and head == changed_head))
                        if direct:
                            state, why = "재계산 대상", "해당 입력/정규화/투영/회전 계약 변경"
                    else:
                        affected = False
                        if change in {"토큰", "Absolute", "RoPE"}:
                            affected = p >= changed_position
                        elif change in {"W_Q", "W_K"}:
                            # 위치0은 제공 Key가 하나라 가중치1. Q/K만 바뀌어도 반환은 유지.
                            affected = p > 0
                        elif change in {"W_V", "W_O", "FFN", "LN1", "LN2"}:
                            affected = True
                        elif change == "기존Mask":
                            affected = p == changed_position
                        if affected:
                            state, why = "추가 확인/재계산", "첫 Block 반환이 달라질 수 있어 둘째 레이어 N1·투영 입력 재검토"
                    rows.append(dict(layer=layer + 1, head=head + 1, position=p,
                                     kind=kind, state=state, reason=why))
    return rows
