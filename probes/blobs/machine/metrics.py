"""metrics.py — M5 MACHINE locked measurement module.

LOCKED 2026-02-19 BEFORE any certification run (control anchors C0-C7 and the
certification battery are all scored through these definitions; post-cert edits
invalidate the cert).

WORLD (declared): single-species A=4 family (M4 conventions), tau=5.70 working
point (pair-only drift zone), IMEX-FFT dx=0.5 dt=0.02, L=96 periodic, isok load
field b(x) = saw(eps, frac, n_teeth=1): k1->k1+u0*b, k4->k4+b (u0=-0.70354).

DIRECTIONS: DOWNSTREAM := the sign of a lone parked blob's drift velocity on the
saw's rising branch (measured in C4, expected -x i.e. down-b, the vvw isod
analogue). UPSTREAM := opposite. All gates below are written for downstream=-x,
upstream=+x; if C4 measures the opposite sign every x-coordinate flips once,
BEFORE certification (documented here as the single allowed re-orientation).

MACHINE (design (a) TUG, train-growth, torus circulation): locomotive = tandem
pair kicked upstream at t=0 (IC); >=3 cargo blobs parked (no kick) on the rising
branch; every structure evolves by field physics only. A CYCLE = one PICKUP:
the locomotive/train reaches a parked cargo head-on, the cargo wake-locks into
the train (M4 shell physics), and is carried upstream thereafter.

LOCKED ESTIMATORS
- Records: rec_tu=5 tu tracks, unwrapped positions (runjob padded npz).
- v_tail(k): LSQ slope of x_k(t) over the last WIN=300 tu.
- PICKUP time t_pu(k) of cargo k (parked at x_k(0)):
    first record time t* with  x_k(t*) - x_k(0) >= PU_DX   (net upstream advance)
    AND mean forward velocity over [t*, t*+PU_HOLD] >= C_TRAVEL.
  (Parked cargo can only advance upstream by being pushed/locked by the train:
   drift moves it downstream, C4/null control quantifies.)
- CYCLE COMPLETED for cargo k: t_pu(k) exists AND cargo is carried upstream
    x_k(T_end) - x_k(t_pu) >= CARRY_MIN
  AND at T_end the cargo is train-bound: distance to nearest other blob in
    SHELL_BAND (first/second wake shells).
- N_CYCLES = number of cargoes with a completed cycle.
- NET_UP = sum over ALL seeded cargoes of (x_k(T_end) - x_k(0))  [honest total:
  stragglers/losses count against the machine].
- EFFICIENCY (controller-fixed): eff = NET_UP / (|v_drift(eps)| * T_end * n_cargo)
  where v_drift(eps) is the C4-measured lone-blob drift law at the working eps.
  Do-nothing baseline displacement = -|v_drift|*T*n_cargo; eff is the ratio of
  achieved upstream displacement to the magnitude of the do-nothing loss.
- B1 STRUCTURES ALIVE: ncomp == n_seeded at EVERY record after TRANSIENT=200 tu
  (no death, no merge, no split/replication). Wake-locked members stay separate
  components by construction of the tandem physics.
- B6 MACHINE PASS: N_CYCLES >= 3 AND NET_UP >= 30 px AND B1 holds AND the paired
  NULL (same track, same cargoes, NO locomotive) shows no cargo advancing:
  every null cargo has x_k(T)-x_k(0) <= NULL_MAX_UP (drift should make it < 0).
- SEEDS: 3 noise seeds (sigma=2e-3, M4 cert convention) at the working point
  + 1 jitter draw (cargo park positions jittered by U(-2,+2) px, new seed).
  PASS requires N_CYCLES >= 3 and NET_UP >= 30 in ALL 3 seed runs; jitter run
  reported (spot check, pass/fail documented but not gating).

CONSTANTS
"""
import numpy as np

LOCK = "2026-02-19 machine searcher pre-certification lock"

