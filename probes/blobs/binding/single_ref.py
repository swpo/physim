import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
from sim import run, make_stamped_world, homog_u0, min_image
from scipy import ndimage as ndi

p = json.loads(sys.argv[1])
dx = float(sys.argv[2])
T = float(sys.argv[3])
z = np.load("/tmp/stamp_P7.npz")
stamp = dict(du=z["du"], dv=z["dv"], dw=z["dw"])
if dx != 1.0:
    f = 1.0/dx
    stamp = {k: ndi.zoom(stamp[k], f, order=3) for k in stamp}
u0h = homog_u0(p.get("lam",2.0), p.get("k1",-0.7), p.get("k3",1.0), p.get("k4",1.5))
L = 64.0
u, v, w = make_stamped_world(L, dx, u0h, stamp, [(32.0, 32.0)])
cents = []
def cb(t, uu, vv, ww, blobs):
    if len(blobs) == 1:
        cents.append([t, blobs[0]["y"], blobs[0]["x"], blobs[0]["area_px"]])
r = run(L=L, dx=dx, T=T, u=u, v=v, w=w, rec_tu=10.0, callback=cb, **p)
c = np.array(cents)
# unwrap displacement
dy = np.array([min_image(c[i+1,1]-c[i,1], L) for i in range(len(c)-1)])
dxx = np.array([min_image(c[i+1,2]-c[i,2], L) for i in range(len(c)-1)])
path = float(np.hypot(dy, dxx).sum())
disp = float(np.hypot(dy.sum(), dxx.sum()))
# speed in last third
n3 = len(dy)//3
v_last = float(np.hypot(dy[-n3:].sum(), dxx[-n3:].sum()) / (c[-1,0]-c[-n3-1,0]))
print(json.dumps(dict(status=r["status"], n=len(c), disp=round(disp,3), path=round(path,3),
                      v_last=round(v_last,5), area_end=int(c[-1,3]))))
