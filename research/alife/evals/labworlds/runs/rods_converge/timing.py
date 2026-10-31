"""CPU per native step through the runner (1 member, correlated noise on), at 128^2 and 192^2; and the module alone."""
import copy, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import rc

res = {}
for n in (128, 192):
    s, info = rc.prepared(n=n)
    w = rc.world(dt=0.05, n=n)
    m = w.load()
    st = copy.deepcopy(s)
    t0 = time.process_time()
    for _ in range(100):
        st = m.step(st)
    res[f"module_{n}_ms"] = round(10 * (time.process_time() - t0), 2)
    o, _ = rc.oracle(w, s, rc.devices(info))
    t0 = time.process_time()
    o.sample_truth([], rc.q(rc.GROUPS, [1.0, 2.0]), 1, truth_seed=1)
    res[f"runner_corr_{n}_ms"] = round(10 * (time.process_time() - t0), 2)
    o, _ = rc.oracle(rc.world(dt=0.05, n=n, noise_corr={}), s, rc.devices(info))
    t0 = time.process_time()
    o.sample_truth([], rc.q(rc.GROUPS, [1.0, 2.0]), 1, truth_seed=1)
    res[f"runner_white_{n}_ms"] = round(10 * (time.process_time() - t0), 2)
    print(json.dumps(res), flush=True)
(rc.OUT / "timing.json").write_text(json.dumps(res, indent=1))
