"""ssim -- level-0 data of the round-5 study `slots` (see s5.py), generated on the GPU and kept on the pod.

usage: python -B ssim.py [A B]      (S5_SIZE=tiny|dev for the CPU code-path test / CPU pilot data)
Per half (designer seed s5.SEEDS[half]): J_ALL = J_CERT + J_EXTRA members of vw.World(aworld specs['both'])
(jax.vmap batching on GPU, lax.map on CPU; init + 50-tick burn-in as the world declares), T free ticks, no input.
At each test tick the J_CERT certification members are cloned R_BR times with explicit fresh keys
(make_key(seed + 50, j, i)) and run TB ticks. The tracker (vw.objects.BlobTracker with the A_gliders settings, the
world's own Phi_objects) is re-run tick by tick on the recorded float64 level-0 frames, starting from the world's
tracker memory, to get what the world's level-1 record does not hold: the full slot table (features + cy, cx, age,
event, uid) and the pixel map of slot labels. The pass is checked against the world's own memory after every chunk.
-> $S5_WORK/data/X_<h>.npy    (J_ALL, T+1, 2, 128, 128) float32      XB_<h>.npy  (J_CERT, nT, R_BR, TB, 2, 128, 128)
                 TAB_<h>.npy  (J_ALL, T+1, 12, 17) float32           TABB_<h>.npy (J_CERT, nT, R_BR, TB, 12, 17)
                 MAP_<h>.npy  (J_ALL, T+1, 128, 128) int8 (slot + 1, 0 = none)
                 BLK_<h>.npy  (J_CERT, T+1, 192) float32 block view   BLKB_<h>.npy (J_CERT, nT, R_BR, TB, 192)
                 sim_<h>.json
"""
import os
import sys
import time

import numpy as np

import s5

s5.setup_paths()
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402

import vw  # noqa: E402
import aworld as AW  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

T0 = time.time()
DATA = s5.work_dir("data")
GPU = jax.default_backend() != "cpu"
PLAT = {"backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "jax": jax.__version__,
        "numpy": np.__version__, "x64": bool(jax.config.jax_enable_x64),
        "batching": "vmap (vw.World)" if GPU else "lax.map (aworld.MapWorld)"}


