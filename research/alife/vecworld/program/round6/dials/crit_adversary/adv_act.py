"""adv_act -- the adversary's "actuator model": the PUBLIC simulator driven by a linearly filtered command.

    python -B adv_act.py IN.npz OUT.npz [lam] [size] [n_lab] [seed] [key=value ...]     (same arguments as adv_sim.py)

DESIGN-STAGE CHECK, CPU, tiny size, state given (as sublevel_second/gvh.py). PILOT values: never to be reused as an exam.

The recipe knows nothing of the hidden part (no carrier, no conversion at cells, no saturating route). It is told
"the simulator is approximate", sees that Lab episodes without input fit the public law, and so puts a generic
linear filter on the one thing left, the command, and runs the public law with it:

    u'(t) = g0 u(t) + g1 Blur_b[ sum_{k >= 1} w_k u(t - k) ],   w_k = (1 - a) a^(k-1), a = exp(-1 / tau)

(a direct path with gain g0 and a first-order lag with gain g1, time constant tau ticks, spread over (2b+1)^2
bumps). Four numbers on a 39-point grid, least squares on the Lab's focus view at every tick (one hidden-world
future per episode), exactly as gvh.py fits H's three numbers on a 27-point grid of the TRUE form. The grid
contains the public law itself (g0 = 1, g1 = 0). The forecast is the public law run under the filtered command.

IN.npz is adv_sim.py's output for the same arguments (the Lab outcomes y_lab; the programs are regenerated here
with the same random stream and checked against its F_lab / F_test). Writes the Lab simulations of every grid
point and the test ensembles of the best point for Lab sizes 4, 8, 16 (first n episodes).
"""
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SUB = os.path.abspath(os.path.join(HERE, "..", "sublevel_second"))
sys.path.insert(0, SUB)

import numpy as np  # noqa: E402

import sublevel as SL  # noqa: E402
from sublevel import MJ, MW  # noqa: E402
import screen as SC  # noqa: E402
import gvh as GV  # noqa: E402
from adv_sim import blur_matrix  # noqa: E402

T0, H, R, RB = GV.T0, GV.H, GV.R, 2
G0, G1, TAU, BL = (0.25, 0.5, 1.0), (1.0, 2.0, 4.0), (3.0, 8.0), (1, 2)
GRID = [(g0, 0.0, 0.0, 0) for g0 in G0] + [(g0, g1, t, b) for g0 in G0 for g1 in G1 for t in TAU for b in BL]


def filtered(P, g0, g1, tau, b, Wb):
    if g1 == 0.0:
        return g0 * P
    a = np.exp(-1.0 / tau)
    lagp = np.zeros_like(P)
    acc = np.zeros(P.shape[1])
    for t in range(1, P.shape[0]):                           # acc(t) = sum_{k>=1} (1-a) a^(k-1) P(t-k)
        acc = a * acc + (1 - a) * P[t - 1]
        lagp[t] = acc
    for _ in range(b):
        lagp = lagp @ Wb
    return g0 * P + g1 * lagp


def main():
    src, out = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    pos = [a for a in args if "=" not in a]
    kv = {k: float(v) for k, v in (a.split("=", 1) for a in args if "=" in a)}
    lam = float(pos[0]) if len(pos) > 0 else 1.0
    size = int(pos[1]) if len(pos) > 1 else 64
    n_lab = int(pos[2]) if len(pos) > 2 else 16
    seed = int(pos[3]) if len(pos) > 3 else 5
    nats, M = 300.0, 16
    truth = dict({"rho": 0.005, "DX": 0.2}, **kv, lam=lam)
    d = np.load(src)
    cfg = SL.small_cfg(size)
    t_cpu = time.process_time()
    rng = np.random.default_rng(seed)
    spec_p, parts = SL.build(cfg)
    dp = MW.MapWorld(spec_p, world_seed=11).designer         # the agent's public simulator, its own noise keys
    spec_h, _ = SL.build(cfg, "pro", hidden=truth)
    dh = MW.MapWorld(spec_h, world_seed=0).designer          # used ONLY to re-form the same start states as gvh.py
    K = parts["tracker"].K
    ens = dh.ensemble(M, seed=(78, seed))
    ens, rec0 = dh.rollout(ens, None, T=T0, rec=("L1",))
    x = {k: np.asarray(v) for k, v in ens.x.items()}
    _, tgt = SC.programs(cfg, rec0["L1"][:, -1], K, nats, np.random.default_rng(0))
    ok = [i for i in range(M) if tgt[i]["mass_t0"] > 0]
    lab_m = [i for i in ok if i < 8]
    test_m = [i for i in ok if i >= 8]
    lab = [(lab_m[j % len(lab_m)],) + GV.one_program(cfg, tgt[lab_m[j % len(lab_m)]], rng, nats) for j in range(n_lab)]
    test = [(i,) + GV.one_program(cfg, tgt[i], rng, nats) for i in test_m for _ in range(4)]
    assert np.array_equal(np.stack([it[2] for it in lab]), d["F_lab"]) and np.array_equal(np.stack([it[2] for it in test]), d["F_test"])
    y_lab = d["y_lab"]                                       # (n_lab, H + 1, 2): what the Lab showed

    def run(items, reps, progs, keys=None):
        mem = np.repeat([it[0] for it in items], reps)
        xs = {k: x[k][mem] for k in MJ.FIELDS}               # public fields only
        P = np.repeat(np.stack(progs), reps, axis=0)
        _, r = dp.rollout(dp.from_states(xs, keys=keys), P, T=H, rec=("L1",))
        L1 = r["L1"].reshape(len(items), reps, H + 1, -1)
        return np.stack([SC.focus_view(L1[j], K, tgt[it[0]], size) for j, it in enumerate(items)])

    Wb = blur_matrix(cfg)
    kl = dp.w._fresh_keys(len(lab) * RB)                     # common random numbers over the grid
    sim_lab = np.stack([run(lab, RB, [filtered(it[1], *g, Wb) for it in lab], keys=kl).mean(1) for g in GRID])
    cpu_grid = time.process_time() - t_cpu
    s_t = np.maximum(y_lab.std(0), 0.1 * np.median(y_lab[:, 1:].std(0), 0))          # (H + 1, 2) Lab-only scale per tick
    sse = ((((sim_lab - y_lab[None]) / s_t)[:, :, 1:]) ** 2).sum((2, 3))             # (n_grid, n_lab)
    best, ens_test = {}, {}
    for n in (4, 8, 16):
        if n > n_lab:
            continue
        g = int(np.argmin(sse[:, :n].sum(1)))
        best[n] = g
        if g not in ens_test:
            ens_test[g] = run(test, R, [filtered(it[1], *GRID[g], Wb) for it in test])
    np.savez_compressed(out, grid=np.array(GRID), sim_lab=sim_lab, sse=sse, best_n=np.array(sorted(best)),
                        best_g=np.array([best[n] for n in sorted(best)]),
                        **{f"ens_g{g}": v for g, v in ens_test.items()},
                        cpu=np.array([cpu_grid, time.process_time() - t_cpu]), RB=np.array(RB))
    print("saved", out, "cpu_s grid", round(cpu_grid, 1), "total", round(time.process_time() - t_cpu, 1))
    for n in sorted(best):
        print("  n", n, "best (g0, g1, tau, blur)", GRID[best[n]], "sse", round(float(sse[best[n], :n].sum()), 2),
              "public law", round(float(sse[2, :n].sum()), 2))


if __name__ == "__main__":
    main()
