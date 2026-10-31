"""c40's CIPS cells (layered dividing condensates) through PhySim's OracleRunner via physim.labworld.

World: /home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py
Fields e (enzyme), p (product), F (fuel), s (amphiphile); native dt 0.1; dx 1; periodic square box.

Subcommands (OMP_NUM_THREADS=1, labkit FFT workers 1, one heavy process at a time):

  prep      prepared state from a divcheck snapshot (decl.json: N, t_prep), device sites, picture
  parity    zero noise, no actions: runner readouts and fields vs the native module run
  noise     LEVEL...: one member per level for 50 tu from the prepared state (body counts, ranges)
  envelope  amp 3 for 50 tu at device0 into each port at several gains (finite? ranges? bodies?)
  score     calibration, truths, controls (predictors) for sham and one fuel pulse, score_case
  table     per-window / per-sensor tables from the cached ensembles
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import copy
import dataclasses
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
from physim import labworld as LW  # noqa: E402
from physim import blobround6_eval as scoring  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402
import labeval as E  # noqa: E402  (read-only reuse: make_oracle, calibrate, frozen_scales, cached, roster)

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
LAB = "/home/user/physim/research/alife"
WORLD = f"{LAB}/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
FIELDS = ("e", "p", "F", "s")
CLIPS = {"e": (0.0, 1.0), "p": (0.0, 1.0), "F": (0.0, None), "s": (0.0, None)}
DECL = HERE / "decl.json"
ST = np.ones((3, 3))


def decl():
    return json.loads(DECL.read_text())


def one_worker(module):
    if hasattr(module, "ops") and hasattr(module.ops, "WORKERS"):
        module.ops.WORKERS = 1


def world(gains=None, noise=None, overrides=None, spt=None, native_dt=0.1):
    d = decl()
    gains = d["gains"] if gains is None else gains
    noise = d["noise"] if noise is None else noise
    spt = d["steps_per_tick"] if spt is None else spt
    ports = {f: LW.Port(gain=float(gains[f]), clip=CLIPS[f]) for f in FIELDS}
    nz = {f: ("proportional", float(noise)) for f in FIELDS}
    return LW.LabWorld(path=WORLD, fields=FIELDS, steps_per_tick=int(spt), native_dt=native_dt, ports=ports,
                       noise=nz, overrides=overrides or {}, dx=1.0, sys_path=(LAB,), carry=("t",))


def prepared():
    with np.load(OUT / "prep.npz") as z:
        st = {f: z[f].astype(np.float64) for f in FIELDS}
        st["t"] = float(z["t"])
    return st, json.loads((OUT / "prep.json").read_text())


def device(i, centre, N):
    lattice, ds, rot, k = (("square", 3.0, 0.3, 13), ("hex", 6.0, 1.1, 19))[i]
    return ProbeDevice(dev_id=i, lattice=lattice, n_rings=3, base_ds=ds, center=np.asarray(centre, float) + 0.5,
                       L=float(N), secret_rot=rot, reflect=False, motion_theta=0.0, motion_reflect=False,
                       node_perm=np.arange(k))


def devices(info):
    return [device(0, info["sites"]["device0"], info["N"]), device(1, info["sites"]["device1"], info["N"])]


def native_module(overrides=None):
    m = LW.LabWorld(path=WORLD, fields=FIELDS, steps_per_tick=1, native_dt=0.1, overrides=overrides or {},
                    sys_path=(LAB,)).load()
    one_worker(m)
    return m


def native_state(m, st, N):
    """The module's own state at the prepared fields (operators from its init, clock carried)."""
    s = m.init(0, (N, N))
    for f in FIELDS:
        s[f] = st[f].copy()
    s["t"] = st["t"]
    return s


sys.path.insert(0, str(HERE))
from plabel import plabel  # noqa: E402


def components(e):
    """Periodic 8-connected bodies e > 0.5 (area >= 6 px): labels, count, areas."""
    lab, j = plabel(e > 0.5)
    return lab, j, [int((lab == i).sum()) for i in range(1, j + 1)]


def periodic_centre(mask, N):
    """Centre of mass of a mask on a periodic box (circular mean per axis)."""
    yy, xx = np.nonzero(mask)
    out = []
    for c in (yy, xx):
        a = 2 * np.pi * c / N
        out.append(float((np.arctan2(np.sin(a).mean(), np.cos(a).mean()) / (2 * np.pi) * N) % N))
    return out


# ----------------------------------------------------------------------------- prep

