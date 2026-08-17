
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from morpho_sim import simulate
from runner import calibrate_plateaus
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

Dv, L, np_, kap, eps = 11.0, 64, (5,6), 0.5, 2.4e-3
cal = calibrate_plateaus(Dv, L, np_)
kstar2 = (1-kap)*cal[0]["S"] + kap*cal[1]["S"]
p = dict(ny=8, nx=L, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=Dv, Dc=10.0,
         sigma=1.0, mode="auto", eps=eps, kstar2=kstar2, steps=60000,
         meas_every=25, seed=1, k_ref=0.62, C0=1.0, t_on=250.0,
         noise_amp=2e-3, Cmin=0.5, Cmax=1.9)
r = simulate(p)
m = r["t"] >= 1000
t = r["t"][m]; modes = r["modes"][m]; n = r["nz"][m]
win = list(range(4, 9))  # rung window for L=64 pair (5,6): 4..8
A = modes[:, win]
srt = np.sort(A, axis=1)
ratio = srt[:, -2] / np.maximum(srt[:, -1], 1e-12)
fig, axes = plt.subplots(2, 1, figsize=(11, 5), sharex=True)
for k in win:
    axes[0].plot(t, modes[:, k], lw=0.8, label="A%d" % k)
axes[0].legend(fontsize=7, ncol=5); axes[0].set_ylabel("mode amp")
axes[1].plot(t, ratio, lw=0.8); axes[1].axhline(0.5, color="r", ls="--", lw=0.7)
ax2 = axes[1].twinx(); ax2.plot(t, n, color="g", lw=1, alpha=0.6)
axes[1].set_ylabel("2nd/1st ratio"); ax2.set_ylabel("n", color="g")
fig.tight_layout(); fig.savefig("strips/mode_competition.png", dpi=110)
# quantify: fraction of time ratio > thr, and event durations at thr
for thr in [0.4, 0.5, 0.6]:
    above = ratio > thr
    d = np.diff(above.astype(int))
    starts = list(np.where(d == 1)[0] + 1); ends = list(np.where(d == -1)[0] + 1)
    if above[0]: starts = [0] + starts
    if above[-1]: ends = ends + [len(above)]
    flips = set(np.where(np.diff(n) != 0)[0].tolist())
    durs = [(e - s) * (t[1] - t[0]) for s, e in zip(starts, ends)
            if any(s - 2 <= f <= e + 2 for f in flips)]
    print("thr=%.1f: frac_above=%.3f n_ev=%d median_dur=%.1f durs=%s"
          % (thr, above.mean(), len(durs), np.median(durs) if durs else -1,
             [round(x, 1) for x in durs]))
