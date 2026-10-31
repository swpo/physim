"""c53's fed vortices through PhySim's own OracleRunner via physim.labworld (local prototype).

  prep       native run from seed 0 to t=500 (no noise), saved
  envelope   amp 3 for 50 tu into each port at several gains; finite? response at device0
  score      native forecast vs native / ablated truths for sham and pulse programs
"""
import argparse, json, pickle, sys, time
from pathlib import Path

import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402
from physim.blobround6_eval import _energy_score  # noqa: E402

HERE = Path(__file__).resolve().parent
W = "/home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py"
LAB = "/home/user/physim/research/alife"
FIELDS = ("om", "Y")


def world(gains, overrides=None, noise=0.003, steps_per_tick=1, native_dt=0.02):
    ports = {"om": LW.Port(gain=gains["om"]), "Y": LW.Port(gain=gains["Y"], clip=(0.0, None))}
    nz = {"om": ("additive", noise), "Y": ("proportional", noise)}
    return LW.LabWorld(path=W, fields=FIELDS, steps_per_tick=steps_per_tick, native_dt=native_dt, ports=ports,
                       noise=nz, overrides=overrides or {}, dx=1.0, sys_path=(LAB,), carry=("t",))


def prep(args):
    w = world({"om": 0.0, "Y": 0.0})
    m = w.load()
    if hasattr(m, "ops") and hasattr(m.ops, "WORKERS"):
        m.ops.WORKERS = 1
    s = m.init(0, (128, 128))
    t0 = time.time()
    for _ in range(int(round(500 / 0.02))):
        s = m.step(s)
    om = s["om"]
    from scipy import ndimage
    lab, n = ndimage.label(om > 0.06)
    areas = ndimage.sum(np.ones_like(om), lab, range(1, n + 1))
    order = np.argsort(areas)[::-1]
    c0 = ndimage.center_of_mass(lab == order[len(order) // 2] + 1)
    c1 = ndimage.center_of_mass(lab == order[0] + 1)
    info = dict(t=float(s["t"]), positive_bodies=int(n), centre=[float(c0[0]), float(c0[1])],
                other=[float(c1[0]), float(c1[1])], secs=round(time.time() - t0, 1))
    with open(HERE / "out" / "vortex_prep.pkl", "wb") as fh:
        pickle.dump(s, fh)
    (HERE / "out" / "vortex_prep.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


def prepared():
    with open(HERE / "out" / "vortex_prep.pkl", "rb") as fh:
        s = pickle.load(fh)
    return s, json.loads((HERE / "out" / "vortex_prep.json").read_text())


def devices(info):
    d0 = ProbeDevice(dev_id=0, lattice="square", n_rings=3, base_ds=3.0, center=np.array(info["centre"]) + 0.5,
                     L=128.0, secret_rot=0.3, reflect=False, motion_theta=0.0, motion_reflect=False,
                     node_perm=np.arange(13))
    d1 = ProbeDevice(dev_id=1, lattice="hex", n_rings=3, base_ds=6.0, center=np.array(info["other"]) + 0.5,
                     L=128.0, secret_rot=1.1, reflect=False, motion_theta=0.0, motion_reflect=False,
                     node_perm=np.arange(19))
    return [d0, d1]


def oracle(gains, ov=None, **kw):
    s, info = prepared()
    w = world(gains, ov, **kw)
    o = LW.oracle(w, s, devices(info))
    m = o._stepper.module
    if hasattr(m, "ops") and hasattr(m.ops, "WORKERS"):
        m.ops.WORKERS = 1
    return o


def envelope(args):
    q = [{"sensor": "device0", "t": [10.0, 25.0, 50.0]}, {"sensor": "global", "t": [50.0]}]
    zero = {"om": 0.0, "Y": 0.0}
    sham = oracle(zero).sample_truth([], q, 1, truth_seed=5)["samples"]
    rows = []
    for p, f in enumerate(FIELDS):
        for g in (1.0, 0.1, 0.01, 0.001):
            o = oracle(dict(zero, **{f: g}))
            act = [{"t": 0.0, "kind": "inject", "device": 0, "port": p, "amp": 3.0, "dur": 50.0}]
            t0 = time.time()
            try:
                out = o.sample_truth(act, q, 1, truth_seed=5)["samples"]
                rows.append(dict(field=f, gain=g, finite=True,
                                 centre=[round(float(v), 4) for v in out[0][0, :, p, 0]],
                                 centre_sham=[round(float(v), 4) for v in sham[0][0, :, p, 0]],
                                 global_var=[round(float(v), 5) for v in out[1][0, 0, :, 1]],
                                 global_var_sham=[round(float(v), 5) for v in sham[1][0, 0, :, 1]],
                                 secs=round(time.time() - t0, 1)))
            except RuntimeError as e:
                rows.append(dict(field=f, gain=g, finite=False, error=str(e), secs=round(time.time() - t0, 1)))
            print(json.dumps(rows[-1]), flush=True)
    (HERE / "out" / "vortex_envelope.json").write_text(json.dumps(rows, indent=1))


def score(args):
    gains = json.loads(args.gains)
    times = [float(t) for t in np.arange(1, 51)]
    q = [{"sensor": "device0", "t": times}, {"sensor": "device1", "t": times}, {"sensor": "global", "t": times}]
    programs = {"sham": [],
                "feed": [{"t": 5.0, "kind": "inject", "device": 0, "port": 1, "amp": 3.0, "dur": 10.0}],
                "stir": [{"t": 5.0, "kind": "inject", "device": 0, "port": 0, "amp": 3.0, "dur": 10.0}]}
    O = {"native": oracle(gains, noise=args.noise), "adv0": oracle(gains, {"adv": 0.0}, noise=args.noise),
         "kF0": oracle(gains, {"kF": 0.0}, noise=args.noise),
         "dthalf": oracle(gains, {"dt": 0.01}, noise=args.noise, steps_per_tick=2, native_dt=0.01)}
    res = {}
    for pname, act in programs.items():
        t0 = time.time()
        fc = O["native"].sample_truth(act, q, args.members, truth_seed=101)["samples"]
        truths = {"native": O["native"].sample_truth(act, q, args.members, truth_seed=202)["samples"]}
        for a in ("adv0", "kF0", "dthalf"):
            truths[a] = O[a].sample_truth(act, q, args.members, truth_seed=303)["samples"]
        np.savez_compressed(HERE / "out" / f"{Path(__file__).stem}_{pname}_samples.npz",
                            **{f"{a}_{g}": tr[gi] for a, tr in dict(forecast=fc, **truths).items()
                               for gi, g in enumerate(("device0", "device1", "global"))})
        for w in (10, 25, 50):
            for gi, gname in enumerate(("device0", "device1", "global")):
                xa = fc[gi][:, :w]                      # (members, times, ports, slots)
                pscale = xa.std(axis=(0, 1, 3), keepdims=True) + 1e-6   # one scale per port (field)
                x = (xa / pscale).reshape(args.members, -1) * 1.0
                scale = 1.0
                for a, tr in truths.items():
                    y = (tr[gi][:, :w] / pscale).reshape(args.members, -1)
                    res.setdefault(pname, {}).setdefault(f"{w}tu", {}).setdefault(gname, {})[a] = \
                        round(float(_energy_score(x / scale, y / scale)), 4)
        print(pname, round(time.time() - t0, 1), "s", flush=True)
    ratios = {p: {w: {g: {a: round(v / r["native"], 2) for a, v in r.items() if a != "native"}
                      for g, r in gw.items()} for w, gw in pw.items()} for p, pw in res.items()}
    out = dict(gains=gains, noise=args.noise, members=args.members, scores=res, ratios=ratios)
    (HERE / "out" / f"vortex_runner_score_n{args.noise:g}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(ratios, indent=1))


def null(args):
    """Re-score the numerical null (dt halved) and a parity check against the saved native samples."""
    gains = json.loads(args.gains)
    times = [float(t) for t in np.arange(1, 51)]
    q = [{"sensor": "device0", "t": times}, {"sensor": "device1", "t": times}, {"sensor": "global", "t": times}]
    z = np.load(HERE / "out" / "vortex_demo_sham_samples.npz")
    fc = [z[f"forecast_{g}"] for g in ("device0", "device1", "global")]
    tn = [z[f"native_{g}"] for g in ("device0", "device1", "global")]
    o = oracle(gains, {"dt": 0.01}, noise=args.noise, steps_per_tick=2, native_dt=0.01)
    td = o.sample_truth([], q, args.members, truth_seed=303)["samples"]
    # parity of the rebuilt-state native arm with the saved native forecast (same seed 101)
    on = oracle(gains, {}, noise=args.noise)
    re = on.sample_truth([], q, 2, truth_seed=101)["samples"]
    out = {"parity_max_abs_vs_saved_forecast": float(max(np.abs(re[i] - fc[i][:2]).max() for i in range(3)))}
    for w in (10, 25, 50):
        for gi, g in enumerate(("device0", "device1", "global")):
            xa = fc[gi][:, :w]
            ps = xa.std(axis=(0, 1, 3), keepdims=True) + 1e-6
            x = (xa / ps).reshape(len(xa), -1)
            nat = _energy_score(x, (tn[gi][:, :w] / ps).reshape(len(xa), -1))
            dth = _energy_score(x, (td[gi][:, :w] / ps).reshape(len(xa), -1))
            out[f"{w}tu/{g}"] = round(float(dth / nat), 2)
    (HERE / "out" / "vortex_null.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "envelope", "score", "null"])
    ap.add_argument("--gains", default='{"om": 0.01, "Y": 0.1}')
    ap.add_argument("--noise", type=float, default=0.003)
    ap.add_argument("--members", type=int, default=8)
    a = ap.parse_args()
    {"prep": prep, "envelope": envelope, "score": score, "null": null}[a.cmd](a)
