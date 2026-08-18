import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
import numpy as np
from sim import run, homog_u0

CANDS = {
  "M0":      dict(Dv=1.0, tau=3.0, k3=1.0, k4=1.5),
  "B_66":    dict(Dv=6.0, tau=6.0, k3=1.5, k4=1.0),
  "C_46":    dict(Dv=4.0, tau=6.0, k3=1.5, k4=1.0),
  "D_64":    dict(Dv=6.0, tau=4.0, k3=1.5, k4=1.0),
  "E_risky": dict(Dv=1.0, tau=3.0, k3=1.0, k4=2.0),
  "F_36":    dict(Dv=3.0, tau=6.0, k3=1.5, k4=1.0),
}
out = {}
for name, p in CANDS.items():
    t0 = time.time()
    r = run(L=96.0, dx=1.0, T=800.0, bumps=[(48.0, 48.0)], rec_tu=10.0, **p)
    el = time.time() - t0
    if r["status"] != "ok":
        out[name] = dict(status=r["status"], t=r.get("t_tu"))
        print(name, out[name], flush=True); continue
    ncomps = [len(f) for f in r["frames"]]
    areas = [f[0]["area_px"] if len(f) == 1 else sum(b["area_px"] for b in f) for f in r["frames"]]
    tail = areas[-20:]
    out[name] = dict(status="ok", ncomp_end=ncomps[-1], ncomp_max=max(ncomps),
                     area_end=areas[-1], area_min=min(tail), area_max=max(tail),
                     runtime_s=round(el,1), tu_per_s=round(800.0/el,1))
    print(name, out[name], flush=True)
json.dump(out, open("/tmp/bind_screen.json","w"), indent=1)
