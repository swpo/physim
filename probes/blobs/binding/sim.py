"""Shared simulation + tracking utilities for the blob-binding probe (M2).

Conventions inherited from day0_probe.py / day0_mobility.py:
  explicit Euler, 5-point periodic Laplacian, dt = min(0.2/Dw, 0.02)*dx^2,
  homogeneous root u0 of -u^3 + (lam-k3-k4) u + k1 = 0 as background,
  blobs seeded as Gaussian u-bumps amp=2.0, sigma^2*2=18 (px^2),
  threshold thr = u0 + 0.45*(sqrt(lam)-u0) for masks.
"""
import numpy as np
from scipy import ndimage

def homog_u0(lam, k1, k3, k4):
    roots = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    return float(real[0])

def make_world(L, dx, u0, bumps, amp=2.0, sig2=18.0):
    """bumps: list of (y,x) in physical units. Periodic-aware Gaussians."""
    n = int(round(L / dx))
    u = np.full((n, n), u0, dtype=np.float64)
    v = u.copy(); w = u.copy()   # inhibitors start FLAT (day0 convention)
    x = np.arange(n) * dx
    Y, X = np.meshgrid(x, x, indexing="ij")
    for (by, bx) in bumps:
        dY = np.abs(Y - by); dY = np.minimum(dY, L - dY)
        dX = np.abs(X - bx); dX = np.minimum(dX, L - dX)
        u += amp * np.exp(-(dY**2 + dX**2) / sig2)
    return u, v, w

