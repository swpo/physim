"""cert_window_refine.py — refine B window edges (and A k4 edge) on finer grid."""
import sys, os, json, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, background, bg_stability, run, persistence_verdict
from concurrent.futures import ProcessPoolExecutor

UB = -0.86756
LOCK = dict(k1_1=-1.0, k4_1=1.4, Du_1=0.65,
            k1_2=-1.0 + 0.75*UB, k4_2=2.15, Du_2=0.65)

def one(job):
    sp, dial, val = job
    p = default_params(); p.update(LOCK)
    p[f"{dial}_{sp}"] = val
    rec = dict(species="AB"[sp-1], dial=dial, val=round(val,4))
    bg = background(p, arch="vvw")
    if bg is None:
        rec.update(ok=False, why="no_bg"); return rec
    g, kw, _ = bg_stability(p, bg, arch="vvw")
    if g > 1e-6:
        rec.update(ok=False, why="bg_unstable"); return rec
    r = run(p, arch="vvw", T=300.0, spots=((sp, 48, 48, 2.0, 3.0),))
    if r["status"] != "ok":
        rec.update(ok=False, why=r["status"]); return rec
    v = persistence_verdict(r["series"], f"a{sp}", f"n{sp}")
    rec.update(ok=(v == "persistent"), why=v, a=r["series"][f"a{sp}"][-1])
    return rec

if __name__ == "__main__":
    jobs = []
    for v in (-1.88, -1.85, -1.82, -1.79, -1.42, -1.40, -1.38):
        jobs.append((2, "k1", v))
    for v in (1.90, 1.94, 1.97, 2.50, 2.55):
        jobs.append((2, "k4", v))
    for v in (1.05, 1.45, 1.5, 1.55):
        jobs.append((1, "k4", v))
    for v in (-1.28, -1.31, -0.92, -0.90):
        jobs.append((1, "k1", v))
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec); print(rec, flush=True)
    json.dump(out, open("/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/cert_window_refine.json","w"), indent=1)
    print("total %.0fs" % (time.time()-t0))
