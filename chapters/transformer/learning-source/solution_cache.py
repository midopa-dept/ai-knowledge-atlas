"""유제와 독립 과제의 수치 풀이. 문제 입력에는 새 항목의 정답을 넣지 않는다."""
from pathlib import Path
import json
import numpy as np
from kv_cache import example_model, transfer_model, full_prefix, incremental, serial, attention

def guided():
    """새 입력 계약을 먼저 정한 뒤 과거 Cache와 두 레이어를 계산한다."""
    model = example_model()
    model["embedding"][2] = [0., 1.]
    _, _, past, _ = full_prefix(model, [0, 1], [0, 1])
    h, logits, updated, trace = incremental(model, [0, 1], [0, 1], 2, 2, past)
    return dict(h=h, logits=logits, updated=updated, trace=trace), past


answer, past = guided()
answers = dict(유제=answer)
new_k = np.array([[1., -1.]]) @ np.eye(2)
new_v = np.array([[1., -1.]]) @ np.array([[1.], [2.]])
k = np.concatenate((np.eye(2), new_k))
v = np.concatenate((np.array([[2.], [4.]]), new_v))
s,a,o = attention(np.array([[1.,2.]]), k, v, np.ones((1,3),bool), [True])
answers["독립4"] = dict(k=new_k,v=new_v,s=s,a=a,o=o)
wrong_scores = .09950371902099879 * past["layers"][1]["heads"][0]["k"]
answers["독립5"] = dict(wrong_scores=wrong_scores)
mm = example_model(); mm["embedding"][1] = [.1,2.]
hc,lc,cc,tc = full_prefix(mm,[0,1,2],[0,1,2])
answers["독립10"] = dict(h=hc,cache=cc,trace=tc)
for name, data in answers.items():
    print(name)
    if "h" in data: print("최종 표현:", " ".join(f"{x:.6f}" for x in data["h"][-1]))
(root := Path(__file__).resolve().parent).joinpath("CACHE_SOLUTIONS.json").write_text(
    json.dumps(serial(answers),ensure_ascii=False,indent=2)+"\n")
