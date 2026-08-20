"""sim.py — PHASE-3 GENESIS engine: L2->L1 reduction tests.

Single-species A=4 world + dynamical b (bfield/sim.py verbatim physics), EXTENDED:
  * freeze_b:    hold b fixed (frozen self-written landscape = static environment)
  * binit_from:  load ONLY the b field from a saved state (landscape reuse),
                 b_scale multiplies it (shape-vs-amplitude separation)
  * two=True:    optional 2nd species (u2,v2,w2) with M7 rotor "xv" cross-v coupling
                 (eta12/eta21); b sources from u1 ONLY and couples into u1 ONLY
                 ("b on the motile species"). At eta=0 or vacuum u2: exactly bfield.

  du1/dt = Du lap u1 + lam u1 - u1^3 - k3 v1 - k4 w1 + k1 + beff*(u0 - w1)
  dv1/dt = (u1 + eta12*(u2 - u0) - v1)/tau1 + Dv1 lap v1
  dw1/dt = (u1 - w1)/theta + Dw lap w1
  du2/dt = Du lap u2 + lam u2 - u2^3 - k3 v2 - k4 w2 + k1
  dv2/dt = (u2 + eta21*(u1 - u0) - v2)/tau2 + Dv2 lap v2
  dw2/dt = (u2 - w2)/theta + Dw lap w2
  db/dt  = (gamma*S(u1) - b)/tau_b + D_b lap b       [skipped if freeze_b]

A_i = tau_i*Dv_i = 4 both. IMEX-FFT dx=0.5 dt=0.02 L=96 periodic default.
Vacuum (u0 x6, b=0) exact for any eta/gamma (cross + source terms vanish).
Sub-pixel Fourier-shift stamp paste (rotor convention; = M4 at grid-aligned).
Sources s1/s2/s3 and static saw/tri/chan profiles: bfield verbatim.
Tracking per species: machine/composite verbatim. Identity MEASURED, never state.
"""
import json, os, time
import numpy as np
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))
PB = os.path.dirname(BASE)
CDATA = os.path.join(PB, "composite", "data")
MDATA = os.path.join(PB, "machine", "data")
BDATA = os.path.join(PB, "bfield", "data")

M0 = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=3.0, theta=0.7,
          Du=1.0, Dv=1.0, Dw=20.0)
A1, A2, A3 = 1.0, 0.4, 0.3


def family_A4(tau, **over):
    p = dict(M0, tau=float(tau), Dv=4.0 / float(tau))
    p.update(over)
    return p


def uniform_state(lam, k1, k3, k4):
    roots = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    return float(real[0])


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


# ------------------------------------------------------------------- tracking
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


class Tracker:
    def __init__(self, L, ref_pos=None):
        self.L = L
        self.ref = ref_pos
        self.prev = None
        self.prev_raw = None

    def update(self, bl):
        L = self.L
        if len(bl) == 0:
            self.prev = None; self.prev_raw = None
            return np.zeros((0, 2)), [], []
        if self.prev_raw is None or len(bl) != len(self.prev_raw):
            if self.ref is not None and len(bl) == len(self.ref) and self.prev is None:
                order, used = [], set()
                for (rx, ry) in self.ref:
                    d = [np.hypot(*min_image(np.array([b["y"] - ry, b["x"] - rx]), L))
                         if j not in used else 1e9 for j, b in enumerate(bl)]
                    j = int(np.argmin(d)); used.add(j); order.append(j)
                bl = [bl[j] for j in order]
            else:
                order = np.argsort([b["x"] + 1e-3 * b["y"] for b in bl])
                bl = [bl[i] for i in order]
            raw = np.array([[b["y"], b["x"]] for b in bl])
            unw = raw.copy()
        else:
            raw = np.array([[b["y"], b["x"]] for b in bl])
            used = set(); idx = []
            for pr in self.prev_raw:
                d = np.array([np.hypot(*min_image(raw[j] - pr, L)) if j not in used
                              else 1e9 for j in range(len(raw))])
                j = int(np.argmin(d)); used.add(j); idx.append(j)
            bl = [bl[j] for j in idx]
            raw = raw[idx]
            step = np.array([min_image(raw[i] - self.prev_raw[i], L)
                             for i in range(len(raw))])
            unw = self.prev + step
        self.prev_raw = raw; self.prev = unw
        return unw.copy(), [b["area"] for b in bl], [b["peak"] for b in bl]


