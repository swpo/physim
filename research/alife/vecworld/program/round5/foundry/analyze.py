"""analyze -- from the GPU job's outputs to results/analysis.json (study foundry, round 5; CPU, seconds).

    python -B analyze.py <job_out_dir> [--job r5-foundry-001] [--out results]

<job_out_dir> is the job's $OUT (fetch.sh unpacks origin/gpu-jobs:jobs/<job_id>/out there). Every number
in analysis.json carries its source file inside the job's outputs (`src`).

Parts: types and gates over the prior; descriptors of the active worlds; which statistics of the weights
predict the types (single-feature AUC and Spearman rho, cross-validated logistic regressions on feature
groups, the linear-stability rule); the candidates at screen size and at certification size; the gliders
world by the same estimator against its published numbers; controls; throughput.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import criteria as CR  # noqa: E402

HZ = CR.HZ
# published gliders numbers (vw1/fresh/closure/results/summary.json, coarse view; vw1/fresh/README.md)
GLIDERS_PUB = dict(
    source="research/alife/vecworld/vw1/fresh/closure/results/summary.json (coarse) and vw1/fresh/README.md",
    ceiling_best_of=[0.991, 0.967, 0.849, 0.495, 0.136, 0.078],
    ceiling_linear_set=[0.988, 0.955, 0.800, 0.371, 0.126, 0.007],
    V_oracle=[0.00062, 0.00091, 0.00213, 0.00911, 0.0604, 0.312],
    V_ridge_p2=[0.0123, 0.0454, 0.2004, 0.6369, 0.8715, 1.0513],
    V_persistence=[0.0578, 0.2047, 0.6587, 1.5834, 2.1775, 2.1423],
    bodies_mean=7.4, body_length_px=12.8, ticks_per_body_length=7.8, fusions_per_100=22.5, fissions_per_100=22.3,
    spread_doubling_ticks=2.3, half_natural_spread_ticks=42)


def load_screen(d):
    files = sorted(f for f in os.listdir(os.path.join(d, "screen")) if f.startswith("chunk_"))
    parts = [dict(np.load(os.path.join(d, "screen", f))) for f in files]
    skip = ("thumb_u8", "thumb_scale", "thumb_index")
    m = {k: np.concatenate([p[k] for p in parts]) for k in parts[0] if k not in skip}
    th = {k: np.concatenate([p[k] for p in parts if k in p]) for k in skip if any(k in p for p in parts)}
    return m, th


def auc(score, y):
    """Area under the ROC curve of `score` for the boolean y (rank formula, ties averaged)."""
    from scipy.stats import rankdata
    y = np.asarray(y, bool)
    ok = np.isfinite(score)
    score, y = np.asarray(score)[ok], y[ok]
    n1, n0 = int(y.sum()), int((~y).sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(score)
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def logit_cv(X, y, folds=5, l2=1.0, seed=0, iters=30):
    """Cross-validated AUC of an L2 logistic regression on rank-normalised features (Newton steps)."""
    from scipy.stats import rankdata
    y = np.asarray(y, float)
    n = len(y)
    if y.sum() < 2 * folds or (n - y.sum()) < 2 * folds:
        return dict(auc=float("nan"), n_pos=int(y.sum()))
    X = np.nan_to_num(np.asarray(X, float), nan=0.0, posinf=0.0, neginf=0.0)
    R = np.stack([(rankdata(X[:, j]) - 0.5) / n for j in range(X.shape[1])], 1)
    Z = np.sqrt(2) * _erfinv(2 * R - 1)                               # normal scores
    Z = np.concatenate([Z, np.ones((n, 1))], 1)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    pred = np.zeros(n)
    for f in range(folds):
        te = perm[f::folds]
        tr = np.setdiff1d(perm, te)
        w = np.zeros(Z.shape[1])
        reg = l2 * np.eye(Z.shape[1])
        reg[-1, -1] = 0.0
        for _ in range(iters):
            p = 1 / (1 + np.exp(-np.clip(Z[tr] @ w, -30, 30)))
            g = Z[tr].T @ (p - y[tr]) + reg @ w
            Hh = (Z[tr] * (p * (1 - p))[:, None]).T @ Z[tr] + reg + 1e-9 * np.eye(Z.shape[1])
            w = w - np.linalg.solve(Hh, g)
        pred[te] = Z[te] @ w
    return dict(auc=auc(pred, y > 0.5), n_pos=int(y.sum()), n=int(n), folds=folds, l2=l2)


def _erfinv(x):
    from scipy.special import erfinv
    return erfinv(np.clip(x, -1 + 1e-12, 1 - 1e-12))


def frac(mask):
    n = len(mask)
    k = int(np.sum(mask))
    p = k / n
    return dict(n=k, of=n, frac=p, se=float(np.sqrt(max(p * (1 - p), 1e-12) / n)))


def q(v, qs=(0.1, 0.5, 0.9)):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    return [float(x) for x in np.quantile(v, qs)] if len(v) else [None] * len(qs)


FEATS = dict(
    prior_scalars=["log_beta", "log_alpha", "gam", "mu", "kappa_on", "kappa", "gr", "log_dens0", "log_dens1",
                   "log_dens_tot", "wq0", "wq1"],
    linear_stability=["lin_growth", "lin_growth_long", "lin_wavelength", "lin_omega", "lin_n_unstable"],
    jacobian=["affx_00", "affx_01", "affx_10", "affx_11", "aff_self_max", "aff_cross_prod", "aff_antisym",
              "aff_loc_self_max", "mob_self_min", "crowd", "drive", "xbar_frac0"],
    weight_norms=["w1_norm", "w2_aff_norm", "w2_mob_norm", "hid_sat"])


def weights_part(ws, t, g, src):
    targets = dict(structured=(t >= 3), active=(t >= 5), bodies_or_movers=(t >= 6), movers=(t == 7),
                   closure_gate=g["closure"], candidate=g["candidate"])
    names = sorted({n for v in FEATS.values() for n in v})
    from scipy.stats import spearmanr
    out = dict(src=src, targets={k: frac(v) for k, v in targets.items()}, single={}, groups={}, rules={})
    for tn, y in targets.items():
        rows = []
        for n in names:
            a = auc(ws[n], y)
            rows.append(dict(feature=n, auc=a, rho=float(spearmanr(ws[n], y.astype(float)).statistic)
                             if np.std(ws[n]) > 0 and 0 < y.sum() < len(y) else float("nan")))
        rows.sort(key=lambda r: -abs((r["auc"] if np.isfinite(r["auc"]) else 0.5) - 0.5))
        out["single"][tn] = rows[:10]
        out["groups"][tn] = {}
        for gn, fs in list(FEATS.items()) + [("all", names)]:
            X = np.stack([ws[n] for n in fs], 1)
            out["groups"][tn][gn] = logit_cv(X, y)
    # the linear-stability rule for structure
    for thr in (1e-4, 1e-3):
        pred = ws["lin_growth"] > thr
        y = targets["structured"]
        tp, fp, fn, tn_ = (pred & y).sum(), (pred & ~y).sum(), (~pred & y).sum(), (~pred & ~y).sum()
        out["rules"][f"lin_growth>{thr:g} -> structured"] = dict(
            predicted=int(pred.sum()), precision=float(tp / max(tp + fp, 1)), recall=float(tp / max(tp + fn, 1)),
            accuracy=float((tp + tn_) / len(y)))
    # conditional yields: how much a screen on the weights alone would enrich the draws
    for name, mask in (("lin_growth>1e-3", ws["lin_growth"] > 1e-3),
                       ("lin_growth>1e-3 & kappa=0", (ws["lin_growth"] > 1e-3) & (ws["kappa_on"] < 0.5)),
                       ("aff_cross_prod<0", ws["aff_cross_prod"] < 0),
                       ("lin_growth>1e-3 & aff_cross_prod<0", (ws["lin_growth"] > 1e-3) & (ws["aff_cross_prod"] < 0))):
        if mask.sum() > 0:
            out["rules"][f"yield | {name}"] = dict(
                n=int(mask.sum()), share_of_draws=float(mask.mean()),
                **{k: float(v[mask].mean()) for k, v in targets.items()},
                base={k: float(v.mean()) for k, v in targets.items()})
    return out


def world_row(d, i, t=None, g=None, s=None):
    keys = ["cv_cell", "pr", "moved", "wavelength", "nb_mean", "body_frac", "rg", "v_net", "v_inst", "body_speed_len",
            "events100", "fusions100", "fissions100", "births100", "deaths100", "survive", "age_mean", "gap_max",
            "gap_argmax_h", "twin_doubling", "twin_half_h", "twin_l1_32", "theta_l1_32", "var_static", "kind_frac0",
            "mean_S", "ovf_kept_ticks", "raw_peak"]
    r = {k: float(d[k][i]) for k in keys}
    for nm in ("ceil", "v_orc", "v_pred", "v_pers", "v_clim", "pl", "gap", "vp_main"):
        r[nm] = [float(d[f"{nm}{h}"][i]) for h in HZ]
    if t is not None:
        r["type"] = CR.TYPES[int(t[i])]
    if g is not None:
        r["gates"] = {k: bool(v[i]) for k, v in g.items()}
    if s is not None:
        r["score"] = float(s[i])
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_out")
    ap.add_argument("--job", default="r5-foundry-001")
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    ap.add_argument("--name", default="analysis.json")
    ap.add_argument("--sel", default="", help="index file of select_enriched.py: adds the yields per arm")
    a = ap.parse_args()
    D = a.job_out
    os.makedirs(a.out, exist_ok=True)
    st = json.load(open(os.path.join(D, "job_state.json")))
    T = st["stages"]["screen"]["sizes"]["T"]
    res = dict(job=a.job, platform=st.get("platform"), config=st.get("config"), ok=st.get("ok"), errors=st.get("errors"),
               seconds_total=st.get("seconds_total"), stages={k: v for k, v in st["stages"].items() if k != "screen"})
    scr = st["stages"]["screen"]
    res["screen_run"] = dict(src="job_state.json:stages.screen", sizes=scr["sizes"], chunk=scr["chunk"],
                             n_done=scr["n_done"], n_chunks=scr["n_chunks"], seconds=scr["seconds_total"],
                             member_ticks=int(sum(c["member_ticks"] for c in scr["chunks"])),
                             member_ticks_per_s_steady=scr.get("member_ticks_per_s_steady"),
                             first_chunk_seconds=scr["chunks"][0]["seconds"],
                             chunk_seconds_median=float(np.median([c["seconds"] for c in scr["chunks"][1:]]))
                             if len(scr["chunks"]) > 1 else None)
    # ---------------- types and gates
    m, thumbs = load_screen(D)
    idx = m["index"].astype(int)
    N = len(idx)
    d = CR.derive(m, T)
    t = CR.classify(d)
    g = CR.gates(d, t)
    s = CR.score(d, t)
    sc = dict(np.load(os.path.join(D, "thetas_scalars.npz")))
    ids = sc.pop("ids", None)                                         # prior index of every array position
    posmap = {int(v): i for i, v in enumerate(ids)} if ids is not None else None
    pidx = np.array([posmap[int(i)] for i in idx]) if posmap else idx  # positions of the screened draws
    P = (lambda i: posmap[int(i)]) if posmap else (lambda i: int(i))
    kap = sc["kappa"][pidx] > 0
    types = {}
    for i, name in enumerate(CR.TYPES):
        types[name] = dict(frac(t == i), kappa0=frac((t == i)[~kap]), kappa_pos=frac((t == i)[kap]))
    res["types"] = dict(src="screen/chunk_*.npz via criteria.classify", n=N, table=types,
                        thresholds=CR.THRESHOLDS)
    res["gates"] = dict(src="screen/chunk_*.npz via criteria.gates",
                        **{k: dict(frac(v), kappa0=frac(v[~kap]), kappa_pos=frac(v[kap])) for k, v in g.items()})
    res["validity"] = dict(src="screen/chunk_*.npz", finite_all=bool((d["finite"] > 0.5).all()),
                           mass_drift_max=float(np.nanmax(d["mass_drift"])), xmin_min=float(np.nanmin(d["xmin"])),
                           kind_drift_max_kappa0=float(np.nanmax(m["kind_drift"][~kap])) if (~kap).any() else None,
                           smax_max=float(np.nanmax(d["smax"])), pr_min=float(np.nanmin(d["pr"])))
    act = t >= 5
    desc = {}
    for k in ("cv_cell", "pr", "wavelength", "moved", "vp_main1", "vp_main16", "nb_mean", "body_frac", "rg", "v_net",
              "events100", "ceil1", "ceil4", "ceil8", "ceil16", "ceil32", "v_orc8", "gap_max", "pl8", "twin_doubling",
              "twin_half_h", "var_static"):
        desc[k] = dict(all=q(d[k]), active=q(d[k][act]) if act.any() else None,
                       movers=q(d[k][t == 7]) if (t == 7).any() else None)
    res["descriptors_q10_q50_q90"] = dict(src="screen/chunk_*.npz via criteria.derive", table=desc)
    # closure profile classes among active worlds
    c1, c8, c32 = d["ceil1"], d["ceil8"], d["ceil32"]
    res["closure_classes_active"] = dict(
        src="screen/chunk_*.npz", n_active=int(act.sum()),
        closed_through_32=frac((c32 > 0.9)[act]) if act.any() else None,
        half_lost_by_8=frac((c8 < 0.5)[act]) if act.any() else None,
        half_lost_by_32_not_8=frac(((c32 < 0.5) & (c8 >= 0.5))[act]) if act.any() else None,
        gap_ge_0p1=frac((d["gap_max"] >= 0.1)[act]) if act.any() else None,
        chaotic_half_spread_within_32=frac(np.isfinite(d["twin_half_h"])[act]) if act.any() else None)
    # ---------------- weights
    ws_all = dict(np.load(os.path.join(D, "wstats.npz")))
    ws_all.pop("ids", None)
    ws = {k: v[pidx] for k, v in ws_all.items()}
    res["weights"] = weights_part(ws, t, g, "wstats.npz against screen/chunk_*.npz")
    res["weights"]["lin_unstable_share"] = frac(ws["lin_growth"] > 1e-4)
    # ---------------- candidates (screen size)
    order = np.argsort(-s, kind="stable")
    cand = [int(i) for i in order if g["candidate"][i]]
    res["candidates_screen"] = dict(src="screen/chunk_*.npz", n_candidates=len(cand),
                                    top=[dict(draw=int(idx[i]), **world_row(d, i, t, g, s),
                                              theta={k: (float(v[pidx[i]]) if v.ndim == 1 else [float(x) for x in v[pidx[i]]])
                                                     for k, v in sc.items()}) for i in order[:40]])
    # ---------------- certification
    cdir = os.path.join(D, "cert")
    if os.path.exists(os.path.join(cdir, "eps010.npz")):
        cz = st["stages"]["certify"]["sizes"]
        runs = {}
        for name in ("eps010", "eps003", "eps030", "hyp010"):
            p = os.path.join(cdir, name + ".npz")
            if os.path.exists(p):
                mm = dict(np.load(p))
                dd = CR.derive(mm, cz["T"])
                runs[name] = (mm, dd)
        mm, dd = runs["eps010"]
        ci = mm["index"].astype(int)
        tt = CR.classify(dd)
        gg = CR.gates(dd, tt)
        ss = CR.score(dd, tt)
        rows = []
        pos = {int(v): k for k, v in enumerate(idx)}
        for j, i in enumerate(ci):
            r = dict(draw=int(i), **world_row(dd, j, tt, gg, ss))
            r["se"] = {nm: [float(x) for x in mm[nm + "_se"][j]] for nm in ("v_orc", "v_pred", "pl")}
            r["pl8_by_neighbour"] = {name: float(runs[name][1]["pl8"][j]) for name in runs}
            r["pl_by_neighbour"] = {name: [float(runs[name][1][f"pl{h}"][j]) for h in HZ] for name in runs}
            r["theta_l1_32_by_neighbour"] = {name: float(runs[name][1]["theta_l1_32"][j]) for name in runs}
            r["rerun_spread"] = {k: [float(runs[name][1][k][j]) for name in runs]
                                 for k in ("ceil8", "v_orc8", "nb_mean", "v_net", "events100", "gap_max")}
            if i in pos:
                r["screen"] = dict(score=float(s[pos[i]]), type=CR.TYPES[int(t[pos[i]])],
                                   candidate=bool(g["candidate"][pos[i]]),
                                   **{k: float(d[k][pos[i]]) for k in ("ceil1", "ceil8", "ceil32", "gap_max", "v_orc8",
                                                                       "nb_mean", "v_net", "events100", "pl8")})
            r["theta"] = {k: (float(v[P(i)]) if v.ndim == 1 else [float(x) for x in v[P(i)]]) for k, v in sc.items()}
            r["weights"] = {k: float(ws_all[k][P(i)]) for k in ("lin_growth", "lin_wavelength", "lin_omega", "affx_00",
                                                                "affx_01", "affx_10", "affx_11", "aff_cross_prod")}
            rows.append(r)
        rows.sort(key=lambda r: -r["score"])
        scr_c = np.array([r.get("screen", {}).get("candidate", False) for r in rows])
        cer_c = np.array([r["gates"]["candidate"] for r in rows])
        res["certification"] = dict(
            src="cert/eps010.npz (+ eps003, eps030, hyp010 for the neighbour sizes)", sizes=cz, n=len(rows),
            n_candidate_at_screen=int(scr_c.sum()), n_candidate_at_cert=int(cer_c.sum()),
            n_candidate_both=int((scr_c & cer_c).sum()),
            gates_at_cert={k: int(v.sum()) for k, v in gg.items()},
            types_at_cert={CR.TYPES[i]: int((tt == i).sum()) for i in range(len(CR.TYPES))}, worlds=rows)
    # ---------------- gliders by the same estimator
    for gname, key in (("ref_gliders.npz", "gliders_same_estimator"), ("ref_gliders_cert.npz", "gliders_cert_size")):
        gp = os.path.join(D, gname)
        if not os.path.exists(gp):
            continue
        gm = dict(np.load(gp))
        gst = st["stages"].get("gliders") or {}
        gs = gst.get("sizes") if key == "gliders_same_estimator" else (gst.get("cert_size") or {}).get("sizes")
        if not gs:                                                    # the job was cut before it recorded the sizes
            gs = dict(T=int(st["stages"]["screen"]["sizes"]["T"] if key == "gliders_same_estimator"
                            else st["stages"]["certify"]["sizes"]["T"]), note="sizes not in job_state.json")
        gd = CR.derive(gm, gs["T"])
        gt = CR.classify(gd)
        ggt = CR.gates(gd, gt)
        gsc = CR.score(gd, gt)
        n = len(gt)
        ms = lambda v: dict(mean=float(np.nanmean(v)), se=float(np.nanstd(v) / np.sqrt(max(n, 1))))
        ref = dict(src=gname, n_runs=n, sizes=gs,
                   types={CR.TYPES[i]: int((gt == i).sum()) for i in range(len(CR.TYPES))},
                   gates={k: int(v.sum()) for k, v in ggt.items()}, score=ms(gsc), published=GLIDERS_PUB)
        for nm in ("ceil", "ceil_raw", "v_orc", "v_pred", "v_pers", "v_clim", "pl", "gap", "vp_main"):
            ref[nm] = [ms(gd[f"{nm}{h}"]) for h in HZ]
        for k in ("nb_mean", "body_frac", "rg", "v_net", "body_speed_len", "events100", "fusions100", "fissions100",
                  "gap_max", "twin_doubling", "twin_half_h", "cv_cell", "pr", "moved", "wavelength", "survive"):
            ref[k] = ms(np.where(np.isfinite(gd[k]), gd[k], np.nan))
        ref["twin_half_h_finite"] = int(np.isfinite(gd["twin_half_h"]).sum())
        ref["mass_drift_max"] = float(np.nanmax(gd["mass_drift"]))
        res[key] = ref
    # ---------------- controls
    cp = os.path.join(D, "controls_diffusion.npz")
    if os.path.exists(cp):
        cm = dict(np.load(cp))
        cd = CR.derive(cm, T)
        ct = CR.classify(cd)
        res["controls_diffusion"] = dict(src="controls_diffusion.npz", n=len(ct),
                                         types={CR.TYPES[i]: int((ct == i).sum()) for i in range(len(CR.TYPES))},
                                         cv_cell=q(cd["cv_cell"]), vp_main1=q(cd["vp_main1"]), pl8=q(cd["pl8"]),
                                         v_orc8=q(cd["v_orc8"]), moved=q(cd["moved"]))
    # ---------------- arms of a prospective enrichment job
    if a.sel:
        sel = json.load(open(a.sel))
        targets = dict(structured=(t >= 3), active=(t >= 5), movers=(t == 7), closure_gate=g["closure"],
                       candidate=g["candidate"])
        arms = {}
        for arm in ("enriched", "control"):
            mk = np.isin(idx, np.asarray(sel[arm]))
            arms[arm] = dict(n=int(mk.sum()), planned=len(sel[arm]),
                             yields={k: frac(v[mk]) for k, v in targets.items()} if mk.any() else None,
                             types={CR.TYPES[i]: int((t[mk] == i).sum()) for i in range(len(CR.TYPES))},
                             score_q=q(s[mk]), n_score_above_0p5=int((s[mk] > 0.5).sum()))
        en, co = arms["enriched"]["yields"], arms["control"]["yields"]
        res["arms"] = dict(src="screen/chunk_*.npz + " + os.path.basename(a.sel), target=sel["target"], pool=sel["pool"],
                           prior_seed=sel["prior_seed"], share_selected=sel["prediction_from_job1"]["share_selected"],
                           prediction_from_job1=sel["prediction_from_job1"], arms=arms,
                           enrichment_observed={k: (en[k]["frac"] / co[k]["frac"] if co[k]["frac"] > 0 else None)
                                                for k in en} if en and co else None)
    with open(os.path.join(a.out, a.name), "w") as f:
        json.dump(res, f, indent=1, default=float)
    # a compact per-draw table for later use (types, score, a few descriptors): small, committed
    keep = ["cv_cell", "pr", "moved", "wavelength", "nb_mean", "body_frac", "rg", "v_net", "events100", "ceil1", "ceil4",
            "ceil8", "ceil16", "ceil32", "v_orc8", "gap_max", "pl8", "twin_doubling", "vp_main1", "vp_main16"]
    tab = dict(draw=idx.tolist(), type=[int(x) for x in t], score=[round(float(x), 4) for x in s],
               candidate=[bool(x) for x in g["candidate"]], types=list(CR.TYPES),
               **{k: [None if not np.isfinite(x) else round(float(x), 4) for x in d[k]] for k in keep})
    with open(os.path.join(a.out, "per_draw.json" if a.name == "analysis.json" else "per_draw_" + a.name), "w") as f:
        json.dump(tab, f, separators=(",", ":"))
    print("types", {k: v["n"] for k, v in types.items()})
    print("gates", {k: v["n"] for k, v in res["gates"].items() if isinstance(v, dict)})
    print("wrote", os.path.join(a.out, a.name))


if __name__ == "__main__":
    main()
