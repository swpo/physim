
import json, os, sys, types
sys.path.insert(0, "/tmp/bk032bundle")
os.chdir("/tmp/bk032bundle")
json.dump({"island": 9, "sim_backend": "gpu_batch", "out_dir": "/tmp/bk032out"},
          open("island_config.json", "w"))

import blobkit.assay_batch as ABM
calls = []
def fake_run(jobs, **kw):
    # record (n_lanes, L, nf_max_of_call, order_of_t0s)
    nfm = max(len(j["genome"]["acts"]) + len(j["genome"]["chans"]) for j in jobs)
    calls.append((len(jobs), kw.get("L", 128.0), nfm,
                  [j.get("t0") for j in jobs]))
    outs = []
    for j in jobs:
        outs.append(dict(interest=1.0, C={}, flags={},
                         horizon=dict(T_used=j.get("t0") or 2500.0,
                                      why_stopped="static", n_extensions=0,
                                      decisions=[], interest_trajectory=[]),
                         summary=dict(horizon={}),
                         D=dict(d5=dict(phase="frozen", winding_max=0,
                                        wind_com_speed=None),
                                d4=dict(moving_frac=0), d1={}, d7={}, d6={})))
    return outs
ABM.run_assay_batch = fake_run
import pod_worker_batch as PWB
PWB.run_assay_batch = fake_run

from blobkit import worlds
g_small = worlds.load("m0")        # nf 3  -> bucket 4
g_small2 = worlds.load("m4")       # nf 3  -> bucket 4
g_mid = worlds.load("mv3")         # nf 8  -> bucket 10
g_mid2 = worlds.load("ds3_017")    # nf 11 -> bucket 14
jobs = [
  dict(cand="a1", kind="screen", genome=dict(g_small), gen=1),
  dict(cand="a2", kind="seed2", seed=2, t0=10000.0, genome=dict(g_small2), gen=0),
  dict(cand="a3", kind="screen", genome=dict(g_mid), gen=1),
  dict(cand="a4", kind="screen", genome=dict(g_mid2), gen=1),
  dict(cand="a5", kind="seed2", seed=2, t0=5000.0, genome=dict(g_small), gen=0),
]
json.dump(jobs, open("/tmp/bk032jobs.json", "w"))
sys.argv = ["pod_worker_batch.py", "/tmp/bk032jobs.json"]
PWB.main()
print("CALLS (n, L, nf_max, t0-order):", calls)
# expect 3 calls: bucket4 (3 lanes, t0 desc 10000,5000,None), bucket10 (mv3), bucket14 (ds3_017)
assert len(calls) == 3, calls
b4 = [c for c in calls if c[0] == 3][0]
assert b4[2] <= 4 or b4[2] == 3          # nf_max of the small call stays small
assert b4[3] == [10000.0, 5000.0, None], b4[3]   # descending expected T
assert sorted(c[2] for c in calls) == [3, 8, 11], calls
rws = json.load(open("/tmp/bk032out/results.json"))
assert len(rws) == 5 and all(r["status"] == "ok" for r in rws)
print("NF-BUCKET GROUPING TEST PASS")
