
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import default_params, background, bg_stability, run
from scipy import ndimage
from concurrent.futures import ProcessPoolExecutor

UBs = {}
def one(job):
    k1, k4, d0 = job
    p = default_params()
    p["k1_1"] = p["k1_2"] = k1; p["k4_1"] = p["k4_2"] = k4
    r = run(p, arch="vvw", T=800.0, spots=((1, 48, 48-d0/2, 2.0, 3.0), (1, 48, 48+d0/2, 2.0, 3.0)),
            rec_every_tu=25.0)
    rec = dict(k1=k1, k4=k4, d0=d0)
    if r["status"] != "ok":
        rec.update(status=r["status"]); return rec
    s = r["series"]; F = r["F"]; thr = r["thr"]
    m = F[0] > thr[0]
    lab, nc = ndimage.label(m)
    rec.update(status="ok", n_end=int(nc), a_end=s["a1"][-1], a_max=max(s["a1"]))
    if nc == 2:
        cs = ndimage.center_of_mass(m, lab, [1, 2])
        d = np.array(cs[0]) - np.array(cs[1]); d = (d + 48) % 96 - 48
        rec["sep"] = round(float(np.hypot(*d)), 2)
    return rec

if __name__ == "__main__":
    pts = [(-1.0, 1.4), (-1.1, 1.6), (-1.2, 1.8), (-1.3, 2.0), (-1.35, 2.1), (-0.7, 1.0)]
    jobs = [(k1, k4, d0) for (k1, k4) in pts for d0 in (10, 16)]
    out = []
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec); print(rec, flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe8_samepair.json"), "w"), indent=1)
