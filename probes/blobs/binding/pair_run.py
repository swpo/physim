import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
from sim import pair_experiment

WPs = {
 "D_64": dict(Dv=6.0, tau=4.0, k3=1.5, k4=1.0),
 "C_46": dict(Dv=4.0, tau=6.0, k3=1.5, k4=1.0),
 "B_66": dict(Dv=6.0, tau=6.0, k3=1.5, k4=1.0),
 "M0":   dict(Dv=1.0, tau=3.0, k3=1.0, k4=1.5),
}
name = sys.argv[1]
d0 = float(sys.argv[2])
T = float(sys.argv[3]) if len(sys.argv) > 3 else 3000.0
z = np.load(f"/tmp/stamp_{name}.npz")
stamp = dict(du=z["du"], dv=z["dv"], dw=z["dw"])
t0 = time.time()
out = pair_experiment(stamp, d0, L=96.0, dx=1.0, T=T, rec_tu=10.0, **WPs[name])
seps = out["seps"]
# compress: keep every 5th + last
keep = seps[::5] + [seps[-1]]
json.dump(dict(name=name, d0=d0, status=out["status"],
               seps=[[round(t,1), (None if not np.isfinite(s) else round(s,3)), n] for t,s,n in keep],
               runtime=round(time.time()-t0,1)),
          open(f"/tmp/pair_{name}_d{d0}.json","w"))
s_end = seps[-1]
print(json.dumps(dict(name=name, d0=d0, t_end=round(s_end[0],1),
                      sep_end=(None if not np.isfinite(s_end[1]) else round(s_end[1],2)),
                      ncomp_end=s_end[2], runtime=round(time.time()-t0,1))))