def log(*a):
    s5.progress(f"[ssim {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def tracker_pass(bt):
    """(mem (B, n_m), frames (n, B, 2*128*128) float64) -> mem', tables (n, B, 12, 17) f32, maps (n, B, HW) int8."""
    def run(mem, X):
        def body(m, x):
            m = jax.vmap(bt.update_memory)(m, x)
            d = bt.split(m)
            return m, (d["table"].astype(jnp.float32), d["map"].astype(jnp.int8))
        return jax.lax.scan(body, mem, X)
    return jax.jit(run)


def sim_half(h):
    seed = s5.SEEDS[h]
    kw = {} if s5.BURN is None else {"burn_ticks": s5.BURN}
    specs, parts = AW.build(**kw)
    w = (vw.World if GPU else AW.MapWorld)(specs["both"], world_seed=0)
    d = w.designer
    bt = parts["tracker"].bt
    tpass = tracker_pass(bt)
    J, JC, T, TEST, TB, R, CH, CB = s5.J_ALL, s5.J_CERT, s5.T, s5.TEST, s5.TB, s5.R_BR, s5.CH, s5.CB
    N = s5.NPIX
    assert all(t % CH == 0 for t in TEST) and T % CH == 0 and TB % CB == 0 and max(TEST) + TB <= T
    t1 = time.time()
    ens = d.ensemble(J, seed=(seed,))
    jax.block_until_ready(ens.carry.x)
    secs = {"init_burn": time.time() - t1, "base": 0.0, "branch": 0.0, "tracker": 0.0}
    inv0 = {k: np.asarray(v) for k, v in ens.invariants().items()}
    log(h, "init + burn-in", J, "members", round(secs["init_burn"], 1), "s")
    nT = len(TEST)
    X = np.lib.format.open_memmap(f"{DATA}/X_{h}.npy", "w+", np.float32, (J, T + 1, 2, N, N))
    XB = np.lib.format.open_memmap(f"{DATA}/XB_{h}.npy", "w+", np.float32, (JC, nT, R, TB, 2, N, N))
    MAP = np.lib.format.open_memmap(f"{DATA}/MAP_{h}.npy", "w+", np.int8, (J, T + 1, N, N))
    TAB = np.zeros((J, T + 1, s5.K, s5.NS), np.float32)
    TABB = np.zeros((JC, nT, R, TB, s5.K, s5.NS), np.float32)
    BLK = np.zeros((JC, T + 1, 192), np.float32)
    BLKB = np.zeros((JC, nT, R, TB, 192), np.float32)

    def wmem(e):                                   # the world's tracker memory (chain = (<Phi_coarse, Phi_objects>,))
        return e.carry.mem[0][1]
    mem = wmem(ens)
    d0 = bt.split(mem)
    TAB[:, 0] = np.asarray(d0["table"], np.float32)
    MAP[:, 0] = np.asarray(d0["map"]).astype(np.int8).reshape(J, N, N)
    chk = {"mem_maxabs_vs_world": 0.0, "readout_maxabs_vs_L1": 0.0}

    def track(mem, xs):                            # xs (B, n, 32768) float64 numpy -> tables (B, n, ..), maps
        t2 = time.time()
        mem, (tab, mp) = tpass(mem, jnp.asarray(np.swapaxes(xs, 0, 1)))
        tab, mp = np.swapaxes(np.asarray(tab), 0, 1), np.swapaxes(np.asarray(mp), 0, 1)
        secs["tracker"] += time.time() - t2
        return mem, tab, mp

    def check(mem, e, tab, L1):
        chk["mem_maxabs_vs_world"] = max(chk["mem_maxabs_vs_world"], float(jnp.max(jnp.abs(mem - wmem(e)))))
        ro = tab[..., :s5.NF].reshape(tab.shape[:-2] + (-1,))
        chk["readout_maxabs_vs_L1"] = max(chk["readout_maxabs_vs_L1"], float(np.abs(ro - L1[..., 192:]).max()))
    t = 0
    while t < T:
        if t in TEST:
            i = TEST.index(t)
            t1 = time.time()
            keys = jnp.concatenate([member_keys(make_key(seed + 50, j, i), R) for j in range(JC)])
            br = ens.clone(rep=R, idx=np.arange(JC), keys=keys)
            mb = wmem(br)
            done = 0
            while done < TB:
                br, r = d.rollout(br, None, T=CB, rec=("x", "L1"))
                mb, tab, _ = track(mb, r["x"][:, 1:])
                check(mb, br, tab, r["L1"][:, 1:].astype(np.float32))
                XB[:, i, :, done:done + CB] = r["x"][:, 1:].astype(np.float32).reshape(JC, R, CB, 2, N, N)
                TABB[:, i, :, done:done + CB] = tab.reshape(JC, R, CB, s5.K, s5.NS)
                BLKB[:, i, :, done:done + CB] = r["L1"][:, 1:, :192].astype(np.float32).reshape(JC, R, CB, 192)
                done += CB
            del br
            secs["branch"] += time.time() - t1
            log(h, "branches at tick", t, {k: round(v, 1) for k, v in secs.items()})
        t1 = time.time()
        ens, r = d.rollout(ens, None, T=CH, rec=("x", "L1"))
        mem, tab, mp = track(mem, r["x"][:, 1:])
        check(mem, ens, tab, r["L1"][:, 1:].astype(np.float32))
        s = 0 if t == 0 else 1
        X[:, t + s:t + CH + 1] = r["x"][:, s:].astype(np.float32).reshape(J, CH + 1 - s, 2, N, N)
        TAB[:, t + 1:t + CH + 1] = tab
        MAP[:, t + 1:t + CH + 1] = mp.reshape(J, CH, N, N)
        BLK[:, t + s:t + CH + 1] = r["L1"][:JC, s:, :192].astype(np.float32)
        secs["base"] += time.time() - t1
        t += CH
    X.flush()
    XB.flush()
    MAP.flush()
    del X, XB, MAP
    for nm, a in (("TAB", TAB), ("TABB", TABB), ("BLK", BLK), ("BLKB", BLKB)):
        np.save(f"{DATA}/{nm}_{h}.npy", a)
    inv1 = {k: np.asarray(v) for k, v in ens.invariants().items()}
    ov = np.asarray(bt.split(mem)["overflow"])
    pres = TAB[..., 0] > 0.5
    ev = TAB[..., 15]
    mt = {"burn": J * (s5.BURN if s5.BURN is not None else AW.BURN_TICKS), "base": J * T, "branch": JC * nT * R * TB}
    meta = {"half": h, "designer_seed": seed, "branch_key": "make_key(seed + 50, j, i), R_BR members", "world_seed": 0,
            "J_ALL": J, "J_CERT": JC, "T": T, "test_ticks": list(TEST), "TB": TB, "R_BR": R, "seconds": secs,
            "member_ticks": mt, "member_ticks_per_s": {"base": mt["base"] / max(secs["base"], 1e-9),
                                                       "branch": mt["branch"] / max(secs["branch"], 1e-9)},
            "platform": PLAT, "size": s5.SIZE, "tracker": parts.get("tracker_kind"),
            "tracker_pass_check": chk, "tracker_overflow_max": ov.max(0).tolist(),
            "objects": {"count_mean": float(pres.sum(-1).mean()), "count_min": int(pres.sum(-1).min()),
                        "count_max": int(pres.sum(-1).max()),
                        "mass_in_objects_mean": float(np.where(pres, TAB[..., 1], 0).sum(-1).mean()),
                        "events_per_traj": {k: float((ev == v).sum() / J) for k, v in vw.objects.EVENTS.items() if v}},
            "mass_drift_max_rel": {k: float(np.max(np.abs(inv1[k] - inv0[k]) / np.abs(inv0[k]))) for k in inv0},
            "mass_mean": {k: float(inv0[k].mean()) for k in inv0}, "mass_sd_across_members": {k: float(inv0[k].std()) for k in inv0}}
    s5.jdump(meta, f"{DATA}/sim_{h}.json")
    s5.jdump(meta, os.path.join(s5.out_dir(), f"sim_{h}.json"))
    log(h, "saved", {k: round(v, 1) for k, v in secs.items()}, "member-ticks/s",
        {k: round(v, 1) for k, v in meta["member_ticks_per_s"].items()}, "tracker check", chk, "objects", meta["objects"])


if __name__ == "__main__":
    log("platform", PLAT, "size", s5.SIZE)
    for h in (sys.argv[1:] or s5.HALVES):
        sim_half(h)
    log("done")
