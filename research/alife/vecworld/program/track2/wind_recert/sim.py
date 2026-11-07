"""sim -- simulations of the wind recertification (all in the wind world of actuation/wind.py).

usage: python -B sim.py smoke            timing, CRN null, program charges (tiny)
       python -B sim.py viab             (a) 6 members x sigma_w in (0, 0.05, 0.1), shared keys,
                                         init + 50 burn-in + 250 ticks; saves states at ticks 100, 200
       python -B sim.py oracle           (a') 12 sigma_w = 0 states (6 members x ticks 100, 200) branched
                                         R = 6 x 16 ticks at each sigma_w with keys shared across sigma_w
       python -B sim.py free [b0 b1]     (b) set F: 16 free trajectories at sigma_w = 0.05, 236 ticks,
                                         test ticks 40/100/160/220, 5 fresh-noise branches x 16 ticks
       python -B sim.py prog [b0 b1]     (b) set P: 16 trajectories at sigma_w = 0.05, 200 ticks, an episode
                                         from the declared mix every 16 ticks (8, 24, ..., 184), test
                                         episodes 24, 56, ..., 184 (balanced classes): 5 program branches
                                         and, for program items, 3 no-input twins on branch keys 0..2
Records are float32: level 1 (336 = coarse 192 + objects 144) every tick, the tracker extras and
globals in the closure layout (K*5 + 5), commands, item metadata. Batches of 4 trajectories are saved
as they finish (results/raw/*.npz); a finished batch is skipped on re-run.
"""
import json
import os
import sys
import time

import jax
import jax.numpy as jnp
import numpy as np

import wr
from vw.world import make_key, member_keys

WD = wr.WD
WW = WD.WindWorld()
PAR = WW.params
init_burn, run = WW.make_init(), WW.make_run()
fold = jax.random.fold_in
K, NF, NS = WD.K_SLOTS, WD.NF, WD.NS
T_ALL = time.time()


def log(*a):
    print(f"[{time.time() - T_ALL:8.1f}s]", *a, flush=True)


def dyn(keys):
    return jax.vmap(lambda k: fold(k, WD._ST_DYN))(keys)


def call(A, m, keys, t0, uw, sig):
    """One run call; uw (B, T, NW); returns numpy y (B,T+1,336), tab (B,T+1,K*5+5), A, m, seconds."""
    uw = np.asarray(uw, float)
    B, T = uw.shape[:2]
    t1 = time.time()
    y, tab, glob, A1, m1 = run(PAR, A, m, keys, jnp.full((B,), int(t0), jnp.int64),
                               jnp.zeros((B, T, WD.KMAX), int), jnp.zeros((B, T, WD.KMAX)), jnp.asarray(uw),
                               jnp.full((B,), float(sig)) if np.ndim(sig) == 0 else jnp.asarray(sig))
    y = np.asarray(y)
    tb = np.concatenate([np.asarray(tab)[..., NF:].reshape(B, T + 1, K * 5), np.asarray(glob)], -1)
    return y, tb, np.asarray(tab), A1, m1, time.time() - t1


def rep(a, r):
    """Repeat members r times (member-major)."""
    return jnp.repeat(a, r, axis=0)


