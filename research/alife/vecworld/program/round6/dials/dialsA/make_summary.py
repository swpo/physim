"""make_summary -- study A: results/summary.json from the job's outputs (CPU, seconds).

Reads results/<job>/scores.npz, info.json, train_info.json, presmoke/*.json and, if present, the runner's
status.json. Every declared criterion is computed by a_stats.criteria (DECLARED.md); everything else is under
"reported" and is never a criterion. Each block names its source (job id, file, key).

usage: python -B make_summary.py [--job r6-dialsA-001] [--dir results/job] [--budget 8] [--out results/summary.json]
"""
import argparse
import json
import os
import sys

sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a_stats as ST  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--job", default="r6-dialsA-001")
ap.add_argument("--dir", default=os.path.join(HERE, "results", "job"))
ap.add_argument("--budget", type=int, default=None)
ap.add_argument("--out", default=os.path.join(HERE, "results", "summary.json"))
args = ap.parse_args()
D = args.dir


def jload(name, default=None):
    p = os.path.join(D, name)
    return json.load(open(p)) if os.path.exists(p) else default


z = np.load(os.path.join(D, "scores.npz"), allow_pickle=False)
meta = ("classes", "etas", "truths", "hs", "axes", "PILOT_NEVER_REUSE_AS_EXAM")
scores = {k: z[k] for k in z.files if k not in meta}
S = ST.Scores(scores, z["classes"], z["etas"])
info = jload("info.json", {})
TR = jload("train_info.json", {})
cfg = info.get("config", {})
budgets = [int(b) for b in cfg.get("budgets", [8, 32, 2])]
NB = args.budget or budgets[0]
DCOL = int(cfg.get("d_first", 32))
HS = [int(h) for h in z["hs"]]
e0, e4 = 0, len(S.etas) - 1
SRC = f"{args.job}: scores.npz"
ALL, TRIG = ST.ALL, ST.TRIG


def short(r, keys=("value", "se", "lower90", "upper90", "median_of_per_truth_ratios", "loo_min", "loo_max")):
    return {k: r[k] for k in keys if k in r}


def closure(name, ei, cls=ALL, nb=NB, hsel=None):
    """(L(P0) - L(X)) / (L(P0) - L(C)), C of DECLARED R7 at budget nb."""
    P0 = S.L("P0", ei, cls=cls, hsel=hsel)
    Lc, _ = ST.C_of(S, ei, nb, cls, hsel)
    Lx = S.L(name, ei, cls=cls, hsel=hsel) if isinstance(name, str) else name
    return short(ST.ratio(P0 - Lx, P0 - Lc))


out = {"study": "round 6, dials, study A: the gliders calibration (plan section 2 A)", "PILOT_NEVER_REUSE_AS_EXAM": True,
       "declared": "DECLARED.md (committed before any run); criteria computed by a_stats.criteria",
       "job": {"id": args.job, "outputs": os.path.relpath(D, HERE)}}
st = jload("status.json")
if st:
    out["job"]["status"] = {k: st.get(k) for k in ("state", "message", "pod", "cost_usd", "billed_usd", "hours", "exit_code",
                                                    "started_at", "finished_at", "review", "rate_usd_per_hour", "gpu_type")
                            if k in st}
    out["job"]["status_source"] = f"origin/gpu-jobs:jobs/{args.job}/status.json"
out["what_ran"] = {"source": f"{args.job}: info.json", "backend": info.get("backend"), "devices": info.get("devices"),
                   "versions": info.get("versions"), "config": cfg, "member_ticks_planned": info.get("member_ticks_planned"),
                   "hours_on_the_jobs_clock": info.get("hours"), "times_seconds": {k: v for k, v in info.get("times", {}).items()
                                                                                  if isinstance(v, (int, float))},
                   "base_final_steps": info.get("base_final_steps"), "base_rule_met": info.get("base_rule_met"),
                   "failed": info.get("failed"), "skipped": info.get("skipped"), "notes": info.get("notes"),
                   "zero_point_of_the_switch_on_the_job_backend": jload("presmoke/zero_point.json"),
                   "speed_guard": jload("presmoke/guard.json"), "family_check": info.get("family_check")}

