"""views -- the screen of screen.py on two observed views and on the exam's horizons (CPU, about 8 minutes).

Same states, keys, programs and scores as screen.py (see its docstring), with the tracker running in the
futures, so that both round-5 views with a history-only signal can be scored from one set of futures:
    block  192 numbers / SC1 (level 1; the ladder's 'block' cell)
    pop    5 numbers (count, tracked mass, mean speed, SD of body mass, largest body: ladder_lib.pop5) /
           public scales (gliders_exam level-2 scales for the first three; SD over this run's no-input
           futures for the other two, as ladder_lib.public_scales)
Horizons 1, 2, 4, 8, 16 (the exam's cells). Quantities per view and program: the state-given screen
(PLUG - O) / (K - O), and the history-only surrogate share (INC public - INC true) / (K - INC true), where
INC(law) = the item's own start + other states' increments under `law` (block view: pushed blocks aligned).
PILOT, design phase: public seeds, never an exam. Writes results/views_<cand>_<eta>.json.
"""
import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument("--cand", default="XW")
ap.add_argument("--eta", type=float, default=4.0)
ap.add_argument("--progs", default="c,d")
ap.add_argument("--ns", type=int, default=6)
ap.add_argument("--R", type=int, default=5)
ap.add_argument("--H", type=int, default=16)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--scratch", default="/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dials_defect_gliders")
args = ap.parse_args()
t00 = time.time()
import dlaw as DL  # noqa: E402
sys.path.insert(0, os.path.join(DL.PROG, "round5", "ladder"))
import ladder_lib as LL  # noqa: E402
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from vw.scoring import energy_fair, energy_loo, _pd  # noqa: E402

GW = DL.GW
NS, R, Hh = args.ns, args.R, args.H
HS = [h for h in (1, 2, 4, 8, 16) if h <= Hh]
CK = {"G": "g", "XW": "xw", "M": "m", "X": "x", "T": "t"}


def log(*a):
    print(f"[{time.time() - t00:6.0f}s]", *a, flush=True)


def loo_cross(X, Y):
    Rn = Y.shape[0]
    Dxy, Dxx = _pd(X, Y), _pd(X, X)
    m = Rn - 1
    out = []
    for r in range(Rn):
        keep = np.arange(Rn) != r
        out.append(Dxy[keep, r].mean() - Dxx[np.ix_(keep, keep)].sum() / (2.0 * m * (m - 1)))
    return float(np.mean(out))


P_pub, Q0, T0 = GW.base_params(), DL.qdict(), jnp.zeros((2, DL.H, DL.W))
Q_true = DL.qdict(**{CK[args.cand]: args.eta})
RN = DL.DRunner()
ks = jax.random.split(jax.random.key(1000 + args.seed), NS)
A, S, m, obs = RN.init_burn(DL.rep(P_pub, NS), DL.rep(Q_true, NS), T0, ks, jnp.full((NS,), DL.SIG))
A, S, m, obs = (np.asarray(v) for v in (A, S, m, obs))
log("burn done")
B = NS * R
kd = GW.dyn_keys(ks)
keys = jnp.stack([jax.random.fold_in(kd[b], 100 + r) for b in range(NS) for r in range(R)])
rs = lambda X: jnp.asarray(np.repeat(np.asarray(X), R, axis=0))


def futures(Q, S_, U):
    y = RN.fut_obs(DL.rep(P_pub, B), DL.rep(Q, B), T0, rs(A), rs(S_), rs(m), keys, jnp.zeros((B,), jnp.int64), rs(U),
                   jnp.full((B,), DL.SIG))
    return np.asarray(y).reshape(NS, R, Hh + 1, LL.N_OBS)


def program(cls, b):
    rng = np.random.default_rng([args.seed, b, ord(cls)])          # as screen.py
    yc, yo = obs[b, :GW.NC], obs[b, GW.NC:GW.NC + GW.NO]
    if cls == "a":
        return np.zeros((Hh, DL.NW))
    if cls == "c":
        return GW.aimed_push(yo, 200.0, DL.SIG, H=Hh)[0]
    if cls == "d":
        return GW.regional_push(yc, rng.uniform(0, 2 * np.pi), 300.0, DL.SIG, H=Hh)
    raise KeyError(cls)


def anchor(U_b, yc):
    on = np.abs(U_b.reshape(Hh, 2, DL.G, DL.G)).sum(1)
    tt = np.flatnonzero(on.sum((1, 2)) > 0)
    if tt.size == 0:
        return GW.heaviest_group(yc)
    ii, jj = np.nonzero(on[tt[0]] > 0)
    cm = lambda v: int(np.rint(np.angle(np.exp(2j * np.pi * (v + 0.5) / DL.G).mean()) * DL.G / (2 * np.pi))) % DL.G
    return cm(ii), cm(jj)


Ya = futures(Q_true, S, np.zeros((NS, Hh, DL.NW)))                 # no input, true law: climatology pool, scales
log("no-input futures done")
pa = LL.pop5(Ya).reshape(-1, 5)
SCP = np.concatenate([LL.SL.SC2, np.maximum(pa[:, 3:].std(0), 1e-6)])
VIEWS = {"block": (lambda Y: Y[..., :GW.NC], DL.SC1, True), "pop": (LL.pop5, SCP, False)}
out = {"what": "state-given screen and history-only surrogate on the block and population views, horizons to 16; see views.py docstring",
       "PILOT_NEVER_REUSE_AS_EXAM": True, "cand": args.cand, "eta": args.eta,
       "config": {"n_states": NS, "R": R, "H": Hh, "hs": HS, "seed": args.seed, "pop_scales": SCP.tolist()}, "programs": {}}


