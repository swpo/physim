"""metrics.py — LOCKED metric definitions for M1 motility certification.
Locked BEFORE certification runs (2026-02-18). Any change after this point
invalidates certified results and must be logged in SUMMARY.md.

Conventions:
- All lengths in PHYSICAL units (dx-independent), times in tu.
- A "run" is the dict returned by sim.run (track: t, com (unwrapped), area, ncomp).

CERTIFICATION PROTOCOL (locked):
- Operating line M1: lam=2, k1=-0.7, k3=1, k4=1.5, theta=0.7, Du=1, Dv=0.65,
  Dw=20 (only Dv differs from M0), L_phys=96, periodic.
- Reference discretization: dx=0.5, stepper=imexfft, dt=0.02.
- Seeded kick: v,w Gaussian bumps (kick_av=0.6*A, kick_d=2.0) displaced
  opposite the desired direction; certification kick angle = 30 deg.
- Speed curve runs: T=900 tu (T=1800 for the two points nearest onset);
  measure window = last WIN=300 tu; steadiness = compare with previous
  300-tu window.
- Traveling: c_med >= C_TRAVEL and straightness >= STRAIGHT_MIN and nc_max == 1.
- Stationary: c_med < C_STAT and nc_max == 1.
- Unpinning (both must hold):
  (a) speed grid-convergence: |c(dx/2) - c(dx)| / c(dx/2) < 0.10 at fixed
      physical params (tau=5.0 point), same dt, same T-window protocol;
  (b) direction isotropy: over >= 8 non-lattice kick angles the final travel
      angle follows the kick (circular |diff| median <= 5 deg, max <= 15 deg),
      AND over >= 8 noise-seeded runs (no kick, noise=2e-3) the final angles
      folded into [0,90) have <= 3/8 within 5 deg of {0, 45, 90}.
"""
import numpy as np

C_TRAVEL = 5e-3      # phys units / tu; above = traveling
C_STAT = 2e-3        # below = stationary
STRAIGHT_MIN = 0.90  # net/path over the window
WIN = 300.0          # tu, certification measurement window
STEADY_REL = 0.07    # |c_prev - c_last| / c_last must be below this
ANG_FOLLOW_MED = 5.0     # deg
ANG_FOLLOW_MAX = 15.0    # deg
LATTICE_TOL = 5.0        # deg, distance to {0,45,90} that counts as "on-lattice"
GRID_CONV_REL = 0.10


def window_metrics(r, t0, t1):
    """Speed/direction/shape metrics on track points with t in [t0, t1]."""
    t = r["t"]; c = r["com"]
    sel = (t >= t0 - 1e-9) & (t <= t1 + 1e-9)
    if sel.sum() < 5 or len(c) < 5:
        return dict(ok=False)
    tt = t[sel]; cc = c[sel]
    d = np.diff(cc, axis=0); dts = np.diff(tt)
    step_speed = np.hypot(d[:, 0], d[:, 1]) / dts
    net = cc[-1] - cc[0]
    path = float(np.hypot(d[:, 0], d[:, 1]).sum())
    straight = float(np.hypot(*net) / path) if path > 1e-12 else 0.0
    ang = float(np.degrees(np.arctan2(net[1], net[0])))  # atan2(y, x)
    n0 = np.searchsorted(t, t0 - 1e-9)
    n1 = np.searchsorted(t, t1 + 1e-9)
    nc_max = int(r["ncomp"][n0:n1].max()) if len(r["ncomp"]) > n0 else -1
    area_med = float(np.median(r["area"][n0:n1])) if len(r["area"]) > n0 else 0.0
    return dict(ok=True, c_med=float(np.median(step_speed)),
                c_mean=float(step_speed.mean()), straight=straight,
                ang=ang, nc_max=nc_max, area_med=area_med)


