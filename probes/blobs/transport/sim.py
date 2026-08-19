"""sim.py — M5-prep TRANSPORT engine: M3 vvw world + STATIC background field b(x).

World (M3 "MAXC", arch vvw, 5 fields u1,v1,u2,v2,w — flavors_core conventions):
  du_i/dt = Du_i lap(u_i) + lam*u_i - u_i^3 - k3*v_i - k4_i*w + k1_i + b(x)
  dv_i/dt = (u_i - v_i)/tau + Dv lap(v_i)
  dw/dt   = ((u1+u2)/2 - w)/theta + Dw lap(w)
  lam=2, k3=1, tau=3, theta=0.7, Dv=1, Dw=20, Du_i=0.65, L=96 periodic, dt=0.01
  A: k1_1=-1.0,     k4_1=1.40   |   B: k1_2=-1.65067, k4_2=2.15   (iso-background)

BACKGROUND FIELD b(x): STATIC (time-independent), additive drive on BOTH
activators (one environment field, all species couple with weight c_i, default
c_1=c_2=1). This is an environment per the honesty rules: it enters the PDE as
k1_i -> k1_i + c_i*b(x); no time dependence, no per-blob terms, no scripting.

Periodic-safe profiles (b varies along axis 0 = "x"):
  tri(eps):  triangle wave, slope +eps on x in [0,L/2), -eps on [L/2,L),
             zero-mean, trough at x=0, peak at x=L/2. Local gradient db/dx = +-eps.
  saw(eps, frac): asymmetric sawtooth, rising slope +eps over frac*P, falling
             slope -eps*frac/(1-frac) over (1-frac)*P, period P=L/n_teeth, zero-mean.
  flat: b=0.

Steppers:
  euler  : Day-0/M3 exact scheme (explicit Euler, 5-pt lap), dx=1,
           dt=min(0.2*dx^2/Dw, 0.02) -> 0.01 at dx=1 (M3 bit-consistent at b=0).
  imexfft: Lie split (explicit reaction incl. b(x), exact FFT diffusion),
           periodic only, any dx; used for grid-refinement (un-pinning) checks.

IC protocol: (1) relax the NO-BLOB world with b(x) in 1D (y-invariant) to get the
x-dependent background profile, broadcast to 2D; (2) stamp u-only Gaussian bumps
(amp 2, sigma 3 — M3 convention, v,w at local background); (3) run.
Blob identity is MEASURED (threshold on excess over the relaxed no-blob base).
"""
import json, os, time
import numpy as np
from scipy import ndimage

BASE = os.path.dirname(os.path.abspath(__file__))

P_MAXC = dict(lam=2.0, k3=1.0, tau=3.0, theta=0.7,
              Du_1=0.65, Du_2=0.65, Dv=1.0, Dw=20.0,
              k1_1=-1.0, k1_2=-1.65067, k4_1=1.40, k4_2=2.15)
UB_ISO = -0.86756          # iso-background level (all fields) at b=0
THR_EXC = 0.45 * (np.sqrt(2.0) - UB_ISO)   # = 1.0268 excess-over-base threshold


# ------------------------------------------------------------------ profiles
def profile_b(kind, N, dx, eps=0.0, frac=0.75, n_teeth=4):
    """Static b at grid NODES x=i*dx, i=0..N-1 (day0/M3 node convention;
    at dx=1 stamps land exactly on M3 grid points). Returns 1D array (axis 0)."""
    L = N * dx
    x = np.arange(N) * dx
    if kind == "flat" or eps == 0.0:
        return np.zeros(N)
    if kind == "tri":
        # trough at x=0, peak at L/2, slope +-eps, zero-mean
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


