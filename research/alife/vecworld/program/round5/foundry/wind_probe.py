"""wind_probe -- do wind commands within a nats budget move a foundry world's block view? (CPU, seconds per world)

    python -B wind_probe.py --draws 12,345 [--prior-seed 2026] [--out results/wind_probe.json]

For each world (theta = draw `index` of the prior): 8 start states (init, 50 burn-in ticks, 100 free ticks).
From each state, 16 ticks under
    base     no command, noise key a
    twin     no command, noise key b                     -> D0(h) = |y_a - y_b|^2 / 2 (the noise floor)
    blind    a 4-tick command, random direction, B nats in total, noise key a
    aimed    a 4-tick command on the densest block (+x), B nats in total, noise key a
for B in BUDGETS. Paired effect E(h) = |y_command - y_base|^2 on the same noise (CPU runs are
bit-deterministic, so the pairing is exact), in units of the climatological variance per channel
(block view standardised with the free run), mean over states, blocks and channels.
Reported per world, program and horizon: E(h) and E(h) / (2 D0(h)) (1 = the command displaces the block
view as much as fresh noise does). E includes the chaotic growth of the displacement, not only the mean effect.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import tnca as TN  # noqa: E402
from vw.core import Noise  # noqa: E402

BUDGETS = (50.0, 200.0, 800.0)
HS = (1, 2, 4, 8, 16)
NS, T_FREE, T_RUN, T_CMD = 8, 100, 16, 4


def make_probe(fam=TN.FAM):
    NW, G = fam.NW, fam.GW

    def probe(th, key, dirs):
        ks = jax.vmap(lambda i: jax.random.fold_in(key, i))(jnp.arange(NS))
        x = jax.vmap(lambda k: TN.init(th, jax.random.fold_in(k, 1)))(ks)
        free = lambda x, k, t: jax.vmap(lambda xx, kk: TN.tick_free(th, xx, Noise(kk, t)))(x, k)
        kb = jax.vmap(lambda k: jax.random.fold_in(k, 2))(ks)
        x, _ = jax.lax.scan(lambda x, t: (free(x, kb, t), None), x, jnp.arange(50))
        kd = jax.vmap(lambda k: jax.random.fold_in(k, 3))(ks)

        def fbody(x, t):
            xn = free(x, kd, t)
            return xn, jax.vmap(TN.block_view)(xn)
        x, yf = jax.lax.scan(fbody, x, jnp.arange(T_FREE))
        mu, sd = yf.mean((0, 1, 3, 4)), jnp.sqrt(yf.var((0, 1, 3, 4)))
        # commands: (n_prog, T_CMD, NW) per state
        S = x.sum(1).reshape(NS, G, fam.H // G, G, fam.W // G).mean((2, 4)).reshape(NS, G * G)
        dense = jnp.argmax(S, 1)
        aimed = jax.vmap(lambda b: jnp.zeros((NW,)).at[G * G + b].set(1.0))(dense)             # +x on that block
        blind = dirs / jnp.sqrt((dirs ** 2).sum((-2, -1), keepdims=True))                        # (NS, T_CMD, NW)
        aim = jnp.broadcast_to(aimed[:, None], (NS, T_CMD, NW)) / jnp.sqrt(T_CMD)
        progs = [jnp.zeros((NS, T_CMD, NW)), jnp.zeros((NS, T_CMD, NW))]
        for B in BUDGETS:
            amp = jnp.sqrt(2.0 * B) * fam.sigma_w                                               # total |u| for B nats
            progs += [amp * blind, amp * aim]
        U = jnp.stack(progs, 1)                                                                  # (NS, n_prog, T_CMD, NW)
        U = jnp.concatenate([U, jnp.zeros((NS, U.shape[1], T_RUN - T_CMD, NW))], 2)
        ka = jax.vmap(lambda k: jax.random.fold_in(k, 4))(ks)
        kb2 = jax.vmap(lambda k: jax.random.fold_in(k, 5))(ks)
        nprog = U.shape[1]
        keys = jax.vmap(lambda a, b: jnp.stack([a] + [b] + [a] * (nprog - 2)))(ka, kb2)          # twin uses key b

        def one(x0, k, u):
            def body(x, tu):
                t, ut = tu
                xn = TN.tick(th, x, Noise(k, t), ut)
                return xn, TN.block_view(xn)
            return jax.lax.scan(body, x0, (jnp.arange(T_RUN), u))[1]
        Y = jax.vmap(lambda x0, kk, uu: jax.vmap(lambda k, u: one(x0, k, u))(kk, uu))(x, keys, U)   # (NS, n_prog, T, Q, G, G)
        Z = (Y - mu[:, None, None]) / jnp.maximum(sd, 1e-300)[:, None, None]
        d = jnp.mean((Z - Z[:, :1]) ** 2, (0, 3, 4, 5))                                          # (n_prog, T)
        return d, S.max(1).mean(), sd
    return jax.jit(probe)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", required=True)
    ap.add_argument("--prior-seed", type=int, default=2026)
    ap.add_argument("--out", default=os.path.join(HERE, "results", "wind_probe.json"))
    a = ap.parse_args()
    fam = TN.FAM
    probe = make_probe(fam)
    rng = np.random.default_rng(77)
    names = ["base", "twin"] + [f"{k}_{int(B)}" for B in BUDGETS for k in ("blind", "aimed")]
    out = dict(what=__doc__.split("\n")[0], prior_seed=a.prior_seed, budgets_nats=list(BUDGETS), horizons=list(HS),
               n_states=NS, command_ticks=T_CMD, sigma_w=fam.sigma_w, platform=dict(backend=jax.default_backend(),
               jax=jax.__version__, dtype="float64"), worlds=[])
    for i in [int(v) for v in a.draws.split(",")]:
        t = time.time()
        th = {k: jnp.asarray(v) for k, v in TN.draw_theta(a.prior_seed, i).items()}
        dirs = jnp.asarray(rng.normal(size=(NS, T_CMD, fam.NW)))
        d, smax, sd = probe(th, jax.random.key(1000 + i), dirs)
        d = np.asarray(d)
        hi = [h - 1 for h in HS]
        D0 = d[1][hi] / 2.0
        w = dict(draw=i, seconds=round(time.time() - t, 1), noise_floor_D0=[float(v) for v in D0], programs={})
        for j, n in enumerate(names[2:], start=2):
            E = d[j][hi]
            w["programs"][n] = dict(effect=[float(v) for v in E],
                                    effect_over_noise=[float(v) for v in E / (2.0 * D0)])
        w["base_self_difference"] = float(d[0].max())
        out["worlds"].append(w)
        print(i, "D0", np.round(D0, 4), "aimed_200", np.round(d[names.index("aimed_200")][hi], 4),
              "blind_200", np.round(d[names.index("blind_200")][hi], 4), flush=True)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
