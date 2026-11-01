"""손계산용 Post-LN Encoder–Decoder를 Token 표에서 두 생성 단계까지 잇는다."""
import json
from pathlib import Path
import numpy as np
from architectures import integrated
from kv_cache import serial


def run():
    source_ids = [0, 1, 2]
    source_table = np.array([[1., 0., 1.], [0., 1., 1.], [1., 1., 0.]])
    source_positions = np.array([[0., 0., 1.], [0., 1., 0.], [1., 0., 0.]])
    target_table = np.array([[1., 0., 1.], [0., 1., 1.], [1., 1., 0.], [1., 0., 0.]])
    # Target ID0=BOS,1=A,2=B,3=C. Logit 열0/1/2는 A/B/C다.
    z = source_table[source_ids] + source_positions
    prefix = [0, 1]
    records = []
    for _ in range(2):
        p = np.zeros((len(prefix), 3)); p[:, 2] = np.arange(len(prefix))
        d = target_table[prefix] + p
        record = integrated(z, d)
        chosen = int(record['logits'].argmax()) + 1
        record.update(source_ids=source_ids, prefix=prefix.copy(),
                      target_embedding=target_table[prefix], target_position=p,
                      chosen_target_id=chosen)
        records.append(record)
        prefix.append(chosen)
    result = dict(source_table=source_table, source_position=source_positions,
                  target_table=target_table, rounds=records, selected_sequence=prefix)
    root = Path(__file__).resolve().parent
    (root/'FLAGSHIP_INTEGRATED.json').write_text(json.dumps(serial(result), ensure_ascii=False, indent=2)+'\n')
    for i, r in enumerate(records):
        print('단계', i+1, '입력', r['prefix'], 'Logit', r['logits'], '선택 ID', r['chosen_target_id'])
        print('최종 Decoder 반환:', r['decoder']['y'][-1])
    return result


if __name__ == '__main__':
    run()
