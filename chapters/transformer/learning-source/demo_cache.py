"""대표 계산·다른 Head 폭 통합 과제·RoPE 전 중간값을 반올림 없이 저장한다."""
from pathlib import Path
import json
from kv_cache import example_model, transfer_model, rope_model, full_prefix, incremental, serial

root = Path(__file__).resolve().parent
records = {}
for name, model, tokens, positions in [
    ("대표", example_model(), [0, 1, 2], [0, 1, 2]),
    ("새통합", transfer_model(), [2, 0, 1], [1, 3, 4]),
    ("RoPE", rope_model(), [2, 0, 1], [1, 3, 4])]:
    old_h, old_logits, past, old_trace = full_prefix(model, tokens[:-1], positions[:-1])
    h, logits, cache, trace = full_prefix(model, tokens, positions)
    inc_h, inc_logits, updated, inc_trace = incremental(
        model, tokens[:-1], positions[:-1], tokens[-1], positions[-1], past)
    records[name] = dict(model=model, tokens=tokens, positions=positions,
                         prefix_h=old_h, prefix_logits=old_logits, old_trace=old_trace,
                         past=past, full_h=h, logits=logits, cache=cache, trace=trace,
                         inc_h=inc_h, inc_logits=inc_logits, updated=updated, inc_trace=inc_trace)
    print(name, "새 위치 최종 표현:", " ".join(f"{x:.6f}" for x in h[-1]))
    for index, t in enumerate(inc_trace):
        print("레이어", index + 1, "새 K:", [serial(a["k"])[0] for a in t["heads"]])
(root / "NUMERICAL_CACHE.json").write_text(json.dumps(serial(records), ensure_ascii=False, indent=2) + "\n")
