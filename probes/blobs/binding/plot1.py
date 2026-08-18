import os, json, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bind = "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding"
def loadj(p):
    return json.load(open(p))

fig, ax = plt.subplots(1, 2, figsize=(11,4.2))
for d in [9.0,10.5,12.0,13.5,15.0,16.5,18.0,20.0,22.0]:
    o = loadj(f"/tmp/bond_P7_d{d}.json")
    seq = np.array([[s[0],s[1]] for s in o["seps"] if s[1] is not None])
    ax[0].plot(seq[:,0], seq[:,1], lw=1.2, label=f"d0={d:g}")
ax[0].set_xlabel("t (tu)"); ax[0].set_ylabel("separation (px)")
ax[0].set_title("P7 (tau=3) pair relaxation, dx=1\n(pinned ladder: 14.65, 16.0, frozen >=18)")
ax[0].legend(fontsize=6, ncol=2); ax[0].grid(alpha=0.3)
for d in (12.0,14.0,15.0,16.0,18.0,20.0,22.0):
    o = loadj(f"/tmp/ref_P7_d{d}.json")
    seq = np.array([[s[0],s[1]] for s in o["seps"] if s[1] is not None])
    ax[1].plot(seq[:,0], seq[:,1], lw=1.2, label=f"d0={d:g}")
o = loadj("/tmp/stab_tau2.5.json")
seq = np.array([[s[0],s[1]] for s in o["seps"] if s[1] is not None])
ax[1].plot(seq[:,0], seq[:,1], "k--", lw=2.2, label="tau=2.5 d0=14.6 (STABLE)")
ax[1].set_xlabel("t (tu)"); ax[1].set_ylabel("separation (px)")
ax[1].set_title("dx=0.5 continuum: tau=3 saddle escapes;\ntau=2.5 binds ~15.7")
ax[1].legend(fontsize=6); ax[1].grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(bind,"strips","fig1_pinning_vs_continuum.png"), dpi=130)
print("fig1 saved")

# escape-time plot (tau=3, dx=1)
esc = []
for f in glob.glob("/tmp/esc_P7_*.json"):
    o = loadj(f); esc.append((o["noise"], o["t_escape"], o["censored"], o["T_max"]))
fig2, ax2 = plt.subplots(figsize=(5.2,4))
lv = sorted(set(e[0] for e in esc))
for nz in lv:
    ts = [e for e in esc if e[0]==nz]
    for (n_, t_, c_, tm_) in ts:
        if c_:
            ax2.plot(n_, tm_, marker="^", color="tab:gray", ms=7)
        else:
            ax2.plot(n_, t_, marker="o", color="tab:red", ms=6)
means = []
for nz in lv:
    real = [e[1] for e in esc if e[0]==nz and not e[2]]
    cen  = [e[3] for e in esc if e[0]==nz and e[2]]
    if real and not cen:
        means.append((nz, np.mean(real)))
if means:
    m = np.array(means); ax2.plot(m[:,0], m[:,1], "r-", lw=1.5)
ax2.set_yscale("log"); ax2.set_xlabel("noise sigma"); ax2.set_ylabel("escape time (tu)")
ax2.set_title("Escape from d*=14.65 well (tau=3, dx=1)\n^ = censored (no escape by T_max)")
ax2.grid(alpha=0.3, which="both")
fig2.tight_layout()
fig2.savefig(os.path.join(bind,"strips","fig2_escape_times_tau3_dx1.png"), dpi=130)
print("fig2 saved")

# field snapshots strip: pair film (d0=12, tau=3, dx=1) + multi finals
z = np.load("/tmp/snap_pair12.npz")
u0 = float(z["u0"])
keys = [k for k in z.files if k.startswith("t")]
keys.sort(key=lambda k: float(k[1:]))
fig3, axs = plt.subplots(1, len(keys), figsize=(2.6*len(keys), 2.9))
for a, k in zip(axs, keys):
    im = a.imshow(z[k]-u0, cmap="inferno", vmin=-0.4, vmax=1.9)
    a.set_title(f"t={k[1:]} tu", fontsize=9); a.axis("off")
fig3.suptitle("Bound-pair formation film: d0=12 -> d*=14.65 (P7 tau=3, dx=1, u-u0)", fontsize=10)
fig3.tight_layout()
fig3.savefig(os.path.join(bind,"strips","fig3_pair_film_frames.png"), dpi=130)
print("fig3 saved")

for nm, f in [("chain3","/tmp/snap_chain3.npz"),("tri3","/tmp/snap_tri3.npz"),("square4","/tmp/snap_square4.npz")]:
    try:
        z = np.load(f)
    except FileNotFoundError:
        continue
    u0 = float(z["u0"]); keys = sorted([k for k in z.files if k.startswith("t")], key=lambda k: float(k[1:]))
    fig4, axs = plt.subplots(1, len(keys), figsize=(2.6*len(keys), 2.9))
    if len(keys)==1: axs=[axs]
    for a, k in zip(axs, keys):
        a.imshow(z[k]-u0, cmap="inferno", vmin=-0.4, vmax=1.9)
        a.set_title(f"t={k[1:]}", fontsize=9); a.axis("off")
    fig4.suptitle(f"multi-blob: {nm} (P7 tau=3, dx=1)", fontsize=10)
    fig4.tight_layout()
    fig4.savefig(os.path.join(bind,"strips",f"fig4_multi_{nm}.png"), dpi=130)
    print(f"fig4 {nm} saved")
