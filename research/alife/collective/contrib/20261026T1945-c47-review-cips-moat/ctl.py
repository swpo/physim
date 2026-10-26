"""c47 controls for c44's moat cut, branched from the same cached t=12000 state as cutmany.py (same target choice).
Arms per target: 'moat' (kF=0 in disk + F=0 in annulus MOAT_IN<=r<=R, as c44), 'iso' (annulus F=0 only, kF kept inside
the disk: the body is isolated but its own footprint still regrows fuel), 'moat_dt2' (moat at world dt/2, operators rebuilt).
Also reports each target's max pixel distance from its centroid (does the annulus touch the body?).
usage: CUT_WORLD=... CUT_CACHE=... python ctl.py SEED T_AFTER FRAC NTARGETS MOAT_IN OUT"""
import sys, os, json, copy, importlib.util, numpy as np
from scipy import ndimage
seed, ta, FR, NT, MOAT, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
def load(dt=None):
    if dt is not None: os.environ["WORLD_P"] = json.dumps({"dt": dt})
    spec = importlib.util.spec_from_file_location("w%s" % dt, os.environ["CUT_WORLD"])
    w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(seed, w.META["size"]); z = np.load(os.environ["CUT_CACHE"])
    s.update(e=z["e"].copy(), p=z["p"].copy(), F=z["F"].copy(), s=z["s"].copy(), t=float(z["t"])); return w, s
w, s0 = load(); H, W = s0["shape"]; tc = s0["t"]
def labels(e):
    lab, n = ndimage.label(e > 0.5)
    for a, b in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:
        for i, j in zip(a, b):
            if i and j and i != j: lab[lab == j] = i
    return lab
def bodies(e):
    lab = labels(e); cs = []
    for i in [i for i in np.unique(lab) if i]:
        yy, xx = np.nonzero(lab == i)
        ang = lambda v, L: (np.angle(np.exp(2j * np.pi * v / L).mean()) / (2 * np.pi) * L) % L
        cs.append((ang(yy, H), ang(xx, W), len(yy), i))
    return cs, lab
def pd(a, b):
    dy = min(abs(a[0] - b[0]), H - abs(a[0] - b[0])); dx = min(abs(a[1] - b[1]), W - abs(a[1] - b[1])); return (dy * dy + dx * dx) ** 0.5
cs, lab0 = bodies(s0["e"]); cs = [c for c in cs if c[2] >= 30]
nn = [min(pd(c, d) for d in cs if d is not c) for c in cs]
order = list(np.argsort(nn)[::-1][:NT])
yy, xx = np.mgrid[0:H, 0:W]
def r2of(c):
    dy = (yy - c[0] + H / 2) % H - H / 2; dx = (xx - c[1] + W / 2) % W - W / 2; return dy * dy + dx * dx
res = {"tc": tc, "targets": {}}
for k, i in enumerate(order):
    c = cs[i]; R = FR * nn[i]; r2 = r2of(c)
    rmax = float(np.sqrt(r2[lab0 == c[3]].max()))
    disk = r2 <= R * R; moat = (r2 >= MOAT * MOAT) & disk
    tg = {"area": int(c[2]), "R": float(R), "rmax_body": rmax}
    for arm in ["moat", "iso", "moat_dt2"]:
        if arm == "moat_dt2": ww, a = load(dt=0.5 * s0["par"]["dt"])
        else: ww, a = w, copy.deepcopy(s0)
        if arm in ("moat", "moat_dt2"): a["par"] = dict(a["par"], cut_t=tc, cut_r=R, cut_y=c[0], cut_x=c[1])
        log = []; nxt = tc
        while a["t"] <= tc + ta + 1e-9:
            if a["t"] >= nxt - 1e-9:
                e = a["e"]; log.append({"t": round(a["t"], 1), "target_px": int(((e > 0.5) & disk).sum()),
                    "e_disk": float(e[disk].sum()), "F_in": float(a["F"][r2 < MOAT * MOAT].mean())}); nxt += 25
            ww.step(a); a["F"] = np.where(moat, 0.0, a["F"])
        tg[arm] = log; print(k, arm, log[0], log[-1], flush=True)
    res["targets"]["cut%d" % k] = tg
json.dump(res, open(out + ".json", "w"), indent=0)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
for k, (n, tg) in enumerate(res["targets"].items()):
    for arm, ls in [("moat", "-"), ("iso", "--"), ("moat_dt2", ":")]:
        t = [r["t"] - tc for r in tg[arm]]
        ax[0].plot(t, [r["target_px"] / tg["area"] for r in tg[arm]], ls, color="C%d" % k, label=f"{n} {arm}" if k == 0 or arm == "moat" else None)
        ax[1].plot(t, [r["F_in"] for r in tg[arm]], ls, color="C%d" % k)
ax[0].set_xlabel("t - t_cut"); ax[0].set_ylabel("target area (e>0.5 in disk) / area at cut"); ax[0].legend(fontsize=6)
ax[1].set_xlabel("t - t_cut"); ax[1].set_ylabel("mean F within r<MOAT_IN")
fig.suptitle(f"seed {seed}: moat (solid), isolation only, kF kept inside (dashed), moat at dt/2 (dotted)", fontsize=8)
fig.tight_layout(); fig.savefig(out + ".png", dpi=80)
