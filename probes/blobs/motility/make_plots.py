
import sys, json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from metrics import curve_verdict, sqrt_law_fit, C_TRAVEL

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
S = OUT + "/strips"
os.makedirs(S, exist_ok=True)

# ---- 1) c(tau) curve ----
cur = json.load(open(OUT + "/cert1_curve.json"))
taus, cs, cls = [], [], []
for k, v in cur.items():
    if not k.startswith("tau"): continue
    taus.append(v["tau"]); cs.append(v.get("c_med") or 0.0); cls.append(v["cls"])
o = np.argsort(taus)
taus = np.array(taus)[o]; cs = np.array(cs)[o]; cls = [cls[i] for i in o]
trav = np.array([c == "traveling" for c in cls])
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.plot(taus[~trav], cs[~trav], "o", color="0.6", label="stationary")
ax.plot(taus[trav], cs[trav], "o-", color="C3", label="traveling")
ax.axhline(C_TRAVEL, ls=":", color="k", lw=0.8)
fit = sqrt_law_fit(taus[trav], cs[trav])
if fit["tau_c"]:
    tt = np.linspace(fit["tau_c"], taus.max(), 100)
    ax.plot(tt, np.sqrt(np.maximum(fit["a"]*(tt-fit["tau_c"]), 0)), "--", color="C0",
            label=f"c=sqrt(a(tau-tau_c)), tau_c={fit['tau_c']:.2f}, R2={fit['r2']:.3f}")
ax.set_xlabel("tau (slow-inhibitor time constant)"); ax.set_ylabel("c  [phys units / tu]")
ax.set_title("Drift bifurcation: blob speed vs tau  (Dv=0.65, dx=0.5, imexfft)")
ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(S + "/c_vs_tau.png", dpi=130)
cv = curve_verdict(taus[trav], cs[trav])
print("curve verdict:", cv); print("sqrt-law:", fit)
json.dump(dict(curve_verdict=cv, sqrt_law=fit,
               taus=[float(x) for x in taus], c=[float(x) for x in cs], cls=cls),
          open(OUT + "/curve_fit.json", "w"), indent=1)

# ---- 2) trajectory strip from cert1 tracks ----
tr = np.load(OUT + "/cert1_tracks.npz")
fig, ax = plt.subplots(figsize=(5.4, 5.4))
for tau in (4.8, 5.0, 5.2, 5.4):
    key = f"tau{tau}_com"
    if key in tr:
        c = tr[key]; ax.plot(c[:,1], c[:,0], lw=1.2, label=f"tau={tau}")
c0 = tr["tau4.4_com"]; ax.plot(c0[:,1], c0[:,0], "k.", ms=3, label="tau=4.4 (stat)")
ax.set_aspect("equal"); ax.legend(fontsize=8); ax.set_xlabel("y [phys]"); ax.set_ylabel("x [phys]")
ax.set_title("COM trajectories (unwrapped), kick 30deg, T=900tu")
fig.tight_layout(); fig.savefig(S + "/trajectories_tau.png", dpi=130)

# ---- 3) angle histogram / kick-follow ----
ang = json.load(open(OUT + "/cert3_angles.json"))
kicks = [float(k) for k in ang["kick_runs"]]
fins = [ang["kick_runs"][k].get("ang") for k in ang["kick_runs"]]
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.2))
axs[0].plot([0, 360], [0, 360], "k:", lw=0.8)
axs[0].plot(kicks, [f % 360 for f in fins], "o", color="C3")
axs[0].set_xlabel("kick angle [deg]"); axs[0].set_ylabel("measured travel angle [deg]")
axs[0].set_title("direction follows seeded kick (dx=0.5)")
nang = [v["ang"] for v in ang["noise_runs"].values() if v.get("cls") == "traveling"]
fold = [a % 90.0 for a in nang]
axs[1].hist(fold, bins=np.arange(0, 95, 5), color="C0", edgecolor="k")
for x in (0, 45, 90): axs[1].axvline(x, color="r", ls=":", lw=1)
axs[1].set_xlabel("travel angle mod 90 [deg]"); axs[1].set_ylabel("count")
axs[1].set_title(f"noise-seeded direction, n={len(fold)} (red = lattice axes)")
fig.tight_layout(); fig.savefig(S + "/angle_isotropy.png", dpi=130)
print("angle-follow:", ang.get("angle_follow_verdict"))
print("lattice-cluster:", ang.get("lattice_cluster_verdict"))
print("plots saved")
