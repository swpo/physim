"""End-to-end exam harness on A_gliders/objects (small: 6 items, prefix 8, horizon 16, 6 replicates).
References: persistence (built in) and a designer kinematic predictor (un-permutes the observation,
moves each slot by q * velocity on the torus, permutes back). Writes results/exam_demo.json."""
import json
import time

import numpy as np

import lenia_world as LW
import analyze as AN
vw = LW.vw

specs, parts = LW.make_specs("A_gliders")
K = parts["tracker"].K
w = vw.VectorWorld(specs["objects"], world_seed=11)
t0 = time.time()
ex = vw.Exam(w, n_items=6, prefix=8, horizon=16, queries=[1, 2, 4, 8, 16], rate=0.5, exam_seed=3)
t_build = time.time() - t0
inv_out = np.argsort(w.out_map)


def kin(item):
    y = item["past_obs"][-1][inv_out]          # back to designer coordinates
    return np.stack([AN.kinematic(y[None], q, K)[0][w.out_map] for q in item["query_times"]])


t0 = time.time()
sc = ex.score(n_rep=6, references={"designer_kinematic": kin})
res = {"build_seconds": t_build, "score_seconds": time.time() - t0, "queries": sc["queries"],
       "mse": sc["mse"], "mse_se": sc["mse_se"], "oracle": sc["oracle"], "skill_vs_oracle": sc["skill"],
       "public_item_keys": list(ex.public()[0].keys()),
       "prefix_inputs_per_item": [len(it["past_program"]) for it in ex.items],
       "test_inputs_per_item": [len(it["program"]) for it in ex.items]}
json.dump(vw.jsonable(res), open("results/exam_demo.json", "w"), indent=1)
print(json.dumps(vw.jsonable(res), indent=1))
