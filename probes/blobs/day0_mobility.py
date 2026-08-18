
import numpy as np, time, json
from scipy import ndimage

def lap(X):
    return (np.roll(X,1,0)+np.roll(X,-1,0)+np.roll(X,1,1)+np.roll(X,-1,1)-4.0*X)

def run(L=96, T=2000.0, noise=0.0, seed=0, k1=-0.7, k4=1.5, theta=0.7,
        Du=1.0, Dv=1.0, Dw=20.0, lam=2.0, k3=1.0, tau=3.0):
    dt = min(0.2/Dw, 0.02); steps = int(T/dt)
    rng = np.random.default_rng(seed)
    roots = np.roots([-1.0, 0.0, lam-k3-k4, k1])
    u0 = float(sorted(r.real for r in roots if abs(r.imag) < 1e-9)[0])
    u = np.full((L,L), u0); v = u.copy(); w = u.copy()
    x = np.arange(L); X, Y = np.meshgrid(x, x, indexing="ij")
    u = u + 2.0*np.exp(-((X-L/2)**2+(Y-L/2)**2)/18.0)
    thr = u0 + 0.45*(np.sqrt(lam)-u0)
    sq = np.sqrt(dt)
    cents = []; areas = []
    rec = max(steps//100, 1)
    for t in range(steps):
        un = u + dt*(Du*lap(u) + lam*u - u**3 - k3*v - k4*w + k1)
        if noise > 0: un += noise*sq*rng.standard_normal((L,L))
        v = v + dt*((u - v)/tau + Dv*lap(v))
        w = w + dt*((u - w)/theta + Dw*lap(w))
        u = un
        if t % rec == 0:
            m = u > thr
            a = int(m.sum())
            if a == 0: return dict(status="died", t_tu=round(t*dt,1))
            cy, cx = ndimage.center_of_mass(m)
            cents.append((float(cy), float(cx))); areas.append(a)
    lab, nc = ndimage.label(u > thr)
    c = np.array(cents)
    # displacement over second half
    h = len(c)//2
    disp = float(np.hypot(*(c[-1]-c[h])))
    path = float(np.sum(np.hypot(*np.diff(c[h:],axis=0).T)))
    return dict(status="ok", ncomp=int(nc), area_med=int(np.median(areas)),
                disp_2ndhalf=round(disp,2), path_2ndhalf=round(path,2),
                area_min=int(min(areas)), area_max=int(max(areas)))

t0=time.time()
for noise in (0.0, 5e-4, 2e-3):
    for seed in (0,1):
        r = run(noise=noise, seed=seed)
        print(f"noise={noise} s{seed}:", r, flush=True)
print("%.0fs" % (time.time()-t0))
