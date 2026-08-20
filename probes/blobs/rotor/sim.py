"""sim.py — M7 ROTOR engine: "xv" twin-world architecture.

Two FULLY PRIVATE 3-component Purwins subsystems (u_i, v_i, w_i), i=1 ("M",
motile-dial species) and i=2 ("S", anchor species), coupled ONLY through a
cross-wired slow-inhibitor drive (j = 3-i):

  du_i/dt = Du lap u_i + lam u_i - u_i^3 - k3 v_i - k4 w_i + k1
  dv_i/dt = (u_i + eta_i*(u_j - u0) - v_i)/tau_i + Dv_i lap v_i
  dw_i/dt = (u_i - w_i)/theta + Dw lap w_i

  A_i = tau_i*Dv_i = 4 FIXED (Dv_i = 4/tau_i): both species share the exact
  statics of the certified M4 family (same stamp, same tail landscape);
  tau_i dials per-species drift INDEPENDENTLY. eta = (eta12, eta21) is the
  ONLY cross-species channel (w is private here, unlike M3-vvw: no shared-w
  repulsion by design — the eta v-channel carries BOTH the repulsive core,
  -k3*eta*dv(0) < 0 in k1-units, and the attractive ring, dv(r)<0 for
  r in (6,15), max depth at r~8; see NOTES.md stamp analysis).
  At eta=0 the two subsystems are EXACT copies of composite/sim.py's M4
  world. The uniform background (u0 in all 6 fields) solves the coupled
  system for ANY eta (cross term vanishes identically at u_j = u0):
  background invariance by construction.

Numerics: IMEX-FFT (batched rfft2 over 6 stacked fields), dx=0.5, dt=0.02,
L=96 periodic — M4/M5 conventions verbatim. Stamp: composite
stamp_A4_dx05.npz (A=4-native single-blob deviations du,dv,dw), pasted per
species; kick = v,w components pasted displaced kick_d OPPOSITE the kick
direction (M4 convention). NEW (documented upgrade): sub-pixel placement by
exact Fourier shift of the stamp deviations — removes the integer-rounding
quantization of kick angles (needed for +-20 deg basin tests). At grid-
aligned positions and axis-aligned kicks it reduces to the M4 protocol
exactly (smoke-tested against the M4 anchor numbers).

Tracking: per-species periodic labeling + circular-mean centroids + greedy
identity matching, unwrapped physical coords (composite/sim.py verbatim).
Blob identity is MEASURED, never a state variable.
"""
import json, os, time
import numpy as np
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))
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
    """Per-species identity tracker (composite/sim.py logic, factored)."""
    def __init__(self, L, ref_pos=None):
        self.L = L
        self.ref = ref_pos       # [(x, y)] identity anchors at (re)init
        self.prev = None         # unwrapped (n,2) [y,x]
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
    """Exact periodic sub-pixel shift (pixels) via Fourier phase ramp."""
    if abs(dy_px) < 1e-12 and abs(dx_px) < 1e-12:
        return a
    n0, n1 = a.shape
    ky = np.fft.fftfreq(n0)[:, None]
    kx = np.fft.rfftfreq(n1)[None, :]
    ph = np.exp(-2j * np.pi * (ky * dy_px + kx * dx_px))
    return np.fft.irfft2(np.fft.rfft2(a) * ph, s=a.shape)


def paste_blobs(u, v, w, stamp, blobs, dx, L):
    """blobs: [(x, y, kick)] physical; kick = None | (angle_deg, kick_d).
    Sub-pixel exact paste; kick = v,w displaced kick_d OPPOSITE the direction."""
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


