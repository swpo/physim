"""csim -- level-0 data of the study `bias2` (see c5.py) for one world (env B5_WORLD), generated on the GPU in
float64 and kept on the pod.

usage: python -B csim.py            (B5_TINY=1 for the CPU code-path test)
Per half (designer seed c5.SEEDS[half]): J members of vw.World(<world's 'pooled' spec>, world_seed 0) with public
parameters (no exam secret), jax.vmap batching. The 'pooled' spec has a memoryless coarse-graining, so no object
tracker runs; only level 0 is recorded. BURN ticks of free evolution (not recorded; in the vortex world they
include the labelling event at t = 300 and the first mutations), then T free ticks, no input (the channel noise
is always on). At each test tick the J_CERT certification members are cloned R_BR times with explicit fresh keys
(make_key(seed + 50, j, i)) and run TB ticks.
Adaptive size: the first two burn-in chunks of half A are timed; if the projected simulation time of both halves
exceeds B5_SIM_BUDGET_S, the number of training-only trajectories (J_EXTRA) is reduced (32 -> 16 -> 8 -> 0) for
both halves. The certification layout never changes.
One study tick = c5.STRIDE world ticks (membrane: 4, through vw.stride; the others 1).
-> $B5_WORK/<world>/data/X_<h>.npy (J, T+1, NCH, 128, 128) float32 in c5.FIELDS order,
   XB_<h>.npy (J_CERT, nT, R_BR, TB, NCH, 128, 128), sim_<h>.json (also in $B5_OUT/<world>)
"""
import os
import sys
import time

import numpy as np

import c5

c5.setup_paths(world=True)
import jax  # noqa: E402

jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402

import vw  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

T0 = time.time()
DATA = c5.work_dir("data")
NP2 = c5.NPIX * c5.NPIX
NC = c5.NCH
PLAT = {"backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "jax": jax.__version__,
        "numpy": np.__version__, "x64": bool(jax.config.jax_enable_x64), "batching": "vmap (vw.World)"}
SIM_BUDGET = min(float(os.environ.get("B5_SIM_BUDGET_S", "2400")), 0.7 * (c5.deadline("sim") - T0))
J_STATE = {"J": c5.J_ALL}