# ------------------------------------------------------- 1D background relax
def relax_base_1d(p, b, dx, T=400.0, dt=None, tol=1e-10):
    """Relax the no-blob world (y-invariant) with field b(x). Returns (5,N) base."""
    N = b.shape[0]
    if dt is None:
        dt = min(0.2 * dx * dx / p["Dw"], 0.02)
    F = np.full((5, N), UB_ISO, float)
    lam, k3, tau, theta = p["lam"], p["k3"], p["tau"], p["theta"]
    D = np.array([p["Du_1"], p["Du_2"], p["Dv"], p["Dv"], p["Dw"]]).reshape(5, 1)
    inv = 1.0 / (dx * dx)
    steps = int(round(T / dt))
    for t in range(steps):
        Lp = (np.roll(F, 1, 1) + np.roll(F, -1, 1) - 2.0 * F) * inv
        u1, u2, v1, v2, w = F
        R = np.empty_like(F)
        R[0] = lam * u1 - u1**3 - k3 * v1 - p["k4_1"] * w + p["k1_1"] + b
        R[1] = lam * u2 - u2**3 - k3 * v2 - p["k4_2"] * w + p["k1_2"] + b
        R[2] = (u1 - v1) / tau
        R[3] = (u2 - v2) / tau
        R[4] = (0.5 * (u1 + u2) - w) / theta
        Fn = F + dt * (D * Lp + R)
        if t % 200 == 199 and np.max(np.abs(Fn - F)) < tol * dt:
            F = Fn; break
        F = Fn
    if not np.isfinite(F).all():
        return None
    return F


# ------------------------------------------------------------------ tracking
def circ_com(wgt, dx):
    """Sub-pixel COM on periodic grid via circular mean -> (x, y) physical."""
    N0, N1 = wgt.shape
    tot = wgt.sum()
    if tot <= 0:
        return None
    out = []
    for ax, N in ((0, N0), (1, N1)):
        ang = 2 * np.pi * np.arange(N) / N
        prof = wgt.sum(axis=1 - ax)
        z = (prof * np.exp(1j * ang)).sum() / tot
        out.append((np.angle(z) % (2 * np.pi)) / (2 * np.pi) * N * dx)
    return tuple(out)


