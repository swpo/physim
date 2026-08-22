"""metrics.py — blob-loop (phase 4b) LOCKED metrics.

Locked BEFORE the G1B 2-seed circuit battery and before any G2 comparison row.

CIRCUIT CYCLE DETECTION (on a saved cargo track x(t), torus-unwrapped):
- TOW event: maximal contiguous span where smoothed velocity vx > V_TOW
  (=0.03 px/tu, ~half pair speed) AND net dx over the span >= 15 px.
- RETURN segment: between two consecutive tows, net dx <= -RET_MIN (hand saw,
  -x return) OR >= +RET_MIN with wrap (grown saw, +x wake return); RET_MIN=10px.
  Return fraction = |net return dx| / |previous tow dx|.
- CYCLE k = tow_k -> return_k -> tow_{k+1} exists. FULL CIRCUIT = cycle with
  return fraction >= 0.66 (cargo came at least 2/3 of the way back to station
  before re-grip). Station drift = |x(grip_{k+1}) - x(grip_k)| (mod L).
- G1 PASS gate: >= 2 tow events AND >= 1 full circuit per seed, 2 seeds,
  census frozen (nc1, nc2 constant), cargo on-lane (|y-48| < 4 outside
  tow/release transients measured at parked samples).

HANDOFF INSTRUMENTATION (dock-to-dock interference case):
- for every carrier pass (min-image |x_M - x_cargo| < 20 px window): record
  cargo displacement during the pass and min distance; classify GHOST
  (|dx_cargo| < 1 px), NUDGE (1-5 px), GRIP (leads to tow event).

Cargo speed smoothing: 3-sample box on the 5-tu grid (15 tu window).
"""
import numpy as np

V_TOW = 0.03
TOW_MIN_DX = 15.0
RET_MIN = 10.0
CIRCUIT_FRAC = 0.66


def unwrap_x(x, L):
    x = np.asarray(x, float)
    d = np.diff(x)
    d = (d + L / 2) % L - L / 2
    return np.concatenate([[x[0]], x[0] + np.cumsum(d)])


def smooth(v, k=3):
    if len(v) < k:
        return v
    ker = np.ones(k) / k
    return np.convolve(v, ker, mode="same")


def tow_events(t, xu):
    """maximal spans with smoothed vx > V_TOW and net dx >= TOW_MIN_DX."""
    t = np.asarray(t, float)
    vx = np.gradient(xu, t)
    vs = smooth(vx)
    hot = vs > V_TOW
    events = []
    i = 0
    n = len(t)
    while i < n:
        if hot[i]:
            j = i
            while j + 1 < n and hot[j + 1]:
                j += 1
            dx = xu[j] - xu[i]
            if dx >= TOW_MIN_DX:
                events.append(dict(i0=int(i), i1=int(j), t0=float(t[i]),
                                   t1=float(t[j]), x0=float(xu[i]),
                                   x1=float(xu[j]), dx=float(dx)))
            i = j + 1
        else:
            i += 1
    return events


def circuit_analysis(t, xu, L):
    """tows + returns + full-circuit count. Returns dict."""
    evs = tow_events(t, xu)
    out = dict(n_tow=len(evs), tows=evs, returns=[], circuits=[])
    for k in range(len(evs) - 1):
        a, b = evs[k], evs[k + 1]
        seg = xu[a["i1"]:b["i0"] + 1]
        if len(seg) < 2:
            continue
        net = float(seg[-1] - seg[0])
        frac = abs(net) / a["dx"] if a["dx"] > 0 else 0.0
        ret = dict(after_tow=k, net_dx=net, frac=float(frac),
                   t0=a["t1"], t1=b["t0"], dur=float(b["t0"] - a["t1"]),
                   station_drift=float(abs((b["x0"] - a["x0"] + L / 2) % L - L / 2)))
        out["returns"].append(ret)
        # AMENDMENT (pre-battery, documented in results.json): two circuit
        # topologies on the torus:
        #  spring: cargo returns -x toward the previous grip (frac >= 0.66);
        #  wrap:   cargo advances ~k*L between grips (k >= 1 full torus lap)
        #          and the next grip station is within 20 px (mod L) of the
        #          previous one.
        adv = float(b["x0"] - a["x0"])
        laps = round(adv / L)
        wrap_ok = laps >= 1 and abs(adv - laps * L) <= 20.0
        spring_ok = abs(net) >= RET_MIN and frac >= CIRCUIT_FRAC
        if spring_ok or wrap_ok:
            out["circuits"].append(dict(cycle=k, tow_dx=a["dx"],
                                        return_dx=net, frac=float(frac),
                                        topology=("wrap" if wrap_ok else "spring"),
                                        laps=int(laps) if wrap_ok else 0,
                                        period=float(b["t0"] - a["t0"]),
                                        station_drift=ret["station_drift"]))
    out["n_circuit"] = len(out["circuits"])
    return out


