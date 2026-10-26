"""Per-species counts and simple overlap-tracked lifetimes from labkit frames.npz.
usage: analyze.py out.png label1=pack1/frames.npz [label2=...]
Channel 0 = prey a, 1 = predator b; body = c > 0.5. dt per frame = 100.
Lifetime of a component: frames during which an overlap chain (largest-overlap successor) continues."""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
DT = 100.0
def lifetimes(masks):
    # returns list of lifetimes (frames) of chains started after frame 0 and ended before the last frame
    labs = [ndimage.label(m, structure=np.ones((3, 3)))[0] for m in masks]
    age = {}; done = []
    prev = None
    for t, L in enumerate(labs):
        n = L.max(); cur = {}
        for i in range(1, n + 1):
            if prev is None: cur[i] = (0, 0); continue
            ov = prev[L == i]; ov = ov[ov > 0]
            if ov.size: j = np.bincount(ov).argmax(); cur[i] = (age.get(j, (0, 0))[0] + 1, age.get(j, (0, t))[1])
            else: cur[i] = (0, t)
        if prev is not None:
            succ = set()
            for i in range(1, n + 1):
                ov = prev[L == i]; ov = ov[ov > 0]
                if ov.size: succ.add(np.bincount(ov).argmax())
            for j, (a, st) in age.items():
                if j not in succ and st > 0: done.append(a + 1)
        age = cur; prev = L
    return done
fig, ax = plt.subplots(1, 2, figsize=(11, 4)); out = {}
for arg in sys.argv[2:]:
    lab, path = arg.split('=')
    R = np.load(path)['render']
    na = [ndimage.label(f[0] > 0.5)[1] for f in R]; nb = [ndimage.label(f[1] > 0.5)[1] for f in R]
    t = np.arange(len(R)) * DT
    l, = ax[0].plot(t, na, label=lab + ' prey'); ax[0].plot(t, nb, '--', color=l.get_color(), label=lab + ' predator')
    lb = lifetimes([f[1] > 0.5 for f in R]); la = lifetimes([f[0] > 0.5 for f in R])
    mid = slice(20, None)
    out[lab] = dict(prey_mean_t2000=float(np.mean(na[mid])), pred_mean_t2000=float(np.mean(nb[mid])),
                    pred_last_alive_t=float(t[np.nonzero(nb)[0].max()]) if any(nb) else 0.0,
                    pred_life_median=float(np.median(lb) * DT) if lb else None, pred_life_n=len(lb),
                    pred_life_p90=float(np.percentile(lb, 90) * DT) if lb else None,
                    prey_life_median=float(np.median(la) * DT) if la else None, prey_life_n=len(la))
    if lb: ax[1].hist(np.array(lb) * DT, bins=30, histtype='step', label=lab + ' predator lifetimes')
ax[0].set_xlabel('t'); ax[0].set_ylabel('droplets (c > 0.5)'); ax[0].legend(fontsize=7)
ax[1].set_xlabel('lifetime of a predator droplet (t, overlap chain, ended chains only)'); ax[1].set_yscale('log'); ax[1].legend(fontsize=7)
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=80)
print(json.dumps(out, indent=1))
