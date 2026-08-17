
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import run, measure, events_from_series
from hier_metrics import save_strip
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
base = dict(theta=0.78, Lam=9.0, M=2.0, D=8.0, gsig=0.35, rho=0.03, g=2e-3)
out = run(L=64, T=30000, seed=0, rec=5, **base)
ev = events_from_series(out["area"], out["ign"], out["rec"])
big = max((e for e in ev if e["t0"] > 10000), key=lambda e: e["size"])
t0 = big["t0"]; print("big event t0=%d size=%d dur=%d" % (t0, big["size"], big["dur"]))
snap_L1 = [t0 + d for d in (3, 12, 25, 45, 70)]
snap_L3 = [t0 - 900, t0 - 10, t0 + 120, t0 + 900, t0 + 1800]
out2 = run(L=64, T=30000, seed=0, rec=5, snap_times=tuple(snap_L1 + snap_L3), **base)
sn = out2["snaps"]
save_strip([sn[t][1] for t in snap_L1], WD + "/strips/W7_L1_fire_front.png",
           titles=["F t0+%d" % (t - t0) for t in snap_L1], cmap="magma", vmax=1.0)
save_strip([sn[t][0] for t in snap_L3], WD + "/strips/W7_L3_fuel_cycle.png",
           titles=["B t0%+d" % (t - t0) for t in snap_L3], cmap="Greens", vmax=1.0)
fig, axes = plt.subplots(3, 1, figsize=(11, 7))
t = np.arange(len(out2["meanB"])) * out2["rec"]
axes[0].plot(t, out2["phi"], lw=0.7, color="darkgreen")
axes[0].set_ylabel("phi=frac(B>theta)"); axes[0].set_title("W7 L3 top: mature-fuel cover")
axes[1].plot(t, out2["area"], lw=0.5, color="orangered")
axes[1].set_ylabel("burning area"); axes[1].set_title("W7 L2: fire events")
import json
sizes = np.array(json.load(open(WD + "/w1_pooled_sizes.json"))["sizes"], float)
xs = np.sort(sizes)[::-1]
axes[2].loglog(xs, np.arange(1, len(xs) + 1), "o", ms=3, alpha=0.6)
axes[2].set_xlabel("event size s"); axes[2].set_ylabel("rank")
axes[2].set_title("L2 sizes, 6 seeds pooled (W1); broad 3 decades, spanning bump at 4096")
fig.tight_layout(); fig.savefig(WD + "/strips/W7_macro_layers.png", dpi=110)
print("saved")
