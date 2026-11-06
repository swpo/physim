"""Fresh closure data through the VW-1 'both' world (MapWorld(specs['both'])): level 1 only, float32.

usage: python -B sim_closure.py TAG SEED J T          (TAG names the output file)
       python -B sim_closure.py probe 999 2 20         (timing + null check, small)

Per process: J designer trajectories (d.ensemble(J, seed=(SEED,)); init + 50-tick burn-in, as the
world declares), T free ticks each (no input). At each test tick t in TEST the privileged state
(x, m) of every member is cloned R-1 = 5 times with fresh noise (Ensemble.clone(fresh=True)) and
the clones run TB = 32 ticks; the base continuation is replicate 0. For the first test tick the
clones run on to TX ticks (chaos curve at long horizons). Records: L1 = <Phi_coarse, Phi_objects>
(192 + 144) every tick, and, designer-side, the tracker's slot-table extras (cy, cx, age, event,
uid per slot) + globals read from the CoarseGrain memory ('TAB'), for the identity-event split.

RecWorld = aworld.MapWorld with one extra record 'TAB' (a read of the tracker memory; the law,
the chain and the keys are untouched). Rollouts go through Designer.rollout in fixed chunks
(aworld.chunked_rollout) so each (B, T) shape compiles once.
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

OUT = "/home/user/evalwork/vecworld/vw1/fresh/closure/results"
TAG, SEED, J, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
PROBE = TAG == "probe"
R = 6
if PROBE:
    TEST, TB, TX, CH, CB = (10,), 4, 8, 10, 4
else:
    TEST, TB, TX, CH, CB = (40, 100, 160, 220), 32, 96, 10, 4
assert all(t % CH == 0 for t in TEST) and max(TEST) + TB <= T and TEST[0] + TX <= T and TB % CB == 0 and TX % CB == 0

specs, parts = AW.build()
tr, LW = parts["tracker"], parts["LW"]
HW, K, NS, NF = tr.l0.HW, tr.K, LW.NS, LW.NF


class RecWorld(AW.MapWorld):
    """MapWorld + record 'TAB': slot-table extras (K x (NS - NF)) and globals from the tracker memory."""

    def _build(self):
        super()._build()
        tick = self._tick

        def tab(c):
            mb = c.mem[0][1]                                   # chain = (pair(coarse, objects),)
            S = mb[HW:HW + K * NS].reshape(K, NS)[:, NF:].reshape(-1)
            return jnp.concatenate([S, mb[HW + K * NS:]])

        def records(c, rec):
            out = {}
            for r in rec:
                if r == "TAB":
                    out[r] = tab(c)
                elif r.startswith("L"):
                    out[r] = vw.flat(self._levels(c.x, c.mem, int(r[1:]))[-1])
                elif r == "x":
                    out[r] = vw.flat(c.x)
                else:
                    raise ValueError(r)
            return out

        def rollout(params, c, A, rec):
            def one(args):
                cb, Ab = args
                first = records(cb, rec)

                def body(cc, a):
                    cc = tick(params, cc, a)
                    return cc, records(cc, rec)
                cb, outs = jax.lax.scan(body, cb, Ab)
                return cb, {r: jnp.concatenate([first[r][None], outs[r]], 0) for r in rec}
            cB, outs = jax.lax.map(one, (c, jnp.swapaxes(A, 0, 1)), batch_size=self.batch_size)
            return cB, {r: jnp.swapaxes(v, 0, 1) for r, v in outs.items()}

        self._rollout_fn = rollout
        self._rollout = jax.jit(rollout, static_argnames=("rec",))
        self._tab = jax.jit(jax.vmap(tab))


def log(*a):
    print(f"[{time.time() - T0:8.1f}s]", *a, flush=True)


T0 = time.time()
w = RecWorld(specs["both"], world_seed=0)
d = w.designer
log("world built; n_in", w.n_in, "n_obs", w.n_obs, "TEST", TEST, "TB", TB, "TX", TX, "J", J, "T", T, "seed", SEED)
ens = d.ensemble(J, seed=(SEED,))
t_init = time.time() - T0
log("init + burn-in", J, "members")
n1 = ens.level(1).shape[1]
Y = [ens.level(1)[:, None].astype(np.float32)]
TABs = [np.asarray(w._tab(ens.carry))[:, None].astype(np.float32)]
nT = len(TEST)
B = np.zeros((J, nT, R - 1, TB, n1), np.float32)
BTAB = np.zeros((J, nT, R - 1, TB, TABs[0].shape[-1]), np.float32)
X = np.zeros((J, R - 1, TX, n1), np.float32)
timing = {"init_burn_s": t_init, "base_s": 0.0, "branch_s": 0.0, "ext_s": 0.0}
null = {}
if PROBE:   # null: two copies of the same state with the same key inside one rollout -> exactly 0
    e2 = ens.clone(rep=2, idx=[0, 1], fresh=False)
    e2, r2 = d.rollout(e2, None, T=4, rec=("L1", "x"))
    null["same_key_same_call_L1_maxabs"] = float(np.abs(r2["L1"][0::2] - r2["L1"][1::2]).max())
    null["same_key_same_call_x_maxabs"] = float(np.abs(r2["x"][0::2] - r2["x"][1::2]).max())
    e3 = ens.clone(rep=2, idx=[0, 1], fresh=True)
    e3, r3 = d.rollout(e3, None, T=4, rec=("L1", "x"))
    null["fresh_key_same_call_x_maxabs_by_tick"] = np.abs(r3["x"][0::2] - r3["x"][1::2]).max((0, 2)).tolist()
    log("null", null)
t = 0
while t < T:
    if t in TEST:
        i = TEST.index(t)
        t1 = time.time()
        br = ens.clone(rep=R - 1, fresh=True)
        br, rb = AW.chunked_rollout(d, br, TB, chunk=CB, rec=("L1", "TAB"))
        B[:, i] = rb["L1"][:, 1:].reshape(J, R - 1, TB, -1)
        BTAB[:, i] = rb["TAB"][:, 1:].reshape(J, R - 1, TB, -1)
        timing["branch_s"] += time.time() - t1
        if i == 0 and TX > TB:
            t1 = time.time()
            X[:, :, :TB] = B[:, 0]
            br, rx = AW.chunked_rollout(d, br, TX - TB, chunk=CB, rec=("L1",))
            X[:, :, TB:] = rx["L1"][:, 1:].reshape(J, R - 1, TX - TB, -1)
            timing["ext_s"] += time.time() - t1
        del br
        log("branches at tick", t, "done")
    t1 = time.time()
    ens, r = d.rollout(ens, None, T=CH, rec=("L1", "TAB"))
    Y.append(r["L1"][:, 1:].astype(np.float32))
    TABs.append(r["TAB"][:, 1:].astype(np.float32))
    timing["base_s"] += time.time() - t1
    t += CH
    if t % 50 == 0 or PROBE:
        log("tick", t)
Y = np.concatenate(Y, 1)
TABs = np.concatenate(TABs, 1)
inv = {k: np.asarray(v) for k, v in ens.invariants().items()}
timing["total_s"] = time.time() - T0
mt = {"base": J * T, "branch": J * nT * (R - 1) * TB, "ext": J * (R - 1) * (TX - TB), "burn": J * AW.BURN_TICKS}
meta = {"tag": TAG, "designer_seed": SEED, "world_seed": 0, "J": J, "T": T, "R": R, "test_ticks": list(TEST),
        "branch_ticks": TB, "ext_ticks": TX, "chunk_base": CH, "chunk_branch": CB, "n1": int(n1), "n_coarse": 192,
        "tab_cols": [f"slot{s}.{c}" for s in range(K) for c in LW.SLOT_EXTRA] +
                    ["g.next_uid", "g.births", "g.deaths", "g.fusions", "g.fissions"],
        "member_ticks": mt, "timing_s": timing, "null_check": null,
        "s_per_member_tick": {"base": timing["base_s"] / mt["base"], "branch": timing["branch_s"] / mt["branch"]},
        "final_mass_per_channel": {k: v.tolist() for k, v in inv.items()},
        "world": w.spec.name, "jax": jax.__version__, "host": os.uname().nodename}
np.savez_compressed(f"{OUT}/sim_{TAG}.npz", Y=Y, TAB=TABs, B=B, BTAB=BTAB, X=X)
json.dump(vw.jsonable(meta), open(f"{OUT}/sim_{TAG}.json", "w"), indent=1)
log("saved", f"{OUT}/sim_{TAG}.npz", json.dumps(vw.jsonable(meta["s_per_member_tick"])))
