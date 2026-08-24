import os, sys, numpy as np, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

fig = plt.figure(figsize=(15, 5))

# (a) V_w landscape spokes
ax = fig.add_subplot(1, 3, 1)
d = np.load(f"{BASE}/data/Vw_N10.npz")
rs, Vg, Vb = d["rs"], d["Vgap"], d["Vblob"]
for etaw, c in [(0.9, "tab:green"), (1.0, "tab:olive")]:
    ax.plot(rs, etaw * Vg, color=c, label=f"gap spoke, etaw={etaw}")
ax.plot(rs, 0.9 * Vb, color="tab:red", lw=1, label="blob spoke, etaw=0.9 (x truncated)")
ax.set_ylim(-0.005, 0.12)
ax.axvline(24.9, color="k", ls=":", lw=0.7)
ax.text(25.2, 0.10, "wall R", fontsize=8)
ax.set_xlabel("r from cell center (px)"); ax.set_ylabel("V_w (k1-units)")
ax.set_title("(a) cross-w barrier landscape\nridge at gap = 0.046*etaw")
ax.legend(fontsize=7)

# (b) barrier map: (tau, etaw) -> outcome
ax = fig.add_subplot(1, 3, 2)
res = json.load(open(f"{BASE}/results.json"))
seen = {}
for r in res:
    if r["name"].startswith(("BC_", "BW_", "PB_")) and r["kind"] == "barrier":
        tau = r["spec"]["cargo"]["tau"]; w = r["spec"].get("etaw12", 0)
        pre = r["spec"].get("prerelax_tu", 0) > 0
        key = (tau, w, pre)
        out = r["outcome"]
        alive = r["cargo_alive"]
        seen[key] = (out, alive)
for (tau, w, pre), (out, alive) in seen.items():
    if out == "NO_REACH":
        m, c = "o", "tab:green"
    elif alive:
        m, c = "^", "tab:orange"
    else:
        m, c = "x", "tab:red"
    ax.scatter([tau], [w], marker=m, c=c, s=90 if pre else 40,
               edgecolors=("k" if pre else "none"), linewidths=0.8, zorder=3)
ax.set_xlabel("cargo tau1 (speed dial)"); ax.set_ylabel("etaw12 (barrier strength)")
ax.set_title("(b) barrier map\ngreen o=CONFINED, orange ^=clean transmit,\nred x=transmit w/ cargo replication; big=prerelaxed")
ax.grid(alpha=0.3)

# (c) confined trajectory: PB_t5p8_w0p9
ax = fig.add_subplot(1, 3, 3)
pr = np.load(f"{BASE}/data/PB_t5p8_w0p9_probe.npz")
ax.plot(pr["t"], pr["rc"], lw=0.9, label="cargo radius r_c(t)")
ax.plot(pr["t"], pr["Rw"], color="k", lw=0.8, label="membrane R(t)")
ax.axhline(24.9 - 11, color="tab:red", ls=":", lw=0.7, label="wall zone edge")
ax.set_xlabel("t (tu)"); ax.set_ylabel("radius (px)")
ax.set_title("(c) CONFINED: tau=5.8, etaw=0.9\ncargo caged 2500tu, ring intact")
ax.legend(fontsize=8); ax.set_ylim(0, 30)

fig.suptitle("R2b: the membrane barrier — v-channel porous (all transmit), cross-w closes the pores", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(f"{BASE}/strips/fig3_R2b_barrier.png", dpi=110)
print("fig3 saved")
