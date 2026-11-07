"""Replay of saved episodes with the JAX tracker (aworld.build(tracker='jax')).

usage: python -B replay.py hero [host]   -> replay_hero[_host].json
       python -B replay.py closure [jax|host] [B]   -> replay_closure[_host]_B<B>.json

hero     the page's hero episode: MapWorld(specs['objects'], world_seed=0), o = w.reset(0), then
         o = w.step(None) x 300 (exactly fresh/media/scripts/hero_run.py). Compared with
         fresh/media/results/hero_objects_s0.npz: agent observations (obs64) bit for bit, designer
         level 1 (L1), level 0 (x, stored float32), tracker extras (tab: cy, cx, age, event, uid) and
         globals (glob). 'host' replays with the VW-0 tracker instead (control).
closure  members 0-3 of fresh/closure/results/sim_A.npz: MapWorld(specs['both'], world_seed=0),
         d.ensemble(B, seed=(301,)) (member keys do not depend on B), level 1 for the first 50 ticks
         (rollouts of 10 ticks, as sim_closure.py), and the tracker extras + globals ('TAB'); the saved
         arrays are float32, so values are compared after casting to float32. B = 18 is the layout
         sim_closure.py compiled (its own re-run check used the same layouts); members 0-3 are compared.
"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: E402,F401
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
import aworld as AW  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
FRESH = "/home/user/evalwork/vecworld/vw1/fresh"
what = sys.argv[1]
kind = sys.argv[2] if len(sys.argv) > 2 else "jax"
T0 = time.time()
specs, parts = AW.build(tracker=kind)
tr, LW = parts["tracker"], parts["LW"]
HW, K, NS, NF = 128 * 128, tr.K, LW.NS, LW.NF


def bitwise_equal(a, b):
    a, b = np.ascontiguousarray(a, np.float64), np.ascontiguousarray(b, np.float64)
    return bool(a.shape == b.shape and np.array_equal(a.view(np.int64), b.view(np.int64)))


if what == "hero":
    S = np.load(f"{FRESH}/media/results/hero_objects_s0.npz")
    w = AW.MapWorld(specs["objects"], world_seed=0)
    d = w.designer
    obs, L1, X, TAB, GLOB = [], [], [], [], []

    def record(o):
        st = d.state()
        m = np.asarray(st["mem"][0])
        obs.append(np.asarray(o, float))
        L1.append(np.asarray(st["observed"], float))
        X.append(np.asarray(st["x"], np.float32))
        TAB.append(m[HW:HW + K * NS].reshape(K, NS)[:, NF:].copy())
        GLOB.append(m[HW + K * NS:HW + K * NS + 5].copy())
    record(w.reset(0))
    for t in range(300):
        record(w.step(None))
    obs, L1, X, TAB, GLOB = map(np.array, (obs, L1, X, TAB, GLOB))
    disc = [2, 3, 4]                                              # age, event, uid
    res = {"episode": "objects world, world_seed 0, reset(0), step(None) x 300", "tracker": kind,
           "keys_in_saved_npz": list(S.files),
           "obs_bit_identical_to_saved_obs64": bitwise_equal(obs, S["obs64"]),
           "obs_equal_to_saved_obs64": bool(np.array_equal(obs, S["obs64"])),
           "obs_coords_differing": int((obs != S["obs64"]).sum()), "obs_coords": int(obs.size),
           "obs_float32_equal_to_saved_obs": bool(np.array_equal(obs.astype(np.float32), S["obs"])),
           "out_map_equal": bool(np.array_equal(w.out_map, S["out_map"])),
           "L1_max_abs_diff": float(np.abs(L1 - S["L1"]).max()),
           "L1_entries_not_bit_identical": int((L1 != S["L1"]).sum()), "L1_entries": int(L1.size),
           "x_float32_equal": bool(np.array_equal(X, S["x"])),
           "tab_discrete_equal": bool(np.array_equal(TAB[..., disc], S["tab"][..., disc])),
           "tab_centroid_max_abs_diff": float(np.abs(TAB[..., :2] - S["tab"][..., :2]).max()),
           "glob_equal": bool(np.array_equal(GLOB, S["glob"])),
           "events_over_episode": dict(zip(["births", "deaths", "fusions", "fissions"],
                                           (GLOB[-1, 1:] - GLOB[0, 1:]).tolist())),
           "wall_s": time.time() - T0}
elif what == "closure":
    S = np.load(f"{FRESH}/closure/results/sim_A.npz")
    Y0, TAB0 = S["Y"][:4, :51], S["TAB"][:4, :51]

    class RecWorld(AW.MapWorld):
        def _build(self):
            super()._build()
            tick = self._tick

            def records(c):
                mb = c.mem[0][1]
                tab = jnp.concatenate([mb[HW:HW + K * NS].reshape(K, NS)[:, NF:].reshape(-1),
                                       mb[HW + K * NS:HW + K * NS + 5]])
                return {"L1": vw.flat(self._levels(c.x, c.mem, 1)[-1]), "TAB": tab}

            def rollout(params, c, A, rec):
                def one(args):
                    cb, Ab = args
                    first = records(cb)

                    def body(cc, a):
                        cc = tick(params, cc, a)
                        return cc, records(cc)
                    cb, outs = jax.lax.scan(body, cb, Ab)
                    return cb, {r: jnp.concatenate([first[r][None], outs[r]], 0) for r in ("L1", "TAB")}
                cB, outs = jax.lax.map(one, (c, jnp.swapaxes(A, 0, 1)), batch_size=self.batch_size)
                return cB, {r: jnp.swapaxes(v, 0, 1) for r, v in outs.items()}
            self._rollout_fn = rollout
            self._rollout = jax.jit(rollout, static_argnames=("rec",))

    w = RecWorld(specs["both"], world_seed=0)
    d = w.designer
    NB = int(sys.argv[3]) if len(sys.argv) > 3 else 18
    ens = d.ensemble(NB, seed=(301,))
    Y, TB = [], []
    for c in range(5):
        ens, r = d.rollout(ens, None, T=10, rec=("L1", "TAB"))
        Y.append(r["L1"] if c == 0 else r["L1"][:, 1:])
        TB.append(r["TAB"] if c == 0 else r["TAB"][:, 1:])
    Y, TB = np.concatenate(Y, 1)[:4], np.concatenate(TB, 1)[:4]
    dc = np.abs(Y[..., :192] - Y0[..., :192].astype(np.float64)).max((0, 2))
    do = np.abs(Y[..., 192:] - Y0[..., 192:].astype(np.float64)).max((0, 2))
    Y32, TB32 = Y.astype(np.float32), TB.astype(np.float32)
    ext = TB32[..., :K * 5].reshape(4, 51, K, 5)
    ext0 = TAB0[..., :K * 5].reshape(4, 51, K, 5)
    res = {"data": "sim_A.npz members 0-3, ticks 0..50 of level 1 (192 coarse + 144 objects)", "tracker": kind,
           "designer_seed": 301, "world_seed": 0, "ensemble_size": NB, "members_compared": [0, 1, 2, 3],
           "coarse_max_abs_diff_by_tick": dc.tolist(), "objects_max_abs_diff_by_tick": do.tolist(),
           "L1_float32_equal": bool(np.array_equal(Y32, Y0)), "L1_entries_differing_float32": int((Y32 != Y0).sum()),
           "L1_entries": int(Y0.size),
           "objects_part_float32_equal": bool(np.array_equal(Y32[..., 192:], Y0[..., 192:])),
           "coarse_part_float32_equal": bool(np.array_equal(Y32[..., :192], Y0[..., :192])),
           "L1_max_abs_diff_vs_float32": float(np.abs(Y - Y0.astype(np.float64)).max()),
           "tab_age_event_uid_equal": bool(np.array_equal(ext[..., 2:], ext0[..., 2:])),
           "tab_centroid_float32_equal": bool(np.array_equal(ext[..., :2], ext0[..., :2])),
           "globals_equal": bool(np.array_equal(TB32[..., K * 5:], TAB0[..., K * 5:])),
           "wall_s": time.time() - T0}
else:
    raise SystemExit(__doc__)
name = f"replay_{what}" + ("" if kind == "jax" else f"_{kind}") + (f"_B{NB}" if what == "closure" else "")
json.dump(res, open(f"{OUT}/{name}.json", "w"), indent=1)
print(json.dumps(res, indent=1))
