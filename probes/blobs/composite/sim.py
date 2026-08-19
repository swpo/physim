"""sim.py — M4 composite dynamics engine.

Numerics copied from motility/sim.py (IMEX-FFT stepper, dx=0.5, dt=0.02 conventions;
euler stepper = Day-0 explicit FTCS, dt=min(0.2*dx^2/Dw, 0.02)), extended with
binding's stamp method (relax single blob -> paste (du,dv,dw) deviations) and
MULTI-BLOB identity tracking (periodic label + nearest-neighbor matching,
unwrapped physical coordinates).

Model (Purwins/Schenk 3-component RD):
  du/dt = Du lap u + lam u - u^3 - k3 v - k4 w + k1
  dv/dt = (u - v)/tau   + Dv lap v
  dw/dt = (u - w)/theta + Dw lap w

Per-blob kick (initial condition only): the v,w stamp components are pasted
DISPLACED by kick_d opposite the desired motion direction (the blob drifts away
from its inhibitor shadow) — the stamp analogue of motility's kick convention.
"""
import numpy as np
from scipy import ndimage

M0 = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=3.0, theta=0.7,
          Du=1.0, Dv=1.0, Dw=20.0)


def uniform_state(lam, k1, k3, k4):
    roots = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    return float(real[0])


def circ_com(wgt, dx):
    N = wgt.shape[0]
    tot = wgt.sum()
    if tot <= 0:
        return None
    ang = 2 * np.pi * (np.arange(N) + 0.5) / N
    out = []
    for ax in (0, 1):
        prof = wgt.sum(axis=1 - ax)
        z = (prof * np.exp(1j * ang)).sum() / tot
        out.append((np.angle(z) % (2 * np.pi)) / (2 * np.pi) * N * dx)
    return tuple(out)


