import sys, time, json
sys.path.insert(0, "/home/user/evalwork/pm_cips_eval/scripts")
from common import PC, E, LW, EVALPILOT, OUT
import numpy as np
which = sys.argv[1]
res = {}
if which == "pm":
    st = PC.load_state(f"{EVALPILOT}/out/prep_s0.npz", PC.PM_FIELDS)
    info = json.load(open(f"{EVALPILOT}/out/prep_s0.json"))
    devs = [PC.device(0, info["sites"]["centre"], 128), PC.device(1, info["sites"]["other"], 128)]
    for dt in (1.0, 0.5, 0.25):
        o = LW.oracle(PC.pm_world(0.01, dt), st, devs)
        t0 = time.process_time()
        o.sample_truth([dict(t=0, kind="inject", device=0, port=1, amp=3.0, dur=10.0)], E.queries(), 1, truth_seed=1)
        res[f"pm_dt{dt}"] = time.process_time() - t0
        print(res, flush=True)
else:
    for path, name in ((PC.CIPS_PATH, "iso"), (PC.CIPS_ORIG, "orig")):
        w = PC.cips_world(0.01, path=path)
        m = PC.native_module(w)
        s = m.init(5, (192, 192))
        st = {f: s[f] for f in PC.CIPS_FIELDS}; st["t"] = 0.0
        devs = [PC.device(0, (20, 150), 192), PC.device(1, (16, 100), 192)]
        for ell in (2.0, None):
            o = LW.oracle(PC.replace(w, noise_corr={f: 2.0 for f in PC.CIPS_FIELDS} if ell else {}), st, devs)
            PC.one_worker(o._stepper.module)
            t0 = time.process_time()
            o.sample_truth([], [dict(sensor="global", t=[10])], 1, truth_seed=1)
            res[f"cips_{name}_ell{ell}_10tu"] = time.process_time() - t0
            print(res, flush=True)
json.dump(res, open(f"{OUT}/logs/timing_{which}.json", "w"), indent=1)
