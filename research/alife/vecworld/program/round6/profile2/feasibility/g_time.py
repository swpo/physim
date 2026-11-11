"""g_time -- profile2 feasibility: what the gliders world with the hidden stress-conversion term (candidate G,
round6/dials/dialsA2) costs on 2 CPU cores.

    taskset -c 0,1 python -I -B g_time.py sim --B 16 --T 16 --out raw/g_sim_B16.json
    taskset -c 0,1 python -I -B g_time.py net --C 48 --batch 128 --out raw/g_net_C48_b128.json

One mode per process (peak resident memory per mode). Compilation timed apart (lower().compile()); timed calls are
calls of the compiled object, `--reps` times (median, min, max).

  sim   the hidden-law simulator of study dialsA2 (round6/dials/dialsA/xlaw.XRunner: gworld's 128 x 128 Flow-Lenia
        wind world, 20 substeps per tick, with dlaw's stress-conversion term at strength eta = 4, plus the public
        object tracker updated every tick, as the Lab, the items and the true-form family run it; the public law
        is the same compiled program at eta = 0). theta = the prior's centre (lR 1, dm_00 0, ls_00 1, lh 1).
        `run`: T ticks under a program (an item's future at 8, 12, 16 ticks is a 16-tick run); `start`: init +
        50-tick burn-in. A Lab episode = start + 16 free ticks + 16 ticks under a program (82 ticks, 33 charged).
        For large B the run is timed on a state after a 1-tick burn-in (cost-equivalent: fixed shapes, no
        data-dependent branch) and the 50-tick start is compiled but not run.
  net   one training step of round 5's block-view net (round5/ladder/ladder_net, as dialsA2 trains it: horizons 8,
        12, 16, lags 0,1,2,4,8, conditioned on theta, M_TRAIN = 4), C channels, given batch, one net, one step per
        dispatch (round 5's trainer; dialsA2's scans 50 steps per dispatch, the same arithmetic).
PILOT ONLY: no truth of the study is used.
"""
from __future__ import annotations

import argparse
import json
import os
import resource
import sys
import time

T_PROC = time.time()
sys.dont_write_bytecode = True
PROG = "/home/user/wt/profile2/research/alife/vecworld/program"
ap = argparse.ArgumentParser()
ap.add_argument("mode", choices=("sim", "net"))
ap.add_argument("--B", type=int, default=1)
ap.add_argument("--T", type=int, default=16)
ap.add_argument("--C", type=int, default=48)
ap.add_argument("--batch", type=int, default=128)
ap.add_argument("--reps", type=int, default=3)
ap.add_argument("--start-reps", type=int, default=None)
ap.add_argument("--out", required=True)
a = ap.parse_args()

sys.path.insert(0, os.path.join(PROG, "round6", "dials", "dialsA"))
t0 = time.time()
import xlaw as X  # noqa: E402  (pins this checkout's port modules, then gworld, ladder_lib, dlaw)
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

T_IMPORT = time.time() - t0
LL, NN, SL, GW = X.LL, X.NN, X.SL, X.GW
NAMES = LL.SETS[4]
OUT = dict(PILOT_NEVER_REUSE_AS_EXAM=True, mode=a.mode, args=vars(a), affinity=sorted(os.sched_getaffinity(0)),
           jax=jax.__version__, xla_flags=os.environ.get("XLA_FLAGS"), cpu="x86 cloud cores (Intel Xeon @ 2.10GHz)",
           seconds_python_start_to_imports_done=time.time() - T_PROC, seconds_imports=T_IMPORT,
           grid=[int(GW.H), int(GW.W)], burn=int(GW.BURN), names=list(NAMES))


