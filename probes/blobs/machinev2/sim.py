"""sim.py — blob-factory engine (phase 3, L3->L2): xv twin-world architecture
+ SPATIALLY STRUCTURED couplings.

Fork of rotor/sim.py (M7-certified engine, conventions verbatim) with three
factory extensions, all vacuum-exact by construction:

1. eta(x,y) FIELDS: the cross-v coupling may be a static 2D field
     dv_i/dt = (u_i + eta_i(x,y)*(u_j - u0) - v_i)/tau_i + Dv_i lap v_i
   eta enters the v-equation exactly like isok enters u: the drive vanishes
   identically at u_j = u0, so ANY static eta(x,y) leaves the uniform
   background an exact fixed point. eta specs: scalar (M7 verbatim) or
   {kind: "const"|"xstep"|"xbox", ...} (release docks / null zones).

2. PER-SPECIES isok b-fields: b_i(x,y) applied as k1 -> k1 + u0*b_i,
   k4 -> k4 + b_i in species i's u-equation only. u0 stays an exact root of
   the driven cubic for all b (machine/sim.py isok mode, ported per species).
   New kinds: "chan" (M5 y-rails), "sawchan" (M5 saw + rails), "forkchan"
   (rail Y-junction: valley center y splits per branch after x0), plus
   rotor's "ringcone".

3. Same stamp, tracking, IMEX-FFT dx=0.5 dt=0.02 conventions as rotor/machine.

At scalar eta and shared b this reduces to rotor/sim.py exactly (smoke-tested
against the M7 anchor).
"""
import json, os, time
import numpy as np
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))
CDATA = os.path.join(os.path.dirname(os.path.dirname(BASE)), "blobs", "composite", "data")
CDATA = os.path.join(os.path.dirname(BASE), "composite", "data")

M0 = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, theta=0.7, Du=1.0, Dw=20.0)
A_STAT = 4.0


def uniform_state(lam, k1, k3, k4):
    roots = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    return float(real[0])


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


# ------------------------------------------------------------------ stamping
def load_stamp(name="stamp_A4_dx05.npz", dx=0.5, stamp_dx=0.5):
    for root in (os.path.join(BASE, "data"), CDATA):
        pth = os.path.join(root, name)
        if os.path.exists(pth):
            stf = np.load(pth)
            out = dict(du=stf["du"], dv=stf["dv"], dw=stf["dw"], u0=float(stf["u0"]))
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


# ------------------------------------------------- static environment fields
def build_bfield(spec, N, dx):
    """Static isok load b(x,y). Kinds:
    ringcone (rotor verbatim); chan: chan_eps*min(|y-yc|,cap);
    saw: machine saw along x (eps, P, frac); sawchan: saw+chan;
    forkchan: rails whose valley center yc(x) splits after x0 with slope
    per branch (branch +1/-1), reaching yc +- dy_max."""
    if not spec:
        return None
    x = (np.arange(N) + 0.0) * dx
    Y, X = np.meshgrid(x, x, indexing="ij")
    L = N * dx
    kind = spec["kind"]
    if kind == "ringcone":
        cx, cy = spec.get("cx", L / 2), spec.get("cy", L / 2)
        dY = np.abs(Y - cy); dY = np.minimum(dY, L - dY)
        dX = np.abs(X - cx); dX = np.minimum(dX, L - dX)
        r = np.hypot(dY, dX)
        b = (spec.get("e_ring", 0.0) * np.minimum(np.abs(r - spec["R0"]), spec.get("cap_r", 8.0))
             + spec.get("e_cen", 0.0) * np.minimum(r, spec.get("cap_c", 6.0)))
        return b - b.min()
    b = np.zeros((N, N))
    if kind == "const":
        return b + spec.get("val", 0.0)
    if kind in ("saw", "sawchan"):
        eps = spec.get("eps", 0.0); frac = spec.get("frac", 0.85)
        P = spec.get("P", 32.0)
        xp = X % P
        up = frac * P
        g = np.where(xp < up, xp - up / 2, up / 2 - (xp - up) * frac / (1 - frac))
        b = b + eps * g
    if kind in ("chan", "sawchan"):
        yc = spec.get("yc", L / 2)
        b = b + spec.get("chan_eps", 0.002) * np.minimum(np.abs(Y - yc),
                                                         spec.get("cap", 24.0))
    if kind == "forkchan":
        yc = spec.get("yc", L / 2)
        x0 = spec.get("x0", L / 2)
        slope = spec.get("slope", 0.15) * spec.get("branch", 1)
        dy_max = spec.get("dy_max", 16.0)
        ytgt = yc + np.clip(slope * (X - x0), -dy_max, dy_max) * (X > x0)
        b = spec.get("chan_eps", 0.002) * np.minimum(np.abs(Y - ytgt),
                                                     spec.get("cap", 24.0))
    if kind not in ("saw", "chan", "sawchan", "forkchan", "const"):
        raise ValueError(kind)
    return b


