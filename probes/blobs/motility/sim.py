"""sim.py — 3-component reaction-diffusion (Purwins/Schenk gas-discharge class).

  du/dt = Du lap(u) + lam*u - u^3 - k3*v - k4*w + k1     (activator)
  dv/dt = (u - v)/tau   + Dv lap(v)                      (slow inhibitor)
  dw/dt = (u - w)/theta + Dw lap(w)                      (fast long-range inhibitor)

Integrator: explicit Euler / FTCS with 5-point Laplacian, EXACTLY the Day-0
scheme, generalized to arbitrary grid spacing dx (lap -> lap/dx^2) and to
no-flux boundaries.  dt auto-rule generalizes Day-0's dt=min(0.2/Dw, 0.02):
dt = min(0.2*dx^2/Dw, 0.02)  [Day-0 point dx=1 -> dt=0.01, bit-compatible].

Physical domain is L_phys x L_phys (default 96x96), N = round(L_phys/dx).
All positions/lengths returned in PHYSICAL units, times in tu.

Blob seeding (initial condition only; all subsequent motion is autonomous):
  u = u0 + A exp(-r^2 / (2 sigma^2))          (Day-0: A=2, sigma=3)
  v = w = u0                                   (Day-0 baseline, no kick)
Optional drift kick (breaks symmetry; direction alpha, displacement d):
  v gets a bump a_v*A exp(-r_v^2/(2 sigma^2)) centered at c - d*(cos a, sin a),
  same for w. The blob drifts AWAY from its displaced inhibitor shadow.
  This is an analytic, sub-pixel, angle-continuous seeded asymmetry.
"""
import numpy as np
from scipy import ndimage


def uniform_state(lam, k1, k3, k4):
    roots = np.roots([-1.0, 0.0, lam - k3 - k4, k1])
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    return float(real[0])


def lap_periodic(X, inv_dx2):
    return (np.roll(X, 1, 0) + np.roll(X, -1, 0) +
            np.roll(X, 1, 1) + np.roll(X, -1, 1) - 4.0 * X) * inv_dx2


def lap_neumann(X, inv_dx2):
    P = np.pad(X, 1, mode="edge")
    return (P[:-2, 1:-1] + P[2:, 1:-1] + P[1:-1, :-2] + P[1:-1, 2:] - 4.0 * X) * inv_dx2


M0 = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=3.0, theta=0.7,
          Du=1.0, Dv=1.0, Dw=20.0)


def make_ic(N, dx, p, A=2.0, sigma=3.0, center=None,
            kick_angle=None, kick_d=2.0, kick_av=0.6):
    u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    L = N * dx
    if center is None:
        center = (L / 2.0, L / 2.0)
    x = (np.arange(N) + 0.5) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    def bump(cx, cy, amp):
        # periodic minimal-image distances so bumps wrap cleanly
        ddx = (X - cx + L / 2) % L - L / 2
        ddy = (Y - cy + L / 2) % L - L / 2
        return amp * np.exp(-(ddx**2 + ddy**2) / (2 * sigma**2))
    u = u0 + bump(center[0], center[1], A)
    v = np.full((N, N), u0)
    w = np.full((N, N), u0)
    if kick_angle is not None:
        a = np.deg2rad(kick_angle)
        cx = center[0] - kick_d * np.cos(a)
        cy = center[1] - kick_d * np.sin(a)
        v = v + bump(cx, cy, kick_av * A)
        w = w + bump(cx, cy, kick_av * A)
    return u, v, w, u0


def circ_com(wgt, dx):
    """Sub-pixel center of mass on a periodic grid via circular mean.
    Returns (px, py) in physical units, or None if wgt sums to ~0."""
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


