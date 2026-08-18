"""probe9_jointpair.py — joint pair selection on the iso-background line ub=-0.86756.

Species i: k4_i = 1.4 + d_i, k1_i = -1.0 + d_i*UB.
Phase 1 (symmetric AA robustness): d in {0,0.15,0.3,0.45}, AA at d0=10,16 (T=800).
Phase 2 (joint pair): A(dA) x B(dB, DuB) grid, tests AA/BB/AB at d0=10 and 16.
This file runs phase 1 + phase 2 in one go with a compact pass/fail per case.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import default_params, background, bg_stability, run
from scipy import ndimage
from concurrent.futures import ProcessPoolExecutor

UB = -0.86756

def dials(d):
    return (-1.0 + d * UB, 1.4 + d)

def pair_params(dA, dB, DuA=1.0, DuB=1.0):
    p = default_params()
    p["k1_1"], p["k4_1"] = dials(dA); p["Du_1"] = DuA
    p["k1_2"], p["k4_2"] = dials(dB); p["Du_2"] = DuB
    return p

def spotcheck(F, thr, i, lone_area):
    """Is species i field two clean spots? Return (nc, area, sep or None, ok)."""
    m = F[i] > thr[i]
    lab, nc = ndimage.label(m)
    a = int(m.sum())
    sep = None
    if nc == 2:
        cs = ndimage.center_of_mass(m, lab, [1, 2])
        dd = np.array(cs[0]) - np.array(cs[1]); dd = (dd + 48) % 96 - 48
        sep = round(float(np.hypot(*dd)), 2)
    ok = (nc == 2) and a <= 3.0 * max(lone_area, 1)
    return nc, a, sep, ok

def enc(p, kind, d0, lone):
    sp = dict(AA=(1,1), AB=(1,2), BB=(2,2))[kind]
    spots = ((sp[0], 48, 48-d0/2, 2.0, 3.0), (sp[1], 48, 48+d0/2, 2.0, 3.0))
    r = run(p, arch="vvw", T=800.0, spots=spots, rec_every_tu=50.0)
    if r["status"] != "ok":
        return dict(kind=kind, d0=d0, ok=False, why=r["status"])
    F, thr = r["F"], r["thr"]
    if kind == "AB":
        m1 = F[0] > thr[0]; m2 = F[1] > thr[1]
        l1, n1 = ndimage.label(m1); l2, n2 = ndimage.label(m2)
        ok = (n1 == 1 and n2 == 1 and m1.sum() <= 3*lone[0] and m2.sum() <= 3*lone[1])
        sep = None
        if n1 == 1 and n2 == 1:
            c1 = ndimage.center_of_mass(m1); c2 = ndimage.center_of_mass(m2)
            dd = np.array(c1) - np.array(c2); dd = (dd + 48) % 96 - 48
            sep = round(float(np.hypot(*dd)), 2)
        return dict(kind=kind, d0=d0, ok=bool(ok), n1=int(n1), n2=int(n2),
                    a1=int(m1.sum()), a2=int(m2.sum()), sep=sep)
    else:
        i = sp[0] - 1
        nc, a, sep, ok = spotcheck(F, thr, i, lone[i])
        return dict(kind=kind, d0=d0, ok=bool(ok), nc=int(nc), a=a, sep=sep)

def one(job):
    dA, dB, DuB = job
    p = pair_params(dA, dB, 1.0, DuB)
    rec = dict(dA=dA, dB=dB, DuB=DuB,
               k4A=round(p["k4_1"],3), k4B=round(p["k4_2"],3))
    bg = background(p, arch="vvw")
    if bg is None:
        rec.update(verdict="no_bg"); return rec
    g, kw, _ = bg_stability(p, bg, arch="vvw")
    if g > 1e-6:
        rec.update(verdict="bg_unstable", g=round(float(g),3)); return rec
    # lone runs
    lone = [None, None]
    for i, sp in ((0, 1), (1, 2)):
        r = run(p, arch="vvw", T=300.0, spots=((sp, 48, 48, 2.0, 3.0),))
        s = r["series"]
        a = s[f"a{sp}"][-1]; n = s[f"n{sp}"][-1]
        if n != 1 or a < 8 or a > 600:
            rec.update(verdict=f"lone{sp}_fail", a=a, n=n); return rec
        lone[i] = a
    rec["loneA"], rec["loneB"] = lone
    cases = []
    allok = True
    for kind in ("AA", "BB", "AB"):
        for d0 in (10, 16):
            c = enc(p, kind, d0, lone)
            cases.append(c); allok = allok and c["ok"]
    rec.update(verdict="PAIR_OK" if allok else "enc_fail", cases=cases)
    return rec

if __name__ == "__main__":
    jobs = []
    for dA in (0.0, 0.15, 0.3):
        for dB in (0.3, 0.45, 0.6, 0.75):
            if dB - dA < 0.25: continue
            for DuB in (0.65, 1.0):
                jobs.append((dA, dB, DuB))
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            cases = rec.get("cases", [])
            bad = [f"{c['kind']}{c['d0']}" for c in cases if not c["ok"]]
            print(f"dA={rec['dA']:.2f} dB={rec['dB']:.2f} DuB={rec['DuB']:.2f} -> "
                  f"{rec['verdict']:<12} lone={rec.get('loneA','-')}/{rec.get('loneB','-')} "
                  f"bad={','.join(bad) if bad else 'none'}", flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe9_jointpair.json"), "w"), indent=1)
