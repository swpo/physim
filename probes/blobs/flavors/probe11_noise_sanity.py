"""probe11_noise_sanity.py — 2000tu noisy sanity for candidate pairs (sigma=2e-3, seeds 0,1)."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import default_params, run, persistence_verdict
from concurrent.futures import ProcessPoolExecutor

UB = -0.86756
PAIRS = {
 "MAXC": ((0.00, 0.65), (0.75, 0.65)),
 "FALL": ((0.30, 0.50), (0.75, 0.65)),
}

def pair_params(pair):
    (dA, DuA), (dB, DuB) = PAIRS[pair]
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0 + dA*UB, 1.4 + dA, DuA
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + dB*UB, 1.4 + dB, DuB
    return p

def one(job):
    pair, sp, seed = job
    p = pair_params(pair)
    r = run(p, arch="vvw", T=2000.0, spots=((sp, 48, 48, 2.0, 3.0),),
            noise=2e-3, seed=seed, rec_every_tu=50.0)
    rec = dict(pair=pair, sp=sp, seed=seed)
    if r["status"] != "ok":
        rec.update(v=r["status"]); return rec
    s = r["series"]
    v = persistence_verdict(s, f"a{sp}", f"n{sp}")
    nmax = max(s[f"n{sp}"])
    rec.update(v=v, a_end=s[f"a{sp}"][-1], n_max=nmax, m_end=s[f"m{sp}"][-1])
    return rec

if __name__ == "__main__":
    jobs = [(pair, sp, seed) for pair in PAIRS for sp in (1, 2) for seed in (0, 1)]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec); print(rec, flush=True)
    print("total %.0fs" % (time.time()-t0))
