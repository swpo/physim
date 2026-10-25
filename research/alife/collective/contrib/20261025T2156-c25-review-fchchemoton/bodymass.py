"""Amphiphile (u+1) and catalyst K inside fixed disks around the five seed-7 bodies (they do not move), every 10th
frame, for the fed run and the two local-cut runs; plus a plot. Body centres and radii from the frame at t=300."""
import numpy as np, json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
B = {"K-vesicle 8 (y44,x124)": (44, 124, 38), "K-free ring (34,34)": (34, 34, 24), "K-free ring (110,77)": (110, 77, 26),
     "K-trimer (160,56)": (160, 56, 27), "K-free Y (178,173)": (178, 173, 18)}
runs = {"fed": "rerun", "cut around K-trimer": "cutK_s7", "cut around K-free ring (110,77)": "cutfree_s7"}
yy, xx = np.mgrid[0:192, 0:192]
def disk(cy, cx, r):
    dy = (yy - cy + 96) % 192 - 96; dx = (xx - cx + 96) % 192 - 96; return dy * dy + dx * dx <= r * r
out = {}; fig, ax = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
for a, (rn, d) in zip(ax, runs.items()):
    R = np.load(d + "/frames.npz")["render"]; t = np.linspace(0, 600, len(R)); out[rn] = {}; i3, i45 = int(np.argmin(abs(t - 300))), int(np.argmin(abs(t - 450)))
    for bn, (cy, cx, r) in B.items():
        m = disk(cy, cx, r); us = R[:, 0][:, m].sum(1); ks = R[:, 2][:, m].sum(1)
        out[rn][bn] = {"u_t300": round(float(us[i3]), 1), "u_t450": round(float(us[i45]), 1), "u_t600": round(float(us[-1]), 1), "K_t300": round(float(ks[i3]), 1), "K_t600": round(float(ks[-1]), 1)}
        a.plot(t, us, label=bn)
    a.axvline(300, color="k", ls=":"); a.set_title(rn, fontsize=9); a.set_xlabel("t")
ax[0].set_ylabel("amphiphile u+1 in body disk"); ax[0].legend(fontsize=7); plt.tight_layout(); plt.savefig("bodymass.png", dpi=70)
print(json.dumps(out, indent=1)); json.dump(out, open("bodymass.json", "w"), indent=1)
