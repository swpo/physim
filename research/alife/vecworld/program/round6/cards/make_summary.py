"""make_summary -- results/summary.json: every number the study claims, with its source (job id, file, key).

Reads results/derived.json, table.json, robustness.json (make_cards.py), results/jobs/<job>/status.json (copies of
origin/gpu-jobs), results/check_cardlib.json, results/cpu_check/. Writes results/summary.json and
results/claims.md (the same claims as sentences, for the README). numpy only.

A source "r6-cards-001:cards/W__R.json:derived.K" means: file out/cards/W__R.json of that job on origin/gpu-jobs,
passed through gates.derive (key K) by make_cards.py; ":gates.K" the same through gates.gates.
"""
from __future__ import annotations

import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

import gates as GT  # noqa: E402

RES = os.path.join(HERE, "results")
J = lambda *p: json.load(open(os.path.join(RES, *p)))
R5_SIGMA = {"n1|block": 0.0053, "n4|block": 0.0175, "n8|block": 0.0126, "n1|pop": 0.0808, "n4|pop": 0.1127, "n8|pop": 0.0408}
R5_SIGMA_SRC = "round5/ladder/results/summary.json:headline.acceptance.sigma_at_mid_budget"


def r(v, n=3):
    if v is None or isinstance(v, (bool, str)):
        return v
    v = float(v)
    return None if not np.isfinite(v) else float(f"{v:.{n}g}")


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    D = J("derived.json")
    jobs_of = D.pop("_jobs")
    T = J("table.json")
    ROB = J("robustness.json")
    W1 = json.load(open(os.path.join(HERE, "worlds.json")))
    W2 = json.load(open(os.path.join(HERE, "worlds2.json")))
    role = {w["name"]: w["role"] for w in W2["worlds"]}
    role.update({w["name"]: w["role"] for w in W1["worlds"]})
    r5type = {w["name"]: w.get("r5_type") for w in W1["worlds"]}

    def src(w, run, key, kind="derived"):
        return f"{jobs_of[w][run]}:cards/{w}__{run.replace('_first', '')}.json:{kind}.{key}"

    def val(w, run, key):
        return D[w][run]["derived"].get(key)

    def gate(w, run, key):
        return D[w][run]["gates"].get(key)
    claims = []

    def claim(cid, text, values, sources):
        claims.append(dict(id=cid, claim=text, values=values, sources=sources))
    names = [t["world"] for t in T]
    # ---------------------------------------------------------------- jobs
    jobs = []
    for jid in sorted(os.listdir(os.path.join(RES, "jobs"))) if os.path.isdir(os.path.join(RES, "jobs")) else []:
        st = J("jobs", jid, "status.json")
        js = J("jobs", jid, "job_state.json") if os.path.exists(os.path.join(RES, "jobs", jid, "job_state.json")) else {}
        cost = st.get("cost") or {}
        jobs.append(dict(job_id=jid, state=st.get("state"), gpu=(st.get("pod") or {}).get("gpu"), provider=(st.get("pod") or {}).get("provider"),
                         rate_usd_hr=(st.get("pod") or {}).get("rate_usd_hr"), billed_usd=cost.get("billed_usd"),
                         conservative_usd=cost.get("conservative_usd"), cap_usd=st.get("cap_usd"), started_at=st.get("started_at"),
                         finished_at=st.get("finished_at") or st.get("updated_at"),
                         billed_hours=None if not cost.get("billed_usd") else r(cost["billed_usd"] / (st.get("pod") or {}).get("rate_usd_hr", float("nan")), 3),
                         pod_requested_at=next((h["at"] for h in st.get("history", []) if h.get("state") == "provisioning"), None),
                         exit_code=st.get("exit_code"), review=(st.get("review") or {}).get("summary"),
                         runs_done=len(js.get("done", [])), runs_failed=js.get("failed"), runs_skipped=js.get("skipped"),
                         presmoke=js.get("presmoke"), presmoke_s=js.get("presmoke_s"), elapsed_s=js.get("elapsed_s"),
                         source=f"origin/gpu-jobs:jobs/{jid}/status.json and out/job_state.json (copies: results/jobs/{jid}/)"))
    # ---------------------------------------------------------------- 1. the card's own test
    ctl = [w for w in names if role.get(w) == "control"]
    test_set = [w for w in ctl if not w.startswith("ctl_diffusion_")]
    rows, n_dull, n_tot = {}, 0, 0
    for w in ctl:
        rows[w] = {run: gate(w, run, "verdict") for run in D[w] if not run.endswith("_first")}
        if w in test_set:
            n_tot += len(rows[w])
            n_dull += sum(1 for v in rows[w].values() if v.startswith("dull"))
    claim("controls", f"The card's own test: {n_dull} of {n_tot} runs of the {len(test_set)} negative controls come out dull "
          "(pure-noise field, uniform and frozen foundry draws, true diffusion, non-interacting bodies; the two no-affinity "
          "worlds that keep the mobility gain are listed but not counted).",
          dict(verdicts=rows, counted=test_set, dull=n_dull, runs=n_tot,
               sigma_hat={w: {run: r(gate(w, run, "sigma_hat_best")) for run in rows[w]} for w in ctl}),
          {w: [src(w, run, "verdict", "gates") for run in rows[w]] for w in ctl})
    # ---------------------------------------------------------------- 2. named worlds
    KEYS = ["grid.pf8", "grid.ceil8", "grid.ceil8_mean", "grid.ceil8_se", "grid.w_theta8", "grid.sigma_hat", "pop.pf8", "pop.ceil8",
            "pop.w_theta8", "pop.sigma_hat", "grid.pl_ratio0.03_8", "grid.pl_ratio0.1_8", "grid.pl_ratio1.0_8", "s.nb_mean",
            "s.half_life_ticks", "s.v_net", "s.events100", "b.pf_disp8", "b.ceil_disp8", "b.ceil_pers_disp8", "b.ceil_field_disp8",
            "b.quiet8", "grid.act_ms", "grid.act_ms_over_vcheap", "grid.act_ms_var", "grid.aim_ratio", "grid.xresp", "grid.tick_share",
            "grid.tick_share_max", "pop.tick_share", "pop.tick_share_max", "grid.member_share", "pop.member_share",
            "x.bodies_to_grid8", "x.grid_to_bodies8", "x.grid_to_pop8", "x.pop_over_pers8", "l.dceil8_AB", "l.dceil8_BA",
            "l.dceil16_AB", "l.dceil16_BA", "l.dceil32_AB", "l.r2_min", "t.l1_8", "t.doubling", "k.law8", "k.law32", "k.lin32",
            "k.const32", "k.pf32", "grid.evidence0.1", "grid.ticks_to_3nats0.1"]
    named = [w for w in names if role.get(w) in ("designed", "shortlist")]
    for w in named:
        run = "A"
        vals = {k: r(val(w, run, k)) for k in KEYS}
        g = D[w][run]["gates"]
        claim(f"card:{w}", f"{w}: {g['verdict']}; sigma_hat {r(g['sigma_hat_best'])} at the {g['sigma_hat_level']} level.",
              dict(vals, gates={k: g[k] for k in g}, verdict_by_run={x: gate(w, x, "verdict") for x in D[w]},
                   late=ROB.get(w, {}).get("late")),
              {k: src(w, run, k) for k in KEYS})
    # ---------------------------------------------------------------- 3. foundry samples
    for tag, sel in (("shortlist", [w for w in names if role.get(w) == "shortlist"]),
                     ("candidates", [w for w in names if role.get(w) == "candidate"]),
                     ("prior", [w for w in names if role.get(w) == "prior"] + [w for w in ctl if w.startswith(("ctl_uniform", "ctl_frozen"))])):
        if not sel:
            continue
        g = lambda k: [bool(gate(w, "A", k)) for w in sel]
        v = lambda k: np.array([np.nan if val(w, "A", k) is None else val(w, "A", k) for w in sel], float)
        late = [ROB.get(w, {}).get("late", {}).get("same") for w in sel]
        late = [x for x in late if x is not None]
        verd = {}
        for w in sel:
            verd[gate(w, "A", "verdict")] = verd.get(gate(w, "A", "verdict"), 0) + 1
        stats = {k: dict(median=r(np.nanmedian(v(k))), mean=r(np.nanmean(v(k))), min=r(np.nanmin(v(k))), max=r(np.nanmax(v(k))))
                 for k in ("grid.ceil8", "grid.pf8", "grid.sigma_hat", "grid.pl_ratio0.03_8", "grid.pl_ratio0.1_8", "s.nb_mean",
                           "s.half_life_ticks", "b.ceil_disp8", "grid.act_ms", "grid.act_ms_over_vcheap", "grid.member_share",
                           "l.dceil16_AB", "x.bodies_to_grid8")}
        claim(f"foundry:{tag}", f"Foundry {tag} ({len(sel)} worlds, run A): {sum(g('exam_worthy'))} exam-worthy, {sum(g('reading_worthy'))} "
              f"reading-worthy, {sum(g('actions'))} pass the actions gate, {sum(g('stationary'))} stationary in the window; "
              f"late window equal to early in {sum(late)} of {len(late)} with a late run.",
              dict(worlds=sel, verdicts=verd, gates={k: int(sum(g(k))) for k in GATE_KEYS}, late_same=int(sum(late)), late_n=len(late),
                   stats=stats, r5_types={w: r5type.get(w) for w in sel}),
              f"r6-cards-001:cards/<world>__A.json for the worlds listed; medians and means over worlds computed here")
    # ---------------------------------------------------------------- 3b. the block level alone (DEVIATIONS.md C1)
    def block_ok(w, run="A"):
        a, b = val(w, run, "grid.sigma_hat"), val(w, run, "grid.pf8")
        return bool(a is not None and b is not None and b >= GT.TH["PF_MIN"] and a >= GT.TH["SIGMA_HAT_MIN"])
    grp = {"designed": [w for w in names if role.get(w) == "designed"], "shortlist": [w for w in names if role.get(w) == "shortlist"],
           "candidates": [w for w in names if role.get(w) == "candidate"], "prior": [w for w in names if role.get(w) == "prior"],
           "controls": ctl}
    runs_of = lambda w: [x for x in D[w] if not x.endswith("_first")]
    claim("block_level", "sigma_hat at the block level alone (robust between seeds and sizes), worlds at or above the 0.15 bar in run A: "
          + "; ".join(f"{k} {sum(block_ok(w) for w in v)} of {len(v)}" for k, v in grp.items()) + ".",
          dict(per_world={w: {x: r(val(w, x, "grid.sigma_hat")) for x in runs_of(w)} for k in ("designed", "shortlist", "controls") for w in grp[k]},
               pop_level={w: {x: r(val(w, x, "pop.sigma_hat")) for x in runs_of(w)} for k in ("designed", "shortlist") for w in grp[k]},
               at_or_above_bar={k: [w for w in v if block_ok(w)] for k, v in grp.items()},
               exam_worthy_by_population_level_only=[w for w in names if gate(w, "A", "exam_worthy") and not block_ok(w)]),
          "<job>:cards/<world>__<run>.json:derived.grid.sigma_hat and derived.pop.sigma_hat (jobs per world in results/derived.json:_jobs)")
    # ---------------------------------------------------------------- 3c. hypotheses that the cards alone can speak to
    vx = [w for w in ("vortex64", "vortex128", "vortex128g16", "vortex64_s4") if w in D]
    claim("H6:vortex_clock", "H6 (a clock takes the population level of the fed vortices): tick share of the population level, mean over "
          "components and its largest component (the kind share), by world and run.",
          {w: {x: dict(mean=r(val(w, x, "pop.tick_share")), max=r(val(w, x, "pop.tick_share_max")), block=r(val(w, x, "grid.tick_share")))
               for x in runs_of(w)} for w in vx},
          {w: [src(w, x, "pop.tick_share") for x in runs_of(w)] for w in vx})
    allw = [w for w in names]
    claim("H7:actions_gate", f"H7: the declared actions gate passes in {sum(bool(gate(w, 'A', 'actions')) for w in allw)} of {len(allw)} worlds "
          f"(run A), including {sum(bool(gate(w, 'A', 'actions')) for w in ctl)} of {len(ctl)} controls: it does not discriminate. "
          "The shift of an aimed 200-nat input in units of the cheap family's error at 4 ticks (added after the first card) does.",
          dict(act_ms={w: r(val(w, "A", "grid.act_ms")) for w in named + ctl},
               act_over_cheap_error={w: {x: r(val(w, x, "grid.act_ms_over_vcheap")) for x in runs_of(w)} for w in named + ctl},
               share_of_variance={w: r(val(w, "A", "grid.act_ms_var")) for w in named + ctl},
               aimed_over_blind={w: r(val(w, "A", "grid.aim_ratio")) for w in named + ctl}),
          "<job>:cards/<world>__<run>.json:derived.grid.act_ms, .grid.act_ms_over_vcheap, .grid.act_ms_var, .grid.aim_ratio")
    claim("H8:learned_variable", f"H8: the learned_differs gate (slow features at least 0.05 more closed than the hand block view at 8 ticks in "
          f"both orders) passes in {sum(bool(gate(w, 'A', 'learned_differs')) for w in allw)} of {len(allw)} worlds in run A.",
          {w: dict(dceil8=[r(val(w, "A", "l.dceil8_AB")), r(val(w, "A", "l.dceil8_BA"))],
                   dceil16=[r(val(w, "A", "l.dceil16_AB")), r(val(w, "A", "l.dceil16_BA"))],
                   dceil32_AB=r(val(w, "A", "l.dceil32_AB")), r2_min=r(val(w, "A", "l.r2_min"))) for w in named},
          "<job>:cards/<world>__A.json:derived.l.*")
    claim("H2:watching_and_experiments", "H2 inputs: evidence index (nats per tick about a 10%-of-prior move of the hidden part, block view), "
          "ticks to 3 nats, and the response difference of an aimed 200-nat input under a prior-sized move (in oracle variances; corrected "
          "estimator only where the run is from r6-cards-002 or the world is a foundry world).",
          {w: dict(evidence=r(val(w, "A", "grid.evidence0.1")), ticks_to_3nats=r(val(w, "A", "grid.ticks_to_3nats0.1")),
                   xresp=r(val(w, "A", "grid.xresp")), job=jobs_of[w]["A"]) for w in named},
          "<job>:cards/<world>__A.json:derived.grid.evidence0.1, .grid.ticks_to_3nats0.1, .grid.xresp")
    claim("structure", "Bodies and the single-body law (quiet steps, displacement at 8 ticks) of the named worlds, runs A / B / late.",
          {w: {x: dict(bodies=r(val(w, x, "s.nb_mean")), half_life=r(val(w, x, "s.half_life_ticks")), v_net=r(val(w, x, "s.v_net")),
                       events100=r(val(w, x, "s.events100")), quiet8=r(val(w, x, "b.quiet8")), body_pf8=r(val(w, x, "b.pf_disp8")),
                       body_ceil8=r(val(w, x, "b.ceil_disp8")), inertia_ceil8=r(val(w, x, "b.ceil_pers_disp8")),
                       with_field_ceil8=r(val(w, x, "b.ceil_field_disp8"))) for x in runs_of(w)} for w in named + ["ctl_freebodies"]},
          "<job>:cards/<world>__<run>.json:derived.s.*, .b.*")
    claim("stationarity", "Member share (variance between members' time-means) of the block view, runs A / B / late, named worlds.",
          {w: {x: dict(member_share=r(val(w, x, "grid.member_share")), pop_member_share=r(val(w, x, "pop.member_share")),
                       stationary_gate=gate(w, x, "stationary")) for x in runs_of(w)} for w in named},
          "<job>:cards/<world>__<run>.json:derived.grid.member_share")
    # ---------------------------------------------------------------- 4. robustness
    seed_w = [w for w in names if "seed" in ROB.get(w, {})]
    if seed_w:
        per = {k: [ROB[w]["seed"][k] for w in seed_w] for k in ROB[seed_w[0]]["seed"]}
        frac = {k: r(np.mean(v)) for k, v in per.items()}
        gsame = {k: r(np.mean([ROB[w]["seed_gates"][k] for w in seed_w])) for k in ROB[seed_w[0]]["seed_gates"]}
        claim("robust:seed", f"Seed robustness over {len(seed_w)} worlds with runs A and B (agreement within 0.05 or 25%): "
              f"entries that agree in at least 90% of worlds: {sorted(k for k, v in frac.items() if v >= 0.9)}; below 70%: "
              f"{sorted(k for k, v in frac.items() if v < 0.7)}.",
              dict(worlds=seed_w, share_of_worlds_agreeing=frac, gates_same_share=gsame,
                   gate_flips={w: [k for k, v in ROB[w]["seed_gates"].items() if not v] for w in seed_w if not all(ROB[w]["seed_gates"].values())}),
              "results/robustness.json:<world>.seed, .seed_gates (from runs A and B of each world)")
    size_w = [w for w in names if "size" in ROB.get(w, {})]
    if size_w:
        keys = sorted(set(k for w in size_w for k in ROB[w]["size"]))
        frac = {k: r(np.mean([ROB[w]["size"][k] for w in size_w if k in ROB[w]["size"]])) for k in keys}
        claim("robust:size", f"Size robustness over {len(size_w)} worlds (64 px against 128 px, counts per area, action entries "
              f"left out): entries that agree in at least 90%: {sorted(k for k, v in frac.items() if v >= 0.9)}; below 70%: "
              f"{sorted(k for k, v in frac.items() if v < 0.7)}.",
              dict(worlds={w: ROB[w].get("size_against") for w in size_w}, share_of_worlds_agreeing=frac,
                   gate_flips={w: [k for k, v in ROB[w]["size_gates"].items() if not v] for w in size_w if not all(ROB[w]["size_gates"].values())}),
              "results/robustness.json:<world>.size, .size_gates")
    late_w = [w for w in names if "late" in ROB.get(w, {})]
    if late_w:
        claim("robust:late", f"Late window against early ({len(late_w)} worlds): the same statistics in "
              f"{sum(1 for w in late_w if ROB[w]['late']['same'])}; not in {[w for w in late_w if not ROB[w]['late']['same']]}.",
              {w: dict(same=ROB[w]["late"]["same"], count_ratio=r(ROB[w]["late"]["count_ratio"]),
                       d_mean_max=r(np.max(np.abs(ROB[w]["late"]["d_mean"]))), log_sd_max=r(np.max(np.abs(ROB[w]["late"]["log_sd_ratio"]))),
                       ceil8=[r(x) for x in ROB[w]["late"]["ceil8"]], sigma_hat=[r(x) for x in ROB[w]["late"]["sigma_hat"]],
                       verdict=ROB[w]["late"]["verdict"]) for w in late_w},
              "results/robustness.json:<world>.late (runs A and late of each world)")
    sh_w = [w for w in names if "split_half" in ROB.get(w, {})]
    if sh_w:
        claim("robust:estimator_size", f"Estimator size (even against odd test states, 16 each): the block view's ceiling at 8 ticks "
              f"agrees in {sum(1 for w in sh_w if ROB[w]['split_half']['ceil8_agree'])} of {len(sh_w)} worlds, its predictable "
              f"fraction in {sum(1 for w in sh_w if ROB[w]['split_half']['pf8_agree'])}.",
              dict(not_agreeing=[w for w in sh_w if not ROB[w]["split_half"]["ceil8_agree"]]),
              "results/robustness.json:<world>.split_half (from series/<world>__A.npz per-state arrays)")
    rr_w = [w for w in names if "rerun" in ROB.get(w, {})]
    if rr_w:
        claim("robust:rerun", "The same seeds simulated in both jobs (run A of " + ", ".join(rr_w) + "): entries agreeing "
              + ", ".join(f"{w} {sum(ROB[w]['rerun'].values())}/{len(ROB[w]['rerun'])}" for w in rr_w) + ".",
              {w: dict(values_first_second=ROB[w]["rerun_values"], jobs=ROB[w]["rerun_jobs"],
                       not_agreeing=[k for k, v in ROB[w]["rerun"].items() if not v],
                       xresp_first_job_biased_low=r(ROB[w]["xresp_first_biased"]), xresp_corrected=r(val(w, "A", "grid.xresp"))) for w in rr_w},
              "results/robustness.json:<world>.rerun")
    # platform
    cpu = os.path.join(RES, "cpu_check", "foundry_04470__A.json")
    if os.path.exists(cpu) and "foundry_04470" in D:
        c = json.load(open(cpu))
        dc = GT.derive(c)
        w, run = "foundry_04470", "A"
        keys = ["grid.pf8", "grid.ceil8", "grid.sigma_hat", "grid.pl_ratio0.1_8", "s.nb_mean", "s.half_life_ticks", "b.ceil_disp8",
                "grid.act_ms", "grid.member_share", "pop.ceil8", "l.dceil16_AB"]
        claim("robust:platform", "CPU (this container) against the GPU job for foundry draw 4470, run A, same code and seeds: "
              f"{sum(GT.robust(dc.get(k), val(w, run, k)) for k in keys)} of {len(keys)} entries agree; verdict {GT.gates(dc)['verdict']!r} "
              f"against {gate(w, run, 'verdict')!r}.",
              {k: dict(cpu=r(dc.get(k)), gpu=r(val(w, run, k))) for k in keys},
              dict(cpu="results/cpu_check/foundry_04470__A.json", gpu=src(w, run, "<key>")))
    # ---------------------------------------------------------------- 5. cost
    groups = {}
    for t in T:
        key = t["family"] + ("" if not t["world"].startswith(("foundry128", "vortex128")) else "128") + ("_s4" if t["world"].endswith("_s4") else "")
        if t["world"].startswith("vortex"):
            key = t["world"].split("g16")[0]
        if t.get("cost_includes_compile"):
            continue
        groups.setdefault(key, []).append(t["ms_per_mt"])
    rate = next((j["rate_usd_hr"] for j in jobs if j.get("rate_usd_hr")), None)
    cost = {k: dict(ms_per_member_tick=r(np.median(v)), member_ticks_per_s=r(1e3 / np.median(v)), n_worlds=len(v),
                    usd_per_million_member_ticks=None if not rate else r(rate * np.median(v) / 3600e3 * 1e6)) for k, v in groups.items()}
    claim("cost", "Cost per member-tick on the job's GPU with the tracker on every member, compile excluded (median over worlds of a group).",
          cost, "results/table.json:ms_per_mt (from timing of runs that were not the first call of their program)")
    # ---------------------------------------------------------------- 6. H1 retrodiction on the gliders cells
    cells = {"n1": "gliders_n1", "n4": "gliders", "n8": "gliders_n8"}
    if all(w in D for w in cells.values()):
        sh, sg, lab, srcs = [], [], [], {}
        for n, w in cells.items():
            for lv, name in (("grid", "block"), ("pop", "pop")):
                v = np.nanmean([x for x in (val(w, run, f"{lv}.sigma_hat") for run in ("A", "B") if run in D[w]) if x is not None])
                sh.append(float(v))
                sg.append(R5_SIGMA[f"{n}|{name}"])
                lab.append(f"{n}|{name}")
                srcs[f"{n}|{name}"] = [src(w, run, f"{lv}.sigma_hat") for run in ("A", "B") if run in D[w]]
        claim("H1:gliders_cells", f"H1 on the six gliders cells whose science share round 5 measured: Spearman rank correlation of "
              f"sigma_hat with the measured share {spearman(sh, sg):.2f}; sigma_hat >= the measured share in "
              f"{sum(a >= b for a, b in zip(sh, sg))} of 6 cells (it is an upper screen).",
              dict(cells=lab, sigma_hat=[r(x) for x in sh], sigma_round5=sg, spearman=r(spearman(sh, sg)),
                   mean_ratio=r(np.mean(np.array(sh) / np.maximum(np.array(sg), 1e-3)))),
              dict(sigma_hat=srcs, sigma_round5=R5_SIGMA_SRC))
    # ---------------------------------------------------------------- 7. the tick of the clock
    for a, b in (("membrane", "membrane_s4"), ("vortex64", "vortex64_s4")):
        if a in D and b in D:
            keys = ["grid.pf8", "grid.ceil8", "grid.w_theta8", "grid.sigma_hat", "pop.pf8", "pop.ceil8", "pop.sigma_hat", "b.ceil_disp8",
                    "pop.tick_share", "pop.tick_share_max", "l.dceil8_AB", "l.dceil16_AB", "grid.act_ms", "k.law8", "k.law32", "k.const32"]
            claim(f"clock:{a}", f"{a} on a clock of 1 world tick against 4: verdict {gate(a, 'A', 'verdict')!r} against {gate(b, 'A', 'verdict')!r}.",
                  {k: [r(val(a, "A", k)), r(val(b, "A", k))] for k in keys},
                  {k: [src(a, "A", k), src(b, "A", k)] for k in keys})
    out = dict(study="cards (round 6): world cards", date="2026-11-11", PILOT_NEVER_REUSE_AS_EXAM=True, jobs=jobs,
               gpu_total=dict(billed_usd=r(sum(j["billed_usd"] or 0 for j in jobs), 4), conservative_usd=r(sum(j["conservative_usd"] or 0 for j in jobs), 4),
                              budget_usd=25.0, source="results/jobs/<job>/status.json:cost"),
               thresholds=GT.TH, claims=claims,
               check_cardlib=dict(passed=J("check_cardlib.json")["passed"], source="results/check_cardlib.json"))
    json.dump(out, open(os.path.join(RES, "summary.json"), "w"), indent=1, default=float)
    with open(os.path.join(RES, "claims.md"), "w") as f:
        for c in claims:
            f.write(f"- **{c['id']}** {c['claim']}\n")
    print(len(claims), "claims ->", os.path.join(RES, "summary.json"))


GATE_KEYS = ["exam_worthy", "structure", "interaction", "reading_worthy", "actions", "stationary", "levels_add", "learned_differs"]
if __name__ == "__main__":
    main()