def cmd_prep(args):
    d = decl()
    N, tp = d["N"], d["t_prep"]
    with np.load(OUT / f"div{N}_s{d['seed']}_snaps.npz") as z:
        arr = z[f"t{tp}"]
    st = {f: arr[i].astype(np.float64) for i, f in enumerate(FIELDS)}
    st["t"] = float(tp)
    lab, n, areas = components(st["e"])
    sites = {}
    # device0: the body named in decl (pixel near it), device1: another body named in decl
    for key in ("device0", "device1"):
        y, x = d["site_hint"][key]
        j = lab[int(y) % N, int(x) % N]
        if j == 0:   # nearest body
            dist = ndimage.distance_transform_edt(lab == 0, return_indices=True)[1]
            j = lab[dist[0][int(y), int(x)], dist[1][int(y), int(x)]]
        sites[key] = [round(v, 2) for v in periodic_centre(lab == j, N)]
    info = dict(N=N, seed=d["seed"], t_prep=tp, bodies=n, areas=areas, sites=sites,
                ranges={f: [float(st[f].min()), float(st[f].max())] for f in FIELDS},
                source=f"out/div{N}_s{d['seed']}_snaps.npz:t{tp}")
    np.savez_compressed(OUT / "prep.npz", t=st["t"], **{f: st[f] for f in FIELDS})
    (OUT / "prep.json").write_text(json.dumps(info, indent=1))
    info["nodes"] = {f"device{i}": (dv.node_positions() - 0.5).round(3).tolist() for i, dv in enumerate(devices(info))}
    (OUT / "prep.json").write_text(json.dumps(info, indent=1))
    print(json.dumps({k: v for k, v in info.items() if k != "nodes"}))


# ----------------------------------------------------------------------------- direct stepper runs

def run_stepper(w, st, ticks, chunk, injections=(), seed=0, track=True):
    """Drive LabStepper directly (as OracleRunner does) and record bodies/ranges every chunk ticks."""
    step = LW.LabStepper(w, dict(w.aux(st), _grid=st["e"].shape))
    one_worker(step.module)
    sim = LW.template(w, st, seed)
    rec = []
    done = 0
    while done < ticks:
        n = min(chunk, ticks - done)
        step(sim, n, injections=list(injections))
        done += n
        F = sim["F"]
        row = dict(tu=round(done * 0.02, 4), finite=bool(np.isfinite(F).all()),
                   ranges={f: [float(np.nanmin(F[i])), float(np.nanmax(F[i]))] for i, f in enumerate(FIELDS)})
        if track and row["finite"]:
            row["bodies"], row["areas"] = components(F[0])[1:]
        rec.append(row)
        if not row["finite"]:
            break
    return sim, rec


