"""check_zero -- the zero point of the dial (CPU, about 1 minute).

Runs 2 members for 8 ticks with wind inputs that cross the trigger (so every hidden term's code path is
live) under (a) gworld.tick, the baseline public law, (b) dlaw.tick with q = None, (c) dlaw.tick with all
strengths traced and equal to zero, (d) dlaw.tick with xw = 1 (must differ). Reports the largest absolute
difference of the level-0 field and of the block view after every tick. Writes results/check_zero.json.
"""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
t00 = time.time()
import dlaw as DL  # noqa: E402
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from vw.core import Noise  # noqa: E402

GW = DL.GW
NT, B = 8, 2
p = GW.base_params()
lev0, _, _ = DL.FJ.make_level("A_gliders", DL.NOISE_STD)
pc = DL.PH.phi_coarse(DL.CFG, DL.G)
T0 = jnp.zeros((2, DL.H, DL.W))
rng = np.random.default_rng(5)
U = np.zeros((B, NT, 2, DL.G, DL.G))
for b in range(B):
    for t in range(NT):
        i, j = rng.integers(0, DL.G, 2)
        U[b, t, :, i:i + 2, j:j + 2] = 0.3 * rng.choice([-1, 1], size=(2, 1, 1))      # peak field above 0.17
U = jnp.asarray(U.reshape(B, NT, DL.NW))


def runner(kind):
    def one(args):
        k, uw, q = args
        A = lev0.init(p, jax.random.fold_in(k, 1))
        S = jnp.zeros((DL.H, DL.W))
        kp = jax.random.fold_in(k, 3)

        def body(c, x):
            A, S, t = c
            if kind == "gworld":
                A = GW.tick(p, A, Noise(kp, t), x, DL.SIG)
            elif kind == "none":
                A, S = DL.tick(p, None, T0, A, S, Noise(kp, t), x, DL.SIG)
            else:
                A, S = DL.tick(p, q, T0, A, S, Noise(kp, t), x, DL.SIG)
            return (A, S, t + 1), (A, pc.phi(A, ()))
        _, (As, ys) = jax.lax.scan(body, (A, S, 0), uw)
        return As, ys
    return jax.jit(lambda ks, U, Q: jax.lax.map(one, (ks, U, Q)))


ks = jax.random.split(jax.random.key(2024), B)
Qz, Q1 = DL.rep(DL.qdict(), B), DL.rep(DL.qdict(xw=1.0), B)
res = {}
for name, kind, Q in (("gworld", "gworld", Qz), ("q_none", "none", Qz), ("traced_zero", "traced", Qz), ("xw_1", "traced", Q1)):
    As, ys = runner(kind)(ks, U, Q)
    res[name] = (np.asarray(As), np.asarray(ys))
    print(name, f"{time.time() - t00:.0f}s", flush=True)
ref = res["gworld"]
out = {"what": "zero point of the dial: dlaw.tick against gworld.tick, 2 members x 8 ticks with inputs above the trigger; CPU float64",
       "max_abs_diff_level0_per_tick": {k: np.abs(v[0] - ref[0]).max((0, 2, 3, 4)).tolist() for k, v in res.items() if k != "gworld"},
       "max_abs_diff_block_view_per_tick": {k: np.abs(v[1] - ref[1]).max((0, 2)).tolist() for k, v in res.items() if k != "gworld"},
       "bitwise_equal_to_gworld": {k: bool(np.array_equal(v[0], ref[0])) for k, v in res.items() if k != "gworld"},
       "level0_max": float(ref[0].max()), "seconds": time.time() - t00}
json.dump(out, open(os.path.join(DL.HERE, "results", "check_zero.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
