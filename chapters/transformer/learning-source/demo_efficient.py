"""본문의 비균일 Local, Causal Global, 특징 집계와 미래 변경을 실행한다."""
import json
from pathlib import Path
import numpy as np
from efficient import (causal_mask, sparse_attention, local_global_mask,
                       kernel_direct, kernel_factorized, kernel_prefix,
                       reachability, minimum_steps, interaction_cost)


def examples():
    p = np.arange(1, 5)
    q, k, v = np.ones((4, 1)), np.log(p)[:, None], p[:, None].astype(float)
    full, local = causal_mask(p, p), causal_mask(p, p, 2)
    f = sparse_attention(q, k, v, full)
    l = sparse_attention(q, k, v, local)
    phi = np.array([[1., 0.], [0., 1.], [1., 1.], [2., 1.]])
    pair = kernel_direct(phi, phi, v)
    state, z, factor = kernel_factorized(phi, phi, v)
    states, prefix = kernel_prefix(phi, phi, v)
    rawsoft = sparse_attention(np.ones((1, 1)), np.array([[2.], [1.], [3.], [5.]]), v, np.ones((1,4),bool))
    causalsoft = sparse_attention(phi, phi, v, full)
    changed = v.copy(); changed[-1] = 40.
    badglobal = kernel_factorized(phi, phi, changed)[2]
    safeprefix = kernel_prefix(phi, phi, changed)[1]
    past = v.copy(); past[0] = 10.
    pastprefix = kernel_prefix(phi, phi, past)[1]
    b = local_global_mask()
    g = sparse_attention(np.zeros((5,1)), np.zeros((5,1)), np.array([[2.],[4.],[8.],[16.],[32.]]), b)
    return {'full_mask': full, 'local_mask': local,
            'full_scores': np.where(full,f[0],0), 'full_weights': f[1], 'full_output': f[2],
            'local_weights': l[1], 'local_output': l[2],
            'reachable': [[sorted(x) for x in layer] for layer in reachability([local]*3)],
            'minimum_1_to_4': minimum_steps(local,1,4),
            'global_mask': b, 'global_output':g[2],
            'global_reachable': [[sorted(x) for x in layer] for layer in reachability([b]*2)],
            'kernel_weights':pair[0], 'kernel_normalized':pair[1], 'kernel_output':pair[2],
            'S':state,'z':z,'factor_output':factor,'prefix_states':states,'prefix_output':prefix,
            'same_scores_softmax':rawsoft[2], 'full_causal_softmax_phi_scaled':causalsoft[2],
            'future40_global':badglobal,'future40_prefix':safeprefix,'past10_prefix':pastprefix,
            'cost':interaction_cost(4,1,1,2,2)}


def serial(x):
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [serial(v) for v in x]
    return x


if __name__ == '__main__':
    data=serial(examples())
    Path(__file__).with_name('NUMERICAL_EFFICIENT.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    for key in ['full_output','local_output','minimum_1_to_4','S','z','prefix_output','same_scores_softmax','full_causal_softmax_phi_scaled','global_output','future40_prefix','future40_global','past10_prefix','cost']:
        print(key, data[key])
