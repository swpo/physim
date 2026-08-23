"""metrics.py — MEMBRANE probe metrics, LOCKED before certification runs.

Phase-5 top-down: closed bounding structures (rings with an inside/outside),
cargo-in-cell. All gates and tolerances fixed HERE, pre-cert (program rule).

Ring conventions:
- Ring of N blobs seeded at radius R0 = d*/(2 sin(pi/N)) about domain center.
- Bond graph: link two blobs if min-image distance <= cut (same-species
  SAME_CUT=21.0 px ~ basin outer edge 19.5 + stretch margin; cross-species
  CROSS_CUT=10.5 px ~ cross d*=8 basin).
- RING CLOSED at a record  <=>  ncomp == N  AND bond graph is the cycle C_N
  (every blob degree exactly 2, single connected cycle of length N).
- CROWDING flag: any same-species pair < CROWD=12 px (inside basin inner wall);
  cross pair < 5.5 px.

GATES (locked):
- G_RING (R1 existence), per (family, N):
    * noiseless run T >= 5000 tu: status ok, ring closed at every record with
      t >= T_TRANS (250 tu), no crowding flag in the final half.
    * working-noise run (sigma = 2e-3) same T, same criteria.
    * radius equilibrated: |R_mean(last 500tu) - R_mean(prev 500tu)| < 0.15 px.
- G_GRID (continuum): dx=0.25 rerun (T >= 1500): ring closed at every t >=
    T_TRANS record AND |R*(0.25) - R*(0.5, same T)| / R* <= 3%.
    (binding's d* itself moved 1.8% on refinement; 3% is the honest band.)
- G_ENCLOSE (R2a): report mean u,v,w inside (disk r < R*-12) vs outside
    (r > R*+12): asymmetry DETECTED if |delta| > 1e-4 (tail scale is ~1e-2,
    numerical floor ~1e-8). Deliver radial profiles (azimuthal average).
- G_BARRIER (R2b): kick/speed probe of wall crossing, cargo = xv species 1,
    membrane = species 2, eta12 > 0. Outcome classes (locked):
      TRANSMIT: cargo min-image radius r_c > R_wall + 6 px at any record
      CAPTURE : final-500tu median r_c in [R_wall-11, R_wall+2] and
                drift |dr_c/dt| < 2e-3 px/tu
      REFLECT : cargo approached r_c >= R_wall-14 then returned to
                r_c < R_wall-14 and neither TRANSMIT nor CAPTURE
      NO_REACH: never approached r_c >= R_wall-14
    Deliverable = outcome + V_eff(x) = -k3*eta12*dv2(x) landscape (k1-units)
    with ridge/gap/well statistics. No pass/fail; the curve is the result.
- G_CARGO (R3): membrane ring + interior cargo, working noise, T >= 3000 tu:
    * both alive: ncomp2 == N and ncomp1 == 1 at every record
    * ring closed at every t >= T_TRANS record
    * cargo confined: r_c(t) < R_wall(t) at every record (never on/past the
      blob circle), where R_wall(t) = membrane R_mean at that record.
- G_PUSH (R4): with mutual eta, motile interior cargo: deliver membrane COM
    displacement + R_mean(t) response vs cargo wall-approach events; compare
    against eta21=0 control. Quantitative report, no pass/fail gate.

Numerics conventions: IMEX-FFT, dx=0.5, dt=0.02, L=96, thr_frac=0.45,
working noise sigma=2e-3 on u-fields, seeds recorded. T_TRANS = 250 tu.
"""
import numpy as np

SAME_CUT = 21.0
CROSS_CUT = 10.5
CROWD_SAME = 12.0
CROWD_CROSS = 5.5
T_TRANS = 250.0
GRID_TOL = 0.03
ENCL_DET = 1e-4
R_EQUIL = 0.15
CAP_DRIFT = 2e-3
WALL_IN = 12.0


def minimg(d, L):
    return (d + L / 2.0) % L - L / 2.0


def circ_centroid(pos, L):
    """Periodic centroid of points pos (n,2) [y,x] via circular mean."""
    ang = 2 * np.pi * np.asarray(pos) / L
    z = np.exp(1j * ang).mean(axis=0)
    return (np.angle(z) % (2 * np.pi)) / (2 * np.pi) * L


def pair_dists(pos, L):
    p = np.asarray(pos)
    n = len(p)
    D = np.zeros((n, n))
    for i in range(n):
        d = minimg(p - p[i], L)
        D[i] = np.hypot(d[:, 0], d[:, 1])
    return D


