"""analyse -- finite-size table, budget curve and state-given screen for study (c) at tiny size (numpy only).

  python -B analyse.py <scratch dir>          -> results/summary.json (everything; about 3 CPU-minutes)
  python -B analyse.py <scratch dir> screen   -> only the finite-size table and the screen are recomputed

Inputs (made by run_pools.sh and screen_state.py; raw arrays are scratch, not committed):
  b{32,48,64}_s*.npz   level-2 trajectories (N, s_b) per box side at declared parameters (eps 0.4, mut128 25)
  scr_{base,oracle,tiles,inputs}.npz   branches from four 64 px states at tick 140
Exam-scale stand-in: the 64 px box. Cost unit: one 64 px episode of 260 ticks (px-ticks).
Score: fair energy score on (N / sd_N, s_b / sd_s) / sqrt(2), 32 forecast members; skill = 1 - L / L(K).
"""
import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXAM_H, T_EXAM = 64, 260
LAB = 60                       # labelling tick: s_b is defined after it
ANCH = (80, 100, 120, 140, 160, 180)
HS = (8, 16, 32, 64)
STEP = 8                       # the laws' time step in ticks
M_FC = 32
C0 = 0.02                      # floor of the kind-share noise shape s (1 - s) + C0


def load_pool(S, H, key="l2"):
    L = []
    metas = []
    for f in sorted(glob.glob(os.path.join(S, f"b{H}_s*.npz"))):
        d = np.load(f)
        L.append(d[key].astype(float))
        metas.append(json.loads(str(d["meta"])))
    return (np.concatenate(L, 0), metas) if L else (None, [])


def l1_fit(l2, s1, lam=0.05):
    """Generic level-1 learner: increments of (N, s_b) per horizon regressed on the 12 level-1 summaries of the
    anchor tick (standardised on the training set), residuals resampled. The nearest stand-in at this size for
    round 5's ridge on level-1 summaries."""
    T = l2.shape[1]
    out = {}
    F0 = s1[:, LAB:].reshape(-1, s1.shape[-1])
    mu, sd = F0.mean(0), F0.std(0) + 1e-6
    for h in HS:
        F = ((s1[:, LAB:T - h] - mu) / sd).reshape(-1, s1.shape[-1])
        F = np.concatenate([np.ones((len(F), 1)), F], 1)
        D = (l2[:, LAB + h:] - l2[:, LAB:T - h]).reshape(-1, 2)
        beta = np.linalg.solve(F.T @ F + lam * len(F) * np.eye(F.shape[1]), F.T @ D)
        out[h] = (beta, D - F @ beta)
    out["mu"], out["sd"] = mu, sd
    return out


def l1_predict(m, x0, f0, h, rng):
    beta, res = m[h]
    F = np.concatenate([[1.0], (f0 - m["mu"]) / m["sd"]])
    return finish(x0 + F @ beta + res[rng.integers(0, len(res), M_FC)])


def fair_es(X, y, scale):
    """X (M, d) forecast members, y (d,) outcome; fair energy score in scaled units."""
    X = X / scale
    y = y / scale
    M = X.shape[0]
    a = np.sqrt(((X - y) ** 2).sum(-1) / X.shape[1]).mean()
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1) / X.shape[1])
    return a - D.sum() / (2 * M * (M - 1))


# ------------------------------------------------------------------ training pairs
def pairs(l2, lag, t_from=LAB + 1, t_to=None):
    """(state, increment over `lag` ticks) pairs from trajectories l2 (B, T, 2), both ends within ticks
    t_from..t_to (default: the end). Index t holds the state after tick t + 1, so tick k is index k - 1."""
    if t_to is not None:
        l2 = l2[:, :t_to]
    a = l2[:, t_from - 1:-lag]
    b = l2[:, t_from - 1 + lag:]
    return a.reshape(-1, 2), (b - a).reshape(-1, 2)


def pool_tiles(l2, rng, n_synth):
    """Synthetic exam-size episodes: four random distinct small-box members, N summed, kind share pooled."""
    B = l2.shape[0]
    out = []
    for _ in range(n_synth):
        idx = rng.choice(B, 4, replace=B < 4)
        n = l2[idx, :, 0].sum(0)
        nb = (l2[idx, :, 0] * l2[idx, :, 1]).sum(0)
        out.append(np.stack([n, nb / np.maximum(n, 1.0)], -1))
    return np.stack(out)


# ------------------------------------------------------------------ generic family: analog ensemble
def analog_fit(l2, area_ratio):
    """Per horizon: states (N in exam-box units, s_b, tick) and increments (dN in exam-box units, ds)."""
    out = {}
    T = l2.shape[1]
    for h in HS:
        x, d = pairs(l2, h)
        tk = np.tile(np.arange(LAB + 1, T - h + 1), l2.shape[0]).astype(float)
        out[h] = (np.stack([x[:, 0] * area_ratio, x[:, 1], tk], -1), np.stack([d[:, 0] * area_ratio, d[:, 1]], -1))
    return out


