"""extras -- study foundryexam: derived numbers for the summary (CPU, instant). Writes results/summary_extra.json,
which make_claims.py merges into results/summary.json. Everything here was written AFTER the results were seen
(descriptive; no declared criterion depends on it).

    python -B extras.py [--analysis results/analysis.json] [--first results/analysis_job003.json]

  weight_error_equivalent  the eps of a weight neighbour whose state-given skill equals a policy's skill (log-linear
                           interpolation between the plug-ins at eps 0.03, 0.1, 0.3): how well an agent holding the
                           hidden state would have to know the weights to match C, FT(512) or P0
  compute                  what the no-experiment policy costs in member-ticks and in episodes with burn-in
                           (332 ticks): the screen that finds the prior worlds, the gate, the training simulations
  between_jobs             arm P, final job against the first full job (same hidden and training worlds; other
                           items, Labs and training seeds), and whether the N arms have the same hidden worlds
  tracker, wind            the round-5 screen's tracker measures of the three centres; the CPU wind probe
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
FOUNDRY = os.path.abspath(os.path.join(HERE, "..", "..", "round5", "foundry"))


def eps_equiv(skill, plug):
    """eps at which the state-given skill (1 - loss) equals `skill`, by log-linear interpolation."""
    pts = [(0.03, 1 - plug["plug03"]), (0.1, 1 - plug["plug10"]), (0.3, 1 - plug["plug30"])]
    if skill >= pts[0][1]:
        return "below 0.03"
    for (e0, s0), (e1, s1) in zip(pts[:-1], pts[1:]):
        if s1 <= skill <= s0:
            f = (s0 - skill) / (s0 - s1)
            return round(math.exp(math.log(e0) + f * (math.log(e1) - math.log(e0))), 3)
    return "above 0.3"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", default=os.path.join(RES, "analysis.json"))
    ap.add_argument("--first", default=os.path.join(RES, "analysis_job003.json"))
    a = ap.parse_args()
    A = json.load(open(a.analysis))
    out = {}
    we = {}
    for arm, R in A["arms"].items():
        plug = {k: R["state_given_loss"][k]["value"] for k in ("plug03", "plug10", "plug30")}
        T = R["table"]
        we[arm] = dict(state_given_skill={k: round(1 - v, 3) for k, v in plug.items()},
                       eps_equivalent={b: eps_equiv(T[b]["oes_pooled"]["value"], plug) for b in ("C", "FT@512", "D@512", "P0", "Dr@8") if b in T})
    out["weight_error_equivalent"] = dict(
        what="eps of a weight neighbour (W = sqrt(1 - eps^2) W_true + eps W_fresh) whose simulator, run from the hidden state, "
             "has the same pooled skill as the policy; log-linear interpolation between eps 0.03, 0.1, 0.3; written after the results",
        source="results/analysis.json: arms.<arm>.state_given_loss and arms.<arm>.table", arms=we)
    # ---- by horizon (per cell): share of C's skill and sigma against the Lab budget, point values on seed-mean scores
    bh = {}
    for arm, R in A["arms"].items():
        oc = R["oes_by_cell"]
        hs = [c[1] for c in R["cells"]]
        sh = lambda b: [oc[b][j] / oc["C"][j] for j in range(len(hs))]
        e = dict(horizons=hs, oes_C=[round(x, 3) for x in oc["C"]], oes_P0=[round(x, 3) for x in oc["P0"]],
                 share_noexp=[round(max(sh(b)[j] for b in ("P0", "S@0", "P0s") if b in oc), 3) for j in range(len(hs))])
        for N in (8, 32, 128, 512):
            cand = [b for b in (f"D@{N}", f"FT@{N}", f"Dr@{N}", "P0", "S@0") if b in oc]
            e[f"sigma@{N}"] = [round(1.0 - max(sh(b)[j] for b in cand), 3) for j in range(len(hs))]
        bh[arm] = e
    out["by_horizon"] = dict(what="per query horizon: oracle-normalised skill of C and P0, the share of C's skill taken with no hypothesis "
                                  "and no experiment, and sigma against the Lab budget (1 - best null share); point values, written after the results",
                             source="results/analysis.json: arms.<arm>.oes_by_cell", arms=bh)
    # ---- compute of the no-experiment policy (arm P)
    pool = json.load(open(os.path.join(RES, "pool.json")))
    gate = A["gate"]["passed"]
    n_e27, ok_e27 = gate["pool:enriched2027"]["of"], gate["pool:enriched2027"]["ok"]
    mt_enrich = 13418496                                   # round5/foundry/results/analysis_r2.json: arms_run.enrich.member_ticks (4096 draws)
    mt_screen1 = 8192 * 3276                               # r5-foundry-001: 8192 draws x 3276 member-ticks (round5/foundry/README.md)
    per_cand_enriched = mt_enrich / (323 + 5)
    per_cand_plain = mt_screen1 / 88
    gate_mt = 8 * 332
    R = A["arms"]["P"]
    nW = R["train_worlds"][0]
    pass_rate = ok_e27 / n_e27
    epw, ep_ticks = 64, 332

    def cost(n_worlds, per_cand):
        find = n_worlds / pass_rate * (per_cand + gate_mt)
        train = n_worlds * epw * ep_ticks
        return dict(worlds=n_worlds, find_member_ticks=round(find), train_member_ticks=train, total_member_ticks=round(find + train),
                    total_episodes_with_burn_in=round((find + train) / ep_ticks))
    out["compute"] = dict(
        what="member-ticks an agent needs for the no-experiment policy of arm P: finding screened worlds (round-5 screen with the "
             "weights-only pre-screen: member-ticks of job r5-foundry-002's enrichment arm per candidate found; without it: job "
             "r5-foundry-001's screen per candidate), the exam-time gate (8 members x 332 ticks per candidate), 64 training episodes "
             "per world; one episode with burn-in = 332 ticks. Written after the results; weight statistics of the pre-screen not counted.",
        member_ticks_per_candidate=dict(with_prescreen=round(per_cand_enriched), without=round(per_cand_plain)),
        gate_pass_rate_enriched=round(pass_rate, 3),
        with_prescreen={f"P0[{n}]": cost(n, per_cand_enriched) for n in (16, 64, nW)},
        without_prescreen={f"P0[{n}]": cost(n, per_cand_plain) for n in (16, 64, nW)},
        skill={f"P0[{n}]": R["table"][k]["oes_pooled"]["value"] for n, k in ((16, "P0w16"), (64, "P0w64"), (nW, "P0")) if k in R["table"]},
        share_of_C={f"P0[{n}]": R["table"][k]["share_of_C"]["value"] for n, k in ((16, "P0w16"), (64, "P0w64"), (nW, "P0")) if k in R["table"]},
        lab_512_episodes_member_ticks=512 * 333, gliders_P0_episodes="about 2,300 (roadmap/DECISIONS.md, decision 2)",
        sources=dict(enrich="round5/foundry/results/analysis_r2.json: arms_run.enrich.member_ticks", screen="round5/foundry/README.md",
                     gate="results/analysis.json: gate.passed", pool=pool["counts"]))
    # ---- between jobs
    if os.path.exists(a.first) and os.path.abspath(a.first) != os.path.abspath(a.analysis):
        B = json.load(open(a.first))
        bj = dict(this_job=A["job"], first_job=B["job"], arm_P={}, hidden_labels={})
        for b in ("C", "Cft", "Cscratch", "P0", "P0s", "S@0", "S@512", "FT@8", "FT@32", "FT@128", "FT@512", "D@8", "D@32", "D@128", "D@512",
                  "Dr@8", "Dr@512", "P0w16", "P0w64", "Kp", "plugPrior", "plug03", "plug10", "plug30", "plugU0"):
            if b in A["arms"]["P"]["table"] and b in B["arms"]["P"]["table"]:
                x, y = A["arms"]["P"]["table"][b]["oes_pooled"], B["arms"]["P"]["table"][b]["oes_pooled"]
                bj["arm_P"][b] = dict(this=round(x["value"], 4), first=round(y["value"], 4), diff=round(x["value"] - y["value"], 4))
        for nm in ("share_noexp", "sigma", "sigma_no_lab"):
            x, y = A["arms"]["P"]["acceptance"][nm], B["arms"]["P"]["acceptance"][nm]
            bj["arm_P"][nm] = dict(this=round(x["value"], 4), first=round(y["value"], 4), diff=round(x["value"] - y["value"], 4),
                                   se_this=round(x["se"], 4))
        for arm in A["arms"]:
            if arm in B["arms"]:
                la, lb = A["arms"][arm]["hidden_labels"], B["arms"][arm]["hidden_labels"]
                bj["hidden_labels"][arm] = dict(same=la == lb, only_this=sorted(set(la) - set(lb)), only_first=sorted(set(lb) - set(la)),
                                                train_worlds_this=A["arms"][arm]["train_worlds"], train_worlds_first=B["arms"][arm]["train_worlds"])
        bj["what"] = ("arm P: the same hidden worlds and training worlds in both jobs; items, Labs, noise secret and every training seed "
                      "differ, and C has more data and steps in the final job. Pooled skill.")
        out["between_jobs"] = bj
    # ---- tracker (round-5 screen) and wind probe
    per = json.load(gzip.open(os.path.join(FOUNDRY, "results", "per_draw.json.gz"), "rt"))
    pos = {int(d): i for i, d in enumerate(per["draw"])}
    out["tracker_centres"] = dict(
        what="round-5 screen (job r5-foundry-001, ticks 50-290) of the three centres: mean number of tracked bodies, share of the mass "
             "in bodies, fusions + fissions per 100 ticks and member. The object view is not examined in this pilot.",
        source="round5/foundry/results/per_draw.json.gz",
        centres={str(c): {k: per[k][pos[c]] for k in ("nb_mean", "body_frac", "events100", "v_net")} for c in pool["centres"]["chosen"]})
    out["wind_probe"] = dict(what="CPU probe before the exam (round5/foundry/wind_probe.py, 8 states per world): aimed 200-nat command, "
                                  "displacement of the block view at 4 ticks over twice the noise floor, and in units of the variance",
                             source="results/wind_probe7.json", ranking=pool["centres"]["ranking"], chosen=pool["centres"]["chosen"])
    # ---- gate at both thresholds, nets trained, largest seed-to-seed difference
    job = A["job"]
    gp = os.path.join(RES, "job", f"{job}_full_gate.json")
    if os.path.exists(gp):
        rows = [r for r in json.load(open(gp))["rows"] if r["kind"] == "pool"]
        base = lambda r: r["cv_cell"] >= 0.25 and r["vp1"] <= 1.0
        out["gate_thresholds"] = dict(
            what="pool worlds passing the exam-time gate with the activity threshold at 0.02 (first version of DESIGN.md) and at 0.2 (used)",
            source=f"results/job/{job}_full_gate.json: rows", pool=len(rows),
            pass_at_0p02=sum(1 for r in rows if base(r) and r["vp16"] >= 0.02), pass_at_0p2=sum(1 for r in rows if base(r) and r["vp16"] >= 0.2),
            median_vp16_of_passing=sorted(r["vp16"] for r in rows if r["ok"])[sum(1 for r in rows if r["ok"]) // 2])
    pp = os.path.join(RES, "job", f"{job}_full_progress.txt")
    if os.path.exists(pp):
        import re
        nets = {m.group(1): int(m.group(2)) for m in re.finditer(r"\] (\w+) all nets done \(\d+s\), (\d+) nets", open(pp).read())}
        out["nets_trained"] = dict(per_arm=nets, total=sum(nets.values()), source=f"results/job/{job}_full_progress.txt")
    sd = {}
    for arm, R in A["arms"].items():
        d = [abs(v[0] - v[1]) for q in R["gaps_oes"].values() for v in q["by_seed_of"].values() if len(v) == 2]
        sd[arm] = round(max(d), 4) if d else None
    out["seed_to_seed"] = dict(what="largest difference of any pooled-skill gap between the two training seeds of one of its policies",
                               source="results/analysis.json: arms.<arm>.gaps_oes.*.by_seed_of", arms=sd)
    with open(os.path.join(RES, "summary_extra.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out["by_horizon"]["arms"]))
    print(json.dumps(out["weight_error_equivalent"]["arms"]))
    print(json.dumps(out["compute"]["with_prescreen"]), out["compute"]["share_of_C"])
    if "between_jobs" in out:
        print(json.dumps(out["between_jobs"]["hidden_labels"]))


if __name__ == "__main__":
    main()
