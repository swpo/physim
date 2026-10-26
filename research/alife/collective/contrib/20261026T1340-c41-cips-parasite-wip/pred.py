"""c41: parasitic autocatalyst on c40's CIPS condensates (after Froese, Ikegami & Virgo 2012).
c: predator species, dc/dt = Dc Lsc^2 lap c - div(chic Lsc^2 c(1-c) grad p) + kp e c^2 - kd c (chic: drift up the prey-made product, same operator as the enzyme); order=1 uses kp e c (1-c) instead of kp e c^2 ; e loses kp e c^2 (enzyme eaten, converted to c).
Usage: pred.py checkpoint SEED T0  (runs base world to T0 and saves ckpt_s{SEED}_t{T0}.npz)
       pred.py run '<params json>' ckpt TA tag   (branches from a checkpoint; params: kp, kd, Dc, c0, cmode)"""
import os, sys, json, importlib.util, numpy as np
from scipy import ndimage as ndi
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("w", os.path.join(here, "world_base.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
from labkit import ops
if sys.argv[1] == "checkpoint":
    seed, T0 = int(sys.argv[2]), float(sys.argv[3])
    s = w.init(seed, w.META["size"])
    while s["t"] < T0 - 1e-9: w.step(s)
    np.savez(os.path.join(here, "ckpt_s%d_t%d.npz" % (seed, T0)), e=s["e"], p=s["p"], F=s["F"], t=s["t"], seed=seed)
    sys.exit()
q = json.loads(sys.argv[2]); ck = np.load(sys.argv[3]); TA = float(sys.argv[4]); tag = sys.argv[5]
s = w.init(int(ck["seed"]), w.META["size"]); s["e"], s["p"], s["F"], s["t"] = ck["e"].copy(), ck["p"].copy(), ck["F"].copy(), float(ck["t"])
kp, kd, Dc, chic = q.get("kp", 1.0), q.get("kd", 0.05), q.get("Dc", 0.1), q.get("chic", 0.0)
rng = np.random.default_rng(q.get("cseed", 1)); H, W = s["shape"]
if q.get("cmode", "noise") == "noise":       # uniform weak noise everywhere (unstructured)
    c = q.get("c0", 0.02) * np.abs(rng.standard_normal((H, W)))
else:                                         # a few random patches (planted)
    c = np.zeros((H, W)); yy, xx = s["yy"], s["xx"]
    for _ in range(int(q.get("npatch", 4))):
        y0, x0 = rng.uniform(0, H), rng.uniform(0, W)
        c += 0.8 * np.exp(-(((yy - y0 + H / 2) % H - H / 2) ** 2 + ((xx - x0 + W / 2) % W - W / 2) ** 2) / 18.0)
L = ops.lap_symbol(H, W) * s["par"]["Lsc"] ** 2; dt = s["par"]["dt"]; Lc = 1.0 / (1 - dt * Dc * L)
def count(f, thr):
    lab, n = ndi.label(f > thr, structure=np.ones((3, 3))); sz = ndi.sum(np.ones_like(f), lab, range(1, n + 1))
    return int((np.array(sz) >= 20).sum()) if n else 0
log = []; snaps = []; k = 0; T0 = s["t"]
while s["t"] <= T0 + TA + 1e-9:
    if k % 500 == 0:
        log.append((round(s["t"]), count(s["e"], 0.5), count(c, 0.3), round(float(c.sum()), 1), round(float(s["F"].mean()), 3)))
        if k % 5000 == 0: snaps.append((s["t"], s["e"].copy(), c.copy()))
    eat = kp * np.clip(s["e"], 0, None) * (c * c if q.get("order", 2) == 2 else c * np.clip(1 - c, 0, None))
    drift = w.vf_flux_div(np.clip(c, 0, 1), s["p"], chic * s["par"]["Lsc"] ** 2) if chic else 0.0
    w.step(s)
    s["e"] = s["e"] - dt * eat
    c = ops.irfft2(ops.rfft2(c + dt * (eat - kd * c) - dt * drift) * Lc, (H, W)); c = np.clip(c, 0, None)
    k += 1
print(tag, json.dumps(q), "| t, prey, pred spots, c total, F:", log[::max(1, len(log) // 16)], flush=True)
json.dump(dict(params=q, log=log), open(os.path.join(here, "pred_%s.json" % tag), "w"))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
n = len(snaps); fig, ax = plt.subplots(1, n, figsize=(2.2 * n, 2.4))
for a, (t, e, cc) in zip(np.atleast_1d(ax), snaps):
    rgb = np.dstack([np.clip(cc / 0.6, 0, 1), np.clip(e, 0, 1), np.clip(e, 0, 1) * 0.6]); a.imshow(rgb); a.set_title("t=%.0f" % t, fontsize=7); a.axis("off")
fig.suptitle("%s %s (cyan-green: enzyme, red: predator c)" % (tag, json.dumps(q)), fontsize=7); fig.tight_layout(); fig.savefig(os.path.join(here, "pred_%s.png" % tag), dpi=65)