# ------------------------------------------------------------------- stamping
def load_stamp(name="stamp_A4_dx05.npz", dx=0.5, stamp_dx=0.5):
    for root in (os.path.join(BASE, "data"), CDATA, MDATA, BDATA):
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


def fshift(a, dy_px, dx_px):
    if abs(dy_px) < 1e-12 and abs(dx_px) < 1e-12:
        return a
    n0, n1 = a.shape
    ky = np.fft.fftfreq(n0)[:, None]
    kx = np.fft.rfftfreq(n1)[None, :]
    ph = np.exp(-2j * np.pi * (ky * dy_px + kx * dx_px))
    return np.fft.irfft2(np.fft.rfft2(a) * ph, s=a.shape)


def paste_blobs(u, v, w, stamp, blobs, dx, L):
    n = u.shape[0]
    ns = stamp["du"].shape[0]
    cy = ns // 2
    for (px, py, kick) in blobs:
        gy, gx = py / dx, px / dx
        iy, ix = int(round(gy)) % n, int(round(gx)) % n
        fy, fx = gy - round(gy), gx - round(gx)
        ys = (np.arange(ns) - cy + iy) % n
        xs = (np.arange(ns) - cy + ix) % n
        u[np.ix_(ys, xs)] += fshift(stamp["du"], fy, fx)
        if kick is None:
            oy_g, ox_g = gy, gx
        else:
            ang, kd = kick
            a = np.deg2rad(ang)
            oy_g = gy - kd * np.sin(a) / dx
            ox_g = gx - kd * np.cos(a) / dx
        jy, jx = int(round(oy_g)) % n, int(round(ox_g)) % n
        gy2, gx2 = oy_g - round(oy_g), ox_g - round(ox_g)
        ys2 = (np.arange(ns) - cy + jy) % n
        xs2 = (np.arange(ns) - cy + jx) % n
        v[np.ix_(ys2, xs2)] += fshift(stamp["dv"], gy2, gx2)
        w[np.ix_(ys2, xs2)] += fshift(stamp["dw"], gy2, gx2)
    return u, v, w


def _find_state(name):
    for root in (os.path.join(BASE, "data"), BDATA):
        pth = os.path.join(root, name + ".npz")
        if os.path.exists(pth):
            return pth
    raise FileNotFoundError(name)


