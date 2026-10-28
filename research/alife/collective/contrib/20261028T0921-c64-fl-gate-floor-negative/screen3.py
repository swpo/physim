import sys, os, json, copy, pickle, numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import world as w
N = 160; seed = int(sys.argv[1]); TA = float(sys.argv[2]); gms = json.loads(sys.argv[3])
s0 = pickle.load(open(f'/tmp/s{seed}_t1000.pkl', 'rb'))
def count(s):
    B = ndimage.gaussian_filter(s['B'].sum(0), 1, mode='wrap'); L, n = ndimage.label(B > 0.3)
    a = np.bincount(L.ravel())[1:]; return int((a >= 8).sum()), float(B.max())
for gm in gms:
    s = copy.deepcopy(s0); w.CFG['gate_k'] = list(range(10)); w.CFG['g_min'] = gm
    s['q'][:] = 0; w.CFG['k_qy'] = 0.0; out = []
    for i in range(int(TA / w.CFG['dt'])):
        s = w.step(s)
        if (i + 1) % int(50 / w.CFG['dt']) == 0: out.append(count(s))
    w.CFG['k_qy'] = 30.0
    print('all kernels, gain floor', gm, 'starved', ' '.join('%d/%.2f' % o for o in out), flush=True)