# ---------------------------------------------------------------- the declared criteria
C = ST.criteria(S, NB, DCOL)
out["criteria"] = {"source": SRC + " through a_stats.criteria", **C}
zp, s, g = C["zero_point"], C["s"], C["g"]
head = {"zero_point_holds": zp["holds"],
        "sigma_0": short(zp["sigma_0"]), "sigma_0_holds": zp["sigma_0"]["holds"],
        "sigma_0_holds_stricter": zp["sigma_0"]["holds_stricter_within_2_round5_se"],
        "zero_pairs": {k: ({**short(v), "holds": v["holds"]} if v.get("holds") is not None else v)
                       for k, v in zp.items() if isinstance(v, dict) and k != "sigma_0"}}
if s:
    head["s"] = {**short(s["aimed_regional"]), "standin_holds": s["standin_holds"], "forecast": 0.20,
                 "study_fails_s_below_0.05": s["study_fails_s_below_0.05"],
                 "fine_tuned_C_picked_share": s["aimed_regional"]["C"].get("share_fine_tuned_picked")}
if g:
    p = g["primary_all_classes"]
    head["g"] = {"value": p["g"], "se": p["g_se"], "lower90": p["g_lower90"], "upper90": p["g_upper90"],
                 "median_of_per_truth_ratios": p["g_median_of_per_truth_ratios"], "loo_range": p["g_loo_range"],
                 "gap_exceeds_2se": p["gap_exceeds_2se"], "verdict": p["verdict"],
                 "contrast_d_mean_lower_upper": [p["contrast_d"]["mean"], p["contrast_d"]["lower90"], p["contrast_d"]["upper90"]],
                 "share_FT_picked": p["G"].get("share_FT_picked")}
    q = g["secondary_aimed_regional"]
    head["g_secondary_aimed_regional"] = {"value": q["g"], "se": q["g_se"], "lower90": q["g_lower90"], "upper90": q["g_upper90"],
                                          "verdict": q["verdict"]}
head["study_fails"] = C["study_fails"]
if not C["study_fails"]["value"] and g and s:
    v = g["verdict"]
    if v == "confirmed":
        head["outcome_in_the_plans_table"] = "A: generic repair confirmed, stand-in " + ("holds" if s["standin_holds"] else "misses")
    elif v == "refuted":
        head["outcome_in_the_plans_table"] = "A: refuted, with s " + (">= 0.15" if s["value"] >= 0.15 else "below 0.15")
    else:
        head["outcome_in_the_plans_table"] = "A: undecided at this number of truths (one extension to 16 truths is allowed)"
elif C["study_fails"]["value"]:
    head["outcome_in_the_plans_table"] = "A: the study itself fails (" + "; ".join(C["study_fails"]["why"]) + "); nothing else is read"
out["headline"] = {"source": "criteria block above", **head}

# ---------------------------------------------------------------- reported, never criteria
rep = {"source": SRC, "note": "reported numbers; none of them is a criterion"}
rep["skill_vs_oracle"] = {f"eta{S.etas[ei]:g}|{name}": {k: {"L": round(v["L"], 5), "skill": round(v["skill_vs_O"], 4)}
                                                       for k, v in ST.skills(S, ei, cls).items()}
                          for ei in range(len(S.etas)) for name, cls in (("all", ALL), ("aimed_regional", TRIG))}
# the state-given screen and what a history-only net keeps of it
scr = {}
for name, cls in (("all", ALL), ("aimed", ("c",)), ("regional", ("d",)), ("blind", ("b",)), ("none", ("a",))):
    K, O, PL_ = S.L("K", e4, cls=cls), S.L("O", e4, cls=cls), S.L("plug", e4, cls=cls)
    scr[name] = {"state_given_share": short(ST.ratio(PL_ - O, K - O))}
    if S.has("Ctrue"):
        Lc, _ = ST.C_of(S, e4, NB, cls)
        scr[name]["history_only_share_s"] = short(ST.ratio(S.L("P0", e4, cls=cls) - Lc, K - Lc))
        scr[name]["kept_fraction"] = short(ST.ratio(S.L("P0", e4, cls=cls) - Lc, PL_ - O))
