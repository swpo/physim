
"""film_strip.py -- flagship proof-of-layer strips + hysteresis figure."""
import sys
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from morpho_sim import simulate
from runner import calibrate_plateaus
from hier_metrics import save_strip
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json

Dv, L, np_, kap, eps = 11.0, 64, (5, 6), 0.5, 2.8e-3
cal = calibrate_plateaus(Dv, L, np_)
kstar2 = (1 - kap) * cal[0]["S"] + kap * cal[1]["S"]
p = dict(ny=48, nx=L, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=Dv, Dc=10.0,
         sigma=1.0, mode="auto", eps=eps, kstar2=kstar2, steps=60000,
         meas_every=25, seed=2, k_ref=0.62, C0=1.0, t_on=250.0,
         noise_amp=2e-3, Cmin=0.5, Cmax=1.9, kymo=True,
         snap_at=[12000, 14200, 14500, 14800, 15200, 20000])
r = simulate(p)
ks = sorted(r["snaps"])
save_strip([r["snaps"][k][0] for k in ks], "strips/flagship_u_2d.png",
           titles=["u t=%d" % int(k * 0.1) for k in ks])
save_strip([r["snaps"][k][1] for k in ks], "strips/flagship_C_2d.png",
           titles=["C t=%d" % int(k * 0.1) for k in ks], cmap="viridis")

fig, axes = plt.subplots(4, 1, figsize=(11, 10), sharex=True,
                         gridspec_kw=dict(height_ratios=[2.4, 1, 1, 1]))
axes[0].imshow(r["kymo"].T, aspect="auto", cmap="magma",
               extent=[r["t"][0], r["t"][-1], 0, L], origin="lower")
axes[0].set_ylabel("x (ring)")
axes[0].set_title("MORPHO COUNTER flagship (Dv=11, L=64, kap=0.5, eps=2.8e-3, seed=2)")
axes[1].plot(r["t"], r["nz"], lw=1.2, color="k"); axes[1].set_ylabel("L3: count n")
axes[2].plot(r["t"], r["Cm"], lw=1, color="tab:blue"); axes[2].set_ylabel("C mean")
axes[3].plot(r["t"], r["envmin"], lw=0.8, color="tab:orange")
axes[3].set_ylabel("L2: min envelope"); axes[3].set_xlabel("t")
fig.tight_layout(); fig.savefig("strips/flagship_kymo.png", dpi=110)

# hysteresis staircase figure from results_hysteresis.json
h = json.load(open("results_hysteresis.json"))
fig, ax = plt.subplots(figsize=(7, 5))
col = {"up": "tab:red", "down": "tab:blue"}
for seed, jumps in h["F64"]["seeds"].items():
    for e in jumps:
        ax.scatter(e["C"], e["to"], color=col[e["dir"]], s=22,
                   marker="^" if e["dir"] == "up" else "v", alpha=0.7)
ax.set_xlabel("control field C"); ax.set_ylabel("stripe count n after jump")
ax.set_title("L3 staircase with hysteresis, L=64 Dv=11 (3 seeds x 2 loops)")
ax.grid(alpha=0.3)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], color=col["up"], marker="^", ls="", label="up-sweep jumps"),
                   Line2D([], [], color=col["down"], marker="v", ls="", label="down-sweep jumps")])
fig.tight_layout(); fig.savefig("strips/hysteresis_staircase.png", dpi=110)
print("film strips saved")
