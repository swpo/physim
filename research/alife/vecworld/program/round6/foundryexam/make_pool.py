"""make_pool -- the public pool of screened worlds of study foundryexam (CPU, seconds).

    python -B make_pool.py --enrich DIR      # DIR = a copy of origin/gpu-jobs:jobs/r5-foundry-002/out

Pool = the early candidates of round 5's foundry (all four gates of ../../round5/foundry/criteria.py at ticks
50-290): prior seed 2026 from results/per_draw.json.gz (job r5-foundry-001) and prior seed 2027 from the
enrichment arm of job r5-foundry-002 (recomputed here from its chunk files with criteria.py, as analyze2.py
does). Writes results/pool.json: per world (prior_seed, index, arm, a few screen measures), and the centres
of the neighbourhood arms chosen by the rule of DESIGN.md section 2 from results/wind_probe7.json.

PILOT ONLY: every theta is a public function of (prior_seed, index); never reuse as an exam.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
FOUNDRY = os.path.abspath(os.path.join(HERE, "..", "..", "round5", "foundry"))
sys.path.insert(0, FOUNDRY)
import criteria as CR  # noqa: E402

SHORTLIST = [4470, 4186, 262, 7567, 6845, 1672, 3078]
KEEP = ("cv_cell", "nb_mean", "body_frac", "v_net", "events100", "ceil1", "ceil8", "ceil32", "v_orc8", "gap_max", "pl8",
        "vp_main1", "vp_main16")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enrich", required=True)
    a = ap.parse_args()
    per = json.load(gzip.open(os.path.join(FOUNDRY, "results", "per_draw.json.gz"), "rt"))
    worlds = []
    cand = np.array(per["candidate"], bool)
    for i in np.flatnonzero(cand):
        worlds.append(dict(prior_seed=2026, index=int(per["draw"][i]), arm="screen2026",
                           **{k: float(per[k][i]) for k in KEEP if k in per}))
    st = json.load(open(os.path.join(a.enrich, "job2_state.json")))
    n_chunks = len(st["arms"]["enrich"]["chunks"])
    files = sorted(f for f in os.listdir(os.path.join(a.enrich, "enrich")) if f.startswith("chunk_"))[:n_chunks]
    parts = [dict(np.load(os.path.join(a.enrich, "enrich", f))) for f in files]
    skip = ("thumb_u8", "thumb_scale", "thumb_index")
    m = {k: np.concatenate([p[k] for p in parts]) for k in parts[0] if k not in skip}
    d = CR.derive(m, st["arms"]["enrich"]["sizes"]["T"])
    t = CR.classify(d)
    g = CR.gates(d, t)
    idx = m["index"].astype(int)
    sel = json.load(open(os.path.join(FOUNDRY, "sel_r2.json")))
    enr, ctl = set(sel["enriched"]), set(sel["control"])
    for i in np.flatnonzero(g["candidate"]):
        arm = "enriched2027" if int(idx[i]) in enr else ("control2027" if int(idx[i]) in ctl else "other2027")
        worlds.append(dict(prior_seed=2027, index=int(idx[i]), arm=arm, **{k: float(d[k][i]) for k in KEEP if k in d}))
    counts = {}
    for w in worlds:
        counts[w["arm"]] = counts.get(w["arm"], 0) + 1
    wp = json.load(open(os.path.join(HERE, "results", "wind_probe7.json")))
    rank = sorted(((x["draw"], x["programs"]["aimed_200"]["effect_over_noise"][2], x["programs"]["aimed_200"]["effect"][2])
                   for x in wp["worlds"]), key=lambda r: -r[1])
    assert sorted(r[0] for r in rank) == sorted(SHORTLIST)
    out = dict(PILOT_NEVER_REUSE_AS_EXAM=True,
               what="public pool of screened worlds (round-5 early candidates) and the centres of the neighbourhood arms",
               sources=dict(screen2026="round5/foundry/results/per_draw.json.gz (job r5-foundry-001), key candidate",
                            seed2027="origin/gpu-jobs:jobs/r5-foundry-002/out/enrich/chunk_*.npz through criteria.py; "
                                     "arms from round5/foundry/sel_r2.json"),
               counts=counts, worlds=worlds,
               centres=dict(rule="top 3 of the 7 shortlisted worlds by wind_probe aimed_200 effect_over_noise at 4 ticks",
                            prior_seed=2026, ranking=[dict(draw=int(r[0]), effect_over_noise_h4=float(r[1]),
                                                           effect_h4_variance_units=float(r[2])) for r in rank],
                            chosen=[int(r[0]) for r in rank[:3]], source="results/wind_probe7.json"))
    with open(os.path.join(HERE, "results", "pool.json"), "w") as f:
        json.dump(out, f, indent=0)
    print(counts, "centres", out["centres"]["chosen"])


if __name__ == "__main__":
    main()
