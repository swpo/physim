"""Local fuel cut on each of several bodies in turn (c44, after c40's cut.py): run the claimed world to T_CUT,
then branch a fed twin and one arm per target, kF=0 inside a disk of radius FRAC x (distance to the target's
nearest other body) around that target only. Logs the target's area (e>0.5 inside the disk) and the bodies outside.
usage: python cutmany.py SEED T_CUT T_AFTER OUT FRAC NTARGETS [MOAT_IN]
MOAT_IN > 0: moat variant: besides kF=0 in the disk, the fuel is also set to 0 every step in the annulus
MOAT_IN <= r <= R around the target (an absorbing ring that blocks fuel diffusing in from the fed medium)."""
import sys, os, json, copy, importlib.util, numpy as np
from scipy import ndimage
seed, tc, ta, out, FR, NT = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], float(sys.argv[5]), int(sys.argv[6])
MOAT = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
spec = importlib.util.spec_from_file_location("w", os.environ.get("CUT_WORLD", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "20261026T1626-c44-cips-lownoise-gen4-claim", "world.py")))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"]); H, W = s["shape"]
cache = os.environ.get("CUT_CACHE", "")
if cache and os.path.exists(cache):
    z = np.load(cache); s.update(e=z["e"], p=z["p"], F=z["F"], s=z["s"], t=float(z["t"]))
else:
    while s["t"] < tc - 1e-9: w.step(s)
    if cache: np.savez(cache, e=s["e"], p=s["p"], F=s["F"], s=s["s"], t=s["t"])
def bodies(e):
    lab, n = ndimage.label(e > 0.5)
    # periodic merge of labels across edges
    for a, b in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:
        for i, j in zip(a, b):
            if i and j and i != j: lab[lab == j] = i
    ids = [i for i in np.unique(lab) if i]
    cs = []
    for i in ids:
        yy, xx = np.nonzero(lab == i)
        ang = lambda v, L: (np.angle(np.exp(2j * np.pi * v / L).mean()) / (2 * np.pi) * L) % L
        cs.append((ang(yy, H), ang(xx, W), len(yy)))
    return cs
def pd(a, b):
    dy = min(abs(a[0] - b[0]), H - abs(a[0] - b[0])); dx = min(abs(a[1] - b[1]), W - abs(a[1] - b[1])); return (dy * dy + dx * dx) ** 0.5
cs = [c for c in bodies(s["e"]) if c[2] >= 30]
nn = [min(pd(c, d) for d in cs if d is not c) for c in cs]
order = list(np.argsort(nn)[::-1][:NT])
if os.environ.get("CUT_AT"):   # explicit targets: the body nearest to each "y,x" point (e.g. a named labkit track's centroid)
    pts = [tuple(map(float, q.split(","))) for q in os.environ["CUT_AT"].split(";")]
    order = [int(np.argmin([pd(c, pt) for c in cs])) for pt in pts]
yy, xx = np.mgrid[0:H, 0:W]
def diskof(c, R):
    dy = (yy - c[0] + H / 2) % H - H / 2; dx = (xx - c[1] + W / 2) % W - W / 2; return dy * dy + dx * dx <= R * R
arms = {"fed": (None, None)}
for k, i in enumerate(order):
    arms[f"cut{k}"] = (cs[i], FR * nn[i])
res, snaps = {"n_bodies_at_cut": len(cs), "targets": {}}, {}
for name, (c, R) in arms.items():
    a = copy.deepcopy(s)
    if c is not None:
        a["par"] = dict(s["par"], cut_t=tc, cut_r=R, cut_y=c[0], cut_x=c[1])
    log, k = [], 0
    if c is not None:
        dy_ = (yy - c[0] + H / 2) % H - H / 2; dx_ = (xx - c[1] + W / 2) % W - W / 2; r2 = dy_ * dy_ + dx_ * dx_
        moat = (r2 >= MOAT * MOAT) & (r2 <= R * R)
    discs = {n2: diskof(c2, R2) for n2, (c2, R2) in arms.items() if c2 is not None}
    while a["t"] <= tc + ta + 1e-9:
        if k % 250 == 0:
            e = a["e"]; row = {"t": round(a["t"]), "n_bodies": len([b for b in bodies(e) if b[2] >= 10])}
            for n2, dk in discs.items():
                row[n2 + "_px"] = int(((e > 0.5) & dk).sum())
            if c is not None:
                dk = discs[name]; row["outside"] = len([b for b in bodies(np.where(dk, 0, e)) if b[2] >= 10]); row["F_disk"] = float(a["F"][dk].mean())
            log.append(row)
        if k % 5000 == 0: snaps.setdefault(name, []).append((round(a["t"]), a["e"].copy()))
        w.step(a); k += 1
        if c is not None and MOAT > 0: a["F"] = np.where(moat, 0.0, a["F"])
    res[name] = log
    if c is not None: res["targets"][name] = {"centroid": [float(c[0]), float(c[1])], "area": int(c[2]), "R": float(R), "nn": float(R / FR)}
    print(name, log[0], log[-1], flush=True)
json.dump(res, open(out + ".json", "w"), indent=0)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
names = list(snaps); nc = len(snaps["fed"])
fig, ax = plt.subplots(len(names), nc, figsize=(1.8 * nc, 1.9 * len(names)))
th = np.linspace(0, 2 * np.pi, 100)
for r, n in enumerate(names):
    for j in range(nc):
        t, e = snaps[n][j]; ax[r, j].imshow(e, cmap="magma", vmin=0, vmax=1); ax[r, j].axis("off")
        for n2, (c2, R2) in arms.items():
            if c2 is not None:
                ax[r, j].plot(c2[1] + R2 * np.cos(th), c2[0] + R2 * np.sin(th), "w-" if n2 == n else "c:", lw=0.7 if n2 == n else 0.4)
        ax[r, j].set_title(f"{n} t={t}", fontsize=7)
fig.suptitle(f"seed {seed}: one arm per target, kF=0 only inside that arm's solid disk from t={tc:.0f} (dotted: other arms' disks); e shown", fontsize=8)
fig.tight_layout(); fig.savefig(out + ".png", dpi=65)
