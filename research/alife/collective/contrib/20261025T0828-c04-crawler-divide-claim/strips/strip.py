"""Strip of one lineage: follow the body that splits at frame F1 back to frame F0 by maximal overlap,
and forward through its daughters. Usage: strip.py pack_seed_dir F0 F1 F2 out.png"""
import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, ".")
from crawler import plabel
d, F0, F1, F2, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
M = np.load(d + "/frames.npz")["matter"]; thr = 0.25
labs = [plabel(m > thr) for m in M]
def comps_overlapping(f, mask):
    lab, n = labs[f]; ids = np.unique(lab[mask & (lab > 0)]); return lab, ids
# find a body at F1-1 that overlaps >=2 bodies at F1
lab0, n0 = labs[F1 - 1]; lab1, _ = labs[F1]
cand = [k for k in range(1, n0 + 1) if len(np.unique(lab1[(lab0 == k) & (lab1 > 0)])) >= 2]
print("split parents at", F1, cand)
k = cand[int(sys.argv[6]) if len(sys.argv) > 6 else 0]
masks = {F1 - 1: lab0 == k}
for f in range(F1 - 2, F0 - 1, -1):
    lab, n = labs[f]; prev = masks[f + 1]
    ov = np.bincount(lab[prev], minlength=n + 1); ov[0] = 0
    masks[f] = lab == ov.argmax()
for f in range(F1, F2 + 1):
    lab, n = labs[f]; prev = masks[f - 1]
    ids = np.unique(lab[prev & (lab > 0)])
    if len(ids) == 0:  # fast movers: dilate
        ids = np.unique(lab[np.roll(prev, 2, 0) | np.roll(prev, -2, 0) | np.roll(prev, 2, 1) | np.roll(prev, -2, 1)]); ids = ids[ids > 0]
    masks[f] = np.isin(lab, ids)
frames = np.linspace(F0, F2, 10).astype(int)
fig, ax = plt.subplots(1, 10, figsize=(20, 2.4))
H = M.shape[1]
for a, f in zip(ax, frames):
    y, x = np.nonzero(masks[f]); 
    cy = np.angle(np.exp(2j*np.pi*y/H).mean())*H/2/np.pi % H; cx = np.angle(np.exp(2j*np.pi*x/H).mean())*H/2/np.pi % H
    img = np.roll(np.roll(M[f], H//2 - int(cy), 0), H//2 - int(cx), 1)[H//2-48:H//2+48, H//2-48:H//2+48]
    mk = np.roll(np.roll(masks[f], H//2 - int(cy), 0), H//2 - int(cx), 1)[H//2-48:H//2+48, H//2-48:H//2+48]
    a.imshow(img, cmap="gray", vmin=0, vmax=1); a.contour(mk, [0.5], colors="r", linewidths=0.8)
    a.set_title(f"frame {f} (t={f*2.5:.0f})", fontsize=8); a.axis("off")
plt.suptitle(f"{d}: lineage member splitting at frame {F1}; red = followed body / its daughters (96 px crop centred on it)", fontsize=9)
plt.tight_layout(); plt.savefig(out, dpi=80)