def analog_members(model, x0, tick, h, fscale, use_tick):
    X, D = model[h]
    q = np.array([x0[0], x0[1], tick])
    w = fscale if use_tick else fscale[:2]
    dist = (((X[:, :len(w)] - q[:len(w)]) / w) ** 2).sum(-1)
    k = int(np.clip(len(X) // 8, 8, 48))
    return D[np.argsort(dist)[:k]]


def finish(out):
    out[:, 0] = np.maximum(out[:, 0], 0.0)
    out[:, 1] = np.clip(out[:, 1], 0.0, 1.0)
    return out


def analog_predict(model, x0, tick, h, rng, fscale, use_tick=False):
    D = analog_members(model, x0, tick, h, fscale, use_tick)
    return finish(x0 + D[rng.integers(0, len(D), M_FC)])


# ------------------------------------------------------------------ generic family: direct regression per horizon
def feats(x, nbar):
    s = x[..., 1]
    return np.stack([np.ones_like(s), s, s * s, x[..., 0] / nbar - 1.0], -1)


def ridge_fit(l2, area_ratio, lam=1e-3):
    """Per horizon: increments regressed on (1, s, s^2, N / Nbar - 1); residuals kept for resampling. A generic
    model with four constants per coordinate and horizon and no law (the strong form of the round-5 control)."""
    out = {}
    nbar = float(l2[:, LAB:, 0].mean() * area_ratio)
    for h in HS:
        x, d = pairs(l2, h)
        x = np.stack([x[:, 0] * area_ratio, x[:, 1]], -1)
        d = np.stack([d[:, 0] * area_ratio, d[:, 1]], -1)
        F = feats(x, nbar)
        beta = np.linalg.solve(F.T @ F + lam * len(F) * np.eye(F.shape[1]), F.T @ d)
        out[h] = (beta, d - F @ beta)
    out["nbar"] = nbar
    return out


def ridge_fss_fit(l32, l48, lam=1e-3):
    """The generic counterpart of the finite-size extrapolation: the per-horizon regression fitted on both small
    boxes with every coefficient linear in 1 / area, read off at the exam box (z = 0); residuals of the 48 px pool."""
    z48 = (1 / 48 ** 2 - 1 / 64 ** 2) / (1 / 32 ** 2 - 1 / 64 ** 2)
    src = ((l32, 4.0, 1.0), (l48, (64 / 48) ** 2, z48))
    nbar = float(np.mean([l2[:, LAB:, 0].mean() * ar for l2, ar, _ in src]))
    out = {"nbar": nbar}
    for h in HS:
        FF, DD = [], []
        for l2, ar, z in src:
            x, d = pairs(l2, h)
            F = feats(np.stack([x[:, 0] * ar, x[:, 1]], -1), nbar)
            FF.append(np.concatenate([F, F * z], 1))
            DD.append(np.stack([d[:, 0] * ar, d[:, 1]], -1))
        F, D = np.concatenate(FF), np.concatenate(DD)
        beta = np.linalg.solve(F.T @ F + lam * len(F) * np.eye(F.shape[1]), F.T @ D)
        out[h] = (beta[:4], DD[1] - FF[1] @ beta)
    return out


def ridge_predict(model, x0, h, rng):
    beta, res = model[h]
    return finish(x0 + feats(x0, model["nbar"]) @ beta + res[rng.integers(0, len(res), M_FC)])


def step_data(sets, t_to=None):
    """Lag-STEP pairs in exam-box units from a list of (trajectories, area ratio, weight)."""
    X, D, W = [], [], []
    for l2, ar, w in sets:
        x, d = pairs(l2, STEP, t_to=t_to)
        X.append(np.stack([x[:, 0] * ar, x[:, 1]], -1))
        D.append(np.stack([d[:, 0] * ar, d[:, 1]], -1))
        W.append(np.full(len(x), w / max(len(x), 1)))
    return np.concatenate(X), np.concatenate(D), np.concatenate(W)


def ridge_it_fit(sets, t_to=None, lam=1e-3):
    """Generic autoregressive model: the 8-tick increment regressed on (1, s, s^2, N / Nbar - 1), residuals kept.
    `sets` may pool sources with weights (the generic way of mixing cheap small-box data with Lab data)."""
    X, D, W = step_data(sets, t_to)
    W = W / W.sum()
    nbar = float((X[:, 0] * W).sum())
    F = feats(X, nbar)
    beta = np.linalg.solve((F * W[:, None]).T @ F + lam * np.eye(F.shape[1]), (F * W[:, None]).T @ D)
    return dict(beta=beta, res=D - F @ beta, p=W, nbar=nbar)


def ridge_it_predict(m, x0, h, rng):
    x = np.tile(x0, (M_FC, 1)).astype(float)
    for _ in range(h // STEP):
        x = finish(x + feats(x, m["nbar"]) @ m["beta"] + m["res"][rng.choice(len(m["res"]), M_FC, p=m["p"])])
    return x


def analog_it_fit(sets, t_to=None):
    X, D, _ = step_data(sets, t_to)
    return dict(X=X, D=D)


def analog_it_predict(m, x0, h, rng, fscale):
    x = np.tile(x0, (M_FC, 1)).astype(float)
    k = int(np.clip(len(m["X"]) // 8, 4, 32))
    for _ in range(h // STEP):
        dist = (((m["X"][None] - x[:, None]) / fscale[:2]) ** 2).sum(-1)               # (M, n)
        nn = np.argpartition(dist, k - 1, axis=1)[:, :k]
        x = finish(x + m["D"][nn[np.arange(M_FC), rng.integers(0, k, M_FC)]])
    return x


def residual_fit(base, lab, fscale, lam=1e-2):
    """Generic multi-fidelity recipe: a correction to the small-box analog model's mean increment, linear in
    (1, s, s^2, N / Nbar - 1), fitted on exam-size Lab episodes (every 4th tick)."""
    out = {}
    nbar = float(lab[:, LAB:, 0].mean())
    T = lab.shape[1]
    for h in HS:
        ticks = np.arange(LAB + 1, T - h + 1, 4)
        X = lab[:, ticks - 1].reshape(-1, 2)
        Dl = (lab[:, ticks - 1 + h] - lab[:, ticks - 1]).reshape(-1, 2)
        m = np.stack([analog_members(base, x, 0.0, h, fscale, False).mean(0) for x in X])
        F = feats(X, nbar)
        out[h] = np.linalg.solve(F.T @ F + lam * len(F) * np.eye(F.shape[1]), F.T @ (Dl - m))
    out["nbar"] = nbar
    return out


# ------------------------------------------------------------------ law family (level-2 effective law)
def law_fit(l2, form, t_to=None):
    """Constants of the level-2 law on increments over STEP ticks. form: 'law' ds = b1 s (1-s) + b2 (1-2s);
    'lin' ds = a0 + a1 (1-2s) (the round-5 checker's control: no selection term); 'const' ds = a0.
    Noise: Var ds = v (s (1-s) + C0) / N; N: dN = c1 (nstar - N), Var dN = q N. Returns per-box constants."""
    x, d = pairs(l2, STEP, t_to=t_to)
    n, s = np.maximum(x[:, 0], 1.0), x[:, 1]
    if form == "law":
        A = np.stack([s * (1 - s), 1 - 2 * s], -1)
    elif form == "lin":
        A = np.stack([np.ones_like(s), 1 - 2 * s], -1)
    else:
        A = np.ones_like(s)[:, None]
    co, *_ = np.linalg.lstsq(A, d[:, 1], rcond=None)
    res = d[:, 1] - A @ co
    v = float(np.mean(res ** 2 * n / (s * (1 - s) + C0)))
    v_flat = float(np.mean(res ** 2))
    nstar = float(x[:, 0].mean())
    dn = x[:, 0] - nstar
    c1 = float(-(dn * d[:, 0]).sum() / max((dn ** 2).sum(), 1e-9))
    rn = d[:, 0] + c1 * dn
    q = float(np.mean(rn ** 2 / n))
    return dict(form=form, co=[float(c) for c in co], v=v, v_flat=v_flat, nstar=nstar, c1=c1, q=q)


def law_predict(c, x0, h, rng, area_ratio, scale_noise=True):
    """Iterate the law from x0 = (N, s_b) at exam scale. Scaling rule of the law: drift constants, v, c1, q are
    per-vortex (box-independent), nstar scales with the area. scale_noise=False: the control without the scaling
    (the training box's increment variance is used as it is, and the N noise is multiplied by the area ratio)."""
    n = np.full(M_FC, x0[0], float)
    s = np.full(M_FC, x0[1], float)
    nstar = c["nstar"] * area_ratio
    for _ in range(h // STEP):
        if c["form"] == "law":
            dr = c["co"][0] * s * (1 - s) + c["co"][1] * (1 - 2 * s)
        elif c["form"] == "lin":
            dr = c["co"][0] + c["co"][1] * (1 - 2 * s)
        else:
            dr = c["co"][0] + 0 * s
        n1 = np.maximum(n, 1.0)
        if scale_noise:
            sd_s = np.sqrt(c["v"] * (s * (1 - s) + C0) / n1)
            sd_n = np.sqrt(c["q"] * n1)
        else:
            sd_s = np.sqrt(c["v_flat"]) + 0 * s
            sd_n = np.sqrt(c["q"] * n1 / area_ratio) * area_ratio
        s = np.clip(s + dr + sd_s * rng.standard_normal(M_FC), 0.0, 1.0)
        n = np.maximum(n + c["c1"] * (nstar - n) + sd_n * rng.standard_normal(M_FC), 0.0)
    return np.stack([n, s], -1)


def fss(c32, c48):
    """Finite-size extrapolation of every constant, linear in 1 / area, from the 32 and 48 px fits to 64 px.
    nstar is extrapolated as a density (per 64 px box area)."""
    a32, a48, a64 = 1 / 32 ** 2, 1 / 48 ** 2, 1 / 64 ** 2
    w = (a64 - a48) / (a48 - a32)
    ex = lambda p, q_: q_ + (q_ - p) * w
    out = dict(form=c32["form"], co=[ex(p, q_) for p, q_ in zip(c32["co"], c48["co"])])
    for k in ("v", "c1", "q", "v_flat"):
        out[k] = max(ex(c32[k], c48[k]), 1e-6)
    out["nstar"] = ex(c32["nstar"] * 4.0, c48["nstar"] * (64 / 48) ** 2)       # already in 64 px box units
    return out


# ------------------------------------------------------------------ main
def main():
    S = sys.argv[1]
    rng = np.random.default_rng(20261111)
    P = {}
    meta = {}
    for H in (32, 48, 64):
        P[H], meta[H] = load_pool(S, H)
    out = {"what": "study (c) compute_limit, tiny CPU checks on the fed-vortex world (exam-scale stand-in 64 px)",
           "PILOT_NEVER_REUSE_AS_EXAM": True,
           "parameters": "declared, not hidden: eps 0.4, mut128 25, all others vxlib.THETA0; float64; CPU",
           "pools": {str(H): dict(members=int(P[H].shape[0]), ticks=int(P[H].shape[1]),
                                  cpu_s=sum(m["cpu_s"] for m in meta[H]),
                                  cost_units_per_episode=round(P[H].shape[1] * H * H / (T_EXAM * EXAM_H ** 2), 4))
                     for H in P if P[H] is not None}}

    # ---------------- 1. finite-size table
    fs = {}
    P128, meta128 = load_pool(S, 128)
    if P128 is not None:
        out["pools"]["128"] = dict(members=int(P128.shape[0]), ticks=int(P128.shape[1]), cpu_s=sum(m["cpu_s"] for m in meta128),
                                   note="finite-size table only")
    for H in (32, 48, 64, 128):
        l2 = P.get(H) if H != 128 else P128
        if l2 is None:
            continue
        B = l2.shape[0]
        n_late = l2[:, LAB:, 0].mean(1)
        sb = l2[..., 1]
        # time (ticks after the first mutation at tick 80) for the member's s_b to stay above 0.75
        t75 = np.array([np.argmax(sb[b] >= 0.75) + 1 if (sb[b] >= 0.75).any() else np.nan for b in range(B)])
        t25 = np.array([np.argmax(sb[b] >= 0.25) + 1 if (sb[b] >= 0.25).any() else np.nan for b in range(B)])
        boot = []
        for _ in range(300):
            idx = rng.integers(0, B, B)
            c = law_fit(l2[idx], "law")
            boot.append([c["co"][0], c["co"][1], c["v"], c["nstar"], c["c1"], c["q"]])
        c = law_fit(l2, "law")
        bs = np.std(boot, 0)
        x, d = pairs(l2, STEP)
        A = np.stack([x[:, 1] * (1 - x[:, 1]), 1 - 2 * x[:, 1]], -1)
        r2 = 1 - ((d[:, 1] - A @ np.array(c["co"])) ** 2).sum() / ((d[:, 1] - d[:, 1].mean()) ** 2).sum()
        fs[str(H)] = dict(
            members=B, N_mean=round(float(n_late.mean()), 3), N_se=round(float(n_late.std(ddof=1) / np.sqrt(B)), 3),
            density_per_64px_box=round(float(n_late.mean() * (64 / H) ** 2), 3),
            density_se=round(float(n_late.std(ddof=1) / np.sqrt(B) * (64 / H) ** 2), 3),
            s_b_mean_at_tick={str(t): round(float(sb[:, t - 1].mean()), 3) for t in (100, 140, 180, 220, 260)},
            ticks_from_s25_to_s75_median=float(np.nanmedian(t75 - t25)),
            ticks_from_s25_to_s75_mean_se=[round(float(np.nanmean(t75 - t25)), 1),
                                           round(float(np.nanstd(t75 - t25, ddof=1) / np.sqrt(np.isfinite(t75 - t25).sum())), 1)],
            members_reaching_s75=int(np.isfinite(t75).sum()),
            law_per_8_ticks=dict(b1=[round(c["co"][0], 4), round(float(bs[0]), 4)], b2=[round(c["co"][1], 4), round(float(bs[1]), 4)],
                                 v=[round(c["v"], 4), round(float(bs[2]), 4)], nstar=[round(c["nstar"], 3), round(float(bs[3]), 3)],
                                 c1=[round(c["c1"], 4), round(float(bs[4]), 4)], q=[round(c["q"], 4), round(float(bs[5]), 4)],
                                 r2_single_increment=round(float(r2), 4),
                                 note="value, bootstrap se over members (300 resamples)"))
    out["finite_size"] = fs

    # ---------------- 2. budget curve on the 64 px truth pool
    T64 = P[64]
    S64, _ = load_pool(S, 64, "s1")
    B64 = T64.shape[0]
    late = T64[:, ANCH[0] - 1:]
    scale = np.array([late[..., 0].std(), late[..., 1].std()])
    fscale = np.array([2.5, 0.15, 20.0])
    unit = {H: P[H].shape[1] * H * H / (T_EXAM * EXAM_H ** 2) for H in P if P[H] is not None}
    MODE = sys.argv[2] if len(sys.argv) > 2 else "all"
    prev_f = os.path.join(HERE, "results", "summary.json")
    if MODE != "all":
        prev = json.load(open(prev_f))
        for k in ("budget_curve", "horizon_transfer", "fss_constants"):
            if k in prev:
                out[k] = prev[k]
    if MODE == "all":
        budgets = (1, 2, 4, 8, 15)
        n_draw = 6
        N_LAB = 2                                  # exam-size Lab episodes of the multi-fidelity recipes
        CELLS = ("", "|h64", "|s_b")
        pol = {}

        def add(name, i, a_, h, es, es_s):
            d = pol.setdefault(name, {c: np.zeros(B64) for c in CELLS} | {"n": np.zeros(B64), "n64": np.zeros(B64)})
            d[""][i] += es
            d["|s_b"][i] += es_s
            d["n"][i] += 1
            if h == 64:
                d["|h64"][i] += es
                d["n64"][i] += 1

        def put(name, i, a_, h, Xf, y):
            add(name, i, a_, h, fair_es(Xf, y, scale), fair_es(Xf[:, 1:2], y[1:2], scale[1:2]))

        items = [(a_, h) for a_ in ANCH for h in HS if a_ + h <= T_EXAM]
        fss_c = None
        if P[48] is not None:
            fss_c = {f: fss(law_fit(P[32], f), law_fit(P[48], f)) for f in ("law", "lin", "const")}
            fss_r = ridge_fss_fit(P[32], P[48])
            out["fss_constants"] = dict(law=fss_c["law"], cost_units=round(P[32].shape[0] * unit[32] + P[48].shape[0] * unit[48], 2))
        for i in range(B64):
            others = np.array([j for j in range(B64) if j != i])
            clim = T64[others][:, LAB + 19:].reshape(-1, 2)                    # long-run: all ticks from 80 on
            r0 = np.random.default_rng([i, 0])
            for (a_, h) in items:
                x0, y = T64[i, a_ - 1].copy(), T64[i, a_ + h - 1]
                put("K", i, a_, h, clim[r0.integers(0, len(clim), 64)], y)
                put("Ktick", i, a_, h, T64[others, a_ + h - 1], y)
                put("persistence", i, a_, h, np.tile(x0, (2, 1)), y)
                if fss_c:
                    for f in fss_c:
                        put(f"{f}_fss32+48", i, a_, h, law_predict(fss_c[f], x0, h, r0, 1.0), y)
                    put("ridge_fss32+48", i, a_, h, ridge_predict(fss_r, x0, h, r0), y)
            for R in budgets:
                for dr in range(n_draw):
                    r_ = np.random.default_rng([i, R, dr])
                    pick64 = r_.choice(others, min(R, len(others)), replace=False)
                    sets = {"64": (T64[pick64], 1.0)}
                    for H in (32, 48):
                        if P[H] is None:
                            continue
                        nH = int(round(R / unit[H]))
                        if 1 <= nH <= P[H].shape[0]:
                            sets[str(H)] = (P[H][r_.choice(P[H].shape[0], nH, replace=False)], (EXAM_H / H) ** 2)
                    mods = {}
                    for key, (tr, ar) in sets.items():
                        mods["A" + key] = ("analog", analog_fit(tr, ar))
                        mods["ridge" + key] = ("ridge", ridge_fit(tr, ar))
                        for form in ("law", "lin", "const"):
                            mods[f"{form}{key}"] = ("law", law_fit(tr, form), ar)
                        if key != "64":
                            mods[f"law{key}_noscale"] = ("law_ns", law_fit(tr, "law"), ar)
                    mods["At64"] = ("analog_t", mods["A64"][1])
                    mods["ridgeL1_64"] = ("l1", l1_fit(T64[pick64], S64[pick64]))
                    if "32" in sets and len(sets["32"][0]) >= 4:
                        tl = analog_fit(pool_tiles(sets["32"][0], r_, 2 * len(sets["32"][0])), 1.0)
                        mods["A32tile"] = ("analog", tl)
                        lab = T64[r_.choice(others, N_LAB, replace=False)]
                        mods[f"A32tile+res{N_LAB}"] = ("analog_res", tl, residual_fit(tl, lab, fscale))
                    for (a_, h) in items:
                        x0, y = T64[i, a_ - 1].copy(), T64[i, a_ + h - 1]
                        for name, m in mods.items():
                            if m[0] == "analog":
                                Xf = analog_predict(m[1], x0, a_, h, r_, fscale)
                            elif m[0] == "analog_t":
                                Xf = analog_predict(m[1], x0, a_, h, r_, fscale, use_tick=True)
                            elif m[0] == "analog_res":
                                Xf = finish(analog_predict(m[1], x0, a_, h, r_, fscale) + feats(x0, m[2]["nbar"]) @ m[2][h])
                            elif m[0] == "ridge":
                                Xf = ridge_predict(m[1], x0, h, r_)
                            elif m[0] == "l1":
                                Xf = l1_predict(m[1], x0, S64[i, a_ - 1], h, r_)
                            else:
                                Xf = law_predict(m[1], x0, h, r_, m[2], scale_noise=(m[0] == "law"))
                            put(f"{name}@R{R}", i, a_, h, Xf, y)

        def L(name, cell, idx=None):
            d = pol[name]
            n = d["n64"] if cell == "|h64" else d["n"]
            v = d[cell] / n
            return v.mean() if idx is None else v[idx].mean()

        def skill(name, cell):
            boot = [1 - L(name, cell, idx) / L("K", cell, idx) for idx in rng.integers(0, B64, (1000, B64))]
            return [round(float(1 - L(name, cell) / L("K", cell)), 4), round(float(np.std(boot)), 4)]

        def diff(n1, n2, cell):
            """Skill of n1 minus skill of n2, paired bootstrap over the truth members: value, se, z."""
            boot = [(L(n2, cell, idx) - L(n1, cell, idx)) / L("K", cell, idx) for idx in rng.integers(0, B64, (1000, B64))]
            v = (L(n2, cell) - L(n1, cell)) / L("K", cell)
            se = float(np.std(boot))
            return [round(float(v), 4), round(se, 4), round(float(v / max(se, 1e-9)), 2)]

        out["budget_curve"] = dict(
            note="skill = 1 - L / L(K), L the fair energy score pooled over items (truth members x 6 anchors x 4 horizons "
                 "at 64 px); value, bootstrap se over truth members. K = long-run distribution (the other members, all "
                 "ticks from 80 on); Ktick = the other members at the target tick. Budget R in 64 px episode equivalents "
                 "(px-ticks): a policy named X32 at R uses round(R / 0.365) episodes at 32 px, X48 round(R / 0.692) at "
                 "48 px, X64 R exam-size episodes (with the parameters fixed and public this is also D(R) on R Lab "
                 "episodes). A = analog ensemble on (N, s_b) (At: also the tick); ridge = increments regressed on "
                 "(1, s, s^2, N) per horizon, residuals resampled; ridgeL1 = the same on the 12 level-1 summaries of the anchor "
                 "tick; law / lin / const = the level-2 law iterated in "
                 "8-tick steps, the round-5 control without the selection term, constant drift; _noscale = law without "
                 "the box-size scaling of its noise; A32tile = analog on synthetic episodes pooled from four 32 px "
                 "members; +res2 = the same plus a linear correction of the mean fitted on 2 exam-size Lab episodes; "
                 "_fss32+48 = law (or control) constants extrapolated linearly in 1 / area from the whole 32 and 48 px "
                 "pools; ridge_fss32+48 = the regression with every coefficient linear in 1 / area, read at 64 px. "
                 "Cells: all, |h64 (64 ticks ahead), |s_b (kind share only).",
            scale_sd=[round(float(v), 4) for v in scale], truth_members=B64, items_per_member=len(items),
            L_K={c or "all": round(float(L("K", c)), 4) for c in CELLS},
            skill={c or "all": {k: skill(k, c) for k in sorted(pol) if k != "K"} for c in CELLS})
        cmp_ = {}
        pairs_ = [("law64", "A64"), ("law64", "ridge64"), ("law64", "lin64"), ("law64", "const64"), ("ridge64", "A64"),
                  ("ridgeL1_64", "ridge64"), ("law64", "ridgeL1_64"), ("At64", "A64"), ("law32", "A32"), ("law32", "lin32"), ("law32", "law32_noscale"), ("A32tile", "A32"),
                  ("A64", "A32"), ("A64", "A32tile"), ("law64", "law32"), ("ridge64", "ridge32"), ("A64", "A48"),
                  ("law64", "law48"), (f"A32tile+res{N_LAB}", "A32tile"), ("law64", f"A32tile+res{N_LAB}")]
        for R in budgets:
            for cell in CELLS:
                for a_, b_ in pairs_:
                    n1, n2 = f"{a_}@R{R}", f"{b_}@R{R}"
                    if n1 in pol and n2 in pol:
                        cmp_[f"{a_} - {b_} {cell} @R{R}".replace("  ", " ")] = diff(n1, n2, cell)
        for cell in CELLS:
            for a_, b_ in (("law64@R2", f"A32tile+res{N_LAB}@R8"), ("law64@R2", "A64@R15"), ("law64@R1", "A64@R4"),
                           ("law64@R2", "A32tile@R15"), ("law_fss32+48", "law64@R15"), ("law_fss32+48", "law32@R15"),
                           ("law_fss32+48", "lin_fss32+48"), ("law_fss32+48", "A32tile@R15"), ("law_fss32+48", "A64@R15"),
                           ("law_fss32+48", "const_fss32+48"), ("law_fss32+48", "ridge_fss32+48"), ("law_fss32+48", "ridge32@R15"),
                           ("ridge_fss32+48", "ridge32@R15"), ("law_fss32+48", "ridge48@R8"), ("law_fss32+48", "law48@R8"),
                           ("ridge64@R15", "ridge32@R15"), ("ridge64@R15", "ridge48@R8"), ("law64@R15", "law48@R8")):
                if a_ in pol and b_ in pol:
                    cmp_[f"{a_} - {b_} {cell}".strip()] = diff(a_, b_, cell)
        out["budget_curve"]["paired_differences"] = dict(note="skill difference (first minus second), bootstrap se, z; paired over the truth members", **cmp_)

        # ---------------- 2b. horizon transfer: nothing at exam size is seen beyond tick T_CUT
        T_CUT = 140
        items_b = [(a_, h) for a_ in (140, 160, 180) for h in (32, 64, 96) if a_ + h <= T_EXAM]
        polb = {}

        def putb(name, i, Xf, y):
            d = polb.setdefault(name, {"all": np.zeros(B64), "s_b": np.zeros(B64), "n": np.zeros(B64)})
            d["all"][i] += fair_es(Xf, y, scale)
            d["s_b"][i] += fair_es(Xf[:, 1:2], y[1:2], scale[1:2])
            d["n"][i] += 1

        small8 = {H: int(round(8 / unit[H])) for H in (32, 48) if P[H] is not None and int(round(8 / unit[H])) <= P[H].shape[0]}
        for i in range(B64):
            others = np.array([j for j in range(B64) if j != i])
            clim = T64[others][:, LAB + 19:].reshape(-1, 2)
            r0 = np.random.default_rng([i, 1])
            full = T64[others]
            refs = {"C_law64_full@R15": ("law", law_fit(full, "law"), 1.0),
                    "C_ridgeit64_full@R15": ("ridge", ridge_it_fit([(full, 1.0, 1.0)]))}
            if fss_c:
                refs["law_fss32+48"] = ("law", fss_c["law"], 1.0)
                refs["lin_fss32+48"] = ("law", fss_c["lin"], 1.0)
            for (a_, h) in items_b:
                x0, y = T64[i, a_ - 1].copy(), T64[i, a_ + h - 1]
                putb("K", i, clim[r0.integers(0, len(clim), 64)], y)
                putb("Ktick", i, T64[others, a_ + h - 1], y)
                putb("persistence", i, np.tile(x0, (2, 1)), y)
                for name, m in refs.items():
                    putb(name, i, law_predict(m[1], x0, h, r0, m[2]) if m[0] == "law" else ridge_it_predict(m[1], x0, h, r0), y)
            for n_lab in budgets:
                for dr in range(n_draw):
                    r_ = np.random.default_rng([i, n_lab, dr, 7])
                    lab = T64[r_.choice(others, min(n_lab, len(others)), replace=False)]
                    mods = {f"{f}64cut": ("law", law_fit(lab, f, t_to=T_CUT), 1.0) for f in ("law", "lin", "const")}
                    mods["ridgeit64cut"] = ("ridge", ridge_it_fit([(lab, 1.0, 1.0)], t_to=T_CUT))
                    if n_lab in (2, 15) and dr < 2:
                        mods["analogit64cut"] = ("analog", analog_it_fit([(lab, 1.0, 1.0)], t_to=T_CUT))
                    for H, nH in small8.items():
                        sm = P[H][r_.choice(P[H].shape[0], nH, replace=False)]
                        ar = (EXAM_H / H) ** 2
                        mods[f"ridgeit{H}"] = ("ridge", ridge_it_fit([(sm, ar, 1.0)]))
                        mods[f"law{H}"] = ("law", law_fit(sm, "law"), ar)
                        mods[f"ridgeit{H}+lab"] = ("ridge", ridge_it_fit([(sm, ar, 1.0), (lab[:, :T_CUT], 1.0, 1.0)]))
                    for (a_, h) in items_b:
                        x0, y = T64[i, a_ - 1].copy(), T64[i, a_ + h - 1]
                        for name, m in mods.items():
                            if m[0] == "law":
                                Xf = law_predict(m[1], x0, h, r_, m[2])
                            elif m[0] == "ridge":
                                Xf = ridge_it_predict(m[1], x0, h, r_)
                            else:
                                Xf = analog_it_predict(m[1], x0, h, r_, fscale)
                            putb(f"{name}@n{n_lab}", i, Xf, y)

        def Lb(name, cell, idx=None):
            v = polb[name][cell] / polb[name]["n"]
            return v.mean() if idx is None else v[idx].mean()

        def skillb(name, cell):
            boot = [1 - Lb(name, cell, idx) / Lb("K", cell, idx) for idx in rng.integers(0, B64, (1000, B64))]
            return [round(float(1 - Lb(name, cell) / Lb("K", cell)), 4), round(float(np.std(boot)), 4)]

        def diffb(n1, n2, cell):
            boot = [(Lb(n2, cell, idx) - Lb(n1, cell, idx)) / Lb("K", cell, idx) for idx in rng.integers(0, B64, (1000, B64))]
            v = (Lb(n2, cell) - Lb(n1, cell)) / Lb("K", cell)
            se = float(np.std(boot))
            return [round(float(v), 4), round(se, 4), round(float(v / max(se, 1e-9)), 2)]

        cmpb = {}
        for n_lab in budgets:
            for cell in ("all", "s_b"):
                for a_, b_ in (("law64cut", "lin64cut"), ("law64cut", "const64cut"), ("law64cut", "ridgeit64cut"),
                               ("law64cut", "analogit64cut"), ("law64cut", "ridgeit32"), ("law64cut", "ridgeit32+lab"),
                               ("law32", "ridgeit32"), ("law64cut", "law32"), ("ridgeit32", "const64cut"), ("law64cut", "ridgeit48+lab"),
                               ("law64cut", "ridgeit48"), ("ridgeit32+lab", "ridgeit32")):
                    n1, n2 = f"{a_}@n{n_lab}", f"{b_}@n{n_lab}"
                    if n1 in polb and n2 in polb:
                        cmpb[f"{a_} - {b_} |{cell} @n{n_lab}"] = diffb(n1, n2, cell)
                for b_ in ("C_law64_full@R15", "C_ridgeit64_full@R15", "Ktick", "law_fss32+48"):
                    if b_ in polb:
                        cmpb[f"law64cut@n{n_lab} - {b_} |{cell}"] = diffb(f"law64cut@n{n_lab}", b_, cell)
        if "law_fss32+48" in polb:
            for cell in ("all", "s_b"):
                cmpb[f"law_fss32+48 - lin_fss32+48 |{cell}"] = diffb("law_fss32+48", "lin_fss32+48", cell)
                cmpb[f"law_fss32+48 - C_law64_full@R15 |{cell}"] = diffb("law_fss32+48", "C_law64_full@R15", cell)
        out["horizon_transfer"] = dict(
            note=f"items: anchors 140, 160, 180 and horizons 32, 64, 96 ticks (within 260); every exam-size source is cut at tick "
                 f"{T_CUT} (pairs within ticks 61..{T_CUT}): X64cut@n = fitted on n exam-size episodes cut there (n Lab "
                 "episodes under a tick budget, or n short exam-size simulations: 0.54 n cost units). All models iterate "
                 "8-tick steps: law / lin / const as above; ridgeit = generic autoregression on (1, s, s^2, N); analogit = "
                 "analog steps (run at n = 2 and 15 only, 2 draws: it is slow and always negative). X32, X48 = fitted on full-length small-box episodes worth 8 cost units (naive rescale); "
                 "+lab = the small-box data pooled half and half with the cut Lab data; C_ = references fitted on 15 "
                 "full exam-size episodes; _fss32+48 as above. skill = 1 - L / L(K); value, bootstrap se over truths.",
            items=items_b, small_box_episodes_at_8_units=small8,
            skill={c: {k: skillb(k, c) for k in sorted(polb) if k != "K"} for c in ("all", "s_b")},
            paired_differences=dict(note="first minus second: skill difference, bootstrap se, z (paired over truths)", **cmpb))

    # ---------------- 3. state-given screen
    def ld(name):
        f = os.path.join(S, name)
        return np.load(f) if os.path.exists(f) else None

    base, o = ld("scr_base.npz"), ld("scr_b_none_dt1.npz")
    if o is not None:
        x0 = base["l2"][:, -1]                                             # (J, 2)
        A0 = json.loads(str(o["meta"]))["A0"]
        J, R, HZ, _ = o["l2"].shape
        hs = [h for h in HS if h <= HZ]
        climK = T64[:, LAB + 19:].reshape(-1, 2)
        climK = climK[np.random.default_rng(5).integers(0, len(climK), 64)]

        def tiles_of(d):
            n, nb = d["n"], d["nb"]                                        # (4, J, R, HZ)
            tot = np.stack([n.sum(0), nb.sum(0) / np.maximum(n.sum(0), 1.0)], -1)
            one = np.stack([n * 4.0, nb / np.maximum(n, 1.0)], -1)
            return tot, one

        def screen(truth, fcs):
            """truth (J, R, HZ, 2); fcs name -> f(j, r, h) -> (M, 2). Per state and horizon mean fair energy score,
            then (L - L(O)) / (L(K) - L(O)) per horizon (pooled over states) and over all horizons per state."""
            Ls = {k: np.array([[np.mean([fair_es(f(j, r, h), truth[j, r, h - 1], scale) for r in range(R)]) for h in hs]
                               for j in range(J)]) for k, f in fcs.items()}                     # (J, nh)
            res = {}
            for k, v in Ls.items():
                if k in ("O", "K"):
                    continue
                per_h = (v.mean(0) - Ls["O"].mean(0)) / (Ls["K"].mean(0) - Ls["O"].mean(0))
                per_j = (v.mean(1) - Ls["O"].mean(1)) / (Ls["K"].mean(1) - Ls["O"].mean(1))
                jk = [np.delete(v, j, 0).mean() - np.delete(Ls["O"], j, 0).mean() for j in range(J)]
                jk = np.array(jk) / np.array([np.delete(Ls["K"], j, 0).mean() - np.delete(Ls["O"], j, 0).mean() for j in range(J)])
                res[k] = dict(per_horizon={str(h): round(float(x), 3) for h, x in zip(hs, per_h)},
                              all=round(float((v.mean() - Ls["O"].mean()) / (Ls["K"].mean() - Ls["O"].mean())), 3),
                              jackknife_se_states=round(float(np.sqrt((J - 1) / J * ((jk - jk.mean()) ** 2).sum())), 3),
                              per_state=[round(float(x), 3) for x in per_j])
            return res, {k: [round(float(x), 4) for x in v.mean(0)] for k, v in Ls.items()}

        scr = {"note": "(L(surrogate) - L(O)) / (L(K) - L(O)): 0 = as good as the oracle, 1 = no better than the long-run "
                       f"distribution. {J} states at tick {A0} x {R} fresh-noise branches; O = the other branches of the same "
                       "state under the same arm (leave-one-out; every surrogate ensemble also leaves out the branch that "
                       "shares the truth's noise key, so all have 7 members except where stated); horizons in ticks; "
                       "f = cost as a fraction of simulating the question once per member"}
        for arm in ("none", "aimed"):
            tr_ = ld(f"scr_b_{arm}_dt1.npz")
            if tr_ is None:
                continue
            tr = tr_["l2"]
            fcs = {"O": lambda j, r, h: np.delete(tr[j], r, 0)[:, h - 1],
                   "K": lambda j, r, h: climK,
                   "tick climatology (the 64 px pool at the target tick)": lambda j, r, h: T64[:, A0 + h - 1],
                   "persistence f=0": lambda j, r, h: np.tile(x0[j], (2, 1)),
                   "truncated horizon f=1/4": lambda j, r, h: np.delete(tr[j], r, 0)[:, h // 4 - 1],
                   "truncated horizon f=1/2": lambda j, r, h: np.delete(tr[j], r, 0)[:, h // 2 - 1],
                   "three members f=3/7 of the ensemble": lambda j, r, h: np.delete(tr[j], r, 0)[:3, h - 1]}
            if arm != "none":
                fcs["oracle ignoring the program"] = lambda j, r, h: np.delete(o["l2"][j], r, 0)[:, h - 1]
            for dtf in (2, 5):
                d = ld(f"scr_b_{arm}_dt{dtf}.npz")
                if d is not None:
                    fcs[f"coarse step x{dtf} f=1/{dtf}"] = (lambda j, r, h, d=d: np.delete(d["l2"][j], r, 0)[:, h - 1])
            t = ld(f"scr_t_{arm}.npz")
            if t is not None:
                tot, one = tiles_of(t)
                fcs["four 32 px tiles f=1"] = lambda j, r, h, tot=tot: np.delete(tot[j], r, 0)[:, h - 1]
                fcs["one 32 px tile f=1/4"] = lambda j, r, h, one=one: np.delete(one[r % 4, j], r, 0)[:, h - 1]
            res, Ls = screen(tr, fcs)
            scr[arm] = dict(screen=res, L_per_horizon=Ls, horizons=hs, nats_mean=round(float(tr_["nats"].mean()), 1))
            if t is not None:
                s0 = t["nb0"].sum(0) / np.maximum(t["n0"].sum(0), 1.0)
                scr[arm]["mean_change"] = {
                    str(h): dict(s_b_oracle=round(float((tr[:, :, h - 1, 1] - x0[:, None, 1]).mean()), 4),
                                 s_b_tiles=round(float((tot[:, :, h - 1, 1] - s0).mean()), 4),
                                 N_oracle=round(float((tr[:, :, h - 1, 0] - x0[:, None, 0]).mean()), 3),
                                 N_tiles=round(float((tot[:, :, h - 1, 0] - t["n0"].sum(0)).mean()), 3)) for h in hs}
                scr[arm]["tiles_start"] = dict(N_sum_of_tiles=t["n0"].sum(0)[:, 0].tolist(), N_exam_box=x0[:, 0].tolist(),
                                               s_b_tiles=s0[:, 0].round(3).tolist(), s_b_exam_box=x0[:, 1].round(3).tolist(),
                                               finite=bool(t["finite"]))
            for dtf in (2, 5):
                d = ld(f"scr_b_{arm}_dt{dtf}.npz")
                if d is not None:
                    scr[arm][f"coarse_x{dtf}_mean_change"] = {
                        str(h): dict(s_b=round(float((d["l2"][:, :, h - 1, 1] - x0[:, None, 1]).mean()), 4),
                                     N=round(float((d["l2"][:, :, h - 1, 0] - x0[:, None, 0]).mean()), 3)) for h in hs}
                    scr[arm][f"coarse_x{dtf}_finite"] = bool(d["finite"])
        inp = {}
        for arm in ("blind", "aimed", "regional"):
            d = ld(f"scr_b_{arm}_dt1.npz")
            if d is None:
                continue
            row = {"nats_mean": round(float(d["nats"].mean()), 1)}
            for h in hs:
                dd = d["l2"][:, :, h - 1] - o["l2"][:, :, h - 1]           # paired: same process-noise keys
                sd = o["l2"][:, :, h - 1].std(1, ddof=1).mean(0)
                row[str(h)] = dict(
                    mean_shift=[round(float(dd[..., 0].mean()), 3), round(float(dd[..., 1].mean()), 4)],
                    se_states=[round(float(dd[..., 0].mean(1).std(ddof=1) / np.sqrt(J)), 3),
                               round(float(dd[..., 1].mean(1).std(ddof=1) / np.sqrt(J)), 4)],
                    rms_paired_change_over_oracle_sd=[round(float(np.sqrt((dd[..., c] ** 2).mean()) / max(sd[c], 1e-9)), 3) for c in (0, 1)])
            inp[arm] = row
        scr["inputs_paired_with_no_input"] = dict(
            note="(N, s_b) under a 200-nat program minus the same branch without input (same noise keys); mean shift, its se "
                 "over states, and the rms change in units of the no-input branches' sd at that horizon", **inp)
        out["screen"] = scr

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "summary.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out["finite_size"], indent=1))
    if MODE == "all":
        for k, v in out["budget_curve"]["skill"]["all"].items():
            print(k, v, out["budget_curve"]["skill"]["|h64"][k], out["budget_curve"]["skill"]["|s_b"][k])
        print("--- horizon transfer")
        for k, v in out["horizon_transfer"]["skill"]["all"].items():
            print(k, v, out["horizon_transfer"]["skill"]["s_b"][k])
    if "screen" in out:
        for arm in ("none", "aimed"):
            if arm in out["screen"]:
                for k, v in out["screen"][arm]["screen"].items():
                    print(arm, k, v["per_horizon"], "all", v["all"], "+-", v["jackknife_se_states"])
        print(json.dumps(out["screen"].get("inputs_paired_with_no_input"), indent=0)[:2500])


if __name__ == "__main__":
    main()
