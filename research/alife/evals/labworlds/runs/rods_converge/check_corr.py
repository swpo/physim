"""Checks for labworld's correlated noise (noise_corr).

1. Default identity: with no noise_corr, the edited labworld.py gives byte-identical runner output to the version at
   HEAD 637f4cb (saved as labworld_before.py), on the rods world with all three noise forms and a pulse program.
2. Draw count: after a step, the member generator's state is the same with and without correlation.
3. Statistics of the smoothed noise (many draws): per-point variance (target 1 per unit sd sqrt(h)), zero net mass for
   the conserved form, covariance at r = 1, 2, 4 world units against exp(-r^2/(4 ell^2)) (additive), and the same
   covariances at dx = 1 and dx = 2/3 (continuum limit), for additive and conserved.
"""
import copy, importlib.util, json, sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("physim.labworld_before", HERE / "labworld_before.py")
OLD = importlib.util.module_from_spec(spec)
OLD.__package__ = "physim"
sys.modules["physim.labworld_before"] = OLD
spec.loader.exec_module(OLD)

sys.path.insert(0, str(HERE))
import rc  # noqa: E402

res = {}
s, info = rc.prepared()
devs = rc.devices(info)
prog = [{"t": 1.0, "kind": "inject", "device": 1, "port": 0, "amp": 2.0, "dur": 1.0}] + rc.PROGRAMS["surf"]
outs = []
for mod in (OLD, LW):
    w = mod.LabWorld(path=rc.W, fields=rc.FIELDS, steps_per_tick=1, native_dt=0.05,
                     ports={f: mod.Port(gain=g) for f, g in rc.GAINS.items()},
                     noise={f: (rc.NOISE_FORM[f], 0.0 if f == "om" else 0.01) for f in rc.FIELDS},
                     dx=1.0, sys_path=(rc.LAB,), carry=())
    o = mod.oracle(w, s, copy.deepcopy(devs))
    outs.append(o.sample_truth(prog, rc.q(rc.GROUPS, [1.0, 3.0, 6.0]), 2, truth_seed=5)["samples"])
res["default_identical_bytes"] = all(a.tobytes() == b.tobytes() for a, b in zip(*outs))
res["members_differ"] = bool(not np.array_equal(outs[1][0][0], outs[1][0][1]))
res["declaration_without_noise_corr_unchanged"] = (
    json.dumps(LW.LabWorld(path="x", fields=("a",), steps_per_tick=1, native_dt=1.0).declaration(), sort_keys=True)
    == json.dumps(OLD.LabWorld(path="x", fields=("a",), steps_per_tick=1, native_dt=1.0).declaration(), sort_keys=True))

# 2. draw count: rng state after one tick, white vs correlated
st = []
for corr in ({}, {f: 2.0 for f in rc.FIELDS}):
    w = rc.world(noise_corr=corr)
    stp = LW.LabStepper(w, dict(w.aux(s), _grid=(128, 128)))
    sim = LW.template(w, s, seed=9)
    stp(sim, 2)
    st.append(sim["rng"].bit_generator.state["state"]["state"])
res["rng_state_equal_after_2_ticks"] = st[0] == st[1]


# 3. statistics
def stats(kind, dx, ell, n=128, reps=400, seed=0):
    w = LW.LabWorld(path=rc.W, fields=("a",), steps_per_tick=1, native_dt=1.0, dx=dx, noise_corr={"a": ell})
    stp = LW.LabStepper.__new__(LW.LabStepper)
    stp.world, stp._filters = w, {}
    rng = np.random.default_rng(seed)
    var, mass, cov = [], [], {r: [] for r in (1.0, 2.0, 4.0)}
    for _ in range(reps):
        if kind == "conserved":
            ey, ex = rng.standard_normal((2, n, n))
            x = stp._smooth((ey - np.roll(ey, 1, 0)) + (ex - np.roll(ex, 1, 1)), ell, conserved=True)
        else:
            x = stp._smooth(rng.standard_normal((n, n)), ell)
        var.append(x.var())
        mass.append(abs(x.sum()))
        for r in cov:
            k = r / dx
            if abs(k - round(k)) < 1e-9:
                k = int(round(k))
                cov[r].append(0.5 * ((x * np.roll(x, k, 0)).mean() + (x * np.roll(x, k, 1)).mean()))
    out = dict(var=round(float(np.mean(var)), 4), max_abs_sum=float(np.max(mass)),
               cov={r: round(float(np.mean(v)), 4) for r, v in cov.items() if v})
    if kind == "additive":
        out["cov_expected"] = {r: round(float(np.exp(-r * r / (4 * ell * ell))), 4) for r in out["cov"]}
    return out


res["stats"] = {f"{kind} dx={dx:.3g} n={n} ell=2": stats(kind, dx, 2.0, n)
                for kind in ("additive", "conserved") for dx, n in ((1.0, 128), (0.5, 256))}
print(json.dumps(res, indent=1))
(HERE / "out" / "check_corr.json").write_text(json.dumps(res, indent=1))
