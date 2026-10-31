"""Item 2: acceptance of the CIPS-iso world through the runner (192^2, dt 0.1, 1 step per tick).

  parity     zero noise, no actions: native module loop vs LabStepper fields at 50 tu, and sample_truth readouts
             (2 members) vs the native fields read through the same devices and the global sensor
  envelope   zero noise, amp 3 for 50 tu at each device centre on each actuator (gains p 1, F 1, s 1)
  noise L..  2 members per intensity level (ell 2), sham, 50 tu: bodies, ranges, member spread at the probes
  det        zero-noise members at dt 0.1 and dt 0.05 on the p_d0 and Fm_d0 programs (deterministic dt error)
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, "/home/user/evalwork/pm_cips_eval/scripts")
from common import PC, E, LW, EVALPILOT, OUT
import numpy as np
sys.path.insert(0, "/home/user/physim/research/alife/evals/labworlds/runs/cips_runner")
from plabel import plabel

D = Path(OUT) / "cips_accept"; D.mkdir(parents=True, exist_ok=True)
SITES = {"device0": [20.2, 153.8], "device1": [16.1, 101.8]}
GAINS = {"p": 1.0, "F": 1.0, "s": 1.0}
N = 192
st = PC.load_state(f"{OUT}/cips_prep/prep_s5_t3100.npz", PC.CIPS_FIELDS)
devs = [PC.device(0, SITES["device0"], N), PC.device(1, SITES["device1"], N)]
progs = dict((p[0], p[1]) for p in PC.cips_programs())


def W(level=0.0, ell=PC.ELL, dt=0.1):
    return PC.cips_world(level, ell=ell if level > 0 else None, gains=GAINS, dt=dt, actuators=PC.CIPS_ACTUATORS)


def bodies(e):
    return int(plabel(e > 0.5)[1])


def run_member(w, actions, seed, track_every=None):
    """One member through LabOracleRunner (devices, scheduling as in the suite); fields every track_every tu."""
    o = LW.oracle(w, st, devs)
    PC.one_worker(o._stepper.module)
    rec = []
    orig = o._fill_queries

    def fill(live, devices, marks, output, member, _orig=orig):
        F = live["F"]
        rec.append(dict(tu=round(live["t_step"] * 0.02, 4), finite=bool(np.isfinite(F).all()), bodies=bodies(F[0]),
                        ranges={f: [float(F[i].min()), float(F[i].max())] for i, f in enumerate(PC.CIPS_FIELDS)}))
        return _orig(live, devices, marks, output, member)
    o._fill_queries = fill
    times = list(range(0, 51, track_every)) if track_every else E.TIMES
    q = [dict(sensor=s, t=times) for s in E.SENSORS]
    t0 = time.process_time()
    out = o.sample_truth(actions, q, 1, truth_seed=seed)["samples"]
    return out, rec, time.process_time() - t0


cmd = sys.argv[1]
if cmd == "parity":
    w0 = W()
    m = PC.native_module(w0)
    s = m.init(0, (N, N))
    for f in PC.CIPS_FIELDS:
        s[f] = st[f].copy()
    s["t"] = st["t"]
    nat, tick = {}, 0
    t0 = time.process_time()
    for t in E.TIMES:
        for _ in range(int(round(t / 0.02)) - tick):
            s = m.step(s)
        tick = int(round(t / 0.02))
        nat[t] = np.stack([s[f] for f in PC.CIPS_FIELDS])
    cpu_native = time.process_time() - t0
    o = LW.oracle(w0, st, devs)
    PC.one_worker(o._stepper.module)
    t1 = time.process_time()
    out = o.sample_truth([], E.queries(), 2, truth_seed=7)["samples"]
    cpu_runner = time.process_time() - t1
    diffs = {}
    for qi, sensor in enumerate(E.SENSORS):
        ref = np.stack([np.stack((nat[t].mean(axis=(1, 2)), nat[t].var(axis=(1, 2))), axis=1) if sensor == "global"
                        else devs[qi].sample(nat[t], 1.0) for t in E.TIMES])
        diffs[sensor] = dict(max_abs_member0=float(np.abs(out[qi][0] - ref).max()),
                             max_abs_member1=float(np.abs(out[qi][1] - ref).max()),
                             members_identical=bool(np.array_equal(out[qi][0], out[qi][1])))
    stp = LW.LabStepper(w0, dict(w0.aux(st), _grid=(N, N)))
    PC.one_worker(stp.module)
    sim = LW.template(w0, st, 0)
    stp(sim, 2500)
    res = dict(field_max_abs_50tu=float(np.abs(sim["F"] - nat[50]).max()), readouts=diffs,
               cpu_native_50tu_s=cpu_native, cpu_runner_2members_s=cpu_runner)
    PC.dump(D / "parity.json", res)
    print(json.dumps(res, indent=1))
elif cmd == "envelope":
    rows = []
    _, sham, cpu = run_member(W(), [], 0, track_every=5)
    rows.append(dict(program="sham", device=None, port=None, cpu_s=cpu, finite=all(r["finite"] for r in sham),
                     bodies=[r["bodies"] for r in sham],
                     max={f: max(r["ranges"][f][1] for r in sham) for f in PC.CIPS_FIELDS},
                     min={f: min(r["ranges"][f][0] for r in sham) for f in PC.CIPS_FIELDS}))
    print(json.dumps(rows[-1]), flush=True)
    for dev in (0, 1):
        for port, a in enumerate(PC.CIPS_ACTUATORS):
            acts = [dict(t=0.0, kind="inject", device=dev, port=port, amp=3.0, dur=50.0)]
            out, rec, cpu = run_member(W(), acts, 0, track_every=5)
            rows.append(dict(program=f"{a.field}{'+' if a.sign > 0 else '-'}_d{dev}_amp3_50tu", device=dev, port=port,
                             cpu_s=cpu, finite=all(r["finite"] for r in rec), bodies=[r["bodies"] for r in rec],
                             max={f: max(r["ranges"][f][1] for r in rec) for f in PC.CIPS_FIELDS},
                             min={f: min(r["ranges"][f][0] for r in rec) for f in PC.CIPS_FIELDS},
                             probe_centre_end={f: float(out[dev][0][-1, i, 0]) for i, f in enumerate(PC.CIPS_FIELDS)}))
            print(json.dumps(rows[-1]), flush=True)
    PC.dump(D / "envelope.json", rows)
elif cmd == "noise":
    res = {}
    for lv in map(float, sys.argv[2:]):
        outs = []
        for seed in (11, 12):
            out, rec, cpu = run_member(W(lv), [], seed, track_every=5)
            outs.append(out)
            res[f"{lv:g}/seed{seed}"] = dict(cpu_s=cpu, bodies=[r["bodies"] for r in rec],
                                             max={f: max(r["ranges"][f][1] for r in rec) for f in PC.CIPS_FIELDS},
                                             min={f: min(r["ranges"][f][0] for r in rec) for f in PC.CIPS_FIELDS})
            print(lv, seed, json.dumps(res[f"{lv:g}/seed{seed}"]), flush=True)
        np.savez_compressed(D / f"noise_{lv:g}.npz", **{f"m{k}_q{q}": outs[k][q] for k in range(2) for q in range(3)})
    old = json.loads((D / "noise.json").read_text()) if (D / "noise.json").exists() else {}
    old.update(res)
    PC.dump(D / "noise.json", old)
elif cmd == "det":
    for prog in sys.argv[2:]:
        for dt in (0.1, 0.05):
            o = LW.oracle(W(dt=dt), st, devs)
            PC.one_worker(o._stepper.module)
            path = D / f"det_{prog}_dt{dt:g}.npz"
            E.cached(path, lambda: o.sample_truth(progs[prog], E.queries(), 1, truth_seed=5),
                     meta=dict(request=dict(id=prog, actions=progs[prog], queries=E.queries()), members=1, seed=5, dt=dt))
elif cmd == "detg":
    # detg '{"p":0.3,"F":0.3}' PORT DEVICE : zero-noise amp 3 for 20 tu at DEVICE on PORT, dt 0.1 vs dt 0.05
    g = json.loads(sys.argv[2]); port, dev = int(sys.argv[3]), int(sys.argv[4])
    acts = [dict(t=0.0, kind="inject", device=dev, port=port, amp=3.0, dur=20.0)]
    tag = "_".join(f"{k}{v:g}" for k, v in sorted(g.items()))
    for dt in (0.1, 0.05):
        w = PC.cips_world(0.0, ell=None, gains={**GAINS, **g}, dt=dt, actuators=PC.CIPS_ACTUATORS)
        o = LW.oracle(w, st, devs)
        PC.one_worker(o._stepper.module)
        E.cached(D / f"detg_{tag}_port{port}_d{dev}_dt{dt:g}.npz", lambda: o.sample_truth(acts, E.queries(), 1, truth_seed=5),
                 meta=dict(request=dict(id="detg", actions=acts, queries=E.queries()), members=1, seed=5, dt=dt, gains=g))
