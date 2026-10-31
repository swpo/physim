"""c34's Marangoni rods through PhySim's own OracleRunner via physim.labworld (local prototype).

  timing     ms per native step through the runner (1 member, 2 tu, noise on)
  parity     zero noise, no actions: runner vs the native module, 50 tu, exact comparison
  envelope   amp 3 for 50 tu at device 0 into each driven port, gain ladder 1 / 0.1 / 0.01 / 0.001
  run        8-member ensembles for one program and a list of arms (saved per arm, resumable)
  score      energy scores of every control predictor against the native truths

World: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py at its defaults.
Prepared state: the battery's native seed-0 state at native t=300 (marangoni/out/prep_s0.npz),
19 rods; device 0 on the median rod's deepest pixel, device 1 on the largest other rod.
"""
import argparse, copy, json, sys, time
from pathlib import Path

import numpy as np
from numpy.fft import fft2, ifft2
from scipy import ndimage

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW  # noqa: E402
from physim.blobround6 import OracleRunner  # noqa: E402
from physim.blobround6_eval import _energy_score  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
W = "/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py"
LAB = "/home/user/physim/research/alife"
PREP = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/out")
FIELDS = ("phi", "q1", "q2", "s", "c", "om")   # om = 0.5 (dx vy - dy vx): the module's own output, observe-only
DRIVEN = ("phi", "q1", "q2", "s", "c")
NATIVE_DT = 0.05
SPT = 1                                         # native steps per public tick: 1 tu = 50 steps = 2.5 native t
NOISE_SD = 0.01                                 # per sqrt(native t)
NOISE_FORM = {"phi": "conserved", "q1": "additive", "q2": "additive", "s": "proportional",
              "c": "proportional", "om": "additive"}
GAINS = {"phi": 0.01, "q1": 0.01, "q2": 0.01, "s": 0.01, "c": 0.01}   # replaced by the envelope result
ARMS = {"native": {}, "mar0": {"mar": 0.0}, "passive": {"zeta": 0.0, "mar": 0.0}, "kappa0": {"kappa": 0.0},
        "chis0": {"chis": 0.0}, "dthalf": {"dt": NATIVE_DT / 2}}
PROGRAMS = {"sham": [],
            "cargo": [{"t": 5.0, "kind": "inject", "device": 0, "port": 4, "amp": 3.0, "dur": 10.0}],
            "surf": [{"t": 5.0, "kind": "inject", "device": 0, "port": 3, "amp": 3.0, "dur": 10.0}]}
TRUTH_SEED, PRED_SEED = 202, 101
TIMES = [float(t) for t in range(1, 51)]
GROUPS = ("device0", "device1", "global")


class RodsStepper(LW.LabStepper):
    """LabStepper plus a 'conserved' noise kind: f += sd sqrt(h) div(eta) / sd(div eta), eta a white vector
    field (two draws), spectral divergence on the module's own dealiased grid, no mass added at k = 0
    (the battery's normalisation: per-pixel sd equal to the additive form's). Draw count per step is fixed
    (2 for a conserved field, 1 otherwise) whatever the sd, so arms and programs stay noise-paired."""

    def _cons(self, state, ex, ey):
        kx, ky, da = state["kx"], state["ky"], state["da"]
        if not hasattr(self, "_csd"):
            self._csd = float(np.sqrt((state["k2"] * da).sum() / da.size))
        return ifft2(1j * (kx * fft2(ex) + ky * fft2(ey)) * da).real / self._csd

    def __call__(self, sim, n, injections=()):
        w = self.world
        if "_lab_aux" not in sim:
            sim["_lab_aux"] = copy.deepcopy(self.aux_template)
        state = dict(sim["_lab_aux"])
        F = np.array(sim["F"], dtype=np.float64, copy=True)
        for i, f in enumerate(w.fields):
            state[f] = F[i]
        rng = sim["rng"]
        h = w.native_dt
        for _ in range(n):
            for _ in range(w.steps_per_tick):
                for inj in injections:
                    f = w.fields[inj["field"]]
                    port = w.ports.get(f)
                    if port is None or inj["amp"] == 0.0:
                        continue
                    state[f] = state[f] + port.gain * inj["amp"] * h * self._bump(state[f].shape, inj["y"], inj["x"])
                    lo, hi = port.clip
                    if lo is not None or hi is not None:
                        state[f] = np.clip(state[f], lo, hi)
                for f in w.fields:
                    kind, sd = w.noise.get(f, ("additive", 0.0))
                    a = sd * np.sqrt(h)
                    if kind == "conserved":
                        ex = rng.standard_normal(state[f].shape)
                        ey = rng.standard_normal(state[f].shape)
                        if sd > 0:
                            state[f] = state[f] + a * self._cons(state, ex, ey)
                        continue
                    xi = rng.standard_normal(state[f].shape)
                    if sd > 0:
                        state[f] = state[f] + (a * xi if kind == "additive" else a * xi * state[f])
                state = self.module.step(state)
            sim["t_step"] += 1
        sim["F"] = w.pack(state)
        sim["_lab_aux"] = {k: v for k, v in state.items() if k not in w.fields}
        return sim