def cmd_parity(args):
    """Zero noise, no actions: (a) LabStepper fields vs the native loop over 50 tu, (b) sample_truth readouts
    (2 members) vs the native fields read through the same devices and the global sensor."""
    d = decl()
    st, info = prepared()
    N, spt = info["N"], d["steps_per_tick"]
    devs = devices(info)
    times = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
    t0 = time.process_time()
    m = native_module()
    s = native_state(m, st, N)
    nat = {}
    tick = 0
    for t in times:
        target = int(round(t / 0.02))
        for _ in range((target - tick) * spt):
            s = m.step(s)
        tick = target
        nat[t] = np.stack([s[f] for f in FIELDS])
    cpu_native = time.process_time() - t0
    # snapshot consistency: the divcheck run continued 100 t past t_prep
    snapfile = OUT / f"div{N}_s{d['seed']}_snaps.npz"
    snap_diff = None
    with np.load(snapfile) as z:
        key = f"t{int(d['t_prep']) + 100}"
        if key in z.files:
            m2 = native_module()
            s2 = native_state(m2, st, N)
            for _ in range(1000):
                s2 = m2.step(s2)
            snap_diff = float(np.abs(np.stack([s2[f] for f in FIELDS]) - z[key]).max())
    w0 = world(noise=0.0)
    q = [dict(sensor=x, t=times) for x in ("device0", "device1", "global")]
    o = LW.oracle(w0, st, devs)
    one_worker(o._stepper.module)
    t1 = time.process_time()
    out = o.sample_truth([], q, 2, truth_seed=7)["samples"]
    cpu_runner = time.process_time() - t1
    diffs = {}
    for qi, sensor in enumerate(("device0", "device1", "global")):
        ref = []
        for t in times:
            Fn = nat[t]
            if sensor == "global":
                ref.append(np.stack((Fn.mean(axis=(1, 2)), Fn.var(axis=(1, 2))), axis=1))
            else:
                ref.append(devs[qi].sample(Fn, 1.0))
        ref = np.stack(ref)
        diffs[sensor] = dict(max_abs_member0=float(np.abs(out[qi][0] - ref).max()),
                             max_abs_member1=float(np.abs(out[qi][1] - ref).max()),
                             members_identical=bool(np.array_equal(out[qi][0], out[qi][1])))
    # full-field parity through the stepper the runner uses
    sim, _ = run_stepper(w0, st, 2500, 2500, track=False)
    field_diff = float(np.abs(sim["F"] - nat[50]).max())
    res = dict(steps_per_tick=spt, native_steps=2500 * spt, field_max_abs_50tu=field_diff,
               readouts=diffs, snapshot_t_prep_plus_100_max_abs=snap_diff,
               cpu_native_50tu_s=round(cpu_native, 1), cpu_runner_2members_s=round(cpu_runner, 1))
    (OUT / "parity.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


def cmd_noise(args):
    """Noise 0 and each level (two members, seeds 11 and 12) for 50 tu from the prepared state."""
    st, info = prepared()
    res = {}
    base = None
    for lvl in [0.0] + list(args.levels):
        finals = []
        for seed in ((11,) if lvl == 0 else (11, 12)):
            t0 = time.process_time()
            sim, rec = run_stepper(world(noise=lvl), st, 2500, 50, seed=seed)
            key = f"{lvl:g}/seed{seed}"
            res[key] = dict(cpu_s=round(time.process_time() - t0, 1), final_bodies=rec[-1].get("bodies"),
                            bodies_by_tu=[(r["tu"], r.get("bodies")) for r in rec],
                            ranges_final=rec[-1]["ranges"],
                            max_e=max(r["ranges"]["e"][1] for r in rec),
                            min_all=min(min(r["ranges"][f][0] for f in FIELDS) for r in rec),
                            finite=all(r["finite"] for r in rec))
            F = sim["F"]
            if base is None:
                base = F.copy()
            else:
                res[key]["final_rms_diff_vs_noise0"] = {f: float(np.sqrt(((F[i] - base[i]) ** 2).mean())) for i, f in enumerate(FIELDS)}
            finals.append(F)
            np.save(OUT / f"noise_{lvl:g}_seed{seed}_final.npy", F.astype(np.float32))
            print(key, json.dumps({k: v for k, v in res[key].items() if k != "bodies_by_tu"}), flush=True)
        if len(finals) == 2:
            res[f"{lvl:g}/member_rms_diff"] = {f: float(np.sqrt(((finals[0][i] - finals[1][i]) ** 2).mean())) for i, f in enumerate(FIELDS)}
    (OUT / "noise.json").write_text(json.dumps(res, indent=1))


def cmd_envelope(args):
    """amp 3 for 50 tu at device0's centre into each port; gains from --gains (per decade)."""
    st, info = prepared()
    dv = devices(info)[0]
    y, x = map(float, dv.center)
    _, sham = run_stepper(world(noise=0.0), st, 2500, 250)
    rows = [dict(port="none", gain=0.0, finite=True, final_bodies=sham[-1]["bodies"], ranges=sham[-1]["ranges"])]
    for pi, f in enumerate(FIELDS):
        for g in args.gains:
            gains = {k: 0.0 for k in FIELDS}
            gains[f] = g
            t0 = time.process_time()
            inj = [dict(field=pi, y=y, x=x, amp=3.0)]
            sim, rec = run_stepper(world(gains=gains, noise=0.0), st, 2500, 250, injections=inj)
            fin = all(r["finite"] for r in rec)
            row = dict(port=f, gain=g, finite=fin, final_bodies=rec[-1].get("bodies"),
                       max_over_run={k: max(r["ranges"][k][1] for r in rec) for k in FIELDS},
                       min_over_run={k: min(r["ranges"][k][0] for r in rec) for k in FIELDS},
                       centre_value_end=float(sim["F"][pi][int(y) % info["N"], int(x) % info["N"]]) if fin else None,
                       cpu_s=round(time.process_time() - t0, 1))
            rows.append(row)
            print(json.dumps(row), flush=True)
            np.save(OUT / f"envelope_{f}_g{g:g}.npy", sim["F"].astype(np.float32))
    (OUT / "envelope.json").write_text(json.dumps(rows, indent=1))


# ----------------------------------------------------------------------------- score

TIMES = E.TIMES
SCORE_TIMES = E.SCORE_TIMES
SENSORS = E.SENSORS
WINDOWS = (10, 25, 50)
N_TRUTH = 8
CAL_SEED, TRUTH_SEED, FORECAST_SEED, BAND_SEED = E.CAL_SEED, E.TRUTH_SEED, E.FORECAST_SEED, E.BAND_SEED


def spec():
    d = decl()
    st, info = prepared()
    null_dt = 0.05
    return E.LabSpec(
        name="cips_layered_divide", world=world(), state=st, devices=devices(info), main_port=2,
        ablations={"kF0": {"kF": 0.0}, "d0": {"d": 0.0}, "chi0": {"chi": 0.0}, "chis0": {"chi_s": 0.0}},
        null={"overrides": {"dt": null_dt}, "steps_per_tick": 2 * d["steps_per_tick"], "native_dt": null_dt},
        hook=one_worker,
        provenance=dict(prepared=str(OUT / "prep.npz"), prep_info=info, prepared_file_sha256=E.file_sha(OUT / "prep.npz"),
                        decl=d))


def programs(sp):
    q = E.queries()
    fuel = dict(t=5, kind="inject", device=0, port=2, amp=3.0, dur=10.0)
    return [dict(id="sham", actions=[], queries=q), dict(id="pulse_d0_F", actions=[fuel], queries=q)]


def window_groups(sp, scales, W):
    groups = []
    ti = {t: TIMES.index(t) for t in SCORE_TIMES if t <= W}
    slots = [int(dv.k) for dv in sp.devices]
    for qi, sensor in enumerate(SENSORS):
        for p, f in enumerate(sp.world.fields):
            if sensor == "global":
                sel, sc = [], []
                for slot, label in ((0, "mean"), (1, "variance")):
                    s = scales[f"{sensor}/{f}/{label}"]["scale"]
                    for t in ti:
                        sel.append(dict(query=qi, time_index=ti[t], port=p, slot=slot)); sc.append(s)
            else:
                s = scales[f"{sensor}/{f}"]["scale"]
                sel = [dict(query=qi, time_index=ti[t], port=p, slot=k) for t in ti for k in range(slots[qi])]
                sc = [s] * len(sel)
            groups.append(dict(id=f"{sensor}/{f}", selectors=sel, scales=sc, unit=f"{f} / frozen scale"))
    return groups


CONTROLS = ["independent_native", "ignore_actions", "wrong_probe_geometry", "initial_persistence",
            "ablate_kF0", "ablate_d0", "ablate_chi0", "ablate_chis0", "numerical_null"]


def cmd_score(args):
    sp = spec()
    out = OUT / "suite"
    out.mkdir(parents=True, exist_ok=True)
    cpu0 = time.process_time()
    progs = programs(sp)
    cal, cal_plan = E.calibrate(sp, out, progs)
    scales = E.frozen_scales(sp, cal)
    cases = [dict(p, id=f"c{i + 1:03d}") for i, p in enumerate(progs)]
    decl_d = {k: getattr(sp.world, k) for k in ("path", "fields", "steps_per_tick", "native_dt", "ports", "noise",
                                                  "overrides", "dx", "sys_path", "carry")}
    decl_d["ports"] = {f: dataclasses.asdict(v) for f, v in decl_d["ports"].items()}
    suite = E._jsonable(dict(world=sp.name, declaration=decl_d, world_sha256=E.file_sha(WORLD),
                             prepared_state_sha256=E.digest_state(sp.state, FIELDS), provenance=sp.provenance,
                             ablations=sp.ablations, numerical_null=sp.null, calibration=dict(plan=cal_plan, scales=scales),
                             cases=cases, windows=WINDOWS, truth_members=N_TRUTH, members=args.members,
                             seeds=dict(cal=CAL_SEED, truth=TRUTH_SEED, forecast=FORECAST_SEED, band=BAND_SEED),
                             controls=CONTROLS))
    spth = out / "suite.json"
    if spth.exists():
        assert json.loads(spth.read_text()) == suite, "frozen suite changed"
    else:
        spth.write_text(json.dumps(suite, indent=1) + "\n")
    rost = E.roster(sp)
    oracles = {}

    def oracle(v):
        if v not in oracles:
            oracles[v] = E.make_oracle(sp, v)
        return oracles[v]

    native = oracle("native")
    init = native.sample_truth([], [dict(sensor=x, t=[0]) for x in SENSORS], 1, truth_seed=0)["samples"]
    persistence = scoring.PersistencePredictor(dict(zip(SENSORS, [a[0, 0] for a in init])), roster=rost)
    order = [c.strip() for c in args.order.split(",")]
    for i, case in enumerate(cases):
        cdir = out / "controls" / case["id"]
        cdir.mkdir(parents=True, exist_ok=True)
        print(case["id"], progs[i]["id"], flush=True)
        (out / "truth").mkdir(exist_ok=True)
        E.cached(out / "truth" / f"{case['id']}.npz",
                 lambda: native.sample_truth(case["actions"], case["queries"], N_TRUTH, truth_seed=TRUTH_SEED + i),
                 meta=dict(request=case, members=N_TRUTH, seed=TRUTH_SEED + i))
        for name in order:
            if name in ("ignore_actions", "initial_persistence"):
                continue
            if name == "band":
                E.cached(cdir / "band_native.npz", lambda: native.sample_truth(
                    case["actions"], case["queries"], args.members, truth_seed=BAND_SEED + i),
                    meta=dict(request=case, members=args.members, seed=BAND_SEED + i, variant="native"))
                continue
            v = {"independent_native": "native"}.get(name, name.removeprefix("ablate_"))
            o = oracle(v)
            E.cached(cdir / f"{name}.npz", lambda: o.sample_truth(
                case["actions"], case["queries"], args.members, truth_seed=FORECAST_SEED + i),
                meta=dict(request=case, members=args.members, seed=FORECAST_SEED + i, variant=v))
    with open(out / "cpu_log.jsonl", "a") as fh:
        fh.write(json.dumps(dict(cpu_s=time.process_time() - cpu0, time=time.strftime("%H:%M:%S"))) + "\n")
    np.savez(out / "persistence_init.npz", **{s: a[0, 0] for s, a in zip(SENSORS, init)})


def load(path):
    with np.load(path, allow_pickle=False) as z:
        meta = json.loads(str(z["meta"]))
        return [z[f"query{i}"] for i in range(len(meta["request"]["queries"]))]


def boot_scores(pred, truth, groups, idx):
    """Energy score per group from pairwise RMS distances (as blobround6_eval._energy_score), for the full
    truth set (idx None: returns [aggregate]) or for truth-member resamples idx (B, n): returns
    {'aggregate': (B,), sensor: (B,)}."""
    out = {}
    for gr in groups:
        sel = lambda arrays: np.column_stack([arrays[x["query"]][:, x["time_index"], x["port"], x["slot"]]
                                              for x in gr["selectors"]]) / np.asarray(gr["scales"])
        X, Y = sel(pred), sel(truth)
        d = X.shape[1]
        D = np.sqrt(((X[:, None, :] - Y[None, :, :]) ** 2).sum(-1) / d)
        S = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1) / d).mean()
        out[gr["id"]] = (D.mean() - 0.5 * S) if idx is None else (D[:, idx].mean(axis=(0, 2)) - 0.5 * S)
    if idx is None:
        return [float(np.mean(list(out.values())))]
    res = {"aggregate": np.mean([v for v in out.values()], axis=0)}
    for sname in SENSORS:
        res[sname] = np.mean([v for k, v in out.items() if k.startswith(sname + "/")], axis=0)
    return res


