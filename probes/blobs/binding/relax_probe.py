import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
from sim import run, make_stamped_world, homog_u0

p = json.loads(sys.argv[1])
z = np.load(sys.argv[2])
u0h = homog_u0(p.get("lam",2.0), p.get("k1",-0.7), p.get("k3",1.0), p.get("k4",1.5))
L, dx = 64.0, 1.0
stamp = dict(du=z["du"], dv=z["dv"], dw=z["dw"])
u, v, w = make_stamped_world(L, dx, u0h, stamp, [(32.0, 32.0)])
u += 0.05 * (u - u0h)          # 5% amplitude kick on u only
peaks = []
def cb(t, uu, vv, ww, blobs):
    peaks.append([t, float(uu.max())])
r = run(L=L, dx=dx, T=150.0, u=u, v=v, w=w, rec_tu=1.0, callback=cb, **p)
pk = np.array(peaks)
fin = pk[-20:,1].mean()
dev = np.abs(pk[:,1] - fin)
m = (pk[:,0] > 2) & (dev > 1e-8)
z2 = np.polyfit(pk[m][:60,0], np.log(dev[m][:60]), 1)
print(json.dumps(dict(rate=float(z2[0]), tau_relax=float(-1/z2[0]),
                      dev0=float(dev[0]), fin=fin)))