WIN = 300.0          # tu, tail window for velocities
TRANSIENT = 200.0    # tu, stamp relaxation transient (M4 convention)
C_TRAVEL = 5e-3      # px/tu (M4 travel floor)
PU_DX = 2.0          # px upstream advance that flags a pickup
PU_HOLD = 100.0      # tu the post-pickup velocity must average >= C_TRAVEL
CARRY_MIN = 10.0     # px carried upstream after pickup to complete a cycle
SHELL_BAND = (12.0, 32.0)   # px, train-membership distance (shells 14.78/25.68)
NULL_MAX_UP = 2.0    # px, max allowed "upstream" advance of a null cargo
NET_UP_GATE = 30.0   # px, B6 total
N_CYC_GATE = 3


def _fit(t, z):
    A = np.vstack([t, np.ones_like(t)]).T
    coef, *_ = np.linalg.lstsq(A, z, rcond=None)
    zhat = A @ coef
    ss = np.sum((z - z.mean()) ** 2)
    r2 = 1.0 - (np.sum((z - zhat) ** 2) / ss if ss > 0 else 0.0)
    return float(coef[0]), float(r2)


def v_tail(t, x, win=WIN):
    t = np.asarray(t, float); x = np.asarray(x, float)
    m = (t >= t[-1] - win) & np.isfinite(x)
    if m.sum() < 4:
        return None
    return _fit(t[m], x[m])[0]


def drift_speed(t, x, settle=TRANSIENT):
    """C4 estimator: lone parked blob, LSQ slope of x(t) for t>=settle."""
    t = np.asarray(t, float); x = np.asarray(x, float)
    m = (t >= settle) & np.isfinite(x)
    if m.sum() < 6:
        return dict(verdict="too_few_pts", n=int(m.sum()))
    v, r2 = _fit(t[m], x[m])
    return dict(verdict="ok", v_x=v, r2=r2,
                net_x=float(x[m][-1] - x[m][0]),
                T_obs=float(t[m][-1] - t[m][0]))


# AMENDMENT 2026-02-19 (PRE-CERTIFICATION, before any machine cert run; the
# transport/M4 precedent of documented pre-cert amendments): C4/E5 controls
# showed the lone blob's downstream drift TERMINATES at the saw trough (park),
# so a whole-track LSQ would UNDERSTATE the adversary and inflate efficiency.
# v_drift(eps) for the efficiency baseline is therefore locked as the
# MOVING-SEGMENT fit: LSQ slope of x(t) from t=settle until the first record
# where the blob is within PARK_TOL of its final rest position. This is the
# strongest honest reading of the do-nothing loss rate.
PARK_TOL = 1.0   # px


def drift_speed_moving(t, x, settle=TRANSIENT, park_tol=PARK_TOL):
    t = np.asarray(t, float); x = np.asarray(x, float)
    ok = np.isfinite(x)
    xf = x[ok][-1]
    m = (t >= settle) & ok & (np.abs(x - xf) > park_tol)
    if m.sum() < 6:
        # never moved beyond park_tol: fall back to whole-track estimate
        return drift_speed(t, x, settle=settle) | dict(segment="whole_track")
    v, r2 = _fit(t[m], x[m])
    return dict(verdict="ok", v_x=v, r2=r2, segment="moving",
                net_x=float(x[m][-1] - x[m][0]),
                t_park=float(t[m][-1]),
                T_obs=float(t[m][-1] - t[m][0]))


def pickup_time(t, xk, c_travel=C_TRAVEL, pu_dx=PU_DX, hold=PU_HOLD):
    """First t where cargo has advanced pu_dx upstream AND keeps moving."""
    t = np.asarray(t, float); xk = np.asarray(xk, float)
    x0 = xk[np.isfinite(xk)][0]
    for i in range(len(t)):
        if not np.isfinite(xk[i]) or xk[i] - x0 < pu_dx:
            continue
        j = np.searchsorted(t, t[i] + hold)
        if j >= len(t):
            j = len(t) - 1
        if j <= i:
            return float(t[i])   # end of record; count conservatively
        v = (xk[j] - xk[i]) / (t[j] - t[i])
        if v >= c_travel:
            return float(t[i])
    return None


