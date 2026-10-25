import os, json, sys, numpy as np, importlib.util
from scipy import ndimage
res = []
for P0 in (None,):
    pass
def run(over, mcs=600, seed=0):
    os.environ["WORLD_P"] = json.dumps(over)
    spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(seed, (128, 128)); H = W = 128
    def cents(sig):
        out = {}
        for c in range(1, int(w.P["N"]) + 1):
            ys, xs = np.nonzero(sig == c)
            if len(ys) == 0: continue
            out[c] = np.array([np.angle(np.exp(2j*np.pi*ys/H).mean())*H/(2*np.pi), np.angle(np.exp(2j*np.pi*xs/W).mean())*W/(2*np.pi)])
        return out
    for i in range(100): s = w.step(s)
    c0 = cents(s["sig"]); disp = {c: np.zeros(2) for c in c0}; prev = c0
    for i in range(mcs):
        s = w.step(s)
        if i % 10 == 9:
            cur = cents(s["sig"])
            for c in disp:
                if c in cur and c in prev: disp[c] += (cur[c] - prev[c] + 64) % 128 - 64
            prev = cur
    A = s["area"][1:]; per = s["perim"][1:]
    frag = np.mean([ndimage.label(s["sig"] == c)[1] for c in range(1, int(w.P["N"]) + 1)])
    d = np.array([np.hypot(*v) for v in disp.values()]) / (2 * np.sqrt(np.mean(A) / np.pi))
    return dict(over=over, area=float(A.mean()), perim=float(per.mean()), frag=float(frag), BL_median=float(np.median(d)), BL_max=float(d.max()))
for over in json.loads(sys.argv[1]):
    print(json.dumps(run(over)), flush=True)
