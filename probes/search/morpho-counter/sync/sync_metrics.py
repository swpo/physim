
"""sync_metrics -- L4 (relative phase) analysis for coupled counters.

Phase construction: each ring's count n(t) is reduced to its dominant 2-level
square wave; UP-flip times t_k define cycle phase phi(t) = 2*pi*(k + frac)
by piecewise-linear interpolation. L4 variable Delta(t) = phi1 - phi2.
  locked (1:1): Delta bounded, net winding < 2*pi over window
  slip: Delta winds; slip times = crossings of 2*pi*m; T_slip = median gap.
Rotation number rho = winding(phi1)/winding(phi2).
"""
import numpy as np


def two_level(t, n):
    vals, counts = np.unique(n, return_counts=True)
    order = np.argsort(-counts)
    if len(vals) < 2:
        return None
    dom = np.sort(vals[order[:2]])
    lev = (n >= dom.mean()).astype(int)
    return lev, dom


def up_flips(t, lev):
    ch = np.where(np.diff(lev) == 1)[0]
    return t[ch + 1]


def phase_series(t, ups):
    """phi(t)/2pi with linear interpolation between up-flips (nan outside)."""
    if len(ups) < 2:
        return None
    k = np.arange(len(ups), dtype=float)
    phi = np.interp(t, ups, k, left=np.nan, right=np.nan)
    return phi


def l4_analysis(t, n1, n2, t_cut=2000.0):
    m = t >= t_cut
    t = t[m]; n1 = n1[m]; n2 = n2[m]
    o1, o2 = two_level(t, n1), two_level(t, n2)
    if o1 is None or o2 is None:
        return {"status": "no_two_level"}
    l1, dom1 = o1; l2, dom2 = o2
    u1, u2 = up_flips(t, l1), up_flips(t, l2)
    if len(u1) < 3 or len(u2) < 3:
        return {"status": "too_few_cycles", "cyc1": len(u1), "cyc2": len(u2)}
    p1, p2 = phase_series(t, u1), phase_series(t, u2)
    ok = ~(np.isnan(p1) | np.isnan(p2))
    if ok.sum() < 50:
        return {"status": "no_overlap"}
    tt, q1, q2 = t[ok], p1[ok], p2[ok]
    delta = q1 - q2                      # in cycles (1.0 = 2*pi)
    wind1 = q1[-1] - q1[0]
    wind2 = q2[-1] - q2[0]
    rho = wind1 / max(wind2, 1e-9)
    net = delta[-1] - delta[0]
    exc = np.abs(delta - np.median(delta)).max()
    # slips: HYSTERETIC winding counter (immune to wobble around a level)
    T1 = np.median(np.diff(u1)); T2 = np.median(np.diff(u2))
    ref = delta[0]
    slips = []
    for i in range(len(delta)):
        if delta[i] - ref >= 1.0:
            slips.append(tt[i]); ref += 1.0
        elif delta[i] - ref <= -1.0:
            slips.append(tt[i]); ref -= 1.0
    slips = np.array(slips)
    T_slip_med = float(np.median(np.diff(slips))) if len(slips) >= 2 else None
    span = tt[-1] - tt[0]
    wind_rate = abs(net) / span          # slips per unit time (asymptotic)
    T_slip_rate = float(1.0 / wind_rate) if wind_rate > 1e-9 else None
    locked = bool(len(slips) == 0 and exc < 1.0)
    return {"status": "ok", "T1": float(T1), "T2": float(T2),
            "cyc1": int(len(u1) - 1), "cyc2": int(len(u2) - 1),
            "rho": float(rho), "net_wind": float(net), "max_exc": float(exc),
            "n_slips": int(len(slips)), "T_slip": T_slip_med,
            "T_slip_rate": T_slip_rate,
            "span": float(span), "locked": locked,
            "dom1": dom1.tolist(), "dom2": dom2.tolist(),
            "delta_t": tt, "delta": delta}


def counting_alive(t, n, t_cut=2000.0):
    """Sanity: ring still a healthy 2-level counter (frac2 >= 0.9, flips >= 4)."""
    m = t >= t_cut
    n = n[m]
    vals, counts = np.unique(n, return_counts=True)
    order = np.argsort(-counts)
    frac2 = counts[order[:2]].sum() / counts.sum() if len(vals) >= 2 else 1.0
    o = two_level(t[m], n)
    if o is None:
        return {"alive": False, "frac2": float(frac2), "flips": 0}
    flips = int((np.diff(o[0]) != 0).sum())
    return {"alive": bool(frac2 >= 0.9 and flips >= 4),
            "frac2": float(frac2), "flips": flips}
