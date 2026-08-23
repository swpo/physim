"""sim.py — MEMBRANE engine: xv twin-world with FREE per-species Dv.

Derived from rotor/sim.py (M7 xv architecture) VERBATIM except:
  * Dv_i is an explicit parameter (rotor hardcoded A_i = tau_i*Dv_i = 4);
    default keeps rotor behavior (Dv_i = 4/tau_i). This lets species mix
    static families: e.g. membrane at the A=5 deep-bond point (tau=2.5,
    Dv=2.0, P7s stamp) + cargo in the A=4 family (Dv=4/tau, A4 stamp).
  * per-species stamp names (stamp1_name/stamp2_name).
  * single-species fast path (species 2 absent -> 3-field integration).
  * bfield support dropped (membranes are self-assembled; no landscapes).

Model (i=1 cargo/probe species, i=2 membrane species; j=3-i):
  du_i/dt = Du lap u_i + lam u_i - u_i^3 - k3 v_i - k4 w_i + k1
  dv_i/dt = (u_i + eta_i*(u_j - u0) - v_i)/tau_i + Dv_i lap v_i
  dw_i/dt = (u_i - w_i)/theta + Dw lap w_i

Numerics: IMEX-FFT batched rfft2, dx=0.5, dt=0.02, L periodic (default 96).
Stamps pasted with exact sub-pixel Fourier shift (rotor convention); kick =
v,w components displaced kick_d OPPOSITE the kick direction. Blob identity is
MEASURED (periodic labeling + tracking), never a state variable.
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
    ky = np.fft.fftfreq(a.shape[0])[:, None]
    kx = np.fft.rfftfreq(a.shape[1])[None, :]
    ph = np.exp(-2j * np.pi * (ky * dy_px + kx * dx_px))
    return np.fft.irfft2(np.fft.rfft2(a) * ph, s=a.shape)


def paste_blobs(u, v, w, stamp, blobs, dx, L):
    """blobs: [(x, y, kick)] physical; kick = None | (angle_deg, kick_d)."""
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


def ring_positions(N, R, cx, cy, phase_deg=0.0):
    """N blob (x, y) positions on a circle of radius R about (cx, cy)."""
    out = []
    for k in range(N):
        a = 2 * np.pi * k / N + np.deg2rad(phase_deg)
        out.append((cx + R * np.cos(a), cy + R * np.sin(a)))
    return out


# ------------------------------------------------------------------ main run
def run(tau1=5.7, tau2=2.5, Dv1=None, Dv2=None, eta12=0.0, eta21=0.0,
        etaw12=0.0, etaw21=0.0,
        L=96.0, dx=0.5, dt=0.02, T=1500.0,
        blobs1=(), blobs2=(), init_from=None, init_slot=1,
        add_blobs1=(), add_blobs2=(),
        noise=0.0, seed=0, rec_tu=5.0, snap_times=(), thr_frac=0.45,
        stamp1_name="stamp_A4_dx05.npz", stamp2_name="stamp_A4_dx05.npz",
        save_fields=True, p_over=None, stop_split=True,
        n1_expect=None, n2_expect=None):
    """Integrate. Species 2 absent (no blobs2/add_blobs2 and eta12==0) ->
    3-field fast path. Returns per-species tracks + fields + snaps (full F)."""
    p = dict(M0, **(p_over or {}))
    N = int(round(L / dx))
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    thr = u0 + thr_frac * (np.sqrt(p["lam"]) - u0)
    Dv1 = A_STAT / tau1 if Dv1 is None else Dv1
    Dv2 = A_STAT / tau2 if Dv2 is None else Dv2
    st1 = load_stamp(stamp1_name, dx=dx)
    st2 = load_stamp(stamp2_name, dx=dx)

    if init_from is not None:
        pth = init_from if not init_from.endswith(".npz") is False and os.path.exists(init_from) else init_from
        if not os.path.exists(pth):
            pth = os.path.join(BASE, "data", init_from if init_from.endswith(".npz")
                               else init_from + ".npz")
        src = np.load(pth)
        F0 = src["F"].astype(float).copy()
        two = (F0.shape[0] == 6) or bool(add_blobs2) or any(
            x != 0.0 for x in (eta12, eta21, etaw12, etaw21))
        nf = 6 if two else 3
        if F0.shape[0] < nf:  # promote 3-field state into a 6-field world
            F = np.full((nf, N, N), u0)
            if init_slot == 2:   # loaded state becomes SPECIES 2 (membrane)
                F[3:6] = F0
            else:
                F[:F0.shape[0]] = F0
        else:
            F = F0
        assert F.shape == (nf, N, N), "init_from grid mismatch"
        if add_blobs1:
            paste_blobs(F[0], F[1], F[2], st1, list(add_blobs1), dx, L)
        if add_blobs2:
            paste_blobs(F[3], F[4], F[5], st2, list(add_blobs2), dx, L)
    else:
        two = bool(blobs2) or any(x != 0.0 for x in (eta12, eta21, etaw12, etaw21))
        nf = 6 if two else 3
        F = np.full((nf, N, N), u0)
        if blobs1:
            paste_blobs(F[0], F[1], F[2], st1, list(blobs1), dx, L)
        if blobs2:
            paste_blobs(F[3], F[4], F[5], st2, list(blobs2), dx, L)

    ref1 = [(b[0], b[1]) for b in (blobs1 or add_blobs1)] or None
    ref2 = [(b[0], b[1]) for b in (blobs2 or add_blobs2)] or None
    tr1, tr2 = Tracker(L, ref1), Tracker(L, ref2)

    lam, k1, k3, k4 = p["lam"], p["k1"], p["k3"], p["k4"]
    theta, Du, Dw = p["theta"], p["Du"], p["Dw"]
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    Dvec = np.array([Du, Dv1, Dw, Du, Dv2, Dw][:nf])
    E = np.exp(-Dvec[:, None, None] * k2[None, :, :] * dt)
    rng = np.random.default_rng(seed)
    sq = np.sqrt(dt)
    n1_0 = n1_expect if n1_expect is not None else len(blobs1 or add_blobs1 or ())
    n2_0 = n2_expect if n2_expect is not None else len(blobs2 or add_blobs2 or ())

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
            u1w, a1, k1w = tr1.update(bl1)
            ts.append(tt)
            P1.append(u1w); A1.append(a1); K1s.append(k1w); NC1.append(len(bl1))
            if two:
                bl2 = blob_list(F[3], thr, dx, L)
                u2w, a2, k2w = tr2.update(bl2)
                P2.append(u2w); A2.append(a2); K2s.append(k2w); NC2.append(len(bl2))
            else:
                bl2 = []
            if stop_split and tt > 50.0 and (
                    (n1_0 and len(bl1) != n1_0) or
                    (two and n2_0 and len(bl2) != n2_0)):
                status = "census_change"; break
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = F.copy()
        if t == steps:
            break
        R = np.empty_like(F)
        if two:
            u1, v1, w1, u2, v2, w2 = F
            R[0] = lam * u1 - u1 ** 3 - k3 * v1 - k4 * w1 + k1
            R[3] = lam * u2 - u2 ** 3 - k3 * v2 - k4 * w2 + k1
            R[1] = (u1 + eta12 * (u2 - u0) - v1) / tau1
            R[4] = (u2 + eta21 * (u1 - u0) - v2) / tau2
            R[2] = (u1 + etaw12 * (u2 - u0) - w1) / theta
            R[5] = (u2 + etaw21 * (u1 - u0) - w2) / theta
        else:
            u1, v1, w1 = F
            R[0] = lam * u1 - u1 ** 3 - k3 * v1 - k4 * w1 + k1
            R[1] = (u1 - v1) / tau1
            R[2] = (u1 - w1) / theta
        Fn = F + dt * R
        if noise > 0:
            Fn[0] += noise * sq * rng.standard_normal((N, N))
            if two:
                Fn[3] += noise * sq * rng.standard_normal((N, N))
        F = np.fft.irfft2(np.fft.rfft2(Fn) * E, s=(N, N))
    wall = time.time() - t0_wall
    return dict(status=status, u0=u0, thr=thr, dt=dt, dx=dx, L=L, N=N,
                two=two, t=np.array(ts),
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
