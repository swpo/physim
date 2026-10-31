"""Deterministic refinement screens (zero noise, no actions, from the prepared state), against the noisy spread.

  spread   8-member noisy sham ensemble at dt 0.05, 128^2, correlated noise, readouts every 1 tu to 10 tu (seed 999):
           the member spread (mean pairwise rms distance in the scoring space) and the frozen screening scales.
  time     dt 0.05 / 0.025 / 0.0125 / 0.00625 at 128^2: readouts at 1, 2, 5, 10 tu; d(dt, dt/2).
  space    n = 128 / 192 / 256 (dx 1, 2/3, 1/2) at dt (arg): d(128, 192), d(192, 256).
Distances: rms over all readout slots of (difference / scale), scale per field (probes) or per field and slot (global).
"""
import argparse, copy, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import rc

MARKS = [1.0, 2.0, 5.0, 10.0]


def scales_from(ens):
    sc = {g: ens[g].std(axis=(0, 1, 3)) + 1e-12 for g in ("device0", "device1")}
    sc["global"] = ens["global"].std(axis=(0, 1)) + 1e-12      # (fields, 2)
    sc["global"][5, 0] = 1.0                                    # mean om is identically 0
    return sc


def scaled(x, g, sc):
    return x / (sc[g][:, None] if g != "global" else sc[g])


def rms(x, y, g, sc):
    return float(np.sqrt(((scaled(x, g, sc) - scaled(y, g, sc)) ** 2).mean()))


def spread(args):
    s, info = rc.prepared()
    o, _ = rc.oracle(rc.world(dt=0.05), s, rc.devices(info))
    t0 = time.process_time()
    out = o.sample_truth([], rc.q(rc.GROUPS, [float(t) for t in range(1, 11)]), 8, truth_seed=999)["samples"]
    ens = {g: out[i] for i, g in enumerate(rc.GROUPS)}
    np.savez_compressed(rc.OUT / "spread_dt005.npz", **ens, cpu=time.process_time() - t0)
    print("spread cpu", round(time.process_time() - t0, 1), flush=True)


def ladder(dts, ns):
    """Zero-noise readouts at MARKS for each (dt, n)."""
    R, cpu = {}, {}
    for dt, n in zip(dts, ns):
        s, info = rc.prepared(n=n, dt=dt)
        devs = rc.devices(info)
        m = rc.world(dt=dt, n=n, noise=0.0).load()
        st = copy.deepcopy(s)
        per_tu = int(round(50 * 0.05 / dt))
        t0 = time.process_time()
        done = 0
        for mk in MARKS:
            k = int(round(mk * per_tu))
            for _ in range(k - done):
                st = m.step(st)
            done = k
            F = np.stack([st[f] for f in rc.FIELDS])
            R[dt, n, mk] = rc.readouts(F, devs, rc.L_BOX / n)
            R[dt, n, mk]["bodies"] = rc.nbodies(st["phi"], dx=rc.L_BOX / n)
        cpu[f"dt{dt}_n{n}"] = round(time.process_time() - t0, 1)
        print(f"dt {dt} n {n} cpu {cpu[f'dt{dt}_n{n}']}", flush=True)
    return R, cpu


def table(R, pairs, label):
    z = np.load(rc.OUT / "spread_dt005.npz")
    ens = {g: z[g] for g in rc.GROUPS}
    sc = scales_from(ens)
    rows = []
    for mk in MARKS:
        ti = int(mk) - 1
        for g in rc.GROUPS:
            X = ens[g][:, ti]
            sp = np.mean([rms(X[i], X[j], g, sc) for i in range(8) for j in range(8) if i != j])
            row = dict(t=mk, group=g, noisy_member_spread=round(float(sp), 4))
            for a, b in pairs:
                d = rms(R[a + (mk,)][g], R[b + (mk,)][g], g, sc)
                row[f"d_{label(a)}_vs_{label(b)}"] = round(d, 4)
                row[f"ratio_{label(a)}_vs_{label(b)}"] = round(d / sp, 3)
            rows.append(row)
    bodies = {f"{label(k[:2])}@{k[2]}": v["bodies"] for k, v in R.items()}
    return rows, bodies


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["spread", "time", "space"])
    ap.add_argument("--dt", type=float, default=0.025)
    a = ap.parse_args()
    rc.OUT.mkdir(exist_ok=True)
    if a.cmd == "spread":
        spread(a)
    elif a.cmd == "time":
        dts = [0.05, 0.025, 0.0125, 0.00625]
        R, cpu = ladder(dts, [128] * 4)
        rows, bodies = table(R, [((dts[i], 128), (dts[i + 1], 128)) for i in range(3)], lambda k: f"dt{k[0]:g}")
        res = dict(cpu=cpu, rows=rows, bodies=bodies)
        (rc.OUT / "det_time.json").write_text(json.dumps(res, indent=1))
        print(json.dumps(res, indent=1))
    else:
        ns = [128, 192, 256]
        R, cpu = ladder([a.dt] * 3, ns)
        rows, bodies = table(R, [((a.dt, 128), (a.dt, 192)), ((a.dt, 192), (a.dt, 256))], lambda k: f"n{k[1]}")
        res = dict(dt=a.dt, cpu=cpu, rows=rows, bodies=bodies)
        (rc.OUT / f"det_space_dt{a.dt:g}.json").write_text(json.dumps(res, indent=1))
        print(json.dumps(res, indent=1))
