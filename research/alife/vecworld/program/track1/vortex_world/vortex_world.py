"""vortex_world -- the fed-vortex world with heredity in the vw types: coarse-grainings, ports, budget.

    level 0   vortex_jax.make_level(cfg): one tick = n_sub native steps (default 250 = 5 time units),
              stirring channel u in R^m held over the tick, channel noise N(0, sigma_a^2 I) every tick.
    level 1   phi_vortices = vw.compose(phi_kinds_field, BlobTracker): the tracker runs on the 2-channel
              field (|om| (1 - f_b), |om| f_b), f_b = b / (a + b + 1e-3), so a slot's mass is its
              circulation magnitude sum |om| over the body and its `frac_c1` feature is the |om|-weighted
              share of label b (kind b iff frac > 0.5). Bodies: blur sigma 1 px, threshold 0.06 on the
              blurred |om| -- the labkit segmentation of the source claim (|om| matter, smooth 1,
              threshold 0.06) -- and mass >= m_min (labkit used area >= 6 px). K slots x 12 features.
    level 2   phi_kinds (memoryless, on level 1): (N, s_b) = (number of present slots, share of kind-b
              slots); the share of kind a is 1 - s_b. Stacked with vw.stack.
    extra     phi_pooled: block means of (om, |om|, Y, |om| f_b) at block size `block` (a field view to
              pair with the vortex list, as gliders paired coarse with objects; not used by the pilot).
    ports     InputPort(Admissible(lo=-u_max, hi=u_max), in_map = identity), no multiplicative noise
              (the channel noise is inside the law); ObservePort(quantum=1e-3, out_map = identity).
    budget    vw.nats.NatsBudget.isotropic(m, sigma_a, tick, episode, total): c(u) = |u|^2 / (2 sigma_a^2).
"""
from __future__ import annotations

import _paths  # noqa: F401
import jax
import jax.numpy as jnp
import numpy as np

import vw
from vw.nats import NatsBudget
import vortex_jax as VJ

TRACK = dict(sigma=1.0, threshold=0.06, m_min=0.5, fallback_px=4.0)


def slots_for(cfg: VJ.Config) -> dict:
    """Slot and component caps scaled with the box (about 35-45 vortices at 128^2 in the source)."""
    s = (cfg.H * cfg.W) / 128 ** 2
    return dict(K=max(24, int(round(56 * s))), max_kept=max(32, int(round(72 * s))), max_raw=max(64, int(round(160 * s))))


def kinds_field(x):
    """(2, H, W): |om| split by the local share of label b."""
    w = jnp.abs(x["om"])
    fb = x["b"] / (x["a"] + x["b"] + 1e-3)
    return jnp.stack([w * (1 - fb), w * fb])


def phi_vortices(cfg: VJ.Config, **kw):
    """(CoarseGrain, BlobTracker): level 1, the vortex list."""
    opts = dict(TRACK, **slots_for(cfg))
    opts.update(kw)
    pre = vw.CoarseGrain.of(kinds_field, name="kinds_field", differentiable=False)
    cg, tr = vw.blob_tracker((2, cfg.H, cfg.W), name=f"vortices{opts['K']}", frac_channel=1, **opts)
    return vw.compose(pre, cg, name=cg.name), tr


def kinds(y1, K: int):
    """(N, s_b) from a level-1 vector (K * 12) or a batch of them (..., K * 12)."""
    T = jnp.reshape(y1, y1.shape[:-1] + (K, vw.objects.NF))
    present = T[..., 0] > 0.5
    n = present.sum(-1).astype(jnp.float64)
    nb = (present & (T[..., 2] > 0.5)).sum(-1).astype(jnp.float64)
    return jnp.stack([n, nb / jnp.maximum(n, 1.0)], -1)


def phi_kinds(K: int) -> vw.CoarseGrain:
    """Level 2 on level 1: (number of vortices, share of kind b)."""
    return vw.CoarseGrain.of(lambda y: kinds(y, K), name="kinds", differentiable=False)


