"""check4 -- the vmap runner (w4.make_runners) against WindWorld's own lax.map runner, same platform.

usage: python -B check4.py [--burn]      -> $W4_OUT/check4.json
Two members (sigma_w 0.05 and 0), the same keys; WindWorld.make_init (or, without --burn, the level's
init without burn-in, to keep the CPU test short) then 3 ticks with an aimed-size wind command on
member 0. Reports max |difference| of level 1 and level 0 per tick between the runners, and the
common-random-numbers null (two copies of one state with one key in one vmap call: identical).
"""
import json
import os
import sys
import time

import numpy as np

import w4

w4.setup_paths()
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402

import wr  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

WD = wr.WD
T0 = time.time()
WW = WD.WindWorld()
PAR = WW.params
iv, rv = w4.make_runners(WW, "vmap")
im, rm = w4.make_runners(WW, "map")
run_ww = WW.make_run()
keys = member_keys(make_key(4242, 0), 2)
sig = jnp.asarray([w4.SIGMA, 0.0])
out = {"backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()]}
if "--burn" in sys.argv:
    A1, m1 = iv(PAR, keys, sig)
    A2, m2 = WW.make_init()(PAR, keys, sig)
    out["init_burn_maxabs_vmap_vs_ww"] = float(jnp.abs(A1 - A2).max())
    A, m = A2, m2
else:
    A = jax.vmap(lambda k: WW.lev0.init(PAR, jax.random.fold_in(k, WD._ST_INIT)))(keys)
    m = jax.vmap(WW.bt.init_memory)(A)
kd = jax.vmap(lambda k: jax.random.fold_in(k, WD._ST_DYN))(keys)
T = 3
uw = np.zeros((2, T, WD.NW))
uw[0, :, 5] = 0.4
t0 = jnp.zeros(2, jnp.int64)
yv, tv, gv, Av, mv = rv(PAR, A, m, kd, t0, jnp.asarray(uw), sig)
ym, tm, gm, Am, mm = rm(PAR, A, m, kd, t0, jnp.asarray(uw), sig)
yw, tw, gw, Aw, mw = run_ww(PAR, A, m, kd, t0, jnp.zeros((2, T, WD.KMAX), int), jnp.zeros((2, T, WD.KMAX)),
                           jnp.asarray(uw), sig)
d = lambda a, b: np.abs(np.asarray(a) - np.asarray(b)).max(axis=tuple(range(2, np.ndim(a)))).max(0).tolist()
out["L1_maxabs_by_tick_vmap_vs_ww"] = d(yv, yw)
out["L1_maxabs_by_tick_map_vs_ww"] = d(ym, yw)
out["table_maxabs_by_tick_vmap_vs_ww"] = d(tv, tw)
out["L0_end_maxabs_vmap_vs_ww"] = float(jnp.abs(Av - Aw).max())
out["L0_end_maxabs_map_vs_ww"] = float(jnp.abs(Am - Aw).max())
# CRN null inside one vmap call
A2, m2 = jnp.stack([A[0], A[0]]), jnp.stack([m[0], m[0]])
k2 = jnp.stack([kd[0], kd[0]])
y2, *_ = rv(PAR, A2, m2, k2, t0, jnp.asarray(np.stack([uw[0], uw[0]])), jnp.asarray([w4.SIGMA, w4.SIGMA]))
out["crn_null_L1_maxabs"] = float(np.abs(np.asarray(y2[0]) - np.asarray(y2[1])).max())
out["wind_effect_member0_L1_maxabs_by_tick"] = np.abs(np.asarray(yv[0]) - np.asarray(
    rv(PAR, A[:1], m[:1], kd[:1], t0[:1], jnp.zeros((1, T, WD.NW)), sig[:1])[0][0])).max(-1).tolist()
out["seconds"] = time.time() - T0
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(w4.out_dir(), "check4.json"), "w"), indent=1)
ok = max(out["L1_maxabs_by_tick_map_vs_ww"]) == 0.0 and out["crn_null_L1_maxabs"] == 0.0 \
    and max(out["L1_maxabs_by_tick_vmap_vs_ww"]) < 1e-6
w4.progress(f"check4 {'ok' if ok else 'FAILED'}: vmap vs ww L1 {out['L1_maxabs_by_tick_vmap_vs_ww']}")
sys.exit(0 if ok else 1)
