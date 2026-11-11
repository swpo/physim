"""make_worlds -- the declared list of worlds of the card study (written once, before the GPU run).

Foundry draws are public functions of (prior seed 2026, index): pilots, never exam instances. The choice uses
round 5's screen (round5/foundry/results/per_draw.json.gz): the shortlist of seven, 16 of the other 81 screen
candidates drawn at random (numpy default_rng(606)), the first 32 prior indices as an unselected sample, and among
those the first 4 that round 5 typed uniform and the first 4 it typed frozen as negative controls.
Runs: A = run seed 6001, B = run seed 6002 (seed robustness), late = seed 6001 after late_gap more ticks.
"""
import gzip
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(gzip.open(os.path.join(HERE, "..", "..", "round5", "foundry", "results", "per_draw.json.gz")))
typ = np.array(d["type"])
cand = np.flatnonzero(np.array(d["candidate"]))
SHORT = [4470, 4186, 262, 7567, 6845, 1672, 3078]
assert all(s in cand for s in SHORT) and len(cand) == 88
rest = np.array([c for c in cand if c not in SHORT])
samp = sorted(int(x) for x in np.random.default_rng(606).choice(rest, size=16, replace=False))
prior = list(range(32))
uni = [i for i in prior if typ[i] == 2][:4]
fro = [i for i in prior if typ[i] == 3][:4]
W = []
ALL = ["A", "B", "late"]
W.append(dict(name="gliders", kind="gliders", role="designed", runs=ALL, priority=1))
W.append(dict(name="vortex64", kind="vortex", H=64, role="designed", runs=ALL, priority=1))
W.append(dict(name="membrane", kind="membrane", role="designed", runs=ALL, priority=1))
for i in SHORT:
    W.append(dict(name=f"foundry_{i:05d}", kind="foundry", draw=i, H=64, role="shortlist", runs=ALL, priority=1,
                  r5_type=d["types"][typ[i]]))
W.append(dict(name="ctl_noise", kind="noise", role="control", runs=["A", "B"], priority=1))
W.append(dict(name="ctl_freebodies", kind="free", role="control", runs=ALL, priority=1))
for i in uni:
    W.append(dict(name=f"ctl_uniform_{i:05d}", kind="foundry", draw=i, H=64, role="control", runs=ALL, priority=1,
                  r5_type=d["types"][typ[i]]))
for i in fro:
    W.append(dict(name=f"ctl_frozen_{i:05d}", kind="foundry", draw=i, H=64, role="control", runs=ALL, priority=1,
                  r5_type=d["types"][typ[i]]))
for j in range(2):
    W.append(dict(name=f"ctl_diffusion_{j}", kind="diffusion", draw=j, H=64, role="control", runs=["A"], priority=1))
for i in samp:
    W.append(dict(name=f"foundry_{i:05d}", kind="foundry", draw=i, H=64, role="candidate", runs=["A", "late"], priority=2,
                  r5_type=d["types"][typ[i]]))
for i in prior:
    if i in uni or i in fro:
        continue
    W.append(dict(name=f"foundry_{i:05d}", kind="foundry", draw=i, H=64, role="prior", runs=["A"], priority=3,
                  r5_type=d["types"][typ[i]]))
for i in SHORT:
    W.append(dict(name=f"foundry128_{i:05d}", kind="foundry", draw=i, H=128, role="size", runs=["A"], priority=4,
                  r5_type=d["types"][typ[i]]))
W.append(dict(name="vortex128", kind="vortex", H=128, role="size", runs=["A"], priority=5))
out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, prior_seed=2026, run_seeds={"A": 6001, "B": 6002, "late": 6001},
           shortlist=SHORT, candidates_sampled=samp, prior_sample=prior, uniform_controls=uni, frozen_controls=fro,
           worlds=W)
json.dump(out, open(os.path.join(HERE, "worlds.json"), "w"), indent=1)
print(len(W), "worlds;", sum(len(w["runs"]) for w in W), "runs; sampled candidates", samp, "uniform", uni, "frozen", fro)
