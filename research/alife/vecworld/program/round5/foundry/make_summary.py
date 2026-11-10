"""make_summary -- results/summary.json of study foundry: every claimed number with its source.

    python -B make_summary.py

Sources (all under results/): analysis.json (analyze.py on job 1), analysis_r2.json (job 2, if present),
checks.json (check_tnca.py, CPU), wind_probe.json, recheck_cpu.json, figs.json, jobs/<job_id>/status.json
(copied from origin/gpu-jobs by fetch.sh). A claim is {id, text, value, source: {job, file, key}} where
`file` is a path inside the job's outputs on origin/gpu-jobs:jobs/<job>/out/ (or a file of this folder) and
`key` the path inside results/analysis*.json that holds the derived number.
"""
from __future__ import annotations

import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
JOB1, JOB2 = "r5-foundry-001", "r5-foundry-002"


def load(name):
    p = os.path.join(RES, name)
    return json.load(open(p)) if os.path.exists(p) else None


def get(d, path):
    for k in path.split("."):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


def ledger_hours(job):
    """Pod hours of the job from the runner's ledger (results/jobs/ledger_rows.md, copied from origin/gpu-jobs:LEDGER.md)."""
    p = os.path.join(RES, "jobs", "ledger_rows.md")
    if not os.path.exists(p):
        return None
    for line in open(p):
        c = [x.strip() for x in line.split("|")]
        if len(c) > 5 and c[1] == job:
            return float(c[5])
    return None


def job_info(job):
    st = load(os.path.join("jobs", job, "status.json"))
    if st is None:
        return None
    pod = st.get("pod") or {}
    hist = st.get("history") or []
    from datetime import datetime
    ts = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None
    a, b = ts(st.get("started_at")), ts(st.get("finished_at"))
    return dict(job_id=job, state=st.get("state"), exit_code=st.get("exit_code"), gpu=pod.get("gpu"),
                provider=pod.get("provider"), rate_usd_hr=pod.get("rate_usd_hr"),
                billed_usd=(st.get("cost") or {}).get("billed_usd"),
                conservative_usd=(st.get("cost") or {}).get("conservative_usd"), cap_usd=st.get("cap_usd"),
                received_at=hist[0]["at"] if hist else None, started_at=st.get("started_at"),
                finished_at=st.get("finished_at"),
                run_hours=round((b - a).total_seconds() / 3600, 3) if a and b else None,
                ref=(st.get("bundle") or {}).get("ref"), review=(st.get("review") or {}).get("summary"),
                pod_hours_ledger=ledger_hours(job),
                source=f"origin/gpu-jobs:jobs/{job}/status.json (copy: results/jobs/{job}/status.json)")


