
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from morpho_sim import simulate
from runner import calibrate_plateaus
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 1, figsize=(11, 6), sharex=False)
for ax, (name, Dv, L, np_, kap, eps) in zip(
        axes, [("L=48 Dv=10", 10.0, 48, (4,5), 0.5, 2.4e-3),
               ("L=64 Dv=11", 11.0, 64, (5,6), 0.5, 2.4e-3)]):
    cal = calibrate_plateaus(Dv, L, np_)
    kstar2 = (1-kap)*cal[0]["S"] + kap*cal[1]["S"]
    p = dict(ny=8, nx=L, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=Dv, Dc=10.0,
             sigma=1.0, mode="auto", eps=eps, kstar2=kstar2, steps=60000,
             meas_every=25, seed=1, k_ref=0.62, C0=1.0, t_on=250.0,
             noise_amp=2e-3, Cmin=0.5, Cmax=1.9)
    r = simulate(p)
    m = r["t"] >= 500
    ax.plot(r["t"][m], r["envmin"][m], lw=0.8, label="envmin")
    ax.plot(r["t"][m], r["amp"][m], lw=0.8, label="global amp")
    ax2 = ax.twinx()
    ax2.plot(r["t"][m], r["nz"][m], color="r", lw=1.2, alpha=0.7)
    ax2.set_ylabel("n", color="r")
    ax.set_title(name); ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig("strips/env_traces.png", dpi=110)
print("saved strips/env_traces.png")
