"""w4 -- shared pieces of the round-4 full-size wind certification (program/round4/wind).

Paths are repository-relative (the study runs on a GPU pod under src/ and on the CPU here).
The world is track2/actuation/wind.py (imported, unchanged) at background sigma_w = 0.05; level 1 is
<Phi_coarse (192), Phi_objects (144)>. New here: a jax.vmap runner of the same tick (GPU batching;
WindWorld's own runner batches with lax.map, the CPU-friendly choice), checked against it in check4.py.

Sets (all generated in one job on one platform):
  F   36 free trajectories at sigma_w = 0.05, the fresh closure layout: init + 50 burn-in, 300 ticks,
      test ticks 40/100/160/220, 5 fresh-noise branches x 32 ticks, the branches at tick 40 run on to 96
  M   the same layout and the same keys at sigma_w = 0 (the wind-free world)
  F2, M2  a second, independent F/M pair (seed SEED_FM2), analysed in the objects view only (no learning
      curve), to double the items of the objects-view F - M contrast
  MW  M's test states branched with wind (sigma_w = 0.05), 6 replicates x 32 ticks whose keys are M's
      (replicate 0 = M's base key and clock, 1..5 = M's branch keys): the paired oracle cost of the wind
  P   36 trajectories at sigma_w = 0.05 under the wind_recert program mix (wr.build_program, the four
      classes none / blind / aimed / regional, 4-tick programs at 150-700 nats), an episode every 16 ticks
      from tick 8 (8, 24, ..., 280), test episodes 24, 56, ..., 280 (9 per trajectory, 324 items, balanced
      classes); at each test episode 5 program branches x 16 ticks and 3 no-input twins on branch keys 0..2
      (twins for every item, so the batch shape is fixed; for 'none' items they duplicate branches 0..2)
Imports: closure_lib (and with it integrate/analyze) must be imported before actuation/ joins sys.path,
because actuation/analyze.py would shadow integrate/analyze.py; use setup_paths(closure=True) first.
"""
from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VEC = os.path.abspath(os.path.join(HERE, "..", "..", ".."))          # research/alife/vecworld
PORT = os.path.join(VEC, "vw1", "port")
CLOSURE_SCRIPTS = os.path.join(VEC, "vw1", "fresh", "closure", "scripts")
ACT = os.path.join(VEC, "program", "track2", "actuation")
WREC = os.path.join(VEC, "program", "track2", "wind_recert")


def setup_paths(closure: bool = False):
    """Put the port first; optionally import closure_lib (and integrate/analyze) before actuation/."""
    if PORT not in sys.path:
        sys.path.insert(0, PORT)
    CL = None
    if closure:
        if CLOSURE_SCRIPTS not in sys.path:
            sys.path.insert(0, CLOSURE_SCRIPTS)
        import closure_lib as CL  # noqa: F401
    for p in (WREC, ACT):
        if p not in sys.path:
            sys.path.insert(0, p)
    return CL


SIGMA = 0.05
J = 36
SEED_FM, SEED_P = 9401, 9501            # new seeds (wind_recert used 9101 / 9201, fresh 301 / 302)
SEED_FM2 = 9411                         # a second F/M pair (objects-view contrast only)
# F / M / MW layout (vw1/fresh/closure/scripts/sim_closure.py)
T_FM, TEST_FM, TB_FM, TX_FM, R_BR = 300, (40, 100, 160, 220), 32, 96, 5
CH_FM, CB_FM = 20, 16                   # base chunk (divides the test ticks), branch chunk
HZ_FM = [1, 2, 4, 8, 16, 32]
# P layout (wind_recert P at 36 trajectories x 300 ticks)
T_P, EP0, EPLEN, TB_P, R_TWIN = 300, 8, 16, 16, 3
EPISODES = tuple(range(EP0, T_P - EPLEN + 1, EPLEN))                # 8, 24, ..., 280
TEST_P = EPISODES[1::2]                                             # 24, 56, ..., 280
HZ_P = [1, 2, 4, 8, 16]


def work_dir():
    w = os.environ.get("W4_WORK", os.path.join(HERE, "work"))
    os.makedirs(w, exist_ok=True)
    return w


def out_dir():
    o = os.environ.get("W4_OUT", os.path.join(HERE, "out"))
    os.makedirs(o, exist_ok=True)
    return o


def progress(msg):
    import time
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    try:
        with open(os.path.join(out_dir(), "progress.txt"), "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


# ----------------------------------------------------------------------------- the vmap runner
def make_runners(WW, batching="vmap"):
    """(init_burn, run) with WindWorld.make_init / make_run semantics (same keys, clocks and law); members
    batched by jax.vmap ('vmap', for the GPU) or jax.lax.map ('map', WindWorld's own choice).
    run(p, A, m, key, t0, uw (B,T,NW), sig (B,)) -> y (B,T+1,336), tab (B,T+1,K,NS), glob (B,T+1,5), A, m
    (no matter kick: this study uses the wind channel only)."""
    import jax
    import jax.numpy as jnp
    from vw.core import Noise
    WD = sys.modules["wind"]
    bt, fold = WW.bt, jax.random.fold_in
    HW = WD.HW

    def one_run(p, A, m, key, t0, uw, sig):
        kp = fold(key, WD._ST_PROC)
        zk = jnp.zeros((HW,))

        def rec(A, m):
            tb, gl = WW.table(m)
            return WW.obs(A, m), tb, gl

        def body(c, w):
            A, m, t = c
            A = WW.tick_x(p, A, Noise(kp, t), zk, w, sig)
            m = bt.update_memory(m, A)
            return (A, m, t + 1), rec(A, m)
        y0, tb0, g0 = rec(A, m)
        (A, m, _), outs = jax.lax.scan(body, (A, m, t0), uw)
        cat = lambda a, b: jnp.concatenate([a[None], b], 0)
        return cat(y0, outs[0]), cat(tb0, outs[1]), cat(g0, outs[2]), A, m

    def one_init(p, k, sig):
        A = WW.lev0.init(p, fold(k, WD._ST_INIT))
        m = bt.init_memory(A)
        kp = fold(fold(k, WD._ST_BURN), WD._ST_PROC)
        z, zw = jnp.zeros((HW,)), jnp.zeros((WD.NW,))

        def body(c, t):
            A, m = c
            A = WW.tick_x(p, A, Noise(kp, t), z, zw, sig)
            return (A, bt.update_memory(m, A)), None
        (A, m), _ = jax.lax.scan(body, (A, m), jnp.arange(WD.BURN_TICKS))
        return A, m

    if batching == "vmap":
        @jax.jit
        def run(p, A, m, key, t0, uw, sig):
            return jax.vmap(one_run, in_axes=(None, 0, 0, 0, 0, 0, 0))(p, A, m, key, t0, uw, sig)

        @jax.jit
        def init_burn(p, k, sig):
            return jax.vmap(one_init, in_axes=(None, 0, 0))(p, k, sig)
    else:
        @jax.jit
        def run(p, A, m, key, t0, uw, sig):
            return jax.lax.map(lambda a: one_run(p, *a), (A, m, key, t0, uw, sig))

        @jax.jit
        def init_burn(p, k, sig):
            return jax.lax.map(lambda a: one_init(p, *a), (k, sig))
    return init_burn, run
