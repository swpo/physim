"""Deciding control for M: grow the claimed world from noise to T0 (colonization, cells swimming),
then copy ONE mature cell (its phi>0.05 halo grown 4 px: phi, K, L, w, local S) into a fresh,
uniform bath (S=1, nothing else) and follow it alone. Comparator: the same cell left in place
(unmodified run), tracked by overlap. Body length 2 sqrt(A/pi); path unwrapped on the torus.
usage: python isolate.py world.py seed T0 T1 ncells out_prefix [key=val ...]"""
import sys, json, os, copy
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
world, seed, T0, T1, ncell, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
wp = {"drive": "kernel", "mu": 1.0, "kd": 0.08, "chi": 5}
for a in sys.argv[7:]:
    k, v = a.split("=", 1)
    try: wp[k] = float(v) if ("." in v or "e" in v) else int(v)
    except ValueError: wp[k] = v
os.environ["WORLD_P"] = json.dumps(wp)
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world
W = load_world(world); H = W.META["size"][0]; dt = W.P["dt"]
s = W.init(seed, (H, H))
for i in range(int(T0 / dt)): s = W.step(s)

def label(phi):
    lab, n = ndimage.label(phi > 0.5)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, w in set(zip(a.tolist(), b.tolist())):
            if u and w and u != w: lab[lab == w] = u
    return lab
def cent(mask):
    ys, xs = np.nonzero(mask)
    return np.array([np.angle(np.exp(2j*np.pi*ys/H).mean())*H/(2*np.pi) % H, np.angle(np.exp(2j*np.pi*xs/H).mean())*H/(2*np.pi) % H])

lab = label(s["phi"]); ids = [l for l in np.unique(lab)[1:]]
areas = {l: (lab == l).sum() for l in ids}
med = np.median(list(areas.values()))
cand = sorted(ids, key=lambda l: abs(areas[l] - med))[:ncell]
print("T0", T0, "cells", len(ids), "median area", med, flush=True)

def follow(st, mask0, T, tag):
    """overlap-track the body that starts as mask0; stop at a split/merge/death; return path in BL."""
    m = mask0; c0 = cent(m); path = [np.zeros(2)]; A = [m.sum()]; ev = "survives"; snaps = []
    nst = int(T / dt); every = int(50 / dt)
    for i in range(1, nst + 1):
        st = W.step(st)
        if i % every: continue
        lb = label(st["phi"])
        hit = [l for l in np.unique(lb[m]) if l]
        if not hit: ev = "dies t+%d" % (i*dt); break
        if len(hit) > 1: ev = "splits t+%d" % (i*dt); break
        nm = lb == hit[0]
        back = [l for l in np.unique(label(st["phi"])[nm]) if l]
        if nm.sum() > 1.6 * m.sum() and tag == "inplace":
            ev = "merges t+%d" % (i*dt); break
        cpos = cent(nm); d = (cpos - c0 + H/2) % H - H/2
        path.append(path[-1] + d); c0 = cpos; m = nm; A.append(nm.sum())
        if i % int(T / 6 / dt) == 0: snaps.append((i*dt, st["phi"].copy(), st["L"].copy(), st["S"].copy()))
    P = np.array(path); BL = 2*np.sqrt(np.mean(A)/np.pi)
    return dict(tag=tag, event=ev, t_followed=(len(path)-1)*50, net_BL=float(np.linalg.norm(P[-1])/BL),
                path_BL=float(np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))/BL) if len(P) > 1 else 0.0,
                BL_px=float(BL), area_ratio=float(max(A)/min(A))), snaps

res = []
for l in cand:
    m = lab == l
    halo = ndimage.binary_dilation(s["phi"] > 0.05, iterations=1) & ndimage.binary_dilation(m, iterations=6)
    iso = copy.deepcopy({k: v for k, v in s.items() if isinstance(v, np.ndarray) and v.shape == (H, H)})
    for k in ("K", "L", "phi", "w"):
        iso[k] = np.where(halo, s[k], 0.0)
    iso["S"] = np.where(halo, s["S"], 1.0)
    r_iso, sn = follow(iso, m.copy(), T1, "isolated")
    r_in, _ = follow(copy.deepcopy({k: v for k, v in s.items() if isinstance(v, np.ndarray) and v.shape == (H, H)}), m.copy(), T1, "inplace")
    res.append({"cell": int(l), "area": int(areas[l]), "isolated": r_iso, "inplace": r_in})
    print(json.dumps(res[-1]), flush=True)
    if sn:
        fig, ax = plt.subplots(3, len(sn), figsize=(2*len(sn), 6), squeeze=False)
        for j, (t, ph, L, S) in enumerate(sn):
            ax[0, j].imshow(ph, vmin=0, vmax=1, cmap="gray"); ax[0, j].set_title("t0+%d phi" % t, fontsize=7)
            ax[1, j].imshow(L, vmin=0, vmax=1.5, cmap="viridis"); ax[1, j].set_title("L", fontsize=7)
            ax[2, j].imshow(S, vmin=0, vmax=1, cmap="magma"); ax[2, j].set_title("S", fontsize=7)
        for a in ax.ravel(): a.axis("off")
        plt.suptitle("cell %d isolated at t=%d (seed %d): %s, net %.2f BL" % (l, T0, seed, r_iso["event"], r_iso["net_BL"]), fontsize=8)
        plt.tight_layout(); plt.savefig("%s_cell%d.png" % (out, l), dpi=70); plt.close()
json.dump(res, open(out + ".json", "w"), indent=1)
