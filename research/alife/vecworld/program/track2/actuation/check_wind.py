"""check_wind -- implementation checks of the wind variant (wind.py) -> results/check_wind.json

1. port equivalence: sigma_w = 0, no input: the variant's tick equals the port world's strided tick
   (aworld.build()['both'], MapWorld, tracker 'jax') from a saved state (states.npz #0) with the same
   member key, over 3 ticks: level 0 and level 1 (max abs difference).
2. shift structure: one tick with command u_w under background sigma_w equals one tick with no
   background and command u_w + sigma_w * eta, eta read from the same noise sub-stream: the input is
   exactly a shift of the noise variable (what the KL accounting needs).
3. KL accounting on the channel: Monte Carlo log-likelihood ratio of the realised wind sequence
   (eta drawn by the variant's own noise function, 20000 keys) for 4-tick aimed programs of 2, 12.5
   and 50 nats against the declared charge; E_0[LR] = 1 at 2 nats.
4. timing of the variant's runner (seconds per member-tick, one core).
5. basis numbers of E (field at a block centre and at a block corner for one block; background field
   SD per unit sigma_w at a point; the field of a uniform 2 x 2 / 4 x 4 group at the body).
"""
import json
import time

import jax
import jax.numpy as jnp
import numpy as np

import wind as WD
import programs as PG
from vw.core import Noise
from vw.world import make_key, member_keys

out = {}
t_all = time.time()
st = np.load("/home/user/evalwork/vecworld/vw1/fresh/inputs/results/states.npz")
X, M = st["x"], WD.host_to_jax_memory(st["m"])
WW = WD.WindWorld()
run = WW.make_run()
p = WW.params
s0 = 0
key = member_keys(make_key(8101, s0), 1)

# readout of the converted memory equals the saved level 1
y0 = np.asarray(WW.obs(jnp.asarray(X[s0]), jnp.asarray(M[s0])))
out["converted_memory_readout_vs_saved_L1_maxabs"] = float(np.abs(y0 - st["L1"][s0]).max())

# 1. port equivalence -------------------------------------------------------------------------
import aworld as AW  # noqa: E402
specs, parts = AW.build()
w = AW.MapWorld(specs["both"], world_seed=0)
d = w.designer
ens = d.from_states(jnp.asarray(X[s0:s0 + 1]), mem=(((), jnp.asarray(M[s0:s0 + 1])),), keys=key)
T = 3
ens2, r = d.rollout(ens, None, T=T, rec=("L1",))
xs_port = np.asarray(ens2.x)
L1_port = np.asarray(r["L1"])[0]
z = lambda *s: jnp.zeros(s)
res = run(p, jnp.asarray(X[s0:s0 + 1]), jnp.asarray(M[s0:s0 + 1]), key, jnp.zeros((1,), jnp.int64),
          jnp.zeros((1, T, WD.KMAX), int), z(1, T, WD.KMAX), z(1, T, WD.NW), z(1))
y, tab, glob, A_end, m_end = [np.asarray(v) for v in res]
out["port_equivalence"] = {"ticks": T, "level0_maxabs_end": float(np.abs(A_end[0] - xs_port[0]).max()),
                           "level1_maxabs_by_tick": [float(np.abs(y[0, t] - L1_port[t]).max()) for t in range(T + 1)],
                           "mass_drift_c0": float(abs(A_end[0, 0].sum() - X[s0, 0].sum())),
                           "mass_drift_c1": float(abs(A_end[0, 1].sum() - X[s0, 1].sum()))}
print("port equivalence", out["port_equivalence"], flush=True)

# 4. timing ----------------------------------------------------------------------------------
B, T = 2, 4
args = (p, jnp.asarray(X[:B]), jnp.asarray(M[:B]), member_keys(make_key(8102, 0), B), jnp.zeros((B,), jnp.int64),
        jnp.zeros((B, T, WD.KMAX), int), z(B, T, WD.KMAX), z(B, T, WD.NW), jnp.full((B,), 0.1))
t1 = time.time()
jax.block_until_ready(run(*args))
t_first = time.time() - t1
t1 = time.time()
jax.block_until_ready(run(*args))
out["timing"] = {"members": B, "ticks": T, "first_call_s": t_first, "s_per_member_tick": (time.time() - t1) / (B * T)}
print("timing", out["timing"], flush=True)

# 2. shift structure -------------------------------------------------------------------------
sig = 0.2
T_ = WW.table(jnp.asarray(M[s0]))[0]
tgt, tier = PG.pick_target(np.asarray(T_))
uw = PG.wind_aimed(np.asarray(T_), tgt, 12.5, sig)[:1]                       # first tick of a 12.5-nat program
kp = jax.random.fold_in(key[0], WD._ST_PROC)
eta = np.asarray(Noise(kp, jnp.asarray(0, jnp.int64)).stream(WD.WIND_STREAM).normal((WD.NW,)))
a_tilde = uw[0] + sig * eta
r1 = run(p, jnp.asarray(X[s0:s0 + 1]), jnp.asarray(M[s0:s0 + 1]), key, jnp.zeros((1,), jnp.int64),
         jnp.zeros((1, 1, WD.KMAX), int), z(1, 1, WD.KMAX), jnp.asarray(uw[None]), jnp.full((1,), sig))