def _find(parent, a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


def periodic_label(mask):
    lab, n = ndimage.label(mask)
    if n <= 1:
        return lab, n
    parent = list(range(n + 1))
    def union(a, b):
        ra, rb = _find(parent, a), _find(parent, b)
        if ra != rb:
            parent[rb] = ra
    for a, b in zip(lab[0, :], lab[-1, :]):
        if a > 0 and b > 0:
            union(int(a), int(b))
    for a, b in zip(lab[:, 0], lab[:, -1]):
        if a > 0 and b > 0:
            union(int(a), int(b))
    remap = {}
    k = 0
    for i in range(1, n + 1):
        r = _find(parent, i)
        if r not in remap:
            k += 1
            remap[r] = k
    lut = np.zeros(n + 1, dtype=lab.dtype)
    for i in range(1, n + 1):
        lut[i] = remap[_find(parent, i)]
    return lut[lab], k


def blob_list(u, thr, dx, L):
    """Per-component sub-pixel centroids (periodic circular mean), areas, peaks."""
    mask = u > thr
    lab, n = periodic_label(mask)
    out = []
    N = u.shape[0]
    for i in range(1, n + 1):
        m = lab == i
        wgt = np.where(m, np.clip(u - thr, 0.0, None), 0.0)
        c = circ_com(wgt, dx)
        ys, xs = np.nonzero(m)
        out.append(dict(y=c[0], x=c[1], area=float(m.sum()) * dx * dx,
                        peak=float(u[ys, xs].max())))
    return out


def min_image(d, L):
    return (d + L / 2) % L - L / 2


def make_world_from_stamp(L, dx, u0, stamp, positions, kicks=None):
    """positions: [(y,x)] physical. kicks: [(angle_deg, kick_d)] or None per blob.
    v,w stamp pasted displaced by kick_d OPPOSITE the kick angle (drift toward angle)."""
    n = int(round(L / dx))
    ns = stamp["du"].shape[0]
    u = np.full((n, n), u0)
    v = u.copy()
    w = u.copy()
    cy = ns // 2
    if kicks is None:
        kicks = [None] * len(positions)
    for (py, px), kick in zip(positions, kicks):
        iy, ix = int(round(py / dx)) % n, int(round(px / dx)) % n
        ys = (np.arange(ns) - cy + iy) % n
        xs = (np.arange(ns) - cy + ix) % n
        u[np.ix_(ys, xs)] += stamp["du"]
        if kick is None:
            v[np.ix_(ys, xs)] += stamp["dv"]
            w[np.ix_(ys, xs)] += stamp["dw"]
        else:
            ang, kd = kick
            a = np.deg2rad(ang)
            # displacement opposite desired direction (y first: dy=sin, dx=cos)
            oy = py - kd * np.sin(a)
            ox = px - kd * np.cos(a)
            # sub-pixel paste via FFT shift of stamp? keep simple: integer + frac via roll of full-res stamp
            jy, jx = int(round(oy / dx)) % n, int(round(ox / dx)) % n
            ys2 = (np.arange(ns) - cy + jy) % n
            xs2 = (np.arange(ns) - cy + jx) % n
            v[np.ix_(ys2, xs2)] += stamp["dv"]
            w[np.ix_(ys2, xs2)] += stamp["dw"]
    return u, v, w


def run_fields(u, v, w, p, T, dx, L, stepper="imexfft", dt=None, noise=0.0,
               seed=0, rec_tu=5.0, ntrack=2, snap_times=(), thr_frac=0.45):
    """Integrate fields; track up to ntrack blobs with identity matching.
    Returns dict: t, pos (nrec x ntrack x 2 unwrapped physical), area, peak,
    ncomp, status, fields, snaps."""
    p = dict(M0, **p)
    N = u.shape[0]
    assert N == int(round(L / dx))
    if dt is None:
        dt = min(0.2 * dx * dx / p["Dw"], 0.02) if stepper == "euler" else 0.02
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    inv_dx2 = 1.0 / (dx * dx)
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    thr = u0 + thr_frac * (np.sqrt(p["lam"]) - u0)
    if stepper == "imexfft":
        kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
        kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
        k2 = kf[:, None] ** 2 + kr[None, :] ** 2
        Eu = np.exp(-p["Du"] * k2 * dt)
        Ev = np.exp(-p["Dv"] * k2 * dt)
        Ew = np.exp(-p["Dw"] * k2 * dt)
    lam, k1, k3, k4 = p["lam"], p["k1"], p["k3"], p["k4"]
    tau, theta, Du, Dv, Dw = p["tau"], p["theta"], p["Du"], p["Dv"], p["Dw"]
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    ts, poss, areas, peaks, ncs = [], [], [], [], []
    prev = None      # list of unwrapped positions per identity
    prev_raw = None
    snaps = {}
    snap_left = sorted(snap_times)
    status = "ok"
    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            if not np.isfinite(u).all():
                status = "blowup"
                break
            bl = blob_list(u, thr, dx, L)
            nc = len(bl)
            if nc == 0:
                status = "died"
                ts.append(tt); ncs.append(0)
                break
            # identity matching to previous raw positions
            if prev_raw is None or len(bl) != len(prev_raw):
                # (re)initialize identities: sort by x then y for determinism
                order = np.argsort([b["x"] + 1e-3 * b["y"] for b in bl])
                bl = [bl[i] for i in order]
                raw = np.array([[b["y"], b["x"]] for b in bl])
                unw = raw.copy() if prev is None else None
                if unw is None:
                    # ncomp changed mid-run: restart unwrap at raw
                    unw = raw.copy()
            else:
                raw = np.array([[b["y"], b["x"]] for b in bl])
                # match each prev to nearest new (greedy, min-image)
                used = set()
                idx = []
                for pr in prev_raw:
                    d = np.array([np.hypot(*min_image(raw[j] - pr, L)) if j not in used
                                  else 1e9 for j in range(len(raw))])
                    j = int(np.argmin(d))
                    used.add(j)
                    idx.append(j)
                bl = [bl[j] for j in idx]
                raw = raw[idx]
                step = np.array([min_image(raw[i] - prev_raw[i], L)
                                 for i in range(len(raw))])
                unw = prev + step
            prev_raw = raw
            prev = unw
            ts.append(tt)
            poss.append(unw.copy())
            areas.append([b["area"] for b in bl])
            peaks.append([b["peak"] for b in bl])
            ncs.append(nc)
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = u.copy()
        if t == steps:
            break
        if stepper == "euler":
            lap_u = (np.roll(u,1,0)+np.roll(u,-1,0)+np.roll(u,1,1)+np.roll(u,-1,1)-4.0*u)*inv_dx2
            lap_v = (np.roll(v,1,0)+np.roll(v,-1,0)+np.roll(v,1,1)+np.roll(v,-1,1)-4.0*v)*inv_dx2
            lap_w = (np.roll(w,1,0)+np.roll(w,-1,0)+np.roll(w,1,1)+np.roll(w,-1,1)-4.0*w)*inv_dx2
            un = u + dt * (Du * lap_u + lam * u - u**3 - k3 * v - k4 * w + k1)
            if noise > 0:
                un += noise * sq * rng.standard_normal(u.shape)
            v = v + dt * ((u - v) / tau + Dv * lap_v)
            w = w + dt * ((u - w) / theta + Dw * lap_w)
            u = un
        else:
            un = u + dt * (lam * u - u**3 - k3 * v - k4 * w + k1)
            if noise > 0:
                un += noise * sq * rng.standard_normal(u.shape)
            vn = v + dt * (u - v) / tau
            wn = w + dt * (u - w) / theta
            u = np.fft.irfft2(np.fft.rfft2(un) * Eu, s=un.shape)
            v = np.fft.irfft2(np.fft.rfft2(vn) * Ev, s=vn.shape)
            w = np.fft.irfft2(np.fft.rfft2(wn) * Ew, s=wn.shape)
    # ragged areas/peaks: pad to nc-major lists
    return dict(status=status, u0=u0, thr=thr, dt=dt, dx=dx, L=L,
                t=np.array(ts),
                pos=poss,             # list of (nc_i x 2) arrays, unwrapped
                area=areas, peak=peaks,
                ncomp=np.array(ncs, dtype=int),
                fields=(u, v, w), snaps=snaps)


def relax_stamp(p, L=64.0, dx=0.5, T=2000.0, stepper="imexfft", A=2.0, sig2=18.0):
    """Relax one seeded blob (Day-0 Gaussian u-bump, v,w flat), return centered stamp."""
    p = dict(M0, **p)
    n = int(round(L / dx))
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    x = np.arange(n) * dx
    Y, X = np.meshgrid(x, x, indexing="ij")
    cy = cx = L / 2
    dY = np.abs(Y - cy); dY = np.minimum(dY, L - dY)
    dX = np.abs(X - cx); dX = np.minimum(dX, L - dX)
    u = u0 + A * np.exp(-(dY**2 + dX**2) / sig2)
    v = np.full((n, n), u0)
    w = np.full((n, n), u0)
    r = run_fields(u, v, w, p, T, dx, L, stepper=stepper, rec_tu=25.0, ntrack=1)
    if r["status"] != "ok" or r["ncomp"][-1] != 1:
        return dict(status="fail", detail=r["status"], ncomp=int(r["ncomp"][-1]) if len(r["ncomp"]) else 0)
    uf, vf, wf = r["fields"]
    b = blob_list(uf, r["thr"], dx, L)[0]
    iy, ix = int(round(b["y"] / dx)) % n, int(round(b["x"] / dx)) % n
    sy, sx = n // 2 - iy, n // 2 - ix
    du = np.roll(np.roll(uf - u0, sy, 0), sx, 1)
    dv = np.roll(np.roll(vf - u0, sy, 0), sx, 1)
    dw = np.roll(np.roll(wf - u0, sy, 0), sx, 1)
    return dict(status="ok", du=du, dv=dv, dw=dw, u0=u0, thr=r["thr"],
                area=b["area"], peak=b["peak"], dx=dx)
