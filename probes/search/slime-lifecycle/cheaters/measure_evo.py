
"""measure_evo.py — L4 metrics on top of the certified L1-L3 stack."""
import numpy as np
import sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from hier_metrics import compact_top_fit, macro_period_quality, relaxation_tau
from measure import l1_wave_period, l2_agg_rise, famine_onsets


def l4_metrics(ser, rec, burn_frac=0.0):
    """Top-of-stack analysis of <c>(t): relaxation approach + equilibrium hold.
    Returns relax tau/r2 (on the approach from init), eq stats on last half,
    and entrainment check: power of <c> fluctuations at the L3 period."""
    cm = np.asarray(ser["cmean"], float)
    t = np.asarray(ser["t"], float)
    n = len(cm)
    out = {}
    # approach fit: from start to first time within eps of eq median
    eq_med = float(np.median(cm[n // 2:]))
    eq_sd_t = float(cm[n // 2:].std())
    out["c_eq"] = eq_med
    out["c_eq_fluct"] = eq_sd_t
    out["csd_eq"] = float(np.median(np.asarray(ser["csd"])[n // 2:]))
    dev0 = abs(cm[0] - eq_med)
    if dev0 > 3 * max(eq_sd_t, 1e-3):
        # find approach window: until |cm-eq| < max(0.25*dev0-ish, 2*fluct)
        thr = max(0.15 * dev0, 2 * eq_sd_t)
        inside = np.where(abs(cm - eq_med) < thr)[0]
        k_end = int(inside[0]) if len(inside) else n
        k_end = max(k_end, 8)
        seg = cm[:k_end]
        rt = relaxation_tau(seg, dt=rec)
        # r2 of exp fit evaluated on the RAW approach segment
        if rt["tau"]:
            tt = np.arange(len(seg)) * rec
            c_inf = eq_med
            a = seg[0] - c_inf
            pred = a * np.exp(-tt / rt["tau"]) + c_inf
            ss = 1 - ((seg - pred) ** 2).sum() / max(((seg - seg.mean()) ** 2).sum(), 1e-12)
            out["relax"] = dict(tau=float(rt["tau"]), r2_logfit=float(rt["r2"]),
                                r2_raw=float(ss), window_ticks=float(k_end * rec))
        else:
            out["relax"] = dict(tau=None, r2_logfit=0.0, r2_raw=0.0,
                                window_ticks=float(k_end * rec))
    else:
        out["relax"] = None  # started at equilibrium
    # full-series compact fit for reference
    out["fit_full"] = compact_top_fit(cm, dt=rec)
    # oscillator check (regime b): ACF on full post-burn series
    b = n // 5
    pq = macro_period_quality(cm[b:] - cm[b:].mean(), dt=rec)
    out["acf"] = pq
    # entrainment to L3: correlate detrended <c> with aggm at lag 0..1 cycle
    agg = np.asarray(ser["aggm"], float)[n // 2:]
    ceq = cm[n // 2:] - np.polyval(np.polyfit(np.arange(len(cm[n // 2:])), cm[n // 2:], 1),
                                   np.arange(len(cm[n // 2:])))
    if agg.std() > 1e-6 and ceq.std() > 1e-9:
        r = float(np.corrcoef(agg, ceq)[0, 1])
    else:
        r = 0.0
    out["entrain_corr_aggm"] = r
    # amplitude of per-cycle wiggle relative to slow signal
    return out


def stack_metrics(out, rec):
    ser = out["ser"]
    m = dict(ok=out["ok"], why=out["why"], t_end=int(out["t"]))
    if len(ser["t"]) < 60:
        return m
    m["l1"] = l1_wave_period(out["fires"], ser, rec)
    m["l2"] = l2_agg_rise(ser, rec)
    on, _ = famine_onsets(ser)
    m["n_famines"] = int(len(on))
    if len(on) > 2:
        m["l3_period"] = float(np.median(np.diff(on)))
    l3fit = compact_top_fit(np.asarray(ser["aggm"])[len(ser["t"]) // 5:], dt=rec)
    m["l3_fit"] = l3fit
    m["l4"] = l4_metrics(ser, rec)
    m["v_end"] = float(ser["vmean"][-1])
    m["lifecycle_alive"] = bool((np.asarray(ser["aggm"])[-len(ser["t"]) // 4:] > 0.3).any()
                                and m.get("n_famines", 0) >= 3 and m["v_end"] > 0.02)
    return m
