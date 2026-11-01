"""세 구조와 통합 Decoder의 전 중간값을 출력한다."""
import json
from pathlib import Path
import numpy as np
from architectures import integrated, exact_cross, parameters, full_allowed
from block import post_ln
from masking import causal_allowed
from sources import cross_attention


def serial(x):
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, dict): return {k: serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [serial(v) for v in x]
    return x


def main():
    np.set_printoptions(precision=6, suppress=True)
    trace = integrated()
    for name in ('content', 'position', 'z', 'e', 'd', 'self_mask', 'cross_mask'):
        print(name, trace[name], sep='\n')
    for group in ('encoder', 'decoder'):
        print(group)
        def show(data, prefix=''):
            for k, v in data.items():
                if isinstance(v, dict): show(v, prefix+k+'.')
                elif isinstance(v, list):
                    for i, item in enumerate(v): show(item, prefix+k+str(i)+'.')
                else: print(prefix+k, v, sep='\n')
        show(trace[group])
    print('마지막 요청의 다음 Token 점수\n', trace['logits'])
    h, e, q, k, v, mask = exact_cross()
    exact = cross_attention(h, e, q, k, v, mask)
    print('축약 Cross의 Q/K/V/S/A/O')
    for name, a in zip(('q', 'k', 'v', 's', 'a', 'o'), exact): print(name, a, sep='\n')
    p, wo, ffn, ln = parameters()
    x = np.array([[1., 0., 2.], [0., 2., 1.], [2., 1., 0.]])
    cm = causal_allowed(np.arange(3), np.arange(3), np.ones(3, dtype=bool))
    dy, dt = post_ln(x, [p], wo, ffn, ln, ln, [cm])
    print('Decoder-only Attention/최종 반환', dt['heads'][0]['a'], dt['heads'][0]['o'], dy, sep='\n')
    Path(__file__).with_name('NUMERICAL_ARCHITECTURES.json').write_text(json.dumps(serial(dict(integrated=trace, exact_cross=exact, decoder_only=dt)), ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': main()
