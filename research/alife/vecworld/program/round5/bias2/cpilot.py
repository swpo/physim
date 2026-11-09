"""cpilot -- CPU look at a world's block-variable time scales before the GPU job (study `bias2`).

usage: python -B cpilot.py J T [burn]        (B5_WORLD; public default parameters; designer seed 9700, never
                                              reused: the study's halves use c5.SEEDS)
J members of the world's 'pooled' spec, burn-in, then T world ticks; block means (16 px) of every c = 1 base
feature are recorded each tick. Prints and saves the block autocorrelation at lags 1..64 world ticks (pooled over
blocks, global standardisation: 2 rho - 1 approximates the persistence closure ceiling when the oracle spread is
small) -> results/pilot_<world>.json. Used to choose the study tick of each world (c5.STRIDE).
"""
import json
import os
import sys
import time

import numpy as np

os.environ.setdefault("B5_PILOT", "1")
import c5

c5.setup_paths(world=True)
import jax  # noqa: E402

jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402

import chand as CHD  # noqa: E402
import csim  # noqa: E402

J, T = int(sys.argv[1]), int(sys.argv[2])
BURN = int(sys.argv[3]) if len(sys.argv) > 3 else 100
LAGS = [1, 2, 4, 8, 16, 32, 64]
t0 = time.time()
w, desc = csim.build_world(stride=1)
d = w.designer
ens = d.ensemble(J, seed=(9700,))
done = 0
while done < BURN:
    n = min(10, BURN - done)
    ens, _ = d.rollout(ens, None, T=n, rec=())
    done += n
    print(f"burn {done}/{BURN} {time.time() - t0:.0f}s", flush=True)
pf = CHD.pixel_features(c5.WORLD)
names = list(c5.BASE1)
pool = jax.jit(lambda x: CHD.pool(jnp.stack([pf(x)[n] for n in names], 1), 0))
F = []
t = 0
while t < T:
    ens, r = d.rollout(ens, None, T=8, rec=("x",))
    x = csim.fields_of(r["x"][:, (0 if t == 0 else 1):])                # (J, n, C, 128, 128)
    F.append(np.asarray(pool(jnp.asarray(x.reshape((-1,) + x.shape[2:]))), np.float64).reshape(J, -1, len(names), 64))
    t += 8
    print(f"tick {t}/{T} {time.time() - t0:.0f}s", flush=True)
F = np.concatenate(F, 1)                                                 # (J, T+1, nf, 64)
out = {"world": c5.WORLD, "J": J, "T": T, "burn": BURN, "designer_seed": 9700, "tick_time": desc["tick_time"],
       "lags_world_ticks": LAGS, "block_autocorr": {}, "seconds": time.time() - t0,
       "member_ticks": J * (BURN + T), "platform": {"backend": jax.default_backend(), "jax": jax.__version__}}
qt = [0, F.shape[1] // 4, F.shape[1] // 2, 3 * F.shape[1] // 4, F.shape[1] - 1]
out["box_mean_at_ticks"] = {"ticks": qt, "per_member": {n: F[:, qt, i].mean(-1).tolist() for i, n in enumerate(names)}}
for i, n in enumerate(names):
    Z = F[:, :, i]
    Zs = (Z - Z.mean()) / Z.std()
    out["block_autocorr"][n] = [float(np.mean(Zs[:, :-L] * Zs[:, L:])) if L < Z.shape[1] else None for L in LAGS]
    print(n, [None if v is None else round(v, 3) for v in out["block_autocorr"][n]], "box mean",
          np.round(F[:, qt, i].mean((0, 2)), 4).tolist())
os.makedirs(os.path.join(c5.HERE, "results"), exist_ok=True)
json.dump(out, open(os.path.join(c5.HERE, "results", f"pilot_{c5.WORLD}.json"), "w"), indent=1)
