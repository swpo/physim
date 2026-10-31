"""phase_membrane through PhySim's own OracleRunner via physim.labworld (local prototype).

  envelope   for each port and gain: inject amp 3 for 50 tu (PhySim's maximum) and
             check the fields stay finite; report the response at the device centre
  score      native forecast vs native truth vs ablated truth, sham and pulse programs,
             energy score per sensor group (device0, device1, global)
"""
import argparse, json, sys, time
from pathlib import Path

import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402
from physim.blobround6_eval import _energy_score  # noqa: E402

HERE = Path(__file__).resolve().parent
PM = "/home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py"
FIELDS = ("S", "K", "L", "phi")


def world(gains, overrides=None, noise=0.01):
    ports = {f: LW.Port(gain=gains[f], clip=(0.0, None)) for f in FIELDS}
    nz = {"phi": ("additive", noise), "S": ("proportional", noise), "K": ("proportional", noise),
          "L": ("proportional", noise)}
    return LW.LabWorld(path=PM, fields=FIELDS, steps_per_tick=1, native_dt=1.0, ports=ports,
                       noise=nz, overrides=overrides or {}, dx=1.0)


def prepared():
    z = np.load(HERE / "out" / "prep_s0.npz")
    info = json.loads((HERE / "out" / "prep_s0.json").read_text())
    return {f: z[f].astype(np.float64) for f in FIELDS}, info


def devices(info):
    c0 = np.array(info["sites"]["centre"]) + 0.5   # pixel index -> world coordinate (dx 1)
    c1 = np.array(info["sites"]["other"]) + 0.5
    d0 = ProbeDevice(dev_id=0, lattice="square", n_rings=3, base_ds=3.0, center=c0, L=128.0,
                     secret_rot=0.3, reflect=False, motion_theta=0.0, motion_reflect=False,
                     node_perm=np.arange(13))
    d1 = ProbeDevice(dev_id=1, lattice="hex", n_rings=3, base_ds=6.0, center=c1, L=128.0,
                     secret_rot=1.1, reflect=False, motion_theta=0.0, motion_reflect=False,
                     node_perm=np.arange(19))
    return [d0, d1]


def envelope(args):
    s0, info = prepared()
    devs = devices(info)
    rows = []
    q = [{"sensor": "device0", "t": [10.0, 25.0, 50.0]}, {"sensor": "global", "t": [50.0]}]
    base_gains = {f: 0.0 for f in FIELDS}
    sham = LW.oracle(world(base_gains), s0, devs).sample_truth([], q, 1, truth_seed=5)["samples"]
    for p, f in enumerate(FIELDS):
        for g in (1.0, 0.1, 0.01, 0.001):
            gains = dict(base_gains, **{f: g})
            o = LW.oracle(world(gains), s0, devs)
            act = [{"t": 0.0, "kind": "inject", "device": 0, "port": p, "amp": 3.0, "dur": 50.0}]
            t0 = time.time()
            try:
                out = o.sample_truth(act, q, 1, truth_seed=5)["samples"]
                d = out[0][0, :, p, 0] - sham[0][0, :, p, 0]    # centre node? node order canonical: ring 0 first
                centre = out[0][0, :, p, 0]
                gl = out[1][0, 0, :, 0] - sham[1][0, 0, :, 0]
                row = dict(field=f, gain=g, finite=True, centre_value=[round(float(v), 4) for v in centre],
                           centre_delta=[round(float(v), 4) for v in d],
                           global_mean_delta=[round(float(v), 4) for v in gl], secs=round(time.time() - t0, 1))
            except RuntimeError as e:
                row = dict(field=f, gain=g, finite=False, error=str(e), secs=round(time.time() - t0, 1))
            rows.append(row)
            print(json.dumps(row), flush=True)
    (HERE / "out" / "runner_envelope.json").write_text(json.dumps(rows, indent=1))


def score(args):
    s0, info = prepared()
    devs = devices(info)
    gains = json.loads(args.gains)
    times = [float(t) for t in np.arange(1, 51)]
    q = [{"sensor": "device0", "t": times}, {"sensor": "device1", "t": times}, {"sensor": "global", "t": times}]
    programs = {"sham": [],
                "pulseK": [{"t": 5.0, "kind": "inject", "device": 0, "port": 1, "amp": 3.0, "dur": 10.0}]}
    arms = {"native": {}, "chi0": {"chi": 0.0}, "gate0": {"gate": 0, "gateK": 0}, "a_half": {"a": 2.0}}
    O = {a: LW.oracle(world(gains, ov, args.noise), s0, devs) for a, ov in arms.items()}
    res = {}
    for pname, act in programs.items():
        t0 = time.time()
        fc = O["native"].sample_truth(act, q, args.members, truth_seed=101)["samples"]
        truths = {"native": O["native"].sample_truth(act, q, args.members, truth_seed=202)["samples"]}
        for a in ("chi0", "gate0", "a_half"):
            truths[a] = O[a].sample_truth(act, q, args.members, truth_seed=303)["samples"]
        np.savez_compressed(HERE / "out" / f"{Path(__file__).stem}_{pname}_samples.npz",
                            **{f"{a}_{g}": tr[gi] for a, tr in dict(forecast=fc, **truths).items()
                               for gi, g in enumerate(("device0", "device1", "global"))})
        for wi, w in enumerate((10, 25, 50)):
            for gi, gname in enumerate(("device0", "device1", "global")):
                xa = fc[gi][:, :w]                      # (members, times, ports, slots)
                pscale = xa.std(axis=(0, 1, 3), keepdims=True) + 1e-6   # one scale per port (field)
                x = (xa / pscale).reshape(args.members, -1) * 1.0
                scale = 1.0
                for a, tr in truths.items():
                    y = (tr[gi][:, :w] / pscale).reshape(args.members, -1)
                    es = _energy_score(x / scale, y / scale)
                    res.setdefault(pname, {}).setdefault(f"{w}tu", {}).setdefault(gname, {})[a] = round(float(es), 4)
        print(pname, round(time.time() - t0, 1), "s", json.dumps(res[pname]), flush=True)
    ratios = {p: {w: {g: {a: round(v / r["native"], 2) for a, v in r.items() if a != "native"}
                      for g, r in gw.items()} for w, gw in pw.items()} for p, pw in res.items()}
    out = dict(gains=gains, noise=args.noise, members=args.members, scores=res, ratios=ratios)
    (HERE / "out" / f"runner_score_n{args.noise:g}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(ratios, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["envelope", "score"])
    ap.add_argument("--gains", default='{"S": 0.01, "K": 0.01, "L": 0.01, "phi": 0.01}')
    ap.add_argument("--noise", type=float, default=0.01)
    ap.add_argument("--members", type=int, default=8)
    a = ap.parse_args()
    {"envelope": envelope, "score": score}[a.cmd](a)
