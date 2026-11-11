"""screen -- the round-5 screen at tiny size for one candidate hidden term (CPU, a few minutes per call).

For n_s hidden states (init + 50-tick burn-in under the TRUE law, no input) and for each input program:
    Y  R replicate futures under the true law (public law + the hidden term at strength eta)
    X  R futures under the PUBLIC law from the same hidden state, same noise keys (common random numbers)
scored on the block view (192 numbers / public scales SC1, RMS norm), horizons hs:
    O     leave-one-out fair energy score of the truths (vw.scoring.energy_loo): the oracle
    PLUG  the public-law simulator from the hidden state: for truth r the ensemble is the public members
          with keys != r (R - 1 members, independent of y_r; same size as the oracle's ensemble), fair
    K     climatology: the other states' true-law no-input futures at the same horizon (vw.scoring.energy_fair)
    screen = (PLUG - O) / (K - O)  (= 1 - OES of the state-given public-law plug-in; round 5: 0.13-0.35
    for hidden parameters, ladder README table column plugPM)
    pair  mean RMS distance between the true and the public future with the SAME noise (0 = invisible)
Programs: a none; c the exam mix's aimed push (200 nats); d the mix's regional push (300 nats);
s designed strong push (200 nats); q designed squeeze (200 nats).
Public-law futures are cached by (state, program, keys) in the scratch directory.
PILOT, design phase: public seeds, nothing here is or may become an exam.

Run: python -B screen.py --cand XW --eta 1 --progs a,c,d,s
"""
import argparse
import hashlib
import json
import os
import sys
import time

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument("--cand", required=True, help="G, XW, M, X, T or PAR (hidden parameter lR, calibration arm)")
ap.add_argument("--eta", type=float, default=1.0)
ap.add_argument("--progs", default="a,c,d,s")
ap.add_argument("--ns", type=int, default=6)
ap.add_argument("--R", type=int, default=5)
ap.add_argument("--H", type=int, default=8)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--tag", default="")
ap.add_argument("--scratch", default="/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dials_defect_gliders")
args = ap.parse_args()
t00 = time.time()
import dlaw as DL  # noqa: E402
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from vw.scoring import energy_fair, energy_loo, _pd  # noqa: E402

GW = DL.GW
NS, R, Hh = args.ns, args.R, args.H
HS = [h for h in (1, 2, 4, 8, 12, 16) if h <= Hh]
CK = {"G": "g", "XW": "xw", "M": "m", "X": "x", "T": "t"}
PROGS = args.progs.split(",")
if "a" not in PROGS:
    PROGS = ["a"] + PROGS
os.makedirs(args.scratch, exist_ok=True)


def log(*a):
    print(f"[{time.time() - t00:6.0f}s]", *a, flush=True)


def loo_cross(X, Y):
    """For each truth r: fair energy score of the ensemble {x_i, i != r} at y_r; mean over r. X, Y (R, d)."""
    Rn = Y.shape[0]
    Dxy, Dxx = _pd(X, Y), _pd(X, X)
    m = Rn - 1
    out = []
    for r in range(Rn):
        keep = np.arange(Rn) != r
        t1 = Dxy[keep, r].mean()
        t2 = Dxx[np.ix_(keep, keep)].sum() / (2.0 * m * (m - 1))
        out.append(t1 - t2)
    return float(np.mean(out))


# ----------------------------------------------------------------------------- laws
P_pub = GW.base_params()
Q0 = DL.qdict()
T0 = jnp.zeros((2, DL.H, DL.W))
if args.cand == "PAR":
    P_true, Q_true, T_true = GW.theta_to_params({"lR": 1.0 + 0.06 * args.eta}), Q0, T0
else:
    P_true, Q_true = P_pub, DL.qdict(**{CK[args.cand]: args.eta})
    T_true = jnp.asarray(DL.terrain(args.seed)) if args.cand == "T" else T0
RN = DL.DRunner()
ks = jax.random.split(jax.random.key(1000 + args.seed), NS)
sig1 = jnp.full((NS,), DL.SIG)
A, S, m, obs = RN.init_burn(DL.rep(P_true, NS), DL.rep(Q_true, NS), T_true, ks, sig1)
A, S, obs = np.asarray(A), np.asarray(S), np.asarray(obs)
log("burn done; S max per state", np.round(S.max((1, 2)), 4).tolist())
mass0 = A.sum((2, 3))                                           # (NS, 2)


def program(cls, b):
    rng = np.random.default_rng([args.seed, b, ord(cls)])
    yc, yo = obs[b, :GW.NC], obs[b, GW.NC:GW.NC + GW.NO]
    if cls == "a":
        return np.zeros((Hh, DL.NW))
    if cls == "c":
        return GW.aimed_push(yo, 200.0, DL.SIG, H=Hh)[0]
    if cls == "d":
        return GW.regional_push(yc, rng.uniform(0, 2 * np.pi), 300.0, DL.SIG, H=Hh)
    if cls == "s":
        return DL.strong_push(yc, rng.uniform(0, 2 * np.pi), H_=Hh)
    if cls == "q":
        return DL.squeeze(yc, H_=Hh)
    raise KeyError(cls)


B = NS * R
kd = GW.dyn_keys(ks)
keys = jnp.stack([jax.random.fold_in(kd[b], 100 + r) for b in range(NS) for r in range(R)])
sigB = jnp.full((B,), DL.SIG)
t0B = jnp.zeros((B,), jnp.int64)
rep_s = lambda X: jnp.asarray(np.repeat(np.asarray(X), R, axis=0))


