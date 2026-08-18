"""probe6_portrait.py — P2d: portraits + w-well signatures + quick noise for 2 candidate pairs.

PAIR-EQD : A=(k1=-0.7,k4=1.0,Du=1.0)  B=(k1=-1.3,k4=1.8,Du=1.0)   (dials only)
PAIR-DU  : A=(k1=-1.0,k4=1.4,Du=1.0)  B=(k1=-1.6507,k4=2.15,Du=0.65) (strong size contrast)
For each pair, each species alone (T=500): area, umax, w-well depth/width, v-well,
patch features; then noise=2e-3 x 500tu survival.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import default_params, background, run, persistence_verdict
from concurrent.futures import ProcessPoolExecutor

PAIRS = {
 "EQD": dict(k1_1=-0.7, k4_1=1.0, Du_1=1.0, k1_2=-1.3, k4_2=1.8, Du_2=1.0),
 "DU":  dict(k1_1=-1.0, k4_1=1.4, Du_1=1.0, k1_2=-1.6507, k4_2=2.15, Du_2=0.65),
}

def wwell(F, bg, L=96):
    w = F[-1]
    wmin = float(w.min()); depth = bg["w"] - wmin
    # width: pixels below bg_w - depth/2
    width = int((w < bg["w"] - 0.5 * depth).sum())
    return depth, width

def one(job):
    pair, sp, noise = job
    p = default_params(); p.update(PAIRS[pair])
    rec = dict(pair=pair, species=sp, noise=noise)
    r = run(p, arch="vvw", T=500.0, spots=((sp, 48, 48, 2.0, 3.0),),
            noise=noise, seed=3)
    if r["status"] != "ok":
        rec.update(verdict=r["status"]); return rec
    s = r["series"]; i = sp
    v = persistence_verdict(s, f"a{i}", f"n{i}")
    depth, width = wwell(r["F"], r["bg"])
    # patch features at center 5x5
    F = r["F"]; bg = r["bg"]
    c = 48; sl = np.s_[c-2:c+3, c-2:c+3]
    du1 = float(F[0][sl].mean() - bg["u1"]); du2 = float(F[1][sl].mean() - bg["u2"])
    dw = float(F[4][sl].mean() - bg["w"])
    rec.update(verdict=v, area=s[f"a{i}"][-1], umax=s[f"m{i}"][-1],
               w_depth=round(depth,4), w_width=width,
               patch_du1=round(du1,4), patch_du2=round(du2,4), patch_dw=round(dw,4))
    return rec

if __name__ == "__main__":
    jobs = [(pair, sp, n) for pair in PAIRS for sp in (1, 2) for n in (0.0, 2e-3)]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            print(rec, flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe6_portrait.json"), "w"), indent=1)
