"""metrics.py — machine-v2 delivery metrics. LOCKED 2026-08-21 09:40 EDT
(before any certification battery; prototype physics recs 1-13 informed the
convoy semantics; any later change = documented amendment in results.json).

MACHINE SEMANTICS (from mapped physics, recs 2-13):
The V2a throughput machine is the BULLDOZER CONVOY: on a railed single lane a
passing carrier captures EVERY on-lane parked S within the eta-well footprint
(push-capture blade at ~7.1px ahead of front M, eta21 in [0.05,0.06]); queued
cargoes chain via same-species S-S bonds (~14.5-15.4). Delivery = the whole
chain crosses the dock edge x1 (eta xbox) and releases front-to-back; the
forkchan sorts the released chain off-lane; the empty carrier keeps lapping.
Sequential single-service is IMPOSSIBLE on one railed lane (P1/P1b/P4/P7:
head-on pass at eta>=0.1 splits the cargo; at 0.05-0.08 rails convert the
factory swing-around into permanent blade capture) — mapped, not assumed.

DEFINITIONS (all tracks unwrapped, torus-safe, Tracker convention):
PICKED(k):  cargo k x-speed >= v_tow_min (0.02 px/tu) sustained >= t_sustain
            (150 tu) with net +x advance. (Near-onset cargo parks alone —
            certified parking brake — so sustained drive == machine action.)
            t_pick = start of the sustained window.
RELEASED(k): cargo (unwrapped) x up-crosses x1 while moving, then speed falls
            below v_park (0.005 px/tu) within t_glide <= 900 tu of the
            crossing (inherits factory DK amendment, widened for chain glides).
SORTED(k):  after release: |y - lane_y| >= y_sort (15 px = certified
            interaction footprint) AND parked at end (net move < 1 px over
            final 300 tu) AND alive (area in [20,45], census frozen).
DELIVERED(k) = PICKED & RELEASED & SORTED, in order.
cycle_service(k) = t_sorted(k) - t_pick(k)   [per-cargo service time]
cycle_machine(k) = t_pick(k+1) - t_pick(k)   [inter-pickup interval]
throughput = n_delivered / T_run * 1000 tu
QUEUE INTEGRITY(k): max |r(t)-r(0)| for t < t_pick(k)  < q_tol (1 px).
FLYBY IMMUNITY(k): after t_sorted(k)+300, max displacement from park position
            < q_tol (1 px) through end of run (covers all later carrier laps).
CENSUS: nc1/nc2 frozen at initial counts all run (stop_split catches this).
CIRCUIT (V2c): cargo unwrapped x advances >= L (one full torus lap) through
            >= 2 distinct tow phases (speed>=0.02) separated by a parked phase
            (speed<0.005 for >=200 tu), ending parked. t_circuit = time of
            x(t)-x(0) >= L.
"""
import numpy as np

V_TOW_MIN = 0.02
T_SUSTAIN = 150.0
V_PARK = 0.005
T_GLIDE = 900.0
Y_SORT = 15.0
Q_TOL = 1.0
AREA_LO, AREA_HI = 20.0, 45.0


def speed(t, x, w=5):
    v = np.gradient(x, t)
    if w > 1 and len(v) > 2 * w:
        v = np.convolve(v, np.ones(w) / w, mode="same")
    return v


def picked(t, x):
    """first sustained-drive window start; None if never picked."""
    v = speed(t, x)
    dt = t[1] - t[0] if len(t) > 1 else 1.0
    n = max(int(round(T_SUSTAIN / dt)), 1)
    ok = v >= V_TOW_MIN
    run = 0
    for i, f in enumerate(ok):
        run = run + 1 if f else 0
        if run >= n:
            i0 = i - n + 1
            if x[i] > x[i0]:
                return float(t[i0])
    return None


