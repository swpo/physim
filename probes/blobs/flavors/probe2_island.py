"""probe2_island.py — P1b: finer symmetric islands for arch w and vvw + 2-spot coexistence."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import (default_params, background, bg_stability, run,
                          persistence_verdict)
from concurrent.futures import ProcessPoolExecutor

T = 300.0

def one(job):
    arch, k1, k4 = job
    p = default_params()
    p["k1_1"] = p["k1_2"] = k1
    p["k4_1"] = p["k4_2"] = k4
    bg = background(p, arch=arch)
    rec = dict(arch=arch, k1=round(k1,3), k4=round(k4,3))
    if bg is None:
        rec.update(verdict="no_bg"); return rec
    g, kw, g0 = bg_stability(p, bg, arch=arch)
    rec.update(bg_u=round(bg["u1"],4), bg_growth=round(float(g),4))
    if g > 1e-6:
        rec.update(verdict="bg_unstable"); return rec
    # lone spot
    r = run(p, arch=arch, T=T, spots=((1, 48, 48, 2.0, 3.0),))
    if r["status"] != "ok":
        rec.update(verdict=r["status"]); return rec
    v1 = persistence_verdict(r["series"], "a1", "n1")
    rec.update(verdict=v1, a1_end=r["series"]["a1"][-1], umax1=r["series"]["m1"][-1])
    if v1 != "persistent":
        return rec
    # 2-spot both-species coexistence (same dials, one spot each, d=32)
    r2 = run(p, arch=arch, T=T, spots=((1, 48, 32, 2.0, 3.0), (2, 48, 64, 2.0, 3.0)))
    if r2["status"] != "ok":
        rec.update(coex="blowup"); return rec
    va = persistence_verdict(r2["series"], "a1", "n1")
    vb = persistence_verdict(r2["series"], "a2", "n2")
    rec.update(coex=f"{va}|{vb}", coex_a1=r2["series"]["a1"][-1],
               coex_a2=r2["series"]["a2"][-1])
    return rec

if __name__ == "__main__":
    jobs = []
    for k1 in np.arange(-1.5, -0.55, 0.1):
        for k4 in np.arange(0.8, 2.61, 0.2):
            jobs.append(("vvw", float(k1), float(k4)))
    for k1 in np.arange(-1.5, -0.75, 0.1):
        for k4 in np.arange(1.0, 2.21, 0.15):
            jobs.append(("w", float(k1), float(k4)))
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            print(f"{rec['arch']:>3} k1={rec['k1']:+.2f} k4={rec['k4']:.2f} -> "
                  f"{rec['verdict']:<12} coex={rec.get('coex','-')}", flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe2_island.json"), "w"), indent=1)