rep["screens_eta4"] = scr
# closures of the P0-to-C gap by policy, class and budget (eta = 4), and at eta = 0
clo = {}
for nb in budgets:
    for pol in (f"FT@{nb}", f"RES@{nb}", f"S@{nb}", f"CFT@{nb}"):
        if S.has(pol) and S.has(f"CFT@{nb}"):
            for name, cls in (("all", ALL), ("aimed_regional", TRIG), ("aimed", ("c",)), ("regional", ("d",)), ("blind", ("b",)), ("none", ("a",))):
                clo[f"{pol}|{name}"] = closure(pol, e4, cls, nb)
    if S.has(f"FT@{nb}") or S.has(f"RES@{nb}"):
        for name, cls in (("all", ALL), ("aimed_regional", TRIG)):
            r = ST.g_rule(S, e4, nb, cls)
            clo[f"G@{nb}|{name}"] = {"value": r["g"], "se": r["g_se"], "lower90": r["g_lower90"], "upper90": r["g_upper90"],
                                     "verdict_if_it_were_the_primary": r["verdict"], "share_FT_picked": r["G"].get("share_FT_picked"),
                                     "median_of_per_truth_ratios": r["g_median_of_per_truth_ratios"], "loo_range": r["g_loo_range"]}
for pol in ("Cpub", "Ctrue"):
    if S.has(pol) and S.has(f"CFT@{NB}"):
        for name, cls in (("all", ALL), ("aimed_regional", TRIG)):
            clo[f"{pol}|{name}"] = closure(pol, e4, cls, NB)
for pol in [k for k in scores if k.startswith(("FTfree@", "RESfree@"))]:
    if S.has(pol) and S.has(f"CFT@{NB}"):
        for name, cls in (("all", ALL), ("aimed_regional", TRIG)):
            clo[f"{pol}|{name}"] = closure(pol, e4, cls, NB)
rep["closure_of_P0_to_C_eta4"] = clo
if g:
    rep["g_per_horizon_eta4"] = {}
    for i, h in enumerate(HS):
        for name, cls in (("all", ALL), ("aimed_regional", TRIG)):
            r = ST.g_rule(S, e4, NB, cls, hsel=[i])
            rep["g_per_horizon_eta4"][f"h{h}|{name}"] = {"value": r["g"], "se": r["g_se"], "gap_exceeds_2se": r["gap_exceeds_2se"]}
    r = ST.g_rule(S, e4, NB, ALL, c_fixed="Ctrue")
    rep["g_with_the_trueform_net_alone_as_C"] = {"value": r["g"], "se": r["g_se"], "lower90": r["g_lower90"], "upper90": r["g_upper90"],
                                                 "verdict_if_it_were_the_primary": r["verdict"]}
# the same shares in units of K-to-C at both dial values (what each policy gains or loses against P0)
gain = {}
for ei in range(len(S.etas)):
    den = S.L("K", ei) - S.L("Cpub", ei)
    for pol in sorted(scores):
        if "@r" in pol or pol in ("K", "O", "P0") or not S.has(pol):
            continue
        gain[f"eta{S.etas[ei]:g}|{pol}"] = short(ST.ratio(S.L("P0", ei) - S.L(pol, ei), den), ("value", "se"))
rep["gain_over_P0_in_units_of_K_to_publicC"] = gain
# the roadmap's science share at eta = 4 against P0 and against the generic repair G (the designer's bars 1, 2)
sg = {}
if g:
    for name, cls in (("all", ALL), ("aimed_regional", TRIG)):
        Lc, _ = ST.C_of(S, e4, NB, cls)
        Lg, _ = ST.G_of(S, e4, NB, cls)
        K = S.L("K", e4, cls=cls)
        sg[f"sigma_against_P0|{name}"] = short(ST.ratio(S.L("P0", e4, cls=cls) - Lc, K - Lc))
        sg[f"sigma_against_G|{name}"] = short(ST.ratio(Lg - Lc, K - Lc))
