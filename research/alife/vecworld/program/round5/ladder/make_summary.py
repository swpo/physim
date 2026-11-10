"""make_summary -- results/summary.json of round 5 study ladder from the GPU job's saved outputs (CPU, no
simulation). Every number carries its source (job id, file, key).

Reads results/job/ (a copy of origin/gpu-jobs:jobs/<job>/out) and results/status.json:
  n<n>/scores.npz          per-item fair energy scores per truth, view and policy (the exam's own scorer)
  n<n>/identification.json posterior contraction per view, arm and budget
  n<n>/prior.json, truths.json, lab.json, train_info.json; info.json; scales.json
Scores are aggregated with vw.scoring (skill_report, oes) and round5/agentenv/evaluator/acceptance.py; this
file adds only bookkeeping (budget interpolation, cluster bootstrap over hidden worlds, rank correlations).

Policies per cell (view x number of hidden parameters n), roadmap notation:
  K climatology, O oracle (leave one out), C conditioned net at the true theta, PM at the box centre,
  P0 conditioned net with theta drawn from the conditioned prior (P0u: unconditioned net trained on
  prior-predictive simulations), S(N) conditioned net at posterior draws from N Lab episodes,
  D(N) the better (lower pooled L) of the unconditioned net and the ridge fitted to N Lab episodes,
  plugPM the simulator at the box centre run from the hidden state.
usage: python -B make_summary.py [--job r5-ladder-001] [--in results/job] [--status results/status.json]
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ladder_lib as LL  # noqa: E402

import numpy as np  # noqa: E402

from vw.scoring import oes, skill_report  # noqa: E402

ACC = LL.load_acceptance()
ap = argparse.ArgumentParser()
ap.add_argument("--job", default="r5-ladder-001")
ap.add_argument("--in", dest="inp", default=os.path.join(HERE, "results", "job"))
ap.add_argument("--status", default=os.path.join(HERE, "results", "status.json"))
ap.add_argument("--out", default=os.path.join(HERE, "results", "summary.json"))
ap.add_argument("--smoke", action="store_true", help="accept every cell (tiny test outputs)")
args = ap.parse_args()
JOB, IN = args.job, args.inp
r4 = lambda x: None if x is None or (isinstance(x, float) and not math.isfinite(x)) else round(float(x), 4)


def J(*p):
    return json.load(open(os.path.join(IN, *p)))


def src(f, key=""):
    return f"{JOB}:out/{f}" + (f" [{key}]" if key else "")


def cluster_boot(S, worlds, fn, n_boot=2000, seed=0):
    """SE of fn(S restricted to items) under a bootstrap over hidden worlds (all items of a world kept)."""
    ids = sorted(set(worlds.tolist()))
    groups = [np.flatnonzero(worlds == w) for w in ids]
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        idx = np.concatenate([groups[j] for j in rng.integers(0, len(ids), len(ids))])
        vals.append(fn({k: v[idx] for k, v in S.items()}))
    a = np.array(vals, float)
    return float(np.nanstd(a, ddof=1))


def agg_oes(S, name, valid):
    """Equal-weight mean over valid cells of the per-cell OES (vw.scoring.oes)."""
    return float(oes(S[name], S["K"], S["O"])[valid].mean())


def n_reach(budgets, vals, target, v0=None):
    """Smallest budget (log2-interpolated between measured budgets) at which the skill curve reaches the
    target; 0 if the zero-budget value v0 already does; None if it never does within the budgets."""
    if v0 is not None and v0 >= target:
        return 0.0
    if vals[0] >= target:
        return float(budgets[0])                      # reached at or before the smallest measured budget
    for a, b, va, vb in zip(budgets[:-1], budgets[1:], vals[:-1], vals[1:]):
        if vb >= target > va:
            f = (target - va) / (vb - va)
            return float(2 ** (math.log2(a) + f * (math.log2(b) - math.log2(a))))
    return None


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 4:
        return None
    rx, ry = np.argsort(np.argsort(x[ok])), np.argsort(np.argsort(y[ok]))
    return r4(np.corrcoef(rx, ry)[0, 1])


def main():
    info = J("info.json")
    budgets = info["config"]["budgets"]
    arm_budgets = info["config"]["arm_budgets"]
    hs = info["config"]["hs"]
    status = json.load(open(args.status)) if os.path.exists(args.status) else {}
    out = {"what": "round 5 study ladder (track 2): difficulty of the gliders wind world as a function of the "
                   "observed view (block 192, object 144, population 5 numbers) and of the number of hidden "
                   "parameters (1, 4, 8): reference ladder K, D(N), P0, PM, S(N), C, O per cell at Lab budgets "
                   "of 2-512 episodes; identification split by passive, blind and aimed inputs",
           "PILOT_NEVER_REUSE_AS_EXAM": True,
           "grader": info.get("grader"),
           "job": {"id": JOB, "backend": info["backend"], "devices": info["devices"], "versions": info["versions"],
                   "hours_in_script": r4(info.get("hours")), "member_ticks": info.get("member_ticks"),
                   "member_ticks_total": info.get("member_ticks_total"), "sets_done": info.get("sets_done"),
                   "failed_or_skipped": info.get("failed"), "seconds_per_set": info.get("seconds_per_set"),
                   "source": src("info.json"),
                   "status": {k: status.get(k) for k in ("state", "exit_code", "cost", "pod", "pods", "started_at",
                                                         "finished_at", "review")} if status else None},
           "config": {**info["config"], "source": src("info.json", "config")},
           "cells": {}, "identification_arms": {}, "hidden_sets": {}}
    rows = []
    for n in info.get("sets_done", []):
        d = f"n{n}"
        prior, truths, ident = J(d, "prior.json"), J(d, "truths.json"), J(d, "identification.json")
        z = np.load(os.path.join(IN, d, "scores.npz"), allow_pickle=True)
        nT = len(truths["truths"])
        out["hidden_sets"][str(n)] = {
            "names": prior["names"], "lo": prior["lo"], "hi": prior["hi"], "shrink_rule_tries": prior["shrink_rule_tries"],
            "frac_viable_box": prior["diag"]["frac_viable"], "prior_sd_u": prior["prior_sd_u"],
            "n_truths": nT, "n_viable_of_candidates": [truths["n_viable"], len(truths["candidates"])],
            "truths_theta": truths["truths"], "secret_commitment": truths["secret_commitment"],
            "source": src(f"{d}/prior.json") + "; " + src(f"{d}/truths.json")}
        worlds = np.concatenate([[i] * len(z[f"t{i}|classes"]) for i in range(nT)])
        for view in LL.VIEWS:
            names = sorted({k.split("|")[2] for k in z.files if k.count("|") == 2 and k.split("|")[1] == view})
            names = [a for a in names if all(f"t{i}|{view}|{a}" in z.files for i in range(nT))]
            if "C" not in names:
                continue
            S = {a: np.concatenate([z[f"t{i}|{view}|{a}"] for i in range(nT)]) for a in names}
            rep = skill_report({"climatology": S["K"], "oracle": S["O"], **{a: S[a] for a in names if a not in ("K", "O")}},
                               cells=[(view, h) for h in hs], n_boot=2000,
                               valid=np.ones(len(hs), bool) if args.smoke else None)
            valid = np.array(rep["valid"], bool)
            A, SE = rep["aggregate"], rep["se"]
            Lp = {a: float(S[a][:, valid].sum(1).mean()) for a in names}

            def gap(a, b):
                g = A[a] - A[b]
                se_w = cluster_boot(S, worlds, lambda T: agg_oes(T, a, valid) - agg_oes(T, b, valid), 1000)
                per = [agg_oes({k: v[worlds == w] for k, v in S.items()}, a, valid)
                       - agg_oes({k: v[worlds == w] for k, v in S.items()}, b, valid) for w in range(nT)]
                return {"gap": r4(g), "se_worlds": r4(se_w), "z_worlds": r4(g / se_w) if se_w > 0 else None,
                        "n_worlds_positive": int(np.sum(np.array(per) > 0)), "n_worlds": nT}
            bs = [b for b in budgets if f"S@{b}" in A]
            # data-only learner: the better of the net and the ridge at each budget (by pooled L)
            dbest = {b: min((f"D@{b}", f"Dr@{b}"), key=lambda a: Lp[a]) for b in bs}
            curves = {"S": [A[f"S@{b}"] for b in bs], "D_net": [A[f"D@{b}"] for b in bs],
                      "D_ridge": [A[f"Dr@{b}"] for b in bs], "D": [A[dbest[b]] for b in bs]}
            target = 0.9 * A["C"]
            n90 = {"S": n_reach(bs, curves["S"], target, v0=A["P0"]), "D": n_reach(bs, curves["D"], target),
                   "D_net": n_reach(bs, curves["D_net"], target), "D_ridge": n_reach(bs, curves["D_ridge"], target)}
            # value of theory: data-only budget / simulate-to-train budget at equal skill
            vot = {}
            for lab, tg, v0 in (("at_90pct_of_C", target, A["P0"]), ("at_skill_of_S_at_2", curves["S"][0], None)):
                nd = n_reach(bs, curves["D"], tg)
                ns = n_reach(bs, curves["S"], tg, v0=v0)
                ns_eff = max(ns, float(bs[0])) if ns is not None else None     # S is not measured below 2 episodes
                vot[lab] = {"N_D": r4(nd), "N_S": r4(ns), "ratio": (r4(nd / ns_eff) if nd is not None and ns_eff else None),
                            "ratio_is_lower_bound": bool(nd is None or (ns is not None and ns < bs[0])),
                            "ratio_lower_bound_if_D_never": (r4(bs[-1] / ns_eff) if nd is None and ns_eff else None)}
            acc = {}
            for b in bs:
                for p0name in ("P0", "P0u"):
                    r = ACC.shares({"K": S["K"], "C": S["C"], "P0": S[p0name], "S": S[f"S@{b}"], "D": S[dbest[b]]},
                                   valid, worlds=worlds, n_boot=2000, seed=b)
                    acc.setdefault(p0name, {})[str(b)] = {
                        "sigma": r4(r["sigma"]), "sigma_se_worlds": r4(r["sigma_worlds"]["se"]) if r.get("sigma_worlds") else None,
                        "null_is": r["null_is"], "D_is": dbest[b], "rho": r4(r["rho"]),
                        "rho_se_worlds": r4(r["rho_worlds"]["se"]) if r.get("rho_worlds") else None,
                        "pass_sigma": r["pass_sigma"], "pass_rho": r["pass_rho"]}
            sig_p0_only = (Lp["P0"] - Lp["C"]) / (Lp["K"] - Lp["C"])
            ck = f"{view}|mix"
            contr = {str(b): ident["summary"][f"{ck}|{b}"] for b in bs if f"{ck}|{b}" in ident["summary"]}
            tinfo = J(d, "train_info.json")
            nets = {k.split("|", 1)[1]: {"steps": v["steps"], "steps_asked": v.get("steps_asked", v["steps"]),
                                         "stopped_early": v.get("stopped_early"), "seconds": r4(v["seconds"])}
                    for k, v in tinfo.items() if isinstance(v, dict) and k.startswith(view + "|")}
            cell = {
                "n_hidden": n, "view": view,
                "nets": {**nets, "any_schedule_cut": bool(any(v["steps"] < v["steps_asked"] or v["stopped_early"]
                                                               for v in nets.values())),
                         "source": src(f"{d}/train_info.json")}, "dim": LL.DIM[view], "n_items": int(len(worlds)), "n_worlds": nT,
                "valid_cells": rep["valid"], "horizons": hs,
                "oes": {a: {"mean": r4(A[a]), "se_items": r4(SE[a])} for a in A if a not in ("climatology", "oracle")},
                "oes_per_cell": {a: [r4(x) for x in rep["oes"][a]] for a in ("C", "PM", "P0", "plugPM")},
                "pooled_L": {a: r4(Lp[a]) for a in names},
                "predictable_fraction_L": r4((Lp["K"] - Lp["O"]) / Lp["K"]),
                "params_matter": {"C_minus_PM": gap("C", "PM"), "C_minus_P0": gap("C", "P0"),
                                  "state_given_O_minus_plugPM": {
                                      "gap": r4(1.0 - A["plugPM"]), "se_items": r4(SE["plugPM"]),
                                      "note": "1 - OES of the simulator at the box centre run from the hidden state"},
                                  "C_minus_P0u": gap("C", "P0u")},
                "identifiability_mix": {b: {"sd_over_prior_sd_per_param": [r4(x) for x in c["contraction_mean"]],
                                            "geo_mean_contraction": r4(math.exp(c["log_contraction_mean_over_params"])),
                                            "in90_frac": r4(c["in90_frac"]), "hpd_le_90_frac": r4(c["hpd_le_90_frac"]),
                                            "ess_min": r4(c["ess_min"])} for b, c in contr.items()},
                "curves": {"budgets": bs, **{k: [r4(x) for x in v] for k, v in curves.items()},
                           "D_is": [dbest[b] for b in bs]},
                "budget_to_90pct_of_C": {k: r4(v) for k, v in n90.items()},
                "budget_note": "episodes; log2-interpolated; 0 = P0 already there; None = not reached by 512; "
                               "a value equal to the smallest budget means reached at or before it",
                "value_of_theory": vot,
                "S_minus_C": {str(b): gap(f"S@{b}", "C") for b in bs},
                "S_minus_P0": {str(b): gap(f"S@{b}", "P0") for b in bs},
                "acceptance": acc, "sigma_vs_P0_only": r4(sig_p0_only),
                "emulator": ident["emulators"].get(ck),
                "source": src(f"{d}/scores.npz") + "; " + src(f"{d}/identification.json", "summary")}
            out["cells"][f"n{n}|{view}"] = cell
            mid = str(bs[min(2, len(bs) - 1)])
            rows.append({"cell": f"n{n}|{view}", "n_hidden": n, "dim": LL.DIM[view],
                         "sigma_mid": acc["P0"][mid]["sigma"], "rho_2": acc["P0"][str(bs[0])]["rho"],
                         "C_minus_PM": cell["params_matter"]["C_minus_PM"]["gap"],
                         "C_minus_P0": cell["params_matter"]["C_minus_P0"]["gap"],
                         "state_given_gap": r4(1.0 - A["plugPM"]), "oes_C": r4(A["C"]),
                         "geo_contraction_2": cell["identifiability_mix"].get(str(bs[0]), {}).get("geo_mean_contraction"),
                         "geo_contraction_last": cell["identifiability_mix"].get(str(bs[-1]), {}).get("geo_mean_contraction"),
                         "projection_r2_mean": r4(np.mean(ident["emulators"][ck]["projection_r2"])) if ck in ident["emulators"] else None,
                         "D_last_minus_P0": r4(curves["D"][-1] - A["P0"]), "oes_P0": r4(A["P0"]),
                         "sigma_last": acc["P0"][str(bs[-1])]["sigma"], "sigma_first": acc["P0"][str(bs[0])]["sigma"],
                         "vot_at_S2": vot["at_skill_of_S_at_2"]["ratio"],
                         "N90_S": n90["S"], "N90_D": n90["D"],
                         "N90_D_rank": n90["D"] if n90["D"] is not None else 4.0 * bs[-1],
                         "predictable_fraction": cell["predictable_fraction_L"]})
            # identification by arm
            arms = {}
            for arm in ("passive", "blind", "aimed", "regional"):
                arms[arm] = {str(b): {"geo_mean_contraction": r4(math.exp(ident["summary"][f"{view}|{arm}|{b}"]["log_contraction_mean_over_params"])),
                                      "sd_over_prior_sd_per_param": [r4(x) for x in ident["summary"][f"{view}|{arm}|{b}"]["contraction_mean"]],
                                      "nats_mean": r4(ident["summary"][f"{view}|{arm}|{b}"]["nats_mean"]),
                                      "in90_frac": r4(ident["summary"][f"{view}|{arm}|{b}"]["in90_frac"])}
                             for b in arm_budgets if f"{view}|{arm}|{b}" in ident["summary"]}
            # paired over truths: log contraction (mean over parameters) aimed vs blind vs passive
            pt = {}
            for r in ident["per_truth_budget"]:
                if r["view"] == view and r["arm"] in arms:
                    pt[(r["arm"], r["n_episodes"], r["truth"])] = float(np.log(r["contraction_sd_ratio"]).mean())
            paired = {}
            for a, b_ in (("aimed", "blind"), ("aimed", "passive"), ("blind", "passive")):
                for nb in arm_budgets:
                    dd = np.array([pt[(a, nb, i)] - pt[(b_, nb, i)] for i in range(nT) if (a, nb, i) in pt and (b_, nb, i) in pt])
                    if len(dd) > 1:
                        se = dd.std(ddof=1) / math.sqrt(len(dd))
                        paired[f"{a}-{b_}|{nb}"] = {"mean_log_ratio": r4(dd.mean()), "se_truths": r4(se),
                                                    "t": r4(dd.mean() / se) if se > 0 else None,
                                                    "ratio_of_geo_contractions": r4(math.exp(dd.mean())), "n_truths": len(dd)}
            out["identification_arms"][f"n{n}|{view}"] = {
                "arms": arms, "paired_over_truths": paired,
                "note": "arms at equal ticks; blind (class e) and aimed (class c) spend the same nats on the same ticks "
                        "with the same number of coefficients; regional (class d) spends 300 nats; passive none. "
                        "A log ratio below 0 means the first arm contracts more.",
                "source": src(f"{d}/identification.json", "summary, per_truth_budget")}
    out["across_cells"] = {
        "table": rows,
        "rank_correlations_spearman": {
            f"{a} ~ {b}": spearman([r[a] for r in rows], [r[b] for r in rows])
            for a in ("sigma_mid", "sigma_last", "N90_D_rank", "rho_2", "C_minus_P0")
            for b in ("n_hidden", "dim", "C_minus_PM", "C_minus_P0", "state_given_gap", "geo_contraction_2",
                      "projection_r2_mean", "predictable_fraction", "oes_C") if a != b} if len(rows) >= 4 else None,
        "note": "one row per cell; sigma_mid = science share at the middle budget; descriptive only (at most 9 cells, "
                "which share simulations within a hidden set)"}
    # depth and hidden-set comparisons at a glance (ROADMAP: does depth alone cost over 30 times the episodes?)
    byc = {r["cell"]: r for r in rows}

    def ratio(a, b):
        return r4(a / b) if a and b else None
    depth, hidden = {}, {}
    for n in info.get("sets_done", []):
        rr = {v: byc.get(f"n{n}|{v}") for v in LL.VIEWS}
        if all(rr.values()):
            depth[f"n{n}"] = {
                "N90_D": {v: r4(rr[v]["N90_D"]) for v in rr}, "N90_S": {v: r4(rr[v]["N90_S"]) for v in rr},
                "N90_D_ratio_to_block": {v: ratio(rr[v]["N90_D"], rr["block"]["N90_D"]) for v in ("object", "pop")},
                "sigma_mid": {v: rr[v]["sigma_mid"] for v in rr}, "sigma_last": {v: rr[v]["sigma_last"] for v in rr},
                "rho_2": {v: rr[v]["rho_2"] for v in rr}, "C_minus_P0": {v: rr[v]["C_minus_P0"] for v in rr},
                "geo_contraction_2": {v: rr[v]["geo_contraction_2"] for v in rr}}
    for v in LL.VIEWS:
        rr = {n: byc.get(f"n{n}|{v}") for n in sorted(info.get("sets_done", []))}
        if all(rr.values()) and rr:
            hidden[v] = {k: {f"n{n}": (r4(rr[n][k]) if isinstance(rr[n][k], float) else rr[n][k]) for n in rr}
                         for k in ("N90_D", "N90_S", "sigma_mid", "sigma_last", "rho_2", "C_minus_P0", "C_minus_PM",
                                   "geo_contraction_2", "geo_contraction_last", "state_given_gap")}
    out["across_cells"]["by_depth_at_fixed_hidden_set"] = depth
    out["across_cells"]["by_hidden_set_at_fixed_view"] = hidden
    out["across_cells"]["caveats"] = [
        "the conditioned net, the P0u net and each D net are one trained net each (no training-seed variance in any SE)",
        "N90 is the budget at which a curve reaches 90% of the OES of C in that cell: a relative target, so a cell "
        "where C itself is poor is 'easy' by this measure; read it beside oes_C and sigma",
        "the views are levels of one exam per truth (same hidden states and programs), the hidden sets are different "
        "truths and simulations"]
    json.dump(out, open(args.out, "w"), indent=1)
    print("wrote", args.out)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