# ----------------------------------------------- background dispersion check
def bg_dispersion(tau1, tau2, eta12, eta21, p_over=None, kmax=3.0, nk=241):
    """Max Re(eig) of the 6-field linearization about the uniform state over
    k in [0,kmax]. Returns (max_growth, k_at_max)."""
    p = dict(M0, **(p_over or {}))
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    fu = p["lam"] - 3 * u0 ** 2
    Dv1, Dv2 = A_STAT / tau1, A_STAT / tau2
    worst, kw = -np.inf, 0.0
    for k in np.linspace(0, kmax, nk):
        q = k * k
        Amat = np.zeros((6, 6))
        # order u1,v1,w1,u2,v2,w2
        Amat[0, 0] = fu - p["Du"] * q; Amat[0, 1] = -p["k3"]; Amat[0, 2] = -p["k4"]
        Amat[1, 0] = 1 / tau1; Amat[1, 1] = -1 / tau1 - Dv1 * q
        Amat[1, 3] = eta12 / tau1
        Amat[2, 0] = 1 / p["theta"]; Amat[2, 2] = -1 / p["theta"] - p["Dw"] * q
        Amat[3, 3] = fu - p["Du"] * q; Amat[3, 4] = -p["k3"]; Amat[3, 5] = -p["k4"]
        Amat[4, 3] = 1 / tau2; Amat[4, 4] = -1 / tau2 - Dv2 * q
        Amat[4, 0] = eta21 / tau2
        Amat[5, 3] = 1 / p["theta"]; Amat[5, 5] = -1 / p["theta"] - p["Dw"] * q
        g = float(np.max(np.linalg.eigvals(Amat).real))
        if g > worst:
            worst, kw = g, float(k)
    return worst, kw


# ------------------------------------------------------------------ main run
def build_bfield(spec, N, dx):
    """Static isok load b(x,y) (machine/sim.py conventions: k1+=u0*b, k4+=b;
    zero-footprint on background). kind "ringcone": ring valley at radius R0
    (slope e_ring, flat beyond cap_r) + center cone valley (slope e_cen, flat
    beyond cap_c); ridge = e_ring*cap_r + e_cen*cap_c between them. Blobs park
    at b-minima (M5 convention: down-b force)."""
    if not spec:
        return None
    x = (np.arange(N) + 0.0) * dx
    Y, X = np.meshgrid(x, x, indexing="ij")
    cx, cy = spec.get("cx", N * dx / 2), spec.get("cy", N * dx / 2)
    dY = np.abs(Y - cy); dY = np.minimum(dY, N * dx - dY)
    dX = np.abs(X - cx); dX = np.minimum(dX, N * dx - dX)
    r = np.hypot(dY, dX)
    if spec["kind"] == "ringcone":
        b = (spec.get("e_ring", 0.0) * np.minimum(np.abs(r - spec["R0"]), spec.get("cap_r", 8.0))
             + spec.get("e_cen", 0.0) * np.minimum(r, spec.get("cap_c", 6.0)))
        return b - b.min()
    raise ValueError(spec["kind"])


def run(tau1=5.7, tau2=2.5, eta12=0.0, eta21=0.0,
        L=96.0, dx=0.5, dt=0.02, T=1500.0,
        blobs1=(), blobs2=(), init_from=None, add_blobs1=(), add_blobs2=(),
        noise=0.0, seed=0, rec_tu=5.0, snap_times=(), thr_frac=0.45,
        stamp_name="stamp_A4_dx05.npz", save_fields=True, p_over=None,
        stop_split=True, bfield=None):
    """Integrate the xv world. blobs_i: [(x, y, kick)] for species i.
    Returns dict with per-species tracks: t, pos1/pos2 (lists of (n,2) [y,x]
    unwrapped), area1/2, peak1/2, ncomp1/2, fields (6,N,N), snaps, status."""
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
    b2d = build_bfield(bfield, N, dx)
    if b2d is not None:
        k1x, k4x = k1 + u0 * b2d, k4 + b2d
    else:
        k1x, k4x = k1, k4
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
            if stop_split and tt > 50.0 and (
                    (n1_0 and len(bl1) != n1_0) or (n2_0 and len(bl2) != n2_0)):
                status = "census_change"; break
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = (F[0].copy(), F[3].copy())
        if t == steps:
            break
        u1, v1, w1, u2, v2, w2 = F
        R = np.empty_like(F)
        R[0] = lam * u1 - u1 ** 3 - k3 * v1 - k4x * w1 + k1x
        R[3] = lam * u2 - u2 ** 3 - k3 * v2 - k4x * w2 + k1x
        R[1] = (u1 + eta12 * (u2 - u0) - v1) / tau1
        R[4] = (u2 + eta21 * (u1 - u0) - v2) / tau2
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
