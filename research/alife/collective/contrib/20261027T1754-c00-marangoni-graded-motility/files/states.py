"""State structure of Marangoni rods from rods.json files (trackrods.py).
Per rod-frame: centroid speed over a +-W frame window (px/t and own lengths/t, own length = the track's median L4),
body-mean flow speed, |cos| between travel and long axis, ring dipole along travel (rod lengths; < 0 = rear-loaded).
Tests: (1) distribution shape of log speed (1 vs 2 Gaussian components, BIC; bimodality coefficient; per-rod means);
(2) variance decomposition: rod identity, size + cycle phase + run time (graded model), residual;
(3) within-rod autocorrelation of speed (relaxation time vs lifetime); (4) two-threshold (Schmitt) state calls and
dwell times (complete dwells only): CV, exponential fit, dwell vs lifetime; (5) heading and ring vs speed.
usage: states.py OUTPREFIX run1/rods.json [run2/rods.json ...]"""
import sys, json, os
import numpy as np
from scipy import stats

W = int(os.environ.get("HALFWIN", "2"))  # half window in frames (2.5 t frames; 2 -> 10 t window, 5 -> 25 t)
MINLEN = 2 * W + 9  # tracks with >= 13 frames (32.5 t) enter the rod-frame tables
import os
BIRTHS = tuple(os.environ.get("BIRTHS", "split").split(","))  # default: split-born rods only (the minority's population)


def load(paths):
    rows = []  # rod-frame rows
    trk = []
    for ri, p in enumerate(paths):
        d = json.load(open(p)); FT = d["FT"]; mar = np.array(d["mar"]); T = d["T"]
        for t in d["tracks"]:
            n = t["n"]
            if n < MINLEN or (BIRTHS != ("all",) and t["birth"] not in BIRTHS): continue
            y = np.array(t["y"]); x = np.array(t["x"]); A = np.array(t["area"]); L4 = np.array(t["L4"])
            ax = np.array(t["ax"]); U = np.array(t["U"]); dip = np.array(t["dip"])
            Lm = float(np.median(L4))
            ks = np.arange(W, n - W)
            vy = (y[ks + W] - y[ks - W]) / (2 * W * FT); vx = (x[ks + W] - x[ks - W]) / (2 * W * FT)
            sp = np.hypot(vy, vx)
            cosax = np.abs(vy * ax[ks, 0] + vx * ax[ks, 1]) / np.maximum(sp, 1e-9)
            ring = (dip[ks, 0] * vy + dip[ks, 1] * vx) / np.maximum(sp, 1e-9) / Lm
            ringmag = np.hypot(dip[ks, 0], dip[ks, 1]) / Lm
            usp = np.hypot(U[ks, 0], U[ks, 1])
            phase = ks / (n - 1)
            f = t["start"] + ks
            tid = len(trk)
            trk.append(dict(run=ri, id=t["id"], n=n, dividing=t["dividing"], fate=t["fate"], Lm=Lm, start=t["start"],
                            parents=t["parents"], lasting=t["lasting"], birth=t["birth"],
                            D=float(np.hypot(y[-1] - y[0], x[-1] - x[0]) / Lm), life=n * FT,
                            sp=sp, spL=sp / Lm, usp=usp, cos=cosax, ring=ring, f=f, phase=phase, A=A[ks]))
            for j, k in enumerate(ks):
                rows.append((ri, tid, f[j], f[j] * FT, mar[f[j]], phase[j], A[k], Lm, sp[j], sp[j] / Lm, usp[j], cosax[j],
                             ring[j], ringmag[j], int(t["dividing"])))
    R = np.array(rows, float)
    cols = "run tid f t mar phase A Lm sp spL usp cos ring ringmag div".split()
    return {c: R[:, i] for i, c in enumerate(cols)}, trk


def gmm1d(x, k, iters=500, seed=0):
    rng = np.random.default_rng(seed); n = len(x)
    best = None
    for rep in range(8):
        mu = np.sort(rng.choice(x, k, replace=False)); sd = np.full(k, x.std()); w = np.full(k, 1 / k)
        for _ in range(iters):
            pdf = w * stats.norm.pdf(x[:, None], mu, sd) + 1e-300
            r = pdf / pdf.sum(1, keepdims=True)
            nk = r.sum(0); w = nk / n; mu = (r * x[:, None]).sum(0) / nk
            sd = np.sqrt((r * (x[:, None] - mu) ** 2).sum(0) / nk) + 1e-6
        ll = np.log((w * stats.norm.pdf(x[:, None], mu, sd)).sum(1) + 1e-300).sum()
        if best is None or ll > best[0]: best = (ll, mu, sd, w)
    ll, mu, sd, w = best
    bic = -2 * ll + (3 * k - 1) * np.log(n)
    return dict(ll=ll, bic=bic, mu=mu, sd=sd, w=w)


def bimod_coef(x):
    n = len(x); g = stats.skew(x); k = stats.kurtosis(x)
    return (g * g + 1) / (k + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))


