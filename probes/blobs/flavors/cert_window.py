"""cert_window.py — B1 window: persistence window >=1.3x in >=2 dials per species.

For each species (other species locked at pair-MAXC dials), scan its own k1_i and
k4_i independently around the locked value. A dial value is IN the window if:
bg exists & stable, lone blob persistent at T=300 (day0-style verdict).
Window ratio = hi/lo of contiguous in-window interval containing the locked value
(|k1| used for k1). Also scans Du_i as a bonus 3rd dial.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, background, bg_stability, run, persistence_verdict
from concurrent.futures import ProcessPoolExecutor

UB = -0.86756
LOCK = dict(k1_1=-1.0, k4_1=1.4, Du_1=0.65,
            k1_2=-1.0 + 0.75*UB, k4_2=2.15, Du_2=0.65)

def one(job):
    sp, dial, val = job
    p = default_params(); p.update(LOCK)
    key = f"{dial}_{sp}"
    p[key] = val
    rec = dict(species="AB"[sp-1], dial=dial, val=round(val,4))
    bg = background(p, arch="vvw")
    if bg is None:
        rec.update(ok=False, why="no_bg"); return rec
    g, kw, _ = bg_stability(p, bg, arch="vvw")
    if g > 1e-6:
        rec.update(ok=False, why="bg_unstable"); return rec
    r = run(p, arch="vvw", T=300.0, spots=((sp, 48, 48, 2.0, 3.0),))
    if r["status"] != "ok":
        rec.update(ok=False, why=r["status"]); return rec
    v = persistence_verdict(r["series"], f"a{sp}", f"n{sp}")
    rec.update(ok=(v == "persistent"), why=v,
               a=r["series"][f"a{sp}"][-1])
    return rec

def window_ratio(vals, oks, locked):
    """Contiguous ok-interval containing locked value; ratio hi/lo (abs)."""
    order = np.argsort(vals)
    vs = np.array(vals)[order]; os_ = np.array(oks)[order]
    li = int(np.argmin(np.abs(vs - locked)))
    if not os_[li]:
        return None, None, None
    lo = li
    while lo > 0 and os_[lo-1]:
        lo -= 1
    hi = li
    while hi < len(vs)-1 and os_[hi+1]:
        hi += 1
    a, b = abs(vs[lo]), abs(vs[hi])
    lo_v, hi_v = min(a, b), max(a, b)
    return float(hi_v/lo_v), float(vs[lo]), float(vs[hi])

if __name__ == "__main__":
    scans = {
        (1, "k1"): [-1.35, -1.25, -1.15, -1.05, -1.0, -0.95, -0.85, -0.75, -0.7],
        (1, "k4"): [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.75, 1.9, 2.05],
        (1, "Du"): [0.4, 0.5, 0.65, 0.8, 0.95],
        (2, "k1"): [-2.2, -2.05, -1.9, -1.75, -1.65067, -1.55, -1.45, -1.35, -1.25],
        (2, "k4"): [1.7, 1.85, 2.0, 2.15, 2.3, 2.45, 2.6, 2.8],
        (2, "Du"): [0.4, 0.5, 0.65, 0.8, 0.95],
    }
    jobs = [(sp, d, v) for (sp, d), vs in scans.items() for v in vs]
    t0 = time.time(); res = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            res.append(rec)
            print(rec, flush=True)
    windows = {}
    for (sp, d), vs in scans.items():
        sub = [r for r in res if r["species"] == "AB"[sp-1] and r["dial"] == d]
        vals = [r["val"] for r in sub]; oks = [r["ok"] for r in sub]
        locked = LOCK[f"{d}_{sp}"]
        ratio, lo, hi = window_ratio(vals, oks, locked)
        windows[f"{'AB'[sp-1]}_{d}"] = dict(ratio=ratio, lo=lo, hi=hi, locked=locked)
        print(f"{'AB'[sp-1]} {d}: ratio={ratio} [{lo},{hi}] locked={locked}", flush=True)
    json.dump(dict(scan=res, windows=windows),
              open("/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/cert_window.json","w"), indent=1)
    print("total %.0fs" % (time.time()-t0))
