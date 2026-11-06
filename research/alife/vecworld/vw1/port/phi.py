"""phi -- the A_gliders coarse-grainings as VW-1 CoarseGrain modules.

Phi_coarse   (JAX, memoryless, differentiable) block means of every channel on a G x G grid plus
             the block mean of A_sum^2 (second moment): 2*64 + 64 = 192 numbers. Same as
             integrate/lenia_world.make_phi_coarse.
Phi_objects  (opaque, with memory) the VW-0 tracker integrate/lenia_world.Tracker, wrapped as is
             (same declared rules, same code): its memory update runs on the host through
             jax.pure_callback; the readout phi(x, m) (the slot table's feature columns) is a JAX
             slice of the memory, so only one host round trip per tick and member.
pair         fan-out <Phi_1, Phi_2>: two coarse-grainings of the SAME level (copying a
             deterministic map is allowed in a Markov category). Not in the vw library; needed to
             observe Phi_coarse and Phi_objects of one level 0 in one world.
population   a level-2 coarse-graining of Phi_objects (JAX, with memory): count, total mass, mean
             speed and an EMA of the fusion count inferred from level 1 alone.
"""
from __future__ import annotations

import _paths  # noqa: F401
import jax
import jax.numpy as jnp
import numpy as np

import vw
from flowlenia_jax import FLConfig


# ----------------------------------------------------------------------------- Phi_coarse
def phi_coarse(cfg: FLConfig, G: int = 8) -> vw.CoarseGrain:
    C, H, W = cfg.C, cfg.H, cfg.W
    b = H // G
    assert b * G == H and W == H

    def f(A):
        X = A.reshape(C, G, b, G, b)
        mean = X.mean((2, 4)).reshape(-1)
        S = A.sum(0).reshape(G, b, G, b)
        m2 = (S ** 2).mean((1, 3)).reshape(-1)
        return jnp.concatenate([mean, m2])

    return vw.CoarseGrain.of(f, name=f"Phi_coarse{G}")


def coarse_names(cfg: FLConfig, G: int = 8) -> list:
    return [f"mean_c{c}[{i},{j}]" for c in range(cfg.C) for i in range(G) for j in range(G)] + \
           [f"m2[{i},{j}]" for i in range(G) for j in range(G)]


# ----------------------------------------------------------------------------- Phi_objects
def vw0_tracker(name: str = "A_gliders", K: int = None, m_min: float = None):
    """The VW-0 Tracker object (integrate/lenia_world.py) with the A_gliders settings."""
    import lenia_world as LW
    cfg = dict(LW.WORLD_CFG[name])
    l0 = LW.Level0(name, cfg["stride"], 0.0)
    tr = LW.Tracker(l0, cfg["K"] if K is None else K, cfg["m_min"] if m_min is None else m_min)
    return tr, LW


def phi_objects(name: str = "A_gliders", K: int = None, m_min: float = None, audit: bool = False) -> tuple:
    """(CoarseGrain, tracker, LW): the VW-0 tracker as an opaque transducer with memory.
    Memory m = [slot-label map (H*W) | slot table (K*NS) | globals (5)] (16593 numbers for K = 12);
    output = the slot table's NF feature columns (K*NF = 144). audit=True appends the tracker's
    cumulative counters (next uid, births, deaths, fusions, fissions): a designer-side view of the
    same transducer, for checking a level 2 against the tracker's own events."""
    tr, LW = vw0_tracker(name, K, m_min)
    HW, Kk, NS, NF = tr.l0.HW, tr.K, LW.NS, LW.NF
    mspec = jax.ShapeDtypeStruct((tr.n_m,), jnp.float64)

    def host_init(x):
        return np.asarray(tr.update_one(None, np.asarray(x, float).ravel()), float)

    def host_update(m, x):
        return np.asarray(tr.update_one(np.asarray(m, float), np.asarray(x, float).ravel()), float)

    def init_memory(x):
        return jax.pure_callback(host_init, mspec, x, vmap_method="sequential")

    def update_memory(m, x):
        return jax.pure_callback(host_update, mspec, m, x, vmap_method="sequential")

    def phi(x, m):
        y = m[HW:HW + Kk * NS].reshape(Kk, NS)[:, :NF].reshape(-1)
        return jnp.concatenate([y, m[HW + Kk * NS:]]) if audit else y

    cg = vw.CoarseGrain(phi=phi, init_memory=init_memory, update_memory=update_memory, opaque=True,
                        name=f"Phi_objects{Kk}" + ("+audit" if audit else ""))
    return cg, tr, LW


