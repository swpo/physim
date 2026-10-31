"""Existing declarations are bit-identical after the noise_intensity change.

Old = labworld.py at 77a6d83 (saved as labworld_before.py, imported as physim.labworld_before);
new = the working tree. Cases on phase_membrane's prepared state (runner_demo.py devices), 30 ticks,
3 members, pulses on several ports of both devices plus a probe move:
  A white noise in all three forms (S conserved, K additive, L proportional, phi additive), sd 0.02
  B variance-matched correlation (noise_corr) on S, L and phi (ell 1.5, 2, 3), weaker levels (stable)
  C runner_demo.py's declaration (physical form, sd 0.01)
  D fed vortices as vortex_demo.py (om additive, Y proportional, 0.003; carry t; roster om+, om-, Y+)
Compared: every sample array byte for byte, the per-member generator state after the run, declaration().
Also: the frozen labeval suites' declarations equal declaration() of the same specs under the new code;
the intensity form at dx = 1 with no ell equals the white form bit for bit (all three kinds);
the intensity form with ell differs from the variance-matched form.
"""
import hashlib, importlib.util, json, pickle, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
import physim  # noqa: E402
from physim import labworld as NEW  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("physim.labworld_before", HERE.parent / "labworld_before.py")
OLD = importlib.util.module_from_spec(spec)
OLD.__package__ = "physim"
sys.modules["physim.labworld_before"] = OLD
spec.loader.exec_module(OLD)

EP = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot")
PM = "/home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py"
FV = "/home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py"
LAB = "/home/user/physim/research/alife"


def dev(i, c):
    lattice, ds, rot, k = (("square", 3.0, 0.3, 13), ("hex", 6.0, 1.1, 19))[i]
    return ProbeDevice(dev_id=i, lattice=lattice, n_rings=3, base_ds=ds, center=np.asarray(c, float) + 0.5, L=128.0,
                       secret_rot=rot, reflect=False, motion_theta=0.0, motion_reflect=False, node_perm=np.arange(k))


def pm_case(LW, noise, corr=None, intensity=()):
    z = np.load(EP / "out" / "prep_s0.npz")
    info = json.loads((EP / "out" / "prep_s0.json").read_text())
    s = {f: z[f].astype(np.float64) for f in ("S", "K", "L", "phi")}
    kw = dict(path=PM, fields=("S", "K", "L", "phi"), steps_per_tick=1, native_dt=1.0,
              ports={f: LW.Port(gain=0.01, clip=(0.0, None)) for f in ("S", "K", "L", "phi")}, noise=noise, dx=1.0)
    if corr is not None:
        kw["noise_corr"] = corr
    if intensity:
        kw["noise_intensity"] = intensity
    w = LW.LabWorld(**kw)
    return w, s, [dev(0, info["sites"]["centre"]), dev(1, info["sites"]["other"])]


def fv_case(LW):
    with open(EP / "out" / "vortex_prep.pkl", "rb") as fh:
        s = pickle.load(fh)
    info = json.loads((EP / "out" / "vortex_prep.json").read_text())
    w = LW.LabWorld(path=FV, fields=("om", "Y"), steps_per_tick=1, native_dt=0.02,
                    ports={"om": LW.Port(gain=0.01), "Y": LW.Port(gain=0.1, clip=(0.0, None))},
                    noise={"om": ("additive", 0.003), "Y": ("proportional", 0.003)}, dx=1.0, sys_path=(LAB,),
                    carry=("t",), actuators=(LW.Actuator("om", 1), LW.Actuator("om", -1), LW.Actuator("Y", 1)))
    return w, s, [dev(0, info["centre"]), dev(1, info["other"])]


ACT = [dict(t=0.0, kind="inject", device=0, port=1, amp=3.0, dur=0.3),
       dict(t=0.1, kind="inject", device=1, port=0, amp=2.0, dur=0.2),
       dict(t=0.2, kind="adjust", device=0, u=[1, 0, 0]),
       dict(t=0.3, kind="inject", device=0, port=2, amp=1.5, dur=0.2)]
Q = [dict(sensor=s, t=[0.0, 0.1, 0.3, 0.6]) for s in ("device0", "device1", "global")]


