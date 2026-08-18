import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
from sim import relax_single, pair_experiment

# candidate points (name -> params); all inherit lam=2,k1=-0.7,theta=0.7,Du=1,Dw=20
PTS = json.loads(sys.argv[1])
name = sys.argv[2]
p = PTS[name]
t0 = time.time()
res = relax_single(L=64.0, dx=1.0, T=1200.0, **p)
if res["status"] != "ok":
    print(json.dumps(dict(name=name, verdict="single_fail", detail=res["status"])))
    sys.exit()
stamp = dict(du=res["du"], dv=res["dv"], dw=res["dw"])
area = res["area_px"]; radius = float(np.sqrt(area/np.pi))
verdicts = {}
for d0 in (round(2.4*radius,1), round(3.2*radius,1)):
    out = pair_experiment(stamp, d0, L=96.0, dx=1.0, T=800.0, rec_tu=20.0, **p)
    ns = [n for t,s,n in out["seps"]]
    ss = [s for t,s,n in out["seps"] if n==2]
    verdict = "pair_ok" if max(ns)==2 and min(ns)==2 else ("merge" if min(ns)<2 else "replicate")
    verdicts[d0] = dict(verdict=verdict, ncomp_max=max(ns), ncomp_min=min(ns),
                        sep_start=round(ss[0],2) if ss else None,
                        sep_end=round(ss[-1],2) if ss else None)
print(json.dumps(dict(name=name, area=area, radius=round(radius,2),
                      t_relax=res["t_relax"], pairs=verdicts,
                      runtime=round(time.time()-t0,1))))
