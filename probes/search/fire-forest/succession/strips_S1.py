
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
from sf_measure import measure4
from hier_metrics import save_strip
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"
base = dict(g=2e-3, Lam=9.0, theta=0.78, M=2.0, D=8.0, gsig=0.35, rho=0.03,
            gT=1e-4, mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03, cT=0.5,
            patch_frac=0.30, Tinit_patch=0.62)
snapT = (500, 10000, 25000, 45000, 59500)
out = run(L=64, T_ticks=60000, seed=0, init="mixed", snap_times=snapT, **base)
res = measure4(out, drop=10000)
sn = out["snaps"]; ts = sorted(sn)
save_strip([sn[t][2] for t in ts], SD + "/strips/S1_L4_treecover.png",
           titles=["T t=%d" % t for t in ts], cmap="YlGn", vmax=1.0)
save_strip([sn[t][0] for t in ts], SD + "/strips/S1_grass_fuel.png",
           titles=["B t=%d" % t for t in ts], cmap="Greens", vmax=1.0)
# burn count map: fires avoid forest?
bc = out["burn_count"].astype(float)
Tf = out["T_final"]
save_strip([Tf, bc], SD + "/strips/S1_biome_vs_burns.png",
           titles=["tree cover T (end)", "burn count (60k ticks)"],
           cmap="viridis")
print("burns in forest cells (T>0.5): %.2f /cell; in grass cells: %.2f /cell" % (
    bc[Tf > 0.5].mean() if (Tf > 0.5).any() else -1, bc[Tf < 0.3].mean()))
fig, axes = plt.subplots(4, 1, figsize=(11, 9), sharex=True)
t = np.arange(len(out["meanT"])) * out["rec"]
axes[0].plot(t, out["meanT"], color="darkgreen", lw=1.2)
rel = res["L4_relax"]
if rel["tau"]:
    tc = t / 1.0
    pred = rel["c"] + rel.get("a", 0) * np.exp(-(tc) / rel["tau"])
    axes[0].plot(t, pred, "--", color="gray", lw=1)
axes[0].set_ylabel("meanT"); axes[0].set_title(
    "L4 biome relaxation: tau4=%.0f r2=%.3f (mosaic settling)" % (rel["tau"] or -1, rel["r2"]))
axes[1].plot(t, out["fracForest"], color="olive", lw=1)
axes[1].set_ylabel("frac forest (T>0.5)")
axes[2].plot(t, out["phi_grass"], color="seagreen", lw=0.6)
axes[2].set_ylabel("phi_grass"); axes[2].set_title(
    "L3 grass fire-return clock: %s r2=%.3f tau3=%.0f" % (res["L3_model"], res["L3_r2"], res["tau3_used"] or -1))
axes[3].plot(t, out["area"], color="orangered", lw=0.5)
axes[3].set_ylabel("burning area"); axes[3].set_xlabel("tick")
axes[3].set_title("L2 fire events")
fig.tight_layout(); fig.savefig(SD + "/strips/S1_macro_layers.png", dpi=110)
print("FRI grass med=%.0f n=%d | FRI forest n=%d" % (
    res["fri_grass_med"] or -1, res["n_fri_grass"], res["n_fri_forest"]))
print("saved")
