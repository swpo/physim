"""f_time -- profile2 feasibility: what the foundry hidden-weights world (candidate F) costs on 2 CPU cores.

    taskset -c 0,1 python -I -B f_time.py sim  --B 16  --out raw/f_sim_B16.json
    taskset -c 0,1 python -I -B f_time.py plug --m 256 --out raw/f_plug_m256.json
    taskset -c 0,1 python -I -B f_time.py net  --C 48 --batch 256 --out raw/f_net_C48_b256.json
    taskset -c 0,1 python -I -B f_time.py fit  --T 32 --out raw/f_fit_T32.json

One mode per process, so that the peak resident memory (ru_maxrss) belongs to that mode alone. Compilation is timed
apart (jax.jit(...).lower(...).compile()); every timed call is a call of the compiled object, repeated `--reps`
times (median, min, max reported). The world is the pilot's public world tnca.draw_theta(2027, 46) (foundrylong's
cpu_part.py uses the same one): PILOT ONLY, never an exam. The automaton's cost does not depend on the state's
values (dense ops, no data-dependent branch), so where a mode needs a state it uses a short spin-up instead of the
300-tick burn-in, and says so in its output.

  sim   the level-0 simulator as the pilot runs it (round6/foundryexam/fx_lib.Runner: per-member weights, vmap):
        init + 300-tick burn-in (`start`), 16 ticks under a program (`run`; one exam item's future, all horizons
        1, 2, 4, 8, 16 come out of it); a Lab episode = start + 16 free ticks + 16 ticks under a mix program.
  plug  the plug-in predictor of one item with m samples (foundrylong/fl_w.predict: m members held to the item's
        17 observed frames by the nudge, then 16 ticks under the item's program), the members taken from a pool
        that the predictor would ship in its artifact (spun up beforehand).
  net   one training step of the pilots' net (round6/foundryexam/fx_net, P0 configuration: lags 0,1,2,4,8 and the
        code), C channels, given batch, M_TRAIN = 4 noise draws per example, one net.
  fit   one Adam gradient of the 16-tick forecast loss with respect to the 248 fit coordinates (foundrylong/fl_w
        _fns(16, 300) value_and_grad, as fit_batch calls it): 8 Lab episodes of T ticks, 4 members, 2 anchors.
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
ap.add_argument("mode", choices=("sim", "plug", "net", "fit"))
ap.add_argument("--B", type=int, default=1)
ap.add_argument("--m", type=int, default=256)
ap.add_argument("--C", type=int, default=48)
ap.add_argument("--batch", type=int, default=256)
ap.add_argument("--T", type=int, default=32)
ap.add_argument("--reps", type=int, default=3)
ap.add_argument("--start-reps", type=int, default=None, help="sim: repetitions of the 300-tick start (default reps; 0 = compile only)")
ap.add_argument("--steps", type=int, default=5, help="net: training steps per timed dispatch")
ap.add_argument("--f32", action="store_true", help="sim: run the automaton in float32 (jax_enable_x64 off after import)")
ap.add_argument("--out", required=True)
a = ap.parse_args()

if a.mode in ("plug", "fit"):
    sys.path.insert(0, os.path.join(PROG, "round6", "foundrylong"))
sys.path.insert(0, os.path.join(PROG, "round6", "foundryexam"))
t0 = time.time()
if a.mode in ("plug", "fit"):
    import fl_w as W  # noqa: E402  (imports fl_lib, which must come before fx_lib: it sets H = 32, horizons 8, 16, 32)
    FL = W.FL
else:
    import fx_lib as FL  # noqa: E402  (tnca, vw: float64)
if a.mode == "net":
    import fx_net as NN  # noqa: E402
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import tnca as TN  # noqa: E402

T_IMPORT = time.time() - t0
if a.f32:                       # the agent's own simulator may run in float32 (the hidden world is float64)
    jax.config.update("jax_enable_x64", False)
FAM = TN.FAM
OUT = dict(PILOT_NEVER_REUSE_AS_EXAM=True, mode=a.mode, args=vars(a), affinity=sorted(os.sched_getaffinity(0)),
           jax=jax.__version__, xla_flags=os.environ.get("XLA_FLAGS"), cpu="x86 cloud cores (Intel Xeon @ 2.10GHz)",
           seconds_python_start_to_imports_done=time.time() - T_PROC, seconds_imports=T_IMPORT)


def stats(xs):
    xs = sorted(float(x) for x in xs)
    return dict(median=xs[len(xs) // 2] if len(xs) % 2 else 0.5 * (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]),
                min=xs[0], max=xs[-1], n=len(xs), all=xs)


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def timed(f, reps):
    out = []
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


TH1 = TN.draw_theta(2027, 46)


def stacked(B):
    return {k: jnp.asarray(v) for k, v in FL.stack_thetas([TH1] * B).items()}


def keys_of(B, seed=0):
    return jax.vmap(lambda i: jax.random.fold_in(jax.random.key(seed), i))(jnp.arange(B))


# ----------------------------------------------------------------------------- sim
if a.mode == "sim":
    B = a.B
    RUN = FL.Runner(B, 300)
    th, keys = stacked(B), keys_of(B)
    ticks = jnp.arange(300)
    OUT["rss_mb_after_setup"] = rss_mb()
    cs, OUT["compile_s_start_300"] = compile_(RUN._start, th, keys, ticks)
    th0 = {kk: v[0] for kk, v in th.items()}
    x = jax.vmap(lambda k: TN.init(th0, k, FAM))(keys)              # unburnt state: cost-equivalent (see header)
    OUT["state_dtype"] = str(x.dtype)
    U = jnp.asarray(np.random.default_rng(0).normal(0, 0.05, (B, FL.H, FL.NW)))
    cr, OUT["compile_s_run_16"] = compile_(RUN._run, th, x, keys, U, 0)
    tr, _ = timed(lambda: cr(th, x, keys, U, 0), a.reps)
    OUT["run16_s"] = stats(tr)
    OUT["member_ticks_per_s_run16"] = B * 16 / OUT["run16_s"]["median"]
    sr = a.reps if a.start_reps is None else a.start_reps
    if sr > 0:
        ts, (xb, y0, _) = timed(lambda: cs(th, keys, ticks), sr)
        OUT["start300_s"] = stats(ts)
        OUT["member_ticks_per_s_start300"] = B * 300 / OUT["start300_s"]["median"]
        # one Lab episode exactly as Runner.episodes builds it: start, 16 free ticks, program from the last frame, 16 ticks
        z = jnp.zeros((B, FL.P, FL.NW))
        cr0 = cr                                                    # same shapes: (B, 16, NW)

        def episode():
            xx, yy, _ = cs(th, keys, ticks)
            xx, Y1, _ = cr0(th, xx, keys, z, 0)
            last = np.asarray(Y1)[:, -1]
            Up = np.stack([FL.prog_dense("abcd"[i % 4], np.random.default_rng([1, i]), last[i]) for i in range(B)])
            return cr0(th, xx, keys, jnp.asarray(Up), FL.P)
        te, _ = timed(episode, sr)
        OUT["episode_332_s"] = stats(te)
        OUT["episode_note"] = "init + 300 burn-in + 16 free + 16 under a mix program (classes a-d), as fx_lib.Runner.episodes"
    OUT["rss_mb_peak"] = rss_mb()

# ----------------------------------------------------------------------------- plug
if a.mode == "plug":
    m = a.m
    th = {k: jnp.asarray(v) for k, v in TH1.items()}
    keys = keys_of(m, 1)
    spin = jax.jit(W.spin, static_argnums=2)
    pool = spin(th, keys, 4)                                        # 4-tick spin-up: cost-equivalent stand-in for the shipped pool
    pool.block_until_ready()
    y = jax.vmap(W.view)(pool[:17])                                 # 17 positive block views as the item's history
    hist = y if y.shape[0] == 17 else jnp.tile(y[:1], (17, 1))
    # (16, NW) aimed program (fl_lib sets FL.H = 32 on import; the pilot's item has 16 test ticks)
    Pt = jnp.asarray(FL.prog_dense("c", np.random.default_rng(3), np.asarray(hist[-1]))[:16])
    pred = jax.jit(lambda th, x, h, p, k: W.predict(th, x, h, p, k, [1, 2, 4, 8, 16]))
    OUT["rss_mb_after_setup"] = rss_mb()
    cp, OUT["compile_s_predict"] = compile_(pred, th, pool, hist, Pt, keys)
    tp, S = timed(lambda: cp(th, pool, hist, Pt, keys), a.reps)
    OUT["predict_s"] = stats(tp)
    OUT["samples_shape"] = list(np.asarray(S).shape)
    OUT["member_ticks"] = m * 32
    OUT["member_ticks_per_s"] = m * 32 / OUT["predict_s"]["median"]
    OUT["pool_bytes_float32"] = int(m * FAM.C * FAM.H * FAM.W * 4)
    OUT["note"] = ("one item: nudge-assimilate the 17 observed frames (16 ticks) and simulate 16 ticks under the item's "
                   "program, m members; the pool (m states after the burn-in) is shipped in the artifact; its spin-up "
                   "here is 4 ticks (cost-equivalent)")
    OUT["rss_mb_peak"] = rss_mb()

# ----------------------------------------------------------------------------- net
if a.mode == "net":
    NN.Cfg.C = a.C
    NN.Cfg.CHUNK = a.steps
    E = 1024
    rng = np.random.default_rng(0)
    obs = np.exp(rng.normal(0, 0.3, (E, FL.T1, FL.NOBS))).astype(np.float32)
    U = np.zeros((E, FL.P + FL.H, FL.NW), np.float32)
    U[:, FL.P:FL.P + 4] = rng.normal(0, 0.1, (E, 4, FL.NW))
    smu, ssd = np.zeros(NN.NS, np.float32), np.ones(NN.NS, np.float32)
    ds = NN.make_dataset(obs, U, smu, ssd)
    cfg = (NN.LAGS_FULL, True, "own")
    D = NN.device_dataset(ds)
    vstep, _ = NN._fns(cfg, tuple(sorted(D)), True, a.batch)
    keys = jnp.stack([jax.random.key(1)])
    Pm = jax.vmap(lambda k: NN.init_params(k, cfg[0]))(keys)
    st = {"t": jnp.zeros((1,), jnp.float32), "m": jax.tree_util.tree_map(jnp.zeros_like, Pm),
          "v": jax.tree_util.tree_map(jnp.zeros_like, Pm)}
    OUT["n_params"] = int(sum(np.prod(v.shape) for v in jax.tree_util.tree_leaves(Pm)))
    ks = jax.random.split(jax.random.key(2), a.steps).reshape(1, a.steps)
    lrs = jnp.full((a.steps,), 1e-3, jnp.float32)
    OUT["rss_mb_after_setup"] = rss_mb()
    cv, OUT["compile_s_step_dispatch"] = compile_(vstep, Pm, st, D, ks, lrs)
    td, _ = timed(lambda: cv(Pm, st, D, ks, lrs), a.reps)
    OUT["dispatch_s"] = stats(td)
    OUT["ms_per_step"] = stats([1e3 * t / a.steps for t in td])
    OUT["examples_per_step"] = a.batch
    OUT["net_samples_per_step"] = a.batch * NN.Cfg.M_TRAIN
    OUT["note"] = f"fx_net P0 configuration, C = {a.C}, {NN.Cfg.BLOCKS} blocks, one net, {a.steps} steps per dispatch (lax.scan)"
    OUT["rss_mb_peak"] = rss_mb()

# ----------------------------------------------------------------------------- fit
if a.mode == "fit":
    T, k, eb, M, A = a.T, 16, 8, 4, 2
    amax = T - k
    vg, ev, sp = W._fns(k, 300)
    th = {kk: jnp.asarray(v) for kk, v in TH1.items()}
    spin = jax.jit(W.spin, static_argnums=2)
    pool = spin(th, keys_of(16, 2), 4)                              # the fit's pool of 16 (cost-equivalent spin-up)
    Yt = jax.jit(lambda th, x, k_: W.forecast(th, x, jnp.zeros((T, FL.NW)), k_, 0))(th, pool[:eb], keys_of(eb, 3))
    hist0 = jax.vmap(W.view)(pool[:eb])                             # (eb, NOBS)
    Ys = jnp.concatenate([hist0[None], Yt], 0).transpose(1, 0, 2)[None]                      # (1, eb, T + 1, NOBS)
    Us = jnp.zeros((1, eb, T, FL.NW)).at[:, :, 16:20].set(0.05)
    dens = W.dens_of(Ys[0])[None]
    Z = jnp.asarray(W.to_z(TH1))[None]
    X0 = pool[jnp.arange(eb * M) % 16].reshape((1, eb, M) + pool.shape[1:])
    keys = jax.vmap(lambda j: jax.random.fold_in(jax.random.key(4), j))(jnp.arange(eb * M)).reshape(1, eb, M)
    scale = jnp.maximum(Ys[0].std((0, 1)), 1e-6)[None]
    an = jnp.asarray(np.random.default_rng(5).integers(0, amax + 1, (1, eb, A)))
    OUT["rss_mb_after_setup"] = rss_mb()
    cg, OUT["compile_s_value_and_grad"] = compile_(vg, Z, dens, X0, Ys, Us, keys, scale, an)
    tg, (l, g) = timed(lambda: cg(Z, dens, X0, Ys, Us, keys, scale, an), a.reps)
    OUT["grad_step_s"] = stats(tg)
    OUT["loss"] = float(np.asarray(l)[0])
    OUT["grad_finite"] = bool(np.all(np.isfinite(np.asarray(g))))
    OUT["n_fit_coordinates"] = int(Z.shape[1])
    OUT["shape"] = dict(T=T, k=k, episodes=eb, members=M, anchors=A, assimilated_ticks_per_member_episode=amax,
                        forward_member_ticks=eb * M * (amax + A * k), forecast_member_ticks_with_gradient=eb * M * A * k)
    OUT["note"] = ("fl_w._fns(16, 300) value_and_grad as fit_batch calls it, one fit (B = 1); the pool respin every 50 steps "
                   "(16 members x 300 ticks) is timed in sim mode (start at B = 16); Adam itself is negligible")
    OUT["rss_mb_peak"] = rss_mb()

OUT["seconds_process"] = time.time() - T_PROC
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
with open(a.out, "w") as f:
    json.dump(OUT, f, indent=1)
print(json.dumps({k: v for k, v in OUT.items() if k not in ("args",)}, default=str)[:1500])
