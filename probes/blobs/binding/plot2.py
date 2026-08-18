import os, json, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bind = "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding"
loadj = lambda p: json.load(open(p))

# --- Fig 5: THE bond curve (tau=2.5): d0 -> trajectories dx=0.5 + final d* markers, plus dx=1 comparison
fig, ax = plt.subplots(1, 2, figsize=(11.5,4.4))
cols = plt.cm.viridis(np.linspace(0,1,8))
for c, d in zip(cols, (9.0, 11.0, 12.5, 14.0, 15.5, 17.0, 18.5, 20.0)):
    o = loadj(f"/tmp/bcs_d{d}.json")
    seq = np.array([[s[0], s[1] if s[1] is not None else np.nan] for s in o["seps"]])
    ax[0].plot(seq[:,0], seq[:,1], color=c, lw=1.4, label=f"d0={d:g}")
ax[0].axhline(15.7, color="r", ls=":", lw=1)
ax[0].text(30, 15.9, "d* = 15.7", color="r", fontsize=9)
ax[0].set_xlabel("t (tu)"); ax[0].set_ylabel("separation")
ax[0].set_title("BOND CURVE tau=2.5, dx=0.5 (continuum), L=48\ntwo-sided convergence to d*=15.7")
ax[0].legend(fontsize=6, ncol=2); ax[0].grid(alpha=0.3); ax[0].set_ylim(5, 36)

d0s, ends = [], []
for d in (13.0, 14.6, 15.5, 17.0, 18.5, 20.0, 22.0):
    o = loadj(f"/tmp/pin1_d{d}.json")
    d0s.append(d); ends.append(o["sep_end"])
ax[1].plot(d0s, ends, "o-", label="dx=1 (L=96, T=3000)")
bcs_pairs = []
for d in (9.0, 11.0, 12.5, 15.5, 17.0, 18.5, 20.0):
    o = loadj(f"/tmp/bcs_d{d}.json")
    bcs_pairs.append((d, o["sep_end"]))
bp = np.array(bcs_pairs)
ax[1].plot(bp[:,0], bp[:,1], "s--", label="dx=0.5 (L=48, T=2500)")
ax[1].plot([8,22],[8,22], "k:", lw=0.8, label="no motion")
ax[1].axhline(15.99, color="tab:blue", ls=":", lw=0.8)
ax[1].axhline(15.70, color="tab:orange", ls=":", lw=0.8)
ax[1].set_xlabel("initial separation d0"); ax[1].set_ylabel("final separation")
ax[1].set_title("Attractor map: d*(dx=1)=15.99 vs d*(dx=0.5)=15.70\nshift 1.8% => UNPINNED bond")
ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(bind,"strips","fig5_bond_curve_tau2p5.png"), dpi=130)
print("fig5")

# --- Fig 6: escape times, both points
fig2, ax2 = plt.subplots(1, 2, figsize=(10,4.1), sharey=True)
for a, (tag, pat, dstar) in zip(ax2, [("tau=3.0 pinned well (dx=1)","/tmp/esc_P7_n*.json",14.65),
                                      ("tau=2.5 continuum bond (dx=1)","/tmp/escs_n*.json",15.99)]):
    esc = [loadj(f) for f in glob.glob(pat)]
    for o in esc:
        if o.get("status") not in ("ok",): continue
        if o["censored"]:
            a.plot(o["noise"], o["T_max"], "^", color="gray", ms=7)
        else:
            col = "tab:red" if o["mode"]=="out" else "tab:purple"
            a.plot(o["noise"], o["t_escape"], "o", color=col, ms=6)
    lv = sorted(set(o["noise"] for o in esc))
    med = []
    for nz in lv:
        real = [o["t_escape"] for o in esc if o["noise"]==nz and not o["censored"]]
        cen = [o for o in esc if o["noise"]==nz and o["censored"]]
        if len(real) >= 2 and not cen:
            med.append((nz, np.median(real)))
    if med:
        m = np.array(med); a.plot(m[:,0], m[:,1], "r-", lw=1.6)
    a.set_yscale("log"); a.set_xlabel("noise sigma"); a.grid(alpha=0.3, which="both")
    a.set_title(tag, fontsize=10)
ax2[0].set_ylabel("escape time (tu)")
fig2.suptitle("Bond strength: escape time vs noise (^=censored, o=escaped, purple=field breakdown)", fontsize=10)
fig2.tight_layout()
fig2.savefig(os.path.join(bind,"strips","fig6_escape_vs_noise.png"), dpi=130)
print("fig6")

# --- Fig 7: molecule gallery at tau=2.5: chain3_s + tri3_s snapshots
rows = []
for nm, f in [("chain (3 blobs)","/tmp/snap_chain3s.npz"), ("triangle (3 blobs)","/tmp/snap_tri3s.npz")]:
    z = np.load(f)
    keys = sorted([k for k in z.files if k.startswith("t")], key=lambda k: float(k[1:]))
    rows.append((nm, z, keys))
fig3, axs = plt.subplots(len(rows), 3, figsize=(8.2, 2.9*len(rows)))
for i, (nm, z, keys) in enumerate(rows):
    u0 = float(z["u0"])
    for j, k in enumerate(keys[:3]):
        a = axs[i][j]
        a.imshow(z[k]-u0, cmap="inferno", vmin=-0.4, vmax=1.9)
        a.set_title(f"{nm}  t={k[1:]}", fontsize=8); a.axis("off")
fig3.suptitle("Blob molecules at d*=16 (tau=2.5, dx=1): stable chain and equilateral triangle", fontsize=10)
fig3.tight_layout()
fig3.savefig(os.path.join(bind,"strips","fig7_molecules_tau2p5.png"), dpi=130)
print("fig7")