def kde_modes(x, grid):
    k = stats.gaussian_kde(x)
    y = k(grid); m = [i for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] > y[i + 1]]
    return y, [(float(grid[i]), float(y[i])) for i in m]


def acf_within(trk, key="spL", maxlag=40, minn=50):
    """mean over tracks of the autocorrelation of speed fluctuations about the POOLED mean (so between-rod and
    slow within-rod variance both appear as a slow component); and about each track's own mean."""
    xs = [t[key] for t in trk if len(t[key]) >= minn]
    allv = np.concatenate(xs); mu, var = allv.mean(), allv.var()
    out_p, out_o = [], []
    for lag in range(maxlag + 1):
        num = 0; den = 0; num_o = 0; den_o = 0
        for x in xs:
            if len(x) <= lag: continue
            a = x[:len(x) - lag] - mu; b = x[lag:] - mu
            num += (a * b).sum(); den += len(a)
            xo = x - x.mean(); ao = xo[:len(x) - lag]; bo = xo[lag:]
            num_o += (ao * bo).sum(); den_o += len(ao) * xo.var()
        out_p.append(num / den / var); out_o.append(num_o / max(den_o, 1e-12))
    return np.array(out_p), np.array(out_o), len(xs)


def schmitt(x, lo, hi):
    """two-threshold state call: 1 = swimming once above hi until below lo; start state by x[0] vs midpoint."""
    st = np.zeros(len(x), int); cur = int(x[0] > 0.5 * (lo + hi))
    for i, v in enumerate(x):
        if cur == 0 and v > hi: cur = 1
        elif cur == 1 and v < lo: cur = 0
        st[i] = cur
    return st


def dwells(trk, key, lo, hi, FT):
    """complete dwells (bounded by switches on both sides) and censored dwells, per state; switches per rod-time."""
    comp = {0: [], 1: []}; cens = {0: [], 1: []}; nsw = 0; ttot = 0.0; never = {0: 0, 1: 0}; nrod = 0
    for t in trk:
        x = t[key]
        if len(x) < 5: continue
        st = schmitt(x, lo, hi); nrod += 1
        ch = np.nonzero(np.diff(st))[0]
        nsw += len(ch); ttot += len(x) * FT
        if len(ch) == 0: never[int(st[0])] += 1
        b = np.concatenate([[-1], ch, [len(x) - 1]])
        for i in range(len(b) - 1):
            seg_state = st[b[i] + 1]; L = (b[i + 1] - b[i]) * FT
            if i == 0 or i == len(b) - 2: cens[seg_state].append(L)
            else: comp[seg_state].append(L)
    return comp, cens, nsw, ttot, never, nrod


def ols_r2(X, y):
    X1 = np.column_stack([np.ones(len(y)), X]); b, *_ = np.linalg.lstsq(X1, y, rcond=None)
    res = y - X1 @ b
    return 1 - res.var() / y.var(), b