def _find(parent, a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a

def periodic_label(mask):
    """scipy label + union across periodic boundaries."""
    lab, n = ndimage.label(mask)
    if n <= 1:
        return lab, n
    parent = list(range(n + 1))
    def union(a, b):
        ra, rb = _find(parent, a), _find(parent, b)
        if ra != rb: parent[rb] = ra
    for a, b in zip(lab[0, :], lab[-1, :]):
        if a > 0 and b > 0: union(int(a), int(b))
    for a, b in zip(lab[:, 0], lab[:, -1]):
        if a > 0 and b > 0: union(int(a), int(b))
    remap = {}
    k = 0
    out = np.zeros_like(lab)
    for i in range(1, n + 1):
        r = _find(parent, i)
        if r not in remap:
            k += 1; remap[r] = k
    lut = np.zeros(n + 1, dtype=lab.dtype)
    for i in range(1, n + 1):
        lut[i] = remap[_find(parent, i)]
    out = lut[lab]
    return out, k

def periodic_centroid(weights, idx, n, dx):
    """Circular-mean centroid of pixels idx=(ys,xs) with weights, box n px."""
    w = weights
    tot = w.sum()
    out = []
    for coord in idx:
        th = 2 * np.pi * coord / n
        C = (w * np.cos(th)).sum() / tot
        S = (w * np.sin(th)).sum() / tot
        phi = np.arctan2(S, C) % (2 * np.pi)
        out.append(phi / (2 * np.pi) * n * dx)
    return out  # physical units

def blob_stats(u, u0, thr, dx, L):
    """Returns list of blobs: dict(y,x,area_px,area_phys,peak). Periodic aware."""
    mask = u > thr
    lab, n = periodic_label(mask)
    blobs = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        w = np.clip(u[ys, xs] - thr, 0, None) + 1e-12
        cy, cx = periodic_centroid(w, (ys, xs), lab.shape[0], dx)
        blobs.append(dict(y=cy, x=cx, area_px=int(len(ys)),
                          area=len(ys) * dx * dx,
                          peak=float(u[ys, xs].max())))
    return blobs

def min_image(d, L):
    return (d + L / 2) % L - L / 2

def pair_sep(b1, b2, L):
    dy = min_image(b1["y"] - b2["y"], L)
    dxx = min_image(b1["x"] - b2["x"], L)
    return float(np.hypot(dy, dxx)), (dy, dxx)

def run(L=96.0, dx=1.0, T=2000.0, bumps=None, noise=0.0, seed=0,
        lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=3.0, theta=0.7,
        Du=1.0, Dv=1.0, Dw=20.0, rec_tu=10.0, callback=None,
        u=None, v=None, w=None, stop_fn=None, amp=2.0, sig2=18.0):
    """Generic driver. Records blob_stats every rec_tu.
    stop_fn(t_tu, blobs) -> truthy to stop early (returned as 'stop').
    Returns dict with times, blobs-per-frame, final fields."""
    dmax = max(Du, Dv, Dw)
    dt = min(0.2 * dx * dx / dmax, 0.02)
    n = int(round(L / dx))
    steps = int(round(T / dt))
    u0 = homog_u0(lam, k1, k3, k4)
    thr = u0 + 0.45 * (np.sqrt(lam) - u0)
    if u is None:
        u, v, w = make_world(L, dx, u0, bumps or [], amp=amp, sig2=sig2)
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    idx2 = dx * dx
    rec_every = max(int(round(rec_tu / dt)), 1)
    times, frames = [], []
    stop = None
    for t in range(steps + 1):
        if t % rec_every == 0:
            if not np.isfinite(u).all():
                return dict(status="blowup", t_tu=t * dt, times=times, frames=frames)
            blobs = blob_stats(u, u0, thr, dx, L)
            times.append(t * dt); frames.append(blobs)
            if callback is not None:
                callback(t * dt, u, v, w, blobs)
            if stop_fn is not None:
                s = stop_fn(t * dt, blobs)
                if s:
                    stop = s
                    break
        lap_u = (np.roll(u,1,0)+np.roll(u,-1,0)+np.roll(u,1,1)+np.roll(u,-1,1)-4.0*u)/idx2
        lap_v = (np.roll(v,1,0)+np.roll(v,-1,0)+np.roll(v,1,1)+np.roll(v,-1,1)-4.0*v)/idx2
        lap_w = (np.roll(w,1,0)+np.roll(w,-1,0)+np.roll(w,1,1)+np.roll(w,-1,1)-4.0*w)/idx2
        un = u + dt*(Du*lap_u + lam*u - u**3 - k3*v - k4*w + k1)
        if noise > 0:
            un += noise * sq * rng.standard_normal((n, n))
        v = v + dt*((u - v)/tau + Dv*lap_v)
        w = w + dt*((u - w)/theta + Dw*lap_w)
        u = un
    return dict(status="ok", stop=stop, times=times, frames=frames,
                u=u, v=v, w=w, u0=u0, thr=thr, dt=dt)

def radial_profile(u, u0, cy, cx, dx, L, rmax=40.0, nbins=160):
    """Angle-averaged u(r)-u0 about (cy,cx), periodic min-image radii."""
    n = u.shape[0]
    x = np.arange(n) * dx
    Y, X = np.meshgrid(x, x, indexing="ij")
    dY = np.abs(Y - cy); dY = np.minimum(dY, L - dY)
    dX = np.abs(X - cx); dX = np.minimum(dX, L - dX)
    r = np.hypot(dY, dX).ravel()
    val = (u - u0).ravel()
    bins = np.linspace(0, rmax, nbins + 1)
    which = np.digitize(r, bins) - 1
    prof = np.full(nbins, np.nan)
    for i in range(nbins):
        m = which == i
        if m.any():
            prof[i] = val[m].mean()
    rmid = 0.5 * (bins[1:] + bins[:-1])
    return rmid, prof


# ---------------- stamp-based pair/multi-blob experiments ----------------

def relax_single(L=64.0, dx=1.0, T=1500.0, center=None, **params):
    """Relax a single seeded blob; return centered deviation stamps + stats."""
    if center is None:
        center = (L/2, L/2)
    r = run(L=L, dx=dx, T=T, bumps=[center], rec_tu=10.0, **params)
    if r["status"] != "ok":
        return dict(status=r["status"])
    frames = r["frames"]
    if len(frames[-1]) != 1:
        return dict(status="not_single", ncomp=len(frames[-1]))
    n = r["u"].shape[0]
    b = frames[-1][0]
    cy, cx = int(round(b["y"]/dx)) % n, int(round(b["x"]/dx)) % n
    u0 = r["u0"]
    # center stamps at (n//2, n//2)
    sy, sx = n//2 - cy, n//2 - cx
    du = np.roll(np.roll(r["u"] - u0, sy, 0), sx, 1)
    dv = np.roll(np.roll(r["v"] - u0, sy, 0), sx, 1)
    dw = np.roll(np.roll(r["w"] - u0, sy, 0), sx, 1)
    # relaxation time: area within 5% of final, sustained
    areas = np.array([f[0]["area_px"] if len(f)==1 else -1 for f in frames], float)
    times = np.array(r["times"])
    fin = areas[-5:].mean()
    ok = np.abs(areas - fin) <= max(0.05*fin, 1.0)
    t_relax = None
    for i in range(len(ok)):
        if ok[i:].all():
            t_relax = float(times[i]); break
    return dict(status="ok", du=du, dv=dv, dw=dw, u0=u0, thr=r["thr"], n=n, dx=dx,
                area_px=b["area_px"], peak=b["peak"], t_relax=t_relax,
                areas=[float(a) for a in areas[::5]])

def make_stamped_world(L, dx, u0, stamp, positions):
    """positions: list of (y,x) physical, rounded to grid. stamp: dict du,dv,dw (ns x ns)."""
    n = int(round(L/dx))
    ns = stamp["du"].shape[0]
    u = np.full((n, n), u0); v = u.copy(); w = u.copy()
    cy = ns//2
    for (py, px) in positions:
        iy, ix = int(round(py/dx)) % n, int(round(px/dx)) % n
        # paste stamp with periodic wrap: target indices
        ys = (np.arange(ns) - cy + iy) % n
        xs = (np.arange(ns) - cy + ix) % n
        u[np.ix_(ys, xs)] += stamp["du"]
        v[np.ix_(ys, xs)] += stamp["dv"]
        w[np.ix_(ys, xs)] += stamp["dw"]
    return u, v, w

def pair_experiment(stamp, d0, L=96.0, dx=1.0, T=3000.0, noise=0.0, seed=0,
                    rec_tu=10.0, keep_fields=False, **params):
    """Two stamped blobs on the x-axis at separation d0. Track separation."""
    u0h = homog_u0(params.get("lam",2.0), params.get("k1",-0.7),
                   params.get("k3",1.0), params.get("k4",1.5))
    yc = L/2
    x1 = L/2 - d0/2; x2 = L/2 + d0/2
    u, v, w = make_stamped_world(L, dx, u0h, stamp, [(yc, x1), (yc, x2)])
    seps = []
    def cb(t, uu, vv, ww, blobs):
        if len(blobs) == 2:
            s, _ = pair_sep(blobs[0], blobs[1], L)
            seps.append((t, s, 2))
        else:
            seps.append((t, float("nan"), len(blobs)))
    r = run(L=L, dx=dx, T=T, u=u, v=v, w=w, noise=noise, seed=seed,
            rec_tu=rec_tu, callback=cb, **params)
    out = dict(status=r["status"], d0=d0, seps=seps)
    if keep_fields and r["status"] == "ok":
        out["u"], out["v"], out["w"] = r["u"], r["v"], r["w"]
    return out
