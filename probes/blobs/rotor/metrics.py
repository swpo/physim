"""metrics.py — LOCKED measurement conventions for M7 ROTOR certification.
LOCKED 2026-02-19 BEFORE certification runs. Any later change invalidates the cert.

TARGET: RT1 HETERODIMER ROTOR — xv architecture (6 fields: private u_i,v_i,w_i,
cross-v coupling eta), A_i = tau_i*Dv_i = 4 both species, S anchored at tau2=2.5,
M dialed by tau1. Reference point: eta12=eta21=0.1, d0=8, tau1=5.7.

Order parameter: bond angle phi(t) = atan2(dy, dx) of the M-S vector (M=species-1
identity 0, S=species-2 identity 0), unwrapped. omega = dphi/dt.

Per-run measurements (records with ncomp1==ncomp2==1):
- omega_last: linear fit of phi over the last WIN=300 tu.
- steady: |omega(prev WIN) - omega(last WIN)| / |omega(last)| < 0.07 (M4 conv).
- t_lock: earliest record time such that ALL subsequent windowed omegas (stride
  WIN/2) are within 7% of omega_last; revs_locked = |phi(T)-phi(t_lock)|/2pi.
- sep_mean/std over last WIN; anchor check: S net drift over locked phase and
  S rms about its locked-phase mean.

RT1 POINT PASS (rotor attractor at a parameter point):
  status ok; nc1==nc2==1 at every record post-TRANSIENT=100tu; sep_std < 0.1;
  |omega_last| >= OMEGA_MIN = 2e-3 rad/tu (20x M4's translation-lock noise 1e-4);
  steady; revs_locked >= 3.0; anchor: S_net < 2.0 px and S_rms < 1.5 px.

RT1 CERT (the attractor claim):
- BASIN: from the static-bond IC, kick M with kd=0.5 at tangential 90 deg and
  misaligned 90+-20 deg (70, 110): all 3 reach RT1 POINT PASS with |omega_last|
  within 10% of each other (sign free — CW/CCW degeneracy is symmetry breaking).
- SEEDS: 3 noise seeds sigma=2e-3, NO kick: spontaneous rotation, RT1 POINT PASS,
  |omega| within 10% of the noiseless reference; signs recorded.
- DIAL: omega(tau1) at >= 4 traveling points, |omega| monotone (no decrease
  worse than 2% of max); sqrt-law fit omega^2 = a*(tau1 - tau_rot); report r2
  (gate: monotone + fit r2 >= 0.90 on the rotating branch).
- GRID: |omega(dx=0.25) - omega(dx=0.5)| / |omega(dx=0.5)| < 0.10 at one point.

RT2 CROSS-BOND (statics, tau1=tau2=2.5 — statics depend only on A=4):
- d*: two-sided convergence (from d0 <= 6 and d0 >= 12) to within 0.3 px band;
- basin: all d0 in [5, 14] converge to d* (no second minimum claimed unless seen);
- escape mini-test: rotor at working point under sigma in {0.01, 0.02, 0.04},
  T >= 2000: bond survives (nc1==nc2==1, sep < 12) or escape sigma documented.

Constants: WIN=300.0; OMEGA_MIN=2e-3; STEADY_REL=0.07; SEP_STD_MAX=0.1;
REVS_MIN=3.0; ANCHOR_NET_MAX=2.0; ANCHOR_RMS_MAX=1.5; BASIN_RELTOL=0.10;
SEED_RELTOL=0.10; GRID_RELTOL=0.10; TRANSIENT=100.0; D_TWOSIDED_BAND=0.3.
"""
import numpy as np

WIN = 300.0
OMEGA_MIN = 2e-3
STEADY_REL = 0.07
SEP_STD_MAX = 0.1
REVS_MIN = 3.0
ANCHOR_NET_MAX = 2.0
ANCHOR_RMS_MAX = 1.5
BASIN_RELTOL = 0.10
SEED_RELTOL = 0.10
GRID_RELTOL = 0.10
TRANSIENT = 100.0
D_TWOSIDED_BAND = 0.3