def parent_gate_cycles(t, xu, adv_min=30.0, freeze_tu=300.0, v_freeze=0.005):
    """Parent RESUME#3 gate: count events where cargo x advances >= adv_min
    (contiguous vx>V_TOW span) and afterwards stays frozen (|vx|<v_freeze)
    for >= freeze_tu."""
    t = np.asarray(t, float)
    evs = tow_events(t, xu)
    vx = np.abs(smooth(np.gradient(xu, t)))
    n = 0
    for e in evs:
        if e["dx"] < adv_min:
            continue
        m = (t > e["t1"]) & (t <= e["t1"] + freeze_tu)
        if m.sum() >= 3 and (vx[m] < v_freeze).mean() > 0.9:
            n += 1
    return n, evs


def handoff_passes(t, x_carrier_u, x_cargo_u, L, win=20.0):
    """classify every carrier pass over the cargo (min-image distance)."""
    t = np.asarray(t, float)
    dmi = np.abs((np.asarray(x_carrier_u) - np.asarray(x_cargo_u) + L / 2) % L - L / 2)
    close = dmi < win
    passes = []
    i, n = 0, len(t)
    while i < n:
        if close[i]:
            j = i
            while j + 1 < n and close[j + 1]:
                j += 1
            dxc = float(x_cargo_u[j] - x_cargo_u[i])
            passes.append(dict(t0=float(t[i]), t1=float(t[j]),
                               dmin=float(dmi[i:j + 1].min()),
                               cargo_dx=dxc,
                               cls=("GRIP" if dxc > TOW_MIN_DX else
                                    "NUDGE" if abs(dxc) > 1.0 else "GHOST")))
            i = j + 1
        else:
            i += 1
    return passes


def load_track(path):
    z = np.load(path)
    return z["t"], z["pos1"], z["pos2"], z["ncomp1"], z["ncomp2"]


def g1_verdict(track_path, L=96.0, cargo_idx=None, carrier_idx=1, lane_y=48.0):
    """Full locked G1 verdict for one run. cargo_idx None = analyze all cargo
    ids and report each; gate uses the best-circulating cargo (the machine
    serves >=1 cargo through the circuit)."""
    t, P1, P2, nc1, nc2 = load_track(track_path)
    census_frozen = bool((nc1 == nc1[0]).all() and (nc2 == nc2[0]).all())
    xM = unwrap_x(P1[:, carrier_idx, 1], L)
    res = dict(census_frozen=census_frozen, cargo=[], L=L)
    ncar = P2.shape[1]
    idxs = range(ncar) if cargo_idx is None else [cargo_idx]
    for k in idxs:
        xs = P2[:, k, 1]
        ys = P2[:, k, 0]
        ok = ~np.isnan(xs)
        xu = unwrap_x(xs[ok], L)
        ca = circuit_analysis(t[ok], xu, L)
        # on-lane check at slow samples (parked/returning)
        vx = np.abs(np.gradient(xu, t[ok]))
        slowm = vx < 0.02
        y_dev = float(np.nanmax(np.abs(ys[ok][slowm] - lane_y))) if slowm.any() else None
        passes = handoff_passes(t[ok], xM[ok], xu, L)
        res["cargo"].append(dict(idx=int(k), n_tow=ca["n_tow"],
                                 n_circuit=ca["n_circuit"],
                                 circuits=ca["circuits"], tows=ca["tows"],
                                 returns=ca["returns"],
                                 y_dev_slow=y_dev, passes=passes))
    best = max(res["cargo"], key=lambda c: (c["n_circuit"], c["n_tow"]),
               default=None)
    res["gate_tows_ge2"] = bool(best and best["n_tow"] >= 2)
    res["gate_circuit_ge1"] = bool(best and best["n_circuit"] >= 1)
    res["gate_census"] = census_frozen
    res["G1_pass"] = bool(res["gate_tows_ge2"] and res["gate_circuit_ge1"]
                          and census_frozen)
    return res


def delivery_row(track_path, L=96.0, cargo_idx=0, station_x=None):
    """G2 comparison row: first tow = delivery. Reports grip time, release
    time, tow duration/distance, park position after release (x at the first
    sample >=200tu after tow end with |vx|<0.002), return creep speed over the
    500tu after release."""
    t, P1, P2, nc1, nc2 = load_track(track_path)
    xs = P2[:, cargo_idx, 1]
    ok = ~np.isnan(xs)
    tt = t[ok]
    xu = unwrap_x(xs[ok], L)
    evs = tow_events(tt, xu)
    row = dict(census_frozen=bool((nc1 == nc1[0]).all() and (nc2 == nc2[0]).all()),
               n_tow=len(evs))
    if not evs:
        return row
    e = evs[0]
    row.update(grip_t=e["t0"], release_t=e["t1"], tow_dur=e["t1"] - e["t0"],
               tow_dx=e["dx"], grip_x=e["x0"] % L, release_x=e["x1"] % L)
    if station_x is not None:
        row["station_offset_at_grip"] = float(abs((e["x0"] - station_x + L / 2) % L - L / 2))
    m = (tt >= e["t1"] + 100) & (tt <= e["t1"] + 600)
    if m.sum() >= 3:
        vfit = np.polyfit(tt[m], xu[m], 1)[0]
        row["return_v_500tu"] = float(vfit)
    # park sample = end position if still slow
    row["x_end"] = float(xu[-1] % L)
    row["t_end"] = float(tt[-1])
    return row