# ----------------------------------------------------------------------------- smoke
def smoke():
    out = {}
    keys = member_keys(make_key(1234, 0), 1)
    t1 = time.time()
    A, m = init_burn(PAR, keys, jnp.full((1,), wr.SIGMA))
    A.block_until_ready()
    out["init_burn_1member_s_incl_compile"] = time.time() - t1
    kd = dyn(keys)
    y, tb, tab, A1, m1, s = call(A, m, kd, 0, np.zeros((1, 4, WD.NW)), wr.SIGMA)
    y, tb, tab, A1, m1, s = call(A1, m1, kd, 4, np.zeros((1, 4, WD.NW)), wr.SIGMA)
    out["s_per_member_tick_1x4"] = s / 4
    # CRN null: two copies of one state, same key, both no input -> identical; and program vs twin differ
    U, info = wr.build_program("aimed", np.random.default_rng(0), tab[0, -1])
    uw = np.zeros((3, 4, WD.NW))
    uw[2] = U
    k3 = jnp.stack([kd[0], kd[0], kd[0]])
    y3, *_ = call(rep(A1, 3), rep(m1, 3), k3, 8, uw, wr.SIGMA)
    out["crn_null_same_key_no_input_L1_maxabs"] = float(np.abs(y3[0] - y3[1]).max())
    out["program_vs_twin_L1_maxabs_by_tick"] = np.abs(y3[2] - y3[0]).max(1).tolist()
    out["aimed_info"] = info
    rng = np.random.default_rng(5)
    out["charges"] = {}
    for kl in wr.CLASSES:
        U, info = wr.build_program(kl, rng, tab[0, -1])
        out["charges"][kl] = {"declared_C": info["C"], "charged_nats": WD.nats(U, wr.SIGMA)}
    log(json.dumps(out, default=float))
    json.dump(out, open(f"{wr.RAW}/smoke.json", "w"), indent=1, default=float)


