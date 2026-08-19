"""sim.py — M5 MACHINE engine: single-species A=4 world + STATIC iso-displacement
load field b(x).

WORLD (M4 traveling-bond family; composite/sim.py numerics, verbatim conventions):
  du/dt = Du lap u + lam u - u^3 - k3 v - k4 w + k1
  dv/dt = (u - v)/tau   + Dv lap v
  dw/dt = (u - w)/theta + Dw lap w
  M0 base: lam=2, k1=-0.7, k3=1, k4=1.5, theta=0.7, Du=1, Dw=20;
  A=4 family: Dv = 4/tau, dial tau (traveling corridor tau in (5.636, ~6.15),
  pair-only zone (5.636, 5.748)). IMEX-FFT, dx=0.5, dt=0.02, L=96 periodic.

LOAD FIELD b(x) — "isok" mode, the single-species port of transport's isod dial:
  k1 -> k1 + u0*b(x),  k4 -> k4 + b(x)   (u0 = uniform state = -0.70354; the
  cubic -u^3+(lam-k3-(k4+b))u + (k1+u0*b) has root u0 for ALL b, exactly).
  Reaction perturbation = b(x)*(u0 - w): vanishes IDENTICALLY on the quiescent
  background (w=u0) — zero-footprint force field, force<->stability decoupled
  (transport/SUMMARY.md isod-mode discovery, ported to the single-species world).
  Static, time-independent, no per-blob terms: a legitimate environment.
  b UNITS: k4-units; eps = slope of b in k4-units/px.

PROFILES (transport/sim.py conventions; b varies along axis 1 = "x" in
composite's (y,x) layout):
  tri(eps): trough x=0, ridge x=L/2, slope +-eps, zero-mean.
  saw(eps, frac, n_teeth): rising slope +eps over frac*P, cliff over (1-frac)*P.

IC: M4 binding-stamp method (stamp_A4_dx05.npz reused from composite/data/);
kick = v,w components pasted kick_d px opposite the desired direction.
init_from chaining: load saved (u,v,w) final state, stamp extra cargo (feed).

Tracking: composite/sim.py verbatim (periodic label, circular-mean centroids,
greedy nearest identity matching, unwrapped physical coords). Blob identity is
MEASURED, never a state variable.
"""
import json, os, time
import numpy as np
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))
CDATA = os.path.join(os.path.dirname(BASE), "composite", "data")

M0 = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=3.0, theta=0.7,
          Du=1.0, Dv=1.0, Dw=20.0)


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
    """b at nodes x=i*dx (1D, laid along axis 1). transport/sim.py conventions."""
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


# ------------------------------------------------------- tracking (composite)
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
    """Load stamp; if run dx != stamp_dx, resample (spline zoom) so the pasted
    deviation has the SAME PHYSICAL size at any resolution (grid-check safe)."""
    for root in (os.path.join(BASE, "data"), CDATA):
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
    """blobs: list of (x, y, kick) with kick = None or (angle_deg, kick_d).
    Kick convention (M4): v,w pasted displaced kick_d OPPOSITE the direction."""
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
def run(tau=5.7, p_over=None, eps=0.0, kind="saw", frac=0.85, n_teeth=2,
        chan_eps=0.0, chan_cap=24.0,
        L=96.0, dx=0.5, dt=0.02, T=1500.0,
        blobs=(), init_from=None, add_blobs=(),
        noise=0.0, seed=0, rec_tu=5.0, snap_times=(), ref_pos=None,
        stamp_name="stamp_A4_dx05.npz", thr_frac=0.45, save_fields=True,
        allow_empty=False):
    """Integrate the A=4 world with static b(x) along axis 1 ("x"). IMEX-FFT only.

    blobs:     fresh-world stamping list [(x, y, kick), ...], kick=(ang_deg, kd)|None
    init_from: npz basename in machine/data/ with u,v,w fields (state chaining)
    add_blobs: extra blobs stamped ON TOP of init_from fields (machine feed)
    ref_pos:   [(x, y), ...] identity-order anchors used at t=0 and at any
               ncomp change; default = stamp positions.
    Returns dict: t, pos (list of (nc,2) [y,x] unwrapped), area, peak, ncomp,
    b, fields, snaps, status, wall_s, tu_per_s.
    """
    p = family_A4(tau, **(p_over or {}))
    N = int(round(L / dx))
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    thr = u0 + thr_frac * (np.sqrt(p["lam"]) - u0)
    b = profile_b(kind, N, dx, eps=eps, frac=frac, n_teeth=n_teeth)
    # (stamp loaded below with dx-aware resampling)
    # optional static y-channel (rails): b2d = b(x) + chan_eps*min(|y-L/2|, cap).
    # Same environment class (static, additive on the iso-displacement dial);
    # zero on the track centerline, pushes down-b (= toward centerline) off-axis.
    # Periodic-safe: constant once |y-L/2| >= cap (cap < L/2).
    if chan_eps:
        yy = (np.arange(N) + 0.0) * dx
        dyc = np.minimum(np.abs(yy - L / 2.0), chan_cap)
        b2d = b[None, :] + chan_eps * dyc[:, None]
    else:
        b2d = b[None, :]
    stamp = load_stamp(stamp_name, dx=dx)
    if init_from is not None:
        src = np.load(os.path.join(BASE, "data", init_from + ".npz"))
        u = src["u"].astype(float).copy()
        v = src["v"].astype(float).copy()
        w = src["w"].astype(float).copy()
        assert u.shape == (N, N), "init_from grid mismatch"
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
            ref_pos = None  # caller should pass explicit refs when chaining

    # effective coefficient fields (iso-displacement load, possibly 2D w/ channel)
    k1x = p["k1"] + u0 * b2d
    k4x = p["k4"] + b2d
    lam, k3 = p["lam"], p["k3"]
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
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    ts, poss, areas, peaks, ncs = [], [], [], [], []
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
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = u.copy()
        if t == steps:
            break
        # ---- IMEX step (reaction explicit incl. b(x), diffusion exact in FFT)
        un = u + dt * (lam * u - u**3 - k3 * v - k4x * w + k1x)
        if noise > 0:
            un += noise * sq * rng.standard_normal(u.shape)
        vn = v + dt * (u - v) / tau_
        wn = w + dt * (u - w) / theta
        u = np.fft.irfft2(np.fft.rfft2(un) * Eu, s=un.shape)
        v = np.fft.irfft2(np.fft.rfft2(vn) * Ev, s=vn.shape)
        w = np.fft.irfft2(np.fft.rfft2(wn) * Ew, s=wn.shape)
    wall = time.time() - t0_wall
    return dict(status=status, u0=u0, thr=thr, dt=dt, dx=dx, L=L, N=N,
                t=np.array(ts), pos=poss, area=areas, peak=peaks,
                ncomp=np.array(ncs, dtype=int), b=b,
                fields=(u, v, w) if save_fields else None, snaps=snaps,
                wall_s=wall, tu_per_s=(ts[-1] / wall if wall > 0 and ts else None))


# ------------------------------------------------------------------ results IO
def append_result(record, path=None):
    """Concurrency-safe append (fcntl lock), transport/sim.py verbatim."""
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


def save_state(name, u, v, w, extra=None):
    np.savez_compressed(os.path.join(BASE, "data", name + ".npz"),
                        u=u.astype(np.float32), v=v.astype(np.float32),
                        w=w.astype(np.float32), **(extra or {}))
