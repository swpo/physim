"""analyse -- finite-size table, budget curve and state-given screen for study (c) at tiny size (numpy only).

  python -B analyse.py <scratch dir>        -> results/summary.json

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


def load_pool(S, H):
    L = []
    metas = []
    for f in sorted(glob.glob(os.path.join(S, f"b{H}_s*.npz"))):
        d = np.load(f)
        L.append(d["l2"].astype(float))
        metas.append(json.loads(str(d["meta"])))
    return (np.concatenate(L, 0), metas) if L else (None, [])


def fair_es(X, y, scale):
    """X (M, d) forecast members, y (d,) outcome; fair energy score in scaled units."""
    X = X / scale
    y = y / scale
    M = X.shape[0]
    a = np.sqrt(((X - y) ** 2).sum(-1) / X.shape[1]).mean()
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1) / X.shape[1])
    return a - D.sum() / (2 * M * (M - 1))


# ------------------------------------------------------------------ training pairs
def pairs(l2, lag, t_from=LAB + 1):
    """(state, increment over `lag` ticks) pairs from trajectories l2 (B, T, 2), ticks >= t_from. Index t holds the
    state after tick t + 1, so tick k is index k - 1."""
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
    """Per horizon: states (N in exam-box units, s_b) and increments (dN in exam-box units, ds)."""
    out = {}
    for h in HS:
        x, d = pairs(l2, h)
        out[h] = (np.stack([x[:, 0] * area_ratio, x[:, 1]], -1), np.stack([d[:, 0] * area_ratio, d[:, 1]], -1))
    return out


def analog_predict(model, x0, h, rng, fscale):
    X, D = model[h]
    dist = (((X - x0) / fscale) ** 2).sum(-1)
    k = int(np.clip(len(X) // 8, 8, 48))
    nn = np.argsort(dist)[:k]
    pick = nn[rng.integers(0, k, M_FC)]
    out = x0 + D[pick]
    out[:, 0] = np.maximum(out[:, 0], 0.0)
    out[:, 1] = np.clip(out[:, 1], 0.0, 1.0)
    return out


# ------------------------------------------------------------------ law family (level-2 effective law)
def law_fit(l2, form):
    """Constants of the level-2 law on increments over STEP ticks. form: 'law' ds = b1 s (1-s) + b2 (1-2s);
    'lin' ds = a0 + a1 (1-2s) (the round-5 checker's control: no selection term); 'const' ds = a0.
    Noise: Var ds = v (s (1-s) + C0) / N; N: dN = c1 (nstar - N), Var dN = q N. Returns per-box constants."""
    x, d = pairs(l2, STEP)
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
                                  tracker_overflow=sum(m["overflow"] for m in meta[H]),
                                  cost_units_per_episode=round(P[H].shape[1] * H * H / (T_EXAM * EXAM_H ** 2), 4))
                     for H in P if P[H] is not None}}

    # ---------------- 1. finite-size table
    fs = {}
    for H in P:
        if P[H] is None:
            continue
        l2 = P[H]
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
    B64 = T64.shape[0]
    late = T64[:, ANCH[0] - 1:]
    scale = np.array([late[..., 0].std(), late[..., 1].std()])
    fscale = np.array([2.5, 0.15])
    unit = {H: P[H].shape[1] * H * H / (T_EXAM * EXAM_H ** 2) for H in P if P[H] is not None}
    budgets = (1, 2, 4, 8, 15)
    n_draw = 6
    pol_scores = {}

    def add(name, i, val):
        pol_scores.setdefault(name, np.zeros(B64))[i] += val

    items = [(a, h) for a in ANCH for h in HS if a + h <= T_EXAM]
    per_item_cells = {}
    for i in range(B64):
        others = np.array([j for j in range(B64) if j != i])
        acc = {}
        for (a, h) in items:
            x0 = T64[i, a - 1].copy()
            y = T64[i, a + h - 1]
            # K: the other exam-size members at the target tick
            Xk = T64[others, a + h - 1]
            acc.setdefault("K", []).append(fair_es(Xk, y, scale))
            acc.setdefault("persistence", []).append(fair_es(np.tile(x0, (2, 1)), y, scale))
        for name in acc:
            add(name, i, np.mean(acc[name]))
        for R in budgets:
            sc = {}
            for dr in range(n_draw):
                r_ = np.random.default_rng([i, R, dr])
                tr64 = T64[r_.choice(others, min(R, len(others)), replace=False)]
                sets = {"64": (tr64, 1.0)}
                for H in (32, 48):
                    if P[H] is None:
                        continue
                    nH = int(round(R / unit[H]))
                    if nH < 1 or nH > P[H].shape[0]:
                        continue
                    trH = P[H][r_.choice(P[H].shape[0], nH, replace=False)]
                    sets[str(H)] = (trH, (EXAM_H / H) ** 2)
                    if H == 32 and nH >= 4:
                        sets["32tile"] = (pool_tiles(trH, r_, 2 * nH), 1.0)
                mods = {}
                for key, (tr, ar) in sets.items():
                    mods["A" + key] = ("analog", analog_fit(tr, ar), ar)
                    if key != "32tile":
                        for form in ("law", "lin", "const"):
                            mods[f"{form}{key}"] = ("law", law_fit(tr, form), ar)
                        if key != "64":
                            mods[f"law{key}_noscale"] = ("law_ns", law_fit(tr, "law"), ar)
                for (a, h) in items:
                    x0 = T64[i, a - 1].copy()
                    y = T64[i, a + h - 1]
                    for name, (kind, mod, ar) in mods.items():
                        if kind == "analog":
                            Xf = analog_predict(mod, x0, h, r_, fscale)
                        else:
                            Xf = law_predict(mod, x0, h, r_, ar, scale_noise=(kind == "law"))
                        sc.setdefault(name, []).append(fair_es(Xf, y, scale))
                        if h == 64:
                            sc.setdefault(name + "|h64", []).append(fair_es(Xf, y, scale))
                        Xs = Xf[:, 1:2]
                        sc.setdefault(name + "|s_b", []).append(fair_es(Xs, y[1:2], scale[1:2]))
            for name, v in sc.items():
                add(f"{name}@R{R}", i, np.mean(v))
        # reference cells for the K of the sub-cells
        accs = {"K|h64": [], "K|s_b": []}
        for (a, h) in items:
            y = T64[i, a + h - 1]
            Xk = T64[others, a + h - 1]
            if h == 64:
                accs["K|h64"].append(fair_es(Xk, y, scale))
            accs["K|s_b"].append(fair_es(Xk[:, 1:2], y[1:2], scale[1:2]))
        for name, v in accs.items():
            add(name, i, np.mean(v))
    # finite-size extrapolated law from the full 32 and 48 px pools (cost = both pools), same for every truth
    if P[48] is not None:
        cf = fss(law_fit(P[32], "law"), law_fit(P[48], "law"))
        cl = fss(law_fit(P[32], "lin"), law_fit(P[48], "lin"))
        for i in range(B64):
            sc = {}
            r_ = np.random.default_rng([i, 999])
            for (a, h) in items:
                x0 = T64[i, a - 1].copy()
                y = T64[i, a + h - 1]
                for name, c in (("law_fss32+48", cf), ("lin_fss32+48", cl)):
                    Xf = law_predict(c, x0, h, r_, 1.0)
                    sc.setdefault(name, []).append(fair_es(Xf, y, scale))
                    sc.setdefault(name + "|s_b", []).append(fair_es(Xf[:, 1:2], y[1:2], scale[1:2]))
                    if h == 64:
                        sc.setdefault(name + "|h64", []).append(fair_es(Xf, y, scale))
            for name, v in sc.items():
                add(name, i, np.mean(v))
        out["fss_constants"] = dict(law=cf, cost_units=round(P[32].shape[0] * unit[32] + P[48].shape[0] * unit[48], 2))

    def skill(name):
        cell = name.split("@")[0].split("|")[1] if "|" in name.split("@")[0] else None
        k = pol_scores["K" + ("|" + cell if cell else "")]
        v = pol_scores[name]
        boot = []
        for _ in range(2000):
            idx = rng.integers(0, B64, B64)
            boot.append(1 - v[idx].mean() / k[idx].mean())
        return [round(float(1 - v.mean() / k.mean()), 4), round(float(np.std(boot)), 4)]

    def diff(n1, n2):
        """Skill of n1 minus skill of n2 with a paired bootstrap over truth members: value, se, z."""
        cell = n1.split("@")[0].split("|")[1] if "|" in n1.split("@")[0] else None
        k = pol_scores["K" + ("|" + cell if cell else "")]
        a, b = pol_scores[n1], pol_scores[n2]
        boot = []
        for _ in range(2000):
            idx = rng.integers(0, B64, B64)
            boot.append((b[idx].mean() - a[idx].mean()) / k[idx].mean())
        v = (b.mean() - a.mean()) / k.mean()
        se = float(np.std(boot))
        return [round(float(v), 4), round(se, 4), round(float(v / max(se, 1e-9)), 2)]

    out["budget_curve"] = dict(
        note="skill = 1 - L / L(K), L the fair energy score pooled over items (16 truth members x 6 anchors x 4 "
             "horizons at 64 px); value, bootstrap se over truth members. Budget R in 64 px episode equivalents "
             "(px-ticks); a policy named X32 at R uses round(R / 0.365) episodes at 32 px, X48 round(R / 0.692) at "
             "48 px. A = analog ensemble (generic), law / lin / const = level-2 law, the round-5 control without "
             "the selection term, constant drift; _noscale = law without the box-size scaling of the noise; "
             "32tile = analog on synthetic episodes pooled from four 32 px members. Cells: all, |h64 (64 ticks "
             "ahead), |s_b (kind share only). K = the other 15 members at the target tick. With the parameters "
             "fixed and public, a policy trained on R exam-size simulations is also D(R) on R Lab episodes.",
        scale_sd=[round(float(s), 4) for s in scale], L_K=round(float(pol_scores["K"].mean()), 4),
        skill={k: skill(k) for k in sorted(pol_scores) if not k.startswith("K")},
    )
    cmp_ = {}
    for R in budgets:
        for cell in ("", "|h64", "|s_b"):
            for a, b in (("law64", "A64"), ("law64", "lin64"), ("law64", "const64"), ("law32", "A32"), ("law32", "lin32"),
                         ("law32", "law32_noscale"), ("A32tile", "A32"), ("A64", "A32"), ("A64", "A32tile"),
                         ("law64", "law32"), ("A64", "A48"), ("law64", "law48")):
                n1, n2 = f"{a}{cell}@R{R}", f"{b}{cell}@R{R}"
                if n1 in pol_scores and n2 in pol_scores:
                    cmp_[f"{a}{cell} - {b}{cell} @R{R}"] = diff(n1, n2)
    if "law_fss32+48" in pol_scores:
        for cell in ("", "|h64", "|s_b"):
            for b in ("law64@R15", "A64@R15", "law32@R15", "A32tile@R15"):
                nb = b.split("@")[0] + cell + "@" + b.split("@")[1]
                if nb in pol_scores:
                    cmp_[f"law_fss32+48{cell} - {nb}"] = diff("law_fss32+48" + cell, nb)
            cmp_[f"law_fss32+48{cell} - lin_fss32+48{cell}"] = diff("law_fss32+48" + cell, "lin_fss32+48" + cell)
    out["budget_curve"]["paired_differences"] = dict(note="skill difference, bootstrap se, z (paired over the 16 truth members)", **cmp_)

    # ---------------- 3. state-given screen
    fo, ft, fi, fb = (os.path.join(S, f"scr_{k}.npz") for k in ("oracle", "tiles", "inputs", "base"))
    if os.path.exists(fo):
        o = np.load(fo)
        tr = o["none"]                                  # (J, R, HZ, 2)
        J, R, HZ, _ = tr.shape
        A0 = json.loads(str(o["meta"]))["A0"]
        x0 = np.load(fb)["l2"][:, -1]                   # (J, 2)
        scr = {}
        hs = [h for h in HS if h <= HZ]

        def score_set(fc_of):
            """Mean fair energy score over states, truths (leave-one-out) and horizons. fc_of(j, r, h) -> (M, 2)."""
            res = {h: [] for h in hs}
            for j in range(J):
                for r in range(R):
                    for h in hs:
                        res[h].append(fair_es(fc_of(j, r, h), tr[j, r, h - 1], scale))
            return {h: float(np.mean(v)) for h, v in res.items()}

        Ls = {"O": score_set(lambda j, r, h: np.delete(tr[j], r, 0)[:, h - 1]),
              "K": score_set(lambda j, r, h: T64[:, min(A0 + h, T64.shape[1]) - 1]),
              "persistence_f0": score_set(lambda j, r, h: np.tile(x0[j], (2, 1))),
              "truncated_f1/4": score_set(lambda j, r, h: np.delete(tr[j], r, 0)[:, h // 4 - 1]),
              "truncated_f1/2": score_set(lambda j, r, h: np.delete(tr[j], r, 0)[:, h // 2 - 1]),
              "three_members_f3/7": score_set(lambda j, r, h: np.delete(tr[j], r, 0)[:3, h - 1])}
        if os.path.exists(ft):
            t = np.load(ft)
            n, nb = t["n"], t["nb"]                     # (4, J, R, HZ)
            tot = np.stack([n.sum(0), nb.sum(0) / np.maximum(n.sum(0), 1.0)], -1)      # (J, R, HZ, 2)
            one = np.stack([n * 4.0, nb / np.maximum(n, 1.0)], -1)                     # (4, J, R, HZ, 2)
            Ls["tiles_f1"] = score_set(lambda j, r, h: tot[j, :, h - 1])
            Ls["one_tile_f1/4"] = {h: float(np.mean([score_set(lambda j, r, hh, q=q: one[q, j, :, hh - 1])[h] for q in range(4)]))
                                   for h in hs}
            scr["tiles_start"] = dict(N_sum_of_tiles=t["n0"].sum(0)[:, 0].tolist(), N_exam_box=x0[:, 0].tolist(),
                                      s_b_tiles=(t["nb0"].sum(0)[:, 0] / np.maximum(t["n0"].sum(0)[:, 0], 1)).round(3).tolist(),
                                      s_b_exam_box=x0[:, 1].round(3).tolist(), finite=bool(t["finite"]))
            scr["mean_s_b_change_over_horizon"] = {
                str(h): dict(oracle=round(float((tr[:, :, h - 1, 1] - x0[:, None, 1]).mean()), 4),
                             tiles=round(float((tot[:, :, h - 1, 1] - (t["nb0"].sum(0) / np.maximum(t["n0"].sum(0), 1))).mean()), 4),
                             oracle_N=round(float((tr[:, :, h - 1, 0] - x0[:, None, 0]).mean()), 3),
                             tiles_N=round(float((tot[:, :, h - 1, 0] - t["n0"].sum(0)).mean()), 3)) for h in hs}
        scr["L"] = {k: {str(h): round(v[h], 4) for h in hs} for k, v in Ls.items()}
        scr["screen_1_minus_skill"] = {
            k: {**{str(h): round((v[h] - Ls["O"][h]) / (Ls["K"][h] - Ls["O"][h]), 3) for h in hs},
                "all": round((np.mean(list(v.values())) - np.mean(list(Ls["O"].values())))
                             / (np.mean(list(Ls["K"].values())) - np.mean(list(Ls["O"].values()))), 3)}
            for k, v in Ls.items() if k not in ("O", "K")}
        scr["note"] = ("(L(surrogate) - L(O)) / (L(K) - L(O)) per horizon in ticks: 0 = as good as the oracle, 1 = no better "
                       "than climatology. O = leave-one-out over the fresh-noise branches of the same state; K = the 64 px "
                       "pool at the target tick; J states x R branches: " + f"{J} x {R}; no error bars at this size")
        if os.path.exists(fi):
            d = np.load(fi)
            inp = {}
            for arm in ("blind", "aimed", "regional"):
                pr = d[arm]                              # (J, R, HZ, 2), same noise keys as the oracle branches
                row = {}
                for h in hs:
                    dd = pr[:, :, h - 1] - tr[:, :, h - 1]
                    sd = tr[:, :, h - 1].std(1, ddof=1).mean(0)
                    row[str(h)] = dict(
                        mean_shift_N=round(float(dd[..., 0].mean()), 3), mean_shift_s_b=round(float(dd[..., 1].mean()), 4),
                        se_N=round(float(dd[..., 0].mean(1).std(ddof=1) / np.sqrt(J)), 3),
                        se_s_b=round(float(dd[..., 1].mean(1).std(ddof=1) / np.sqrt(J)), 4),
                        rms_paired_change_over_oracle_sd=[round(float(np.sqrt((dd[..., c] ** 2).mean()) / max(sd[c], 1e-9)), 3) for c in (0, 1)])
                    # how much an oracle that ignores the program loses on program truths
                    l_ign = np.mean([fair_es(tr[j, :, h - 1], pr[j, r, h - 1], scale) for j in range(J) for r in range(R)])
                    l_own = np.mean([fair_es(np.delete(pr[j], r, 0)[:, h - 1], pr[j, r, h - 1], scale) for j in range(J) for r in range(R)])
                    row[str(h)]["L_oracle_ignoring_program"] = round(float(l_ign), 4)
                    row[str(h)]["L_oracle_with_program"] = round(float(l_own), 4)
                row["nats_mean"] = round(float(d[arm + "_nats"].mean()), 1)
                inp[arm] = row
            scr["inputs"] = inp
            scr["inputs_note"] = ("paired with the no-input branches (same process-noise keys); rms change is over all "
                                  "branches, in units of the no-input branches' sd at that horizon (N, s_b); "
                                  "se of the mean shift over the J states")
        out["screen"] = scr

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "summary.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out["finite_size"], indent=1))
    print(json.dumps({k: v for k, v in out["budget_curve"]["skill"].items() if "|" not in k}, indent=0))
    if "screen" in out:
        print(json.dumps(out["screen"], indent=1)[:4000])


if __name__ == "__main__":
    main()