def analyse(paths, prefix, FT=2.5, thr=None):
    R, trk = load(paths)
    rep = {}
    ls = np.log10(np.maximum(R["spL"], 1e-4))
    g1, g2 = gmm1d(ls, 1), gmm1d(ls, 2)
    # effective sample size: one sample per decorrelation time (estimated below) -> BIC with n_eff
    pac, oac, nac = acf_within(trk)
    tau_p = FT * (np.argmax(pac < np.exp(-1)) if (pac < np.exp(-1)).any() else len(pac))
    tau_o = FT * (np.argmax(oac < np.exp(-1)) if (oac < np.exp(-1)).any() else len(oac))
    neff = len(ls) * FT / max(tau_o, FT)
    dbic_eff = ((g2["ll"] - g1["ll"]) * (neff / len(ls)) * -2) + 3 * np.log(neff)  # BIC2 - BIC1 rescaled to n_eff
    grid = np.linspace(-3, 0, 301)
    _, modes_inst = kde_modes(ls, grid)
    per_rod = np.array([np.log10(max(np.mean(t["spL"]), 1e-4)) for t in trk])
    _, modes_rod = kde_modes(per_rod, grid)
    rep["n_rodframes"] = int(len(ls)); rep["n_rods"] = len(trk)
    rep["speed_px_per_t"] = dict(median=float(np.median(R["sp"])), q10=float(np.quantile(R["sp"], .1)), q90=float(np.quantile(R["sp"], .9)))
    rep["speed_L_per_t"] = dict(median=float(np.median(R["spL"])), q10=float(np.quantile(R["spL"], .1)), q90=float(np.quantile(R["spL"], .9)))
    rep["log_speed_gmm"] = dict(bic1=g1["bic"], bic2=g2["bic"], dBIC_2minus1_raw=g2["bic"] - g1["bic"],
                                dBIC_2minus1_neff=float(dbic_eff), neff=float(neff),
                                mu2=g2["mu"].tolist(), sd2=g2["sd"].tolist(), w2=g2["w"].tolist(),
                                ashman_D=float(abs(g2["mu"][0] - g2["mu"][1]) / np.sqrt(0.5 * (g2["sd"][0] ** 2 + g2["sd"][1] ** 2))))
    rep["bimodality_coef_log_inst"] = float(bimod_coef(ls)); rep["bimodality_coef_log_perrod"] = float(bimod_coef(per_rod))
    rep["kde_modes_log_inst"] = modes_inst; rep["kde_modes_log_perrod"] = modes_rod
    # variance decomposition of log speed
    tid = R["tid"].astype(int); grp_mean = np.bincount(tid, ls) / np.maximum(np.bincount(tid), 1)
    between = np.var(grp_mean[tid]); total = np.var(ls)
    X = np.column_stack([np.log10(R["A"]), R["phase"], R["phase"] ** 2, R["t"] / 1000, (R["t"] / 1000) ** 2, np.log10(R["Lm"])])
    r2_graded, b = ols_r2(X, ls)
    X2 = np.column_stack([X, np.eye(len(grp_mean))[tid]]) if len(grp_mean) < 400 else None
    r2_rod = between / total
    rep["var_decomp_log_speed"] = dict(total=float(total), share_between_rods=float(r2_rod),
                                       r2_graded_size_phase_time=float(r2_graded))
    if X2 is not None:
        r2_both, _ = ols_r2(X2, ls); rep["var_decomp_log_speed"]["r2_rod_plus_graded"] = float(r2_both)
    rep["acf"] = dict(tau_pooledmean=float(tau_p), tau_ownmean=float(tau_o), ntracks=nac,
                      pooled=pac[:41:4].round(3).tolist(), own=oac[:41:4].round(3).tolist(), lags_t=(np.arange(0, 41, 4) * FT).tolist())
    rep["median_life_t"] = float(np.median([t["life"] for t in trk]))
    rep["median_cycle_dividing_t"] = float(np.median([t["life"] for t in trk if t["dividing"]] or [np.nan]))
    # Schmitt thresholds: from argument or the pooled quantiles (40th / 60th percentiles in lengths per t)
    if thr is None:
        thr = (float(np.quantile(R["spL"], 0.4)), float(np.quantile(R["spL"], 0.6)))
    lo, hi = thr
    comp, cens, nsw, ttot, never, nrod = dwells(trk, "spL", lo, hi, FT)
    dw = {}
    for s_ in (0, 1):
        c = np.array(comp[s_])
        if len(c) >= 5:
            cv = float(c.std() / c.mean())
            ks = stats.kstest((c - c.min()) / (c.mean() - c.min()), "expon") if c.mean() > c.min() else None
            dw[s_] = dict(n_complete=len(c), mean=float(c.mean()), median=float(np.median(c)), cv=cv,
                          ks_shifted_exp_p=float(ks.pvalue) if ks else None, n_censored=len(cens[s_]),
                          mean_censored=float(np.mean(cens[s_])) if cens[s_] else None)
        else:
            dw[s_] = dict(n_complete=len(c), n_censored=len(cens[s_]))
    rep["dwell"] = dict(thresholds_L_per_t=[lo, hi], rest=dw[0], swim=dw[1], switches=nsw, rod_time=ttot,
                        switches_per_100t=100 * nsw / ttot, rods=nrod, rods_never_switch_rest=never[0],
                        rods_never_switch_swim=never[1])
    sweep = []
    for a, b in ((0.3, 0.7), (0.4, 0.6), (0.2, 0.8), (0.5, 0.9), (0.1, 0.5)):
        l_, h_ = float(np.quantile(R["spL"], a)), float(np.quantile(R["spL"], b))
        c_, _, ns_, tt_, _, _ = dwells(trk, "spL", l_, h_, FT)
        sweep.append(dict(q=(a, b), lo=l_, hi=h_, rest_mean=float(np.mean(c_[0])) if c_[0] else None,
                          swim_mean=float(np.mean(c_[1])) if c_[1] else None, sw_per_100t=100 * ns_ / tt_,
                          cv=[float(np.std(c_[k]) / np.mean(c_[k])) if len(c_[k]) > 3 else None for k in (0, 1)]))
    rep["dwell_threshold_sweep"] = sweep
    # heading and ring vs speed quartiles
    q = np.quantile(R["spL"], [0, .25, .5, .75, 1])
    hv = []
    for i in range(4):
        m = (R["spL"] >= q[i]) & (R["spL"] <= q[i + 1])
        hv.append(dict(q=i + 1, spL=float(np.median(R["spL"][m])), cos_axis=float(np.median(R["cos"][m])),
                       ring_along=float(np.median(R["ring"][m])), ringmag=float(np.median(R["ringmag"][m]))))
    rep["by_speed_quartile"] = hv
    rep["corr_speed_ringmag_spearman"] = float(stats.spearmanr(R["spL"], R["ringmag"])[0])
    json.dump(rep, open(prefix + "_states.json", "w"), indent=1, default=float)
    np.savez_compressed(prefix + "_rodframes.npz", **R)
    return rep, R, trk


if __name__ == "__main__":
    rep, R, trk = analyse(sys.argv[2:], sys.argv[1])
    print(json.dumps(rep, indent=1, default=float))