class OutOfRange(RuntimeError):
    pass


def nbodies(phi, min_area=6):
    lab, n = ndimage.label(phi > 0, structure=np.ones((3, 3)))
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):   # periodic merge
        for i, j in zip(a, b):
            if i and j and i != j:
                lab[lab == j] = i
    ids, areas = np.unique(lab[lab > 0], return_counts=True)
    return int((areas >= min_area).sum())


class Watch:
    """Wraps the stepper (the runner still drives it): per member, field extremes and body counts after every
    stepper call (every agenda tick: 1 tu here), final-state snapshots, and an optional range check."""

    def __init__(self, inner, bounds=None, snap_members=2):
        self.inner, self.bounds, self.snap_members = inner, bounds, snap_members
        self.members = []

    def __call__(self, sim, n, injections=()):
        if sim["t_step"] == 0:
            self.members.append(dict(ext={f: [np.inf, -np.inf] for f in FIELDS}, bodies=[], snap=None))
        rec = self.members[-1]
        sim = self.inner(sim, n, injections=injections)
        F = sim["F"]
        for i, f in enumerate(FIELDS):
            lo, hi = float(np.nanmin(F[i])), float(np.nanmax(F[i]))
            rec["ext"][f] = [min(rec["ext"][f][0], lo), max(rec["ext"][f][1], hi)]
            if not np.isfinite(F[i]).all():
                rec["fail"] = dict(t=sim["t_step"] * 0.02, field=f, why="non-finite")
                raise OutOfRange(json.dumps(rec["fail"]))
            if self.bounds and f in self.bounds:
                blo, bhi = self.bounds[f]
                if lo < blo or hi > bhi:
                    rec["fail"] = dict(t=round(sim["t_step"] * 0.02, 2), field=f, why="range", lo=lo, hi=hi)
                    raise OutOfRange(json.dumps(rec["fail"]))
        rec["bodies"].append((round(sim["t_step"] * 0.02, 2), nbodies(F[0])))
        if len(self.members) <= self.snap_members:
            rec["snap"] = np.array(F, dtype=np.float32)
        return sim


def world(gains=None, overrides=None, noise=NOISE_SD, spt=SPT, native_dt=NATIVE_DT):
    gains = GAINS if gains is None else gains
    ports = {f: LW.Port(gain=gains[f]) for f in DRIVEN if gains.get(f, 0.0) > 0}
    nz = {f: (NOISE_FORM[f], 0.0 if f == "om" else noise) for f in FIELDS}
    return LW.LabWorld(path=W, fields=FIELDS, steps_per_tick=spt, native_dt=native_dt, ports=ports, noise=nz,
                       overrides=overrides or {}, dx=1.0, sys_path=(LAB,), carry=())


