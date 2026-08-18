"""probe3_diff.py — P2: differentiate species in ONE world (arch vvw).

Fix A=(k1_1,k4_1), sweep B=(k1_2,k4_2) along/around the island diagonal.
For each B-dial: coupled background + stability, lone-A run, lone-B run, A+B run.
Report areas/amplitudes -> pick dials with max size contrast, all persistent.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import (default_params, background, bg_stability, run,
                          persistence_verdict)
from concurrent.futures import ProcessPoolExecutor

T = 250.0
ANCHORS = [(-1.0, 1.4), (-0.7, 1.0)]
B_K1 = [-1.4, -1.3, -1.2, -1.1, -1.0, -0.9, -0.8, -0.7]
B_K4 = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2]

def one(job):
    (ak1, ak4), bk1, bk4 = job
    p = default_params()
    p["k1_1"], p["k4_1"] = ak1, ak4
    p["k1_2"], p["k4_2"] = bk1, bk4
    rec = dict(ak1=ak1, ak4=ak4, bk1=bk1, bk4=bk4)
    bg = background(p, arch="vvw")
    if bg is None:
        rec.update(verdict="no_bg"); return rec
    g, kw, g0 = bg_stability(p, bg, arch="vvw")
    rec.update(bg_u1=round(bg["u1"],4), bg_u2=round(bg["u2"],4),
               bg_growth=round(float(g),4))
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
    rAB = run(p, arch="vvw", T=T, spots=((1, 48, 30, 2.0, 3.0), (2, 48, 66, 2.0, 3.0)))
    if rAB["status"] != "ok":
        rec.update(verdict="coex_blowup"); return rec
    vcA = persistence_verdict(rAB["series"], "a1", "n1")
    vcB = persistence_verdict(rAB["series"], "a2", "n2")
    rec.update(verdict=f"{vcA}|{vcB}",
               coex_aA=rAB["series"]["a1"][-1], coex_aB=rAB["series"]["a2"][-1])
    return rec

if __name__ == "__main__":
    jobs = [(a, bk1, bk4) for a in ANCHORS for bk1 in B_K1 for bk4 in B_K4]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            v = rec.get("verdict", "?")
            print(f"A=({rec['ak1']},{rec['ak4']}) B=({rec['bk1']},{rec['bk4']}) -> {v:<24}"
                  f" aA={rec.get('aA','-')} aB={rec.get('aB','-')}"
                  f" coex={rec.get('coex_aA','-')}/{rec.get('coex_aB','-')}", flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe3_diff.json"), "w"), indent=1)
