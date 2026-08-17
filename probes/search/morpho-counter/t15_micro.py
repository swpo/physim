
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from morpho_sim import simulate
from runner import calibrate_plateaus
from hier_metrics import macro_period_quality
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

Dv, L, np_, kap, eps = 11.0, 64, (5,6), 0.5, 2.4e-3
cal = calibrate_plateaus(Dv, L, np_)
kstar2 = (1-kap)*cal[0]["S"] + kap*cal[1]["S"]
p = dict(ny=8, nx=L, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=Dv, Dc=10.0,
         sigma=1.0, mode="auto", eps=eps, kstar2=kstar2, steps=30000,
         meas_every=25, seed=1, k_ref=0.62, C0=1.0, t_on=250.0,
         noise_amp=2e-3, Cmin=0.5, Cmax=1.9,
         trace_win=(20000, 21000))  # ticks -> t in [2000, 2100]
r = simulate(p)
tr = r["trace"]
# L1 micro: kinetics relaxation. Perturbation response: use ACF of the noisy trace
x = tr - tr.mean()
acf = np.correlate(x, x, "full")[len(x)-1:]
acf /= acf[0]
i37 = np.argmax(acf < np.exp(-1))
print("L1 pixel-trace ACF 1/e time: %.1f t (%.0f ticks)" % (i37*0.1, i37))
fig, ax = plt.subplots(figsize=(8,3))
ax.plot(np.arange(len(tr))*0.1 + 2000, tr, lw=0.6)
ax.set_xlabel("t"); ax.set_ylabel("u(pixel)")
ax.set_title("L1 micro trace (single pixel), quiescent plateau")
fig.tight_layout(); fig.savefig("strips/L1_trace.png", dpi=110)
print("trace std=%.4f" % tr.std())
