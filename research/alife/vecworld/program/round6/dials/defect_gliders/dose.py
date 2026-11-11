"""dose -- what a designed dose-response series shows at level 1 (CPU, about 2 minutes).

For the stress-conversion candidate (xw): the designed strong push (2 x 2 blocks at the heaviest group) at
several amplitudes and durations, each inside the tick cap of 100 nats and 200 nats per episode. Observable,
computable from the block view alone: the change of the total channel-0 mass, sum over blocks of the block mean
(the public law conserves it exactly), 4 ticks after the first input tick, as a fraction of the channel-0 mass
in the pushed 2 x 2 blocks before the push. Also the same series for the mix's two operating points.
PILOT, design phase: public seeds, never an exam. Writes results/dose_<cand>.json.
"""
import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument("--cand", default="XW")
ap.add_argument("--eta", type=float, default=1.0)
ap.add_argument("--ns", type=int, default=6)
ap.add_argument("--R", type=int, default=2)
args = ap.parse_args()
t00 = time.time()
import dlaw as DL  # noqa: E402
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

GW = DL.GW
NS, R, Hh = args.ns, args.R, 4
CK = {"G": "g", "XW": "xw", "M": "m", "X": "x", "T": "t"}
P, Q, T0 = GW.base_params(), DL.qdict(**{CK[args.cand]: args.eta}), jnp.zeros((2, DL.H, DL.W))
RN = DL.DRunner()
ks = jax.random.split(jax.random.key(1000), NS)                  # the screen's states (seed 0)
A, S, m, obs = RN.init_burn(DL.rep(P, NS), DL.rep(Q, NS), T0, ks, jnp.full((NS,), DL.SIG))
A, S, obs = np.asarray(A), np.asarray(S), np.asarray(obs)
B = NS * R
kd = GW.dyn_keys(ks)
keys = jnp.stack([jax.random.fold_in(kd[b], 100 + r) for b in range(NS) for r in range(R)])
rep_s = lambda X: jnp.asarray(np.repeat(np.asarray(X), R, axis=0))
blk = DL.H // DL.G
arms = [("strong", pt, nt) for pt in (12.5, 25.0, 50.0, 100.0) for nt in (1, 2)] + [("aimed", 50.0, 4), ("regional", 75.0, 4)]
rows = []
for kind, per_tick, nt in arms:
    U, local = [], []
    for b in range(NS):
        yc, yo = obs[b, :GW.NC], obs[b, GW.NC:GW.NC + GW.NO]
        ang = np.random.default_rng([0, b, 9]).uniform(0, 2 * np.pi)
        if kind == "strong":
            u = DL.strong_push(yc, ang, ticks=nt, per_tick=per_tick, H_=Hh)
        elif kind == "aimed":
            u = GW.aimed_push(yo, 200.0, DL.SIG, H=Hh)[0]
        else:
            u = GW.regional_push(yc, ang, 300.0, DL.SIG, H=Hh)
        U.append(u)
        on = (np.abs(u.reshape(Hh, 2, DL.G, DL.G)).sum((0, 1)) > 0)                    # pushed blocks
        local.append(float((yc[:64].reshape(DL.G, DL.G) * on).sum() * blk * blk))      # channel-0 mass there
    U = np.stack(U)
    y, _, _ = RN.fut(DL.rep(P, B), DL.rep(Q, B), T0, rep_s(A), rep_s(S), keys, jnp.zeros((B,), jnp.int64), rep_s(U),
                     jnp.full((B,), DL.SIG))
    y = np.asarray(y).reshape(NS, R, Hh + 1, GW.NC)
    c0 = y[..., :64].sum(-1) * blk * blk                                               # (NS, R, Hh + 1) total c0 mass
    c1 = y[..., 64:128].sum(-1) * blk * blk
    d0 = (c0[:, :, -1] - c0[:, :, 0]).mean(1)                                          # per state
    frac = d0 / np.maximum(np.array(local), 1e-9)
    fpk = float(np.hypot(*np.asarray(DL.WD.wind_field(jnp.asarray(U[0, 0])))).max())
    rows.append({"program": kind, "nats_per_tick": per_tick, "ticks": nt, "nats": float(np.mean([GW.nats_of(u) for u in U])),
                 "peak_field": fpk, "dc0_over_local_c0_mean": float(frac.mean()), "se_states": float(frac.std(ddof=1) / np.sqrt(NS)),
                 "dc0_over_total_c0_mean": float((d0 / c0[:, 0, 0]).mean()),
                 "total_mass_change_max_abs": float(np.abs((c0 + c1)[:, :, -1] - (c0 + c1)[:, :, 0]).max())})
    print(f"[{time.time() - t00:5.0f}s]", rows[-1], flush=True)
out = {"what": "dose-response of the total channel-0 mass (a level-1 quantity the public law conserves) to designed pushes",
       "PILOT_NEVER_REUSE_AS_EXAM": True, "cand": args.cand, "eta": args.eta, "n_states": NS, "R": R, "ticks_observed": Hh,
       "trigger": {"W0": DL.W0, "full": DL.W0 + DL.DW}, "rows": rows, "seconds": time.time() - t00,
       "member_ticks": NS * 50 + len(arms) * B * Hh}
json.dump(out, open(os.path.join(DL.HERE, "results", f"dose_{args.cand}.json"), "w"), indent=1)