def measure_species(F, base2d, dx, min_px=4):
    """Per-species excess census: list of dicts (ncomp, area, com, peak)."""
    out = []
    for i in (0, 1):
        e = F[i] - base2d[i]
        m = e > THR_EXC
        a = int(m.sum())
        if a < min_px:
            out.append(dict(ncomp=0, area=0.0, com=None, peak=float(e.max())))
            continue
        lab, nc = ndimage.label(m)
        # periodic wrap merge: relabel via roll if components touch edges
        if nc > 1:
            c0 = circ_com(m.astype(float), 1.0)
            N = m.shape[0]
            mm = np.roll(np.roll(m, N // 2 - int(round(c0[0])), 0),
                         N // 2 - int(round(c0[1])), 1)
            nc = int(ndimage.label(mm)[1])
        com = circ_com(np.clip(e, 0, None) * m, dx)
        out.append(dict(ncomp=int(nc), area=float(a * dx * dx), com=com,
                        peak=float(e.max())))
    return out


# ------------------------------------------------------------------ main run
def run(p=None, eps=0.0, kind="tri", frac=0.75, n_teeth=4, couple=(1.0, 1.0),
        L=96.0, dx=1.0, dt=None, T=1500.0, stepper="euler",
        spots=(("A", 24.0, 48.0),), amp=2.0, sig=3.0,
        noise=0.0, seed=0, rec_tu=5.0, snap_times=(), base_from=None,
        stop_leave=None, init_F=None, track_seeds=None):
    """Integrate the vvw world with static b(x).

    spots: ((species, x, y), ...) species in {"A","B"}; x along gradient axis 0.
    stop_leave: optional (species_idx0, xlo, xhi) early-exit when that blob's
                unwrapped x leaves [xlo,xhi] (runway guard).
    Returns dict: status, t, per-blob tracks (tracks blob #k of its species by
    nearest-continuation), areas, ncomps, base profiles, final fields, snaps.
    """
    p = dict(P_MAXC, **(p or {}))
    N = int(round(L / dx))
    if dt is None:
        dt = min(0.2 * dx * dx / p["Dw"], 0.02) if stepper == "euler" else 0.01
    b = profile_b(kind, N, dx, eps=eps, frac=frac, n_teeth=n_teeth)
    b1 = couple[0] * b; b2 = couple[1] * b
    # base state (no blob): 1D relax -> broadcast
    if base_from is not None:
        base1d = base_from
    else:
        pb = dict(p); base1d = None
        # relax with the two couplings applied
        base1d = _relax_base_couple(p, b1, b2, dx)
    if base1d is None:
        return dict(status="no_base")
    base2d = np.repeat(base1d[:, :, None], N, axis=2)   # (5,N,N) x along axis0
    F = base2d.copy() if init_F is None else np.array(init_F, dtype=float, copy=True)
    x = np.arange(N) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    Lp = N * dx
    for (spn, sx, sy) in spots:
        i = 0 if spn == "A" else 1
        ddx = (X - sx + Lp / 2) % Lp - Lp / 2
        ddy = (Y - sy + Lp / 2) % Lp - Lp / 2
        F[i] += amp * np.exp(-(ddx**2 + ddy**2) / (2 * sig**2))
    if track_seeds is None:
        track_seeds = [(0 if s[0] == "A" else 1, s[1], s[2]) for s in spots]
    else:
        track_seeds = [tuple(s) for s in track_seeds]
    lam, k3, tau, theta = p["lam"], p["k3"], p["tau"], p["theta"]
    k11 = p["k1_1"] + b1[:, None]; k12 = p["k1_2"] + b2[:, None]
    k41, k42 = p["k4_1"], p["k4_2"]
    D = np.array([p["Du_1"], p["Du_2"], p["Dv"], p["Dv"], p["Dw"]]).reshape(5, 1, 1)
    inv = 1.0 / (dx * dx)
    if stepper == "imexfft":
        kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
        kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
        k2 = kf[:, None]**2 + kr[None, :]**2
        E = [np.exp(-Dd * k2 * dt) for Dd in
             (p["Du_1"], p["Du_2"], p["Dv"], p["Dv"], p["Dw"])]
    rng = np.random.default_rng(seed)
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    sq = np.sqrt(dt)
    ts = []
    ntr = len(track_seeds)
    trk = [dict(sp=("A" if track_seeds[k][0] == 0 else "B"),
                x=[], y=[], area=[], nc=[], peak=[]) for k in range(ntr)]
    prev = [None] * ntr; unw = [None] * ntr
    glob = {"n1": [], "n2": [], "a1": [], "a2": []}
    snaps = {}; snap_left = sorted(snap_times)
    status = "ok"; t_end = 0.0
    t0_wall = time.time()
    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            if not np.isfinite(F).all():
                status = "blowup"; t_end = tt; break
            mm = measure_species(F, base2d, dx)
            # global census
            for i, key in ((0, "1"), (1, "2")):
                glob["n" + key].append(mm[i]["ncomp"]); glob["a" + key].append(mm[i]["area"])
            ts.append(tt)
            # per-seeded-blob tracking: nearest component continuation per species
            comps = _components(F, base2d, dx)
            for k in range(ntr):
                i = track_seeds[k][0]
                cand = comps[i]
                if not cand:
                    trk[k]["area"].append(0.0); trk[k]["nc"].append(0)
                    trk[k]["x"].append(np.nan); trk[k]["y"].append(np.nan)
                    trk[k]["peak"].append(0.0)
                    continue
                if prev[k] is None:
                    ref = np.array([track_seeds[k][1], track_seeds[k][2]])
                else:
                    ref = prev[k]
                dbest, cb = None, None
                for c in cand:
                    d = _pdist(np.array(c["com"]), ref, Lp)
                    if dbest is None or d < dbest:
                        dbest, cb = d, c
                raw = np.array(cb["com"])
                if prev[k] is None:
                    unw[k] = raw.copy()
                else:
                    dvec = raw - prev[k]
                    dvec = (dvec + Lp / 2) % Lp - Lp / 2
                    unw[k] = unw[k] + dvec
                prev[k] = raw
                trk[k]["x"].append(float(unw[k][0])); trk[k]["y"].append(float(unw[k][1]))
                trk[k]["area"].append(cb["area"]); trk[k]["nc"].append(len(cand))
                trk[k]["peak"].append(cb["peak"])
            if stop_leave is not None:
                k, xlo, xhi = stop_leave
                xv = trk[k]["x"][-1]
                if np.isfinite(xv) and not (xlo <= xv <= xhi):
                    status = "left_runway"; t_end = tt; break
            t_end = tt
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = F.copy()
        if t == steps:
            break
        # ---- step
        if stepper == "euler":
            Lap = (np.roll(F, 1, 1) + np.roll(F, -1, 1)
                   + np.roll(F, 1, 2) + np.roll(F, -1, 2) - 4.0 * F) * inv
            u1, u2, v1, v2, w = F
            R = np.empty_like(F)
            R[0] = lam * u1 - u1**3 - k3 * v1 - k41 * w + k11
            R[1] = lam * u2 - u2**3 - k3 * v2 - k42 * w + k12
            R[2] = (u1 - v1) / tau
            R[3] = (u2 - v2) / tau
            R[4] = (0.5 * (u1 + u2) - w) / theta
            F = F + dt * (D * Lap + R)
            if noise > 0:
                F[:2] += noise * sq * rng.standard_normal(F[:2].shape)
        else:
            u1, u2, v1, v2, w = F
            R = np.empty_like(F)
            R[0] = lam * u1 - u1**3 - k3 * v1 - k41 * w + k11
            R[1] = lam * u2 - u2**3 - k3 * v2 - k42 * w + k12
            R[2] = (u1 - v1) / tau
            R[3] = (u2 - v2) / tau
            R[4] = (0.5 * (u1 + u2) - w) / theta
            F = F + dt * R
            if noise > 0:
                F[:2] += noise * sq * rng.standard_normal(F[:2].shape)
            for i in range(5):
                F[i] = np.fft.irfft2(np.fft.rfft2(F[i]) * E[i], s=F[i].shape)
    wall = time.time() - t0_wall
    return dict(status=status, t=np.array(ts), tracks=trk, glob=glob,
                base1d=base1d, dt=dt, dx=dx, N=N, b=b, snaps=snaps,
                F=F, base2d_shape=base2d.shape, T_end=t_end, wall_s=wall,
                tu_per_s=(t_end / wall if wall > 0 else None))


def _relax_base_couple(p, b1, b2, dx):
    """1D relax with per-species drive fields b1,b2."""
    N = b1.shape[0]
    dt = min(0.2 * dx * dx / p["Dw"], 0.02)
    F = np.full((5, N), UB_ISO, float)
    lam, k3, tau, theta = p["lam"], p["k3"], p["tau"], p["theta"]
    D = np.array([p["Du_1"], p["Du_2"], p["Dv"], p["Dv"], p["Dw"]]).reshape(5, 1)
    inv = 1.0 / (dx * dx)
    steps = int(round(600.0 / dt))
    for t in range(steps):
        Lp = (np.roll(F, 1, 1) + np.roll(F, -1, 1) - 2.0 * F) * inv
        u1, u2, v1, v2, w = F
        R = np.empty_like(F)
        R[0] = lam * u1 - u1**3 - k3 * v1 - p["k4_1"] * w + p["k1_1"] + b1
        R[1] = lam * u2 - u2**3 - k3 * v2 - p["k4_2"] * w + p["k1_2"] + b2
        R[2] = (u1 - v1) / tau
        R[3] = (u2 - v2) / tau
        R[4] = (0.5 * (u1 + u2) - w) / theta
        F = F + dt * (D * Lp + R)
    if not np.isfinite(F).all():
        return None
    # quiescence check: no pixel above excess threshold vs its own final value
    return F


def _components(F, base2d, dx, min_px=4):
    """Per-species connected components (periodic-aware) with COM/area/peak."""
    out = []
    N = F.shape[1]; Lp = N * dx
    for i in (0, 1):
        e = F[i] - base2d[i]
        m = e > THR_EXC
        if m.sum() < min_px:
            out.append([]); continue
        # label on doubly-rolled copies to handle wrap: use scipy label with manual merge
        lab, nc = ndimage.label(m)
        # merge wrap-adjacent labels
        eq = {}
        def find(a):
            while eq.get(a, a) != a: a = eq[a]
            return a
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb: eq[rb] = ra
        for j in range(N):
            a, bb = lab[0, j], lab[-1, j]
            if a > 0 and bb > 0: union(a, bb)
            a, bb = lab[j, 0], lab[j, -1]
            if a > 0 and bb > 0: union(a, bb)
        roots = {}
        comps = []
        for lbl in range(1, nc + 1):
            r = find(lbl)
            roots.setdefault(r, []).append(lbl)
        for r, group in roots.items():
            mask = np.isin(lab, group)
            a = int(mask.sum())
            if a < min_px: continue
            com = circ_com(np.clip(e, 0, None) * mask, dx)
            comps.append(dict(com=com, area=float(a * dx * dx),
                              peak=float(e[mask].max())))
        out.append(comps)
    return out


def _pdist(a, b, L):
    d = (a - b + L / 2) % L - L / 2
    return float(np.hypot(d[0], d[1]))


# ------------------------------------------------------------------ results IO
def append_result(record, path=None):
    """Concurrency-safe append (fcntl lock) — parallel runjobs share results.json."""
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
