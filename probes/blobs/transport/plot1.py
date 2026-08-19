import json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

tdir = "/Users/spoho/Documents/prime/test/physim/probes/blobs/transport"
res = json.load(open(f"{tdir}/results.json"))
def get(rid):
    for r in res:
        if r["id"] == rid: return r

# ---------------- fig1: drift curves
fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
ax = axes[0]
Beps = [0.00125, 0.0025, 0.00375, 0.005, 0.0075, 0.00875, 0.009, 0.0095]
Bv = []
for e in Beps:
    r = get(f"Bcurve_eps{e}") or get(f"Bflip_eps{e}_s0")
    Bv.append(r["drift"]["v_x"])
Bflip_e = [0.01, 0.0125]; Bflip_v = [get("Bcurve_eps0.01")["drift"]["v_x"], get("Bflip_eps0.0125_s0")["drift"]["v_x"]]
seeds = [get(f"Bcurve_eps0.0025_s{s}")["drift"]["v_x"] for s in (1,2,3)]
dx025 = get("Bcurve_eps0.0025_dx025")["drift"]["v_x"]
ax.plot(Beps, Bv, "o-", color="tab:blue", label="B (dx=0.5)")
ax.plot(Bflip_e, Bflip_v, "s--", color="tab:red", label="B flipped branch")
ax.plot([0.0025]*3, seeds, "x", color="k", ms=8, label="3 seeds (noise 2.5e-3)")
ax.plot([0.0025], [dx025], "d", color="tab:green", ms=9, label="dx=0.25 check")
ax.axhline(0, color="gray", lw=0.5); ax.axvspan(0.0095, 0.0135, alpha=0.12, color="red")
ax.set_xlabel("eps (k1-units/px)"); ax.set_ylabel("v_x (px/tu)")
ax.set_title("B drift vs gradient: v=2.75*eps, FLIP at eps*~0.0095-0.010")
ax.legend(fontsize=8)

ax = axes[1]
Apeps = [0.00125, 0.0025, 0.00375, 0.005, 0.0075, 0.01]
Apv = [get(f"Ap065_drift_eps{e}")["drift"]["v_x"] for e in Apeps]
apseeds = [get(f"Ap065_eps0.0025_s{s}")["drift"]["v_x"] for s in (1,2,3)]
apdx = get("Ap065_eps0.0025_dx025")["drift"]["v_x"]
ax.plot(Apeps, Apv, "o-", color="tab:orange", label="A' (d=0.65)")
ax.plot(Beps, Bv, "o-", color="tab:blue", alpha=0.4, label="B")
ax.plot([0.0025]*3, apseeds, "x", color="k", label="3 seeds")
ax.plot([0.0025], [apdx], "d", color="tab:green", ms=9, label="dx=0.25")
ax.set_xlabel("eps"); ax.set_ylabel("v_x (px/tu)")
ax.set_title("Species selectivity: same sign, A' 1.2-1.4x faster (low eps)")
ax.legend(fontsize=8)

ax = axes[2]
for jid, lab, c in (("Bcurve_eps0.005", "B eps=0.005 (drifts up)", "tab:blue"),
                    ("Bcurve_eps0.01", "B eps=0.01 (FLIPS down)", "tab:red"),
                    ("Ap065_drift_eps0.0025", "A' eps=0.0025", "tab:orange")):
    d = np.load(f"{tdir}/data/{jid}.npz")
    ax.plot(d["t"], d["trk0_x"], color=c, label=lab)
ax.axhline(48, color="gray", ls=":", lw=1, label="ridge x=48")
ax.axhline(24, color="gray", lw=0.5)
ax.set_xlabel("t (tu)"); ax.set_ylabel("x (px)"); ax.set_title("sample tracks")
ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig(f"{tdir}/strips/fig1_drift_curves.png", dpi=110); plt.close()

# ---------------- fig2: blocking
fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
ax = axes[0]
for jid, lab, c in (("block_Bwall_s0", "cargo + wall (s0)", "tab:blue"),
                    ("block_Bwall_s1", "cargo + wall (s1,noise)", "tab:cyan"),
                    ("block_Bwall_s2", "cargo + wall (s2,noise)", "tab:green"),
                    ("block_ctrl_s0", "cargo NO wall (control)", "tab:red")):
    d = np.load(f"{tdir}/data/{jid}.npz")
    ax.plot(d["t"], d["trk0_x"], color=c, label=lab)