def prepared():
    """The battery's prepared state plus om (the flow of that state: one native step on a copy)."""
    z = np.load(PREP / "prep_s0.npz")
    info = json.loads((PREP / "prep_s0.json").read_text())
    m = world().load()
    s = m.init(0, (128, 128))
    for f in ("phi", "q1", "q2", "s", "c"):
        s[f] = z[f].astype(np.float64).copy()
    s1 = m.step(copy.deepcopy(s))
    s["om"] = s1["om"].copy()
    return s, info


def devices(info, shift=(0.0, 0.0)):
    c0 = np.array(info["sites"]["centre"], float) + 0.5 + np.array(shift)
    c1 = np.array(info["sites"]["other"], float) + 0.5 + np.array(shift)
    d0 = ProbeDevice(dev_id=0, lattice="square", n_rings=3, base_ds=3.0, center=c0 % 128, L=128.0,
                     secret_rot=0.3, reflect=False, motion_theta=0.0, motion_reflect=False, node_perm=np.arange(13))
    d1 = ProbeDevice(dev_id=1, lattice="hex", n_rings=3, base_ds=6.0, center=c1 % 128, L=128.0,
                     secret_rot=1.1, reflect=False, motion_theta=0.0, motion_reflect=False, node_perm=np.arange(19))
    return [d0, d1]


def oracle(w, s, devs, bounds=None):
    stepper = RodsStepper(w, dict(w.aux(s), _grid=s["phi"].shape))
    watch = Watch(stepper, bounds)
    o = OracleRunner(_template=LW.template(w, s), _devices=devs, _port_perm=np.arange(len(FIELDS)),
                     _adjust_mix=np.eye(3), _stepper=watch)
    return o, watch


def arm_world(arm, gains, noise=NOISE_SD):
    if arm == "dthalf":
        return world(gains, ARMS[arm], noise, spt=2 * SPT, native_dt=NATIVE_DT / 2)
    return world(gains, ARMS[arm], noise)


def q(sensors, times):
    return [{"sensor": g, "t": times} for g in sensors]


def timing(args):
    s, info = prepared()
    o, _ = oracle(world(), s, devices(info))
    t0 = time.process_time(); w0 = time.time()
    o.sample_truth([], q(GROUPS, [1.0, 2.0]), 1, truth_seed=1)
    cpu = time.process_time() - t0
    out = dict(steps=100, cpu_s=round(cpu, 2), wall_s=round(time.time() - w0, 2), ms_per_step=round(10 * cpu, 2))
    print(json.dumps(out))
    (OUT / "timing.json").write_text(json.dumps(out, indent=1))


def parity(args):
    s, info = prepared()
    devs = devices(info)
    nt = int(round(args.tu / 0.02))
    w = world(noise=0.0)
    o, watch = oracle(w, s, devs)
    t0 = time.process_time()
    out = o.sample_truth([], q(GROUPS, [float(args.tu)]), args.members, truth_seed=7)["samples"]
    cpu_runner = time.process_time() - t0
    m = w.load()
    ref = copy.deepcopy(s)
    t0 = time.process_time()
    for _ in range(nt * SPT):
        ref = m.step(ref)
    cpu_native = time.process_time() - t0
    refF = np.stack([ref[f] for f in FIELDS])
    runF = [mem["snap"] for mem in watch.members]
    # the snapshot is float32; compare the exact float64 runner state through the global sensor and the probes
    gl = np.stack((refF.mean(axis=(1, 2)), refF.var(axis=(1, 2))), axis=1)
    d0 = devs[0].sample(refF, 1.0)
    d1 = devs[1].sample(refF, 1.0)
    res = dict(tu=args.tu, native_steps=nt * SPT, members=args.members,
               max_abs_global=[float(np.abs(out[2][k, 0] - gl).max()) for k in range(args.members)],
               max_abs_device0=[float(np.abs(out[0][k, 0] - d0).max()) for k in range(args.members)],
               max_abs_device1=[float(np.abs(out[1][k, 0] - d1).max()) for k in range(args.members)],
               max_abs_field_float32=[float(np.abs(F - refF.astype(np.float32)).max()) for F in runF],
               members_identical=bool(all(np.array_equal(out[g][0], out[g][k]) for g in range(3)
                                          for k in range(args.members))),
               cpu_runner_s=round(cpu_runner, 1), cpu_native_s=round(cpu_native, 1),
               bodies_t0=nbodies(s["phi"]), bodies_end=nbodies(ref["phi"]),
               native_extremes={f: [float(ref[f].min()), float(ref[f].max())] for f in FIELDS},
               runner_extremes_over_window=watch.members[0]["ext"],
               runner_bodies=watch.members[0]["bodies"])
    print(json.dumps({k: v for k, v in res.items() if k != "runner_bodies"}, indent=1))
    (OUT / "parity.json").write_text(json.dumps(res, indent=1))


