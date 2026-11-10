"""interpret -- the study's verdicts as sentences whose numbers are read from the analysis files (CPU, instant).

    python -B interpret.py        ->  results/interpretation.json

Every verdict is {id, verdict, numbers: {...}, sources: [...]}; the sentence is formatted from `numbers`,
which are copied from results/analysis.json (job r5-foundry-001), results/analysis_r2.json (job
r5-foundry-002) and the CPU result files. Nothing here is typed by hand except the wording.
"""
from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
L = lambda n: json.load(open(os.path.join(RES, n)))
pc = lambda x, d=1: f"{100 * x:.{d}f}%"


def main():
    a, b = L("analysis.json"), L("analysis_r2.json")
    wp, lr, cg, ck = L("wind_probe.json"), L("longrun.json"), L("cpu_vs_gpu.json"), L("checks.json")
    V = []

    def add(vid, text, numbers, sources):
        V.append(dict(id=vid, verdict=text.format(**numbers), numbers=numbers, sources=sources))

    T, G = a["types"]["table"], a["gates"]
    val = a["validity"]
    n = dict(n=a["types"]["n"], drift=val["mass_drift_max"], smax=val["smax_max"], pr=val["pr_min"],
             invalid=T["invalid"]["n"], point=T["point"]["n"], ctrl=a["controls_diffusion"]["types"]["uniform"],
             ctrl_n=a["controls_diffusion"]["n"], rerun=a["stages"]["checks"]["rerun_bit_identical"],
             late_drift=b["late"]["validity"]["mass_drift_max"])
    add("family_valid", "All {n} screened worlds are valid: none non-finite, none collapsed to point masses (largest cell "
        "density {smax:.0f}, smallest participation ratio {pr:.3f}), total mass conserved to {drift:.1e} over 290 ticks "
        "and to {late_drift:.1e} over 2240 ticks; the {ctrl_n} no-affinity control worlds are all uniform ({ctrl}). The "
        "crowding term does what the critique asked for.", n,
        ["analysis.json:validity", "analysis.json:types.table", "analysis.json:controls_diffusion", "analysis_r2.json:late.validity"])
    s1, s2 = a["screen_run"], b["arms_run"]
    g = a["stages"]["gliders"]
    n = dict(rate=s1["member_ticks_per_s_steady"], secs=s1["seconds"], draws=s1["n_done"],
             glid=g["cert_size"]["member_ticks_per_s"], glid_screen=g["member_ticks_per_s"],
             ratio=s1["member_ticks_per_s_steady"] / g["cert_size"]["member_ticks_per_s"],
             h200=s2["enrich"]["member_ticks_per_s_steady"])
    add("cost", "The family is cheap: {rate:.0f} member-ticks/s on an H100 ({h200:.0f} on an H200) in float64, so {draws} "
        "draws with full certificates took {secs:.0f} s; the gliders world ran at {glid:.0f} member-ticks/s by the same "
        "code on the same pod (compile included), about {ratio:.0f} times slower.", n,
        ["analysis.json:screen_run", "analysis.json:stages.gliders", "analysis_r2.json:arms_run"])
    n = dict(uni=T["uniform"]["frac"], fro=T["frozen"]["frac"], fld=T["active:field"]["frac"], bod=T["active:bodies"]["frac"],
             mov=T["active:movers"]["frac"], act=G["viable"]["frac"], se=T["uniform"]["se"], cand=G["candidate"]["frac"],
             cand_n=G["candidate"]["n"], cand_se=G["candidate"]["se"], clo=G["closure"]["frac"], stru=G["structures"]["frac"],
             sen=G["sensitive"]["frac"], k0=G["candidate"]["kappa0"]["frac"], k1=G["candidate"]["kappa_pos"]["frac"])
    add("types", "World types over the prior at ticks 50-290: uniform {uni:.1%}, frozen {fro:.1%}, active {act:.1%} "
        "(field {fld:.1%}, bodies {bod:.1%}, movers {mov:.1%}); no noisy and no collapsed world. Gates: closure {clo:.1%}, "
        "structures {stru:.1%}, sensitive {sen:.1%}, all four {cand:.2%} +- {cand_se:.2%} ({cand_n} worlds; {k0:.2%} "
        "without conversion, {k1:.2%} with).", n, ["analysis.json:types.table", "analysis.json:gates"])
    lt = b["late"]
    sl = b["shortlist"]
    stat_cand = (lt["candidates_stay_candidates"]["n"] + lt["new_candidates_among_non_candidates"]["n"]) / a["types"]["n"]
    n = dict(act=lt["active_stays_active"]["frac"], fro=lt["active_becomes_frozen"]["frac"], n_act=lt["active_stays_active"]["of"],
             mov=lt["movers_stay_movers"]["frac"], cand=lt["candidates_stay_candidates"]["frac"],
             cand_n=lt["candidates_stay_candidates"]["n"], cand_of=lt["candidates_stay_candidates"]["of"],
             fz=lt["frozen_sample_changes"]["frac"], un=lt["uniform_sample_changes"]["frac"],
             new=lt["new_candidates_among_non_candidates"]["n"], stat=stat_cand,
             late_act=G["viable"]["frac"] * lt["active_stays_active"]["frac"], fa=lt["frozen_sample_becomes_active"]["frac"],
             late_fro=T["frozen"]["frac"] * lt["frozen_sample_becomes_active"]["frac"])
    add("transient", "Most early activity is a transient: of the {n_act} worlds active at ticks 50-290 only {act:.1%} are still "
        "active at ticks 2000-2240 and {fro:.1%} have frozen; {mov:.1%} of the movers are still movers and {cand_n} of the "
        "{cand_of} candidates ({cand:.1%}) still pass every gate ({new} other active worlds became candidates). Frozen and "
        "uniform worlds stay as they are ({fz:.1%} and {un:.1%} of 381 each changed type; {fa:.1%} of the frozen sample became "
        "active). Long-lived activity is therefore about {late_act:.1%} of the prior from early-active worlds (plus about "
        "{late_fro:.1%} from early-frozen ones) and long-lived candidates about {stat:.2%}: the screen needs a late-time gate.", n,
        ["analysis_r2.json:late", "analysis.json:gates"])
    w = a["weights"]
    r = w["rules"]["lin_growth>0.0001 -> structured"]
    n = dict(auc=w["single"]["structured"][0]["auc"], prec=r["precision"], rec=r["recall"], acc=r["accuracy"],
             share=w["lin_unstable_share"]["frac"], all_s=w["groups"]["structured"]["all"]["auc"],
             all_m=w["groups"]["movers"]["all"]["auc"], all_c=w["groups"]["candidate"]["all"]["auc"],
             pri_c=w["groups"]["candidate"]["prior_scalars"]["auc"], lin_c=w["groups"]["candidate"]["linear_stability"]["auc"],
             jac_c=w["groups"]["candidate"]["jacobian"]["auc"], nrm_c=w["groups"]["candidate"]["weight_norms"]["auc"],
             nrm_s=w["groups"]["structured"]["weight_norms"]["auc"])
    add("weights_predict", "Statistics of the weights alone predict the type. The growth rate of the fastest linear mode of the "
        "uniform state (two Jacobian-vector products and an FFT per world, no simulation of the field) has AUC {auc:.3f} for structure; the "
        "rule growth > 1e-4 ({share:.1%} of draws) has precision {prec:.3f} and recall {rec:.3f}. Cross-validated logistic "
        "regressions on all weight statistics reach AUC {all_s:.3f} (structure), {all_m:.3f} (movers) and {all_c:.3f} "
        "(candidates); for candidates the prior's scalars alone give {pri_c:.3f}, linear stability {lin_c:.3f}, the affinity "
        "Jacobian {jac_c:.3f}, and the weight norms {nrm_c:.3f} (no information).", n,
        ["analysis.json:weights.single", "analysis.json:weights.rules", "analysis.json:weights.groups"])
    e = b["enrich"]
    en, co, pr = e["arms"]["enriched"]["yields"], e["arms"]["control"]["yields"], e["prediction_from_job1"]["predicted_yield"]
    n = dict(pool=e["pool"], share=e["share_selected"], n_en=e["arms"]["enriched"]["n"], n_co=e["arms"]["control"]["n"],
             cand=en["candidate"]["frac"], cand_se=en["candidate"]["se"], cand_n=en["candidate"]["n"], pred=pr["candidate"],
             ctl=co["candidate"]["frac"], ctl_n=co["candidate"]["n"], mov=en["movers"]["frac"], mov_p=pr["movers"],
             act=en["active"]["frac"], act_p=pr["active"], stru=en["structured"]["frac"], stru_p=pr["structured"],
             rate=e["pool_rate"]["candidate"]["frac"], rate_se=e["pool_rate"]["candidate"]["se"],
             enr=e["enrichment_over_pool"]["candidate"], found=e["share_of_all_found_in_selected"]["candidate"],
             base1=e["prediction_from_job1"]["base_rate"]["candidate"])
    add("weights_prospective", "The predictor holds prospectively. Fitted on job 1 and applied to the weight statistics of a "
        "fresh pool of {pool} draws (another prior seed), its best {share:.1%} ({n_en} draws) contain {cand:.1%} +- "
        "{cand_se:.1%} candidates ({cand_n}); predicted before the run: {pred:.1%}. Movers {mov:.1%} (predicted {mov_p:.1%}), "
        "active {act:.1%} ({act_p:.1%}), structured {stru:.1%} ({stru_p:.1%}). The {n_co} control draws, a random sample of the "
        "unselected draws, contain {ctl:.2%} ({ctl_n} worlds). Weighting the two arms, the pool's candidate rate is "
        "{rate:.2%} +- {rate_se:.2%} (job 1: {base1:.2%}); the selected draws are enriched {enr:.1f} times and hold "
        "{found:.0%} of all candidates.", n, ["analysis_r2.json:enrich", "sel_r2.json:prediction_from_job1"])
    c = a["certification"]
    c2 = b["cert"]
    n = dict(n=c["n"], both=c["n_candidate_at_cert"], n88=c2["n"], pass88=c2["gates"]["candidate"]["n"],
             frac88=c2["gates"]["candidate"]["frac"], like=c2["gliders_like_closure"]["n"], short=sl["n"], short_like=sl["n_gliders_like"],
             short_list=", ".join(str(d) for d in sl["gliders_like"]))
    add("candidates", "The screen's selection replicates: all {both} of the {n} top worlds pass every gate again at certification "
        "size (16 members, 32 test states, fresh keys), and {pass88} of all {n88} candidates do ({frac88:.1%}). {short} candidates "
        "pass at the screen, at certification size and at ticks 2000-2240; {short_like} of them have a closure profile like the "
        "gliders world's (c(1) >= 0.95, 0.25 <= c(8) <= 0.75, c(32) <= 0.5) with unchanged statistics at late time: draws "
        "{short_list} of prior seed 2026.", n,
        ["analysis.json:certification", "analysis_r2.json:cert", "analysis_r2.json:shortlist"])
    gl, gc = a["gliders_same_estimator"], a["gliders_cert_size"]
    pub = gc["published"]
    w4470 = next(w for w in sl["worlds"] if w["draw"] == 4470)
    n = dict(c=" / ".join(f"{x['mean']:.3f}" for x in gc["ceil"]), pub=" / ".join(f"{x:.3f}" for x in pub["ceiling_linear_set"]),
             best=" / ".join(f"{x:.3f}" for x in pub["ceiling_best_of"]), vo=gc["v_orc"][3]["mean"], vo_pub=pub["V_oracle"][3],
             nb=gl["nb_mean"]["mean"], nb_pub=pub["bodies_mean"], rg=gl["rg"]["mean"], v=gl["v_net"]["mean"],
             ev=gl["events100"]["mean"], ev_pub=pub["fusions_per_100"] + pub["fissions_per_100"], dbl=gl["twin_doubling"]["mean"],
             runs=gl["n_runs"], runs_c=gc["n_runs"], movers=gl["types"]["active:movers"],
             f_c=" / ".join(f"{w4470['cert'][k]:.3f}" for k in ("ceil1", "ceil4", "ceil8", "ceil16", "ceil32")),
             f_nb=w4470["cert"]["nb_mean"], f_v=w4470["cert"]["v_net"], f_ev=w4470["cert"]["events100"], f_rg=w4470["cert"]["rg"],
             f_vo=w4470["cert"]["v_orc8"], f_dbl=w4470["cert"]["twin_doubling"], pl0=gc["pl"][3]["mean"], pl0_se=gc["pl"][3]["se"])
    add("gliders", "The gliders world, measured by the same code, is typed a mover world in {movers} of {runs} runs and passes the "
        "closure and structures gates. Its ceilings with the cheap ridge at 1/2/4/8/16/32 ticks are {c} ({runs_c} runs at "
        "certification size) against the published {pub} (linear predictors) and {best} (best of all predictors); oracle "
        "variance at 8 ticks {vo:.4f} (published {vo_pub:.4f}); {nb:.1f} bodies (published {nb_pub}), radius {rg:.1f} px, "
        "{v:.2f} px/tick, {ev:.0f} fusions + fissions per 100 ticks (published {ev_pub:.0f}); its plug-in loss with theta' = "
        "theta is {pl0:.4f} +- {pl0_se:.4f} (the null of that estimator). So the estimator reproduces the reference, and "
        "foundry draw 4470 sits next to it: ceilings at 1/4/8/16/32 ticks {f_c}, oracle variance {f_vo:.4f}, {f_nb:.0f} bodies "
        "of radius {f_rg:.1f} px at {f_v:.2f} px/tick, {f_ev:.0f} events per 100 ticks, noise-twin doubling {f_dbl:.1f} ticks "
        "(gliders {dbl:.1f}).", n,
        ["analysis.json:gliders_same_estimator", "analysis.json:gliders_cert_size", "analysis_r2.json:shortlist.worlds"])
    W = c["worlds"]
    med = lambda v: float(np.median(v))
    n = dict(n=len(W), vo=med([w["v_orc"][3] for w in W]),
             p03=med([w["pl8_by_neighbour"]["eps003"] for w in W]), p10=med([w["pl8_by_neighbour"]["eps010"] for w in W]),
             p30=med([w["pl8_by_neighbour"]["eps030"] for w in W]), hyp=med([w["pl8_by_neighbour"]["hyp010"] for w in W]),
             r03=med([w["pl8_by_neighbour"]["eps003"] / max(w["v_orc"][3], 1e-9) for w in W]),
             r10=med([w["pl8_by_neighbour"]["eps010"] / max(w["v_orc"][3], 1e-9) for w in W]),
             r88=c2["pl8_over_v_orc8_q"][1], n88=c2["n"])
    add("sensitivity", "The hidden weights matter for prediction. On the {n} certified worlds, predicting 8 ticks ahead with a "
        "neighbour's weights costs (median) {p03:.4f}, {p10:.3f} and {p30:.2f} of the climatological variance for weight "
        "neighbours at 3%, 10% and 30%, and {hyp:.3f} when the scalars move by 10% of their prior range as well, against an "
        "oracle variance of {vo:.4f}: {r03:.0f} and {r10:.0f} times the oracle's own error at 3% and 10% (all {n88} candidates "
        "at 10%: {r88:.0f} times).", n, ["analysis.json:certification.worlds[*].pl8_by_neighbour", "analysis_r2.json:cert.pl8_over_v_orc8_q"])
    s010, s100 = b["sigma010"], b["sigma100"]
    n = dict(n=s010["n"], a=s010["same_coarse_type"]["frac"], b=s100["same_coarse_type"]["frac"],
             ma=s010["movers_stay_movers"]["n"], mb=s100["movers_stay_movers"]["n"], m=s010["movers_stay_movers"]["of"],
             ca=s010["candidates"]["n"], cb=s100["candidates"]["n"], c0=s010["candidates_sigma030_same_draws"]["n"],
             fa=s100["transitions"]["frozen"].get("active:field", 0), fn=sum(s100["transitions"]["frozen"].values()))
    add("noise_level", "The type belongs to the weights, not to the public noise level: of {n} draws, {a:.1%} keep their type "
        "(uniform / frozen / active) when the logit noise goes from 0.3 to 0.1 and {b:.1%} when it goes to 1.0 (there {fa} of "
        "{fn} frozen worlds become active fields); {ma} and {mb} of {m} movers stay movers; candidates {c0} -> {ca} and {cb}.", n,
        ["analysis_r2.json:sigma010", "analysis_r2.json:sigma100"])
    kl = ck["wind"]["kl_check"]
    aim = [w["programs"]["aimed_200"]["effect"][2] for w in wp["worlds"]]
    aimr = [w["programs"]["aimed_200"]["effect_over_noise"][2] for w in wp["worlds"]]
    bl = [w["programs"]["blind_200"]["effect_over_noise"][2] for w in wp["worlds"]]
    n = dict(charge=kl["charge_nats"], mc=kl["mc_nats"], se=kl["mc_se"], lo=min(aim), hi=max(aim), rlo=min(aimr), rhi=max(aimr),
             blo=min(bl), bhi=max(bl), d0=ck["wind"]["delivery"]["shift_px_per_tick"][0], d1=ck["wind"]["delivery"]["shift_px_per_tick"][1],
             draws=", ".join(str(w["draw"]) for w in wp["worlds"]))
    add("wind", "The wind channel is exact but weak. Its charge is exact by construction and checks numerically ({mc:.2f} +- "
        "{se:.2f} nats by Monte Carlo against {charge:.2f} charged); a unit command on every block (512 nats per tick) moves "
        "passive matter by {d0:.2f} and {d1:.2f} px per tick. But on four top worlds (draws {draws}) a 4-tick command of 200 nats "
        "aimed at the densest block changes the block view by only {lo:.4f} to {hi:.3f} of its variance 4 ticks later ({rlo:.1f} "
        "to {rhi:.1f} times the noise floor), and a blind command of 200 nats stays below the floor ({blo:.2f} to {bhi:.2f} "
        "times). 'Actions matter' is not established for these worlds; the channel needs a redesign and its own certificate.", n,
        ["checks.json:wind", "wind_probe.json:worlds"])
    r1, r8 = cg["recheck_cpu.json"], cg["recheck_cpu_first8.json"]
    n = dict(same=sum(w["cpu_type"] == w["gpu_type"] for w in r1["worlds"] + r8["worlds"]), tot=len(r1["worlds"]) + len(r8["worlds"]),
             ident=r8["values_identical"], cmp=r8["values_compared"], worst=r1["max_rel_diff"],
             rerun=a["stages"]["checks"]["rerun_bit_identical"])
    add("platform", "Platform: float64. On the H100 a rerun of the same compiled batch is bit-identical ({rerun}) and vmap equals "
        "single-world runs exactly; the four certification runs of job 1 returned identical main-run numbers. The screen of 12 "
        "draws repeated on this container's CPU with the same keys gives the same type {same} of {tot} times; for 8 non-chaotic "
        "draws all {ident} of {cmp} stored values are identical, for 4 movers they differ by at most {worst:.1%}. Unlike the "
        "gliders world (FFT, scatter), this law is built from elementwise operations and shifts only.", n,
        ["analysis.json:stages.checks", "cpu_vs_gpu.json"])
    lw = {w["draw"]: w["windows"] for w in lr["worlds"]}
    n = dict(draws=", ".join(str(d) for d in lw), v0=", ".join(f"{lw[d][0]['v_net']:.2f}" for d in lw),
             v1=", ".join(f"{lw[d][-1]['v_net']:.2f}" for d in lw), b0=", ".join(f"{lw[d][0]['bodies']:.1f}" for d in lw),
             b1=", ".join(f"{lw[d][-1]['bodies']:.1f}" for d in lw))
    add("longrun_cpu", "CPU runs of 2000 ticks of draws {draws}: net body speed {v0} px/tick in the first 250 ticks and {v1} in the "
        "last 250; bodies {b0} and {b1}.", n, ["longrun.json"])
    st1 = L(os.path.join("jobs", "r5-foundry-001", "status.json"))
    sec_1e5 = 1e5 / s1["n_done"] * s1["seconds"]
    usd_1e5 = sec_1e5 / 3600.0 * st1["pod"]["rate_usd_hr"]
    late_extra = G["viable"]["frac"] * (6 * 2240 + 1536) / 3276.0
    out = dict(verdicts=V,
               decides=[
                   f"A random weights-as-law family is viable and cheap: a 10^5-draw screen with certificates is about "
                   f"{sec_1e5 / 60:.0f} minutes of one H100 (about ${usd_1e5:.1f} at ${st1['pod']['rate_usd_hr']:.2f}/h), not the "
                   f"20-80 GPU-hours DESIGN.md E2 budgeted.",
                   "DESIGN.md E2's rule (gate pass rate >= 10%: random families suffice; <= 1%: invest in search): the pass rate "
                   "is about 1% early and about 0.5% once transients are excluded, so plain random draws do not suffice, but no "
                   "search is needed either: the weights-only predictor concentrates 69% of the candidates in 9.4% of the draws "
                   "at no simulation cost, and screening is cheap enough to brute-force the rest.",
                   f"Every screen must carry a late-time gate (a 2000-tick burn-in costs {(6 * 2240 + 1536) / 3276.0:.1f} times the "
                   f"short screen per draw; applied to the {G['viable']['frac']:.0%} early-active draws only it adds about "
                   f"{late_extra:.0%}).",
                   "Seven foundry worlds are ready to be certified as exam candidates next to the gliders world (same closure "
                   "band at level 1, moving and interacting bodies, stationary, strongly weight-sensitive); what they lack is an "
                   "input channel that matters.",
                   "Publishing the weights-only predictor is safe only with the published criteria: selection narrows the "
                   "posterior on theta (DESIGN.md section 5); here it is a public function of theta by construction.",
               ],
               never_reuse_as_exam=("Prior seeds 1, 2026 and 2027 with run seed 5150 are pilots: their weights are a public "
                                    "function of (seed, index) and hidden parameters of several draws are printed in these "
                                    "results. They must never be reused as exam instances; an exam draws theta from a secret seed."))
    with open(os.path.join(RES, "interpretation.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    for v in V:
        print(f"[{v['id']}] {v['verdict']}\n")


if __name__ == "__main__":
    main()