# ------------------------------------------------------------------- main run
def run(tau=5.7, p_over=None, two=False, tau2=2.5, eta12=0.0, eta21=0.0,
        gamma=0.0, tau_b=200.0, D_b=0.0, source="s2",
        eps=0.0, kind="flat", frac=0.85, n_teeth=2,
        chan_eps=0.0, chan_cap=24.0,
        L=96.0, dx=0.5, dt=0.02, T=1500.0,
        blobs=(), blobs2=(), init_from=None, add_blobs=(), add_blobs2=(),
        vacuum_blob_sector=False, binit_from=None, freeze_b=False, b_scale=1.0,
        noise=0.0, seed=0, rec_tu=5.0, snap_times=(), ref_pos=None, ref_pos2=None,
        stamp_name="stamp_A4_dx05.npz", thr_frac=0.45, save_fields=True,
        allow_empty=False):
    p = family_A4(tau, **(p_over or {}))
    N = int(round(L / dx))
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    thr = u0 + thr_frac * (np.sqrt(p["lam"]) - u0)
    thr_src = u0 + 0.45 * (np.sqrt(p["lam"]) - u0)
    bstat1d = profile_b(kind, N, dx, eps=eps, frac=frac, n_teeth=n_teeth)
    if chan_eps:
        yy = (np.arange(N) + 0.0) * dx
        dyc = np.minimum(np.abs(yy - L / 2.0), chan_cap)
        b2d = bstat1d[None, :] + chan_eps * dyc[:, None]
    else:
        b2d = bstat1d[None, :] * np.ones((N, 1))
    stamp = load_stamp(stamp_name, dx=dx)
    bdyn = np.zeros((N, N))
    u2 = v2 = w2 = None
    if init_from is not None:
        src = np.load(_find_state(init_from))
        u = src["u"].astype(float).copy()
        v = src["v"].astype(float).copy()
        w = src["w"].astype(float).copy()
        if "bdyn" in src:
            bdyn = src["bdyn"].astype(float).copy()
        if two and "u2" in src:
            u2 = src["u2"].astype(float).copy()
            v2 = src["v2"].astype(float).copy()
            w2 = src["w2"].astype(float).copy()
        assert u.shape == (N, N), "init_from grid mismatch"
        if vacuum_blob_sector:
            u[:] = u0; v[:] = u0; w[:] = u0
            if u2 is not None:
                u2[:] = u0; v2[:] = u0; w2[:] = u0
    else:
        u = np.full((N, N), u0)
        v = u.copy(); w = u.copy()
        u, v, w = paste_blobs(u, v, w, stamp, list(blobs), dx, L)
    if binit_from is not None:
        src = np.load(_find_state(binit_from))
        bdyn = src["bdyn"].astype(float).copy()
        if bdyn.shape != (N, N):
            from scipy.ndimage import zoom
            bdyn = zoom(bdyn, N / bdyn.shape[0], order=3, mode="grid-wrap")
            assert bdyn.shape == (N, N)
    bdyn *= b_scale
    if add_blobs:
        u, v, w = paste_blobs(u, v, w, stamp, list(add_blobs), dx, L)
    if two:
        if u2 is None:
            u2 = np.full((N, N), u0)
            v2 = u2.copy(); w2 = u2.copy()
        if blobs2 or add_blobs2:
            u2, v2, w2 = paste_blobs(u2, v2, w2, stamp,
                                     list(blobs2) + list(add_blobs2), dx, L)

    if ref_pos is None and init_from is None and blobs:
        ref_pos = [(bx, by) for (bx, by, _k) in blobs]
    if ref_pos is None and add_blobs:
        ref_pos = [(bx, by) for (bx, by, _k) in add_blobs]
    if two and ref_pos2 is None:
        bb2 = list(blobs2) + list(add_blobs2)
        if bb2:
            ref_pos2 = [(bx, by) for (bx, by, _k) in bb2]

    lam, k3, k4b, k1b = p["lam"], p["k3"], p["k4"], p["k1"]
    tau1_, theta = p["tau"], p["theta"]
    Du, Dv1, Dw = p["Du"], p["Dv"], p["Dw"]
    Dv2 = 4.0 / tau2
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    Eu = np.exp(-Du * k2 * dt)
    Ev1 = np.exp(-Dv1 * k2 * dt)
    Ew = np.exp(-Dw * k2 * dt)
    Ev2 = np.exp(-Dv2 * k2 * dt) if two else None
    Eb = np.exp(-D_b * k2 * dt) if (D_b > 0 and not freeze_b) else None
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    tr1 = Tracker(L, ref_pos)
    tr2 = Tracker(L, ref_pos2) if two else None
    ts, poss, areas, ncs = [], [], [], []
    poss2, areas2, ncs2 = [], [], []
    b_mins, b_maxs, b_at = [], [], []
    umax_dev = []
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
            if nc == 0 and not allow_empty and not two:
                status = "died"; ts.append(tt); ncs.append(0)
                poss.append(np.zeros((0, 2))); areas.append([])
                b_mins.append(float(bdyn.min())); b_maxs.append(float(bdyn.max()))
                b_at.append([]); umax_dev.append(float(np.abs(u - u0).max()))
                break
            unw, ar, _pk = tr1.update(bl)
            ts.append(tt); poss.append(unw); areas.append(ar); ncs.append(nc)
            b_mins.append(float(bdyn.min())); b_maxs.append(float(bdyn.max()))
            b_at.append([float(bdyn[int(round(b_["y"] / dx)) % N,
                                    int(round(b_["x"] / dx)) % N]) for b_ in bl])
            umax_dev.append(float(np.abs(u - u0).max()))
            if two:
                bl2 = blob_list(u2, thr, dx, L)
                unw2, ar2, _ = tr2.update(bl2)
                poss2.append(unw2); areas2.append(ar2); ncs2.append(len(bl2))
        while snap_left and tt >= snap_left[0] - 1e-9:
            key = snap_left.pop(0)
            snaps[key] = (u.copy(), bdyn.copy()) if not two else \
                         (u.copy(), bdyn.copy(), u2.copy())
        if t == steps:
            break
        if source == "s1":
            S = np.tanh((u - u0) / A1)
        elif source == "s2":
            S = np.tanh(np.clip(u - thr_src, 0.0, None) / A2)
        elif source == "s3":
            S = np.tanh((w - u0) / A3)
        else:
            raise ValueError(source)
        beff = b2d + bdyn
        if two:
            un = u + dt * (lam * u - u**3 - k3 * v - k4b * w + k1b + beff * (u0 - w))
            vn = v + dt * (u + eta12 * (u2 - u0) - v) / tau1_
            wn = w + dt * (u - w) / theta
            un2 = u2 + dt * (lam * u2 - u2**3 - k3 * v2 - k4b * w2 + k1b)
            vn2 = v2 + dt * (u2 + eta21 * (u - u0) - v2) / tau2
            wn2 = w2 + dt * (u2 - w2) / theta
            if noise > 0:
                un += noise * sq * rng.standard_normal(u.shape)
                un2 += noise * sq * rng.standard_normal(u.shape)
            u2 = np.fft.irfft2(np.fft.rfft2(un2) * Eu, s=un2.shape)
            v2 = np.fft.irfft2(np.fft.rfft2(vn2) * Ev2, s=vn2.shape)
            w2 = np.fft.irfft2(np.fft.rfft2(wn2) * Ew, s=wn2.shape)
        else:
            un = u + dt * (lam * u - u**3 - k3 * v - k4b * w + k1b + beff * (u0 - w))
            vn = v + dt * (u - v) / tau1_
            wn = w + dt * (u - w) / theta
            if noise > 0:
                un += noise * sq * rng.standard_normal(u.shape)
        if not freeze_b:
            bn = bdyn + dt * (gamma * S - bdyn) / tau_b
            bdyn = (np.fft.irfft2(np.fft.rfft2(bn) * Eb, s=bn.shape)
                    if Eb is not None else bn)
        u = np.fft.irfft2(np.fft.rfft2(un) * Eu, s=un.shape)
        v = np.fft.irfft2(np.fft.rfft2(vn) * Ev1, s=vn.shape)
        w = np.fft.irfft2(np.fft.rfft2(wn) * Ew, s=wn.shape)
    wall = time.time() - t0_wall
    out = dict(status=status, u0=u0, thr=thr, dt=dt, dx=dx, L=L, N=N,
               t=np.array(ts), pos=poss, area=areas,
               ncomp=np.array(ncs, dtype=int), b=bstat1d,
               b_min=np.array(b_mins), b_max=np.array(b_maxs), b_at=b_at,
               umax_dev=np.array(umax_dev),
               snaps=snaps, wall_s=wall,
               tu_per_s=(ts[-1] / wall if wall > 0 and ts else None))
    if two:
        out["pos2"] = poss2; out["area2"] = areas2
        out["ncomp2"] = np.array(ncs2, dtype=int)
    if save_fields:
        out["fields"] = (u, v, w, bdyn) if not two else (u, v, w, bdyn, u2, v2, w2)
    else:
        out["fields"] = None
    return out


# ---------------------------------------------------------------- results IO
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


def save_state(name, u, v, w, bdyn=None, u2=None, v2=None, w2=None, extra=None):
    kw = dict(u=u.astype(np.float32), v=v.astype(np.float32),
              w=w.astype(np.float32))
    if bdyn is not None:
        kw["bdyn"] = bdyn.astype(np.float32)
    if u2 is not None:
        kw["u2"] = u2.astype(np.float32)
        kw["v2"] = v2.astype(np.float32)
        kw["w2"] = w2.astype(np.float32)
    np.savez_compressed(os.path.join(BASE, "data", name + ".npz"),
                        **kw, **(extra or {}))
