"""Item 3 pilots: zero-noise single members of each program (native) and of the matching ablations on chosen
programs, with readouts at the suite's 15 times and full fields at 0/10/20/30/40/50 tu (float16, for pictures).

  pilot.py pm|cips [variant:program ...]   (default: every program native + the planned ablation pairs)
"""
import json, sys, time, dataclasses
from pathlib import Path
sys.path.insert(0, "/home/user/evalwork/pm_cips_eval/scripts")
from common import PC, E, LW, EVALPILOT, OUT
import numpy as np

world_name = sys.argv[1]
D = Path(OUT) / "pilot" / world_name
D.mkdir(parents=True, exist_ok=True)
SNAP = [0, 10, 20, 30, 40, 50]


def pm_setup():
    st = PC.load_state(f"{EVALPILOT}/out/prep_s0.npz", PC.PM_FIELDS)
    info = json.load(open(f"{EVALPILOT}/out/prep_s0.json"))
    devs = [PC.device(0, info["sites"]["centre"], 128), PC.device(1, info["sites"]["other"], 128)]
    w = PC.pm_world(0.0, 0.5, ell=None, actuators=PC.PM_ACTUATORS)
    abl = {"a2": {"a": 2.0}, "chi0": {"chi": 0.0}, "feed10": {"F": 0.06}, "feed3": {"F": 0.02}, "DS2": {"DS": 0.4}}
    pairs = [("a2", p) for p in ("sham", "K_d0", "L_d0", "L_rim")] + [("chi0", p) for p in ("sham", "L_d0", "L_rim")] \
        + [("feed10", p) for p in ("sham", "Sm_d0", "Sm_d1", "Sp_d1")]
    return st, devs, w, abl, dict((p[0], p[1]) for p in PC.pm_programs()), pairs


CIPS_SITES = {"device0": [20.2, 153.8], "device1": [16.1, 101.8]}


def cips_setup():
    st = PC.load_state(f"{OUT}/cips_prep/prep_s5_t3100.npz", PC.CIPS_FIELDS)
    devs = [PC.device(0, CIPS_SITES["device0"], 192), PC.device(1, CIPS_SITES["device1"], 192)]
    w = PC.cips_world(0.0, ell=None, gains={"p": 0.3, "F": 0.3, "s": 1.0}, actuators=PC.CIPS_ACTUATORS)
    abl = {"chi0": {"chi": 0.0}, "kF0": {"kF": 0.0}, "chis0": {"chi_s": 0.0}, "d0": {"d": 0.0}, "DF10": {"DF": 20.0}}
    pairs = [("chi0", p) for p in ("sham", "p_d0", "p_d1")] + [("kF0", p) for p in ("sham", "Fp_d0")] \
        + [("chis0", p) for p in ("sham", "s_d0")] + [("d0", p) for p in ("sham",)] + [("DF10", p) for p in ("sham", "Fm_d0", "Fm_d1")]
    return st, devs, w, abl, dict((p[0], p[1]) for p in PC.cips_programs()), pairs


st, devs, w, abl, progs, pairs = (pm_setup if world_name == "pm" else cips_setup)()
todo = [a.split(":") for a in sys.argv[2:]] or ([("native", p) for p in progs] + pairs)
for variant, prog in todo:
    path = D / f"{variant}__{prog}.npz"
    if path.exists():
        continue
    wv = w if variant == "native" else PC.replace(w, overrides={**w.overrides, **abl[variant]})
    o = LW.oracle(wv, st, devs)
    PC.one_worker(o._stepper.module)
    snaps = {}
    orig = o._fill_queries

    def fill(live, devices, marks, output, member, _orig=orig):
        t = round(live["t_step"] * 0.02, 6)
        if t in SNAP:
            snaps[f"F_{int(t)}"] = np.asarray(live["F"], dtype=np.float16)
            snaps[f"c0_{int(t)}"] = np.asarray(devices[0].center); snaps[f"c1_{int(t)}"] = np.asarray(devices[1].center)
        return _orig(live, devices, marks, output, member)
    o._fill_queries = fill
    q = [dict(sensor=s, t=sorted(set(E.TIMES) | set(SNAP))) for s in E.SENSORS]
    t0 = time.process_time()
    res = o.sample_truth(progs[prog], q, 1, truth_seed=1)["samples"]
    cpu = time.process_time() - t0
    F = np.stack([np.asarray(r) for r in res[:2]]) if False else None
    np.savez_compressed(path, cpu_s=cpu, times=np.array(q[0]["t"]), d0=res[0][0], d1=res[1][0], gl=res[2][0],
                        **snaps)
    fin = all(np.isfinite(r).all() for r in res)
    rng_ = {f: [float(res[2][0][:, i, 0].min()), float(res[2][0][:, i, 0].max())] for i, f in enumerate(w.fields)}
    print(f"{variant}:{prog} cpu {cpu:.1f}s finite {fin}", flush=True)
