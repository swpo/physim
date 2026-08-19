import json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
tdir = "/Users/spoho/Documents/prime/test/physim/probes/blobs/transport"
res = json.load(open(f"{tdir}/results.json"))
def get(rid):
    for r in res:
        if r["id"] == rid: return r

fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
ax = axes[0]
ies = [0.00125,0.0025,0.005,0.0075,0.01,0.02,0.03]
ivs = [get(f"isod_B_eps{e}")["drift"]["v_x"] for e in ies]
seeds = [get(f"isod_B_eps0.005_s{s}")["drift"]["v_x"] for s in (1,2,3)]
ax.plot(ies, ivs, "o-", color="tab:purple", label="B, mode=isod")
ax.plot([0.005]*3, seeds, "x", color="k", label="3 seeds (noise)")
r = get("isod_B_eps0.005_dx025")
if r and "v_x" in r.get("drift", {}):
    ax.plot([0.005], [r["drift"]["v_x"]], "d", color="tab:green", ms=9, label="dx=0.25")
ap = get("isod_Ap_eps0.005")
ax.plot([0.005], [ap["drift"]["v_x"]], "s", color="tab:orange", label="A' @0.005")
xx = np.linspace(0, 0.031, 10)
ax.plot(xx, -0.906*xx, ":", color="gray", label="v=-0.906 eps")
ax.set_xlabel("eps (d-units/px)"); ax.set_ylabel("v_x (px/tu)")
ax.set_title("isod-mode drift: SAFE to eps=0.02 (area stays ~30)")
ax.legend(fontsize=8)

ax = axes[1]
eps = [0.00125, 0.00175, 0.0025, 0.003, 0.00375]
sod = [15.74, 14.74, 14.18, 13.39, 12.90]
ax.plot(eps, sod, "o-", color="tab:blue")
ax.plot([0.0025]*3, [14.18, 14.34, 14.36], "x", color="k", label="3 seeds")
ax.plot([0.0025], [14.19], "d", color="tab:green", ms=9, label="x0=16 launch")
ax.set_xlabel("eps (k1-mode)"); ax.set_ylabel("standoff gap (px)")
ax.set_title("BLOCKING: wall standoff vs push strength")
ax.legend(fontsize=8)

ax = axes[2]
y0s = [10, 11, 12, 14, 16]
yrms = [1.493, 1.207, 1.021, 0.724, 0.000]
ax.plot(y0s, yrms, "o-", color="tab:blue", label="rails")
ax.plot([9], [7.822], "s", color="tab:red", label="y0=9: rail-captured")
ax.plot([12], [4.0], "^", color="tab:gray", label="control no rails")
ax.plot([12.03, 11.97], [1.021, 1.019], "x", color="k", label="2 noise seeds")
ax.set_xlabel("cargo start y0 (rails at 8/24, center 16)")
ax.set_ylabel("y_rms about centerline (px)")
ax.set_title("CHANNELING: capture curve")
ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig(f"{tdir}/strips/fig5_certified_curves.png", dpi=110); plt.close()
print("fig5 saved")
