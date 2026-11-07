"""membrane_world -- the phase_membrane world in the vw types: coarse-grainings, ports, budget.

    level 0   membrane_jax.make_level(cfg): one tick = n_sub native steps (default 20 x dt 0.5 = 10 time
              units), substrate channel u in R^m held over the tick, channel noise N(0, sigma_a^2 I) every tick.
    level 1   phi_cells = vw.compose(cells_field, BlobTracker(audit=True)): the cell list. The tracker runs on
              the 2-channel field (phi (1 - k), phi k), k = clip(K, 0, 1), whose channel sum is phi: bodies are
              the 8-connected components of blur(phi, sigma 1) > 0.5 with mass sum(phi) >= m_min. phi is the
              right field because a cell *is* an inside-phase domain (the wall is the phi = 1/2 level set of an
              Allen-Cahn interface; the source's stats() and the suites count phi > 0.5 components); K, L or the
              wall 4 phi (1 - phi) would give catalyst spots, link rings or annuli. 0.5 is the wall midpoint and
              the switching point of the untilted double well; results/threshold.json reports how counts and
              sizes move between 0.3 and 0.7. Per slot (vw.objects.FEATURES): present, mass (= phi-area, px),
              frac_c1 (= the cell's phi-weighted mean catalyst K), centroid on the torus, radius of gyration,
              shape q1 q2, velocity. audit=True appends the tracker's 5 cumulative counters (next_uid, births,
              deaths, fusions, fissions), so level 1 carries its own event ledger. K slots x 12 + 5 numbers.
    level 2   phi_population (on level 1, with memory): (N, mean size, division rate) = (number of present
              slots, their mean mass, divisions per cell per 100 time units over the last W = 50 ticks:
              sum of the per-tick division counts / sum of the per-tick cell counts / tick_time * 100). A division
              is a slot that is present now, was empty at the previous tick (the tracker never refills a slot in
              the tick it empties, so this is a new cell) and has mass >= m_div = 50. Why not the tracker's
              fission counter: in the pilot 55% of fission products are < 50 px and 79-94% of those dissolve
              within 20 ticks (shed wall fragments, not daughters), cells below ~50 px shrink on average and
              cells above grow (analysis.json level1_main); new cells by birth are tiny (median 13 px), so new
              slots >= 50 px are division products. Memory: (presence at the previous tick, ring buffers of W
              division counts and W cell counts, tick index): a deterministic transducer of level 1. Stacked
              with vw.stack.
    extra     phi_pooled: block means of (S, K, L, phi) at block size `block` (a field view to pair with the cell
              list, WORLDS.md 2.2: cells compete for S).
    ports     InputPort(Admissible(lo=-u_max, hi=u_max), identity in_map), no multiplicative noise (the channel
              noise is inside the law); ObservePort(quantum=1e-3, identity out_map).
    budget    vw.nats.NatsBudget.isotropic(m, sigma_a, tick, episode, total): c(u) = |u|^2 / (2 sigma_a^2).
"""
from __future__ import annotations

import _paths  # noqa: F401
import jax
import jax.numpy as jnp
import numpy as np

import vw
from vw.nats import NatsBudget
import membrane_jax as MJ

TRACK = dict(sigma=1.0, threshold=0.5, m_min=12.0, fallback_px=4.0)
W_RATE = 50            # level-2 rate window (ticks)
M_DIV = 50.0           # minimum mass (phi-area, px) of a new cell counted as a division product
GLOBAL_FISSIONS = 4    # index of 'fissions' in vw.objects.GLOBALS


def slots_for(cfg: MJ.Config) -> dict:
    """Slot and component caps scaled with the box (20-30 cells, up to ~60 raw components at 128^2)."""
    s = (cfg.H * cfg.W) / 128 ** 2
    return dict(K=max(16, int(round(48 * s))), max_kept=max(24, int(round(64 * s))), max_raw=max(32, int(round(128 * s))))


