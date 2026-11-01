"""Head별 값 폭이 달라도 대응 좌표를 함께 옮기는 해설 코드."""
import numpy as np


def reorder(heads, masks, wo, order):
    if sorted(order) != list(range(len(heads))):
        raise ValueError("order는 모든 Head를 한 번씩 포함해야 한다")
    widths = [np.asarray(t[2]).shape[1] for t in heads]
    offsets = np.cumsum([0] + widths)
    coords = np.concatenate([np.arange(offsets[r], offsets[r+1])
                             for r in order])
    return ([heads[r] for r in order], [masks[r] for r in order],
            wo[coords, :])