def jack(num, den):
    jk = [float(np.delete(num, b, 0).sum() / np.delete(den, b, 0).sum()) for b in range(NS)]
    return float(num.sum() / den.sum()), float(np.sqrt((NS - 1) / NS * ((np.array(jk) - np.mean(jk)) ** 2).sum()))


for cls in args.progs.split(","):
    U = np.stack([program(cls, b) for b in range(NS)])
    Yt_, Xp_ = futures(Q_true, S, U), futures(Q0, np.zeros_like(S), U)
    anc = [anchor(U[b], obs[b, :GW.NC]) for b in range(NS)]
    log(f"program {cls}: futures done")
    np.savez(os.path.join(args.scratch, f"fut16_{args.cand}_{args.eta:g}_{cls}.npz"), Yt=Yt_[..., :GW.NC], Xp=Xp_[..., :GW.NC], U=U,
             anc=np.array(anc), Ya=Ya[..., :GW.NC], pop_t=LL.pop5(Yt_), pop_p=LL.pop5(Xp_), pop_a=LL.pop5(Ya), SCP=SCP)
    out["programs"][cls] = {}
    for vn, (fv, sc, roll) in VIEWS.items():
        Yt, Xp, Yc = fv(Yt_), fv(Xp_), fv(Ya)
        d = Yt.shape[-1]
        Oo = np.array([[float(energy_loo(Yt[b, :, h] / sc)) for h in HS] for b in range(NS)])
        Pl = np.array([[loo_cross(Xp[b, :, h] / sc, Yt[b, :, h] / sc) for h in HS] for b in range(NS)])
        Kk = np.array([[float(energy_fair(np.concatenate([Yc[o, :, h] for o in range(NS) if o != b]) / sc, Yt[b, :, h] / sc))
                        for h in HS] for b in range(NS)])

        def inc(Yl, b, h):
            rows = []
            for o in range(NS):
                if o != b:
                    dl = Yl[o, :, h] - Yl[o, :1, 0]
                    if roll:
                        dl = np.roll(dl.reshape(R, 3, DL.G, DL.G), (anc[b][0] - anc[o][0], anc[b][1] - anc[o][1]), axis=(2, 3)).reshape(R, d)
                    rows.append(Yt[b, 0, 0][None] + dl)
            return np.concatenate(rows) / sc
        It = np.array([[float(energy_fair(inc(Yt, b, h), Yt[b, :, h] / sc)) for h in HS] for b in range(NS)])
        Ip = np.array([[float(energy_fair(inc(Xp, b, h), Yt[b, :, h] / sc)) for h in HS] for b in range(NS)])
        scr, scr_se = jack(Pl - Oo, Kk - Oo)
        shr, shr_se = jack(Ip - It, Kk - It)
        best = np.minimum(It.mean(0), Kk.mean(0))                  # per horizon: the better of INC true and K
        out["programs"][cls][vn] = {
            "screen_pooled": scr, "screen_se_jackknife_states": scr_se,
            "screen_per_horizon": ((Pl - Oo).mean(0) / (Kk - Oo).mean(0)).tolist(),
            "surrogate_share_pooled": shr, "surrogate_share_se_jackknife_states": shr_se,
            "surrogate_share_per_horizon": ((Ip - It).mean(0) / (Kk - It).mean(0)).tolist(),
            "skill_vs_O": {"INC_true": float((Kk - It).sum() / (Kk - Oo).sum()), "INC_public": float((Kk - Ip).sum() / (Kk - Oo).sum())},
            "L_mean_per_horizon": {"O": Oo.mean(0).tolist(), "PLUG": Pl.mean(0).tolist(), "K": Kk.mean(0).tolist(),
                                   "INC_true": It.mean(0).tolist(), "INC_public": Ip.mean(0).tolist()},
            "INC_true_beats_K_at_horizons": [int(h) for h, a, k in zip(HS, It.mean(0), Kk.mean(0)) if a < k]}
        log(f"  {vn}: screen {scr:+.3f} (se {scr_se:.3f}) per h {np.round((Pl - Oo).mean(0) / (Kk - Oo).mean(0), 3).tolist()}; "
            f"surrogate share {shr:+.3f} (se {shr_se:.3f}) per h {np.round((Ip - It).mean(0) / (Kk - It).mean(0), 3).tolist()}")
    if cls != "a":
        mean_pop = {k: LL.pop5(v)[:, :, -1].mean((0, 1)).tolist() for k, v in (("true", Yt_), ("public", Xp_))}
        out["programs"][cls]["pop_mean_at_end"] = mean_pop
out["seconds"] = time.time() - t00
out["member_ticks"] = NS * RN.burn + B * Hh * (1 + 2 * len(args.progs.split(",")))
json.dump(out, open(os.path.join(DL.HERE, "results", f"views_{args.cand}_{args.eta:g}.json"), "w"), indent=1)
log("wrote")