# ----------------------------------------------------------------------------- (a) viability
def viab():
    fn = f"{wr.RAW}/viab.npz"
    J, S = wr.V_J, wr.V_SIGMAS
    k6 = member_keys(make_key(wr.V_SEED, 0), J)
    keys = k6[jnp.asarray(np.tile(np.arange(J), len(S)))]
    sig = np.repeat(S, J)
    t1 = time.time()
    A, m = init_burn(PAR, keys, jnp.asarray(sig))
    A.block_until_ready()
    secs = {"init_burn": time.time() - t1, "run": 0.0}
    log("viab init + burn-in", round(secs["init_burn"], 1), "s")
    mass0 = np.asarray(A).sum((2, 3))
    kd = dyn(keys)
    Ys, TABs, TABf = [], [], []
    states = {}
    CH = 50
    for c in range(wr.V_T // CH):
        y, tb, tab, A, m, s = call(A, m, kd, c * CH, np.zeros((len(sig), CH, WD.NW)), sig)
        secs["run"] += s
        sl = slice(0, None) if c == 0 else slice(1, None)
        Ys.append(y[:, sl].astype(np.float32))
        TABs.append(tb[:, sl].astype(np.float32))
        TABf.append(tab[:, sl][..., NF:].astype(np.float32))
        tick = (c + 1) * CH
        if tick in wr.V_ORACLE_TICKS:
            i0 = np.flatnonzero(sig == 0.0)
            states[tick] = (np.asarray(A)[i0], np.asarray(m)[i0])
        log("viab tick", tick, "chunk", round(s, 1), "s")
    A1 = np.asarray(A)
    np.savez_compressed(fn, y=np.concatenate(Ys, 1), tab=np.concatenate(TABf, 1), TAB=np.concatenate(TABs, 1),
                        sigmas=sig, member=np.tile(np.arange(J), len(S)), mass0=mass0, mass1=A1.sum((2, 3)),
                        seconds=np.array([secs["init_burn"], secs["run"]]))
    np.savez_compressed(f"{wr.RAW}/viab_states.npz",
                        A=np.concatenate([states[t][0] for t in wr.V_ORACLE_TICKS]),
                        m=np.concatenate([states[t][1] for t in wr.V_ORACLE_TICKS]),
                        tick=np.repeat(wr.V_ORACLE_TICKS, J), member=np.tile(np.arange(J), len(wr.V_ORACLE_TICKS)))
    log("viab saved", fn, secs)


def oracle():
    st = np.load(f"{wr.RAW}/viab_states.npz")
    A0, M0 = jnp.asarray(st["A"]), jnp.asarray(st["m"])
    nS, R = A0.shape[0], wr.V_ORACLE_R
    keys = jnp.concatenate([member_keys(make_key(wr.V_ORACLE_SEED, s), R) for s in range(nS)])
    Y, secs = [], []
    for sw in wr.V_SIGMAS:
        y, *_, s = call(rep(A0, R), rep(M0, R), keys, 0, np.zeros((nS * R, wr.TB, WD.NW)), sw)
        Y.append(y.reshape(nS, R, wr.TB + 1, -1).astype(np.float32))
        secs.append(s)
        log("oracle sigma", sw, round(s, 1), "s")
    np.savez_compressed(f"{wr.RAW}/oracle.npz", y=np.stack(Y), sigmas=np.array(wr.V_SIGMAS), tick=st["tick"],
                        member=st["member"], seconds=np.array(secs))


# ----------------------------------------------------------------------------- (b) set F
def free(b0, b1):
    keysJ = member_keys(make_key(wr.F_SEED, 0), wr.F_J)
    nT = len(wr.F_TEST)
    for b in range(b0, b1):
        fn = f"{wr.RAW}/free_b{b}.npz"
        if os.path.exists(fn):
            continue
        js = np.arange(b * wr.BATCH, (b + 1) * wr.BATCH)
        nb = len(js)
        keys = keysJ[jnp.asarray(js)]
        t1 = time.time()
        A, m = init_burn(PAR, keys, jnp.full((nb,), wr.SIGMA))
        A.block_until_ready()
        secs = {"init_burn": time.time() - t1, "base": 0.0, "branch": 0.0}
        kd = dyn(keys)
        Ys, TABs = [], []
        Bb = np.zeros((nb, nT, wr.R_BR, wr.TB, WD.NC + WD.NO), np.float32)
        t = 0
        while t < wr.F_T:
            if t in wr.F_TEST:
                i = wr.F_TEST.index(t)
                bk = jnp.concatenate([member_keys(make_key(wr.F_SEED + 1, int(j), i), wr.R_BR) for j in js])
                yb, *_, s = call(rep(A, wr.R_BR), rep(m, wr.R_BR), bk, t, np.zeros((nb * wr.R_BR, wr.TB, WD.NW)), wr.SIGMA)
                Bb[:, i] = yb[:, 1:].reshape(nb, wr.R_BR, wr.TB, -1)
                secs["branch"] += s
            y, tb, tab, A, m, s = call(A, m, kd, t, np.zeros((nb, wr.F_CHUNK, WD.NW)), wr.SIGMA)
            secs["base"] += s
            Ys.append((y if t == 0 else y[:, 1:]).astype(np.float32))
            TABs.append((tb if t == 0 else tb[:, 1:]).astype(np.float32))
            t += wr.F_CHUNK
        np.savez_compressed(fn, Y=np.concatenate(Ys, 1), TAB=np.concatenate(TABs, 1), B=Bb, js=js,
                            seconds=np.array([secs["init_burn"], secs["base"], secs["branch"]]))
        log(f"free batch {b}", {k: round(v, 1) for k, v in secs.items()})


# ----------------------------------------------------------------------------- (b) set P
def prog(b0, b1):
    keysJ = member_keys(make_key(wr.P_SEED, 0), wr.P_J)
    nT = len(wr.P_TEST)
    test_cls = wr.assign_test_classes(wr.P_J * nT)
    for b in range(b0, b1):
        fn = f"{wr.RAW}/prog_b{b}.npz"
        if os.path.exists(fn):
            continue
        js = np.arange(b * wr.BATCH, (b + 1) * wr.BATCH)
        nb = len(js)
        keys = keysJ[jnp.asarray(js)]
        t1 = time.time()
        A, m = init_burn(PAR, keys, jnp.full((nb,), wr.SIGMA))
        A.block_until_ready()
        secs = {"init_burn": time.time() - t1, "base": 0.0, "branch": 0.0}
        kd = dyn(keys)
        y, tb, tab, A, m, s = call(A, m, kd, 0, np.zeros((nb, wr.P_EP0, WD.NW)), wr.SIGMA)
        secs["base"] += s
        Ys, TABs = [y.astype(np.float32)], [tb.astype(np.float32)]
        table = tab[:, -1]
        Ufull = np.zeros((nb, wr.P_T, WD.NW), np.float32)
        Bb = np.zeros((nb, nT, wr.R_BR, wr.TB, WD.NC + WD.NO), np.float32)
        Bn = np.full((nb, nT, wr.R_TWIN, wr.TB, WD.NC + WD.NO), np.nan, np.float32)
        ep_meta, item_meta = [], []
        for e, te in enumerate(wr.P_EPISODES):
            uw = np.zeros((nb, wr.P_EPLEN, WD.NW))
            for a, j in enumerate(js):
                rng = np.random.default_rng([wr.P_SEED + 3, int(j), e])
                if te in wr.P_TEST:
                    kl = test_cls[int(j) * nT + wr.P_TEST.index(te)]
                else:
                    kl = wr.CLASSES[int(rng.integers(len(wr.CLASSES)))]
                U, info = wr.build_program(kl, rng, table[a])
                uw[a, :wr.T_IN] = U
                info.update({"j": int(j), "episode": e, "tick": int(te), "test": te in wr.P_TEST,
                             "charged_nats": WD.nats(U, wr.SIGMA)})
                ep_meta.append(info)
            Ufull[:, te:te + wr.T_IN] = uw[:, :wr.T_IN]
            if te in wr.P_TEST:
                i = wr.P_TEST.index(te)
                bk = jnp.concatenate([member_keys(make_key(wr.P_SEED + 1, int(j), i), wr.R_BR) for j in js])
                nn = [a for a in range(nb) if np.abs(uw[a]).sum() > 0]
                tw_keys = [bk[a * wr.R_BR + r] for a in nn for r in range(wr.R_TWIN)]
                Ab = jnp.concatenate([rep(A, wr.R_BR)] + ([A[jnp.asarray(np.repeat(nn, wr.R_TWIN))]] if nn else []))
                mb = jnp.concatenate([rep(m, wr.R_BR)] + ([m[jnp.asarray(np.repeat(nn, wr.R_TWIN))]] if nn else []))
                kb = jnp.concatenate([bk] + ([jnp.stack(tw_keys)] if nn else []))
                ub = np.concatenate([np.repeat(uw, wr.R_BR, 0), np.zeros((len(nn) * wr.R_TWIN, wr.TB, WD.NW))])
                yb, *_, s = call(Ab, mb, kb, te, ub, wr.SIGMA)
                secs["branch"] += s
                Bb[:, i] = yb[:nb * wr.R_BR, 1:].reshape(nb, wr.R_BR, wr.TB, -1)
                if nn:
                    Bn[np.array(nn), i] = yb[nb * wr.R_BR:, 1:].reshape(len(nn), wr.R_TWIN, wr.TB, -1)
                for a, j in enumerate(js):
                    item_meta.append(dict(ep_meta[-nb + a], test_index=i))
            y, tb, tab, A, m, s = call(A, m, kd, te, uw, wr.SIGMA)
            secs["base"] += s
            Ys.append(y[:, 1:].astype(np.float32))
            TABs.append(tb[:, 1:].astype(np.float32))
            table = tab[:, -1]
        np.savez_compressed(fn, Y=np.concatenate(Ys, 1), TAB=np.concatenate(TABs, 1), U=Ufull, B=Bb, Bnone=Bn, js=js,
                            seconds=np.array([secs["init_burn"], secs["base"], secs["branch"]]))
        json.dump({"episodes": ep_meta, "items": item_meta, "seconds": secs}, open(fn.replace(".npz", ".json"), "w"),
                  indent=1, default=float)
        log(f"prog batch {b}", {k: round(v, 1) for k, v in secs.items()},
            "classes", [it["klass"] for it in item_meta])


if __name__ == "__main__":
    mode = sys.argv[1]
    rng_args = [int(a) for a in sys.argv[2:4]] if len(sys.argv) > 3 else [0, 4]
    {"smoke": smoke, "viab": viab, "oracle": oracle}.get(mode, lambda: None)()
    if mode == "free":
        free(*rng_args)
    elif mode == "prog":
        prog(*rng_args)
    log("done", mode)
