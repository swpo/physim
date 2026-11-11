"""make_claims -- study foundryexam: results/summary.json (every quoted number with its source) and a table.

    python -B make_claims.py [--analysis results/analysis.json] [--job r6-foundryexam-002]

Reads results/analysis.json (make_summary.py, from the job's per-item scores), results/job/status*.json (copies of
origin/gpu-jobs:jobs/<job>/status.json) and results/pool.json, wind_probe7.json. Each claim carries
source = {job, file, key}; `file` is a path under this folder and `key` a path inside it; the per-item scores behind
analysis.json are at origin/gpu-jobs:jobs/<job>/out/full/<arm>/scores.npz.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")


def get(d, path):
    for k in path.split("."):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


def q3(q):
    """value, se, 90% interval, median over worlds of a make_summary quantity."""
    return dict(value=round(q["value"], 4), se=round(q["se"], 4), p05=round(q["p05"], 4), p95=round(q["p95"], 4),
                median_world=round(q["median_world"], 4), se_worlds_only=round(q["se_worlds_only"], 4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", default=os.path.join(RES, "analysis.json"))
    ap.add_argument("--job", default="r6-foundryexam-002")
    a = ap.parse_args()
    A = json.load(open(a.analysis))
    job = A["job"]
    claims = []

    def add(cid, text, key, value=None, file="results/analysis.json", jobid=None):
        v = get(A, key) if value is None else value
        if isinstance(v, dict) and "value" in v and "p05" in v:
            v = q3(v)
        claims.append(dict(id=cid, text=text, value=v, source=dict(job=jobid or job, file=file, key=key)))

    for arm, R in A["arms"].items():
        p = f"arms.{arm}"
        acc = R["acceptance"]
        add(f"{arm}.worlds", f"arm {arm}: hidden worlds, items", f"{p}.n_hidden",
            value=dict(n_hidden=R["n_hidden"], n_items=R["n_items"], train_worlds=R["train_worlds"], valid_cells=R["valid_cells"]))
        add(f"{arm}.ceiling", f"arm {arm}: which candidate is the ceiling C", f"{p}.ceiling_is")
        for b in ("C", "Cscratch", "Cmid", "Cbig", "Cft", "Csm", "P0", "P0s", "S@0", "P0w16", "P0w64", "Kp", "plugTrue"):
            if b in R["table"]:
                add(f"{arm}.oes.{b}", f"arm {arm}: pooled oracle-normalised skill of {b}", f"{p}.table.{b}.oes_pooled")
        for fam in ("S", "FT", "D", "Dr"):
            if fam in R["budgets"]["curves"]:
                add(f"{arm}.curve.{fam}", f"arm {arm}: {fam}(N), share of C's skill and pooled OES by Lab budget",
                    f"{p}.budgets.curves.{fam}")
        add(f"{arm}.sigma", f"arm {arm}: science share sigma at the largest budget (null = {acc['null_is']})", f"{p}.acceptance.sigma")
        add(f"{arm}.sigma_verdict", f"arm {arm}: verdict on sigma >= 0.15 from the 90% interval", f"{p}.acceptance.sigma_verdict")
        add(f"{arm}.sigma_no_lab", f"arm {arm}: sigma with no Lab at all (null = best no-experiment policy)", f"{p}.acceptance.sigma_no_lab")
        for N, v in acc["sigma_by_budget"].items():
            add(f"{arm}.sigma@{N}", f"arm {arm}: sigma at Lab budget {N}", f"{p}.acceptance.sigma_by_budget.{N}")
        add(f"{arm}.share_noexp", f"arm {arm}: share of C's skill with no hypothesis and no experiment", f"{p}.acceptance.share_noexp")
        add(f"{arm}.trivial", f"arm {arm}: verdict of criterion 2", f"{p}.acceptance.trivial_verdict")
        for N, v in acc["rho"].items():
            add(f"{arm}.rho@{N}", f"arm {arm}: scripted share rho of amortised inference at {N} Lab episodes", f"{p}.acceptance.rho.{N}")
        for N, v in acc.get("rho_finetune", {}).items():
            add(f"{arm}.rhoFT@{N}", f"arm {arm}: share of the P0-to-C gap closed by fine-tuning P0 on {N} Lab episodes",
                f"{p}.acceptance.rho_finetune.{N}")
        for g in R["gaps_oes"]:
            add(f"{arm}.gap.{g}", f"arm {arm}: gap {g} in pooled OES", f"{p}.gaps_oes.{g}",
                value=dict(q3(R["gaps_oes"][g]), z=None if R["gaps_oes"][g].get("z") is None else round(R["gaps_oes"][g]["z"], 2),
                           by_seed_of=R["gaps_oes"][g]["by_seed_of"]))
        for b, v in R["state_given_loss"].items():
            add(f"{arm}.state_given.{b}", f"arm {arm}: state-given loss 1 - OES of the simulator from the hidden state, {b}",
                f"{p}.state_given_loss.{b}")
        if R["actions"]:
            add(f"{arm}.actions", f"arm {arm}: loss of the input-blind oracle on items with a program, share of the K-to-O range",
                f"{p}.actions.classes_bcd")
            add(f"{arm}.actions_verdict", f"arm {arm}: verdict of criterion 4", f"{p}.actions.verdict")
            add(f"{arm}.actions_worlds", f"arm {arm}: hidden worlds with input-blind loss >= 0.10", f"{p}.actions.worlds_at_least_0p10")
            for c in "bcd":
                add(f"{arm}.actions.{c}", f"arm {arm}: the same for program class {c}", f"{p}.actions.class_{c}")
            if "blind_loss_over_C_excess" in R["actions"]:
                add(f"{arm}.actions_vs_C", f"arm {arm}: input-blind loss over C's own excess above the oracle",
                    f"{p}.actions.blind_loss_over_C_excess")
        for k in ("N90_data_only", "N_P0_data_only", "N90_finetune", "P0_share_of_C"):
            if k in R["budgets"]:
                add(f"{arm}.{k}", f"arm {arm}: {k}", f"{p}.budgets.{k}")
        for hh, e in R.get("by_horizon", {}).items():
            for nm in ("share_noexp", "sigma@8", "sigma@32", "sigma@512"):
                if nm in e:
                    add(f"{arm}.h{hh}.{nm}", f"arm {arm}, horizon {hh} ticks only: {nm} (after-the-fact breakdown)", f"{p}.by_horizon.{hh}.{nm}")
        add(f"{arm}.convergence", f"arm {arm}: convergence by criterion 6 per kind of net", f"{p}.convergence")
        add(f"{arm}.stationarity", f"arm {arm}: share of the variance carried by the tick alone", f"{p}.stationarity")
        add(f"{arm}.oes_by_class", f"arm {arm}: per-cell-mean OES by program class", f"{p}.oes_by_class",
            value={c: {b: round(v[b], 3) for b in ("C", "P0", "plugU0", "plugTrue") if b in v} for c, v in (R["oes_by_class"] or {}).items()})
    add("gate", "exam-time gate: worlds passing by kind", "gate.passed")
    add("job.info", "job: sizes, platform, member-ticks, hours, failed, skipped", "job_info",
        value={k: A["job_info"].get(k) for k in ("size", "arms", "platform", "member_ticks_public_simulator", "hours", "failed", "skipped")})
    pool = json.load(open(os.path.join(RES, "pool.json")))
    claims.append(dict(id="pool", text="public pool of screened worlds by source", value=pool["counts"],
                       source=dict(job="r5-foundry-001, r5-foundry-002", file="results/pool.json", key="counts")))
    claims.append(dict(id="centres", text="centres of the neighbourhood arms and the wind probe's ranking (aimed 200 nats, effect over noise at 4 ticks)",
                       value=pool["centres"]["ranking"], source=dict(job="local CPU", file="results/pool.json", key="centres.ranking")))
    jobs = []
    for f in sorted(os.listdir(os.path.join(RES, "job"))) if os.path.isdir(os.path.join(RES, "job")) else []:
        if f.startswith("status") and f.endswith(".json"):
            st = json.load(open(os.path.join(RES, "job", f)))
            pods = st.get("pods") or []
            jobs.append(dict(job_id=st.get("job_id"), state=st.get("state"), exit_code=st.get("exit_code"), message=st.get("message"),
                             cost=st.get("cost"), gpu=[p.get("gpu_type") or p.get("gpu") for p in pods] or st.get("gpu"),
                             provider=[p.get("provider") for p in pods] or st.get("provider"),
                             rate_usd_hr=[p.get("rate_usd_hr") or p.get("price_hr") for p in pods] or st.get("rate_usd_hr"),
                             started_at=st.get("started_at"), finished_at=st.get("finished_at"), run_hours=st.get("run_hours"),
                             review=(st.get("review") or {}).get("summary"), errors=st.get("errors"),
                             source=f"origin/gpu-jobs:jobs/{st.get('job_id')}/status.json (copy: results/job/{f})"))
    out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, study="foundryexam (round 6): an exam pilot where the hidden law is a network's weights",
               date="2026-11-11", jobs=jobs, design="DESIGN.md (criteria and thresholds declared before any GPU request)",
               claims=claims,
               pilots_never_exam="Every hidden world of this study is a public function of public seeds (prior seeds 2026 and 2027, "
                                 "neighbour seeds 606000 + draw) and its weights are in origin/gpu-jobs:jobs/<job>/out/full/<arm>/worlds.json. "
                                 "They, their Lab data and their items must never be reused as an exam.")
    extra = os.path.join(RES, "summary_extra.json")
    if os.path.exists(extra):
        out.update(json.load(open(extra)))
    with open(os.path.join(RES, "summary.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("claims", len(claims), "jobs", [j["job_id"] for j in jobs])


if __name__ == "__main__":
    main()
