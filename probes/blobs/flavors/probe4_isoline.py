"""probe4_isoline.py — P2b: differentiate B along iso-background line + Du_2 dial.

A anchor = (k1_1,k4_1)=(-1.0,1.4), ub=-0.86756.
B dials: k4_2 = 1.4+delta, k1_2 = -1.0 + delta*ub  (keeps bg symmetric & stable),
         Du_2 in {0.6, 1.0, 1.5}.
Checks: lone-A, lone-B, then A+B at d=32. Records size + amplitude of each.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import (default_params, background, bg_stability, run,
                          persistence_verdict)
from concurrent.futures import ProcessPoolExecutor

T = 250.0
UB = -0.86756
DELTAS = [-0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
DUS = [0.6, 1.0, 1.5]

def one(job):
    delta, du2 = job
    p = default_params()
    p["k1_1"], p["k4_1"] = -1.0, 1.4
    p["k4_2"] = 1.4 + delta
    p["k1_2"] = -1.0 + delta * UB
    p["Du_2"] = du2
    rec = dict(delta=round(delta,3), du2=du2,
               k1_2=round(p["k1_2"],4), k4_2=round(p["k4_2"],3))
    bg = background(p, arch="vvw")
    if bg is None:
        rec.update(verdict="no_bg"); return rec
    g, kw, g0 = bg_stability(p, bg, arch="vvw")
    rec.update(bg_growth=round(float(g),4))
    if g > 1e-6:
        rec.update(verdict="bg_unstable"); return rec
    rB = run(p, arch="vvw", T=T, spots=((2, 48, 48, 2.0, 3.0),))
    if rB["status"] != "ok":
        rec.update(verdict="blowup"); return rec
    vB = persistence_verdict(rB["series"], "a2", "n2")
    rec.update(vB=vB, aB=rB["series"]["a2"][-1], mB=rB["series"]["m2"][-1])
    if vB != "persistent":
        rec.update(verdict="B_"+vB); return rec
    rAB = run(p, arch="vvw", T=T, spots=((1, 48, 30, 2.0, 3.0), (2, 48, 66, 2.0, 3.0)))
    if rAB["status"] != "ok":
        rec.update(verdict="coex_blowup"); return rec
    vcA = persistence_verdict(rAB["series"], "a1", "n1")
    vcB = persistence_verdict(rAB["series"], "a2", "n2")
    s = rAB["series"]
    rec.update(verdict=f"{vcA}|{vcB}", coex_aA=s["a1"][-1], coex_aB=s["a2"][-1],
               coex_mA=s["m1"][-1], coex_mB=s["m2"][-1])
    return rec

if __name__ == "__main__":
    jobs = [(d, du) for d in DELTAS for du in DUS]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            print(f"delta={rec['delta']:+.2f} Du2={rec['du2']:.1f} -> "
                  f"{rec.get('verdict','?'):<26} aB={rec.get('aB','-')} mB={rec.get('mB','-')} "
                  f"coex a={rec.get('coex_aA','-')}/{rec.get('coex_aB','-')} "
                  f"m={rec.get('coex_mA','-')}/{rec.get('coex_mB','-')}", flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe4_isoline.json"), "w"), indent=1)
