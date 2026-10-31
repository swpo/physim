"""8-member ensembles through the runner: one program, one (dt, n), one member seed; readouts every 1 tu to 50 tu.

usage: ens.py --program sham|surf --dt DT --n N --seed S [--members 8]
Saves out/ens_{program}_dt{dt}_n{n}_s{seed}.npz (device0, device1, global, bodies per member per tu, final snapshots of
the first 2 members, cpu); skipped when it exists.
"""
import argparse, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import rc


def path(program, dt, n, seed):
    return rc.OUT / f"ens_{program}_dt{dt:g}_n{n}_s{seed}.npz"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--program", required=True)
    ap.add_argument("--dt", type=float, required=True)
    ap.add_argument("--n", type=int, default=128)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--members", type=int, default=8)
    a = ap.parse_args()
    p = path(a.program, a.dt, a.n, a.seed)
    if p.exists():
        print("skip", p.name, flush=True)
        sys.exit(0)
    s, info = rc.prepared(n=a.n, dt=a.dt)
    o, watch = rc.oracle(rc.world(dt=a.dt, n=a.n), s, rc.devices(info))
    t0 = time.process_time()
    out = o.sample_truth(rc.PROGRAMS[a.program], rc.q(rc.GROUPS, rc.TIMES), a.members, truth_seed=a.seed)["samples"]
    cpu = time.process_time() - t0
    np.savez_compressed(p, **{g: out[i] for i, g in enumerate(rc.GROUPS)},
                        snaps=np.stack([m["snap"] for m in watch.members if m["snap"] is not None]),
                        bodies=np.array([[b for _, b in m["bodies"]] for m in watch.members]),
                        body_t=np.array([t for t, _ in watch.members[0]["bodies"]]), cpu=cpu)
    print(p.name, f"cpu {cpu:.0f}s", flush=True)