def build_etafield(spec, N, dx):
    """Static cross-coupling field eta(x,y). Scalar -> scalar (M7 verbatim).
    Kinds: const; xstep: eta0 for x<xn, ->0 beyond (tanh width w);
    xbox: eta0 inside [x0,x1] (tanh edges width w)."""
    if spec is None:
        return 0.0
    if isinstance(spec, (int, float)):
        return float(spec)
    x = (np.arange(N) + 0.0) * dx
    Y, X = np.meshgrid(x, x, indexing="ij")
    kind = spec["kind"]
    eta0 = spec.get("eta0", 0.1)
    w = spec.get("w", 3.0)
    if kind == "const":
        return eta0 * np.ones((N, N))
    if kind == "xstep":
        return eta0 * 0.5 * (1.0 - np.tanh((X - spec["xn"]) / w))
    if kind == "xbox":
        return eta0 * 0.25 * ((1.0 + np.tanh((X - spec["x0"]) / w))
                              * (1.0 - np.tanh((X - spec["x1"]) / w)))
    raise ValueError(kind)


# ------------------------------------------------------------------ main run
def run(tau1=5.7, tau2=2.5, eta12=0.0, eta21=0.0,
        L=96.0, dx=0.5, dt=0.02, T=1500.0,
        blobs1=(), blobs2=(), init_from=None, add_blobs1=(), add_blobs2=(),
        noise=0.0, seed=0, rec_tu=5.0, snap_times=(), thr_frac=0.45,
        stamp_name="stamp_A4_dx05.npz", save_fields=True, p_over=None,
        stop_split=True, bfield=None, bfield2=None):
    """xv world w/ factory extensions. eta12/eta21: scalar or etafield spec.
    bfield: isok b for species 1 (and 2 unless bfield2 given)."""
    p = dict(M0, **(p_over or {}))
    N = int(round(L / dx))
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    thr = u0 + thr_frac * (np.sqrt(p["lam"]) - u0)
    Dv1, Dv2 = A_STAT / tau1, A_STAT / tau2
    stamp = load_stamp(stamp_name, dx=dx)

    if init_from is not None:
        src = np.load(os.path.join(BASE, "data", init_from + ".npz"))
        F = src["F"].astype(float).copy()
        assert F.shape == (6, N, N), "init_from grid mismatch"
        if add_blobs1:
            paste_blobs(F[0], F[1], F[2], stamp, list(add_blobs1), dx, L)
        if add_blobs2:
            paste_blobs(F[3], F[4], F[5], stamp, list(add_blobs2), dx, L)
    else:
        F = np.full((6, N, N), u0)
        if blobs1:
            paste_blobs(F[0], F[1], F[2], stamp, list(blobs1), dx, L)
        if blobs2:
            paste_blobs(F[3], F[4], F[5], stamp, list(blobs2), dx, L)

    ref1 = [(b[0], b[1]) for b in (blobs1 or add_blobs1)] or None
    ref2 = [(b[0], b[1]) for b in (blobs2 or add_blobs2)] or None
    tr1, tr2 = Tracker(L, ref1), Tracker(L, ref2)

    lam, k1, k3, k4 = p["lam"], p["k1"], p["k3"], p["k4"]
    theta, Du, Dw = p["theta"], p["Du"], p["Dw"]
    b1 = build_bfield(bfield, N, dx)
    b2 = build_bfield(bfield2, N, dx) if bfield2 is not None else b1
    k1x1, k4x1 = (k1 + u0 * b1, k4 + b1) if b1 is not None else (k1, k4)
    k1x2, k4x2 = (k1 + u0 * b2, k4 + b2) if b2 is not None else (k1, k4)
    E12 = build_etafield(eta12, N, dx)
    E21 = build_etafield(eta21, N, dx)
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    Dvec = np.array([Du, Dv1, Dw, Du, Dv2, Dw])
    E = np.exp(-Dvec[:, None, None] * k2[None, :, :] * dt)
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    n1_0, n2_0 = len(blobs1 or add_blobs1 or ()), len(blobs2 or add_blobs2 or ())
    if init_from is not None:
        # census baseline = blobs present in the loaded state + added
        n1_0 = None; n2_0 = None   # set from first record below
    ts = []
    P1, A1, K1s, NC1 = [], [], [], []
    P2, A2, K2s, NC2 = [], [], [], []
    snaps = {}; snap_left = sorted(snap_times)
    status = "ok"
    t0_wall = time.time()
    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            if not np.isfinite(F).all():
                status = "blowup"; break
            bl1 = blob_list(F[0], thr, dx, L)
            bl2 = blob_list(F[3], thr, dx, L)
            u1w, a1, k1w = tr1.update(bl1)
            u2w, a2, k2w = tr2.update(bl2)
            ts.append(tt)
            P1.append(u1w); A1.append(a1); K1s.append(k1w); NC1.append(len(bl1))
            P2.append(u2w); A2.append(a2); K2s.append(k2w); NC2.append(len(bl2))
            if n1_0 is None:
                n1_0, n2_0 = len(bl1), len(bl2)
            if stop_split and tt > 50.0 and (
                    (n1_0 and len(bl1) != n1_0) or (n2_0 and len(bl2) != n2_0)):
                status = "census_change"; break
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = (F[0].copy(), F[3].copy())
        if t == steps:
            break
        u1, v1, w1, u2, v2, w2 = F
        R = np.empty_like(F)
        R[0] = lam * u1 - u1 ** 3 - k3 * v1 - k4x1 * w1 + k1x1
        R[3] = lam * u2 - u2 ** 3 - k3 * v2 - k4x2 * w2 + k1x2
        R[1] = (u1 + E12 * (u2 - u0) - v1) / tau1
        R[4] = (u2 + E21 * (u1 - u0) - v2) / tau2
        R[2] = (u1 - w1) / theta
        R[5] = (u2 - w2) / theta
        Fn = F + dt * R
        if noise > 0:
            Fn[0] += noise * sq * rng.standard_normal((N, N))
            Fn[3] += noise * sq * rng.standard_normal((N, N))
        F = np.fft.irfft2(np.fft.rfft2(Fn) * E, s=(N, N))
    wall = time.time() - t0_wall
    return dict(status=status, u0=u0, thr=thr, dt=dt, dx=dx, L=L, N=N,
                t=np.array(ts),
                pos1=P1, area1=A1, peak1=K1s, ncomp1=np.array(NC1, int),
                pos2=P2, area2=A2, peak2=K2s, ncomp2=np.array(NC2, int),
                fields=F if save_fields else None, snaps=snaps,
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


def save_state(name, F, extra=None):
    np.savez_compressed(os.path.join(BASE, "data", name + ".npz"),
                        F=F.astype(np.float32), **(extra or {}))
