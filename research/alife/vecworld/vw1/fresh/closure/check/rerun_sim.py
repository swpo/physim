"""Checker: re-run sim_A (designer seed 301, J = 18) from scratch through the VW-1 'both' world for
ticks 0..50 of the base run and the first 4 ticks of the tick-40 fresh-noise clones, and compare
bit for bit with results/sim_A.npz (same compiled layouts: base B=18 T=10, clones B=90 T=4).
RecWorld is copied verbatim from scripts/sim_closure.py (that file runs at import)."""
import json, sys, time
sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa
import jax, jax.numpy as jnp, numpy as np
import vw
import aworld as AW
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.1f}s]", *a, flush=True)
specs, parts = AW.build()
tr, LW = parts["tracker"], parts["LW"]
HW, K, NS, NF = tr.l0.HW, tr.K, LW.NS, LW.NF

class RecWorld(AW.MapWorld):
    def _build(self):
        super()._build()
        tick = self._tick
        def tab(c):
            mb = c.mem[0][1]
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

S = np.load("/home/user/evalwork/vecworld/vw1/fresh/closure/results/sim_A.npz")
Y, TAB, B = S["Y"], S["TAB"], S["B"]
w = RecWorld(specs["both"], world_seed=0); d = w.designer
ens = d.ensemble(18, seed=(301,))
log("init+burn done")
res = {"world": w.spec.name, "L1_tick0_maxabs": float(np.abs(ens.level(1).astype(np.float32) - Y[:, 0]).max()),
       "TAB_tick0_maxabs": float(np.abs(np.asarray(w._tab(ens.carry)).astype(np.float32) - TAB[:, 0]).max())}
log(res)
t = 0
while t < 50:
    if t == 40:
        br = ens.clone(rep=5, fresh=True)
        br, rb = AW.chunked_rollout(d, br, 4, chunk=4, rec=("L1", "TAB"))
        got = rb["L1"][:, 1:].reshape(18, 5, 4, -1).astype(np.float32)
        res["clone_tick40_first4_L1_maxabs"] = float(np.abs(got - B[:, 0, :, :4]).max())
        res["clone_tick40_first4_L1_maxabs_vs_base"] = float(np.abs(got - Y[:, None, 41:45]).max())
        log("clones", res["clone_tick40_first4_L1_maxabs"])
    ens, r = d.rollout(ens, None, T=10, rec=("L1", "TAB"))
    res[f"base_L1_ticks{t+1}-{t+10}_maxabs"] = float(np.abs(r["L1"][:, 1:].astype(np.float32) - Y[:, t + 1:t + 11]).max())
    res[f"base_TAB_ticks{t+1}-{t+10}_maxabs"] = float(np.abs(r["TAB"][:, 1:].astype(np.float32) - TAB[:, t + 1:t + 11]).max())
    log("tick", t + 10, res[f"base_L1_ticks{t+1}-{t+10}_maxabs"])
    t += 10
res["seconds"] = time.time() - T0
json.dump(res, open("/home/user/evalwork/vecworld/vw1/fresh/closure/check/rerun_sim.json", "w"), indent=1)
log("saved", res)