def is_cycle_CN(pos, L, cut=SAME_CUT):
    """True iff bond graph (dist<=cut) is exactly the cycle C_N."""
    n = len(pos)
    if n < 3:
        return False, None
    D = pair_dists(pos, L)
    A = (D > 0) & (D <= cut)
    deg = A.sum(axis=1)
    if not np.all(deg == 2):
        return False, deg
    # walk the cycle
    seen = {0}
    prev, cur = -1, 0
    for _ in range(n):
        nxt = [j for j in np.nonzero(A[cur])[0] if j != prev]
        if not nxt:
            return False, deg
        prev, cur = cur, int(nxt[0])
        if cur == 0:
            break
        seen.add(cur)
    return (cur == 0 and len(seen) == n), deg


def ring_stats(pos, L):
    """Centroid, radii, angular-ordered neighbor gaps."""
    p = np.asarray(pos, float)
    C = circ_centroid(p, L)
    d = minimg(p - C, L)
    r = np.hypot(d[:, 0], d[:, 1])
    th = np.arctan2(d[:, 0], d[:, 1])
    order = np.argsort(th)
    gaps = []
    for k in range(len(p)):
        i, j = order[k], order[(k + 1) % len(p)]
        dd = minimg(p[j] - p[i], L)
        gaps.append(float(np.hypot(*dd)))
    return dict(C=C.tolist(), R_mean=float(r.mean()), R_std=float(r.std()),
                r=r.tolist(), gap_min=float(np.min(gaps)),
                gap_max=float(np.max(gaps)), gap_mean=float(np.mean(gaps)),
                gaps=gaps, order=order.tolist())


def ring_record_check(pos, L, N, cut=SAME_CUT, crowd=CROWD_SAME):
    """Per-record ring verdict."""
    ok_n = (len(pos) == N)
    cyc, deg = (False, None)
    crowded = False
    st = None
    if ok_n:
        cyc, deg = is_cycle_CN(pos, L, cut)
        D = pair_dists(pos, L)
        iu = np.triu_indices(N, 1)
        crowded = bool((D[iu] < crowd).any())
        st = ring_stats(pos, L)
    return dict(ncomp_ok=ok_n, cycle=bool(cyc), crowded=crowded, stats=st)


def ring_timeseries_verdict(ts, poss, L, N, T_min, cut=SAME_CUT,
                            crowd=CROWD_SAME):
    """Gate G_RING evaluation over a full track. poss: list of (n_i,2)."""
    ts = np.asarray(ts)
    recs = [ring_record_check(p, L, N, cut, crowd) for p in poss]
    post = ts >= T_TRANS
    closed_all = all(r["ncomp_ok"] and r["cycle"]
                     for r, m in zip(recs, post) if m)
    half = ts >= ts[-1] / 2.0
    crowd_late = any(r["crowded"] for r, m in zip(recs, half) if m and r["ncomp_ok"])
    Rm = np.array([r["stats"]["R_mean"] if r["stats"] else np.nan for r in recs])
    # equilibration: compare mean R over last 500tu vs previous 500tu
    m1 = ts >= ts[-1] - 500.0
    m2 = (ts >= ts[-1] - 1000.0) & ~m1
    equil = (abs(np.nanmean(Rm[m1]) - np.nanmean(Rm[m2])) < R_EQUIL
             if m2.any() else False)
    long_enough = ts[-1] >= T_min - 1e-6
    return dict(closed_all_post=bool(closed_all), crowd_late=bool(crowd_late),
                equil=bool(equil), T=float(ts[-1]), long_enough=bool(long_enough),
                R_final=float(np.nanmean(Rm[m1])) if m1.any() else None,
                R_series_summary=dict(
                    first=float(Rm[post][0]) if post.any() else None,
                    last=float(Rm[-1]) if len(Rm) else None,
                    max=float(np.nanmax(Rm)) if len(Rm) else None,
                    min=float(np.nanmin(Rm)) if len(Rm) else None),
                gate=bool(closed_all and not crowd_late and equil and long_enough))


def enclosure_stats(field, u0, C, R_wall, dx, L, w_in=WALL_IN):
    """Mean field deviation inside disk (r < R_wall - w_in) vs outside
    (r > R_wall + w_in), min-image radii about C."""
    n = field.shape[0]
    x = (np.arange(n) + 0.0) * dx
    Y, X = np.meshgrid(x, x, indexing="ij")
    dY = minimg(Y - C[0], L)
    dX = minimg(X - C[1], L)
    r = np.hypot(dY, dX)
    inside = r < (R_wall - w_in)
    outside = r > (R_wall + w_in)
    f = field - u0
    return dict(mean_in=float(f[inside].mean()) if inside.any() else None,
                mean_out=float(f[outside].mean()) if outside.any() else None,
                std_out=float(f[outside].std()) if outside.any() else None,
                n_in=int(inside.sum()), n_out=int(outside.sum()))


