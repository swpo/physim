"""probe5_contrast.py — P2c: lock the species pair. 2D (delta, Du2) x Du1 mini-sweep.

Also records B lone amplitude/area AND coexistence values + a close-range sanity
(d=20) to prefer pairs that won't competitively exclude at moderate range.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import (default_params, background, bg_stability, run,
                          persistence_verdict)
from concurrent.futures import ProcessPoolExecutor

T = 250.0
UB = -0.86756

def one(job):
    delta, du2, du1 = job
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, du1
    p["k4_2"] = 1.4 + delta
    p["k1_2"] = -1.0 + delta * UB
    p["Du_2"] = du2
    rec = dict(delta=round(delta,3), du2=du2, du1=du1)
    bg = background(p, arch="vvw")
    if bg is None:
        rec.update(verdict="no_bg"); return rec
    g, kw, g0 = bg_stability(p, bg, arch="vvw")
    if g > 1e-6:
        rec.update(verdict="bg_unstable"); return rec
    rA = run(p, arch="vvw", T=T, spots=((1, 48, 48, 2.0, 3.0),))
    rB = run(p, arch="vvw", T=T, spots=((2, 48, 48, 2.0, 3.0),))
    if rA["status"] != "ok" or rB["status"] != "ok":
        rec.update(verdict="blowup"); return rec
    vA = persistence_verdict(rA["series"], "a1", "n1")
    vB = persistence_verdict(rB["series"], "a2", "n2")
    rec.update(vA=vA, aA=rA["series"]["a1"][-1], mA=rA["series"]["m1"][-1],
               vB=vB, aB=rB["series"]["a2"][-1], mB=rB["series"]["m2"][-1])
    if vA != "persistent" or vB != "persistent":
        rec.update(verdict="lone_fail"); return rec
    # coexistence far (d=36) and moderately close (d=20)
    res = {}
    for tag, d in (("far", 36), ("mid", 20)):
        rAB = run(p, arch="vvw", T=T,
                  spots=((1, 48, 48 - d//2, 2.0, 3.0), (2, 48, 48 + d - d//2, 2.0, 3.0)))
        if rAB["status"] != "ok":
            res[tag] = "blowup"; continue
        vcA = persistence_verdict(rAB["series"], "a1", "n1")
        vcB = persistence_verdict(rAB["series"], "a2", "n2")
        s = rAB["series"]
        res[tag] = f"{vcA}|{vcB}"
        rec[f"{tag}_aA"], rec[f"{tag}_aB"] = s["a1"][-1], s["a2"][-1]
    rec.update(far=res.get("far"), mid=res.get("mid"),
               verdict="pair_ok" if res.get("far") == "persistent|persistent" else "coex_fail")
    return rec

if __name__ == "__main__":
    jobs = []
    for delta in (0.3, 0.45, 0.6, 0.75):
        for du2 in (0.35, 0.45, 0.55, 0.65):
            for du1 in (1.0, 1.3):
                jobs.append((delta, du2, du1))
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            print(f"d={rec['delta']:+.2f} Du2={rec['du2']:.2f} Du1={rec['du1']:.1f} -> "
                  f"{rec.get('verdict','?'):<12} A:{rec.get('aA','-')}px/{rec.get('mA','-')} "
                  f"B:{rec.get('aB','-')}px/{rec.get('mB','-')} far={rec.get('far','-')} "
                  f"mid={rec.get('mid','-')}", flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe5_contrast.json"), "w"), indent=1)
