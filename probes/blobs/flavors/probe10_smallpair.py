"""probe10_smallpair.py — both species compact: dial pairs on isoline w/ Du<1.

Species: (d, Du) with k4=1.4+d, k1=-1.0+d*UB.
Candidates: A in {(0.3,0.65),(0.3,0.5),(0.15,0.65),(0.15,0.5),(0.0,0.65),(0.0,0.5)}
            B in {(0.6,0.65),(0.75,0.65),(0.6,0.5),(0.75,0.5),(0.45,0.5)}
Battery per pair: bg stability, lone A/B (T=300), AA/BB/AB at d0=10,16 (T=800).
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import default_params, background, bg_stability, run
from scipy import ndimage
from concurrent.futures import ProcessPoolExecutor

UB = -0.86756

def pair_params(dA, DuA, dB, DuB):
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0 + dA*UB, 1.4 + dA, DuA
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + dB*UB, 1.4 + dB, DuB
    return p

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
        ok = (n1 == 1 and n2 == 1 and m1.sum() <= 2.2*lone[0] and m2.sum() <= 2.2*lone[1])
        sep = None
        if n1 >= 1 and n2 >= 1:
            c1 = ndimage.center_of_mass(m1); c2 = ndimage.center_of_mass(m2)
            dd = np.array(c1) - np.array(c2); dd = (dd + 48) % 96 - 48
            sep = round(float(np.hypot(*dd)), 2)
        return dict(kind=kind, d0=d0, ok=bool(ok), n1=int(n1), n2=int(n2),
                    a1=int(m1.sum()), a2=int(m2.sum()), sep=sep)
    i = sp[0] - 1
    m = F[i] > thr[i]
    lab, nc = ndimage.label(m)
    a = int(m.sum()); sep = None
    if nc == 2:
        cs = ndimage.center_of_mass(m, lab, [1, 2])
        dd = np.array(cs[0]) - np.array(cs[1]); dd = (dd + 48) % 96 - 48
        sep = round(float(np.hypot(*dd)), 2)
    ok = (nc == 2 and a <= 2.2*2*lone[i]) or (nc == 1 and a <= 2.2*lone[i])
    return dict(kind=kind, d0=d0, ok=bool(ok), nc=int(nc), a=a, sep=sep,
                merged=bool(nc == 1))

def one(job):
    dA, DuA, dB, DuB = job
    p = pair_params(dA, DuA, dB, DuB)
    rec = dict(dA=dA, DuA=DuA, dB=dB, DuB=DuB)
    bg = background(p, arch="vvw")
    if bg is None:
        rec.update(verdict="no_bg"); return rec
    g, kw, _ = bg_stability(p, bg, arch="vvw")
    if g > 1e-6:
        rec.update(verdict="bg_unstable", g=round(float(g),3)); return rec
    lone = [None, None]; amps = [None, None]
    for i, sp in ((0, 1), (1, 2)):
        r = run(p, arch="vvw", T=300.0, spots=((sp, 48, 48, 2.0, 3.0),))
        s = r["series"]
        a = s[f"a{sp}"][-1]; n = s[f"n{sp}"][-1]
        if n != 1 or a < 8 or a > 600:
            rec.update(verdict=f"lone{sp}_fail", a=a, n=n); return rec
        lone[i] = a; amps[i] = s[f"m{sp}"][-1]
    rec["loneA"], rec["loneB"] = lone
    rec["ampA"], rec["ampB"] = amps
    cases = []; allok = True
    for kind in ("AA", "BB", "AB"):
        for d0 in (10, 16):
            c = enc(p, kind, d0, lone)
            cases.append(c); allok = allok and c["ok"]
    rec.update(verdict="PAIR_OK" if allok else "enc_fail", cases=cases)
    return rec

if __name__ == "__main__":
    A_CAND = [(0.3, 0.65), (0.3, 0.5), (0.15, 0.65), (0.15, 0.5), (0.0, 0.65), (0.0, 0.5)]
    B_CAND = [(0.6, 0.65), (0.75, 0.65), (0.6, 0.5), (0.75, 0.5), (0.45, 0.5)]
    jobs = [(dA, DuA, dB, DuB) for (dA, DuA) in A_CAND for (dB, DuB) in B_CAND
            if (dB - dA) >= 0.3 or (dB > dA and DuA - DuB >= 0.15)]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            cases = rec.get("cases", [])
            bad = [f"{c['kind']}{c['d0']}" for c in cases if not c["ok"]]
            print(f"A=({rec['dA']:.2f},{rec['DuA']:.2f}) B=({rec['dB']:.2f},{rec['DuB']:.2f}) -> "
                  f"{rec['verdict']:<12} lone={rec.get('loneA','-')}/{rec.get('loneB','-')} "
                  f"amp={rec.get('ampA','-')}/{rec.get('ampB','-')} "
                  f"bad={','.join(bad) if bad else '-'}", flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe10_smallpair.json"), "w"), indent=1)
