"""metrics.py — LOCKED measurement conventions for M4 composite-dynamics certification.
LOCKED 2026-02-18 BEFORE certification runs. Any later change invalidates the cert.

CERTIFIED MODE TARGET: (a) TRAVELING BOND — wake-locked tandem pair.

Param family (the M4 resolution of the round-1 binding/motility tension):
  Static structure depends on (tau,Dv) only through A = tau*Dv (steady v-eq:
  u = v - tau*Dv lap v). Family: A = 4.0 FIXED (static bond exists: M2 certified
  the d*~15.5 bond at tau=2.0,Dv=2.0 i.e. A=4), dial = tau with Dv = 4/tau.
  All other params M0: lam=2, k1=-0.7, k3=1, k4=1.5, theta=0.7, Du=1, Dw=20.

Discretization (motility conventions): IMEX-FFT stepper, dx=0.5, dt=0.02,
L=96 periodic. Integrator per experiment documented in results.json.

IC (binding stamp method): A=4-native stamp (single blob relaxed 2000 tu at
Dv=1.6,tau=2.5 on L=64 dx=0.5, deviations du,dv,dw) pasted at two positions
d0=15.0 apart along an axis at angle phi; kick = v,w stamp components pasted
displaced kick_d=0.5 px opposite the kick direction (per-blob). Curve runs:
both blobs kicked ALONG the pair axis (co_along), phi=0.

Measurements (blob tracking: u > u0 + 0.45*(sqrt(lam)-u0), periodic components,
circular-mean centroids, greedy identity matching, unwrapped physical coords):
- c_pair: median step speed of the pair COM over the last WIN=300 tu; steadiness:
  |c(prev win) - c(last win)| / c(last win) < 0.07.
- bond length under motion: sep mean/std over last WIN; STABLE if std < 0.1 px
  and ncomp==2 at every record after t=200 (transient).
- TRAVELING BOND at a point: ncomp==2 throughout (post-transient), c_pair >= 5e-3,
  COM straightness >= 0.90, sep_mean in [13,17] (first tandem shell; second shell
  [24,27] documented separately), sep_std < 0.1.
- Curve gate (>=5 pts): c_pair vs tau monotone (no decrease worse than 2% of max)
  + sqrt-law fit c^2 = a*(tau - tau_c) with r2 >= 0.95 on the traveling branch.
- OUT-OF-WINDOW AUDIT (round-1 style): fit sqrt law on tau <= 6.0 branch points,
  predict c(6.1); PASS if |pred - meas| / meas <= 0.15.
- Isotropy spot check (4 axis angles {30, 57, 120, 203} deg at tau=6.0): final
  COM motion angle within 5 deg of the kick/axis angle; no lattice clustering.
- Seeds (>=3): tau=6.0, sigma=2e-3, NO kick, d0=15.0, seeds {1,2,3}: spontaneous
  tandem: all lock to sep 14.78 +- 0.15 and |c_pair - 0.1407| / 0.1407 <= 0.10.
  (Direction free — symmetric IC + noise; also serves as noise-robustness.)
- B1 composite: tau=6.0, sigma=2e-3, T >= 3200 tu: ncomp==2 at every record
  post-transient, sep stable band [14.4, 15.2], pair still traveling at end.
- Single-blob reference on the same grid (same stamp, one blob, kick kd=0.5):
  c_single(tau) measured with identical windows — for the composite-vs-single
  contrast (pair onset BELOW single onset; c_pair > c_single above).
- Unpinning one-off: c_pair(dx=0.5) vs c_pair(dx=0.25) at tau=6.0, rel diff < 0.10.

Constants: WIN=300.0; C_TRAVEL=5e-3; C_STAT=2e-3; STRAIGHT_MIN=0.90;
SEP_STD_MAX=0.1; SHELL1=(13.0,17.0); SEED_SEP_TOL=0.15; SEED_C_RELTOL=0.10;
OOW_RELTOL=0.15; ANG_TOL=5.0 deg; GRID_CONV_REL=0.10.
"""
import numpy as np

WIN = 300.0
C_TRAVEL = 5e-3
C_STAT = 2e-3
STRAIGHT_MIN = 0.90
SEP_STD_MAX = 0.1
SHELL1 = (13.0, 17.0)
SHELL2 = (24.0, 27.0)
SEED_SEP_TOL = 0.15
SEED_C_RELTOL = 0.10
OOW_RELTOL = 0.15
ANG_TOL = 5.0
GRID_CONV_REL = 0.10
TRANSIENT = 200.0


