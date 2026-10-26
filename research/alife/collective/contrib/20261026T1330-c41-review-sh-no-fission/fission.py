"""Classify molecule-count increases: a molecule at t whose spots end up in >= 2 molecules at t+dt.
Records sizes (spots) of the pieces. usage: fission.py '<WORLD_P json>' nsteps"""
import os, sys, json, importlib.util, numpy as np
from scipy import ndimage as ndi
wp = json.loads(sys.argv[1]); nsteps = int(sys.argv[2])
os.environ["WORLD_P"] = json.dumps(wp)
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(wp.get("seed", 0), w.META["size"]); dx = w.P["L"] / w.P["N"]
def lab(u):
    sp, ns = ndi.label(ndi.gaussian_filter(u, 1.0) > 0.6)
    mol, nm = ndi.label(ndi.binary_dilation(sp > 0, iterations=max(1, int(round(2.2 / dx)))), structure=np.ones((3, 3)))
    # periodic merge
    for a, b in ((mol[0], mol[-1]), (mol[:, 0], mol[:, -1])):
        for i, j in set(zip(a.tolist(), b.tolist())):
            if i and j and i != j: mol[mol == j] = i
    spm = {}
    for k in range(1, ns + 1):
        ys, xs = np.nonzero(sp == k); spm[k] = mol[ys[0], xs[0]]
    sizes = {}
    for k, m in spm.items(): sizes[m] = sizes.get(m, 0) + 1
    return sp, mol, sizes
prev = None; events = []; hist = []; U = []
for k in range(nsteps):
    s = w.step(s)
    if k % 50 == 0:
        sp, mol, sizes = lab(s["u"])
        if prev is not None and k * w.P["dt"] > 150:
            pmol, psizes = prev
            for m, n in psizes.items():
                if n < 2: continue
                kids = [c for c in np.unique(mol[pmol == m]) if c]
                kids = [c for c in kids if sizes.get(c, 0) >= 1]
                if len(kids) >= 2:
                    kk = sorted(kids, key=lambda c: -sizes[c])[:2]
                    pts = [np.argwhere(mol == c)[0] for c in kk]
                    events.append([round(s["t"]), n, sorted([sizes[c] for c in kids], reverse=True), len(hist) - 1, pts, sorted([sizes[c] for c in kk])[0]])
        hist.append((mol, sizes)); U.append(s['u'].copy())
        prev = (mol, sizes)
# persistence: follow each piece's pixel 10 censuses (50 t) later by the molecule under a 3x3 patch; pieces persist if different molecules
def follow(i, pt, j):
    y, x = pt
    for jj in range(i + 1, j + 1):
        m = hist[jj][0]; H, W = m.shape
        patch = m[np.ix_([(y + d) % H for d in range(-3, 4)], [(x + d) % W for d in range(-3, 4)])]
        v = patch[patch > 0]
        if not len(v): return None
        lab_ = np.bincount(v).argmax(); ys, xs = np.nonzero(m == lab_)
        # move the tracked point to that molecule's pixel nearest the old point
        d2 = ((ys - y + H/2) % H - H/2) ** 2 + ((xs - x + W/2) % W - W/2) ** 2; q = d2.argmin(); y, x = ys[q], xs[q]
    return lab_
pers = []
for e in events:
    i = e[3]; j = i + 10
    if j >= len(hist) or e[5] < 2: continue
    a, b = follow(i, e[4][0], j), follow(i, e[4][1], j)
    if a is not None and b is not None and a != b: pers.append(e)
big = [e for e in events if e[5] >= 2]
print("persistent >= 50 t, both pieces >= 2 spots:", len(pers), "of", len([e for e in big if e[3] + 10 < len(hist)]))
for e in pers[:15]: print(e[0], e[1], e[2])
print(json.dumps(wp)); print("break-up events (parent >=2 spots):", len(events), "; both pieces >= 2 spots:", len(big))


import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sel = pers[:4]
fig, ax = plt.subplots(len(sel), 6, figsize=(12, 2.1 * len(sel)), squeeze=False)
for r, e in enumerate(sel):
    i = e[3]; y, x = e[4][0]; H, W = U[0].shape
    for c, j in enumerate([i - 4, i - 2, i - 1, i, i + 4, i + 10]):
        j = min(max(j, 0), len(U) - 1)
        crop = np.roll(np.roll(U[j], H // 2 - y, 0), W // 2 - x, 1)[H//2-40:H//2+40, W//2-40:W//2+40]
        ax[r, c].imshow(crop, cmap="magma", vmin=-0.5, vmax=2); ax[r, c].axis("off")
        ax[r, c].set_title("t=%d" % (150 + (j - (len(U) - len(hist))) * 5 if False else (j * 5)), fontsize=7)
    ax[r, 0].set_title("t=%d  %d spots -> %s" % (e[0], e[1], e[2][:3]), fontsize=7, loc="left")
plt.suptitle("SH spot molecules breaking up on a consumed resource (crop follows the larger piece; frames every 5 t; last = +50 t)", fontsize=8)
plt.tight_layout(); plt.savefig("fission_events.png", dpi=80)
