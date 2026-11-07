"""Lockstep: <host Phi_objects, JAX Phi_objects> on the SAME A_gliders level-0 trajectory.

usage: python -B lockstep.py TAG SEED J T
  -> lockstep_TAG.json (summary) and lockstep_TAG.npz (per member and tick: comparison record)

World: the A_gliders world of aworld.build (Flow-Lenia JAX, stride 20, burn-in 50 ticks, world_seed 0)
whose chain is phi.pair(host tracker, JAX tracker): both read the identical level-0 state each tick
(one World, one key per member, members d.ensemble(J, seed=(SEED,))). Memories are compared inside
the compiled tick (record 'CMP'), every tick including t = 0 (after init + burn-in, during which both
memories were already updated in lockstep):
  map, discrete slot columns (present, age, event, uid), globals: number of differing entries;
  overflow block of the JAX memory; per slot-table column max |host - jax| and max relative diff;
  number of continuous entries that are not bit-identical; agent observation = q*round(y/q)
  (q = 1e-3; the permutation is the same for both) -> number of differing coordinates;
  margins: min |blur - threshold| over pixels, min |mass - m_min| over raw components (how close a
  discrete decision came to a rounding flip).
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
from vw import objects as OB  # noqa: E402
import aworld as AW  # noqa: E402
import phi as PH  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
TAG, SEED, J, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
CH = 10
T0 = time.time()

specs, parts = AW.build(tracker="host")
po_h, LW = parts["phi_objects"], parts["LW"]
po_j, trj, _ = PH.phi_objects_jax()
bt = trj.bt
HW, K, NS, NF = bt.HW, bt.K, OB.NS, OB.NF
DISC = np.array([0, NF + 2, NF + 3, NF + 4])
q = AW.OBS.quantum
common = dict(base=parts["level"], inport=vw.InputPort(admissible=AW.INPUTS), outport=AW.OBS,
              burn_in=AW.BURN_TICKS * AW.STRIDE, replay="initial", public_notes=AW.NOTE)
spec = vw.stride(vw.WorldSpec(chain=(PH.pair(po_h, po_j, name="<host,jax>"),), name="A_gliders/lockstep", **common),
                 AW.STRIDE)


def raw_mass_margin(x):
    """min |mass - m_min| over the raw components of x (before the mass filter)."""
    A = x.reshape(bt.shape)
    S = A[0] + A[1]
    fg = OB.gaussian_blur_wrap(S, bt.sigma, bt.truncate) > bt.threshold
    L = OB.periodic_components(fg)
    fgf = fg.ravel()
    root = fgf & (L == jnp.arange(HW, dtype=jnp.int32))
    rank = jnp.cumsum(root.astype(jnp.int32)) - 1
    raw = jnp.where(fgf, jnp.minimum(rank[jnp.minimum(L, HW - 1)], bt.max_raw), bt.max_raw)
    mass = jnp.zeros(bt.max_raw + 1).at[raw].add(S.ravel())[:bt.max_raw]
    ok = jnp.arange(bt.max_raw) < rank[-1] + 1
    return jnp.min(jnp.where(ok, jnp.abs(mass - bt.m_min), jnp.inf))


def cmp(c):
    mh, mj = c.mem[0]
    Th, Tj = mh[HW:HW + K * NS].reshape(K, NS), mj[HW:HW + K * NS].reshape(K, NS)
    gh, gj = mh[HW + K * NS:], mj[HW + K * NS:HW + K * NS + 5]
    d = jnp.abs(Th - Tj)
    den = jnp.maximum(jnp.abs(Th), jnp.abs(Tj))
    rel = jnp.where(den > 0, d / jnp.where(den > 0, den, 1.0), 0.0)
    yh, yj = Th[:, :NF].ravel(), Tj[:, :NF].ravel()
    nobs = jnp.sum(q * jnp.round(yh / q) != q * jnp.round(yj / q))
    S = c.x[0] + c.x[1]
    B = OB.gaussian_blur_wrap(S, bt.sigma, bt.truncate)
    cont = np.setdiff1d(np.arange(NS), DISC)
    return jnp.concatenate([
        jnp.stack([jnp.sum(mh[:HW] != mj[:HW]), jnp.sum(Th[:, DISC] != Tj[:, DISC]), jnp.sum(gh != gj),
                   nobs, jnp.sum(Th[:, cont] != Tj[:, cont]), jnp.sum(Th[:, 0]),
                   jnp.min(jnp.abs(B - bt.threshold)), raw_mass_margin(c.x)]).astype(jnp.float64),
        mj[HW + K * NS + 5:], gj, d.max(0), rel.max(0)])


CMP_NAMES = (["map_diff", "disc_diff", "glob_diff", "obs_diff", "cont_not_bitequal", "n_present",
              "blur_thr_margin", "mass_mmin_margin"] + list(OB.OVERFLOW) + list(OB.GLOBALS) +
             [f"abs.{f}" for f in OB.FEATURES + OB.SLOT_EXTRA] + [f"rel.{f}" for f in OB.FEATURES + OB.SLOT_EXTRA])


class CmpWorld(AW.MapWorld):
    def _build(self):
        super()._build()
        tick = self._tick

        def rollout(params, c, A, rec):
            def one(args):
                cb, Ab = args
                first = cmp(cb)

                def body(cc, a):
                    cc = tick(params, cc, a)
                    return cc, cmp(cc)
                cb, outs = jax.lax.scan(body, cb, Ab)
                return cb, {"CMP": jnp.concatenate([first[None], outs], 0)}
            cB, outs = jax.lax.map(one, (c, jnp.swapaxes(A, 0, 1)), batch_size=self.batch_size)
            return cB, {r: jnp.swapaxes(v, 0, 1) for r, v in outs.items()}
        self._rollout_fn = rollout
        self._rollout = jax.jit(rollout, static_argnames=("rec",))


w = CmpWorld(spec, world_seed=0)
d = w.designer
ens = d.ensemble(J, seed=(SEED,))
t_init = time.time() - T0
print(f"[{time.time() - T0:7.1f}s] init + burn-in, {J} members", flush=True)
recs, done = [], 0
while done < T:
    ens, r = d.rollout(ens, None, T=CH, rec=("CMP",))
    recs.append(r["CMP"] if done == 0 else r["CMP"][:, 1:])
    done += CH
    if done % 50 == 0:
        R = np.concatenate(recs, 1)
        print(f"[{time.time() - T0:7.1f}s] tick {done}: map/disc/glob/obs diffs "
              f"{R[..., :4].sum((0, 1)).tolist()}", flush=True)
R = np.concatenate(recs, 1)                                   # (J, T+1, n)
ix = {n: i for i, n in enumerate(CMP_NAMES)}
feat = list(OB.FEATURES + OB.SLOT_EXTRA)
cont_cols = [f for i, f in enumerate(feat) if i not in DISC]
res = {
    "tag": TAG, "designer_seed": SEED, "world_seed": 0, "members": J, "ticks_after_burnin": T,
    "records_per_member": int(R.shape[1]), "world": "aworld A_gliders, MapWorld, chain = pair(host, jax)",
    "numpy_disabled_cpu_features": os.environ.get("NPY_DISABLE_CPU_FEATURES", ""),
    "member_ticks_compared": int(R.shape[0] * R.shape[1]),
    "slot_map_entries_differing": int(R[..., ix["map_diff"]].sum()),
    "discrete_slot_entries_differing": int(R[..., ix["disc_diff"]].sum()),
    "globals_entries_differing": int(R[..., ix["glob_diff"]].sum()),
    "ticks_with_any_discrete_mismatch": int(((R[..., ix["map_diff"]] + R[..., ix["disc_diff"]] +
                                              R[..., ix["glob_diff"]]) > 0).sum()),
    "jax_overflow_final": {n: R[:, -1, ix[n]].tolist() for n in OB.OVERFLOW},
    "obs_coords_compared": int(R.shape[0] * R.shape[1] * K * NF),
    "obs_coords_differing": int(R[..., ix["obs_diff"]].sum()),
    "obs_equality_rate": float(1 - R[..., ix["obs_diff"]].sum() / (R.shape[0] * R.shape[1] * K * NF)),
    "continuous_entries_compared": int(R.shape[0] * R.shape[1] * K * len(cont_cols)),
    "continuous_entries_not_bit_identical": int(R[..., ix["cont_not_bitequal"]].sum()),
    "max_abs_diff": {f: float(R[..., ix[f"abs.{f}"]].max()) for f in feat},
    "max_rel_diff": {f: float(R[..., ix[f"rel.{f}"]].max()) for f in feat},
    "max_abs_diff_all": float(max(R[..., ix[f"abs.{f}"]].max() for f in feat)),
    "max_rel_diff_all": float(max(R[..., ix[f"rel.{f}"]].max() for f in feat)),
    "min_blur_threshold_margin": float(R[..., ix["blur_thr_margin"]].min()),
    "min_mass_mmin_margin": float(R[..., ix["mass_mmin_margin"]].min()),
    "events_final_sum_over_members": {n: float(R[:, -1, ix[n]].sum()) for n in OB.GLOBALS[1:]},
    "objects_present_mean": float(R[..., ix["n_present"]].mean()),
    "timing_s": {"init_burnin": t_init, "total": time.time() - T0},
}
np.savez_compressed(f"{OUT}/lockstep_{TAG}.npz", R=R.astype(np.float32), names=np.array(CMP_NAMES))
json.dump(res, open(f"{OUT}/lockstep_{TAG}.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("max_abs_diff", "max_rel_diff")}, indent=1))