def run(LW, case, *a, **k):
    w, s, d = case(LW, *a, **k)
    o = LW.oracle(w, s, d)
    m = o._stepper.module
    if hasattr(m, "ops") and hasattr(m.ops, "WORKERS"):
        m.ops.WORKERS = 1
    out = o.sample_truth(ACT, Q, 3, truth_seed=77)["samples"]
    h = hashlib.sha256(b"".join(np.ascontiguousarray(x).tobytes() for x in out)).hexdigest()[:16]
    return h, out, w


def main():
    white = {"S": ("conserved", 0.02), "K": ("additive", 0.02), "L": ("proportional", 0.02), "phi": ("additive", 0.02)}
    phys = {"phi": ("additive", 0.01), "S": ("proportional", 0.01), "K": ("proportional", 0.01), "L": ("proportional", 0.01)}
    corr = {"S": 1.5, "L": 2.0, "phi": 3.0}
    weak = {"S": ("conserved", 0.002), "K": ("additive", 0.005), "L": ("proportional", 0.02), "phi": ("additive", 0.005)}
    res = {}
    for name, case, a, k in (("A_white_all_forms", pm_case, (white,), {}),
                             ("B_variance_matched_corr", pm_case, (weak, corr), {}),
                             ("C_runner_demo", pm_case, (phys,), {}),
                             ("D_fed_vortices_signed", fv_case, (), {})):
        ho, oo, wo = run(OLD, case, *a, **k)
        hn, on, wn = run(NEW, case, *a, **k)
        spread = float(max(np.abs(x[0] - x[1]).max() for x in on))
        res[name] = dict(old=ho, new=hn, identical=ho == hn and all(np.array_equal(x, y) for x, y in zip(oo, on)),
                         declaration_equal=wo.declaration() == wn.declaration(), member_spread=spread)
        print(name, res[name], flush=True)
    # generator state after a step: a direct stepper call, old vs new
    for LW, tag in ((OLD, "old"), (NEW, "new")):
        w, s, d = pm_case(LW, weak, corr)
        st = LW.LabStepper(w, dict(w.aux(s), _grid=s["S"].shape))
        sim = dict(F=w.pack(s), t_step=0, rng=np.random.default_rng(5))
        st(sim, 3, [dict(field=1, y=40.0, x=40.0, amp=3.0)])
        res[f"rng_after_3_ticks_{tag}"] = int(sim["rng"].integers(0, 2**62))
    res["rng_equal"] = res["rng_after_3_ticks_old"] == res["rng_after_3_ticks_new"]
    # frozen labeval suite declarations
    sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
    import labeval as LE
    for tag, fn in (("pm", LE.phase_membrane), ("fv", LE.fed_vortices)):
        frozen = json.loads((EP / "suite" / tag / "suite.json").read_text())["declaration"]
        res[f"suite_{tag}_declaration_unchanged"] = LE._jsonable(fn().world.declaration()) == frozen
    # intensity form at dx 1 without ell = white form, bit for bit
    hw, _, _ = run(NEW, pm_case, white)
    hi, _, wi = run(NEW, pm_case, white, None, ("S", "K", "L", "phi"))
    res["intensity_white_dx1_equals_white"] = hw == hi
    res["intensity_declaration"] = wi.declaration()["noise_intensity"]
    hc, _, _ = run(NEW, pm_case, weak, corr)
    hci, _, _ = run(NEW, pm_case, weak, corr, ("S", "K", "L", "phi"))
    res["intensity_corr_differs_from_variance_matched"] = hc != hci
    # validation
    bad = []
    for kw in (dict(noise_intensity=("X",)), dict(noise_intensity=("K", "K")), dict(noise_intensity="K")):
        try:
            pm_case(NEW, {"K": ("additive", 0.01)}, None, **{"intensity": kw["noise_intensity"]})
            bad.append(f"accepted {kw}")
        except ValueError as e:
            bad.append(f"ValueError: {e}")
    res["validation"] = bad
    print(json.dumps({k: v for k, v in res.items() if not k.startswith(("A_", "B_", "C_", "D_"))}, indent=1))
    (HERE.parent / "out" / "ident.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
