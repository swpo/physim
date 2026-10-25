"""Branched cut-vs-twin for the neural-field comet world (deterministic dynamics, so the twin is exact).
Run to T0, pick mature compact comets, cut a fraction of each (front half, rear half, or core disk),
evolve cut and twin copies for T1 and follow the comet by maximum overlap in each arm.
usage: twincut.py world.py seed outdir [T0 T1 frac]"""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, out = int(sys.argv[2]), sys.argv[3]
T0 = float(sys.argv[4]) if len(sys.argv) > 4 else 500.0
T1 = float(sys.argv[5]) if len(sys.argv) > 5 else 100.0
FRAC = float(sys.argv[6]) if len(sys.argv) > 6 else 0.4
os.makedirs(out, exist_ok=True)
dt = w.P["dt"]; size = w.META["size"]

def lab_of(s):
    m = w.f(s["u"]) > 0.5
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    # periodic merge
    for a, b in ((lab[:, 0], lab[:, -1]), (lab[0, :], lab[-1, :])):
        for x, y in set(zip(a[(a > 0) & (b > 0)].tolist(), b[(a > 0) & (b > 0)].tolist())):
            if x != y: lab[lab == y] = x
    return lab

def cen(mask):
    H, W = mask.shape; c = []
    for ax, Nn in ((0, H), (1, W)):
        idx = np.nonzero(mask)[ax]; a = 2 * np.pi * idx / Nn
        c.append((np.arctan2(np.sin(a).mean(), np.cos(a).mean()) % (2 * np.pi)) * Nn / (2 * np.pi))
    return np.array(c)

s = w.init(seed, size)
nT0 = int(round(T0 / dt)); n5 = int(round(5 / dt))
for i in range(nT0 - n5): s = w.step(s)
lab_prev = lab_of(s)
for i in range(n5): s = w.step(s)
lab = lab_of(s)
ids, areas = np.unique(lab[lab > 0], return_counts=True)
med = np.median(areas)
# candidates: compact comets of at least the median area that existed 5 t ago (overlap) and are not touching others
cands = []
for k, A in zip(ids, areas):
    mk = lab == k
    ov = lab_prev[mk]; ov = ov[ov > 0]
    if A < med or len(ov) == 0: continue
    pk = np.bincount(ov).argmax(); mp = lab_prev == pk
    c1, c0 = cen(mk), cen(mp); H, W = mk.shape
    v = (c1 - c0 + np.array([H, W]) / 2) % np.array([H, W]) - np.array([H, W]) / 2
    if np.hypot(*v) < 0.5: continue  # not moving
    cands.append((A, k, v))
cands.sort(key=lambda z: -z[0])
picks = cands[:3]
res = {"seed": seed, "T0": T0, "T1": T1, "frac": FRAC, "median_area": float(med), "comets": []}
nT1 = int(round(T1 / dt)); every = int(round(1.0 / dt))
fig, axs = plt.subplots(2 * len(picks) * 3, 7, figsize=(14, 4 * len(picks) * 3))
row = 0
for A, k, v in picks:
    mk = lab == k; c = cen(mk); H, W = mk.shape
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - c[0] + H / 2) % H - H / 2; dx_ = (xx - c[1] + W / 2) % W - W / 2
    proj = (dy * v[0] + dx_ * v[1]) / np.hypot(*v)
    for mode in ("front", "rear", "core"):
        if mode == "front": cutm = mk & (proj > np.quantile(proj[mk], 1 - FRAC))
        elif mode == "rear": cutm = mk & (proj < np.quantile(proj[mk], FRAC))
        else:
            rr = np.hypot(dy, dx_); cutm = mk & (rr <= np.quantile(rr[mk], FRAC))
        arms = {"twin": copy.deepcopy(s), "cut": w.damage(copy.deepcopy(s), cutm.copy())}
        track = {a: [] for a in arms}; cur = {a: mk.copy() for a in arms}; snaps = {a: [] for a in arms}
        fu0 = w.f(s["u"])[mk].sum()
        for i in range(nT1 + 1):
            if i % every == 0:
                for a, st in arms.items():
                    L = lab_of(st); ov = L[cur[a]]; ov = ov[ov > 0]
                    if len(ov) == 0:
                        track[a].append([i * dt, 0, 0]); cur[a] = np.zeros_like(mk); continue
                    kk = np.bincount(ov).argmax(); m2 = L == kk; cur[a] = m2
                    track[a].append([i * dt, int(m2.sum()), float(w.f(st["u"])[m2].sum())])
                    if (i // every) % (int(T1) // 6) == 0 and len(snaps[a]) < 7:
                        cc = cen(m2); sh = (int(H / 2 - cc[0]), int(W / 2 - cc[1]))
                        snaps[a].append((i * dt, np.roll(w.f(st["u"]), sh, (0, 1)), np.roll(st["r"], sh, (0, 1))))
            if i < nT1:
                for a in arms: arms[a] = w.step(arms[a])
        tw, cu = np.array(track["twin"]), np.array(track["cut"])
        rec = {"comet": int(k), "area0": int(A), "mode": mode, "cut_px": int(cutm.sum()), "cut_frac_px": float(cutm.sum() / A),
               "ratio_cut_twin": [[float(t), float(a2 / max(a1, 1))] for (t, a1, _), (_, a2, _) in zip(tw[::10], cu[::10])],
               "cut_area_t": cu[::10, 1].tolist(), "twin_area_t": tw[::10, 1].tolist(),
               "cut_lost_t": float(cu[cu[:, 1] == 0, 0][0]) if (cu[:, 1] == 0).any() else None,
               "twin_lost_t": float(tw[tw[:, 1] == 0, 0][0]) if (tw[:, 1] == 0).any() else None}
        both = (tw[:, 1] > 0) & (tw[:, 0] >= 5)
        rr = cu[both, 1] / tw[both, 1]
        rec["regrown_t"] = float(tw[both, 0][rr >= 0.9][0]) if (rr >= 0.9).any() else None
        rec["twin_life"] = rec["twin_lost_t"] or T1
        rec["cut_life"] = rec["cut_lost_t"] or T1
        res["comets"].append(rec)
        print(json.dumps({k2: rec[k2] for k2 in ("comet", "area0", "mode", "cut_frac_px", "cut_lost_t", "twin_lost_t", "regrown_t")}), "cut/twin area at t=0,10..100:", [round(r[1], 2) for r in rec["ratio_cut_twin"]], flush=True)
        for j, a in enumerate(("twin", "cut")):
            for q in range(7):
                ax = axs[row, q]; ax.set_xticks([]); ax.set_yticks([])
                if q < len(snaps[a]):
                    t, fu, r = snaps[a][q]
                    ax.imshow(fu[H // 2 - 24:H // 2 + 24, W // 2 - 24:W // 2 + 24], cmap="magma", vmin=0, vmax=1)
                    ax.set_title(f"c{k} {mode} {a} t+{t:.0f} A={track[a][int(t)][1]}", fontsize=7)
            row += 1
fig.suptitle(f"neural-field comets, seed {seed}: cut at t={T0} ({FRAC:.0%}), branched exact twin (top) vs cut (bottom), centred crops of f(u)", fontsize=9)
fig.tight_layout(); fig.savefig(f"{out}/twincut.png", dpi=60)
json.dump(res, open(f"{out}/result.json", "w"), indent=1)