def cmd_table(args):
    sp = spec()
    out = OUT / "suite"
    suite = json.loads((out / "suite.json").read_text())
    scales = suite["calibration"]["scales"]
    rost = E.roster(sp)
    z = np.load(out / "persistence_init.npz")
    persistence = scoring.PersistencePredictor({s: z[s] for s in SENSORS}, roster=rost)
    res = {}
    for ci, case in enumerate(suite["cases"]):
        cid = case["id"]
        cdir = out / "controls" / cid
        truth = load(out / "truth" / f"{cid}.npz")
        preds = {}
        for name in CONTROLS + ["band_native"]:
            f = cdir / f"{name}.npz"
            if name == "ignore_actions":
                if case["actions"]:
                    preds[name] = load(out / "controls" / suite["cases"][0]["id"] / "independent_native.npz")
                continue
            if name == "initial_persistence":
                preds[name] = persistence.predict(case["actions"], case["queries"], n_samples=suite["members"])["samples"]
                continue
            if f.exists():
                preds[name] = load(f)
        rng = np.random.default_rng(2026 + ci)
        boot_idx = rng.integers(0, len(truth[0]), size=(400, len(truth[0])))
        for W in WINDOWS:
            groups = window_groups(sp, scales, W)
            boot = {}
            for name, pred in preds.items():
                r = scoring.score_case(case, {"samples": pred}, {"samples": truth}, groups=groups,
                                       n_samples=len(pred[0]), n_truth=len(truth[0]), roster=rost)
                g = {x["id"]: x["energy_score"] for x in r["joint_energy"]}
                res.setdefault(cid, {}).setdefault(f"{W}tu", {})[name] = dict(
                    aggregate=r["joint_energy_equal_group_mean"], groups=g,
                    sensors={s: float(np.mean([v for k, v in g.items() if k.startswith(s + "/")])) for s in SENSORS})
                boot[name] = boot_scores(pred, truth, groups, boot_idx)
                chk = float(np.mean([boot_scores(pred, truth, [gr], None)[0] for gr in groups]))
                assert abs(chk - r["joint_energy_equal_group_mean"]) <= 1e-9 * max(1.0, abs(chk)), (name, chk)
            ref = boot["independent_native"]
            for name, b in boot.items():
                if name == "independent_native":
                    continue
                entry = res[cid][f"{W}tu"][name]
                entry["ratio_ci90_truth_bootstrap"] = {
                    k: [float(np.quantile(b[k] / ref[k], 0.05)), float(np.quantile(b[k] / ref[k], 0.95))]
                    for k in ["aggregate"] + list(SENSORS)}
    (out / "scores.json").write_text(json.dumps(res, indent=1))
    lines = []
    for cid, per in res.items():
        fam = next(c["actions"] for c in suite["cases"] if c["id"] == cid)
        lines.append(f"\n### {cid} {'sham' if not fam else 'fuel pulse at device0 (amp 3, t=5, dur 10)'}\n")
        lines.append("Ratio to independent_native (score in its row); per window: aggregate | device0 | device1 | global\n")
        names = [n for n in CONTROLS + ["band_native"] if n in per["10tu"]]
        hdr = "| predictor | " + " | ".join(f"{W} tu agg | d0 | d1 | gl" for W in WINDOWS) + " |"
        lines += [hdr, "|---" * (1 + 4 * len(WINDOWS)) + "|"]
        for n in names:
            cells = []
            for W in WINDOWS:
                ref, r = per[f"{W}tu"]["independent_native"], per[f"{W}tu"][n]
                if n == "independent_native":
                    cells += [f"{r['aggregate']:.3g}"] + [f"{r['sensors'][s]:.3g}" for s in SENSORS]
                else:
                    ci = r.get("ratio_ci90_truth_bootstrap", {}).get("aggregate")
                    cells += [f"{r['aggregate'] / ref['aggregate']:.2f}" + (f" [{ci[0]:.2f}-{ci[1]:.2f}]" if ci else "")] + [f"{r['sensors'][s] / ref['sensors'][s]:.2f}" for s in SENSORS]
            lines.append(f"| {n} | " + " | ".join(cells) + " |")
    lines.append("\nPer (sensor, field) group at 50 tu: ratio to independent_native\n")
    for cid, per in res.items():
        g50 = per["50tu"]
        gids = list(g50["independent_native"]["groups"])
        lines += [f"\n{cid}\n", "| predictor | " + " | ".join(gids) + " |", "|---" * (len(gids) + 1) + "|"]
        lines.append("| independent_native (score) | " + " | ".join(f"{g50['independent_native']['groups'][g]:.3g}" for g in gids) + " |")
        for n, r in g50.items():
            if n == "independent_native":
                continue
            lines.append(f"| {n} | " + " | ".join(f"{r['groups'][g] / g50['independent_native']['groups'][g]:.2f}" for g in gids) + " |")
    (out / "table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "parity", "noise", "envelope", "score", "table"])
    ap.add_argument("--levels", type=float, nargs="*", default=[0.01, 0.03])
    ap.add_argument("--gains", type=float, nargs="*", default=[1.0, 0.1, 0.01])
    ap.add_argument("--members", type=int, default=8)
    ap.add_argument("--order", default="independent_native,ablate_kF0,ablate_d0,ablate_chi0,ablate_chis0,"
                                       "wrong_probe_geometry,numerical_null,band")
    a = ap.parse_args()
    dict(prep=cmd_prep, parity=cmd_parity, noise=cmd_noise, envelope=cmd_envelope, score=cmd_score,
         table=cmd_table)[a.cmd](a)
