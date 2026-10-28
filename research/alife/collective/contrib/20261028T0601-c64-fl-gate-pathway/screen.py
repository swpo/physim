import sys, os, json, copy, pickle, numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import world as w
N = 160; seed = int(sys.argv[1]); T0 = 1000.0; TA = float(sys.argv[2]); sets = json.loads(sys.argv[3])
pk = f'/tmp/s{seed}_t1000.pkl'
if os.path.exists(pk): s0 = pickle.load(open(pk, 'rb'))
else:
    s0 = w.init(seed, (N, N))
    for i in range(int(T0 / w.CFG['dt'])): s0 = w.step(s0)
    pickle.dump(s0, open(pk, 'wb'))
def count(s):
    B = ndimage.gaussian_filter(s['B'].sum(0), 1, mode='wrap'); L, n = ndimage.label(B > 0.3)
    a = np.bincount(L.ravel())[1:]; return int((a >= 8).sum()), float(B.max())
print('t0', count(s0), flush=True)
for S in sets:
    s = copy.deepcopy(s0); w.CFG['gate_k'] = S if S != 'all' else 'all'
    s['q'][:] = 0; w.CFG['k_qy'] = 0.0
    out = []
    for i in range(int(TA / w.CFG['dt'])):
        s = w.step(s)
        if (i + 1) % int(50 / w.CFG['dt']) == 0: out.append(count(s))
    w.CFG['k_qy'] = 30.0
    print('gate', S, 'starved n/peak every 50t:', ' '.join('%d/%.2f' % o for o in out), flush=True)