# ----------------------------------------------------------------------------- fan-out
def pair(a: vw.CoarseGrain, b: vw.CoarseGrain, name: str = None) -> vw.CoarseGrain:
    """<a, b>: both coarse-grainings read the same state; output and memory are pairs."""
    has = a.has_memory or b.has_memory

    def phi(x, m):
        ma, mb = m if has else ((), ())
        return (a.phi(x, ma), b.phi(x, mb))

    def m_init(x):
        return (a.init_memory(x) if a.has_memory else (), b.init_memory(x) if b.has_memory else ())

    def m_upd(m, x):
        ma, mb = m
        return (a.update_memory(ma, x) if a.has_memory else ma, b.update_memory(mb, x) if b.has_memory else mb)

    return vw.CoarseGrain(phi=phi, init_memory=m_init if has else None, update_memory=m_upd if has else None,
                          differentiable=a.differentiable and b.differentiable, opaque=a.opaque or b.opaque,
                          name=name or f"<{a.name},{b.name}>")


# ----------------------------------------------------------------------------- level 2
POP_NAMES = ["count", "total_mass", "mean_speed", "fusion_rate_ema"]


def population(K: int, NF: int, H: int = 128, W: int = 128, ema_ticks: float = 16.0, slack: float = 4.0):
    """Level 2 on the Phi_objects output y (K slots x NF features: present, mass, frac_c1, x_cos,
    x_sin, y_cos, y_sin, rg, q1, q2, vx, vy). Memory: (previous y, fusion count of the last tick,
    EMA rate). A slot that vanishes between ticks counts as FUSED if its last centroid lies within
    rg_s + rg_j + slack px (torus) of a slot j present at both ticks; it reads level 1 only.
    Returns (CoarseGrain, fused_count(y_prev, y_new)) so the inference can be audited offline."""
    E = H / (2 * np.pi)

    def unpack(y):
        S = y[:K * NF].reshape(K, NF)
        pres = S[:, 0] > 0.5
        cx = jnp.arctan2(S[:, 4], S[:, 3]) * W / (2 * np.pi)
        cy = jnp.arctan2(S[:, 6], S[:, 5]) * H / (2 * np.pi)
        return S, pres, cy, cx

    def fused_count(y0, y1):
        S0, p0, cy0, cx0 = unpack(y0)
        S1, p1, cy1, cx1 = unpack(y1)
        van = p0 & ~p1
        surv = p0 & p1
        dy = (cy0[:, None] - cy1[None, :] + H / 2) % H - H / 2
        dx = (cx0[:, None] - cx1[None, :] + W / 2) % W - W / 2
        d = jnp.sqrt(dy ** 2 + dx ** 2)
        near = (d <= S0[:, 7][:, None] + S1[:, 7][None, :] + slack) & surv[None, :]
        return jnp.sum(van & near.any(1)).astype(jnp.float64)

    def m_init(y):
        return (y, jnp.zeros(()), jnp.zeros(()))

    def m_upd(m, y):
        yp, _, r = m
        f = fused_count(yp, y)
        return (y, f, r + (f - r) / ema_ticks)

    def phi(y, m):
        S, pres, _, _ = unpack(y)
        n = pres.sum().astype(jnp.float64)
        mass = jnp.sum(jnp.where(pres, S[:, 1], 0.0))
        speed = jnp.sum(jnp.where(pres, jnp.hypot(S[:, 10], S[:, 11]), 0.0)) / jnp.maximum(n, 1.0)
        return jnp.stack([n, mass, speed, m[2]])

    del E
    cg = vw.CoarseGrain(phi=phi, init_memory=m_init, update_memory=m_upd, name="Psi_population")
    return cg, fused_count