rep["science_share_eta4"] = sg
# sigma at the zero point once more through round 5's own function (acceptance.shares, bootstrap over worlds)
try:
    import importlib.util
    f = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "round5", "agentenv", "evaluator", "acceptance.py")
    spec = importlib.util.spec_from_file_location("agentenv_acceptance", f)
    ACC = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ACC)
    it = lambda a: a.mean(1).reshape(-1, a.shape[-1])                   # seed mean, (truth x item, horizon)
    sc1 = lambda n: it(scores[n][e0][:, :, 1].astype(float))
    d_ = {"K": sc1("K"), "C": sc1("Cpub"), "P0": sc1("P0")}
    if f"S@{DCOL}" in scores:
        d_["S"] = sc1(f"S@{DCOL}")
    if S.has(f"Dnet@{DCOL}") or S.has(f"Dridge@{DCOL}"):
        d_["D"] = it(ST.picked_items(S, [f"Dnet@{DCOL}", f"Dridge@{DCOL}"], e0))
    nT, nI = scores["K"].shape[1], scores["K"].shape[4]
    r = ACC.shares(d_, None, worlds=np.repeat(np.arange(nT), nI), n_boot=1000, seed=DCOL)
    rep["sigma_0_by_acceptance_py"] = {k: r.get(k) for k in ("sigma", "null_is", "rho", "sigma_worlds", "rho_worlds", "L", "per_world")}
except Exception as exc:
    rep["sigma_0_by_acceptance_py"] = {"error": repr(exc)}
# the base schedule: every rung scored
rungs = sorted({int(k.split("@r")[1]) for k in scores if "@r" in k})
rr = {}
for st_ in rungs:
    a, b, c_ = f"P0@r{st_}", f"Cpub@r{st_}", f"Ctrue@r{st_}"
    if not S.has(a, b, c_):
        continue
    rr[str(st_)] = {
        "sigma_0_null_P0": short(ST.ratio(S.L(a, e0) - S.L(b, e0), S.L("K", e0) - S.L(b, e0)), ("value", "se")),
        "s_trueform_net_alone_aimed_regional": short(ST.ratio(S.L(a, e4, cls=TRIG) - S.L(c_, e4, cls=TRIG),
                                                              S.L("K", e4, cls=TRIG) - S.L(c_, e4, cls=TRIG)), ("value", "se")),
        "zero_trueformC_vs_publicC": short(ST.ratio(S.L(c_, e0) - S.L(b, e0), S.L("K", e0) - S.L(b, e0)), ("value", "se")),
        "skill_vs_O": {f"eta{S.etas[ei]:g}|{n_}": round(float((S.L("K", ei).mean() - S.L(x, ei).mean()) / (S.L("K", ei).mean() - S.L("O", ei).mean())), 4)
                       for ei in range(len(S.etas)) for n_, x in (("P0", a), ("Cpub", b), ("Ctrue", c_))}}
rep["base_schedule_rungs"] = rr
out["reported"] = rep

# ---------------------------------------------------------------- training
tr = {"source": f"{args.job}: train_info.json"}
tr["base"] = [{k: b.get(k) for k in ("steps", "best_step", "best_val", "rule_met", "seconds", "stopped_early", "net_order")}
              | {"val_mean_curve": [[h["step"], h["val_mean"]] for h in b.get("hist", [])]} for b in TR.get("base", [])]
tr["fine_tunes"] = {nb: [{"steps": f["steps"], "rule_met": f["rule_met"], "rule": f["rule"], "timing": {k: v for k, v in f["timing"].items()
                                                                                                    if not k.startswith("group_")}}
                         for f in fs] for nb, fs in TR.get("ft", {}).items()}
tr["D"] = {nb: [{"steps": d["steps"], "rule_met": d["rule_met"], "best_steps": [b for g_ in d["groups"] for b in g_["best_step"]]}
                for d in ds] for nb, ds in TR.get("D", {}).items()}
out["training"] = tr
# cost of the reference policies in episode equivalents (crit_cost: 476 per 6,000 steps of one net on one CPU thread)
fs = info.get("base_final_steps") or 0
out["cost_in_episode_equivalents"] = {
    "source": "crit_cost/results/recompute.json [net_training_inside_the_research_budget]; this job's schedule",
    "research_budget_told": 8192, "P0_simulation": 6144, "P0_training": round(476 * fs / 6000),
    "P0_total": 6144 + round(476 * fs / 6000),
    "FT_extra_per_world": {"lab_episodes": NB, "fine_tune_steps_at_batch_64": cfg.get("ft_steps"),
                           "note": "cross-validation multiplies the fine-tune steps by folds + 1"}}
json.dump(out, open(args.out, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print(json.dumps(out["headline"], indent=1, default=str))
