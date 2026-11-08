"""sim4 -- simulations of the round-4 wind certification (sets F, M, MW, P; see w4.py).

usage: python -B sim4.py fm|fm2|p|all [--tiny] [--batching vmap|map]
  fm   F (sigma_w = 0.05) and M (sigma_w = 0) in one batch with the same keys (72 members), then MW
       (M's test states branched with wind on M's keys) -> $W4_WORK/FM.npz, FM.json
  fm2  a second, independent F/M pair (seed SEED_FM2) for the objects-view F - M contrast -> FM2.npz
  p    P (program mix) -> $W4_WORK/P.npz, P.json
  --tiny  code-path test: 2 trajectories, short layout (CPU)
Records are float32: level 1 (336) every tick; for base trajectories the tracker extras + globals in the
closure layout (K*5 + 5); for branches the 5 globals (identity-event counters).
"""
import json
import os
import sys
import time

import numpy as np

import w4

w4.setup_paths()
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402

import wr  # noqa: E402   (wind_recert: program mix; imports actuation/wind.py and programs.py)
from vw.world import make_key, member_keys  # noqa: E402

WD = wr.WD
MODE = sys.argv[1]
TINY = "--tiny" in sys.argv
BATCHING = sys.argv[sys.argv.index("--batching") + 1] if "--batching" in sys.argv else "vmap"
WORK = w4.work_dir()
K, NF, NS = WD.K_SLOTS, WD.NF, WD.NS
T0 = time.time()

if TINY:
    J = 2
    T_FM, TEST_FM, TB_FM, TX_FM, CH, CB = 12, (4,), 4, 8, 4, 4
    T_P, EPISODES, TEST_P, EPLEN, TB_P = 12, (2, 6), (6,), 4, 4
else:
    J = w4.J
    T_FM, TEST_FM, TB_FM, TX_FM, CH, CB = w4.T_FM, w4.TEST_FM, w4.TB_FM, w4.TX_FM, w4.CH_FM, w4.CB_FM
    T_P, EPISODES, TEST_P, EPLEN, TB_P = w4.T_P, w4.EPISODES, w4.TEST_P, w4.EPLEN, w4.TB_P
R_BR, R_TWIN = w4.R_BR, w4.R_TWIN
assert all(t % CH == 0 for t in TEST_FM) and TB_FM % CB == 0 and TX_FM % CB == 0 and T_FM % CH == 0

WW = WD.WindWorld()
PAR = WW.params
init_burn, run = w4.make_runners(WW, BATCHING)
fold = jax.random.fold_in
PLAT = {"backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "jax": jax.__version__,
        "numpy": np.__version__, "batching": BATCHING, "x64": bool(jax.config.jax_enable_x64)}


