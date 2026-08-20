"""sim.py — M6 BFIELD engine: single-species A=4 world + DYNAMICAL iso-displacement
field b(x,y,t).

WORLD (machine/sim.py conventions, verbatim numerics; composite/M4 family):
  du/dt = Du lap u + lam u - u^3 - k3 v - k4 w + k1 + b*(u0 - w)
  dv/dt = (u - v)/tau   + Dv lap v
  dw/dt = (u - w)/theta + Dw lap w
  db/dt = (gamma*S(u,w) - b)/tau_b + D_b lap b          <-- NEW: b is a FIELD
  M0 base: lam=2, k1=-0.7, k3=1, k4=1.5, theta=0.7, Du=1, Dw=20;
  A=4 family: Dv = 4/tau. IMEX-FFT, dx=0.5, dt=0.02, L=96 periodic default.

b COUPLING — exactly machine's isok: k1_eff = k1 + u0*b, k4_eff = k4 + b, i.e. the
single reaction term +b*(u0 - w). u0 = -0.70354 stays an EXACT root of the cubic for
any b. VACUUM EXACTNESS WITH DYNAMICS: on the vacuum (u=v=w=u0) all sources vanish
(S1: u-u0=0; S2: u<thr; S3: w-u0=0), so db/dt = -b/tau_b + D_b lap b: b relaxes to 0
and the vacuum (u0,u0,u0,0) is an exact fixed point. Moreover the b-coupling term
b*(u0-w) is QUADRATIC in deviations from vacuum (delta_b * delta_w), so the vacuum's
LINEAR stability is exactly that of the b-less world. Feedback acts only at blob
amplitude — dynamical zero-footprint.

SOURCES (bounded by construction — saturation built into S, b is never clipped):
  s1: S = tanh((u - u0)/A1)            signed (tail ring u<u0 deposits opposite sign)
  s2: S = tanh(max(u - THR,0)/A2)      one-sided core deposit, 0 outside the blob
  s3: S = tanh((w - u0)/A3)            halo-sourced (w-shadow, Dw=20 wide)
  A1=1.0, A2=0.4, A3=0.3 fixed scale constants (blob core saturates S ~ 0.94-0.98).
  THR = u0 + 0.45*(sqrt(lam) - u0) = 0.24944 (the tracking threshold, frozen).
  Steady parked-blob core: b -> ~gamma*S_sat (|b| <= |gamma|), spread by D_b.

b UNITS: k4-units (identical to machine's level ladder; C3 window applies as prior:
active pair window ~[-0.05,+0.025], single statics alive [-0.15,+0.2] uniform).
gamma = full-saturation deposit level in k4-units.

Static b(x) profiles (machine verbatim: saw/tri + y-channel rails) remain available
and ADD to the dynamic field: b_eff = b_static(x,y) + b_dyn(x,y,t).

IC: M4 binding-stamp method (stamp_A4_dx05.npz from composite/data/), kick = v,w
displaced kick_d px. b_dyn(t=0) = 0 unless binit_from (state chaining incl. b).

Tracking: machine/sim.py verbatim (periodic label, circular-mean centroids, greedy
identity matching, unwrapped coords). Blob identity is MEASURED, never state.
"""
import json, os, time
import numpy as np
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))
CDATA = os.path.join(os.path.dirname(BASE), "composite", "data")
MDATA = os.path.join(os.path.dirname(BASE), "machine", "data")

M0 = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=3.0, theta=0.7,
          Du=1.0, Dv=1.0, Dw=20.0)

A1, A2, A3 = 1.0, 0.4, 0.3   # source saturation scales (frozen constants)


def family_A4(tau, **over):
    p = dict(M0, tau=float(tau), Dv=4.0 / float(tau))
    p.update(over)
    return p


def uniform_state(lam, k1, k3, k4):
    roots = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    return float(real[0])


# ---------------------------------------------------------------- b profiles
def profile_b(kind, N, dx, eps=0.0, frac=0.85, n_teeth=2):
    L = N * dx
    x = np.arange(N) * dx
    if kind == "flat" or eps == 0.0:
        return np.zeros(N)
    if kind == "tri":
        g = np.where(x < L / 2, x - L / 4, 3 * L / 4 - x)
        return eps * g
    if kind == "saw":
        P = L / n_teeth
        xp = x % P
        up = frac * P
        g = np.where(xp < up, xp - up / 2,
                     up / 2 - (xp - up) * frac / (1 - frac))
        return eps * g
    raise ValueError(kind)


# ------------------------------------------------------- tracking (machine verbatim)
def circ_com(wgt, dx):
    tot = wgt.sum()
    if tot <= 0:
        return None
    out = []
    for ax in (0, 1):
        Nax = wgt.shape[ax]
        ang = 2 * np.pi * (np.arange(Nax) + 0.5) / Nax
        prof = wgt.sum(axis=1 - ax)
        z = (prof * np.exp(1j * ang)).sum() / tot
        out.append((np.angle(z) % (2 * np.pi)) / (2 * np.pi) * Nax * dx)
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
    mask = u > thr
    lab, n = periodic_label(mask)
    out = []
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


