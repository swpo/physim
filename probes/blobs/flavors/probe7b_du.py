"""probe7b: encounter preview for DU pair A=(-1.0,1.4,Du=1.0), B=(-1.6507,2.15,Du=0.65)."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flavors_core import default_params, run
from scipy import ndimage
from concurrent.futures import ProcessPoolExecutor

def params():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, 1.0
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.6507, 2.15, 0.65
    return p

def sep_periodic(c1, c2, L=96):
    d = np.array(c1) - np.array(c2)
    d = (d + L/2) % L - L/2
    return float(np.hypot(*d))

def one(job):
    kind, d0 = job
    p = params()
    y = 48; x1, x2 = 48 - d0/2, 48 + d0/2
    sp = dict(AA=(1,1), AB=(1,2), BB=(2,2))[kind]
    spots = ((sp[0], y, x1, 2.0, 3.0), (sp[1], y, x2, 2.0, 3.0))
    r = run(p, arch="vvw", T=1500.0, spots=spots, rec_every_tu=25.0)
    rec = dict(kind=kind, d0=d0)
    if r["status"] != "ok":
        rec.update(status=r["status"]); return rec
    s = r["series"]; F = r["F"]; thr = r["thr"]
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
        if nc >= 2:
            cs = ndimage.center_of_mass(m, lab, range(1, nc+1))
            seps = [round(sep_periodic(cs[0], cs[1]), 2)]
        else:
            seps = [f"nc={nc}"]
    rec.update(status="ok", n1_end=s["n1"][-1], n2_end=s["n2"][-1],
               a1_end=s["a1"][-1], a2_end=s["a2"][-1],
               a1_max=max(s["a1"]), a2_max=max(s["a2"]),
               sep=seps[-1] if kind != "AB" else seps[::5])
    return rec

if __name__ == "__main__":
    jobs = [(k, d) for k in ("AA", "AB", "BB") for d in (8, 10, 14, 18, 24)]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec); print(rec, flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "probe7b_du.json"), "w"), indent=1)