def phi_pooled(cfg: VJ.Config, block: int = 16) -> vw.CoarseGrain:
    H, W, b = cfg.H, cfg.W, block

    def f(x):
        w = jnp.abs(x["om"])
        F = jnp.stack([x["om"], w, x["Y"], w * x["b"] / (x["a"] + x["b"] + 1e-3)])
        return F.reshape(4, H // b, b, W // b, b).mean((2, 4)).ravel()
    return vw.CoarseGrain.of(f, name=f"pooled{b}")


def nats_budget(cfg: VJ.Config, tick=None, episode=None, total=None) -> NatsBudget:
    note = (f"stirring coefficients u (one per bump of a public {cfg.G}x{cfg.G} grid of zero-mean Gaussian bumps, "
            f"std {cfg.stir_w} px) enter as u + eta, eta ~ N(0, {cfg.sigma_a}^2 I), at every tick")
    return NatsBudget.isotropic(cfg.m, cfg.sigma_a, tick=tick, episode=episode, total=total, note=note)


NOTE = ("Inputs stir: coordinate j adds vorticity in the shape of public bump j, spread over the tick, on top of "
        "background stirring of the same shape (Gaussian, std sigma_a per coordinate and tick). Costs in nats: "
        "|u|^2 / (2 sigma_a^2) per tick.")


def build(cfg: VJ.Config = VJ.Config(), theta: dict | None = None, u_max: float = 0.2, burn_in: int = 0,
          quantum: float = 1e-3):
    """WorldSpecs {'vortices' (level 1 observed), 'kinds' (stacked level 2 observed), 'pooled'} and the parts."""
    lev = VJ.make_level(cfg, theta)
    p1, tr = phi_vortices(cfg)
    p2 = phi_kinds(tr.K)
    inport = vw.InputPort(admissible=vw.Admissible(lo=-u_max, hi=u_max), in_map=tuple(range(cfg.m)))
    common = dict(base=lev, inport=inport, burn_in=burn_in, replay="initial", public_notes=NOTE)
    s1 = vw.WorldSpec(chain=(p1,), outport=vw.ObservePort(quantum=quantum, out_map=tuple(range(tr.n_out))),
                      name=f"fedvortex{cfg.H}/vortices", **common)
    s2 = vw.stack(s1, p2, name=f"fedvortex{cfg.H}/kinds")
    s2 = s2.replace(inport=inport, outport=vw.ObservePort(quantum=quantum, out_map=(0, 1)))   # stack unbinds the maps
    pp = phi_pooled(cfg)
    n_pool = 4 * (cfg.H // 16) * (cfg.W // 16)
    sp = vw.WorldSpec(chain=(pp,), outport=vw.ObservePort(quantum=quantum, out_map=tuple(range(n_pool))),
                      name=f"fedvortex{cfg.H}/pooled", **common)
    return {"vortices": s1, "kinds": s2, "pooled": sp}, {"level": lev, "phi1": p1, "phi2": p2, "tracker": tr,
                                                          "phi_pooled": pp, "cfg": cfg}


class MapWorld(vw.World):
    """vw.World whose ensembles are batched with jax.lax.map (members one after another, each member's
    rollout one scan), as port/aworld.MapWorld: the spectral step is cache-bound on one CPU core and
    vmap makes each member about 1.5x slower (122 vs 81 ms per member-tick at 64^2). Same pure
    functions, keys and numbers as vw.World."""

    def _build(self):
        super()._build()
        tick = self._tick

        def records(c, rec):
            out = {}
            for r in rec:
                if r == "obs":
                    out[r] = self._obs(c)
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
            cB, outs = jax.lax.map(one, (c, jnp.swapaxes(A, 0, 1)))
            return cB, {r: jnp.swapaxes(v, 0, 1) for r, v in outs.items()}

        self._rollout_fn = rollout
        self._rollout = jax.jit(rollout, static_argnames=("rec",))
        self._v_init = jax.jit(lambda params, ki, kd: jax.lax.map(
            lambda kk: self._init_member(params, kk[0], kk[1]), (ki, kd)))
