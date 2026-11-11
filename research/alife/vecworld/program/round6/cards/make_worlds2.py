"""make_worlds2 -- the declared list of the second job (written after the first job's membrane and vortex cards
were seen on the CPU at small size, before any result of the second job).

Why: round 5 studied the membrane world on a clock of 40 time units (4 world ticks, `bias2`), and the division
cycle is about 1,850 time units; the card's horizons of 1 to 32 world ticks (10 to 320 time units) end before
anything a cell does. The same holds for selection among the fed vortices (5 time units per world tick). The
second job repeats those cards on slower clocks, so that the card says how its entries depend on the tick.

It also adds the gliders world with the 1- and 8-parameter hidden sets of round 5's ladder. With the 4-parameter
card of the first job that gives sigma_hat in six cells (block view, population x 1, 4, 8 hidden parameters) whose
science share round 5 measured: a retrodiction test of hypothesis H1 (rank order), declared before these runs.

After the Mac's review of the first job (review.md on origin/gpu-jobs:jobs/r6-cards-001), and before any card was
read: run A of gliders, vortex64 and membrane again with the corrected response-difference estimator (item 2: it
cannot be recomputed from the first job's cards); two true diffusion controls with gam = 0 as in round 5 (item 5);
the 128-px vortex world with 8-px blocks, so that its block view compares with the 64-px one (item 6).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = ["A", "B", "late"]
W = [dict(name="membrane_s4", kind="membrane", stride=4, role="designed", runs=ALL, priority=1),
     dict(name="vortex64_s4", kind="vortex", H=64, stride=4, role="designed", runs=ALL, priority=1),
     dict(name="gliders_n1", kind="gliders", n_hidden=1, role="designed", runs=["A", "B"], priority=1),
     dict(name="gliders_n8", kind="gliders", n_hidden=8, role="designed", runs=["A", "B"], priority=1),
     # after the Mac's review of the first job (written before any card of either job was read):
     dict(name="gliders", kind="gliders", role="designed", runs=["A"], priority=1),      # unbiased response difference
     dict(name="vortex64", kind="vortex", H=64, role="designed", runs=["A"], priority=1),
     dict(name="membrane", kind="membrane", role="designed", runs=["A"], priority=1),
     dict(name="ctl_puredif_0", kind="puredif", draw=0, H=64, role="control", runs=["A"], priority=1),
     dict(name="ctl_puredif_1", kind="puredif", draw=1, H=64, role="control", runs=["A"], priority=1),
     dict(name="vortex128g16", kind="vortex", H=128, G=16, role="size", runs=["A"], priority=3)]
out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, prior_seed=2026, run_seeds={"A": 6001, "B": 6002, "late": 6001}, worlds=W)
json.dump(out, open(os.path.join(HERE, "worlds2.json"), "w"), indent=1)
print(len(W), "worlds;", sum(len(w["runs"]) for w in W), "runs")
