"""screen_state -- the state-given screen for study (c) on the fed-vortex world at tiny size (CPU).

Round-5 screen, translated: the level's response given the hidden state, ORACLE (the exam-scale law run from the
state with fresh noise) against an AFFORDABLE simulator run from the same state. Exam-scale stand-in: 64 px.
Stages (each a few CPU-minutes; files under <scratch>):
  base                         J states at tick A0 (default 140) from the declared initial law   -> scr_base.npz
  branch --arm A --dtf F       R fresh-noise branches of HZ ticks per state at 64 px under arm A (none, or a
                               200-nat program of the public mix: blind = class b, aimed = class c, regional =
                               class d) with the native step multiplied by F (1 = the law; 2, 4 = the cheap
                               integrator: the same law at 1/F of the cost)                     -> scr_b_A_dtF.npz
  tiles --arm A                every state cut into four 32 px tiles, each run periodically with R fresh-noise
                               branches (arm aimed: the 64 px program restricted to each tile)  -> scr_t_A.npz
All arms share the process-noise keys per branch (paired). Parameters are declared (eps 0.4, mut128 25, others
default): PILOT_NEVER_REUSE_AS_EXAM, nothing hidden. vxlib and vortex_jax are not changed: the coarse step is made
by constructing the runner with a patched Config default inside this process only.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "round5", "vortexexam"))
import jax  # noqa: E402

jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
import vxlib as VX  # noqa: E402

FIELDS = ("om", "Y", "a", "b", "t")
EPS, MUT = 0.4, 25.0
CLS = {"none": "a", "blind": "b", "aimed": "c", "regional": "d"}


def rep_tree(X, R):
    return {k: jnp.repeat(jnp.asarray(v), R, axis=0) for k, v in X.items()}


def runner(H, dtf=1):
    """vxlib.Runner at native step 0.02 * dtf with 250 / dtf steps per tick (same tick time)."""
    if dtf == 1:
        return VX.Runner(H=H)
    orig_cfg, orig_dt = VX.VJ.Config, VX.DT
    try:
        VX.DT = orig_dt * dtf
        VX.VJ.Config = lambda **kw: orig_cfg(dt=orig_dt * dtf, **kw)
        r = VX.Runner(H=H, n_sub=VX.N_SUB // dtf)
    finally:
        VX.VJ.Config, VX.DT = orig_cfg, orig_dt
    assert abs(r.cfg.tick_time - VX.TICK_TIME) < 1e-12
    return r


def programs(arm, seed, y0, r, HZ):
    n = y0.shape[0]
    U = np.zeros((n, HZ, r.m))
    for i in range(n):
        U[i] = VX.make_program(CLS[arm], np.random.default_rng([seed, 5, i]), y0[i], r.K, r.H, HZ, 200.0, r.centres)
    return U


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=("base", "branch", "tiles"))
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--arm", default="none", choices=tuple(CLS))
    ap.add_argument("--dtf", type=int, default=1)
    ap.add_argument("--J", type=int, default=4)
    ap.add_argument("--A0", type=int, default=140)
    ap.add_argument("--R", type=int, default=8)
    ap.add_argument("--HZ", type=int, default=64)
    ap.add_argument("--seed", type=int, default=77)
    a = ap.parse_args()
    S = a.scratch
    c0 = time.process_time()
    fb = os.path.join(S, "scr_base.npz")
    if a.stage == "base":
        r = VX.Runner(H=64)
        Q = VX.theta_batch(a.J, eps=EPS, mut128=MUT)
        keys = jax.random.split(jax.random.key(a.seed), a.J)
        X, M, Y = r.rollout(Q, keys, a.A0, chunk=20)
        l2 = VX.level2(Y, r.K)
        np.savez_compressed(fb, l2=l2, **{k: np.asarray(X[k]) for k in FIELDS},
                            meta=json.dumps(dict(J=a.J, A0=a.A0, seed=a.seed, eps=EPS, mut128=MUT,
                                                 cpu_s=round(time.process_time() - c0, 1))))
        print("base", l2[:, -1].tolist(), round(time.process_time() - c0), "cpu-s", flush=True)
        return
    b = np.load(fb)
    J = b["om"].shape[0]
    X0 = {k: b[k] for k in FIELDS}
    R, HZ = a.R, a.HZ
    kd = jax.random.split(jax.random.key(a.seed + 1), J * R)               # the same for every arm and surrogate
    r64 = VX.Runner(H=64) if (a.stage == "tiles" or a.dtf == 1) else None
    if a.stage == "branch":
        r = r64 if a.dtf == 1 else runner(64, a.dtf)
        Q = VX.theta_batch(J * R, eps=EPS, mut128=MUT)
        X = rep_tree(X0, R)
        M = jax.vmap(lambda x: r.bt.init_memory(r.kinds_field(x)))(X)
        y0 = VX.first_list(r, M)
        U = programs(a.arm, a.seed, y0, r, HZ)
        _, _, Y = r.run(Q, X, M, r.proc_keys(kd, fresh=True), a.A0, U.transpose(1, 0, 2))
        l2 = VX.level2(Y.transpose(1, 0, 2), r.K).reshape(J, R, HZ, 2)
        l0 = VX.level2(y0[:, None], r.K)[:, 0].reshape(J, R, 2)
        np.savez_compressed(os.path.join(S, f"scr_b_{a.arm}_dt{a.dtf}.npz"), l2=l2, l2_0=l0, U=U.astype(np.float32),
                            nats=VX.nats_of(U), finite=bool(np.isfinite(np.asarray(Y)).all()),
                            meta=json.dumps(dict(J=J, R=R, HZ=HZ, A0=a.A0, arm=a.arm, dtf=a.dtf,
                                                 cpu_s=round(time.process_time() - c0, 1))))
        print("branch", a.arm, a.dtf, "N,s_b at +HZ:", l2[:, :, -1].mean(1).round(3).tolist(),
              round(time.process_time() - c0), "cpu-s", flush=True)
        return
    # tiles
    X = rep_tree(X0, R)
    M64 = jax.vmap(lambda x: r64.bt.init_memory(r64.kinds_field(x)))(X)
    U64 = programs(a.arm, a.seed, VX.first_list(r64, M64), r64, HZ)       # (J R, HZ, 16), as in the branch stage
    r = VX.Runner(H=32)
    quads = [(0, 0), (0, 1), (1, 0), (1, 1)]
    Xq, Uq = [], []
    for (qi, qj) in quads:
        Xq.append({k: (jnp.asarray(X[k])[:, 32 * qi:32 * qi + 32, 32 * qj:32 * qj + 32] if k != "t" else jnp.asarray(X[k]))
                   for k in FIELDS})
        idx = [(qi * 2 + ti) * 4 + (qj * 2 + tj) for ti in (0, 1) for tj in (0, 1)]
        Uq.append(U64[:, :, idx])
    Xt = {k: jnp.concatenate([x[k] for x in Xq], 0) for k in FIELDS}       # (4 J R, ...), quadrant-major
    Ut = np.concatenate(Uq, 0)
    n_all = 4 * J * R
    Q = VX.theta_batch(n_all, eps=EPS, mut128=MUT)
    M = jax.vmap(lambda x: r.bt.init_memory(r.kinds_field(x)))(Xt)
    y0 = VX.first_list(r, M)
    kp = r.proc_keys(jax.random.split(jax.random.key(a.seed + 2), n_all), fresh=True)
    _, _, Y = r.run(Q, Xt, M, kp, a.A0, Ut.transpose(1, 0, 2))
    Tb = VX.tables(Y.transpose(1, 0, 2), r.K)
    pres = Tb[..., 0] > 0.5
    n = pres.sum(-1).astype(float).reshape(4, J, R, HZ)
    nb = (pres & (Tb[..., 2] > 0.5)).sum(-1).astype(float).reshape(4, J, R, HZ)
    T0 = VX.tables(y0, r.K)
    p0 = T0[..., 0] > 0.5
    n0 = p0.sum(-1).astype(float).reshape(4, J, R)
    nb0 = (p0 & (T0[..., 2] > 0.5)).sum(-1).astype(float).reshape(4, J, R)
    np.savez_compressed(os.path.join(S, f"scr_t_{a.arm}.npz"), n=n, nb=nb, n0=n0, nb0=nb0,
                        finite=bool(np.isfinite(np.asarray(Y)).all()),
                        meta=json.dumps(dict(J=J, R=R, HZ=HZ, A0=a.A0, arm=a.arm, cpu_s=round(time.process_time() - c0, 1))))
    print("tiles", a.arm, "N at start (sum of tiles)", n0.sum(0)[:, 0].tolist(), "exam-box N", b["l2"][:, -1, 0].tolist(),
          "N at +HZ", n.sum(0)[:, :, -1].mean(1).round(2).tolist(), round(time.process_time() - c0), "cpu-s", flush=True)


if __name__ == "__main__":
    main()