r2 = run(p, jnp.asarray(X[s0:s0 + 1]), jnp.asarray(M[s0:s0 + 1]), key, jnp.zeros((1,), jnp.int64),
         jnp.zeros((1, 1, WD.KMAX), int), z(1, 1, WD.KMAX), jnp.asarray(a_tilde[None, None]), z(1))
r0 = run(p, jnp.asarray(X[s0:s0 + 1]), jnp.asarray(M[s0:s0 + 1]), key, jnp.zeros((1,), jnp.int64),
         jnp.zeros((1, 1, WD.KMAX), int), z(1, 1, WD.KMAX), z(1, 1, WD.NW), jnp.full((1,), sig))
out["shift_structure"] = {"sigma_w": sig, "state": s0, "target_slot": tgt,
                          "level0_maxabs_shifted_vs_command": float(np.abs(np.asarray(r1[3]) - np.asarray(r2[3])).max()),
                          "level0_maxabs_command_vs_twin": float(np.abs(np.asarray(r1[3]) - np.asarray(r0[3])).max()),
                          "charge_first_tick_nats": WD.nats(uw, sig)}
print("shift", out["shift_structure"], flush=True)

# 3. KL accounting on the channel --------------------------------------------------------------
N = 20000
keys = member_keys(make_key(8103, 0), N)
etas = jax.jit(jax.vmap(lambda k: jnp.stack([Noise(jax.random.fold_in(k, WD._ST_PROC), jnp.asarray(t, jnp.int64))
                                             .stream(WD.WIND_STREAM).normal((WD.NW,)) for t in range(PG.T_IN)])))(keys)
etas = np.asarray(etas)                                                       # (N, T_IN, NW)
kl = {}
for C in (2.0, 12.5, 50.0):
    U = PG.wind_aimed(np.asarray(T_), tgt, C, sig)                           # (T_IN, NW)
    declared = WD.nats(U, sig)
    at = U[None] + sig * etas                                                 # realised wind under P_u
    llr = ((at ** 2).sum((1, 2)) - ((at - U[None]) ** 2).sum((1, 2))) / (2 * sig ** 2)
    a0 = sig * etas                                                           # under P_0
    llr0 = ((a0 ** 2).sum((1, 2)) - ((a0 - U[None]) ** 2).sum((1, 2))) / (2 * sig ** 2)
    row = {"declared_nats": declared, "mc_E_u_logLR": float(llr.mean()), "mc_se": float(llr.std() / np.sqrt(N)),
           "mc_E_0_logLR": float(llr0.mean()), "closed_form_E_0_logLR": -declared,
           "eta_std_check": float(etas.std())}
    if C <= 2.0:
        lr0 = np.exp(llr0)
        row.update({"mc_E_0_LR": float(lr0.mean()), "mc_E_0_LR_se": float(lr0.std() / np.sqrt(N)),
                    "chi2_bound_sqrt(e^2C-1)": float(np.sqrt(np.expm1(2 * declared))),
                    "linear_gaussian_sqrt(2C)": float(np.sqrt(2 * declared))})
    kl[str(C)] = row
out["kl_channel_mc"] = {"N": N, "sigma_w": sig, "program": "wind_aimed, 4 ticks, state 0 target", "rows": kl}
print("kl", json.dumps(kl), flush=True)

# 5. basis numbers ------------------------------------------------------------------------------
g, s2 = WD.basis_profile()
b = WD.H // WD.G
U22 = np.zeros((2, WD.G, WD.G)); U22[0, 0:2, 0:2] = 1.0
U44 = np.zeros((2, WD.G, WD.G)); U44[0, 0:4, 0:4] = 1.0
f22 = np.asarray(WD.wind_field(jnp.asarray(U22)))[0]
f44 = np.asarray(WD.wind_field(jnp.asarray(U44)))[0]
out["basis"] = {"grid": f"{WD.G}x{WD.G} blocks of {b} px, 2 components", "smooth_px": WD.SMOOTH_PX,
                "one_block_field_at_own_centre": float(g[7, 7] * 0.25 + g[7, 8] * 0.25 + g[8, 7] * 0.25 + g[8, 8] * 0.25),
                "one_block_field_at_own_corner": float(g[15, 15]),
                "background_field_sd_per_sigma_w": {"min": float(np.sqrt(s2.min())), "max": float(np.sqrt(s2.max())),
                                                    "mean_var_sqrt": float(np.sqrt(s2.mean()))},
                "random_walk_px_per_tick_per_sigma_w": float(4 * np.sqrt(s2.mean())),
                "group2x2_field_at_group_centre": float(f22[15:17, 15:17].mean()),
                "group2x2_field_at_inner_block_centre": float(f22[7:9, 7:9].mean()),
                "group4x4_field_at_centre": float(f44[31:33, 31:33].mean()),
                "uniform_field_check": float(np.asarray(WD.wind_field(jnp.ones((2, WD.G, WD.G)))).std())}
out["seconds"] = time.time() - t_all
json.dump(out, open(f"{WD.RES}/check_wind.json", "w"), indent=1)
print(json.dumps(out["basis"]), "\nseconds", out["seconds"], flush=True)