ax.axhline(45.5, color="k", ls="--", lw=1, label="wall x=45.5")
ax.set_xlabel("t"); ax.set_ylabel("cargo x"); ax.set_title("BLOCKING: standoff at d~11.9px, control passes")
ax.legend(fontsize=8)

ax = axes[1]
d = np.load(f"{tdir}/data/block_Bwall_s0.npz")
F = d["Ffinal"]
im = ax.imshow(F[1].T, origin="lower", cmap="magma", extent=[0,96,0,96])
ax.set_title("final u2: cargo parked at wall standoff")
plt.colorbar(im, ax=ax, fraction=0.045)

ax = axes[2]
d = np.load(f"{tdir}/data/wall_hold_eps0.00125.npz")
ax.plot(d["t"], d["trk0_area"], label="wall area (eps=0.00125)")
ax.set_xlabel("t"); ax.set_ylabel("stripe area px^2")
ax.set_title("wall holds at lower eps (structure static)")
ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig(f"{tdir}/strips/fig2_blocking.png", dpi=110); plt.close()

# ---------------- fig3: channeling
fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
ax = axes[0]
for y0 in (9.0, 10.0, 11.0, 12.0, 14.0, 16.0):
    d = np.load(f"{tdir}/data/chan_y{y0}.npz")
    ax.plot(d["trk0_x"], d["trk0_y"], label=f"y0={y0}")
ax.axhline(8, color="k", lw=2, alpha=0.4); ax.axhline(24, color="k", lw=2, alpha=0.4)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_title("cargo paths between rails (y=8,24)")
ax.legend(fontsize=7)
ax = axes[1]
d = np.load(f"{tdir}/data/chan_y12.0.npz")
F = d["Ffinal"]
im = ax.imshow(F[0].T + F[1].T, origin="lower", cmap="magma", extent=[0,80,0,80])
ax.set_title("final u1+u2: rails + channeled cargo")
plt.colorbar(im, ax=ax, fraction=0.045)
ax = axes[2]
d = np.load(f"{tdir}/data/chan_ctrl_y12.npz")
dr = np.load(f"{tdir}/data/chan_y12.0.npz")
ax.plot(dr["t"], dr["trk0_y"], label="rails: y -> 16 (centerline)")
ax.plot(d["t"], d["trk0_y"], label="no rails: y stays 12 then stripe")
ax.axhline(16, color="gray", ls=":")
ax.set_xlabel("t"); ax.set_ylabel("cargo y"); ax.set_title("channel centering (rails vs control)")
ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig(f"{tdir}/strips/fig3_channel.png", dpi=110); plt.close()

# ---------------- fig4: conveyor + ratchet
fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
ax = axes[0]
for jid, lab, c in (("conv_probe", "saw f=0.7 eps=0.005 (+x)", "tab:blue"),
                    ("conv_mirror", "saw f=0.3 (mirror, -x)", "tab:red"),
                    ("conveyor_f0.8", "saw f=0.8 eps=0.0027", "tab:green"),
                    ("conveyor_f0.2", "saw f=0.2 (mirror)", "tab:olive")):
    try:
        d = np.load(f"{tdir}/data/{jid}.npz")
        ax.plot(d["t"], d["trk0_x"], color=c, label=lab)
    except FileNotFoundError: pass
ax.set_xlabel("t"); ax.set_ylabel("x"); ax.set_title("sawtooth transport: direction follows asymmetry")
ax.legend(fontsize=8)
ax = axes[1]
b = np.load(f"{tdir}/data/conv_probe.npz")["b"]
xs = np.arange(len(b))*0.5
ax.plot(xs, b, label="saw f=0.7 eps=0.005")
b8 = np.load(f"{tdir}/data/conveyor_f0.8.npz")["b"]
ax.plot(np.arange(len(b8))*0.5, b8, label="saw f=0.8 eps=0.0027")
ax.set_xlabel("x"); ax.set_ylabel("b(x)"); ax.set_title("sawtooth profiles (static field)")
ax.legend(fontsize=8)
ax = axes[2]
for jid, lab in (("ratchet_pilot_sig0.02", "sigma=0.02"), ("ratchet_pilot_sig0.03", "sigma=0.03")):
    d = np.load(f"{tdir}/data/{jid}.npz")
    ax.plot(d["t"], d["trk0_x"] - d["trk0_x"][0], label=lab)
ax.set_xlabel("t"); ax.set_ylabel("x - x0"); ax.set_ylim(-2, 2)
ax.set_title("NOISE ratchet: NO transport in 3000 tu (honest negative)")
ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig(f"{tdir}/strips/fig4_ratchet.png", dpi=110); plt.close()
print("figs 1-4 saved")