def stats(xs):
    xs = sorted(float(x) for x in xs)
    return dict(median=xs[len(xs) // 2] if len(xs) % 2 else 0.5 * (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]),
                min=xs[0], max=xs[-1], n=len(xs), all=xs)


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def timed(f, reps):
    out, r = [], None
    for _ in range(reps):
        t = time.time()
        r = f()
        jax.block_until_ready(r)
        out.append(time.time() - t)
    return out, r


def compile_(fn, *args):
    t = time.time()
    c = fn.lower(*args).compile()
    return c, time.time() - t


if a.mode == "sim":
    B, T = a.B, a.T
    th = np.tile(np.array([[1.0, 0.0, 1.0, 1.0]]), (B, 1))
    Pp = X.params_batch_x(NAMES, th, np.full(B, 4.0))
    k = jax.random.split(jax.random.key(0), B)
    sig = jnp.full((B,), X.SIG)
    XR = X.XRunner(burn=GW.BURN)
    OUT["rss_mb_after_setup"] = rss_mb()
    cs, OUT["compile_s_start_50"] = compile_(XR.init_burn, Pp, k, sig)
    XR1 = X.XRunner(burn=1)
    A, m = XR1.init_burn(Pp, k, sig)                                 # 1-tick state (cost-equivalent)
    kd = GW.dyn_keys(k)
    t0s = jnp.zeros((B,), jnp.int64)
    U = jnp.zeros((B, T, X.NW)).at[:, :4].set(0.05)
    cr, OUT["compile_s_run_T"] = compile_(XR.run, Pp, A, m, kd, t0s, U, sig)
    tr, _ = timed(lambda: cr(Pp, A, m, kd, t0s, U, sig), a.reps)
    OUT["run_T_s"] = stats(tr)
    OUT["member_ticks_per_s_run"] = B * T / OUT["run_T_s"]["median"]
    OUT["core_s_per_member_tick_run"] = 2.0 / OUT["member_ticks_per_s_run"]
    sr = a.reps if a.start_reps is None else a.start_reps
    if sr > 0:
        ts, _ = timed(lambda: cs(Pp, k, sig), sr)
        OUT["start50_s"] = stats(ts)
        OUT["member_ticks_per_s_start50"] = B * GW.BURN / OUT["start50_s"]["median"]
        if T == 16:
            def episode():
                A_, m_ = cs(Pp, k, sig)
                y1, _, _, A_, m_ = cr(Pp, A_, m_, kd, t0s, jnp.zeros((B, 16, X.NW)), sig)
                y1 = SL.quantize(np.asarray(y1))
                Up = np.zeros((B, 16, X.NW))
                for b in range(B):
                    prog = LL.CLASSES["cd"[b % 2]](np.random.default_rng([1, b]), y1[b], 16, SL.EP_CAP)
                    Up[b] = X.program_dense(prog, 16, X.NW)
                return cr(Pp, A_, m_, kd, jnp.full((B,), 16, jnp.int64), jnp.asarray(Up), sig)
            te, _ = timed(episode, sr)
            OUT["episode_82_s"] = stats(te)
            OUT["episode_note"] = "init + 50 burn-in + 16 free + 16 under an aimed or regional program (classes c, d), as sim_episodes_x"
    OUT["rss_mb_peak"] = rss_mb()

if a.mode == "net":
    NN.Cfg.C = a.C
    NN.Cfg.BATCH = a.batch
    NN.Cfg.LAGS, NN.Cfg.HS = (0, 1, 2, 4, 8), (8, 12, 16)
    E = 1024
    rng = np.random.default_rng(0)
    obs = np.abs(rng.normal(0.1, 0.05, (E, 33, X.N_OBS))).astype(np.float32)
    U = np.zeros((E, 32, X.NW), np.float32)
    U[:, 16:20] = rng.normal(0, 0.05, (E, 4, X.NW))
    th_u = rng.uniform(-1, 1, (E, 4))
    ds = NN.make_dataset("block", obs, U, None, theta_u=th_u)
    D = NN.stack_datasets([ds])
    vstep, _ = NN._fns("block", True, tuple(sorted(D)))
    keys = jax.random.split(jax.random.key(1), 1)
    Pm = jax.vmap(lambda kk: NN.init_params("block", kk, True))(keys)
    st = {"t": jnp.zeros((1,), jnp.float32), "m": jax.tree_util.tree_map(jnp.zeros_like, Pm),
          "v": jax.tree_util.tree_map(jnp.zeros_like, Pm)}
    OUT["n_params"] = int(sum(np.prod(v.shape) for v in jax.tree_util.tree_leaves(Pm)))
    ks = jax.random.split(jax.random.key(2), 1)
    OUT["rss_mb_after_setup"] = rss_mb()
    cv, OUT["compile_s_step"] = compile_(vstep, Pm, st, D, ks, 1e-3)
    td, _ = timed(lambda: cv(Pm, st, D, ks, 1e-3), max(a.reps, 5))
    OUT["ms_per_step"] = stats([1e3 * t for t in td])
    OUT["note"] = f"ladder_net block view, cond, C = {a.C}, {NN.Cfg.BLOCKS} blocks, batch {a.batch} x {NN.Cfg.M_TRAIN} draws, one net"
    OUT["rss_mb_peak"] = rss_mb()

OUT["seconds_process"] = time.time() - T_PROC
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
with open(a.out, "w") as f:
    json.dump(OUT, f, indent=1)
print(json.dumps({k: v for k, v in OUT.items() if k not in ("args",)}, default=str)[:1500])