def released(t, x, x1, t_pick, L, y=None, carriers=None):
    """AMENDED (rec 19, pre-cert): release = dock-edge crossing + glide, OR
    carrier-interaction end (fork-first layouts sort without an x1 crossing).
    carriers: list of (cx, cy) unwrapped carrier tracks. Returns (t_cross, t_release)."""
    m = t >= t_pick
    ti, xi = t[m], x[m]
    vi = speed(t, x)[m]
    # branch 1: unwrapped crossing of x1 + j*L
    j = np.floor((xi[0] - x1) / L) + 1
    edge = x1 + j * L
    cr = np.where((xi[:-1] < edge) & (xi[1:] >= edge))[0]
    if len(cr):
        tc = float(ti[cr[0] + 1])
        g = (ti >= tc) & (ti <= tc + T_GLIDE)
        slow = np.where(np.abs(vi[g]) < V_PARK)[0]
        if len(slow):
            return tc, float(ti[g][slow[0]])
    # branch 2 (amendment): carrier-interaction end
    if carriers is not None and y is not None:
        yi = y[m]
        dmin = np.full(len(ti), 1e9)
        for (kx, ky) in carriers:
            kxm, kym = kx[m], ky[m]
            # torus-aware distance (positions unwrapped; fold into L)
            ddx = np.abs((xi - kxm + L / 2) % L - L / 2)
            ddy = np.abs((yi - kym + L / 2) % L - L / 2)
            dmin = np.minimum(dmin, np.hypot(ddx, ddy))
        dt = ti[1] - ti[0] if len(ti) > 1 else 1.0
        nfree = max(int(round(300.0 / dt)), 1)
        free = dmin > 15.0
        run = 0
        for i, f in enumerate(free):
            run = run + 1 if f else 0
            if run >= nfree:
                t_freed = float(ti[i - nfree + 1])
                g = (ti >= t_freed) & (ti <= t_freed + T_GLIDE)
                slow = np.where(np.abs(vi[g]) < V_PARK)[0]
                if len(slow):
                    return t_freed, float(ti[g][slow[0]])
                return t_freed, None
    return None, None


def sorted_park(t, x, y, t_release, lane_y):
    m = t >= t_release
    ys = np.abs(y[m] - lane_y)
    s = np.where(ys >= Y_SORT)[0]
    if not len(s):
        return None, None, None
    ts = float(t[m][s[0]])
    e = t >= t[-1] - 300.0
    net = float(np.hypot(x[e][-1] - x[e][0], y[e][-1] - y[e][0]))
    return ts, net, bool(net < Q_TOL)


def cargo_delivery(t, x, y, x1, L, lane_y=48.0, areas=None, carriers=None):
    out = dict(t_pick=None, t_cross=None, t_release=None, t_sorted=None,
               end_net300=None, delivered=False)
    out["t_pick"] = picked(t, x)
    if out["t_pick"] is None:
        return out
    out["t_cross"], out["t_release"] = released(t, x, x1, out["t_pick"], L,
                                                y=y, carriers=carriers)
    if out["t_release"] is None:
        return out
    out["t_sorted"], out["end_net300"], parked = sorted_park(t, x, y,
                                                             out["t_release"], lane_y)
    if out["t_sorted"] is None:
        return out
    alive = True
    if areas is not None:
        a = areas[np.isfinite(areas)]
        alive = bool((a >= AREA_LO).all() and (a <= AREA_HI).all())
    out["alive"] = alive
    out["delivered"] = bool(parked and alive)
    return out


def queue_integrity(t, x, y, t_pick):
    m = t < (t_pick if t_pick is not None else t[-1] + 1)
    if m.sum() < 2:
        return dict(max_disp=0.0, ok=True)
    d = np.hypot(x[m] - x[0], y[m] - y[0])
    return dict(max_disp=float(d.max()), ok=bool(d.max() < Q_TOL))


def flyby_immunity(t, x, y, t_sorted):
    if t_sorted is None:
        return dict(max_disp=None, ok=None)
    m = t >= t_sorted + 300.0
    if m.sum() < 2:
        return dict(max_disp=0.0, ok=True)
    d = np.hypot(x[m] - x[m][0], y[m] - y[m][0])
    return dict(max_disp=float(d.max()), ok=bool(d.max() < Q_TOL))


def circuit(t, x, L):
    """V2c: full-torus circuit detection on unwrapped cargo x."""
    v = speed(t, x)
    adv = x - x[0]
    tow = v >= V_TOW_MIN
    parkm = np.abs(v) < V_PARK
    # count tow phases separated by >=200tu parked
    phases, in_tow, t_park0 = 0, False, None
    dt = t[1] - t[0] if len(t) > 1 else 1.0
    npark = max(int(200.0 / dt), 1)
    run_park = 0
    armed = True
    for i in range(len(t)):
        if parkm[i]:
            run_park += 1
            if run_park >= npark:
                armed = True
        else:
            run_park = 0
        if tow[i] and armed:
            phases += 1
            armed = False
    icirc = np.where(adv >= L)[0]
    t_circ = float(t[icirc[0]]) if len(icirc) else None
    return dict(n_tow_phases=int(phases), t_circuit=t_circ,
                net_x=float(adv[-1]), end_parked=bool(parkm[-1]),
                ok=bool(t_circ is not None and phases >= 2))