def envelope(args):
    s, info = prepared()
    devs = devices(info)
    base = json.loads((OUT / "parity.json").read_text())["runner_extremes_over_window"]   # noise-free sham, 50 tu
    om_max = max(abs(base["om"][0]), abs(base["om"][1]))
    bounds = {"phi": (-1.1, 1.1), "q1": (-1.0, 1.0), "q2": (-1.0, 1.0), "s": (0.0, 2 * base["s"][1]),
              "c": (0.0, 2 * base["c"][1]), "om": (-3 * om_max, 3 * om_max)}
    rows = []
    for p, f in enumerate(FIELDS):
        if f not in args.fields:
            continue
        for g in args.ladder:
            gains = {k: 0.0 for k in DRIVEN}
            gains[f] = g
            o, watch = oracle(world(gains, noise=0.0), s, devs, bounds=bounds)
            act = [{"t": 0.0, "kind": "inject", "device": 0, "port": p, "amp": 3.0, "dur": 50.0}]
            t0 = time.process_time()
            row = dict(field=f, gain=g)
            try:
                out = o.sample_truth(act, q(["device0", "global"], TIMES), 1, truth_seed=5)["samples"]
                row.update(passed=True, centre_t10_25_50=[round(float(out[0][0, i, p, 0]), 4) for i in (9, 24, 49)],
                           global_mean_t10_25_50=[round(float(out[1][0, i, p, 0]), 5) for i in (9, 24, 49)])
            except (OutOfRange, RuntimeError) as e:
                row.update(passed=False, fail=json.loads(str(e)) if str(e).startswith("{") else str(e))
            mem = watch.members[0]
            row.update(extremes={k: [round(v[0], 4), round(v[1], 4)] for k, v in mem["ext"].items()},
                       bodies=[mem["bodies"][0], mem["bodies"][-1]] if mem["bodies"] else [],
                       cpu_s=round(time.process_time() - t0, 1))
            if mem["snap"] is not None and row["passed"]:
                np.savez_compressed(OUT / f"envelope_{f}_g{g:g}.npz", F=mem["snap"])
            rows.append(row)
            print(json.dumps(row), flush=True)
            if row["passed"]:
                break
    path = OUT / "envelope.json"
    old = json.loads(path.read_text()) if path.exists() else {}
    old.setdefault("rows", []).extend(rows)
    old["bounds"] = bounds
    path.write_text(json.dumps(old, indent=1))


def run(args):
    s, info = prepared()
    devs = devices(info)
    gains = json.loads((OUT / "gains.json").read_text())
    act = PROGRAMS[args.program]
    for arm in args.arms:
        role, a = arm.split(":")          # truth:native, pred:mar0, ...
        path = OUT / f"{args.program}_{role}_{a}.npz"
        if path.exists():
            print("skip", path.name, flush=True)
            continue
        d = devs + devices(info, shift=(0.0, 3.0)) if (role == "pred" and a == "native") else devs
        sensors = list(GROUPS) + (["device2", "device3"] if len(d) == 4 else [])
        for k in range(2, len(d)):
            d[k].dev_id = k
        o, watch = oracle(arm_world(a, gains), s, d)
        t0 = time.process_time()
        out = o.sample_truth(act, q(sensors, TIMES), args.members,
                             truth_seed=TRUTH_SEED if role == "truth" else PRED_SEED)["samples"]
        cpu = time.process_time() - t0
        snaps = np.stack([m["snap"] for m in watch.members if m["snap"] is not None])
        np.savez_compressed(path, **{g: out[i] for i, g in enumerate(sensors)}, snaps=snaps,
                            bodies=np.array([[b for _, b in m["bodies"]] for m in watch.members]),
                            body_t=np.array([t for t, _ in watch.members[0]["bodies"]]),
                            ext=np.array([[m["ext"][f] for f in FIELDS] for m in watch.members]),
                            cpu=cpu)
        print(args.program, arm, f"cpu {cpu:.0f}s", flush=True)