# ------------------------------------------------------------------ stamping
def load_stamp(name="stamp_A4_dx05.npz", dx=0.5, stamp_dx=0.5):
    for root in (os.path.join(BASE, "data"), CDATA, MDATA):
        pth = os.path.join(root, name)
        if os.path.exists(pth):
            st = np.load(pth)
            out = dict(du=st["du"], dv=st["dv"], dw=st["dw"], u0=float(st["u0"]))
            if abs(dx - stamp_dx) > 1e-12:
                from scipy.ndimage import zoom
                f = stamp_dx / dx
                for k in ("du", "dv", "dw"):
                    out[k] = zoom(out[k], f, order=3, mode="grid-wrap")
            return out
    raise FileNotFoundError(name)


def paste_blobs(u, v, w, stamp, blobs, dx, L):
    n = u.shape[0]
    ns = stamp["du"].shape[0]
    cy = ns // 2
    for (px, py, kick) in blobs:
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
            oy = py - kd * np.sin(a)
            ox = px - kd * np.cos(a)
            jy, jx = int(round(oy / dx)) % n, int(round(ox / dx)) % n
            ys2 = (np.arange(ns) - cy + jy) % n
            xs2 = (np.arange(ns) - cy + jx) % n
            v[np.ix_(ys2, xs2)] += stamp["dv"]
            w[np.ix_(ys2, xs2)] += stamp["dw"]
    return u, v, w


