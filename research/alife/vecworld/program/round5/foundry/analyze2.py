"""analyze2 -- from the outputs of job 2 (job2.py) to results/analysis_r2.json (CPU, seconds).

    python -B analyze2.py <job2_out_dir> [--job r5-foundry-002] [--out results]

Needs results/per_draw.json.gz (the types of job 1) and sel_r2.json (the arms of the enrichment test).
Parts, one per arm:
  enrich   yields of every target in the enriched arm (the best 9.4% of a fresh pool by the weights-only
           score) and in the control arm, against the yields predicted from job 1 before the run
           (sel_r2.json: prediction_from_job1). The control arm is a random sample of the UNSELECTED part
           of the pool (select_enriched.py takes the first unselected pool indices), not of the whole
           prior; the rate over the whole pool is therefore the share-weighted mix of the two arms
           (`pool_rate`), and the enrichment is quoted against that (`enrichment_over_pool`)
  late     type at ticks 2000-2240 against the type at ticks 50-290 (job 1) for the same draws: transition
           counts; what remains of the candidates; descriptors early and late
  sigma    type under logit noise 0.1 and 1.0 against the type at 0.3 (job 1) for draws 0..2047
  cert     the candidates of job 1 at the certification size: gates, descriptors, how many look like the
           gliders world in the closure profile
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import analyze as AN  # noqa: E402
import criteria as CR  # noqa: E402

frac, q = AN.frac, AN.q


def load_arm(D, name, st=None):
    """The arm's chunks. Only the chunks recorded in job2_state.json are read (a chunk file is written
    before the state, so a file without a record may be incomplete: review of r5-foundry-002, point 3)."""
    d = os.path.join(D, name)
    if not os.path.isdir(d):
        return None
    files = sorted(f for f in os.listdir(d) if f.startswith("chunk_"))
    if st is not None:
        files = files[:len((st["arms"].get(name) or {}).get("chunks", []))]
    if not files:
        return None
    parts = [dict(np.load(os.path.join(d, f))) for f in files]
    skip = ("thumb_u8", "thumb_scale", "thumb_index")
    return {k: np.concatenate([p[k] for p in parts]) for k in parts[0] if k not in skip}


def typed(m, T):
    d = CR.derive(m, T)
    t = CR.classify(d)
    g = CR.gates(d, t)
    return d, t, g, CR.score(d, t)


def transitions(t0, t1):
    """Counts[type before][type after], only the non-empty rows and columns."""
    out = {}
    for i, a in enumerate(CR.TYPES):
        row = {b: int(((t0 == i) & (t1 == j)).sum()) for j, b in enumerate(CR.TYPES)}
        if sum(row.values()):
            out[a] = {b: v for b, v in row.items() if v}
    return out


def coarse(t):
    """0 uniform, 1 frozen, 2 active (other types: 3)."""
    return np.where(t == 2, 0, np.where(t == 3, 1, np.where(t >= 5, 2, 3)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_out")
    ap.add_argument("--job", default="r5-foundry-002")
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    a = ap.parse_args()
    D = a.job_out
    st = json.load(open(os.path.join(D, "job2_state.json")))
    per = json.load(gzip.open(os.path.join(a.out, "per_draw.json.gz"), "rt"))
    p_draw, p_type, p_cand, p_score = (np.array(per[k]) for k in ("draw", "type", "candidate", "score"))
    pos1 = {int(v): i for i, v in enumerate(p_draw)}
    res = dict(job=a.job, platform=st.get("platform"), ok=st.get("ok"), errors=st.get("errors"),
               seconds_total=st.get("seconds_total"),
               arms_run={k: {kk: v.get(kk) for kk in ("n_planned", "n_done", "seconds", "member_ticks_per_s_steady", "sizes",
                                                      "prior_seed", "stopped", "failed", "skipped")}
                         for k, v in st["arms"].items()})
    for k, v in res["arms_run"].items():
        v["family_sigma"] = (st["arms"][k].get("family") or {}).get("sigma")
        v["member_ticks"] = int(sum(c["member_ticks"] for c in st["arms"][k].get("chunks", [])))

    def tgt(t, g):
        return dict(structured=(t >= 3), active=(t >= 5), movers=(t == 7), closure_gate=g["closure"], candidate=g["candidate"])

    # ---------------- enrich
    m = load_arm(D, "enrich", st)
    if m is not None:
        sel = json.load(open(os.path.join(HERE, "sel_r2.json")))
        d, t, g, s = typed(m, st["arms"]["enrich"]["sizes"]["T"])
        idx = m["index"].astype(int)
        targets = tgt(t, g)
        arms = {}
        for arm in ("enriched", "control"):
            mk = np.isin(idx, np.asarray(sel[arm]))
            arms[arm] = dict(n=int(mk.sum()), planned=len(sel[arm]), yields={k: frac(v[mk]) for k, v in targets.items()},
                             types={CR.TYPES[i]: int((t[mk] == i).sum()) for i in range(len(CR.TYPES))},
                             n_score_above_0p9=int((s[mk] > 0.9).sum()))
        en, co = arms["enriched"]["yields"], arms["control"]["yields"]
        base1 = sel["prediction_from_job1"]["base_rate"]
        sh = sel["prediction_from_job1"]["share_selected"]
        pool_rate = {k: dict(frac=sh * en[k]["frac"] + (1 - sh) * co[k]["frac"],
                             se=float(np.sqrt((sh * en[k]["se"]) ** 2 + ((1 - sh) * co[k]["se"]) ** 2))) for k in en}
        res["enrich"] = dict(
            src="enrich/chunk_*.npz + sel_r2.json", target=sel["target"], pool=sel["pool"], prior_seed=sel["prior_seed"],
            share_selected=sel["prediction_from_job1"]["share_selected"], prediction_from_job1=sel["prediction_from_job1"],
            arms=arms, control_is="a random sample of the unselected 90.6% of the pool, not of the whole prior",
            pool_rate=pool_rate,
            enrichment_over_pool={k: en[k]["frac"] / pool_rate[k]["frac"] for k in en},
            share_of_all_found_in_selected={k: sh * en[k]["frac"] / pool_rate[k]["frac"] for k in en},
            enrichment_over_unselected={k: (en[k]["frac"] / co[k]["frac"] if co[k]["frac"] and co[k]["frac"] > 0 else None)
                                     for k in en},
            enrichment_over_job1_base={k: en[k]["frac"] / base1[k] for k in en},
            observed_minus_predicted_in_se={k: (en[k]["frac"] - sel["prediction_from_job1"]["predicted_yield"][k])
                                            / max(en[k]["se"], 1e-9) for k in en},
            top_enriched=[dict(draw=int(idx[i]), **AN.world_row(d, i, t, g, s))
                          for i in np.argsort(-s, kind="stable")[:12]])
    # ---------------- late
    m = load_arm(D, "late", st)
    if m is not None:
        d, t, g, s = typed(m, st["arms"]["late"]["sizes"]["T"])
        idx = m["index"].astype(int)
        j = np.array([pos1[int(i)] for i in idx])
        t0, c0 = p_type[j], p_cand[j]
        e = json.load(gzip.open(os.path.join(a.out, "per_draw.json.gz"), "rt"))
        early = {k: np.array([np.nan if v is None else v for v in e[k]], float)[j] for k in ("nb_mean", "v_net", "events100",
                                                                                              "ceil8", "moved", "gap_max")}
        act0, mov0 = t0 >= 5, t0 == 7
        res["late"] = dict(
            src="late/chunk_*.npz against results/per_draw.json.gz (job 1)", burn=st["arms"]["late"]["sizes"]["burn"], n=len(idx),
            transitions=transitions(t0, t),
            active_stays_active=frac((t >= 5)[act0]), active_becomes_frozen=frac((t == 3)[act0]),
            active_becomes_uniform=frac((t == 2)[act0]),
            movers_stay_movers=frac((t == 7)[mov0]), movers_stay_active=frac((t >= 5)[mov0]),
            candidates_stay_candidates=frac(g["candidate"][c0]), candidates_stay_movers=frac((t == 7)[c0]),
            candidates_stay_active=frac((t >= 5)[c0]),
            frozen_sample_changes=frac((t != 3)[t0 == 3]), frozen_sample_becomes_active=frac((t >= 5)[t0 == 3]),
            uniform_sample_changes=frac((t != 2)[t0 == 2]), uniform_sample_becomes_active=frac((t >= 5)[t0 == 2]),
            new_candidates_among_non_candidates=frac(g["candidate"][~c0 & act0]),
            candidates_early_late_median={k: [float(np.nanmedian(early[k][c0])), float(np.nanmedian(d[k][c0]))]
                                          for k in early},
            movers_early_late_median={k: [float(np.nanmedian(early[k][mov0])), float(np.nanmedian(d[k][mov0]))]
                                      for k in early},
            late_candidates=[int(i) for i in idx[g["candidate"] & c0]],
            validity=dict(mass_drift_max=float(np.nanmax(d["mass_drift"])), finite_all=bool((d["finite"] > 0.5).all())))
    # ---------------- sigma
    for name in ("sigma010", "sigma100"):
        m = load_arm(D, name, st)
        if m is None:
            continue
        d, t, g, s = typed(m, st["arms"][name]["sizes"]["T"])
        idx = m["index"].astype(int)
        j = np.array([pos1[int(i)] for i in idx])
        t0 = p_type[j]
        same = coarse(t0) == coarse(t)
        res[name] = dict(src=f"{name}/chunk_*.npz against results/per_draw.json.gz (job 1, sigma 0.3)",
                         sigma=st["arms"][name]["family"]["sigma"], n=len(idx), transitions=transitions(t0, t),
                         types={CR.TYPES[i]: frac(t == i) for i in range(len(CR.TYPES)) if (t == i).any()},
                         types_sigma030_same_draws={CR.TYPES[i]: frac(t0 == i) for i in range(len(CR.TYPES)) if (t0 == i).any()},
                         same_coarse_type=frac(same), same_exact_type=frac(t0 == t),
                         movers_stay_movers=frac((t == 7)[t0 == 7]), movers_stay_active=frac((t >= 5)[t0 == 7]),
                         candidates=frac(g["candidate"]), candidates_sigma030_same_draws=frac(p_cand[j]),
                         candidates_stay=frac(g["candidate"][p_cand[j]]),
                         twin_doubling_active_q=q(d["twin_doubling"][t >= 5]), v_orc8_active_q=q(d["v_orc8"][t >= 5]))
    # ---------------- cert
    m = load_arm(D, "cert", st)
    if m is not None:
        d, t, g, s = typed(m, st["arms"]["cert"]["sizes"]["T"])
        idx = m["index"].astype(int)
        c1, c8, c32 = d["ceil1"], d["ceil8"], d["ceil32"]
        like = (c1 >= 0.95) & (c8 >= 0.25) & (c8 <= 0.75) & (c32 <= 0.5)
        rows = []
        for i in np.argsort(-s, kind="stable"):
            r = dict(draw=int(idx[i]), **AN.world_row(d, i, t, g, s))
            r["screen_score"] = float(p_score[pos1[int(idx[i])]])
            rows.append(r)
        res["cert"] = dict(
            src="cert/chunk_*.npz", sizes=st["arms"]["cert"]["sizes"], n=len(idx),
            gates={k: frac(v) for k, v in g.items()}, types={CR.TYPES[i]: int((t == i).sum()) for i in range(len(CR.TYPES))},
            gliders_like_closure=dict(rule="c(1) >= 0.95, 0.25 <= c(8) <= 0.75, c(32) <= 0.5", **frac(like),
                                      draws=[int(i) for i in idx[like]]),
            quantiles={k: q(d[k]) for k in ("nb_mean", "rg", "v_net", "body_speed_len", "events100", "ceil1", "ceil4", "ceil8",
                                            "ceil16", "ceil32", "v_orc8", "gap_max", "pl8", "twin_doubling", "wavelength",
                                            "body_frac")},
            pl8_over_v_orc8_q=q(d["pl8"] / np.maximum(d["v_orc8"], 1e-12)),
            worlds=rows)
    # ---------------- shortlist: candidates of job 1 that pass every gate at certification size and at late time
    if "cert" in res and "late" in res:
        mc, ml = load_arm(D, "cert", st), load_arm(D, "late", st)
        dc, tc, gc, sc_ = typed(mc, st["arms"]["cert"]["sizes"]["T"])
        dl, tl, gl, sl = typed(ml, st["arms"]["late"]["sizes"]["T"])
        il = {int(v): i for i, v in enumerate(ml["index"])}
        like = set(res["cert"]["gliders_like_closure"]["draws"])
        rows = []
        for i, dr in enumerate(mc["index"].astype(int)):
            if int(dr) not in il:
                continue
            j = il[int(dr)]
            if gc["candidate"][i] and gl["candidate"][j]:
                rows.append(dict(draw=int(dr), gliders_like_closure=int(dr) in like,
                                 cert={k: float(dc[k][i]) for k in ("ceil1", "ceil4", "ceil8", "ceil16", "ceil32", "v_orc8",
                                                                    "nb_mean", "rg", "v_net", "events100", "pl8", "gap_max",
                                                                    "twin_doubling", "body_speed_len")},
                                 late={k: float(dl[k][j]) for k in ("ceil1", "ceil4", "ceil8", "ceil16", "ceil32", "v_orc8",
                                                                    "nb_mean", "rg", "v_net", "events100", "pl8", "gap_max",
                                                                    "twin_doubling", "body_speed_len")}))
        rows.sort(key=lambda r: r["late"]["ceil8"])
        c1, c8, c32 = dl["ceil1"], dl["ceil8"], dl["ceil32"]
        lk = (c1 >= 0.95) & (c8 >= 0.25) & (c8 <= 0.75) & (c32 <= 0.5) & gl["candidate"]
        res["shortlist"] = dict(
            src="cert/chunk_*.npz and late/chunk_*.npz", rule="candidate at the screen (job 1), at certification size and at ticks 2000-2240",
            n=len(rows), of=int(len(mc["index"])), n_gliders_like=int(sum(r["gliders_like_closure"] for r in rows)),
            gliders_like=[r["draw"] for r in rows if r["gliders_like_closure"]], worlds=rows,
            late_arm=dict(n=int(len(tl)), candidates=int(gl["candidate"].sum()), movers=int((tl == 7).sum()),
                          active=int((tl >= 5).sum()),
                          candidates_with_gliders_like_closure=[int(v) for v in ml["index"].astype(int)[lk]]))
    with open(os.path.join(a.out, "analysis_r2.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    print("arms", {k: (v.get("n_done"), v.get("n_planned")) for k, v in res["arms_run"].items()})
    for k in ("enrich", "late", "sigma010", "sigma100", "cert", "shortlist"):
        if k in res:
            print(k, json.dumps({kk: vv for kk, vv in res[k].items() if kk not in ("worlds", "top_enriched", "transitions",
                                                                                   "prediction_from_job1", "arms")},
                                default=float)[:700])
    print("wrote", os.path.join(a.out, "analysis_r2.json"))


if __name__ == "__main__":
    main()
