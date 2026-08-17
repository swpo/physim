
"""succession measurement: 4-layer gates.

L1 tau1 = mean hot residence; L2 tau2 = size-weighted median event duration;
L3 = grass fire-return clock: compact_top_fit on phi (frac B>theta) over the
     post-transient window + median per-cell FRI split by biome
     (local modulation check: FRI_forest/FRI_grass or forest burn ~ 0);
L4 = biome field meanT: relaxation/switch fit (compact_top_fit) + tau4.
G1 (round 2): sep21, sep32, sep43 all >= 5 and tau4/tau1 >= 3000.
"""
import numpy as np, sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from hier_metrics import *
from sf_core import run, nominal_Tg


def events_from_series(area, ign, rec, gap_recs=2):
    active = area > 0
    ev = []
    i, n = 0, len(active)
    while i < n:
        if not active[i]:
            i += 1; continue
        j = i
        while j < n:
            if active[j]:
                j += 1
            else:
                k = j
                while k < n and not active[k] and (k - j) < gap_recs:
                    k += 1
                if k < n and active[k]:
                    j = k
                else:
                    break
        ev.append(dict(t0=int(i * rec), dur=int((j - i) * rec),
                       size=int(ign[i:j].sum()), peak=int(area[i:j].max())))
        i = j
    return ev


def wmedian(vals, wts):
    idx = np.argsort(vals)
    v = np.asarray(vals, float)[idx]; wt = np.asarray(wts, float)[idx]
    c = np.cumsum(wt)
    if c[-1] <= 0: return None
    return float(v[np.searchsorted(c, 0.5 * c[-1])])


def fit_exp_relax(x, dt):
    """robust relaxation fit for L4: x -> c + a*exp(-t/tau), c fixed to tail
    mean, tau by log-linear regression, r2 in DATA space."""
    x = np.asarray(x, float)
    c = x[-max(5, len(x) // 8):].mean()
    y = x - c
    if abs(y[0]) < 1e-9:
        return dict(tau=None, r2=0.0, c=float(c))
    sgn = np.sign(y[0]); y = y * sgn
    good = y > 0.02 * y[0]
    if good.sum() < 8:
        return dict(tau=None, r2=0.0, c=float(c))
    t = np.arange(len(x)) * dt
    A = np.vstack([t[good], np.ones(good.sum())]).T
    (m, b), *_ = np.linalg.lstsq(A, np.log(y[good]), rcond=None)
    if m >= 0:
        return dict(tau=None, r2=0.0, c=float(c))
    pred = c + sgn * np.exp(b) * np.exp(m * t)
    r2 = 1 - ((x - pred) ** 2).sum() / max(((x - x.mean()) ** 2).sum(), 1e-12)
    return dict(tau=float(-1 / m), r2=float(r2), c=float(c),
                a=float(sgn * np.exp(b)))


def measure4(out, drop=10000, coarse=50, l4_coarse=250):
    rec = out["rec"]; i0 = drop // rec
    res = dict(runtime=round(out["runtime"], 2), f=out["f"], Tg=round(out["Tg"], 1))
    phi = out["phi_grass"][i0:]; mT = out["meanT"]; fF = out["fracForest"]
    res["T_start"] = float(mT[:10].mean()); res["T_end"] = float(mT[-40:].mean())
    res["fracF_end"] = float(fF[-40:].mean())
    res["fracF_last20_drift"] = float(fF[-len(fF)//5:].max() - fF[-len(fF)//5:].min())
    # ---- L3 grass clock (post-transient phi) ----
    sub = max(1, coarse // rec)
    n = len(phi) // sub
    phc = phi[:n * sub].reshape(n, sub).mean(1)
    top3 = compact_top_fit(phc, dt=rec * sub)
    res["L3_model"] = top3["model"]; res["L3_r2"] = top3["r2"]
    res["L3_params"] = top3["params"]
    tau3 = None
    if top3["model"] == "oscillator":
        tau3 = top3["params"].get("period")
    elif top3["model"] == "switch" and top3["params"].get("mean_dwell"):
        tau3 = 2 * top3["params"]["mean_dwell"]
    res["tau3"] = tau3
    # local modulation: per-cell FRI by biome
    fg = np.asarray(out["fri_grass"], float); ff = np.asarray(out["fri_forest"], float)
    res["fri_grass_med"] = float(np.median(fg)) if len(fg) > 20 else None
    res["fri_forest_med"] = float(np.median(ff)) if len(ff) > 20 else None
    res["n_fri_grass"] = int(len(fg)); res["n_fri_forest"] = int(len(ff))
    res["tau3_fri"] = res["fri_grass_med"]
    # ---- L2 events ----
    ev = events_from_series(out["area"][i0:], out["ign"][i0:], rec)
    sizes = [e["size"] for e in ev if e["size"] > 0]
    res["n_events"] = len(sizes)
    if sizes:
        durs = [e["dur"] for e in ev if e["size"] > 0]
        res["size_max"] = int(max(sizes)); res["size_med"] = float(np.median(sizes))
        res["tau2"] = wmedian(durs, sizes)
        pl = powerlaw_tail(sizes)
        res["pl"] = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in pl.items()}
    else:
        res["size_max"] = 0; res["tau2"] = None; res["pl"] = None
    res["tau1"] = (out["hot_ticks"] / out["ign_total"] if out["ign_total"] > 0 else None)
    # ---- L4 biome ----
    sub4 = max(1, l4_coarse // rec)
    n4 = len(mT) // sub4
    mTc = mT[:n4 * sub4].reshape(n4, sub4).mean(1)
    rel = fit_exp_relax(mTc, dt=rec * sub4)
    res["L4_relax"] = rel
    top4 = compact_top_fit(mTc, dt=rec * sub4)
    res["L4_model"] = top4["model"]; res["L4_r2"] = top4["r2"]
    res["L4_params"] = top4["params"]
    # choose tau4: relaxation tau if fit decent, else switch dwell
    tau4 = rel["tau"] if (rel["tau"] and rel["r2"] >= 0.8) else None
    if tau4 is None and top4["model"] == "switch" and top4["params"].get("mean_dwell"):
        tau4 = 2 * top4["params"]["mean_dwell"]
    res["tau4"] = tau4
    # separations
    t1, t2, t3, t4 = res["tau1"], res["tau2"], res.get("tau3"), res.get("tau4")
    if t3 is None: t3 = res.get("tau3_fri")
    res["tau3_used"] = t3
    res["sep21"] = t2 / t1 if (t1 and t2) else None
    res["sep32"] = t3 / t2 if (t2 and t3) else None
    res["sep43"] = t4 / t3 if (t3 and t4) else None
    res["span41"] = t4 / t1 if (t1 and t4) else None
    return res


def gates4(res, runtime_cap=300.0, min_events=12):
    g1 = all([res.get("sep21") and res["sep21"] >= 5,
              res.get("sep32") and res["sep32"] >= 5,
              res.get("sep43") and res["sep43"] >= 5,
              res.get("span41") and res["span41"] >= 3000,
              res["n_events"] >= min_events])
    # G2 on L4: relaxation r2>=0.85 or switch with flips>=6
    rel = res["L4_relax"]
    g2 = (rel["tau"] is not None and rel["r2"] >= 0.85) or (
        res["L4_model"] == "switch" and res["L4_r2"] >= 0.85
        and res["L4_params"].get("n_flips", 0) >= 6)
    g5 = res["runtime"] <= runtime_cap
    return dict(G1=bool(g1), G2=bool(g2), G5=bool(g5))