# ------------------------------------------------------------------ main run
def run(tau=5.7, p_over=None,
        gamma=0.0, tau_b=200.0, D_b=0.5, source="s2",
        eps=0.0, kind="flat", frac=0.85, n_teeth=2,
        chan_eps=0.0, chan_cap=24.0,
        L=96.0, dx=0.5, dt=0.02, T=1500.0,
        blobs=(), init_from=None, add_blobs=(), vacuum_blob_sector=False,
        noise=0.0, seed=0, rec_tu=5.0, snap_times=(), ref_pos=None,
        stamp_name="stamp_A4_dx05.npz", thr_frac=0.45, save_fields=True,
        allow_empty=False):
    """Integrate the A=4 world + dynamical b. IMEX-FFT all 4 fields.

    b_eff = b_static(x[,y]) + b_dyn;  b_dyn(0)=0 (or from init_from if it has b).
    Records per rec_tu: tracking + b_dyn stats (min, max, b at blob centers).
    Returns dict incl. bstats arrays and final fields (u,v,w,bdyn).
    """
    p = family_A4(tau, **(p_over or {}))
    N = int(round(L / dx))
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    thr = u0 + thr_frac * (np.sqrt(p["lam"]) - u0)
    thr_src = u0 + 0.45 * (np.sqrt(p["lam"]) - u0)   # frozen source threshold
    bstat1d = profile_b(kind, N, dx, eps=eps, frac=frac, n_teeth=n_teeth)
    if chan_eps:
        yy = (np.arange(N) + 0.0) * dx
        dyc = np.minimum(np.abs(yy - L / 2.0), chan_cap)
        b2d = bstat1d[None, :] + chan_eps * dyc[:, None]
    else:
        b2d = bstat1d[None, :]
    stamp = load_stamp(stamp_name, dx=dx)
    bdyn = np.zeros((N, N))
    if init_from is not None:
        src = np.load(os.path.join(BASE, "data", init_from + ".npz"))
        u = src["u"].astype(float).copy()
        v = src["v"].astype(float).copy()
        w = src["w"].astype(float).copy()
        if "bdyn" in src:
            bdyn = src["bdyn"].astype(float).copy()
        assert u.shape == (N, N), "init_from grid mismatch"
        if vacuum_blob_sector:
            # IC surgery (documented per-run): keep the b sector (emergent
            # structure), reset the blob sector to vacuum. ICs are free; the
            # b field configuration was reached by autonomous dynamics.
            u[:] = u0; v[:] = u0; w[:] = u0
        if add_blobs:
            u, v, w = paste_blobs(u, v, w, stamp, list(add_blobs), dx, L)
    else:
        u = np.full((N, N), u0)
        v = u.copy(); w = u.copy()
        u, v, w = paste_blobs(u, v, w, stamp, list(blobs), dx, L)

    if ref_pos is None:
        if init_from is None and blobs:
            ref_pos = [(bx, by) for (bx, by, _k) in blobs]
        elif add_blobs:
            ref_pos = None

    lam, k3, k4b, k1b = p["lam"], p["k3"], p["k4"], p["k1"]
    tau_, theta = p["tau"], p["theta"]
    Du, Dv, Dw = p["Du"], p["Dv"], p["Dw"]
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    Eu = np.exp(-Du * k2 * dt)
    Ev = np.exp(-Dv * k2 * dt)
    Ew = np.exp(-Dw * k2 * dt)
    Eb = np.exp(-D_b * k2 * dt) if D_b > 0 else None
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    ts, poss, areas, peaks, ncs = [], [], [], [], []
    b_mins, b_maxs, b_at = [], [], []
    prev = None; prev_raw = None
    snaps = {}; snap_left = sorted(snap_times)
    status = "ok"
    t0_wall = time.time()
    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            if not np.isfinite(u).all():
                status = "blowup"; break
            bl = blob_list(u, thr, dx, L)
            nc = len(bl)
            if nc == 0:
                ts.append(tt); ncs.append(0)
                areas.append([]); peaks.append([]); poss.append(np.zeros((0, 2)))
                b_mins.append(float(bdyn.min())); b_maxs.append(float(bdyn.max()))
                b_at.append([])
                if not allow_empty:
                    status = "died"; break
                prev = None; prev_raw = None
            elif prev_raw is None or len(bl) != len(prev_raw):
                if ref_pos is not None and len(bl) == len(ref_pos) and prev is None:
                    order, used = [], set()
                    for (rx, ry) in ref_pos:
                        d = [np.hypot(*min_image(np.array([b_["y"] - ry, b_["x"] - rx]), L))
                             if j not in used else 1e9 for j, b_ in enumerate(bl)]
                        j = int(np.argmin(d)); used.add(j); order.append(j)
                    bl = [bl[j] for j in order]
                else:
                    order = np.argsort([b_["x"] + 1e-3 * b_["y"] for b_ in bl])
                    bl = [bl[i] for i in order]
                raw = np.array([[b_["y"], b_["x"]] for b_ in bl])
                unw = raw.copy()
            else:
                raw = np.array([[b_["y"], b_["x"]] for b_ in bl])
                used = set(); idx = []
                for pr in prev_raw:
                    d = np.array([np.hypot(*min_image(raw[j] - pr, L)) if j not in used
                                  else 1e9 for j in range(len(raw))])
                    j = int(np.argmin(d)); used.add(j); idx.append(j)
                bl = [bl[j] for j in idx]
                raw = raw[idx]
                step = np.array([min_image(raw[i] - prev_raw[i], L)
                                 for i in range(len(raw))])
                unw = prev + step
            if nc > 0:
                prev_raw = raw; prev = unw
                ts.append(tt); poss.append(unw.copy())
                areas.append([b_["area"] for b_ in bl])
                peaks.append([b_["peak"] for b_ in bl])
                ncs.append(nc)
                b_mins.append(float(bdyn.min())); b_maxs.append(float(bdyn.max()))
                b_at.append([float(bdyn[int(round(b_["y"] / dx)) % N,
                                        int(round(b_["x"] / dx)) % N]) for b_ in bl])
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = (u.copy(), bdyn.copy())
        if t == steps:
            break
        # ---- source ----
        if source == "s1":
            S = np.tanh((u - u0) / A1)
        elif source == "s2":
            S = np.tanh(np.clip(u - thr_src, 0.0, None) / A2)
        elif source == "s3":
            S = np.tanh((w - u0) / A3)
        else:
            raise ValueError(source)
        beff = b2d + bdyn
        # ---- IMEX step (reaction explicit incl. b-term, diffusion exact in FFT)
        un = u + dt * (lam * u - u**3 - k3 * v - k4b * w + k1b + beff * (u0 - w))
        if noise > 0:
            un += noise * sq * rng.standard_normal(u.shape)
        vn = v + dt * (u - v) / tau_
        wn = w + dt * (u - w) / theta
        bn = bdyn + dt * (gamma * S - bdyn) / tau_b
        u = np.fft.irfft2(np.fft.rfft2(un) * Eu, s=un.shape)
        v = np.fft.irfft2(np.fft.rfft2(vn) * Ev, s=vn.shape)
        w = np.fft.irfft2(np.fft.rfft2(wn) * Ew, s=wn.shape)
        bdyn = (np.fft.irfft2(np.fft.rfft2(bn) * Eb, s=bn.shape)
                if Eb is not None else bn)
    wall = time.time() - t0_wall
    return dict(status=status, u0=u0, thr=thr, dt=dt, dx=dx, L=L, N=N,
                t=np.array(ts), pos=poss, area=areas, peak=peaks,
                ncomp=np.array(ncs, dtype=int), b=bstat1d,
                b_min=np.array(b_mins), b_max=np.array(b_maxs), b_at=b_at,
                fields=(u, v, w, bdyn) if save_fields else None, snaps=snaps,
                wall_s=wall, tu_per_s=(ts[-1] / wall if wall > 0 and ts else None))


# ------------------------------------------------------------------ results IO
def append_result(record, path=None):
    import fcntl
    path = path or os.path.join(BASE, "results.json")
    lockp = path + ".lock"
    with open(lockp, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            with open(path) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        record = dict(record)
        record.setdefault("ts", time.strftime("%Y-%m-%d %H:%M:%S"))
        data.append(record)
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=1)
        os.replace(tmp, path)
        fcntl.flock(lk, fcntl.LOCK_UN)
    return len(data)


def save_state(name, u, v, w, bdyn=None, extra=None):
    kw = dict(u=u.astype(np.float32), v=v.astype(np.float32),
              w=w.astype(np.float32))
    if bdyn is not None:
        kw["bdyn"] = bdyn.astype(np.float32)
    np.savez_compressed(os.path.join(BASE, "data", name + ".npz"),
                        **kw, **(extra or {}))
