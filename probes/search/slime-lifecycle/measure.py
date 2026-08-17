
"""measure.py — layer metrics for the slime lifecycle world."""
import numpy as np
import sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from hier_metrics import macro_period_quality, compact_top_fit


def famine_onsets(ser, thr=0.5):
    hf = ser["hf"]; tt = ser["t"]
    idx = np.where((hf[:-1] < thr) & (hf[1:] >= thr))[0]
    return tt[idx], idx


def l1_wave_period(fires, ser, rec):
    """Collective relay rhythm: ACF period of fires(t) inside famine phases."""
    hf = ser["hf"]; tt = ser["t"].astype(int)
    per, qs = [], []
    # famine segments
    on = np.where((hf[:-1] < 0.5) & (hf[1:] >= 0.5))[0]
    off = np.where((hf[:-1] >= 0.5) & (hf[1:] < 0.5))[0]
    for i in on:
        ends = off[off > i]
        j = ends[0] if len(ends) else len(hf) - 1
        a, b = tt[i] + 200, tt[j]  # skip aggregation transient? no: keep from +200
        if b - a < 600:
            continue
        seg = fires[a:b].astype(float)
        pq = macro_period_quality(seg, dt=1.0, max_lag=300)
        if pq["period"] and pq["n_cycles"] >= 5:
            per.append(pq["period"]); qs.append(pq["q"])
    if not per:
        return dict(period=None, q=0.0, n=0)
    return dict(period=float(np.median(per)), q=float(np.median(qs)), n=len(per))


def l2_agg_rise(ser, rec):
    """Aggregation timescale: median 10-90% rise time of aggm after famine
    onsets (chemotactic collapse into mounds). Physical, robust."""
    aggm = ser["aggm"]; hf = ser["hf"]
    on = np.where((hf[:-1] < 0.5) & (hf[1:] >= 0.5))[0]
    off = np.where((hf[:-1] >= 0.5) & (hf[1:] < 0.5))[0]
    rises = []
    for i in on:
        ends = off[off > i]
        j = int(ends[0]) if len(ends) else len(hf) - 1
        if (j - i) * rec < 600:
            continue
        seg = aggm[i:j]
        mid = seg[len(seg) // 4: 3 * len(seg) // 4]
        if len(mid) < 4:
            continue
        plat = float(np.median(mid))
        if plat < 0.3:
            continue
        above10 = np.where(seg >= 0.1 * plat)[0]
        above90 = np.where(seg >= 0.9 * plat)[0]
        if len(above10) == 0 or len(above90) == 0:
            continue
        rises.append((above90[0] - above10[0]) * rec)
    if not rises:
        return dict(rise=None, n=0)
    return dict(rise=float(np.median(rises)), n=len(rises))


def l2_coarsen_tau(ser, rec):
    """Aggregation timescale: exp-fit tau of ncl decay after each famine onset."""
    ncl = ser["ncl"]; hf = ser["hf"]
    on = np.where((hf[:-1] < 0.5) & (hf[1:] >= 0.5))[0]
    taus = []
    for i in on:
        seg = ncl[i:i + int(1500 / rec)]
        if len(seg) < 10 or seg.max() < 4:
            continue
        k0 = int(np.argmax(seg))
        seg = seg[k0:].astype(float)
        if len(seg) < 8:
            continue
        c = seg[-3:].mean()
        y = seg - c
        good = y > max(0.5, 0.05 * y[0])
        if good.sum() < 5:
            continue
        t = np.arange(len(seg))[good] * rec
        ly = np.log(y[good])
        A = np.vstack([t, np.ones_like(t)]).T
        (m, b), *_ = np.linalg.lstsq(A, ly, rcond=None)
        if m < 0:
            taus.append(-1.0 / m)
    if not taus:
        return dict(tau=None, n=0)
    return dict(tau=float(np.median(taus)), n=len(taus))


def l3_top(ser, rec, burn_frac=0.2):
    """Top lifecycle law on aggm (aggregated dormant biomass fraction)."""
    n = len(ser["t"])
    b = int(n * burn_frac)
    res = {}
    for key in ("aggm", "hf", "cv"):
        x = ser[key][b:]
        fit = compact_top_fit(x, dt=rec)
        pq = macro_period_quality(x, dt=rec)
        res[key] = dict(fit=fit, acf_period=pq["period"], acf_q=pq["q"],
                        acf_ncyc=pq["n_cycles"])
    return res


def candidate_metrics(out, rec):
    ser = out["ser"]
    m = dict(ok=out["ok"], why=out["why"], t_end=int(out["t"]))
    if len(ser["t"]) < 50:
        return m
    m["l1"] = l1_wave_period(out["fires"], ser, rec)
    m["l2"] = l2_agg_rise(ser, rec)
    m["l2_ncl"] = l2_coarsen_tau(ser, rec)
    m["l3"] = l3_top(ser, rec)
    # refire hist median
    fh = out.get("fire_hist")
    if fh is not None and fh.sum() > 100:
        cs = np.cumsum(fh)
        m["l1_refire_med"] = int(np.searchsorted(cs, cs[-1] / 2))
    # amplitude of lifecycle
    b = len(ser["t"]) // 5
    m["aggm_range"] = float(np.percentile(ser["aggm"][b:], 95) - np.percentile(ser["aggm"][b:], 5))
    m["vmean_last"] = float(ser["vmean"][-1])
    onsets, _ = famine_onsets(ser)
    m["n_famines"] = int(len(onsets))
    if len(onsets) > 2:
        m["famine_period_med"] = float(np.median(np.diff(onsets)))
    return m


def gate_check(m, budget_s=None):
    """Evaluate G1/G2 partially (G3-G5 need extra runs)."""
    g = {}
    l1p = m.get("l1", {}).get("period")
    l2t = m.get("l2_ncl", {}).get("tau")
    l3 = m.get("l3", {})
    best = None
    for key in ("aggm", "hf", "cv"):
        f = l3.get(key, {}).get("fit", {})
        mdl, r2, pr = f.get("model"), f.get("r2", 0), f.get("params", {})
        okm = (mdl == "oscillator" and pr.get("n_cycles", 0) >= 5) or \
              (mdl == "switch" and pr.get("n_flips", 0) >= 6) or (mdl == "relaxation")
        if mdl in ("oscillator", "switch") and okm and r2 >= 0.85:
            if best is None or r2 > best[1]:
                best = (key, r2, mdl, pr)
    g["G2"] = best is not None
    g["G2_detail"] = best
    l2t = m.get("l2", {}).get("rise") or l2t
    if l1p and l2t and best:
        # top period: prefer ACF period of aggm (robust for square waves),
        # else 2*mean_dwell for switch fits
        per = l3.get("aggm", {}).get("acf_period")
        if not per:
            per = best[3].get("period") or (2 * best[3].get("mean_dwell", 0)
                                            if best[3].get("mean_dwell") else None)
        if per:
            g["sep12"] = l2t / l1p
            g["sep23"] = per / l2t
            g["G1"] = (g["sep12"] >= 5) and (g["sep23"] >= 5)
        else:
            g["G1"] = False
    else:
        g["G1"] = False
    return g
