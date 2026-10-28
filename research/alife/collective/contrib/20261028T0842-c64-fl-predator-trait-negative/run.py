"""usage: WORLD_P=... run.py SEED T OUT.json -- records every 10 t: predator count, mass-weighted mean and SD of log trait, prey count."""
import sys, os, json, numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import world as w
seed, T, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]; N = 160
s = w.init(seed, (N, N)); dt = w.CFG['dt']; rec = []
for i in range(int(T / dt) + 1):
    if i % int(10 / dt) == 0:
        B = s['B'].sum(0); A = s['A'].sum(0); lt = np.log(w.trait(s)); m = B > 0.3
        nB = ndimage.label(ndimage.gaussian_filter(B, 1, mode='wrap') > 0.3)[1]; nA = ndimage.label(ndimage.gaussian_filter(A, 1, mode='wrap') > 0.3)[1]
        mu = float((lt * B).sum() / max(B.sum(), 1e-9)); sd = float(np.sqrt((((lt - mu) ** 2) * B).sum() / max(B.sum(), 1e-9)))
        rec.append(dict(t=round(i * dt, 1), nB=int(nB), nA=int(nA), mu=mu, sd=sd, body_mu=float(lt[m].mean()) if m.any() else 0.0))
    s = w.step(s)
json.dump(rec, open(out, 'w')); print(json.dumps(rec[-1]))
