
import sys, json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
S = OUT + "/strips"

# --- refresh angle isotropy figure with cert6 (symmetric-IC noise runs) ---
ang = json.load(open(OUT + "/cert3_angles.json"))
kicks = [float(k) for k in ang["kick_runs"]]
fins = [ang["kick_runs"][k].get("ang") for k in ang["kick_runs"]]
c6 = json.load(open(OUT + "/cert6_noise_dirs.json"))
nang = [v["ang"] for v in c6["runs"].values() if v.get("cls") == "traveling"]
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.2))
axs[0].plot([0, 360], [0, 360], "k:", lw=0.8)
axs[0].plot([k % 360 for k in kicks], [f % 360 for f in fins], "o", color="C3")
axs[0].set_xlabel("seeded kick angle [deg]"); axs[0].set_ylabel("measured travel angle [deg]")
axs[0].set_title("direction follows seeded kick (9 angles, max dev 0.015 deg)")
fold = [a % 90.0 for a in nang]
axs[1].hist(fold, bins=np.arange(0, 95, 5), color="C0", edgecolor="k")
for x in (0, 45, 90): axs[1].axvline(x, color="r", ls=":", lw=1)
axs[1].set_xlabel("travel angle mod 90 [deg]"); axs[1].set_ylabel("count")
axs[1].set_title(f"noise-chosen directions, n={len(fold)} seeds (red = lattice axes)")
fig.tight_layout(); fig.savefig(S + "/angle_isotropy.png", dpi=130)

# --- noise-seed trajectories (rose plot) ---
fig, ax = plt.subplots(figsize=(5.2, 5.2))
for s in range(8):
    f = OUT + f"/cert6_track_seed{s}.npz"
    if not os.path.exists(f): continue
    d = np.load(f)
    c = d["com"] - d["com"][0]
    ax.plot(c[:,1], c[:,0], lw=1.0, label=f"seed {s}")
ax.plot(0, 0, "k+", ms=10)
ax.set_aspect("equal"); ax.set_xlabel("dy [phys]"); ax.set_ylabel("dx [phys]")
ax.set_title("noise-chosen travel directions, symmetric IC (T=2000tu)")
ax.legend(fontsize=7, loc="upper left")
fig.tight_layout(); fig.savefig(S + "/noise_direction_rose.png", dpi=130)

# --- blob field snapshots: stationary vs traveling (u field with COM path) ---
sys.path.insert(0, OUT)
from sim import run
r1 = run(p=dict(k1=-0.7, Dv=0.65, tau=4.4), T=300.0, dx=0.5, stepper="imexfft",
         kick_angle=30.0, snap_times=(300.0,))
r2 = run(p=dict(k1=-0.7, Dv=0.65, tau=5.2), T=300.0, dx=0.5, stepper="imexfft",
         kick_angle=30.0, snap_times=(300.0,))
fig, axs = plt.subplots(1, 2, figsize=(10.2, 5.0))
for ax, r, ttl in ((axs[0], r1, "tau=4.4 stationary"), (axs[1], r2, "tau=5.2 traveling")):
    u = r["snaps"][300.0]
    ax.imshow(u.T, origin="lower", cmap="magma", extent=[0,96,0,96])
    c = np.mod(r["com"], 96.0)
    ax.plot(c[:,0], c[:,1], "c.", ms=1.5)
    ax.set_title(ttl + " (u at t=300, cyan: COM track)")
fig.tight_layout(); fig.savefig(S + "/field_stat_vs_travel.png", dpi=130)

# --- collision panel from cert4b snaps ---
sn = np.load(OUT + "/cert4b_collision_snaps.npz")
keys = ["snap0.0", "snap300.0", "snap450.0", "snap600.0", "snap1000.0"]
fig, axs = plt.subplots(1, len(keys), figsize=(3.0*len(keys), 3.2))
for ax, k in zip(axs, keys):
    ax.imshow(sn[k].T, origin="lower", cmap="magma", extent=[0,96,0,96])
    ax.set_title(f"t={k[4:]}", fontsize=9); ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("collision: traveler (from lower-left) hits stationary blob -> chase pair (both move, no merge)")
fig.tight_layout(); fig.savefig(S + "/collision_panel.png", dpi=130)

# --- long-run trajectory (cert5, 10k tu) ---
d = np.load(OUT + "/cert5_track.npz")
c = d["com"]
fig, ax = plt.subplots(figsize=(5.6, 5.0))
ax.plot(c[:,1], c[:,0], lw=0.8, color="C3")
ax.plot(c[0,1], c[0,0], "ko", ms=5); ax.plot(c[-1,1], c[-1,0], "k^", ms=7)
ax.set_aspect("equal"); ax.set_xlabel("y [phys]"); ax.set_ylabel("x [phys]")
ax.set_title("B1: 10,000 tu traveling blob, noise 2e-3 (unwrapped COM, o->^)")
fig.tight_layout(); fig.savefig(S + "/longrun_10ktu.png", dpi=130)
print("plots2 saved")
