"""aworld -- the VW-0 A_gliders world re-expressed in the VW-1 types.

    level 0   L_FL: one Flow-Lenia substep with the VW-0 zero-sum kick and flow noise 0.5
              (flowlenia_jax.make_level); the world uses vw.stride(., 20): one tick = 20 substeps,
              input before the first, burn-in 1000 substeps = 50 ticks, as VW-0.
    level 1   Phi_coarse (JAX) | Phi_objects | <Phi_coarse, Phi_objects>; Phi_objects is the tracker
              build(tracker=...) selects: 'jax' (phi.phi_objects_jax, pure JAX) or 'host' (the VW-0
              tracker through a host callback, the reference; the default, see README); same rules,
              same observations.
    ports     InputPort(Admissible(k=8, lo=-1, hi=1, total=4, zero_sum=True)) on the 128*128 cells
              (hidden permutation); ObservePort(noise=0, quantum=1e-3) (hidden permutation).

MapWorld is vw.World with members batched by jax.lax.map instead of jax.vmap. On CPU the
Flow-Lenia state (2 x 128 x 128 float64, plus 20 kernel convolutions and a 9-way scatter per
substep) is cache-bound: vmap makes each member 1.5-1.8x slower, lax.map keeps the single-member
speed. Same pure functions, same keys, same numbers (checked in check_batching).
"""
from __future__ import annotations

import _paths  # noqa: F401
import jax
import jax.numpy as jnp
import numpy as np

import vw
import flowlenia_jax as FJ
import phi as PH

STRIDE, BURN_TICKS, NOISE_STD, G = 20, 50, 0.5, 8
TRACKER = "jax"       # default Phi_objects implementation: 'jax' (pure JAX) | 'host' (reference)
INPUTS = vw.Admissible(k=8, lo=-1.0, hi=1.0, total=4.0, zero_sum=True)
OBS = vw.ObservePort(noise=0.0, quantum=1e-3)
NOTE = ("Inputs move matter: a negative coordinate removes at most the matter present at its site; under "
        "zero sum the positive coordinates receive exactly what was removed, in proportion.")


def build(name: str = "A_gliders", noise_std: float = NOISE_STD, stride: int = STRIDE, burn_ticks: int = BURN_TICKS,
          inputs: vw.Admissible = INPUTS, obs: vw.ObservePort = OBS, with_objects: bool = True,
          tracker: str = TRACKER):
    """WorldSpecs {'coarse', 'objects', 'both'} (all strided) and the parts. tracker: 'jax' | 'host'."""
    if tracker not in ("jax", "host"):
        raise ValueError("build: tracker must be 'jax' or 'host'")
    lev, cfg, meta = FJ.make_level(name, noise_std)
    pc = PH.phi_coarse(cfg, G)
    parts = {"level": lev, "cfg": cfg, "meta": meta, "phi_coarse": pc}
    common = dict(base=lev, inport=vw.InputPort(admissible=inputs), outport=obs, burn_in=burn_ticks * stride,
                  replay="initial", public_notes=NOTE)
    specs = {"coarse": vw.stride(vw.WorldSpec(chain=(pc,), name=f"{name}/coarse{G}", **common), stride)}
    if with_objects:
        po, tr, LW = PH.phi_objects_jax(name) if tracker == "jax" else PH.phi_objects(name)
        parts.update(phi_objects=po, tracker=tr, LW=LW, tracker_kind=tracker)
        specs["objects"] = vw.stride(vw.WorldSpec(chain=(po,), name=f"{name}/objects{tr.K}", **common), stride)
        specs["both"] = vw.stride(vw.WorldSpec(chain=(PH.pair(pc, po),), name=f"{name}/coarse+objects", **common),
                                  stride)
    return specs, parts


class MapWorld(vw.World):
    """vw.World whose ensembles are batched with jax.lax.map (members one after another, each
    member's whole rollout in one scan). batch_size=None: fully sequential."""

    batch_size = None

    def _build(self):
        super()._build()
        tick, k = self._tick, self.k_obs

        def records(c, rec):
            out = {}
            for r in rec:
                if r == "obs":
                    out[r] = self._obs(c)
                elif r == "obs_continuous":
                    out[r] = self._obs_continuous(c)
                elif r == "clean":
                    out[r] = self._clean(c)
                elif r == "x":
                    out[r] = vw.flat(c.x)
                elif r.startswith("L"):
                    out[r] = vw.flat(self._levels(c.x, c.mem, int(r[1:]))[-1])
                else:
                    raise ValueError(f"rollout: unknown record {r!r}")
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

        def v_init(params, ki, kd):
            return jax.lax.map(lambda kk: self._init_member(params, kk[0], kk[1]), (ki, kd), batch_size=self.batch_size)

        self._rollout_fn = rollout
        self._rollout = jax.jit(rollout, static_argnames=("rec",))
        self._v_init = jax.jit(v_init)
        del k


def chunked_rollout(d, ens, T: int, chunk: int = 10, rec=("L1",), P=None):
    """Designer.rollout in fixed-size chunks: the library materialises dense (T, B, n_in) input
    arrays (n_in = 16384 here) and recompiles for every new T. Returns (ens, records (B, T+1, d))."""
    outs, done = {r: [] for r in rec}, 0
    while done < T:
        n = min(chunk, T - done)
        ens, r = d.rollout(ens, P, T=n, rec=rec)
        for k in rec:
            outs[k].append(r[k] if done == 0 else r[k][:, 1:])
        done += n
    return ens, {k: np.concatenate(v, 1) for k, v in outs.items()}


def inverse_in_map(w: vw.World) -> np.ndarray:
    inv = -np.ones(w.inport.n_u, int)
    inv[w.in_map] = np.arange(w.n_in)
    return inv
