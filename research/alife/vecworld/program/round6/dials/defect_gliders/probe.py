"""probe -- constants behind the candidates (CPU, about 2 minutes): the background wind field, the peak fields
of the exam mix's programs and of the designed probes, how often the triggers fire without inputs, and the
speed of the tick with and without the tracker. Writes results/probe.json.
Run: OMP_NUM_THREADS=1 nice -n 10 python -B probe.py
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

GW, WD = DL.GW, DL.WD
out = {"what": "constants behind the candidate hidden terms; CPU; command: python -B probe.py"}
# background field: per component sd at a point = sigma_w sqrt(sum_b g_b(p)^2)
g, s2 = WD.basis_profile()
sd = DL.SIG * np.sqrt(s2)
rng = np.random.default_rng(0)
mags = []
for _ in range(400):
    E = np.asarray(WD.wind_field(jnp.asarray(DL.SIG * rng.standard_normal(DL.NW))))
    mags.append(np.hypot(E[0], E[1]))
mags = np.stack(mags)
out["background"] = {"sd_per_component_min_max": [float(sd.min()), float(sd.max())],
                     "magnitude_percentiles_50_99_99.99_max_over_400_ticks": [float(v) for v in np.percentile(mags, [50, 99, 99.99, 100])],
                     "frac_points_above_W0": float((mags > DL.W0).mean()),
                     "ticks_with_any_point_above_W0_of_400": int((mags.max((1, 2)) > DL.W0).sum()),
                     "W0": DL.W0, "DW": DL.DW}


def peak(U):
    E = np.asarray(WD.wind_field(jnp.asarray(U)))
    m = np.hypot(E[0], E[1])
    return float(m.max()), float((m > DL.W0).mean()), float((m > DL.W0 + DL.DW).mean())


yc = np.zeros(192)
yc[128 + 3 * 8 + 3] = 1.0
yo = np.zeros(144)
yo[0:12] = [1, 100, 0, 1, 0, 1, 0, 3, 0, 0, 1.0, 0.0]        # one body, speed 1 along x
progs = {"mix_aimed_200": GW.aimed_push(yo, 200.0, H=8)[0], "mix_regional_300": GW.regional_push(yc, 0.3, 300.0, H=8),
         "designed_strong_200": DL.strong_push(yc, 0.3), "designed_squeeze_200": DL.squeeze(yc)}
out["programs"] = {}
for k, U in progs.items():
    pk = peak(U[0])
    out["programs"][k] = {"nats": GW.nats_of(U), "nats_tick0": GW.nats_of(U[0]), "max_coefficient": float(np.abs(U).max()),
                          "peak_field": pk[0], "frac_area_above_W0": pk[1], "frac_area_full_trigger": pk[2],
                          "ticks_with_input": int((np.abs(U).sum(1) > 0).sum())}
# speed: burn with tracker, futures without
RN = DL.DRunner(burn=10)
P1 = DL.rep(GW.base_params(), 2)
Q0 = DL.rep(DL.qdict(), 2)
T0 = jnp.zeros((2, DL.H, DL.W))
ks = jax.random.split(jax.random.key(11), 2)
sig = jnp.full((2,), DL.SIG)
t = time.time()
A, S, m, obs = RN.init_burn(P1, Q0, T0, ks, sig)
A.block_until_ready()
t1 = time.time() - t
t = time.time()
A, S, m, obs = RN.init_burn(P1, Q0, T0, jax.random.split(jax.random.key(12), 2), sig)
A.block_until_ready()
t2 = time.time() - t
uw = jnp.zeros((2, 10, DL.NW))
kd = GW.dyn_keys(ks)
t = time.time()
y, A2, S2 = RN.fut(P1, Q0, T0, A, S, kd, jnp.zeros((2,), jnp.int64), uw, sig)
y.block_until_ready()
t3 = time.time() - t
t = time.time()
y, A2, S2 = RN.fut(P1, Q0, T0, A, S, kd, jnp.zeros((2,), jnp.int64), uw, sig)
y.block_until_ready()
t4 = time.time() - t
out["speed_one_thread"] = {"burn_with_tracker_ticks_per_s": 20 / t2, "burn_compile_s": t1 - t2,
                           "future_block_view_ticks_per_s": 20 / t4, "future_compile_s": t3 - t4}
out["seconds"] = time.time() - t00
os.makedirs(os.path.join(DL.HERE, "results"), exist_ok=True)
json.dump(out, open(os.path.join(DL.HERE, "results", "probe.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
