"""check_lib -- CPU checks of vxlib (a few CPU-minutes at 64^2).

  1. Runner at the default parameters against the vw World of track1/vortex_world (vortex_world.build with
     mut_dt = 200 at 64^2 = mut128 50): same member keys, T ticks crossing the labelling (tick 60) and the first
     mutation (t = 400, tick 80). Compared: the level-1 vortex list at every tick and level 2.
     Both batching paths of the Runner are run: lax.map of single-member ticks (CPU default) and the batch tick
     with the batch-level mutation cond (the GPU path).
  2. A member with mut128 = 25 mutates at t = 400 (64^2: every 100) -- the per-member mutation interval works
     and differs from the default member.
  3. level2 / summaries / raster shapes; the program mix costs what it says.
usage: python -B check_lib.py [T]     -> results/check_lib.json
"""
import json
import os
import sys
import time

import vxlib as VX

import jax
import jax.numpy as jnp
import numpy as np

from vw.world import make_key, member_keys

VJ, VW = VX.VJ, VX.VW
T = int(sys.argv[1]) if len(sys.argv) > 1 else 84
H, B = 64, 2
out = {"T": T, "H": H, "B": B, "backend": jax.default_backend(), "jax": jax.__version__}

# reference: the vw World
t0 = time.time()
cfg = VJ.Config(H=H, W=H, G=H // 16, mut_dt=200.0)
specs, parts = VW.build(cfg)
w = VW.MapWorld(specs["kinds"], world_seed=0, params={k: jnp.asarray(v, jnp.float64) for k, v in VJ.THETA.items()})
ens = w.designer.ensemble(B, seed=11)
_, r = w.designer.rollout(ens, T=T, rec=("L1", "L2"))
L1_ref, L2_ref = np.asarray(r["L1"]), np.asarray(r["L2"])
out["ref_seconds"] = time.time() - t0
ki = member_keys(make_key(3, 0, 11), B)                 # Designer.ensemble: make_key(_NS_DESIGNER, world_seed, seed)

res = {}
for name, cpu_map in (("map", True), ("batch", False)):
    t0 = time.time()
    RN = VX.Runner(H, cpu_map=cpu_map)
    Q = VX.theta_batch(B)
    X, M, Y1 = RN.rollout(Q, ki, T, chunk=T)
    X0, M0 = RN.init(Q, ki)
    y0 = np.asarray(jax.vmap(lambda m: RN.bt.phi(None, m))(M0))
    Y = np.concatenate([y0[:, None], Y1], 1)
    d1 = float(np.abs(Y - L1_ref.astype(np.float32)).max())
    L2 = VX.level2(Y, RN.K)
    d2 = float(np.abs(L2 - L2_ref).max())
    res[name] = {"max_abs_diff_L1": d1, "max_abs_diff_L2": d2, "seconds": time.time() - t0,
                 "s_b_end": L2[:, -1, 1].tolist(), "N_end": L2[:, -1, 0].tolist(),
                 "a_sum": float(np.asarray(X["a"]).sum()), "b_sum": float(np.asarray(X["b"]).sum())}
    print(name, res[name], flush=True)
out["default_vs_vw_world"] = res
out["ref_s_b_end"] = L2_ref[:, -1, 1].tolist()
out["ref_b_present"] = bool((L1_ref[..., 2::12] > 0).any())

# 2. per-member mutation interval
RN = VX.Runner(H)
Q = VX.theta_batch(B, mut128=np.array([50.0, 25.0]))
k2 = jnp.stack([ki[0], ki[0]])
X, M, Y1 = RN.rollout(Q, k2, T, chunk=T)
bs = np.asarray(X["b"]).sum((1, 2))
fb = VX.summaries(Y1, RN.K)[:, :, 2]
out["mut128"] = {"values": [50.0, 25.0], "b_sum_end": bs.tolist(),
                 "first_tick_with_b": [int(np.argmax(f > 0)) + 1 if (f > 0).any() else None for f in fb],
                 "expect": "64^2: mut128 50 -> first mutation at t 400 (tick 80, list after tick 81); 25 -> t 400 too "
                           "(every 100: 400 is the first multiple after the labelling step unless the labelling "
                           "step itself mutates), then t 500"}
print(out["mut128"], flush=True)

# 3. shapes and costs
S = VX.summaries(Y1, RN.K)
R = VX.raster(Y1, RN.K, H)
assert S.shape == (B, T, len(VX.S1_NAMES)) and R.shape == (B, T, 2 * (H // 16) ** 2)
mass = np.where(Y1.reshape(B, T, RN.K, 12)[..., 0] > 0.5, Y1.reshape(B, T, RN.K, 12)[..., 1], 0).sum(-1)
assert np.allclose(R[..., :(H // 16) ** 2].sum(-1), mass, rtol=1e-5), "raster mass"
rng = np.random.default_rng(0)
costs = {}
for c in VX.PROGRAM_CLASSES:
    U = VX.make_program(c, rng, Y1[0, -1], RN.K, H, 8, 200.0, RN.centres)
    costs[c] = float(VX.nats_of(U))
out["program_costs_at_200_nats"] = costs
assert costs["a"] == 0 and all(abs(costs[c] - 200) < 1e-6 for c in "bcd"), costs
ok = all(v["max_abs_diff_L1"] < 1e-3 and v["max_abs_diff_L2"] == 0 for v in res.values())
out["pass"] = bool(ok)
os.makedirs(os.path.join(VX.HERE, "results"), exist_ok=True)
json.dump(out, open(os.path.join(VX.HERE, "results", "check_lib.json"), "w"), indent=1)
print("PASS" if ok else "FAIL", flush=True)
sys.exit(0 if ok else 1)