def certify_point(r, T):
    """Locked per-run measurement: last WIN window + steadiness vs previous."""
    if r["status"] != "ok":
        return dict(cls=r["status"])
    last = window_metrics(r, T - WIN, T)
    prev = window_metrics(r, T - 2 * WIN, T - WIN)
    if not last.get("ok"):
        return dict(cls="short")
    steady = None
    if prev.get("ok") and last["c_med"] > 0:
        steady = abs(prev["c_med"] - last["c_med"]) / max(last["c_med"], 1e-12)
    if last["nc_max"] > 1:
        cls = "split"
    elif last["c_med"] >= C_TRAVEL and last["straight"] >= STRAIGHT_MIN:
        cls = "traveling"
    elif last["c_med"] < C_STAT:
        cls = "stationary"
    else:
        cls = "marginal"
    return dict(cls=cls, steady_rel=steady, **{k: last[k] for k in
                ("c_med", "c_mean", "straight", "ang", "nc_max", "area_med")})


def circ_diff_deg(a, b):
    """Smallest signed angular difference a-b in degrees."""
    return (a - b + 180.0) % 360.0 - 180.0


def fold_lattice_deg(a):
    """Fold an angle into [0, 90) (lattice symmetry of the square grid)."""
    return float(np.mod(a, 90.0))


def dist_to_lattice_deg(a):
    f = fold_lattice_deg(a)
    return float(min(abs(f - 0.0), abs(f - 45.0), abs(f - 90.0)))


def curve_verdict(taus, cs):
    """Gate B2 curve check on traveling-branch points (locked):
    monotone: no decrease worse than 2% of max(c);
    smooth: quadratic fit in tau has R2 >= 0.95."""
    taus = np.asarray(taus, float); cs = np.asarray(cs, float)
    order = np.argsort(taus); taus, cs = taus[order], cs[order]
    dec = np.diff(cs).min() if len(cs) > 1 else 0.0
    monotone = bool(dec >= -0.02 * cs.max())
    if len(cs) >= 4:
        co = np.polyfit(taus, cs, 2)
        pred = np.polyval(co, taus)
        ss = 1 - ((cs - pred) ** 2).sum() / max(((cs - cs.mean()) ** 2).sum(), 1e-15)
        smooth = bool(ss >= 0.95); r2 = float(ss)
    else:
        smooth = False; r2 = 0.0
    return dict(monotone=monotone, smooth=smooth, quad_r2=r2, n=len(cs))


def sqrt_law_fit(taus, cs):
    """Fit c^2 = a*(tau - tau_c) on the traveling branch (drift bifurcation
    normal form). Returns tau_c, a, r2 of the linear fit in c^2."""
    taus = np.asarray(taus, float); cs = np.asarray(cs, float)
    A = np.vstack([taus, np.ones_like(taus)]).T
    (m, b), *_ = np.linalg.lstsq(A, cs ** 2, rcond=None)
    pred = A @ np.array([m, b])
    y = cs ** 2
    r2 = 1 - ((y - pred) ** 2).sum() / max(((y - y.mean()) ** 2).sum(), 1e-15)
    if m <= 0:
        return dict(tau_c=None, a=float(m), r2=float(r2))
    return dict(tau_c=float(-b / m), a=float(m), r2=float(r2))


def unpin_speed_verdict(c_coarse, c_fine):
    rel = abs(c_fine - c_coarse) / max(abs(c_fine), 1e-12)
    return dict(rel_change=float(rel), passed=bool(rel < GRID_CONV_REL))


def angle_follow_verdict(kick_angles, final_angles):
    d = [abs(circ_diff_deg(f, k)) for k, f in zip(kick_angles, final_angles)]
    d = np.array(d)
    return dict(median_dev=float(np.median(d)), max_dev=float(d.max()),
                passed=bool(np.median(d) <= ANG_FOLLOW_MED and d.max() <= ANG_FOLLOW_MAX),
                devs=[float(x) for x in d])


def lattice_cluster_verdict(final_angles, n_max_on_lattice=3):
    dists = [dist_to_lattice_deg(a) for a in final_angles]
    on = sum(1 for x in dists if x <= LATTICE_TOL)
    return dict(n=len(final_angles), n_on_lattice=int(on),
                dists=[round(x, 2) for x in dists],
                passed=bool(on <= n_max_on_lattice))
