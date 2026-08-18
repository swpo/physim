"""cert_b1.py — B1 EXISTENCE certification for species A and B of pair MAXC.

Runs (per species):
  clean  1e4 tu (lifetime)                       seed n/a
  noisy  1e4 tu sigma=2.5e-3 (robust+non-repl)   seed 0   [sigma/amp ~ 1.2e-3 > 1e-3]
  noisy  2e3 tu sigma=2.5e-3 seeds 1,2 (seed robustness)
PASS if: alive at end, ncomp==1 at every record after t>=50 tu, area stable
(tail min>=8, max<=600), no blowup. Also reports wallclock (B7).
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, run
from concurrent.futures import ProcessPoolExecutor

UB = -0.86756
def pair_params():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, 0.65
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + 0.75*UB, 2.15, 0.65
    return p

def one(job):
    sp, T, noise, seed = job
    p = pair_params()
    t0 = time.time()
    r = run(p, arch="vvw", T=T, spots=((sp, 48, 48, 2.0, 3.0),),
            noise=noise, seed=seed, rec_every_tu=100.0)
    wall = time.time() - t0
    rec = dict(species="AB"[sp-1], T=T, noise=noise, seed=seed,
               wall_s=round(wall,1), tu_per_s=round(T/wall,1))
    if r["status"] != "ok":
        rec.update(passed=False, why=r["status"]); return rec
    s = r["series"]; i = sp
    a = np.array(s[f"a{i}"]); n = np.array(s[f"n{i}"])
    settle = 1  # skip t=0 record
    alive = a[-1] >= 8
    nonrepl = bool((n[settle:] == 1).all())
    bounded = bool(a[settle:].max() <= 600 and a[settle:].min() >= 8)
    tail = a[-max(len(a)//4,1):]
    stable = bool((tail.max()-tail.min()) <= max(6, 0.3*tail.mean()))
    rec.update(passed=bool(alive and nonrepl and bounded and stable),
               alive=bool(alive), nonreplicating=nonrepl, bounded=bounded,
               stable=stable, area_end=int(a[-1]), area_min=int(a[settle:].min()),
               area_max=int(a[settle:].max()), ncomp_max=int(n[settle:].max()),
               umax_end=s[f"m{i}"][-1],
               area_series_every1000tu=[int(x) for x in a[::10]])
    return rec

if __name__ == "__main__":
    jobs = []
    for sp in (1, 2):
        jobs.append((sp, 1e4, 0.0, 0))
        jobs.append((sp, 1e4, 2.5e-3, 0))
        jobs.append((sp, 2e3, 2.5e-3, 1))
        jobs.append((sp, 2e3, 2.5e-3, 2))
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec)
            print({k: rec[k] for k in rec if k != "area_series_every1000tu"}, flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open("/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/cert_b1.json","w"), indent=1)