def load(program, role, arm):
    z = np.load(OUT / f"{program}_{role}_{arm}.npz")
    return {k: z[k] for k in z.files}


def scales():
    """One pooled scale per field per group, fixed before scoring from the independent native predictor of the
    sham program over the whole 50 tu window (sd over members, times and nodes / mean-variance slots)."""
    z = load("sham", "pred", "native")
    return {g: z[g].std(axis=(0, 1, 3)) + 1e-9 for g in GROUPS}


def es(pred, truth, sc, w, idx_p=None, idx_t=None):
    x = pred[:, :w] / sc[None, None, :, None]
    y = truth[:, :w] / sc[None, None, :, None]
    if idx_p is not None:
        x = x[idx_p]
    if idx_t is not None:
        y = y[idx_t]
    return float(_energy_score(x.reshape(len(x), -1), y.reshape(len(y), -1)))


def score(args):
    sc = scales()
    rng = np.random.default_rng(0)
    res = {}
    initial = None
    for prog in PROGRAMS:
        if not (OUT / f"{prog}_truth_native.npz").exists():
            continue
        truth = load(prog, "truth", "native")
        preds = {}
        for a in ("native", "mar0", "passive", "kappa0", "chis0", "dthalf"):
            if (OUT / f"{prog}_pred_{a}.npz").exists():
                preds[a] = load(prog, "pred", a)
        if prog != "sham" and (OUT / "sham_pred_native.npz").exists():
            preds["ignore_actions"] = load("sham", "pred", "native")
        if "native" in preds:
            nat = preds["native"]
            preds["wrong_probe_geometry"] = {"device0": nat["device2"], "device1": nat["device3"],
                                             "global": nat["global"]}
        # initial persistence: the t=0 readout held constant (computed once, from the prepared template)
        if initial is None:
            s, info = prepared()
            o, _ = oracle(world(), s, devices(info))
            init = o.sample_truth([], q(GROUPS, [0.0]), 1, truth_seed=0)["samples"]
            initial = {g: np.repeat(init[i], len(TIMES), axis=1) for i, g in enumerate(GROUPS)}
        preds["initial_persistence"] = initial
        subs = [(rng.choice(8, 6, replace=False), rng.choice(8, 6, replace=False)) for _ in range(args.nsub)]
        for w in (10, 25, 50):
            full, sub = {}, {}
            for a, p in preds.items():
                for g in GROUPS:
                    full[a, g] = es(p[g], truth[g], sc[g], w)
                    sub[a, g] = np.array([es(p[g], truth[g], sc[g], w, ip if len(p[g]) == 8 else None, it)
                                          for ip, it in subs])
                full[a, "mean"] = np.mean([full[a, g] for g in GROUPS])
                sub[a, "mean"] = np.mean([sub[a, g] for g in GROUPS], axis=0)
            for g in GROUPS + ("mean",):
                row = {}
                for a in preds:
                    r = sub[a, g] / sub["native", g]
                    row[a] = dict(es=round(float(full[a, g]), 4), ratio=round(float(full[a, g] / full["native", g]), 2),
                                  sub90=[round(float(np.percentile(r, 5)), 2), round(float(np.percentile(r, 95)), 2)])
                res.setdefault(prog, {}).setdefault(f"{w}tu", {})[g] = row
    out = dict(scales={g: v.round(5).tolist() for g, v in sc.items()}, fields=FIELDS, results=res,
               note="ratio = energy score of the control predictor / of the independent native predictor, both "
                    "against the same 8 native truth members; sub90 = 5-95% range of that ratio over "
                    f"{args.nsub} random 6-of-8 subsets of predictor members (paired across predictors) and truths")
    (OUT / "scores.json").write_text(json.dumps(out, indent=1))
    for prog, pw in res.items():
        for w, gw in pw.items():
            for g, row in gw.items():
                print(prog, w, g, " ".join(f"{a}={r['ratio']}" for a, r in row.items()))


