
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
import numpy as np
from morpho_sim import simulate
from hier_metrics import save_strip
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

base = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0, Dc=10.0,
            sigma=1.0, mode="auto", steps=60000, meas_every=25, seed=1,
            k_ref=0.62, C0=0.9, t_on=250.0, kstar2=0.268, noise_amp=2e-3,
            Cmin=0.5, Cmax=1.8, kymo=True,
            snap_at=[16000, 20000, 25000, 30000, 35000, 40000])
r = simulate(dict(base, eps=2.4e-3))
np.savez("logs/flagship_seed1.npz", **{k: v for k, v in r.items() if k not in ("snaps",)})
ks = sorted(r["snaps"])
save_strip([r["snaps"][k][0] for k in ks], "strips/flip_u.png",
           titles=["u t=%d" % int(k*0.1) for k in ks])

fig, axes = plt.subplots(4, 1, figsize=(10, 9), sharex=True,
                         gridspec_kw=dict(height_ratios=[2.2, 1, 1, 1]))
ax = axes[0]
ax.imshow(r["kymo"].T, aspect="auto", cmap="magma",
          extent=[r["t"][0], r["t"][-1], 0, 64], origin="lower")
ax.set_ylabel("x (ring)")
ax.set_title("kymograph u(x,t): stripe insertion/annihilation events")
axes[1].plot(r["t"], r["nz"], lw=1); axes[1].set_ylabel("count n")
axes[2].plot(r["t"], r["Cm"], lw=1); axes[2].set_ylabel("C mean")
axes[3].plot(r["t"], r["envmin"], lw=0.8); axes[3].set_ylabel("min envelope")
axes[3].set_xlabel("t")
fig.tight_layout(); fig.savefig("strips/flip_kymo.png", dpi=110)
print("saved kymo. flips:", int((np.diff(r["nz"][r["t"]>=600])!=0).sum()))
