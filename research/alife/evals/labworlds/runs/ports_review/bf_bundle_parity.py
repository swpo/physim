"""Reviewer re-run: LabOracleRunner.wrap vs OracleRunner on the offline BF bundle (make_oracle on its
prepared state), suite case c002 with the bundle builder's truth seed, compared to the stored truth."""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(v, "1")
import json, sys, time, resource
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
sys.path.insert(0, "/home/user/physim/generators/physim")
import numpy as np
import physim
from physim import blobround6 as R6, labworld as LW
import eval_preparation as EP

B = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/b_dece87"
OUT = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/ports_review"
res = dict(physim=physim.__file__, R6=R6.__file__, EP=EP.__file__)
suite = json.load(open(f"{B}/suite.json"))
idx = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rec = suite["cases"][idx]
case = rec["request"]
z = np.load(f"{B}/truth/{case['id']}.npz", allow_pickle=False)
assert json.loads(str(z["request"])) == case
truth = [z[f"query{i}"] for i in range(len(case["queries"]))]
base = EP.make_oracle(B)
lab = LW.LabOracleRunner.wrap(base)
res["case"] = case["id"]; res["truth_seed"] = 71000 + idx
res["perm"] = base._perm.tolist(); res["lab_actuators"] = [list(a) for a in lab._actuators]
out = {}
for name, r in (("OracleRunner", base), ("LabOracleRunner.wrap", lab)):
    t0 = time.process_time()
    out[name] = r.sample_truth(case["actions"], case["queries"], 2, truth_seed=71000 + idx)["samples"]
    res[f"cpu_{name}"] = round(time.process_time() - t0, 1)
same = lambda a, b: all(x.shape == y.shape and x.dtype == y.dtype and x.tobytes() == y.tobytes() for x, y in zip(a, b))
res["lab_vs_base_bitwise"] = same(out["OracleRunner"], out["LabOracleRunner.wrap"])
for name in out:
    res[f"{name}_vs_stored_truth_bitwise"] = same(out[name], truth)
    res[f"{name}_vs_stored_truth_maxabs"] = float(max(np.abs(a - b).max() for a, b in zip(out[name], truth)))
# static: default roster when an observe-only row is not last in the private permutation (no stepping)
w = LW.LabOracleRunner.wrap(base, observe_only=[2])
res["default_roster_with_observe_only_row2"] = dict(perm=w._perm.tolist(), actuators=[list(a) for a in w._actuators],
    observed_port_rows=w._perm.tolist())
print(json.dumps(res, indent=1))
json.dump(res, open(f"{OUT}/bf_bundle_parity.json", "w"), indent=1)