def log(*a):
    w4.progress(f"[sim4 {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def dyn(keys):
    return jax.vmap(lambda k: fold(k, WD._ST_DYN))(keys)


def call(A, m, keys, t0, uw, sig):
    """One run call -> y (B,T+1,336) f32, tab65 (B,T+1,K*5+5) f32, full table (B,T+1,K,NS), glob, A, m, s."""
    uw = np.asarray(uw, float)
    B, T = uw.shape[:2]
    t1 = time.time()
    t0a = jnp.asarray(np.broadcast_to(np.asarray(t0, np.int64), (B,)))
    sg = jnp.asarray(np.broadcast_to(np.asarray(sig, float), (B,)))
    y, tab, glob, A1, m1 = run(PAR, A, m, keys, t0a, jnp.asarray(uw), sg)
    y = np.asarray(y, np.float32)
    tab, glob = np.asarray(tab), np.asarray(glob)
    tb = np.concatenate([tab[..., NF:].reshape(B, T + 1, K * 5), glob], -1).astype(np.float32)
    return y, tb, tab, glob.astype(np.float32), A1, m1, time.time() - t1


def chunked(A, m, keys, t0, B, T, sig, chunk):
    """Run T ticks without input in chunks; returns y (B,T,336), glob (B,T,5) (ticks 1..T), A, m, s."""
    ys, gs, secs = [], [], 0.0
    for c in range(T // chunk):
        y, _, _, g, A, m, s = call(A, m, keys, np.asarray(t0) + c * chunk, np.zeros((B, chunk, WD.NW)), sig)
        ys.append(y[:, 1:])
        gs.append(g[:, 1:])
        secs += s
    return np.concatenate(ys, 1), np.concatenate(gs, 1), A, m, secs


def rep(a, r):
    return jnp.repeat(a, r, axis=0)


# ----------------------------------------------------------------------------- F, M, MW
def sim_fm(seed=w4.SEED_FM, tag="FM"):
    keysJ = member_keys(make_key(seed, 0), J)
    keys = jnp.concatenate([keysJ, keysJ])                      # F members 0..J-1, M members J..2J-1
    sig = np.concatenate([np.full(J, w4.SIGMA), np.zeros(J)])
    jj = np.tile(np.arange(J), 2)
    nb = 2 * J
    t1 = time.time()
    A, m = init_burn(PAR, keys, jnp.asarray(sig))
    A.block_until_ready()
    secs = {"init_burn": time.time() - t1, "base": 0.0, "branch": 0.0, "ext": 0.0, "mw": 0.0}
    log("FM init + burn-in", round(secs["init_burn"], 1), "s,", nb, "members")
    kd = dyn(keys)
    nT = len(TEST_FM)
    Ys, TABs = [], []
    Bb = np.zeros((nb, nT, R_BR, TB_FM, WD.NC + WD.NO), np.float32)
    BG = np.zeros((nb, nT, R_BR, TB_FM, 5), np.float32)
    X = np.zeros((nb, R_BR, TX_FM, WD.NC + WD.NO), np.float32)
    MW = np.zeros((J, nT, R_BR + 1, TB_FM, WD.NC + WD.NO), np.float32)
    MWG = np.zeros((J, nT, R_BR + 1, TB_FM, 5), np.float32)
    t = 0
    while t < T_FM:
        if t in TEST_FM:
            i = TEST_FM.index(t)
            bk = jnp.concatenate([member_keys(make_key(seed + 1, int(j), i), R_BR) for j in jj])
            sb = np.repeat(sig, R_BR)
            Ab, mb = rep(A, R_BR), rep(m, R_BR)
            yb, gb, Ab, mb, s = chunked(Ab, mb, bk, t, nb * R_BR, TB_FM, sb, CB)
            Bb[:, i] = yb.reshape(nb, R_BR, TB_FM, -1)
            BG[:, i] = gb.reshape(nb, R_BR, TB_FM, -1)
            secs["branch"] += s
            if i == 0 and TX_FM > TB_FM:
                X[:, :, :TB_FM] = Bb[:, 0]
                yx, _, _, _, s = chunked(Ab, mb, bk, t + TB_FM, nb * R_BR, TX_FM - TB_FM, sb, CB)
                X[:, :, TB_FM:] = yx.reshape(nb, R_BR, TX_FM - TB_FM, -1)
                secs["ext"] += s
            del Ab, mb
            # MW: M's states, keys of M's base continuation (replicate 0) and branches (1..5), with wind
            iM = np.arange(J, 2 * J)
            kw = jnp.concatenate([jnp.concatenate([kd[a][None], bk[a * R_BR:(a + 1) * R_BR]]) for a in iM])
            Aw, mw = rep(A[jnp.asarray(iM)], R_BR + 1), rep(m[jnp.asarray(iM)], R_BR + 1)
            yw, gw, _, _, s = chunked(Aw, mw, kw, t, J * (R_BR + 1), TB_FM, w4.SIGMA, CB)
            MW[:, i] = yw.reshape(J, R_BR + 1, TB_FM, -1)
            MWG[:, i] = gw.reshape(J, R_BR + 1, TB_FM, -1)
            secs["mw"] += s
            del Aw, mw
            log("FM branches at tick", t, {k: round(v, 1) for k, v in secs.items()})
        y, tb, _, _, A, m, s = call(A, m, kd, t, np.zeros((nb, CH, WD.NW)), sig)
        Ys.append(y if t == 0 else y[:, 1:])
        TABs.append(tb if t == 0 else tb[:, 1:])
        secs["base"] += s
        t += CH
    Y, TAB = np.concatenate(Ys, 1), np.concatenate(TABs, 1)
    # check: MW replicate 0 at sigma 0 would be M's base; with wind it must differ, and its first tick only
    # through the wind (recorded, not asserted)
    mt = {"burn": nb * WD.BURN_TICKS, "base": nb * T_FM, "branch": nb * nT * R_BR * TB_FM,
          "ext": nb * R_BR * (TX_FM - TB_FM), "mw": J * nT * (R_BR + 1) * TB_FM}
    meta = {"set": f"{tag}: F+M+MW", "J": J, "T": T_FM, "test_ticks": list(TEST_FM), "TB": TB_FM, "TX": TX_FM, "R_BR": R_BR,
            "seed": seed, "branch_seed": seed + 1, "sigma_F": w4.SIGMA, "sigma_M": 0.0,
            "rows": "Y/TAB/B/BG/X rows 0..J-1 = F, J..2J-1 = M (same keys); MW rows = M's members",
            "seconds": secs, "member_ticks": mt,
            "member_ticks_per_s": {k: mt[k] / max(secs["init_burn" if k == "burn" else k], 1e-9) for k in mt},
            "platform": PLAT, "tiny": TINY,
            "final_mass_mean_F": np.asarray(A)[:J].sum((2, 3)).mean(0).tolist(),
            "final_mass_mean_M": np.asarray(A)[J:].sum((2, 3)).mean(0).tolist()}
    np.savez(f"{WORK}/{tag}.npz", Y=Y, TAB=TAB, B=Bb, BG=BG, X=X, MW=MW, MWG=MWG, sig=sig)
    json.dump(meta, open(f"{WORK}/{tag}.json", "w"), indent=1, default=float)
    log(tag, "saved", {k: round(v, 1) for k, v in secs.items()}, "member-ticks/s",
        {k: round(v, 1) for k, v in meta["member_ticks_per_s"].items()})


# ----------------------------------------------------------------------------- P
def sim_p():
    keysJ = member_keys(make_key(w4.SEED_P, 0), J)
    nT = len(TEST_P)
    test_cls = wr.assign_test_classes(J * nT)
    nb = J
    t1 = time.time()
    A, m = init_burn(PAR, keysJ, jnp.full((nb,), w4.SIGMA))
    A.block_until_ready()
    secs = {"init_burn": time.time() - t1, "base": 0.0, "branch": 0.0}
    log("P init + burn-in", round(secs["init_burn"], 1), "s")
    kd = dyn(keysJ)
    y, tb, tab, _, A, m, s = call(A, m, kd, 0, np.zeros((nb, EPISODES[0], WD.NW)), w4.SIGMA)
    secs["base"] += s
    Ys, TABs = [y], [tb]
    table = tab[:, -1]
    T_end = EPISODES[-1] + EPLEN                                 # last base tick (296 at full size)
    Ufull = np.zeros((nb, T_end, WD.NW), np.float32)
    Bb = np.zeros((nb, nT, R_BR, TB_P, WD.NC + WD.NO), np.float32)
    Bn = np.zeros((nb, nT, R_TWIN, TB_P, WD.NC + WD.NO), np.float32)
    BG = np.zeros((nb, nT, R_BR + R_TWIN, TB_P, 5), np.float32)
    ep_meta, item_meta = [], []
    for e, te in enumerate(EPISODES):
        uw = np.zeros((nb, EPLEN, WD.NW))
        for a in range(nb):
            rng = np.random.default_rng([w4.SEED_P + 3, a, e])
            if te in TEST_P:
                kl = test_cls[a * nT + TEST_P.index(te)]
            else:
                kl = wr.CLASSES[int(rng.integers(len(wr.CLASSES)))]
            U, info = wr.build_program(kl, rng, table[a])
            uw[a, :wr.T_IN] = U
            info.update({"j": a, "episode": e, "tick": int(te), "test": te in TEST_P,
                         "charged_nats": WD.nats(U, wr.SIGMA)})
            ep_meta.append(info)
        Ufull[:, te:te + wr.T_IN] = uw[:, :wr.T_IN]
        if te in TEST_P:
            i = TEST_P.index(te)
            bk = jnp.concatenate([member_keys(make_key(w4.SEED_P + 1, a, i), R_BR) for a in range(nb)])
            tw = jnp.stack([bk[a * R_BR + r] for a in range(nb) for r in range(R_TWIN)])
            Ab = jnp.concatenate([rep(A, R_BR), rep(A, R_TWIN)])
            mb = jnp.concatenate([rep(m, R_BR), rep(m, R_TWIN)])
            ub = np.zeros((nb * (R_BR + R_TWIN), TB_P, WD.NW))
            L = min(EPLEN, TB_P)
            ub[:nb * R_BR, :L] = np.repeat(uw, R_BR, 0)[:, :L]
            yb, _, _, gb, _, _, s = call(Ab, mb, jnp.concatenate([bk, tw]), te, ub, w4.SIGMA)
            secs["branch"] += s
            Bb[:, i] = yb[:nb * R_BR, 1:].reshape(nb, R_BR, TB_P, -1)
            Bn[:, i] = yb[nb * R_BR:, 1:].reshape(nb, R_TWIN, TB_P, -1)
            BG[:, i, :R_BR] = gb[:nb * R_BR, 1:].reshape(nb, R_BR, TB_P, -1)
            BG[:, i, R_BR:] = gb[nb * R_BR:, 1:].reshape(nb, R_TWIN, TB_P, -1)
            for a in range(nb):
                item_meta.append(dict(ep_meta[-nb + a], test_index=i))
        y, tb, tab, _, A, m, s = call(A, m, kd, te, uw, w4.SIGMA)
        secs["base"] += s
        Ys.append(y[:, 1:])
        TABs.append(tb[:, 1:])
        table = tab[:, -1]
        if e % 4 == 0:
            log("P episode", e, "tick", te, {k: round(v, 1) for k, v in secs.items()})
    Y, TAB = np.concatenate(Ys, 1), np.concatenate(TABs, 1)
    assert Y.shape[1] == T_end + 1 and EPISODES[0] + len(EPISODES) * EPLEN == T_end, Y.shape
    mt = {"burn": nb * WD.BURN_TICKS, "base": nb * (Y.shape[1] - 1), "branch": nb * nT * (R_BR + R_TWIN) * TB_P}
    meta = {"set": "P", "J": J, "T": int(Y.shape[1] - 1), "episodes": list(EPISODES), "test_ticks": list(TEST_P),
            "TB": TB_P, "R_BR": R_BR, "R_TWIN": R_TWIN, "seed": w4.SEED_P, "branch_seed": w4.SEED_P + 1,
            "class_seed": "wr.assign_test_classes default (9204); non-test episodes rng [SEED_P + 3, j, e]",
            "sigma": w4.SIGMA, "seconds": secs, "member_ticks": mt, "platform": PLAT, "tiny": TINY,
            "episodes_meta": ep_meta, "items": item_meta}
    np.savez(f"{WORK}/P.npz", Y=Y, TAB=TAB, U=Ufull, B=Bb, Bnone=Bn, BG=BG)
    json.dump(meta, open(f"{WORK}/P.json", "w"), indent=1, default=float)
    log("P saved", Y.shape, {k: round(v, 1) for k, v in secs.items()})


if __name__ == "__main__":
    log("platform", PLAT, "mode", MODE, "tiny", TINY)
    if MODE in ("fm", "all"):
        sim_fm()
    if MODE in ("fm2", "all"):
        sim_fm(w4.SEED_FM2, "FM2")
    if MODE in ("p", "all"):
        sim_p()
    log("done", MODE)
