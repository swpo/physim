"""Per-cell particle composition over time: count, kind-1 fraction, distinct founder labels, purity."""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from scipy import ndimage
from labkit.world import load_world
W = load_world(sys.argv[1]); seed = int(sys.argv[2]); T = int(sys.argv[3]); out = sys.argv[4]
for kv in sys.argv[5:]:
    k, v = kv.split('='); W.P[k] = float(v)
s = W.init(seed, (128, 128)); rec = []
for t in range(T + 1):
    if t % 250 == 0:
        lab, n = ndimage.label(s['phi'] > 0.5, structure=np.ones((3, 3)))
        H, Wd = lab.shape
        c = lab[s['py'].astype(int) % H, s['px'].astype(int) % Wd]
        cells = []
        for i in range(1, n + 1):
            m = c == i
            if m.sum() < 20: continue
            k = s['kind'][m]; l = s['lab'][m]
            u, cnt = np.unique(l, return_counts=True)
            cells.append(dict(n=int(m.sum()), f1=float((k == 1).mean()), nlab=int(len(u)), top=float(cnt.max() / m.sum())))
        out_frac = float((c == 0).mean())
        rec.append(dict(t=t, ncell=len(cells), N=int(len(s['py'])), outside=out_frac,
                        births=s['births'].tolist(), deaths=s['deaths'].tolist(), flips=s['flips'], cells=cells))
        if t % 1000 == 0:
            nl = [x['nlab'] for x in cells]; tp = [x['top'] for x in cells]; f = [x['f1'] for x in cells]
            print(t, len(cells), len(s['py']), round(out_frac, 4), 'nlab med', np.median(nl) if nl else 0, 'top med', round(np.median(tp), 2) if tp else 0,
                  'f1', np.round(sorted(f), 2).tolist() if f else [], flush=True)
    s = W.step(s)
json.dump(rec, open(out, 'w'))
