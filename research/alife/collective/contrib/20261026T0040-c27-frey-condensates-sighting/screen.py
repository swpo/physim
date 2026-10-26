import os, json, sys, numpy as np, importlib.util
from scipy import ndimage
def run(over, steps=int(os.environ.get("STEPS", "12000")), seed=0):
    os.environ["WORLD_P"] = json.dumps(over)
    spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(seed, (128, 128)); H = W = 128
    def comps(phi):
        lab, n = ndimage.label(phi > 0)
        if n == 0: return [], lab
        cm = ndimage.center_of_mass(np.ones_like(phi), lab, range(1, n + 1)); ar = ndimage.sum(np.ones_like(phi), lab, range(1, n + 1))
        return [(np.array(c), a) for c, a in zip(cm, ar) if a >= 8], lab
    hist = []
    for i in range(steps):
        s = w.step(s)
        if i % (steps // 30) == steps // 30 - 1: hist.append(comps(s["phi"])[0])
    n = [len(h) for h in hist]
    # crude speed: for each comp at the last two samples, nearest-neighbour displacement
    sp = []
    for a, b in zip(hist[-6:-1], hist[-5:]):
        for c, A in b:
            if a:
                d = min(np.hypot(*((c - c0 + 64) % 128 - 64)) for c0, _ in a); sp.append(d / ((steps // 30) * w.P["dt"]))
    return dict(over=over, n_series=n[::3], mean_area=float(np.mean([A for _, A in hist[-1]])) if hist[-1] else 0,
                speed_median=float(np.median(sp)) if sp else 0, s_min=float(s["s"].min()), finite=bool(np.isfinite(s["phi"]).all()))
for over in json.loads(sys.argv[1]):
    print(json.dumps(run(over)), flush=True)
