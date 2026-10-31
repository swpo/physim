"""Independent recheck of labeval outputs: bitwise re-run of one truth and one forecast member,
re-scoring from cached ensembles, override checks, and the band's early-window ratios."""
import json, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import labeval as E

SUITE = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/suite")
out = SUITE / "pm"
spec = E.phase_membrane()
suite = json.loads((out / "suite.json").read_text())
groups, rost = suite["groups"], E.roster(spec)

def load(p):
    with np.load(p, allow_pickle=False) as z:
        return [z[f"query{i}"] for i in range(3)], json.loads(str(z["meta"])) if "meta" in z.files else None

# 0. the frozen suite recomputed from code + calibration cache equals suite.json groups/scales
progs = E.build_programs(spec)
cal, plan = E.calibrate(spec, out, progs)       # cached, no simulation
sc = E.frozen_scales(spec, cal)
print("scales identical to suite.json:", sc == suite["calibration"]["scales"])
print("groups identical:", E._jsonable(E.score_groups(spec, sc)) == groups)

# 1. bitwise re-run of truth c001 (2 members) and member 0 of independent_native c006
native = E.make_oracle(spec, "native")
case1 = suite["cases"][0]["request"]
t0 = time.process_time()
tr = native.sample_truth(case1["actions"], case1["queries"], 2, truth_seed=E.TRUTH_SEED + 0)["samples"]
cached_tr, meta = load(out / "truth" / "c001.npz")
print(f"truth c001 rerun cpu {time.process_time()-t0:.1f}s; bitwise equal:",
      all(np.array_equal(a, b) for a, b in zip(tr, cached_tr)), "meta seed", meta["seed"])
case6 = suite["cases"][5]["request"]
t0 = time.process_time()
m0 = native.sample_truth(case6["actions"], case6["queries"], 1, truth_seed=E.FORECAST_SEED + 5)["samples"]
cached_n6, meta6 = load(out / "controls" / "c006" / "independent_native.npz")
print(f"native c006 member0 rerun cpu {time.process_time()-t0:.1f}s; equal to cached member 0:",
      all(np.array_equal(a[:1], b[:1]) for a, b in zip(m0, cached_n6)), "meta", meta6["seed"], meta6["variant"])

# 2. re-score c006 from cached arrays and compare to scores.json
S = json.loads((out / "controls" / "c006" / "scores.json").read_text())
truth6, _ = load(out / "truth" / "c006.npz")
for name in ["independent_native", "numerical_null", "ablate_chi0", "wrong_probe_geometry"]:
    pred, _ = load(out / "controls" / "c006" / f"{name}.npz")
    r = E.scoring.score_case(case6, {"samples": pred}, {"samples": truth6}, groups=groups,
                             n_samples=8, n_truth=2, roster=rost)
    print(f"  c006 {name:>22}: rescored {r['joint_energy_equal_group_mean']:.6f} vs json {S[name]['joint_energy_equal_group_mean']:.6f}")
band6, _ = load(out / "band" / "c006.npz")
nat6, _ = load(out / "controls" / "c006" / "independent_native.npz")
pooled = [np.concatenate([a, b]) for a, b in zip(nat6, band6)]
rb = E.scoring.score_case(case6, {"samples": band6}, {"samples": truth6}, groups=groups, n_samples=8, n_truth=2, roster=rost)
rp = E.scoring.score_case(case6, {"samples": pooled}, {"samples": truth6}, groups=groups, n_samples=16, n_truth=2, roster=rost)
print(f"  c006 band(8) {rb['joint_energy_equal_group_mean']:.4f}; mean of two 8-member scores "
      f"{0.5*(rb['joint_energy_equal_group_mean']+S['independent_native']['joint_energy_equal_group_mean']):.4f}; "
      f"true pooled 16-member ensemble {rp['joint_energy_equal_group_mean']:.4f}")

# 3. bimodality at device1 in c006: per-member mean device1 phi at t=50 (query1, last time, port 3)
null6, _ = load(out / "controls" / "c006" / "numerical_null.npz")
f = lambda a: np.round(a[1][:, -1, 3, :].mean(axis=1), 3)
print("  c006 device1 phi mean t=50  truth", f(truth6), "\n   native", f(nat6), "\n   band  ", f(band6), "\n   null  ", f(null6))

# 4. overrides really reach the stepper
for v in ("chi0", "gate0", "a2", "numerical_null"):
    o = E.make_oracle(spec, v)
    P = o._stepper.module.P
    print(f"  pm {v}: chi {P['chi']} gate {P['gate']} gateK {P['gateK']} a {P['a']} dt {P['dt']} "
          f"steps/tick {o._stepper.world.steps_per_tick} h {o._stepper.world.native_dt}")
fv = E.fed_vortices()
prep_par = fv.state.get("par")
for v in ("native", "adv0", "kF0", "numerical_null"):
    o = E.make_oracle(fv, v)
    par = o._stepper.aux_template["par"]
    diff = {k: (prep_par.get(k), par[k]) for k in par if prep_par is not None and prep_par.get(k) != par[k]}
    print(f"  fv {v}: adv {par['adv']} kF {par['kF']} dt {par['dt']} t {o._stepper.aux_template['t']} "
          f"steps/tick {o._stepper.world.steps_per_tick}; par differs from prepared: {diff}")
print("total cpu", round(time.process_time(), 1))
