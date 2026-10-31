"""Zero-noise sham at dt 0.5 and dt 0.25 from the PM suite's prepared state: deterministic dt error of the
readouts relative to the suite's native member spread on the sham case (independent_native + band + truths)."""
import sys, json
sys.path.insert(0, "/home/user/evalwork/pm_cips_eval/scripts")
from common import PC, E, LW, OUT
import numpy as np
from pathlib import Path
spec = PC.pm_spec(0.01, 0.5, 0.25)
D = Path(OUT) / "pm_noise"
res = {}
runs = {}
for dt in (0.5, 0.25):
    w = PC.replace(spec.world, noise={f: (k, 0.0) for f, (k, _) in spec.world.noise.items()}, noise_corr={},
                   overrides={**spec.world.overrides, "dt": dt}, steps_per_tick=int(round(1 / dt)), native_dt=dt)
    o = LW.oracle(w, spec.state, spec.devices)
    runs[dt] = E.cached(D / f"det_sham_dt{dt:g}.npz", lambda: o.sample_truth([], E.queries(), 1, truth_seed=3),
                        meta=dict(request=dict(id="sham", actions=[], queries=E.queries()), members=1, seed=3, dt=dt))
S = Path(OUT) / "suite_pm"
def load(p):
    with np.load(p) as z:
        return [z[f"query{i}"] for i in range(3)]
nat = [np.concatenate([x[q] for x in (load(S / "controls/c001/independent_native.npz"), load(S / "controls/c001/band_native.npz"), load(S / "truth/c001.npz"))]) for q in range(3)]
ti = [E.TIMES.index(t) for t in E.SCORE_TIMES]
for q, s in enumerate(E.SENSORS):
    sd = nat[q][:, ti].std(axis=0, ddof=1)
    d = runs[0.5][q][0][ti] - runs[0.25][q][0][ti]
    for p, f in enumerate(PC.PM_FIELDS):
        for slot in (range(d.shape[-1]) if s != "global" else (0, 1)):
            pass
        if s == "global":
            for slot, lab in ((0, "mean"), (1, "var")):
                res[f"{s}/{f}/{lab}"] = round(float(np.sqrt((d[:, p, slot] ** 2).mean() / (sd[:, p, slot] ** 2).mean())), 2)
        else:
            res[f"{s}/{f}"] = round(float(np.sqrt((d[:, p] ** 2).mean() / (sd[:, p] ** 2).mean())), 2)
json.dump(res, open(D / "det_sham_error_over_spread.json", "w"), indent=1)
print(res)