def readouts(F, devs):
    return {"device0": devs[0].sample(F, 1.0), "device1": devs[1].sample(F, 1.0),
            "global": np.stack((F.mean(axis=(1, 2)), F.var(axis=(1, 2))), axis=1)}


def rms(x, y, sc):
    d = (x - y) / sc[:, None]
    return float(np.sqrt((d ** 2).mean()))


def numerics(args):
    """Noise-free time-step convergence of the world itself, and parity of the runner's dt/2 arm with the native
    module at dt/2; distances in the scoring space (pooled scales) against the noisy ensemble's member spread."""
    s, info = prepared()
    devs = devices(info)
    marks = [1.0, 2.0, 5.0]
    R = {}
    cpu = {}
    for dt in (0.05, 0.025, 0.0125):
        m = world(overrides={"dt": dt}).load()
        st = copy.deepcopy(s)
        per_tu = int(round(50 * 0.05 / dt))
        t0 = time.process_time()
        done = 0
        for mk in marks:
            for _ in range(int(round(mk * per_tu)) - done):
                st = m.step(st)
            done = int(round(mk * per_tu))
            R[dt, mk] = readouts(np.stack([st[f] for f in FIELDS]), devs)
        cpu[dt] = round(time.process_time() - t0, 1)
    gains = json.loads((OUT / "gains.json").read_text())
    o, _ = oracle(arm_world("dthalf", gains, noise=0.0), s, devs)
    run = o.sample_truth([], q(GROUPS, marks), 1, truth_seed=3)["samples"]
    sc = scales()
    ens = load("sham", "pred", "native")
    tru = load("sham", "truth", "native")
    out = {"cpu_native_s": cpu, "runner_dthalf_vs_native_dthalf_max_abs": {}, "rows": []}
    for gi, g in enumerate(GROUPS):
        out["runner_dthalf_vs_native_dthalf_max_abs"][g] = float(max(np.abs(run[gi][0, k] - R[0.025, mk][g]).max()
                                                                  for k, mk in enumerate(marks)))
    for k, mk in enumerate(marks):
        ti = int(mk) - 1
        for g in GROUPS:
            X = ens[g][:, ti]
            spread = np.mean([rms(X[i], X[j], sc[g]) for i in range(8) for j in range(8) if i != j])
            cross = np.mean([rms(X[i], tru[g][j, ti], sc[g]) for i in range(8) for j in range(8)])
            out["rows"].append(dict(t=mk, group=g,
                                    d_dt005_vs_dt0025=round(rms(R[0.05, mk][g], R[0.025, mk][g], sc[g]), 4),
                                    d_dt0025_vs_dt00125=round(rms(R[0.025, mk][g], R[0.0125, mk][g], sc[g]), 4),
                                    noisy_member_spread=round(float(spread), 4),
                                    noisy_pred_truth=round(float(cross), 4)))
    (OUT / "numerics.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["timing", "parity", "envelope", "run", "score", "numerics"])
    ap.add_argument("--tu", type=float, default=50.0)
    ap.add_argument("--members", type=int, default=8)
    ap.add_argument("--fields", nargs="+", default=list(DRIVEN))
    ap.add_argument("--ladder", nargs="+", type=float, default=[1.0, 0.1, 0.01, 0.001])
    ap.add_argument("--program", default="sham")
    ap.add_argument("--arms", nargs="+", default=["truth:native", "pred:native"])
    ap.add_argument("--nsub", type=int, default=200)
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    {"timing": timing, "parity": parity, "envelope": envelope, "run": run, "score": score, "numerics": numerics}[a.cmd](a)
