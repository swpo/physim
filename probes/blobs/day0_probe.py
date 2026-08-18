
import numpy as np, time, json
from scipy import ndimage

def lap(X):
    return (np.roll(X,1,0)+np.roll(X,-1,0)+np.roll(X,1,1)+np.roll(X,-1,1)-4.0*X)

def run(L=96, T=600.0, Du=1.0, Dv=1.0, Dw=20.0,
        lam=2.0, k1=-0.6, k3=1.0, k4=2.0, tau=3.0, theta=0.5, seed=0):
    dt = min(0.2/max(Du,Dv,Dw), 0.02)   # diffusive stability with margin
    steps = int(T/dt)
    roots = np.roots([-1.0, 0.0, lam-k3-k4, k1])
    u0 = float(sorted(r.real for r in roots if abs(r.imag) < 1e-9)[0])
    u = np.full((L,L), u0); v = u.copy(); w = u.copy()
    x = np.arange(L); X, Y = np.meshgrid(x, x, indexing="ij")
    u = u + 2.0*np.exp(-((X-L/2)**2+(Y-L/2)**2)/(2*3.0**2))
    thr = u0 + 0.45*(np.sqrt(lam)-u0)
    areas = []
    rec_every = max(steps//60, 1)
    for t in range(steps):
        un = u + dt*(Du*lap(u) + lam*u - u**3 - k3*v - k4*w + k1)
        v  = v + dt*((u - v)/tau + Dv*lap(v))
        w  = w + dt*((u - w)/theta + Dw*lap(w))
        u = un
        if t % 500 == 0 and not np.isfinite(u).all():
            return dict(status="blowup", t=t)
        if t % rec_every == 0:
            areas.append(int((u > thr).sum()))
    lab, ncomp = ndimage.label(u > thr)
    a = np.array(areas); tail = a[-10:]
    ok = (ncomp == 1) and tail.min() >= 8 and tail.max() <= 600 and \
         (tail.max()-tail.min()) <= max(6, 0.3*tail.mean())
    return dict(status="ok", ncomp=int(ncomp), area_end=int(a[-1]),
                series=[int(x) for x in a[::6]], persistent=bool(ok),
                u0=round(u0,3), dt=round(dt,4))

t0 = time.time()
res = {}
for k1 in (-0.5, -0.7, -0.9):
    for k4 in (1.5, 2.5):
        for theta in (0.35, 0.7):
            key = f"k1{k1}_k4{k4}_th{theta}"
            r = run(k1=k1, k4=k4, theta=theta, Dw=20.0)
            res[key] = r
            print(key, "->", {k: r[k] for k in r if k != "series"}, flush=True)
print("total %.0fs" % (time.time()-t0))
json.dump(res, open("/tmp/blob_smoke2.json","w"))