def rotor_series(t, pos1, pos2, ncomp1, ncomp2):
    """t, sep, unwrapped bond angle, M track, S track (records w/ nc1==nc2==1)."""
    ts, seps, angs, Ms, Ss = [], [], [], [], []
    for i in range(len(t)):
        if ncomp1[i] == 1 and ncomp2[i] == 1 and len(pos1[i]) and len(pos2[i]):
            m, s = pos1[i][0], pos2[i][0]
            d = m - s
            ts.append(t[i]); seps.append(float(np.hypot(*d)))
            angs.append(float(np.arctan2(d[0], d[1])))
            Ms.append(m); Ss.append(s)
    return (np.array(ts), np.array(seps),
            np.unwrap(np.array(angs)) if len(angs) else np.array([]),
            np.array(Ms) if Ms else np.zeros((0, 2)),
            np.array(Ss) if Ss else np.zeros((0, 2)))


def win_slope(ts, ys, t0, t1):
    m = (ts >= t0 - 1e-9) & (ts <= t1 + 1e-9)
    if m.sum() < 3:
        return None
    return float(np.polyfit(ts[m], ys[m], 1)[0])


def rotor_verdict(t, pos1, pos2, ncomp1, ncomp2, T):
    """Locked per-run RT1 point verdict."""
    out = dict(cls="fail")
    ts, seps, angs, Ms, Ss = rotor_series(t, pos1, pos2, ncomp1, ncomp2)
    if len(ts) < 10:
        out["cls"] = "no_series"
        return out
    post = t >= TRANSIENT
    n1 = np.asarray(ncomp1)[post]; n2 = np.asarray(ncomp2)[post]
    if (n1 != 1).any() or (n2 != 1).any():
        out["cls"] = "census_change"
        return out
    Tend = ts[-1]
    om_last = win_slope(ts, angs, Tend - WIN, Tend)
    om_prev = win_slope(ts, angs, Tend - 2 * WIN, Tend - WIN)
    m = ts >= Tend - WIN
    out.update(omega_last=om_last, sep_mean=float(seps[m].mean()),
               sep_std=float(seps[m].std()),
               steady_rel=(abs(om_prev - om_last) / max(abs(om_last), 1e-12)
                           if om_prev is not None and om_last is not None else None))
    # t_lock scan
    t_lock = None
    if om_last is not None and abs(om_last) > 0:
        starts = np.arange(TRANSIENT, Tend - WIN + 1e-9, WIN / 2)
        oms = [(s, win_slope(ts, angs, s, s + WIN)) for s in starts]
        ok_from = None
        for i, (s, om) in enumerate(oms):
            if om is None or abs(om - om_last) > 0.07 * abs(om_last):
                ok_from = None
            elif ok_from is None:
                ok_from = s
        t_lock = ok_from
    if t_lock is not None:
        sel = ts >= t_lock
        out["t_lock"] = float(t_lock)
        out["revs_locked"] = float(abs(angs[-1] - angs[sel][0]) / (2 * np.pi))
        Sl = Ss[sel]
        out["S_net"] = float(np.hypot(*(Sl[-1] - Sl[0])))
        out["S_rms"] = float(np.hypot(*(Sl - Sl.mean(0)).T.reshape(2, -1)).max())
        out["orbit_R"] = float(out["sep_mean"])
    if (om_last is not None and abs(om_last) >= OMEGA_MIN
            and out.get("steady_rel") is not None and out["steady_rel"] < STEADY_REL
            and out["sep_std"] < SEP_STD_MAX
            and out.get("revs_locked", 0.0) >= REVS_MIN
            and out.get("S_net", 99.0) < ANCHOR_NET_MAX
            and out.get("S_rms", 99.0) < ANCHOR_RMS_MAX):
        out["cls"] = "rotor"
    elif om_last is not None and abs(om_last) < OMEGA_MIN:
        # static or translating? use M speed
        d = np.diff(Ms[m], axis=0); dt = np.diff(ts[m])
        cM = float(np.median(np.hypot(d[:, 0], d[:, 1]) / dt)) if len(dt) else 0.0
        out["c_M_last"] = cM
        out["cls"] = "translator" if cM >= 5e-3 else "static"
    else:
        out["cls"] = "unsteady"
    return out


def sqrt_law_fit(xs, oms):
    xs = np.asarray(xs, float); oms = np.abs(np.asarray(oms, float))
    A = np.vstack([xs, np.ones_like(xs)]).T
    (mm, bb), *_ = np.linalg.lstsq(A, oms ** 2, rcond=None)
    pred = A @ np.array([mm, bb])
    y = oms ** 2
    r2 = 1 - ((y - pred) ** 2).sum() / max(((y - y.mean()) ** 2).sum(), 1e-15)
    return dict(a=float(mm), x_c=(float(-bb / mm) if mm > 0 else None), r2=float(r2))
