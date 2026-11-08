"""bsim -- level-0 data of the round-4 study `bias` (see b4.py), generated on the GPU and kept on the pod.

usage: python -B bsim.py            (B4_TINY=1 for the CPU code-path test)
Per half (designer seed b4.SEEDS[half]): J_ALL = J_CERT + J_EXTRA members of vw.World(aworld specs['both'])
(jax.vmap batching; init + 50-tick burn-in as the world declares), T free ticks, no input. At each test tick the
J_CERT certification members are cloned R_BR times with explicit fresh keys (make_key(seed + 50, j, i)) and run
TB ticks. Records (float32): raw level 0 x (2 x 128 x 128) and level 1 L1 = <Phi_coarse (192), Phi_objects (144)>.
-> $B4_WORK/data/X_<h>.npy (J_ALL, T+1, 2, 128, 128), L1_<h>.npy (J_ALL, T+1, 336),
   XB_<h>.npy (J_CERT, nT, R_BR, TB, 2, 128, 128), L1B_<h>.npy (J_CERT, nT, R_BR, TB, 336), sim_<h>.json
"""
import os
import sys
import time

import numpy as np

import b4

b4.setup_paths()
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402

import vw  # noqa: E402
import aworld as AW  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

T0 = time.time()
DATA = b4.work_dir("data")
PLAT = {"backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "jax": jax.__version__,
        "numpy": np.__version__, "x64": bool(jax.config.jax_enable_x64), "batching": "vmap (vw.World)"}


def log(*a):
    b4.progress(f"[bsim {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def sim_half(h):
    seed = b4.SEEDS[h]
    kw = {} if b4.BURN is None else {"burn_ticks": b4.BURN}
    specs, parts = AW.build(**kw)
    w = vw.World(specs["both"], world_seed=0)
    d = w.designer
    J, JC, T, TEST, TB, R, CH, CB = b4.J_ALL, b4.J_CERT, b4.T, b4.TEST, b4.TB, b4.R_BR, b4.CH, b4.CB
    assert all(t % CH == 0 for t in TEST) and T % CH == 0 and TB % CB == 0 and max(TEST) + TB <= T
    t1 = time.time()
    ens = d.ensemble(J, seed=(seed,))
    jax.block_until_ready(ens.carry.x)
    secs = {"init_burn": time.time() - t1, "base": 0.0, "branch": 0.0}
    inv0 = {k: np.asarray(v) for k, v in ens.invariants().items()}
    log(h, "init + burn-in", J, "members", round(secs["init_burn"], 1), "s")
    X = np.lib.format.open_memmap(f"{DATA}/X_{h}.npy", "w+", np.float32, (J, T + 1, 2, b4.NPIX, b4.NPIX))
    L1 = np.zeros((J, T + 1, 336), np.float32)
    nT = len(TEST)
    XB = np.lib.format.open_memmap(f"{DATA}/XB_{h}.npy", "w+", np.float32, (JC, nT, R, TB, 2, b4.NPIX, b4.NPIX))
    L1B = np.zeros((JC, nT, R, TB, 336), np.float32)
    t = 0
    while t < T:
        if t in TEST:
            i = TEST.index(t)
            t1 = time.time()
            keys = jnp.concatenate([member_keys(make_key(seed + 50, j, i), R) for j in range(JC)])
            br = ens.clone(rep=R, idx=np.arange(JC), keys=keys)
            done = 0
            while done < TB:
                br, r = d.rollout(br, None, T=CB, rec=("x", "L1"))
                XB[:, i, :, done:done + CB] = r["x"][:, 1:].astype(np.float32).reshape(JC, R, CB, 2, b4.NPIX, b4.NPIX)
                L1B[:, i, :, done:done + CB] = r["L1"][:, 1:].astype(np.float32).reshape(JC, R, CB, 336)
                done += CB
            del br
            secs["branch"] += time.time() - t1
            log(h, "branches at tick", t, {k: round(v, 1) for k, v in secs.items()})
        t1 = time.time()
        ens, r = d.rollout(ens, None, T=CH, rec=("x", "L1"))
        s = 0 if t == 0 else 1
        X[:, t + s:t + CH + 1] = r["x"][:, s:].astype(np.float32).reshape(J, CH + 1 - s, 2, b4.NPIX, b4.NPIX)
        L1[:, t + s:t + CH + 1] = r["L1"][:, s:].astype(np.float32)
        secs["base"] += time.time() - t1
        t += CH
    X.flush()
    XB.flush()
    del X, XB
    np.save(f"{DATA}/L1_{h}.npy", L1)
    np.save(f"{DATA}/L1B_{h}.npy", L1B)
    inv1 = {k: np.asarray(v) for k, v in ens.invariants().items()}
    mt = {"burn": J * (b4.BURN if b4.BURN is not None else AW.BURN_TICKS), "base": J * T, "branch": JC * nT * R * TB}
    meta = {"half": h, "designer_seed": seed, "branch_key": "make_key(seed + 50, j, i), R_BR members", "world_seed": 0,
            "J_ALL": J, "J_CERT": JC, "T": T, "test_ticks": list(TEST), "TB": TB, "R_BR": R, "seconds": secs,
            "member_ticks": mt, "member_ticks_per_s": {"base": mt["base"] / max(secs["base"], 1e-9),
                                                       "branch": mt["branch"] / max(secs["branch"], 1e-9)},
            "platform": PLAT, "tiny": b4.TINY, "tracker": parts.get("tracker_kind"),
            "mass_drift_max_rel": {k: float(np.max(np.abs(inv1[k] - inv0[k]) / np.abs(inv0[k]))) for k in inv0},
            "mass_mean": {k: float(inv0[k].mean()) for k in inv0}, "mass_sd_across_members": {k: float(inv0[k].std()) for k in inv0}}
    b4.jdump(meta, f"{DATA}/sim_{h}.json")
    b4.jdump(meta, os.path.join(b4.out_dir(), f"sim_{h}.json"))
    log(h, "saved", {k: round(v, 1) for k, v in secs.items()}, "member-ticks/s",
        {k: round(v, 1) for k, v in meta["member_ticks_per_s"].items()}, "mass drift", meta["mass_drift_max_rel"])


if __name__ == "__main__":
    log("platform", PLAT, "tiny", b4.TINY)
    for h in (sys.argv[1:] or b4.HALVES):
        sim_half(h)
    log("done")