def futures(P, Q, T, S_, U):
    y, A_end, S_end = RN.fut(DL.rep(P, B), DL.rep(Q, B), T, rep_s(A), rep_s(S_), keys, t0B, rep_s(U), sigB)
    return np.asarray(y).reshape(NS, R, Hh + 1, GW.NC), np.asarray(A_end).reshape((NS, R) + A.shape[1:])


def public_futures(U):
    """Per-state cache: the public ensemble depends on the state, the program and the keys only."""
    hs = [hashlib.sha1(A[b].tobytes() + U[b].tobytes() + f"{R},{Hh},{args.seed},{b}".encode()).hexdigest()[:16] for b in range(NS)]
    fs = [os.path.join(args.scratch, f"pub_{h}.npz") for h in hs]
    if all(os.path.exists(f) for f in fs):
        d = [np.load(f) for f in fs]
        return np.stack([x["y"] for x in d]), np.stack([x["m"] for x in d]), True
    y, A_end = futures(P_pub, Q0, T0, np.zeros_like(S), U)
    mass = A_end.sum((3, 4))
    for b, f in enumerate(fs):
        np.savez(f, y=y[b].astype(np.float64), m=mass[b])
    return y, mass, False


out = {"what": "round-5 screen at tiny size, block view; see screen.py docstring",
       "PILOT_NEVER_REUSE_AS_EXAM": True,
       "cand": args.cand, "eta": args.eta, "config": {"n_states": NS, "R": R, "H": Hh, "hs": HS, "seed": args.seed,
                                                     "constants": {k: getattr(DL, k) for k in ("W0", "DW", "KXW", "KON", "TAU", "A0", "DA", "KX", "T_RMS", "T_CORR")}},
       "burn": {"S_max": float(S.max()), "mass_c0_c1_per_state": mass0.tolist()}, "programs": {}}
Ytrue = {}
for cls in PROGS:
    U = np.stack([program(cls, b) for b in range(NS)])
    Yt, At = futures(P_true, Q_true, T_true, S, U)
    Xp, mp, hit = public_futures(U)
    Ytrue[cls] = Yt
    log(f"program {cls}: futures done (public cache {'hit' if hit else 'miss'})")
    sc = DL.SC1
    Oo = np.array([[float(energy_loo(Yt[b, :, h] / sc)) for h in HS] for b in range(NS)])
    Pl = np.array([[loo_cross(Xp[b, :, h] / sc, Yt[b, :, h] / sc) for h in HS] for b in range(NS)])
    Ya = Ytrue["a"]
    Kk = np.array([[float(energy_fair(np.concatenate([Ya[o, :, h] for o in range(NS) if o != b]) / sc, Yt[b, :, h] / sc))
                    for h in HS] for b in range(NS)])
    pair = np.array([[float(np.sqrt((((Yt[b, :, h] - Xp[b, :, h]) / sc) ** 2).mean(-1)).mean()) for h in HS] for b in range(NS)])
    num, den = Pl - Oo, Kk - Oo
    pooled = float(num.sum() / den.sum())
    jk = [float(np.delete(num, b, 0).sum() / np.delete(den, b, 0).sum()) for b in range(NS)]
    se = float(np.sqrt((NS - 1) / NS * ((np.array(jk) - np.mean(jk)) ** 2).sum()))
    cellmean = float((num.mean(0) / den.mean(0)).mean())
    mt = At.sum((3, 4))                                         # (NS, R, 2) final masses, true law
    out["programs"][cls] = {
        "nats_per_state": [GW.nats_of(u) for u in U],
        "screen_pooled": pooled, "screen_pooled_se_jackknife_states": se, "screen_cellmean": cellmean,
        "screen_per_horizon": (num.mean(0) / den.mean(0)).tolist(),
        "screen_per_state": (num.sum(1) / den.sum(1).mean()).tolist(),
        "pair_rms_per_horizon": pair.mean(0).tolist(), "pair_rms_max": float(pair.max()),
        "L_mean_per_horizon": {"O": Oo.mean(0).tolist(), "PLUG": Pl.mean(0).tolist(), "K": Kk.mean(0).tolist()},
        "c0_mass_change_frac_true_mean_per_state": ((mt[:, :, 0].mean(1) - mass0[:, 0]) / mass0[:, 0]).tolist(),
        "c0_mass_change_frac_public_max_abs": float(np.abs((mp[:, :, 0] - mass0[:, None, 0]) / mass0[:, None, 0]).max()),
        "m2_mean_end_true_over_public": float(Yt[:, :, -1, 128:].mean() / Xp[:, :, -1, 128:].mean()),
        "public_cache_hit": hit}
    log(f"  screen pooled {pooled:+.3f} (se {se:.3f}), cell mean {cellmean:+.3f}, pair rms {pair.mean(0).round(3).tolist()}, "
        f"dc0 {np.mean(out['programs'][cls]['c0_mass_change_frac_true_mean_per_state']):+.4f}")
out["seconds"] = time.time() - t00
out["member_ticks"] = NS * RN.burn + len(PROGS) * B * Hh * 2
name = f"screen_{args.cand}_{args.eta:g}{args.tag}.json"
json.dump(out, open(os.path.join(DL.HERE, "results", name), "w"), indent=1)
log("wrote", name)