def main():
    ana = load("analysis.json")
    chk = load("checks.json")
    out = dict(study="foundry (round 5, track 1): world foundry v0, the affinity transport NCA family",
               date="2026-11-10", jobs=[j for j in (job_info(JOB1), job_info(JOB2)) if j],
               platform=ana.get("platform") if ana else None, config=ana.get("config") if ana else None, claims=[])
    C = out["claims"]

    def claim(cid, text, value, job, file, key, a=None):
        C.append(dict(id=cid, text=text, value=value, source=dict(job=job, file=file, key=key)))

    def A(cid, text, key, file, fmt=None, an=ana, job=JOB1, afile="results/analysis.json"):
        try:
            v = get(an, key)
        except Exception as e:                                       # a missing part is recorded, not hidden
            v = f"MISSING ({e!r})"
        claim(cid, text, v if fmt is None else fmt(v), job, file, f"{afile}:{key}")

    if chk:
        for cid, text, key in (
                ("K1", "CPU check, 8 worlds x 400 substeps with wind commands: largest relative drift of the total mass",
                 "conservation.total_mass_rel_drift_max"),
                ("K2", "CPU check: largest relative drift of one kind's mass in the worlds with kappa = 0",
                 "conservation.kind_mass_rel_drift_max_kappa0"),
                ("K3", "CPU check: smallest cell value (positivity)", "conservation.min_cell"),
                ("K4", "CPU check: largest relative error of the 6 lattice symmetries (shift, rot90, rot180, flips, transpose)",
                 "symmetry.rel_error_max"),
                ("K5", "CPU check: Monte Carlo KL of a 3-tick wind program against its charge (nats, se, z)",
                 "wind.kl_check"),
                ("K6", "CPU check: passive matter under a unit +x command on every block (512 nats per tick): shift in px per tick per kind, and the noise-free formula",
                 "wind.delivery"),
                ("K7", "CPU check: growth of the fastest linear mode, symbol against direct simulation (relative error)",
                 "linear.rel_error_max")):
            claim(cid, text, get(chk, key), "local CPU", "results/checks.json", key)
    if ana:
        F = "screen/chunk_*.npz"
        A("S0", "draws screened; member-ticks; seconds; steady member-ticks per second", "screen_run", "job_state.json",
          lambda v: {k: v[k] for k in ("n_done", "member_ticks", "seconds", "member_ticks_per_s_steady", "chunk")})
        A("S1", "world types over the prior: count, share and binomial se per type", "types.table", F,
          lambda v: {k: {kk: x[kk] for kk in ("n", "frac", "se")} for k, x in v.items()})
        A("S2", "gates over the prior (viable, closure, structures, sensitive, candidate = all)", "gates", F,
          lambda v: {k: {kk: x[kk] for kk in ("n", "frac", "se")} for k, x in v.items() if isinstance(x, dict)})
        A("S3", "validity over all screened draws on the GPU: finite, mass drift, smallest cell, largest density, smallest participation ratio",
          "validity", F)
        A("S4", "closure classes among the active worlds", "closure_classes_active", F)
        A("S5", "quantiles (10, 50, 90%) of the descriptors: all draws, active worlds, movers", "descriptors_q10_q50_q90.table", F)
        A("W1", "share of draws whose uniform state is linearly unstable (lin_growth > 1e-4)", "weights.lin_unstable_share", "wstats.npz")
        A("W2", "rules on the weights alone: precision and recall of lin_growth for structure; yields given simple conditions",
          "weights.rules", "wstats.npz + " + F)
        A("W3", "cross-validated AUC of logistic regressions on groups of weight statistics, per target", "weights.groups",
          "wstats.npz + " + F, lambda v: {t: {g: round(x["auc"], 4) if x["auc"] == x["auc"] else None for g, x in gg.items()}
                                         for t, gg in v.items()})
        A("W4", "best single weight statistics per target (AUC, Spearman rho)", "weights.single", "wstats.npz + " + F,
          lambda v: {t: rows[:5] for t, rows in v.items()})
        A("T1", "candidates at screen size: number; the 40 best worlds by score with their descriptors",
          "candidates_screen.n_candidates", F)
        if "certification" in ana:
            A("T2", "certification of the top worlds at larger size: how many pass the gates again", "certification",
              "cert/eps010.npz", lambda v: {k: v[k] for k in ("n", "n_candidate_at_screen", "n_candidate_at_cert",
                                                               "n_candidate_both", "gates_at_cert", "types_at_cert", "sizes")})
            A("T3", "certified worlds by score: descriptors, ceilings, plug-in loss by neighbour size", "certification.worlds",
              "cert/*.npz", lambda v: [{k: w[k] for k in ("draw", "score", "type", "gates", "nb_mean", "rg", "v_net",
                                                            "events100", "ceil", "v_orc", "v_pred", "gap_max", "twin_doubling",
                                                            "twin_half_h", "pl8_by_neighbour", "wavelength", "body_frac")}
                                       for w in v[:12]])
        for key, cid in (("gliders_same_estimator", "G1"), ("gliders_cert_size", "G2")):
            if key in ana:
                A(cid, f"the gliders world by the same estimator ({key}): types, gates, ceilings, oracle, bodies; published numbers alongside",
                  key, ana[key]["src"], lambda v: {k: v[k] for k in ("n_runs", "sizes", "types", "gates", "score", "ceil", "v_orc",
                                                                     "v_pred", "nb_mean", "rg", "v_net", "events100",
                                                                     "twin_doubling", "twin_half_h", "gap_max", "pl", "published")})
        if "controls_diffusion" in ana:
            A("N1", "control worlds without affinity (beta = gam = kappa = 0): types and floors", "controls_diffusion",
              "controls_diffusion.npz")
        A("P1", "job stages: seconds and results of the on-pod checks (conservation, vmap against single runs, rerun determinism)",
          "stages.checks", "job_state.json")
    a2 = load("analysis_r2.json")
    if a2:
        R = dict(an=a2, job=JOB2, afile="results/analysis_r2.json")
        A("R0", "job 2 arms: draws done, seconds, member-ticks, steady member-ticks per second", "arms_run", "job2_state.json",
          lambda v: {k: {kk: x[kk] for kk in ("n_planned", "n_done", "seconds", "member_ticks", "member_ticks_per_s_steady",
                                              "prior_seed", "family_sigma")} for k, x in v.items()}, **R)
        A("R1", "prospective test of the weights-only predictor: yields per arm, the yields predicted from job 1 before the "
          "run, the pool rate (arms weighted by their shares), enrichment over the pool, share of all found in the selected draws",
          "enrich", "enrich/chunk_*.npz + sel_r2.json",
          lambda v: dict(pool=v["pool"], prior_seed=v["prior_seed"], share_selected=v["share_selected"], control_is=v["control_is"],
                         predicted_yield=v["prediction_from_job1"]["predicted_yield"],
                         enriched={k: {kk: x[kk] for kk in ("n", "of", "frac", "se")} for k, x in v["arms"]["enriched"]["yields"].items()},
                         control={k: {kk: x[kk] for kk in ("n", "of", "frac", "se")} for k, x in v["arms"]["control"]["yields"].items()},
                         pool_rate=v["pool_rate"], enrichment_over_pool=v["enrichment_over_pool"],
                         share_of_all_found_in_selected=v["share_of_all_found_in_selected"],
                         observed_minus_predicted_in_se=v["observed_minus_predicted_in_se"]), **R)
        A("R2", "late time (ticks 2000-2240) against the screen (ticks 50-290) for the same 2000 draws: transition counts and "
          "what remains of the active worlds, the movers and the candidates", "late", "late/chunk_*.npz + results/per_draw.json.gz",
          lambda v: {k: x for k, x in v.items() if k != "late_candidates"}, **R)
        for arm, cid in (("sigma010", "R3"), ("sigma100", "R4")):
            A(cid, f"logit noise {0.1 if arm == 'sigma010' else 1.0} instead of 0.3 for draws 0-2047: types, transitions, movers, candidates",
              arm, f"{arm}/chunk_*.npz + results/per_draw.json.gz", **R)
        A("R5", "all 88 candidates of job 1 at certification size: gates, types, quantiles (10, 50, 90%), gliders-like closure profiles",
          "cert", "cert/chunk_*.npz", lambda v: {k: x for k, x in v.items() if k != "worlds"}, **R)
        A("R6", "shortlist: candidates at the screen, at certification size and at late time, with both sets of descriptors",
          "shortlist", "cert/chunk_*.npz + late/chunk_*.npz", **R)
    d = load("wind_probe.json")
    if d:
        claim("X1", "wind probe (CPU): paired effect E of 4-tick wind commands on the block view of four top worlds at horizons "
              "1, 2, 4, 8, 16 ticks, and E / (2 D0) against the noise floor",
              [dict(draw=w["draw"], noise_floor_D0=w["noise_floor_D0"], **{k: w["programs"][k] for k in ("blind_200", "aimed_200", "aimed_800")})
               for w in d["worlds"]], "local CPU", "results/wind_probe.json", "worlds")
    d = load("wind_probe_sigma_w1.json")
    if d:
        claim("X4", "exploration (CPU): the same probe with the wind noise at 1.0 instead of 0.25",
              [dict(draw=w["draw"], noise_floor_D0=w["noise_floor_D0"], **{k: w["programs"][k] for k in ("blind_200", "aimed_200", "aimed_800")})
               for w in d["worlds"]], "local CPU", "results/wind_probe_sigma_w1.json", "worlds")
    d = load("cpu_vs_gpu.json")
    if d:
        claim("X2", "CPU (this container) against the H100 of job 1: the screen's descriptors of 12 draws with the same keys",
              {k: {kk: v[kk] for kk in ("max_rel_diff", "values_identical", "values_compared", "worlds")}
               for k, v in d.items() if isinstance(v, dict)}, "local CPU + " + JOB1,
              "results/cpu_vs_gpu.json (from results/recheck_cpu*.json and screen/chunk_*.npz)", "*")
    d = load("longrun.json")
    if d:
        claim("X3", "CPU runs of 2000 ticks of four top worlds: windows of 250 ticks (moved, bodies, net speed, events, vp16)",
              [dict(draw=w["draw"], first=w["windows"][0], last=w["windows"][-1]) for w in d["worlds"]], "local CPU",
              "results/longrun.json", "worlds")
    out["pilots_never_exam"] = (interp or {}).get("never_reuse_as_exam") if (interp := load("interpretation.json")) else None
    out["figures"] = load("figs.json")
    interp = load("interpretation.json")
    if interp:
        out["interpretation"] = interp
    js = out["jobs"]
    out["gpu_total"] = dict(pod_hours=round(sum(j["pod_hours_ledger"] or 0 for j in js), 3),
                            billed_usd=round(sum(j["billed_usd"] or 0 for j in js), 4), budget_usd=25.0,
                            source="results/jobs/ledger_rows.md (pod hours) and results/jobs/<job>/status.json:cost.billed_usd")
    with open(os.path.join(RES, "summary.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("claims", len(C), "->", os.path.join(RES, "summary.json"), os.path.getsize(os.path.join(RES, "summary.json")), "bytes")


if __name__ == "__main__":
    main()