def cells_field(x):
    """(2, H, W): phi split by the local catalyst level k = clip(K, 0, 1); the channel sum is phi."""
    k = jnp.clip(x["K"], 0.0, 1.0)
    return jnp.stack([x["phi"] * (1 - k), x["phi"] * k])


def phi_cells(cfg: MJ.Config, **kw):
    """(CoarseGrain, BlobTracker): level 1, the cell list with the cumulative event counters."""
    opts = dict(TRACK, **slots_for(cfg))
    opts.update(kw)
    pre = vw.CoarseGrain.of(cells_field, name="cells_field", differentiable=False)
    cg, tr = vw.blob_tracker((2, cfg.H, cfg.W), name=f"cells{opts['K']}", frac_channel=1, audit=True, **opts)
    return vw.compose(pre, cg, name=cg.name), tr


def table(y1, K: int):
    """(present (.., K) bool, mass (.., K), cumulative fissions (..)) from level-1 vectors (.., K*NF + 5)."""
    T = jnp.reshape(y1[..., :K * vw.objects.NF], y1.shape[:-1] + (K, vw.objects.NF))
    return T[..., 0] > 0.5, T[..., 1], y1[..., K * vw.objects.NF + GLOBAL_FISSIONS]


def population_now(y1, K: int):
    """(N, mean size) of a level-1 vector."""
    pres, mass, _ = table(y1, K)
    n = pres.sum(-1).astype(jnp.float64)
    return n, jnp.where(pres, mass, 0.0).sum(-1) / jnp.maximum(n, 1.0)


def phi_population(K: int, tick_time: float, W: int = W_RATE, m_div: float = M_DIV) -> vw.CoarseGrain:
    """Level 2 on level 1: (N, mean size, divisions per cell per 100 t over the last W ticks); module doc."""

    def m_init(y1):
        pres, _, _ = table(y1, K)
        return (pres.astype(jnp.float64), jnp.zeros((W,)), jnp.zeros((W,)), jnp.zeros((), jnp.int64))

    def m_upd(m, y1):
        prev, bd, bn, k = m
        pres, mass, _ = table(y1, K)
        n, _ = population_now(y1, K)
        new = (pres & (prev < 0.5) & (mass >= m_div)).sum().astype(jnp.float64)
        i = k % W
        return (pres.astype(jnp.float64), bd.at[i].set(new), bn.at[i].set(n), k + 1)

    def phi(y1, m):
        n, size = population_now(y1, K)
        _, bd, bn, _ = m
        rate = 100.0 * bd.sum() / (jnp.maximum(bn.sum(), 1.0) * tick_time)
        return jnp.stack([n, size, rate])

    return vw.CoarseGrain(phi=phi, init_memory=m_init, update_memory=m_upd, differentiable=False,
                          name=f"population_w{W}")


def level2_from_level1(L1, K: int, tick_time: float, W: int = W_RATE, m_div: float = M_DIV):
    """Level-2 series (S, T, 3) from saved level-1 series (S, T, K*12 + 5), with the declared transducer."""
    cg = phi_population(K, tick_time, W, m_div)

    def one(ys):
        m0 = cg.init_memory(ys[0])

        def body(m, y):
            m = cg.update_memory(m, y)
            return m, cg.phi(y, m)
        _, out = jax.lax.scan(body, m0, ys[1:])
        return jnp.concatenate([cg.phi(ys[0], m0)[None], out], 0)
    return np.asarray(jax.jit(jax.vmap(one))(jnp.asarray(L1, jnp.float64)))


