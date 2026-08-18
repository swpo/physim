"""probe1_arch.py — P1: which architecture has a robust symmetric existence island?

For each arch in (w, vw, vvw): sweep symmetric (k1, k4) with lone u1 spot.
Prefilter: background must exist and be linearly stable (else record + skip sim).
Verdict per point: persistent / dead / split / domain / unsteady / bg_unstable.
Also for each point, check u2 stays quiet (no induced second-species structure).
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import (default_params, background, bg_stability, run,
                          persistence_verdict)
from concurrent.futures import ProcessPoolExecutor

K1S = [-0.5, -0.7, -0.9, -1.1, -1.3]
K4S = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
ARCHS = ["w", "vw", "vvw"]
T = 300.0

def one(job):
    arch, k1, k4 = job
    p = default_params()
    p["k1_1"] = p["k1_2"] = k1
    p["k4_1"] = p["k4_2"] = k4
    bg = background(p, arch=arch)
    rec = dict(arch=arch, k1=k1, k4=k4)
    if bg is None:
        rec.update(verdict="no_bg")
        return rec
    g, kw, g0 = bg_stability(p, bg, arch=arch)
    rec.update(bg_u=round(bg["u1"], 4), bg_growth=round(float(g), 4),
               bg_k=round(float(kw), 3))
    if g > 1e-6:
        rec.update(verdict="bg_unstable")
        return rec
    r = run(p, arch=arch, T=T, spots=((1, 48, 48, 2.0, 3.0),))
    if r["status"] != "ok":
        rec.update(verdict=r["status"])
        return rec
    v = persistence_verdict(r["series"], "a1", "n1")
    a2max = max(r["series"]["a2"])
    rec.update(verdict=v, a1_end=r["series"]["a1"][-1],
               umax1=r["series"]["m1"][-1], a2_max=a2max,
               a1_series=r["series"]["a1"][::3])
    return rec

if __name__ == "__main__":
    jobs = [(a, k1, k4) for a in ARCHS for k1 in K1S for k4 in K4S]
    t0 = time.time()
    out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            print(f"{rec['arch']:>3} k1={rec['k1']:+.1f} k4={rec['k4']:.1f} -> "
                  f"{rec['verdict']:<12} "
                  + (f"a1={rec.get('a1_end')} a2max={rec.get('a2_max')} "
                     f"um={rec.get('umax1')}" if 'a1_end' in rec else
                     f"g={rec.get('bg_growth')}"), flush=True)
    print("total %.0fs" % (time.time() - t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe1_arch.json"), "w"), indent=1)
