"""Re-draw member 0 of the cached independent_native ensembles with the labworld.py now on the branch
(commit 42a8c72, LabOracleRunner) and compare bit for bit with the ensembles made at ec321ea."""
import json, subprocess, sys, time
sys.argv = sys.argv[:1]
import numpy as np
import cips as C
sp = C.spec()
out = C.OUT / "suite"
suite = json.loads((out / "suite.json").read_text())
rev = subprocess.run(["git", "-C", "/home/user/swpo/residency-environments", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(["git", "-C", "/home/user/swpo/residency-environments", "status", "--short"], capture_output=True, text=True).stdout.strip()
o = C.E.make_oracle(sp, "native")
res = dict(head=rev, dirty=dirty, runner=type(o).__name__)
t0 = time.process_time()
for i, case in enumerate(suite["cases"]):
    new = o.sample_truth(case["actions"], case["queries"], 1, truth_seed=C.FORECAST_SEED + i)["samples"]
    old = C.load(out / "controls" / case["id"] / "independent_native.npz")
    res[case["id"]] = max(float(np.abs(n[0] - c[0]).max()) for n, c in zip(new, old))
res["cpu_s"] = round(time.process_time() - t0, 1)
(C.OUT / "recheck.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res))
