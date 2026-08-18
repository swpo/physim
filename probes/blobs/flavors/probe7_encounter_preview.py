"""probe7_encounter_preview.py — P3 preview: pair interactions vs initial distance.

EQD pair world: A=(k1=-0.7,k4=1.0), B=(k1=-1.3,k4=1.8), both Du=1.
Cases: AA, AB, BB at d0 in (10, 14, 18, 24); T=1500; track centroids & separation.
Also: dt/2 invariance check on lone A and lone B (area/umax compare).
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import default_params, background, run, persistence_verdict
from scipy import ndimage
from concurrent.futures import ProcessPoolExecutor

def params():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -0.7, 1.0, 1.0
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.3, 1.8, 1.0
    return p

def sep_periodic(c1, c2, L=96):
    d = np.array(c1) - np.array(c2)
    d = (d + L/2) % L - L/2
    return float(np.hypot(*d))

def one(job):
    kind, d0 = job
    p = params()
    L = 96
    y = 48
    x1, x2 = 48 - d0/2, 48 + d0/2
    sp = dict(AA=(1, 1), AB=(1, 2), BB=(2, 2))[kind]
    spots = ((sp[0], y, x1, 2.0, 3.0), (sp[1], y, x2, 2.0, 3.0))
    r = run(p, arch="vvw", T=1500.0, spots=spots, rec_every_tu=25.0)
    rec = dict(kind=kind, d0=d0)
    if r["status"] != "ok":
        rec.update(status=r["status"]); return rec
    s = r["series"]
    # final separation: label blobs in the union of species masks
    F = r["F"]; thr = r["thr"]
    seps = []
    if kind == "AB":
        for t in range(len(s["t"])):
            c1, c2 = s["c1"][t], s["c2"][t]
            seps.append(None if c1[0] is None or c2[0] is None
                        else round(sep_periodic(c1, c2), 2))
    else:
        i = sp[0]
        m = F[i-1] > thr[i-1]
        lab, nc = ndimage.label(m)
        cs = ndimage.center_of_mass(m, lab, range(1, nc+1))
        seps = [round(sep_periodic(cs[0], cs[1]), 2)] if nc == 2 else [f"nc={nc}"]
    rec.update(status="ok",
               n1_end=s["n1"][-1], n2_end=s["n2"][-1],
               a1_end=s["a1"][-1], a2_end=s["a2"][-1],
               sep_series=seps[::4] if kind == "AB" else seps,
               sep_end=seps[-1] if seps else None)
    return rec

def dtcheck():
    out = []
    for sp in (1, 2):
        vals = {}
        for dtf in (1.0, 0.5):
            p = params()
            r = run(p, arch="vvw", T=300.0, spots=((sp, 48, 48, 2.0, 3.0),),
                    dt=0.01 * dtf)
            s = r["series"]
            vals[dtf] = (s[f"a{sp}"][-1], s[f"m{sp}"][-1])
        out.append(dict(species=sp, dt1=vals[1.0], dt05=vals[0.5]))
    return out

if __name__ == "__main__":
    print("dt check:", dtcheck(), flush=True)
    jobs = [(k, d) for k in ("AA", "AB", "BB") for d in (10, 14, 18, 24)]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            print(rec, flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe7_encounters.json"), "w"), indent=1)