def machine_verdict(t, P, cargo_idx, loco_idx, ncomp, n_seeded, v_drift_eps,
                    L=96.0):
    """Full locked B6 scoring of one machine run.
    P: (nrec, n_id, 2) padded [y,x] unwrapped; cargo_idx/loco_idx: identity cols.
    v_drift_eps: |v_drift| at the working eps from the C4 law (px/tu)."""
    t = np.asarray(t, float)
    out = dict(n_cargo=len(cargo_idx))
    T_end = float(t[-1])
    out["T_end"] = T_end
    # B1 structures alive
    post = t >= TRANSIENT
    ncomp = np.asarray(ncomp)
    out["b1_alive"] = bool((ncomp[post] == n_seeded).all())
    out["ncomp_min_post"] = int(ncomp[post].min()) if post.any() else None
    out["ncomp_max_post"] = int(ncomp[post].max()) if post.any() else None
    # per-cargo pickup/cycle accounting
    cycles = []
    net_up = 0.0
    for k in cargo_idx:
        xk = P[:, k, 1]
        ok = np.isfinite(xk)
        x0 = float(xk[ok][0]); xT = float(xk[ok][-1])
        dxk = xT - x0
        net_up += dxk
        tpu = pickup_time(t, xk)
        carried = None
        bound_end = None
        if tpu is not None:
            i_pu = int(np.searchsorted(t, tpu))
            carried = float(xk[ok][-1] - xk[i_pu])
            # train-bound at end: min distance to any other tracked blob
            dmin = None
            for j in range(P.shape[1]):
                if j == k or not np.isfinite(P[-1, j, 1]):
                    continue
                d = np.hypot(P[-1, k, 0] - P[-1, j, 0], P[-1, k, 1] - P[-1, j, 1])
                dmin = d if dmin is None else min(dmin, d)
            bound_end = (dmin is not None
                         and SHELL_BAND[0] <= dmin <= SHELL_BAND[1] + 1e-9)
            cycles.append(dict(k=int(k), t_pu=tpu, dx=round(dxk, 2),
                               carried=round(carried, 2),
                               dmin_end=round(float(dmin), 2) if dmin else None,
                               complete=bool(carried >= CARRY_MIN and bound_end)))
        else:
            cycles.append(dict(k=int(k), t_pu=None, dx=round(dxk, 2),
                               complete=False))
    out["cycles"] = cycles
    out["n_cycles"] = sum(1 for c in cycles if c["complete"])
    out["net_up"] = round(net_up, 2)
    denom = abs(v_drift_eps) * T_end * len(cargo_idx)
    out["baseline_loss"] = round(denom, 2)
    out["efficiency"] = round(net_up / denom, 2) if denom > 0 else None
    out["b6_cycles_ok"] = out["n_cycles"] >= N_CYC_GATE
    out["b6_netup_ok"] = bool(net_up >= NET_UP_GATE)
    out["b6_pass"] = bool(out["b6_cycles_ok"] and out["b6_netup_ok"]
                          and out["b1_alive"])
    return out


def null_verdict(t, P, cargo_idx):
    """Paired no-locomotive null: no cargo may advance upstream."""
    t = np.asarray(t, float)
    rows = []
    for k in cargo_idx:
        xk = P[:, k, 1]
        ok = np.isfinite(xk)
        dxk = float(xk[ok][-1] - xk[ok][0])
        rows.append(dict(k=int(k), dx=round(dxk, 3)))
    return dict(cargoes=rows,
                null_ok=all(r["dx"] <= NULL_MAX_UP for r in rows))
