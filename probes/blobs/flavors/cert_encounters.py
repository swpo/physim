"""cert_encounters.py — B3 encounter table: AA/AB/BB x 3 seeds, close range.

Protocol (pre-registered):
  d0=10 px (well inside interaction range; lone blob radii ~4-7 px), T=2000 tu,
  sigma=2.5e-3 noise, seeds 0,1,2. Blob census via metrics.census every 100 tu.
  Outcome coding at t=2000:
    repel      : 2 blobs of the seeded species (same-kind) or 1 of each (AB),
                 final separation > d0, per-blob areas within 2.2x lone areas
    merge      : 1 blob where 2 were seeded (same species)
    annihilate : 0 blobs (or one species lost in AB)
    convert    : species census changed kind (e.g. A became B)
    deform     : blob count ok but area out of band (stripe-like)
  Conservation bookkeeping: species excess mass before/after.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, make_state, stepper, thresholds
import metrics
from concurrent.futures import ProcessPoolExecutor

UB = -0.86756
LONE = dict(A=169, B=25)   # clean lone areas (probe10/probe11)

def pair_params():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, 0.65
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + 0.75*UB, 2.15, 0.65
    return p

def outcome(kind, cen, d0):
    nA, nB = len(cen["A"]), len(cen["B"])
    aA = sum(b["area"] for b in cen["A"]); aB = sum(b["area"] for b in cen["B"])
    if kind == "AA":
        if nA == 0 and nB == 0: return "annihilate"
        if nB > 0: return "convert"
        if nA == 1: return "merge" if aA <= 2.2*LONE["A"] else "deform"
        if nA == 2:
            sep = metrics.sep_periodic((cen["A"][0]["cy"], cen["A"][0]["cx"]),
                                       (cen["A"][1]["cy"], cen["A"][1]["cx"]))
            band = aA <= 2.2*2*LONE["A"]
            if not band: return "deform"
            return "repel" if sep > d0 else "static"
        return "replicate"
    if kind == "BB":
        if nA == 0 and nB == 0: return "annihilate"
        if nA > 0: return "convert"
        if nB == 1: return "merge" if aB <= 2.2*LONE["B"] else "deform"
        if nB == 2:
            sep = metrics.sep_periodic((cen["B"][0]["cy"], cen["B"][0]["cx"]),
                                       (cen["B"][1]["cy"], cen["B"][1]["cx"]))
            band = aB <= 2.2*2*LONE["B"]
            if not band: return "deform"
            return "repel" if sep > d0 else "static"
        return "replicate"
    # AB
    if nA == 0 and nB == 0: return "annihilate"
    if nA == 0: return "A_annihilated"
    if nB == 0: return "B_annihilated"
    if nA == 1 and nB == 1:
        sep = metrics.sep_periodic((cen["A"][0]["cy"], cen["A"][0]["cx"]),
                                   (cen["B"][0]["cy"], cen["B"][0]["cx"]))
        band = (aA <= 2.2*LONE["A"]) and (aB <= 2.2*LONE["B"])
        if not band: return "deform"
        return "repel" if sep > d0 else "static"
    return "replicate"

def one(job):
    kind, seed, d0 = job
    p = pair_params()
    sp = dict(AA=(1,1), AB=(1,2), BB=(2,2))[kind]
    spots = ((sp[0], 48.0, 48.0-d0/2, 2.0, 3.0), (sp[1], 48.0, 48.0+d0/2, 2.0, 3.0))
    F, bg = make_state(p, L=96, arch="vvw", spots=spots)
    thr = thresholds(p, bg)
    step = stepper(p, arch="vvw")
    rng = np.random.default_rng(seed)
    dt = 0.01; T = 2000.0
    m0 = metrics.excess_mass(F, bg)
    rec = dict(kind=kind, seed=seed, d0=d0)
    hist = []
    for t in range(int(T/dt)+1):
        if t % int(100/dt) == 0:
            if not np.isfinite(F).all():
                rec.update(outcome="blowup"); return rec
            cen = metrics.census(F, thr)
            hist.append(dict(t=round(t*dt), nA=len(cen["A"]), nB=len(cen["B"])))
        if t < int(T/dt):
            F = step(F, dt, rng, 2.5e-3)
    cen = metrics.census(F, thr)
    m1 = metrics.excess_mass(F, bg)
    o = outcome(kind, cen, d0)
    seps = None
    allb = [("A", b) for b in cen["A"]] + [("B", b) for b in cen["B"]]
    if len(allb) == 2:
        seps = round(metrics.sep_periodic((allb[0][1]["cy"], allb[0][1]["cx"]),
                                          (allb[1][1]["cy"], allb[1][1]["cx"])), 2)
    rec.update(outcome=o, nA=len(cen["A"]), nB=len(cen["B"]),
               areas_A=[b["area"] for b in cen["A"]],
               areas_B=[b["area"] for b in cen["B"]],
               sep_end=seps,
               mass0=dict(A=round(m0["A"],1), B=round(m0["B"],1)),
               mass1=dict(A=round(m1["A"],1), B=round(m1["B"],1)),
               census_hist=hist[::4])
    return rec

if __name__ == "__main__":
    jobs = [(k, s, 10) for k in ("AA", "AB", "BB") for s in (0, 1, 2)]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=9) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            print({k: rec[k] for k in rec if k != "census_hist"}, flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open("/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/cert_encounters.json","w"), indent=1)
