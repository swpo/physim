"""Independent recomputation of the harness headline numbers from results/d2_scores.npz and the
stage JSONs (own aggregation and own paired bootstrap; does not import vw.scoring)."""
import json
import math
import sys

import numpy as np

R = "/home/user/evalwork/vecworld/program/track2/harness/results/"
Z = np.load(R + "d2_scores.npz", allow_pickle=False)
cells = [(1, 1), (1, 2), (1, 4), (1, 8), (1, 16), (2, 16), (2, 32)]
out = {}


def ok(clim, orc, z=3.0):
    d = clim - orc
    return d.mean(0) > z * d.std(0, ddof=1) / math.sqrt(d.shape[0])


def aggs(S, valid, idx=None):
    m = {k: (v if idx is None else v[idx]).mean(-2) for k, v in S.items()}
    den = m["climatology"] - m["oracle"]
    res = {}
    for k in S:
        num = m["climatology"] - m[k]
        res[k] = {"pooled": num[..., valid].sum(-1) / den[..., valid].sum(-1),
                  "mean": (num / den)[..., valid].mean(-1)}
    return res


def report(tag, n, valid, nb=4000, seed=12345):
    preds = sorted({k.split("/")[1] for k in Z.files if k.startswith(tag + "/") and k.count("/") == 1}
                   - {"classes", "climatology_v1", "oracle_v1"})
    S = {k: Z[f"{tag}/{k}"][:n] for k in preds}
    pt = aggs(S, valid)
    idx = np.random.default_rng(seed).integers(0, n, size=(nb, n))
    bt = aggs(S, valid, idx)
    return S, pt, bt


def gap(pt, bt, a, b, mode):
    g = float(pt[a][mode] - pt[b][mode])
    se = float((bt[a][mode] - bt[b][mode]).std(ddof=1))
    return [round(g, 4), round(se, 4), round(g / se, 2) if se > 0 else None]


v128 = ok(Z["n128R16/climatology"], Z["n128R16/oracle"])
out["valid_n128"] = v128.tolist()
out["valid_n256R4_own"] = ok(Z["n256R4/climatology"], Z["n256R4/oracle"]).tolist()
den = (Z["n128R16/climatology"] - Z["n128R16/oracle"]).mean(0)
out["denominator_fair_n128"] = [round(x, 4) for x in den]
w = den[v128] / den[v128].sum()
out["pooled_weight_per_valid_cell"] = [round(x, 3) for x in w]
out["pooled_weight_h<=4"] = round(float(w[:3].sum()), 3)
out["pooled_weight_h16_cells"] = round(float(w[4:].sum()), 3)

budgets = ("small_passive", "small_active", "large_passive", "large_active")
for alloc, (tag, n) in {"n64_R16": ("n128R16", 64), "n128_R16": ("n128R16", 128), "n256_R4": ("n256R4", 256)}.items():
    S, pt, bt = report(tag, n, v128)
    e = {}
    for mode in ("pooled", "mean"):
        e[mode] = {"agg": {k: [round(float(pt[k][mode]), 4), round(float(bt[k][mode].std(ddof=1)), 4)]
                           for k in ("B1@small_passive", "B1@large_passive", "B2@small_passive", "B2@large_passive",
                                     "B3_true_theta", "B2@zero", "ctrl_prior_mean")}}
        for b in budgets:
            ch = ["B0@" + b, "B1@" + b, "B2@" + b, "B3_true_theta", "oracle"]
            gs = {f"{c}-{a}": gap(pt, bt, c, a, mode) for a, c in zip(ch[:-1], ch[1:])}
            gs[f"B1@{b}-climatology"] = gap(pt, bt, "B1@" + b, "climatology", mode)
            gs["check1_passes(all z>=3)"] = all(v[2] is not None and v[2] >= 3 for k, v in gs.items()
                                                if not k.endswith("climatology"))
            e[mode][b] = gs
    out[alloc] = e
    if alloc == "n256_R4":       # EXAM's own rule on this exam's references
        own = ok(Z["n256R4/climatology"], Z["n256R4/oracle"])
        S2, pt2, bt2 = report(tag, n, own)
        out["n256_R4_own_cells_mean_se_B3"] = round(float(bt2["B3_true_theta"]["mean"].std(ddof=1)), 4)
        out["n256_R4_own_cells_mean_B3"] = round(float(pt2["B3_true_theta"]["mean"]), 4)

# v1 convention, B3 on n128 (stage B's oes_B3 v1_R16 uses stage-B's own valid cells = fair cells_ok)
S = {"climatology": Z["n128R16/climatology_v1"], "oracle": Z["n128R16/oracle_v1"], "B3": Z["n128R16/B3_true_theta/v1"]}
pt = aggs(S, v128)
out["B3_v1_mean_valid_n128"] = round(float(pt["B3"]["mean"]), 4)
Sf = {"climatology": Z["n128R16/climatology"], "oracle": Z["n128R16/oracle"], "B3": Z["n128R16/B3_true_theta"]}
out["B3_fair_mean_valid_n128"] = round(float(aggs(Sf, v128)["B3"]["mean"]), 4)
out["denominator_v1_n128"] = [round(x, 4) for x in (S["climatology"] - S["oracle"]).mean(0)]

# stage C: equal-weight mean of B1@small_passive (world 0), from per-cell mean scores
C0 = json.load(open(R + "stageC_w0.json"))
ms = C0["report"]["mean_score"]
v = np.array(C0["report"]["valid"])
cl, orc, b1 = (np.array(ms[k]) for k in ("climatology", "oracle", "B1@small_passive"))
o = (cl - b1) / (cl - orc)
out["stageC_w0_B1_small_passive_mean"] = round(float(o[v].mean()), 3)
out["stageC_w0_B1_small_passive_cell_1_16"] = round(float(o[4]), 2)

# theta headroom per world (pooled point, from per-cell mean scores)
for w_ in range(3):
    Cw = json.load(open(R + f"stageC_w{w_}.json"))
    ms, v = Cw["report"]["mean_score"], np.array(Cw["report"]["valid"])
    cl, orc = np.array(ms["climatology"]), np.array(ms["oracle"])
    pool = {k: float(((cl - np.array(ms[k]))[v]).sum() / ((cl - orc)[v]).sum())
            for k in ("ctrl_prior_mean", "B2@zero_noreweight", "B2@zero", "B2@small_passive", "B2@large_passive",
                      "B3_true_theta")}
    out[f"pooled_w{w_}"] = {k: round(x, 3) for k, x in pool.items()}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps(out, indent=1))