def pair_series(r):
    """t, sep, unwrapped bond angle (rad), COM (n x 2) for records with ncomp==2."""
    ts, seps, angs, coms = [], [], [], []
    for i, tt in enumerate(r["t"]):
        if i < len(r["pos"]) and r["ncomp"][i] == 2:
            P = r["pos"][i]
            d = P[0] - P[1]
            ts.append(tt)
            seps.append(float(np.hypot(*d)))
            angs.append(float(np.arctan2(d[0], d[1])))
            coms.append((P[0] + P[1]) / 2)
    return (np.array(ts), np.array(seps),
            np.unwrap(np.array(angs)) if len(angs) else np.array([]),
            np.array(coms))


def window(ts, xs, t0, t1):
    sel = (ts >= t0 - 1e-9) & (ts <= t1 + 1e-9)
    return ts[sel], xs[sel]


def com_speed(ts, coms, t0, t1):
    sel = (ts >= t0 - 1e-9) & (ts <= t1 + 1e-9)
    tt, cc = ts[sel], coms[sel]
    if len(tt) < 4:
        return None
    d = np.diff(cc, axis=0)
    dts = np.diff(tt)
    sp = np.hypot(d[:, 0], d[:, 1]) / dts
    net = cc[-1] - cc[0]
    path = float(np.hypot(d[:, 0], d[:, 1]).sum())
    return dict(c_med=float(np.median(sp)),
                straight=float(np.hypot(*net) / path) if path > 1e-12 else 0.0,
                ang=float(np.degrees(np.arctan2(net[0], net[1]))))  # pos is (y,x)


def certify_travel_bond(r, T):
    """Locked per-run verdict for a pair run of length T."""
    out = dict(cls="fail")
    if r["status"] != "ok":
        out["cls"] = r["status"]
        return out
    nc = r["ncomp"]
    tarr = r["t"]
    post = tarr >= TRANSIENT
    if (nc[post] != 2).any():
        out["cls"] = "split" if nc[post].max() > 2 else "merged_or_died"
        out["ncomp_max"] = int(nc.max())
        return out
    ts, seps, angs, coms = pair_series(r)
    last = com_speed(ts, coms, T - WIN, T)
    prev = com_speed(ts, coms, T - 2 * WIN, T - WIN)
    _, sep_w = window(ts, seps, T - WIN, T)
    out.update(c_pair=last["c_med"], straight=last["straight"], ang=last["ang"],
               sep_mean=float(sep_w.mean()), sep_std=float(sep_w.std()),
               steady_rel=abs(prev["c_med"] - last["c_med"]) / max(last["c_med"], 1e-12))
    shell = SHELL1[0] <= out["sep_mean"] <= SHELL1[1]
    shell2 = SHELL2[0] <= out["sep_mean"] <= SHELL2[1]
    if (last["c_med"] >= C_TRAVEL and last["straight"] >= STRAIGHT_MIN
            and out["sep_std"] < SEP_STD_MAX and (shell or shell2)
            and out["steady_rel"] < 0.07):
        out["cls"] = "travel_bond" if shell else "travel_bond_shell2"
    elif last["c_med"] < C_STAT and (shell or shell2):
        out["cls"] = "static_bond"
    else:
        out["cls"] = "other"
    return out


def sqrt_law_fit(taus, cs):
    taus = np.asarray(taus, float)
    cs = np.asarray(cs, float)
    A = np.vstack([taus, np.ones_like(taus)]).T
    (m, b), *_ = np.linalg.lstsq(A, cs ** 2, rcond=None)
    pred = A @ np.array([m, b])
    y = cs ** 2
    r2 = 1 - ((y - pred) ** 2).sum() / max(((y - y.mean()) ** 2).sum(), 1e-15)
    if m <= 0:
        return dict(tau_c=None, a=float(m), r2=float(r2))
    return dict(tau_c=float(-b / m), a=float(m), r2=float(r2))


def curve_verdict(taus, cs):
    taus = np.asarray(taus, float)
    cs = np.asarray(cs, float)
    order = np.argsort(taus)
    taus, cs = taus[order], cs[order]
    dec = np.diff(cs).min() if len(cs) > 1 else 0.0
    monotone = bool(dec >= -0.02 * cs.max())
    fit = sqrt_law_fit(taus, cs)
    return dict(monotone=monotone, n=len(cs), **fit)


def circ_diff_deg(a, b):
    return (a - b + 180.0) % 360.0 - 180.0
