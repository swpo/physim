"""make_job2_inputs -- the index lists of job2.py (CPU, a second). Needs results/per_draw.json.gz (job 1) and
sel_r2.json (select_enriched.py). Writes job2_inputs.json.

  late    every active world of job 1 (type index >= 5), then 381 frozen and 381 uniform worlds drawn at random
          (numpy default_rng(0)), 2000 draws in all, prior seed 2026
  enrich  sel_r2.json's interleaved index (96 enriched + 32 control per 128), prior seed 2027
  sigma   draws 0..2047 of prior seed 2026
  cert    the candidates of job 1 by decreasing score, prior seed 2026
"""
import gzip
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
per = json.load(gzip.open(os.path.join(HERE, "results", "per_draw.json.gz"), "rt"))
draw, t, s, cand = np.array(per["draw"]), np.array(per["type"]), np.array(per["score"]), np.array(per["candidate"])
rng = np.random.default_rng(0)
act = draw[t >= 5]
fro = np.sort(rng.choice(draw[t == 3], 381, replace=False))
uni = np.sort(rng.choice(draw[t == 2], 381, replace=False))
sel = json.load(open(os.path.join(HERE, "sel_r2.json")))
ci = np.nonzero(cand)[0]
ci = ci[np.argsort(-s[ci], kind="stable")]
out = dict(
    late=dict(prior_seed=2026, index=[int(i) for i in np.concatenate([act, fro, uni])], n_active=int(len(act)),
              n_frozen=int(len(fro)), n_uniform=int(len(uni))),
    enrich=dict(prior_seed=sel["prior_seed"], index=sel["index"], n_enriched=len(sel["enriched"]),
                n_control=len(sel["control"]), source="sel_r2.json"),
    sigma=dict(prior_seed=2026, index=list(range(2048))),
    cert=dict(prior_seed=2026, index=[int(draw[i]) for i in ci]))
with open(os.path.join(HERE, "job2_inputs.json"), "w") as f:
    json.dump(out, f)
print({k: len(v["index"]) for k, v in out.items()})
