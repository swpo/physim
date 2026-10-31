"""Deterministic size of the dt-halving offset vs the ensemble spread (noise 0, one member each).

For sham and the fuel pulse: native (dt 0.1, 1 step/tick) and null (dt 0.05, 2 steps/tick) at noise 0;
the offset RMS over nodes per (sensor, field, time) against the noise-0.01 spread of the cached
independent_native ensemble (std over its 8 members, RMS over nodes) at the same time.
"""
import json, sys, time
sys.argv = sys.argv[:1]
import numpy as np
import cips as C

sp = C.spec()
out = C.OUT / "suite"
suite = json.loads((out / "suite.json").read_text())
st, info = C.prepared()
res = {}
t0 = time.process_time()
for case in suite["cases"]:
    q = case["queries"]
    runs = {}
    for name, kw in (("native", {}), ("null", dict(overrides={"dt": 0.05}, spt=2, native_dt=0.05))):
        w = C.world(noise=0.0, **kw)
        o = C.LW.oracle(w, st, C.devices(info))
        C.one_worker(o._stepper.module)
        runs[name] = o.sample_truth(case["actions"], q, 1, truth_seed=5)["samples"]
    ens = C.load(out / "controls" / case["id"] / "independent_native.npz")
    rows = {}
    for qi, sensor in enumerate(C.SENSORS):
        for p, f in enumerate(C.FIELDS):
            off = np.sqrt(((runs["null"][qi][0, :, p, :] - runs["native"][qi][0, :, p, :]) ** 2).mean(axis=-1))
            spr = np.sqrt((ens[qi][:, :, p, :].std(axis=0) ** 2).mean(axis=-1))
            rows[f"{sensor}/{f}"] = dict(offset_over_spread=[round(float(a / max(b, 1e-300)), 2) for a, b in zip(off, spr)])
    res[case["id"]] = dict(times=q[0]["t"], groups=rows)
res["cpu_s"] = round(time.process_time() - t0, 1)
(C.OUT / "nulldiff.json").write_text(json.dumps(res, indent=1))
for cid in ("c001", "c002"):
    print(cid, "times", res[cid]["times"])
    for g, r in res[cid]["groups"].items():
        print(f"  {g:12s}", r["offset_over_spread"])
print("cpu", res["cpu_s"])
