import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
import numpy as np
from sim import run, radial_profile

CANDS = {
  "M0":   dict(Dv=1.0, tau=3.0, k3=1.0, k4=1.5),
  "B_66": dict(Dv=6.0, tau=6.0, k3=1.5, k4=1.0),
  "C_46": dict(Dv=4.0, tau=6.0, k3=1.5, k4=1.0),
  "D_64": dict(Dv=6.0, tau=4.0, k3=1.5, k4=1.0),
}
out = {}
for name, pcand in CANDS.items():
    t0 = time.time()
    r = run(L=96.0, dx=1.0, T=1500.0, bumps=[(48.0, 48.0)], rec_tu=25.0, **pcand)
    if r["status"] != "ok" or len(r["frames"][-1]) != 1:
        out[name] = dict(status="bad"); continue
    b = r["frames"][-1][0]
    rmid, pu = radial_profile(r["u"], r["u0"], b["y"], b["x"], 1.0, 96.0, rmax=45.0, nbins=90)
    # centroid drift over last half
    cs = [(f[0]["y"], f[0]["x"]) for f in r["frames"] if len(f)==1]
    c = np.array(cs); h = len(c)//2
    drift = float(np.hypot(*(c[-1]-c[h])))
    # zero crossings of tail beyond blob edge
    edge = np.sqrt(b["area"]/np.pi)
    zc = []
    for i in range(len(rmid)-1):
        if rmid[i] > edge and np.isfinite(pu[i]) and np.isfinite(pu[i+1]) and pu[i]*pu[i+1] < 0:
            zc.append(float(rmid[i]))
    out[name] = dict(status="ok", area=b["area_px"], peak=round(b["peak"],3),
                     radius=round(edge,2), drift2nd=round(drift,4),
                     zero_crossings=[round(z,1) for z in zc],
                     r=[round(float(x),2) for x in rmid],
                     prof_u=[None if not np.isfinite(x) else float(x) for x in pu],
                     runtime_s=round(time.time()-t0,1))
    print(name, {k:out[name][k] for k in ("area","peak","radius","drift2nd","zero_crossings","runtime_s")}, flush=True)
json.dump(out, open("/tmp/bind_profiles.json","w"))