def log(*a):
    c5.progress(f"[csim {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def build_world(stride=None):
    """-> (vw.World, description). Public default parameters; tiny mode shortens the tick (code path only).
    One study tick = `stride` world ticks (default c5.STRIDE; vw.stride: the channel noise is drawn at every
    world tick)."""
    stride = c5.STRIDE if stride is None else int(stride)
    if c5.WORLD == "vortex":
        import vortex_jax as VJ
        import vortex_world as VW
        cfg = VJ.Config()
        if c5.TINY:                      # 10 native steps per tick, labels from the start: NOT the studied world
            cfg = VJ.replace(cfg, n_sub=10, lab_t=0.4, mut_dt=1.0)
        specs, parts = VW.build(cfg)
        desc = {"module": "track1/vortex_world", "config": {k: getattr(cfg, k) for k in cfg.__dataclass_fields__},
                "theta": dict(VJ.THETA), "tick_time": cfg.tick_time}
    elif c5.WORLD == "gliders":
        import aworld as AW
        kw = {"burn_ticks": 2} if c5.TINY else {}
        specs, parts = AW.build(with_objects=False, **kw)
        desc = {"module": "vw1/port/aworld (A_gliders, 'coarse' spec: no tracker)", "tick_time": 1.0,
                "config": {"substeps_per_tick": AW.STRIDE, "burn_ticks_in_init": kw.get("burn_ticks", AW.BURN_TICKS),
                           "flow_noise": AW.NOISE_STD}}
        specs = {"pooled": specs["coarse"]}
    else:
        import membrane_jax as MJ
        import membrane_world as MW
        cfg = MJ.Config()
        specs, parts = MW.build(cfg)
        desc = {"module": "track1/membrane_world", "config": {k: getattr(cfg, k) for k in cfg.__dataclass_fields__},
                "theta": dict(MJ.THETA), "tick_time": cfg.tick_time}
    spec = specs["pooled"]
    if stride > 1:
        spec = vw.stride(spec, stride)
    desc["stride_world_ticks_per_study_tick"] = stride
    desc["study_tick_time"] = desc["tick_time"] * stride
    w = vw.World(spec, world_seed=0)
    return w, desc


def fields_of(xflat):
    """Flat level-0 records (..., NCH * 128^2 [+ 1]) in vw.flat leaf order -> (..., NCH, 128, 128) float32 in
    c5.FIELDS order."""
    lead = xflat.shape[:-1]
    assert xflat.shape[-1] in (NC * NP2, NC * NP2 + 1), xflat.shape
    F = xflat[..., :NC * NP2].reshape(lead + (NC, c5.NPIX, c5.NPIX))
    perm = [c5.FLAT_ORDER.index(f) for f in c5.FIELDS]
    return F[..., perm, :, :].astype(np.float32)


def check_layout(w, ens):
    """The flat record really is the fields in c5.FLAT_ORDER (checked against the state pytree)."""
    x = ens.x
    xf = ens.x_flat()
    F = fields_of(xf)
    if not isinstance(x, dict):                      # gliders: one array (B, 2, 128, 128)
        assert np.array_equal(F, np.asarray(x, np.float32).reshape(F.shape))
        return
    keys = [k for k in sorted(x.keys()) if np.asarray(x[k]).ndim == 3]
    assert tuple(keys) == c5.FLAT_ORDER, (keys, c5.FLAT_ORDER)
    for i, f in enumerate(c5.FIELDS):
        assert np.array_equal(F[:, i], np.asarray(x[f], np.float32)), f


def sim_half(h, w, desc):
    seed = c5.SEEDS[h]
    d = w.designer
    JC, T, TEST, TB, R, CH, CB = c5.J_CERT, c5.T, c5.TEST, c5.TB, c5.R_BR, c5.CH, c5.CB
    assert all(t % CH == 0 for t in TEST) and T % CH == 0 and TB % CB == 0 and max(TEST) + TB <= T
    assert c5.BURN % 2 == 0
    t1 = time.time()
    J0 = c5.J_ALL if h == "A" else J_STATE["J"]
    ens = d.ensemble(J0, seed=(seed,))
    jax.block_until_ready(ens.carry.x)
    check_layout(w, ens)
    secs = {"init": time.time() - t1, "burn": 0.0, "base": 0.0, "branch": 0.0}
    # burn-in in chunks of CH (the last one shorter); half A: time chunk 2 and decide J
    done, rate, chunk_i = 0, None, 0
    while done < c5.BURN:
        n = min(CH, c5.BURN - done)
        tb = time.time()
        ens, _ = d.rollout(ens, None, T=n, rec=())
        jax.block_until_ready(ens.carry.x)
        dt = time.time() - tb
        secs["burn"] += dt
        done += n
        chunk_i += 1
        if h == "A" and chunk_i == 2 and not c5.TINY:
            rate = ens.B * n / dt                                   # member-ticks per second, compiled
            nT = len(TEST)

            def total(J):
                return 2 * (J * (c5.BURN + T) + JC * nT * R * TB) / rate
            J = c5.J_ALL
            for extra in (32, 16, 8, 0):
                J = JC + min(extra, c5.J_EXTRA)
                if total(J) <= SIM_BUDGET:
                    break
            log(f"{h} burn-in rate {rate:.1f} member-ticks/s at B = {ens.B}; projected {total(c5.J_ALL):.0f}s for both "
                f"halves at J = {c5.J_ALL}, budget {SIM_BUDGET:.0f}s -> J = {J} ({total(J):.0f}s)")
            J_STATE["J"] = J
            J_STATE["rate_burn"] = rate
            left = c5.deadline("sim") - time.time()
            if total(J) > 0.85 * left:                             # fail in minutes, not at the deadline (15% margin)
                raise RuntimeError(f"simulation too slow: {total(J):.0f}s needed at J = {J}, {left:.0f}s to the deadline "
                                   f"(needs <= 85% of it)")
            if J < ens.B:
                ens = ens.clone(rep=1, idx=np.arange(J))
    J = ens.B
    assert J == J_STATE["J"] or c5.TINY
    log(h, "init + burn-in", J, "members", {k: round(v, 1) for k, v in secs.items()})
    ens = vw.world.Ensemble(w, ens.carry, 0)       # recorded tick 0 = after burn-in (the members' own clocks, which
    #                                                 key the noise, keep counting from the start of the burn-in)
    X = np.lib.format.open_memmap(f"{DATA}/X_{h}.npy", "w+", np.float32, (J, T + 1, NC, c5.NPIX, c5.NPIX))
    nT = len(TEST)
    XB = np.lib.format.open_memmap(f"{DATA}/XB_{h}.npy", "w+", np.float32, (JC, nT, R, TB, NC, c5.NPIX, c5.NPIX))
    t = 0
    while t < T:
        if t in TEST:
            i = TEST.index(t)
            t1 = time.time()
            keys = jnp.concatenate([member_keys(make_key(seed + 50, j, i), R) for j in range(JC)])
            br = ens.clone(rep=R, idx=np.arange(JC), keys=keys)
            done = 0
            while done < TB:
                br, r = d.rollout(br, None, T=CB, rec=("x",))
                XB[:, i, :, done:done + CB] = fields_of(r["x"][:, 1:]).reshape(JC, R, CB, NC, c5.NPIX, c5.NPIX)
                done += CB
                del r
            del br
            secs["branch"] += time.time() - t1
            log(h, "branches at tick", t, {k: round(v, 1) for k, v in secs.items()})
        t1 = time.time()
        ens, r = d.rollout(ens, None, T=CH, rec=("x",))
        s = 0 if t == 0 else 1
        X[:, t + s:t + CH + 1] = fields_of(r["x"][:, s:])
        del r
        secs["base"] += time.time() - t1
        t += CH
        if time.time() > c5.deadline("sim"):
            raise RuntimeError(f"simulation deadline passed at half {h}, tick {t}")
    X.flush()
    XB.flush()
    # field statistics (per field: mean, sd, min, max over the recorded base frames of every 10th tick)
    sub = np.asarray(X[:, ::10], np.float64)
    stats = {f: {"mean": float(sub[:, :, i].mean()), "sd": float(sub[:, :, i].std()), "min": float(sub[:, :, i].min()),
                 "max": float(sub[:, :, i].max())} for i, f in enumerate(c5.FIELDS)}
    gm = np.stack([np.asarray(X[j], np.float64).reshape(T + 1, NC, -1).mean(-1) for j in range(J)])
    glob = {f: {"mean_first": float(gm[:, 0, i].mean()), "mean_last": float(gm[:, -1, i].mean()),
                "rel_change_first_to_last": float(np.mean(np.abs(gm[:, -1, i] - gm[:, 0, i])) / (np.mean(np.abs(gm[:, :, i])) + 1e-300)),
                "rel_rms_step": float(np.sqrt(np.mean(np.diff(gm[:, :, i], axis=1) ** 2)) / (np.mean(np.abs(gm[:, :, i])) + 1e-300))}
            for i, f in enumerate(c5.FIELDS)}
    del X, XB
    mt = {"burn": J0 * min(2 * CH, c5.BURN) + J * max(c5.BURN - 2 * CH, 0), "base": J * T, "branch": JC * nT * R * TB}
    meta = {"world": c5.WORLD, "world_desc": desc, "half": h, "designer_seed": seed,
            "branch_key": "make_key(seed + 50, j, i), R_BR members", "world_seed": 0, "spec": "pooled (no tracker)",
            "J_ALL": J, "J_CERT": JC, "J_requested": c5.J_ALL, "T": T, "burn_ticks": c5.BURN, "test_ticks": list(TEST),
            "units": "T, burn_ticks, test_ticks, TB and member_ticks are in STUDY ticks (stride world ticks each)",
            "TB": TB, "R_BR": R, "seconds": secs, "member_ticks": mt,
            "member_ticks_per_s": {"burn_chunk2": J_STATE.get("rate_burn"), "base": mt["base"] / max(secs["base"], 1e-9),
                                   "branch": mt["branch"] / max(secs["branch"], 1e-9)},
            "platform": PLAT, "tiny": c5.TINY, "fields": list(c5.FIELDS), "field_stats": stats,
            "global_field_means": glob,
            "note": "base/branch rates include the host transfer of the float64 records"}
    c5.jdump(meta, f"{DATA}/sim_{h}.json")
    c5.jdump(meta, os.path.join(c5.out_dir(), f"sim_{h}.json"))
    log(h, "saved", {k: round(v, 1) for k, v in secs.items()}, "member-ticks/s",
        {k: (round(v, 1) if v else v) for k, v in meta["member_ticks_per_s"].items()})


if __name__ == "__main__":
    log("platform", PLAT, "world", c5.WORLD, "tiny", c5.TINY)
    w, desc = build_world()
    for h in (sys.argv[1:] or c5.HALVES):
        sim_half(h, w, desc)
    log("done")