def radial_profile(field, u0, C, dx, L, rmax=None, nbin=96):
    n = field.shape[0]
    x = (np.arange(n) + 0.0) * dx
    Y, X = np.meshgrid(x, x, indexing="ij")
    dY = minimg(Y - C[0], L)
    dX = minimg(X - C[1], L)
    r = np.hypot(dY, dX).ravel()
    f = (field - u0).ravel()
    rmax = rmax or L / 2.0
    bins = np.linspace(0, rmax, nbin + 1)
    idx = np.digitize(r, bins) - 1
    prof = np.full(nbin, np.nan)
    for i in range(nbin):
        m = idx == i
        if m.any():
            prof[i] = f[m].mean()
    return 0.5 * (bins[1:] + bins[:-1]), prof


def classify_barrier(ts, r_c, R_wall, T_tail=500.0):
    """LOCKED outcome classes for the wall-crossing probe (see G_BARRIER)."""
    ts = np.asarray(ts); r_c = np.asarray(r_c)
    if (r_c > R_wall + 6.0).any():
        return "TRANSMIT"
    tail = ts >= ts[-1] - T_tail
    med_tail = float(np.median(r_c[tail]))
    if len(ts[tail]) > 3:
        drift = abs(np.polyfit(ts[tail], r_c[tail], 1)[0])
    else:
        drift = np.inf
    if (R_wall - 11.0) <= med_tail <= (R_wall + 2.0) and drift < CAP_DRIFT:
        return "CAPTURE"
    approached = (r_c >= R_wall - 14.0).any()
    if approached:
        i0 = int(np.argmax(r_c >= R_wall - 14.0))
        if (r_c[i0:] < R_wall - 14.0).any():
            return "REFLECT"
        return "AT_WALL"  # approached, still there, not settled/captured
    return "NO_REACH"


# ---------------------------------------------------------------- xv variant
CROWD_SAME_XV = 10.0


def is_cycle_alternating(pos1, pos2, L, cross_cut=CROSS_CUT):
    """Alternating A-B ring check: bipartite cross-bond graph (dist<=cross_cut
    between species only) must be a single 2N cycle with every blob degree 2."""
    p1 = np.asarray(pos1, float); p2 = np.asarray(pos2, float)
    n1, n2 = len(p1), len(p2)
    if n1 != n2 or n1 < 2:
        return False, None
    n = n1 + n2
    P = np.vstack([p1, p2])
    A = np.zeros((n, n), bool)
    for i in range(n1):
        d = minimg(p2 - p1[i], L)
        hit = np.hypot(d[:, 0], d[:, 1]) <= cross_cut
        A[i, n1:][hit] = True
        A[n1:, i][hit] = True
    deg = A.sum(axis=1)
    if not np.all(deg == 2):
        return False, deg
    seen = {0}; prev, cur = -1, 0
    for _ in range(n):
        nxt = [j for j in np.nonzero(A[cur])[0] if j != prev]
        if not nxt:
            return False, deg
        prev, cur = cur, int(nxt[0])
        if cur == 0:
            break
        seen.add(cur)
    return (cur == 0 and len(seen) == n), deg


def xvring_record_check(pos1, pos2, L, Nhalf, cross_cut=CROSS_CUT):
    ok_n = (len(pos1) == Nhalf and len(pos2) == Nhalf)
    cyc, deg = (False, None)
    crowded = False
    st = None
    if ok_n:
        cyc, deg = is_cycle_alternating(pos1, pos2, L, cross_cut)
        for p in (pos1, pos2):
            D = pair_dists(p, L)
            iu = np.triu_indices(len(p), 1)
            if (D[iu] < CROWD_SAME_XV).any():
                crowded = True
        allp = np.vstack([pos1, pos2])
        st = ring_stats(allp, L)
    return dict(ncomp_ok=ok_n, cycle=bool(cyc), crowded=crowded, stats=st)


def xvring_timeseries_verdict(ts, poss1, poss2, L, Nhalf, T_min,
                              cross_cut=CROSS_CUT):
    ts = np.asarray(ts)
    recs = [xvring_record_check(a, b, L, Nhalf, cross_cut)
            for a, b in zip(poss1, poss2)]
    post = ts >= T_TRANS
    closed_all = all(r["ncomp_ok"] and r["cycle"]
                     for r, m in zip(recs, post) if m)
    half = ts >= ts[-1] / 2.0
    crowd_late = any(r["crowded"] for r, m in zip(recs, half) if m and r["ncomp_ok"])
    Rm = np.array([r["stats"]["R_mean"] if r["stats"] else np.nan for r in recs])
    m1 = ts >= ts[-1] - 500.0
    m2 = (ts >= ts[-1] - 1000.0) & ~m1
    equil = (abs(np.nanmean(Rm[m1]) - np.nanmean(Rm[m2])) < R_EQUIL
             if m2.any() else False)
    long_enough = ts[-1] >= T_min - 1e-6
    return dict(closed_all_post=bool(closed_all), crowd_late=bool(crowd_late),
                equil=bool(equil), T=float(ts[-1]), long_enough=bool(long_enough),
                R_final=float(np.nanmean(Rm[m1])) if m1.any() else None,
                gate=bool(closed_all and not crowd_late and equil and long_enough))