def phi_pooled(cfg: MJ.Config, block: int = 16) -> vw.CoarseGrain:
    H, W, b = cfg.H, cfg.W, block

    def f(x):
        F = jnp.stack([x["S"], x["K"], x["L"], x["phi"]])
        return F.reshape(4, H // b, b, W // b, b).mean((2, 4)).ravel()
    return vw.CoarseGrain.of(f, name=f"pooled{b}")


def nats_budget(cfg: MJ.Config, tick=None, episode=None, total=None) -> NatsBudget:
    note = (f"substrate coefficients u (one per bump of a public {cfg.G}x{cfg.G} grid of Gaussian bumps of std "
            f"{cfg.bump_w} px and peak 1) enter as u + eta, eta ~ N(0, {cfg.sigma_a}^2 I), at every tick")
    return NatsBudget.isotropic(cfg.m, cfg.sigma_a, tick=tick, episode=episode, total=total, note=note)


NOTE = ("Inputs feed or withdraw substrate: coordinate j adds substrate in the shape of public bump j, spread over "
        "the tick, on top of background feeding fluctuations of the same shape (Gaussian, std sigma_a per "
        "coordinate and tick). Costs in nats: |u|^2 / (2 sigma_a^2) per tick.")


def build(cfg: MJ.Config = MJ.Config(), theta: dict | None = None, u_max: float = 0.2, burn_in: int = 0,
          quantum: float = 1e-3, W: int = W_RATE, m_div: float = M_DIV):
    """WorldSpecs {'cells' (level 1 observed), 'population' (stacked level 2 observed), 'pooled'} and parts."""
    lev = MJ.make_level(cfg, theta)
    p1, tr = phi_cells(cfg)
    p2 = phi_population(tr.K, cfg.tick_time, W, m_div)
    inport = vw.InputPort(admissible=vw.Admissible(lo=-u_max, hi=u_max), in_map=tuple(range(cfg.m)))
    common = dict(base=lev, inport=inport, burn_in=burn_in, replay="initial", public_notes=NOTE)
    n1 = tr.n_out + len(vw.objects.GLOBALS)
    s1 = vw.WorldSpec(chain=(p1,), outport=vw.ObservePort(quantum=quantum, out_map=tuple(range(n1))),
                      name=f"membrane{cfg.H}/cells", **common)
    s2 = vw.stack(s1, p2, name=f"membrane{cfg.H}/population")
    s2 = s2.replace(inport=inport, outport=vw.ObservePort(quantum=quantum, out_map=(0, 1, 2)))  # stack unbinds maps
    pp = phi_pooled(cfg)
    n_pool = 4 * (cfg.H // 16) * (cfg.W // 16)
    sp = vw.WorldSpec(chain=(pp,), outport=vw.ObservePort(quantum=quantum, out_map=tuple(range(n_pool))),
                      name=f"membrane{cfg.H}/pooled", **common)
    return {"cells": s1, "population": s2, "pooled": sp}, {"level": lev, "phi1": p1, "phi2": p2, "tracker": tr,
                                                            "phi_pooled": pp, "cfg": cfg}


class MapWorld(vw.World):
    """vw.World whose ensembles are batched with jax.lax.map (members one after another, each member's rollout
    one scan), as port/aworld.MapWorld and vortex_world.MapWorld: on one core vmap makes a member-tick slower
    (12.3 ms at B = 1 against 16.4 at B = 4 and 20.1 at B = 16 per member, results/timing.json). Same pure
    functions, keys and numbers as vw.World. Extra record 'ev' (designer only): the tracker's per-slot
    (event, uid) columns, K x 2, for lineage analysis; it needs the chain's first entry to be phi_cells."""

    def _build(self):
        super()._build()
        tick = self._tick
        tr_mem = lambda c: c.mem[0][1]                                    # noqa: E731  compose memory (pre, tracker)
        K = None
        for cg in self.spec.chain[:1]:
            K = int(cg.name.replace("cells", "")) if cg.name.startswith("cells") else None

        def records(c, rec):
            out = {}
            for r in rec:
                if r == "obs":
                    out[r] = self._obs(c)
                elif r == "clean":
                    out[r] = self._clean(c)
                elif r == "x":
                    out[r] = vw.flat(c.x)
                elif r == "ev":
                    HW = c.x["phi"].size
                    T = tr_mem(c)[HW:HW + K * vw.objects.NS].reshape(K, vw.objects.NS)
                    out[r] = T[:, vw.objects.NF + 3:vw.objects.NF + 5]
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
