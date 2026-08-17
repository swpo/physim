
"""runner.py -- candidate evaluation for the morpho-counter search (v3, METRIC-LOCKED).

METRIC LOCK (final, 2026-02-17): tau2 = median duration of a requantization
EVENT: from onset of the deep envelope pinch (envmin first below 0.5x the
PRECEDING inter-event plateau) to healed (envmin back above 0.8x the
FOLLOWING plateau after the last flip). Flip clusters separated < 100 t merge.
Both sub-phases (pinch = phase slip; heal = amplitude regrowth) are
non-adiabatic defect dynamics; the slow pre-pinch sag is slaved to L3 and
excluded. Sensitivity alternatives (pinch-only width, exp-fit healing tau)
are reported in SUMMARY.md; gates use ONLY this locked definition.

Theory coordinates of a candidate:
  Dv        : inhibitor diffusion -> Turing band ratio r=k_hi/k_lo
  (L,n_pair): ring length -> rung ladder k_n = 2 pi n / L
  kappa     : setpoint position in the MEASURED S-gap
  eps       : C drive gain (slow-timescale lever)
  noise     : kinetic noise amplitude

Layer timescales (all MEASURED per run):
  tau1: micro kinetics = 1/e time of the ACF of a detrended single-pixel trace
  tau2: requantization event = median duration of envelope pinches around
        count flips, threshold 0.5x LOCAL baseline (median env in +-[150,600]t
        around the flip, excluding +-150t core)
  tau3: counter period = median up-crossing interval of the 2-level count
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from morpho_sim import simulate, turing_info
from hier_metrics import compact_top_fit

A, B, DU = 0.1, 0.9, 1.0

_calib_cache = {}

def calibrate_plateaus(Dv, L, n_pair, dt=0.1, seed=7):
    key = (Dv, L, tuple(n_pair))
    if key in _calib_cache:
        return _calib_cache[key]
    out = []
    for n in n_pair:
        p = dict(ny=8, nx=L, dx=1.0, dt=dt, a=A, b=B, Du=DU, Dv=Dv, Dc=10.0,
                 sigma=1.0, mode="auto", eps=0.0, steps=6000, meas_every=100,
                 seed=seed, k_ref=0.62, C0=1.0, seed_mode=n, noise_amp=2e-3)
        r = simulate(p)
        out.append({"n": n, "held": int(r["nz"][-1]) == n,
                    "S": float(r["Sm"][-1]), "n_final": int(r["nz"][-1])})
    _calib_cache[key] = out
    return out


def dwell_stats(t, n, lo, hi):
    lev = np.where(n >= (lo + hi) / 2, 1, 0)
    ch = np.where(np.diff(lev) != 0)[0]
    if len(ch) < 2:
        return {"n_flips": int(len(ch)), "period": None, "n_cycles": 0,
                "dwell_lo": None, "dwell_hi": None}
    seg_t = t[ch]
    dwell_hi, dwell_lo = [], []
    for i in range(len(ch) - 1):
        d = seg_t[i + 1] - seg_t[i]
        (dwell_hi if lev[ch[i] + 1] == 1 else dwell_lo).append(d)
    ups = seg_t[np.array([lev[c + 1] == 1 for c in ch])]
    per = float(np.median(np.diff(ups))) if len(ups) >= 2 else None
    return {"n_flips": int(len(ch)), "period": per, "n_cycles": int(max(len(ups) - 1, 0)),
            "dwell_lo": float(np.median(dwell_lo)) if dwell_lo else None,
            "dwell_hi": float(np.median(dwell_hi)) if dwell_hi else None}


def event_stats(t, envmin, n_series):
    """L2 defect (requantization) events and their HEALING time.

    Definition (fixed before certification; see SUMMARY caveats):
      event   = cluster of count flips separated < 100 t (one requantization).
      tau2    = median healing time: from the LAST flip of the cluster to the
                first time envmin >= 0.8 * plateau_next, where plateau_next =
                median envmin over the following inter-event dwell (core only,
                150 t margins). Healing reflects L2-proper dynamics (defect
                zip + amplitude regrowth at the Turing rate), NOT the slow
                adiabatic sag before the flip (that part is slaved to L3).
      Also reported: pinch_w = median full-width of the deep pinch
                (envmin < 0.5 * plateau_next) around the flip.
    """
    dtm = t[1] - t[0] if len(t) > 1 else 1.0
    flips = np.where(np.diff(n_series) != 0)[0]
    if len(flips) == 0:
        return {"n_events": 0, "tau2": None}
    groups = [[flips[0]]]
    for f in flips[1:]:
        if t[f] - t[groups[-1][-1]] < 100.0:
            groups[-1].append(f)
        else:
            groups.append([f])
    marg = max(int(150.0 / dtm), 1)

    def plateau_between(i0, i1):
        lo_c = min(i0 + marg, len(t) - 2)
        hi_c = max(i1 - marg, lo_c + 3)
        return float(np.median(envmin[lo_c:hi_c]))

    durs, heals, pinches = [], [], []
    for gi, g in enumerate(groups):
        f_first, f_last = g[0], g[-1] + 1
        prv = groups[gi - 1][-1] + 1 if gi > 0 else 0
        nxt = groups[gi + 1][0] if gi + 1 < len(groups) else len(t) - 1
        plat_pre = plateau_between(prv, f_first)
        plat_post = plateau_between(f_last, nxt)
        # event START: onset of deep pinch vs PRECEDING plateau
        a = f_first
        while a > 0 and envmin[a] < 0.5 * plat_pre:
            a -= 1
        # event END: healed vs FOLLOWING plateau
        b = f_last
        while b < len(t) - 1 and envmin[b] < 0.8 * plat_post:
            b += 1
        durs.append(max((b - a) * dtm, dtm))
        heals.append(max((b - f_last) * dtm, dtm))
        c = f_last
        while c < len(t) - 1 and envmin[c] < 0.5 * plat_post:
            c += 1
        pinches.append(max((c - a) * dtm, dtm))
    if not durs:
        return {"n_events": int(len(groups)), "tau2": None}
    return {"n_events": int(len(groups)), "tau2": float(np.median(durs)),
            "heal_med": float(np.median(heals)),
            "pinch_med": float(np.median(pinches)),
            "ev_durs": [round(float(d), 1) for d in durs]}


def micro_tau(trace, dt):
    """1/e ACF time of the detrended pixel trace (slow drift removed)."""
    x = np.asarray(trace, float)
    w = max(int(50.0 / dt), 5)
    kern = np.ones(w) / w
    sm = np.convolve(x, kern, "same")
    y = x - sm
    y = y[w:-w]
    if y.std() < 1e-9:
        return None
    y = y - y.mean()
    acf = np.correlate(y, y, "full")[len(y) - 1:]
    acf /= acf[0]
    below = np.where(acf < np.exp(-1))[0]
    return float(below[0] * dt) if len(below) else None


def eval_candidate(cand, steps=60000, dt=0.1, seed=1, t_cut=1000.0,
                   want_kymo=False, C0=None, snap_at=None):
    Dv, L, kappa, eps, noise = (cand["Dv"], cand["L"], cand["kappa"],
                                cand["eps"], cand.get("noise", 2e-3))
    sigma_c = cand.get("sigma", 1.0)
    Dc_c = cand.get("Dc", 10.0)
    n_pair = tuple(cand["n_pair"])
    ti = turing_info(A, B, DU, Dv)
    cal = calibrate_plateaus(Dv, L, n_pair, dt=dt)
    res = {"cand": dict(cand), "band_ratio": round(ti["k_hi"] / ti["k_lo"], 3),
           "growth": round(ti["growth"], 4), "calib": cal}
    if not (cal[0]["held"] and cal[1]["held"]):
        res["status"] = "calib_fail (branch not stable at C=1)"
        return res
    S_lo, S_hi = cal[0]["S"], cal[1]["S"]
    kstar2 = (1 - kappa) * S_lo + kappa * S_hi
    res["kstar2"] = round(kstar2, 4)
    tr_lo = steps // 3
    p = dict(ny=8, nx=L, dx=1.0, dt=dt, a=A, b=B, Du=DU, Dv=Dv, Dc=Dc_c,
             sigma=sigma_c, mode="auto", eps=eps, kstar2=kstar2, steps=steps,
             meas_every=25, seed=seed, k_ref=0.62, C0=(C0 if C0 is not None else 1.0),
             t_on=250.0, noise_amp=noise, Cmin=0.5, Cmax=1.9, kymo=want_kymo,
             snap_at=snap_at or [], trace_win=(tr_lo, tr_lo + 15000))
    t0 = time.time()
    r = simulate(p)
    res["runtime_s"] = round(time.time() - t0, 1)
    if "blown" in r:
        res["status"] = "numerics_blowup"
        return res
    m = r["t"] >= t_cut
    t, n = r["t"][m], r["nz"][m]
    vals, counts = np.unique(n, return_counts=True)
    order = np.argsort(-counts)
    dom = sorted(vals[order[:2]].astype(int).tolist()) if len(vals) >= 2 else [int(vals[0])] * 2
    frac2 = float(counts[order[:2]].sum() / counts.sum()) if len(vals) >= 2 else 1.0
    res["rungs_visited"] = vals.astype(int).tolist()
    res["dom_pair"] = dom
    res["frac_2level"] = round(frac2, 4)
    ds = dwell_stats(t, n, dom[0], dom[1])
    res.update({k: (round(v, 1) if isinstance(v, float) else v) for k, v in ds.items()})
    ft = compact_top_fit(n, dt=float(t[1] - t[0]))
    res["top_model"], res["top_r2"] = ft["model"], ft["r2"]
    res["top_params"] = {k: (round(v, 2) if isinstance(v, float) else v)
                         for k, v in ft["params"].items()}
    ev = event_stats(t, r["envmin"][m], n)
    res.update(ev)
    tau1 = micro_tau(r.get("trace"), dt) if r.get("trace") is not None else None
    res["tau1"] = round(tau1, 1) if tau1 else None
    res["tau1_lin"] = round(1.0 / max(ti["growth"], 1e-9), 1)
    res["tau2"] = ev["tau2"]
    res["tau3_period"] = ds["period"]
    res["C_range"] = [round(float(r["Cm"][m].min()), 3), round(float(r["Cm"][m].max()), 3)]
    res["clamp_hit"] = bool(r["Cm"][m].min() <= 0.505 or r["Cm"][m].max() >= 1.895)
    sep12 = (ev["tau2"] / tau1) if (ev["tau2"] and tau1) else 0.0
    sep23 = (ds["period"] / ev["tau2"]) if (ds["period"] and ev["tau2"]) else 0.0
    res["sep12"], res["sep23"] = round(sep12, 1), round(sep23, 1)
    g1 = sep12 >= 5 and sep23 >= 5 and ev["n_events"] >= 4
    g2 = (ft["model"] == "switch" and ft["r2"] >= 0.85
          and ft["params"].get("n_flips", 0) >= 6)
    g5 = res["runtime_s"] <= 180 and steps <= 60000 and L <= 96
    res["G1"], res["G2"], res["G5"] = bool(g1), bool(g2), bool(g5)
    res["status"] = "ok"
    if want_kymo:
        res["_rec"] = r
    return res


if __name__ == "__main__":
    for cand in [dict(Dv=10.0, L=48, kappa=0.5, eps=2.4e-3, n_pair=(4, 5)),
                 dict(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6))]:
        out = eval_candidate(cand)
        out.pop("_rec", None)
        print(json.dumps({k: v for k, v in out.items() if k != "calib"}, indent=None))
