"""Audit arms from a saved state of the claimed world (construction lens).
usage: python arms.py STATE.npz T_AFTER OUTPREFIX ARMSPEC_JSON [LOG_DT]
ARMSPEC_JSON: {"name": {"par": {...overrides of world P...}, "moat": [r_in, R], "target": "auto"|null}, ...}
A "target" arm picks the body whose nearest other body is farthest (as c40/c44 cut.py) and applies
cut_r = 0.75 x that distance (kF=0 in the disk, the world's own cut option) and, if "moat" is given,
F=0 every step in the annulus r_in <= r <= R (c44's absorbing moat).
Logs bodies (periodic-merged, >=10 px), body areas, total body area, mean F, every LOG_DT t."""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage

CLAIM = "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
spec = importlib.util.spec_from_file_location("w", CLAIM)
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
stf, ta, out, armspec = sys.argv[1], float(sys.argv[2]), sys.argv[3], json.loads(sys.argv[4])
LOG = float(sys.argv[5]) if len(sys.argv) > 5 else 50.0
z = np.load(stf)
seed = 0


def bodies(e, H, W):
    lab, n = ndimage.label(e > 0.5)
    for a, b in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:
        for i, j in zip(a, b):
            if i and j and i != j:
                lab[lab == j] = i
    out = []
    for i in [i for i in np.unique(lab) if i]:
        yy, xx = np.nonzero(lab == i)
        ang = lambda v, L: (np.angle(np.exp(2j * np.pi * v / L).mean()) / (2 * np.pi) * L) % L
        out.append((float(ang(yy, H)), float(ang(xx, W)), int(len(yy))))
    return out


res, snaps = {}, {}
for name, spec_a in armspec.items():
    s = w.init(seed, w.META["size"])
    s["par"] = dict(s["par"], **spec_a.get("par", {}))
    s.update(e=z["e"].copy(), p=z["p"].copy(), F=z["F"].copy(), s=z["s"].copy(), t=float(z["t"]))
    if spec_a.get("F1"):
        s["F"] = np.ones_like(s["F"])   # reservoir: fuel held at 1 everywhere (with par hold=1)
    H, W = s["shape"]
    t0 = s["t"]
    tgt = None
    moat = None
    R = None
    if spec_a.get("target"):
        cs = [c for c in bodies(s["e"], H, W) if c[2] >= 30]
        def pd(a, b):
            dy = min(abs(a[0] - b[0]), H - abs(a[0] - b[0])); dx = min(abs(a[1] - b[1]), W - abs(a[1] - b[1])); return (dy * dy + dx * dx) ** 0.5
        nn = [min(pd(c, d) for d in cs if d is not c) for c in cs]
        k = int(np.argsort(nn)[::-1][spec_a.get("rank", 0)])
        tgt = cs[k]; R = spec_a.get("frac", 0.75) * nn[k]
        s["par"].update(cut_t=t0, cut_r=R, cut_y=tgt[0], cut_x=tgt[1])
        yy, xx = np.mgrid[0:H, 0:W]
        dy = (yy - tgt[0] + H / 2) % H - H / 2; dx = (xx - tgt[1] + W / 2) % W - W / 2
        r2 = dy * dy + dx * dx
        disk = r2 <= R * R
        if spec_a.get("moat"):
            moat = (r2 >= spec_a["moat"] ** 2) & disk
    log = []
    k = 0
    nlog = max(1, int(round(LOG / s["par"]["dt"])))
    nsnap = max(1, int(round(ta / 5 / s["par"]["dt"])))
    while s["t"] <= t0 + ta + 1e-9:
        if k % nlog == 0:
            bs = [b for b in bodies(s["e"], H, W) if b[2] >= 10]
            row = {"t": round(s["t"], 1), "n": len(bs), "area": int((s["e"] > 0.5).sum()),
                   "areas": sorted(b[2] for b in bs), "mean_F": float(s["F"].mean()), "max_e": float(s["e"].max()),
                   "mean_e": float(s["e"].mean())}
            if tgt is not None:
                row["target_px"] = int(((s["e"] > 0.5) & disk).sum())
                row["outside_n"] = len([b for b in bodies(np.where(disk, 0, s["e"]), H, W) if b[2] >= 10])
                row["F_disk"] = float(s["F"][disk].mean())
            log.append(row)
        if k % nsnap == 0:
            snaps.setdefault(name, []).append((round(s["t"]), s["e"].copy()))
        w.step(s); k += 1
        if moat is not None:
            s["F"] = np.where(moat, 0.0, s["F"])
    res[name] = {"spec": spec_a, "target": tgt, "R": R, "log": log}
    print(name, {k2: v for k2, v in log[0].items() if k2 != "areas"}, {k2: v for k2, v in log[-1].items() if k2 != "areas"}, flush=True)
json.dump(res, open(out + ".json", "w"), indent=0)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
names = list(snaps); nc = max(len(v) for v in snaps.values())
fig, ax = plt.subplots(len(names), nc, figsize=(1.9 * nc, 2.0 * len(names)), squeeze=False)
th = np.linspace(0, 2 * np.pi, 100)
for r, n in enumerate(names):
    for j in range(nc):
        ax[r, j].axis("off")
        if j < len(snaps[n]):
            t, e = snaps[n][j]; ax[r, j].imshow(e, cmap="magma", vmin=0, vmax=1)
            nb = len([b for b in bodies(e, *e.shape) if b[2] >= 10])
            ax[r, j].set_title(f"{n} t={t} n={nb}", fontsize=7)
            tg = res[n]["target"]
            if tg is not None:
                ax[r, j].plot(tg[1] + res[n]["R"] * np.cos(th), tg[0] + res[n]["R"] * np.sin(th), "c-", lw=0.6)
fig.suptitle(f"{os.path.basename(out)}: enzyme e from {os.path.basename(stf)}", fontsize=8)
fig.tight_layout(); fig.savefig(out + ".png", dpi=70)
