"""Legibility data: J fresh designer trajectories of the VW-1 'both' world (<Phi_coarse, Phi_objects>), T free ticks.

usage: python -B stats_run.py J T SEED     -> results/stats_both_J{J}_T{T}.npz (+ .log)

Per member and tick (t = 0 .. T): L1 (336, designer basis: 192 coarse then 144 objects; float32), the
tracker's slot extras tab (K, 5: cy, cx, age, event, uid) and globals glob (5: next uid, births,
deaths, fusions, fissions) read from the carry's tracking memory (designer side, small), and the
per-channel mass from Ensemble.invariants (float64). No level-0 state is stored.
Ensemble: designer.ensemble(J, seed=(SEED,)) (init + 50-tick burn-in), then designer.rollout one tick
at a time (one compiled shape, B = J), no input.
"""
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: F401,E402
import jax  # noqa: E402
import numpy as np  # noqa: E402

import aworld as AW  # noqa: E402

OUT = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
J, T, SEED = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
t0, c0 = time.time(), time.process_time()
log = open(f"{OUT}/stats_both_J{J}_T{T}.log", "w")
specs, parts = AW.build()
w = AW.MapWorld(specs["both"], world_seed=0)
d = w.designer
tr, LW = parts["tracker"], parts["LW"]
K, NS, NF, HW = tr.K, LW.NS, LW.NF, 128 * 128


def mem_parts(ens):
    ms = [np.asarray(m) for m in jax.tree_util.tree_leaves(ens.carry.mem) if m.ndim == 2 and m.shape[1] == tr.n_m]
    assert len(ms) == 1
    m = ms[0]
    return m[:, HW:HW + K * NS].reshape(-1, K, NS)[:, :, NF:].copy(), m[:, HW + K * NS:].copy()


def mass(ens):
    inv = ens.invariants()
    return np.stack([inv["mass_c0"], inv["mass_c1"]], -1)


ens = d.ensemble(J, seed=(SEED,))
print(f"init + burn-in {J} members: {time.time() - t0:.1f} s", file=log, flush=True)
L1, TAB, GLOB, MASS = [ens.level(1)], [], [], [mass(ens)]
tb, gl = mem_parts(ens)
TAB.append(tb)
GLOB.append(gl)
for t in range(T):
    ens, r = d.rollout(ens, None, T=1, rec=("L1",))
    L1.append(r["L1"][:, 1])
    tb, gl = mem_parts(ens)
    TAB.append(tb)
    GLOB.append(gl)
    MASS.append(mass(ens))
    if (t + 1) % 10 == 0:
        print(f"tick {t + 1} wall {time.time() - t0:.1f} s", file=log, flush=True)
sw = lambda a: np.swapaxes(np.array(a), 0, 1)       # (T+1, J, ...) -> (J, T+1, ...)
L1, TAB, GLOB, MASS = sw(L1), sw(TAB), sw(GLOB), sw(MASS)
np.savez_compressed(f"{OUT}/stats_both_J{J}_T{T}.npz", L1=L1.astype(np.float32), tab=TAB.astype(np.float32),
                    glob=GLOB.astype(np.float32), mass=MASS, seed=SEED, wall_s=time.time() - t0,
                    cpu_s=time.process_time() - c0, burn_ticks=AW.BURN_TICKS, stride=AW.STRIDE)
print(f"done wall {time.time() - t0:.1f} s cpu {time.process_time() - c0:.1f} s", file=log, flush=True)