def ncomp_periodic(mask):
    """Connected components with periodic wrap handled by recentering."""
    if not mask.any():
        return 0
    N = mask.shape[0]
    c = circ_com(mask.astype(float), 1.0)
    m = np.roll(np.roll(mask, N // 2 - int(round(c[0])), 0),
                N // 2 - int(round(c[1])), 1)
    return int(ndimage.label(m)[1])


def run(p=None, T=600.0, dx=1.0, L_phys=96.0, dt=None, boundary="periodic",
        noise=0.0, seed=0, rec_tu=2.0, ic=None, A=2.0, sigma=3.0,
        kick_angle=None, kick_d=2.0, kick_av=0.6, snap_times=(),
        thr_frac=0.45, stepper="euler", center=None):
    """Integrate; track blob COM (unwrapped, physical units), area, ncomp.

    stepper="euler":   Day-0 exact scheme (explicit Euler + 5-pt Laplacian),
                       dt default min(0.2*dx^2/Dw, 0.02) (Day-0: dx=1 -> 0.01).
    stepper="imexfft": Lie split-step — explicit-Euler reaction, then EXACT
                       periodic diffusion via FFT integrating factor
                       exp(-D k^2 dt), continuum spectrum k=2*pi*m/L.
                       Unconditionally diffusion-stable; dt default 0.02
                       (reaction-limited). Periodic boundaries only.
    Returns dict with track arrays + final fields."""
    p = dict(M0, **(p or {}))
    N = int(round(L_phys / dx))
    if dt is None:
        dt = min(0.2 * dx * dx / p["Dw"], 0.02) if stepper == "euler" else 0.02
    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    inv_dx2 = 1.0 / (dx * dx)
    lap = lap_periodic if boundary == "periodic" else lap_neumann
    if stepper == "imexfft":
        assert boundary == "periodic", "imexfft is periodic-only"
        kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
        kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
        k2 = kf[:, None] ** 2 + kr[None, :] ** 2
        Eu = np.exp(-p["Du"] * k2 * dt)
        Ev = np.exp(-p["Dv"] * k2 * dt)
        Ew = np.exp(-p["Dw"] * k2 * dt)
    rng = np.random.default_rng(seed)
    if ic is None:
        u, v, w, u0 = make_ic(N, dx, p, A=A, sigma=sigma, center=center,
                              kick_angle=kick_angle, kick_d=kick_d, kick_av=kick_av)
    else:
        u, v, w = [np.array(a, dtype=float, copy=True) for a in ic]
        u0 = uniform_state(p["lam"], p["k1"], p["k3"], p["k4"])
    thr = u0 + thr_frac * (np.sqrt(p["lam"]) - u0)
    lam, k1, k3, k4 = p["lam"], p["k1"], p["k3"], p["k4"]
    tau, theta, Du, Dv, Dw = p["tau"], p["theta"], p["Du"], p["Dv"], p["Dw"]
    sq = np.sqrt(dt)
    ts, coms, areas, ncs = [], [], [], []
    snaps = {}
    snap_left = sorted(snap_times)
    prev_raw = None; unwrapped = None; Lp = N * dx
    status = "ok"
    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            m = u > thr
            a = m.sum()
            if a == 0:
                status = "died"; ts.append(tt); areas.append(0.0); break
            wgt = np.clip(u - thr, 0.0, None)
            raw = np.array(circ_com(wgt, dx))
            if prev_raw is None:
                unwrapped = raw.copy()
            else:
                d = raw - prev_raw
                d = (d + Lp / 2) % Lp - Lp / 2
                unwrapped = unwrapped + d
            prev_raw = raw
            ts.append(tt); coms.append(unwrapped.copy())
            areas.append(float(a) * dx * dx); ncs.append(ncomp_periodic(m))
            if not np.isfinite(u).all():
                status = "blowup"; break
        while snap_left and tt >= snap_left[0] - 1e-9:
            snaps[snap_left.pop(0)] = u.copy()
        if t == steps:
            break
        if stepper == "euler":
            un = u + dt * (Du * lap(u, inv_dx2) + lam * u - u**3 - k3 * v - k4 * w + k1)
            if noise > 0:
                un += noise * sq * rng.standard_normal(u.shape)
            v = v + dt * ((u - v) / tau + Dv * lap(v, inv_dx2))
            w = w + dt * ((u - w) / theta + Dw * lap(w, inv_dx2))
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
    return dict(status=status, N=N, dx=dx, dt=dt, thr=thr, u0=u0,
                t=np.array(ts), com=np.array(coms) if coms else np.zeros((0, 2)),
                area=np.array(areas), ncomp=np.array(ncs, dtype=int),
                fields=(u, v, w), snaps=snaps)
