"""make_worlds2 -- the declared list of the second job (written after the first job's membrane and vortex cards
were seen on the CPU at small size, before any result of the second job).

Why: round 5 studied the membrane world on a clock of 40 time units (4 world ticks, `bias2`), and the division
cycle is about 1,850 time units; the card's horizons of 1 to 32 world ticks (10 to 320 time units) end before
anything a cell does. The same holds for selection among the fed vortices (5 time units per world tick). The
second job repeats those cards on slower clocks, so that the card says how its entries depend on the tick.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = ["A", "B", "late"]
W = [dict(name="membrane_s4", kind="membrane", stride=4, role="designed", runs=ALL, priority=1),
     dict(name="vortex64_s4", kind="vortex", H=64, stride=4, role="designed", runs=ALL, priority=1),
     dict(name="gliders_s4", kind="gliders", stride=4, role="designed", runs=["A"], priority=2)]
out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, prior_seed=2026, run_seeds={"A": 6001, "B": 6002, "late": 6001}, worlds=W)
json.dump(out, open(os.path.join(HERE, "worlds2.json"), "w"), indent=1)
print(len(W), "worlds;", sum(len(w["runs"]) for w in W), "runs")
