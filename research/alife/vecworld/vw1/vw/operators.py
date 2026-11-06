"""vw.operators -- composition operators on levels, coarse-grainings and worlds.

All operators build new pure functions from old ones; none adds hidden state, so purity,
batching (vmap) and explicit randomness (Noise streams and sub-steps) are preserved.

stack(spec, cg)            post-compose a coarse-graining L_k -> L_{k+1}; observe the new level
product(*specs, noise=)    X0 x X0', F0 x F0', Phi x Phi' (monoidal); noise 'independent'
                           (stream i per factor), 'shared' (one stream for all: common random
                           numbers) or ('correlated', rho) for two Gaussian-explicit levels
couple(src, dst, wire)     src's observed level, read through a declared sensor (noise, value
                           step), mapped by `wire` into dst's input port each tick
stride(spec, n)            one tick = n level-0 steps; input before the first sub-step
refine(spec, fine, psi)    a new level -1 with an approximate factor map psi: X_-1 -> X_0; the
                           input port moves to level -1; optional commutation-error check
commutation_error(...)     the defect of a coarse-graining as a morphism between two levels
"""
from __future__ import annotations

import math
from typing import Callable, Optional, Sequence

import jax
import jax.numpy as jnp
import numpy as np

from .core import CoarseGrain, Level, Noise, compose_all, flat, identity, product_cg
from .ports import Admissible, InputPort
from .world import WorldSpec, _NS_CERT, make_key, member_keys


# ----------------------------------------------------------------------------- helpers
def _chain_start(chain, x):
    mem, y = [], x
    for cg in chain:
        m = cg.init_memory(y) if cg.has_memory else ()
        y = cg.phi(y, m)
        mem.append(m)
    return tuple(mem)


def _chain_update(chain, mem, x):
    out, y = [], x
    for cg, m in zip(chain, mem):
        if cg.has_memory:
            m = cg.update_memory(m, y)
        y = cg.phi(y, m)
        out.append(m)
    return tuple(out)


def _chain_top(chain, x, mem):
    y = x
    for cg, m in zip(chain, mem):
        y = cg.phi(y, m)
    return y


def _prefixed(conserved: dict, prefix: str, getter: Callable) -> dict:
    return {f"{prefix}{k}": (lambda f: (lambda x: f(getter(x))))(f) for k, f in conserved.items()}


# ----------------------------------------------------------------------------- stack
def stack(spec: WorldSpec, cg: CoarseGrain, at: Optional[int] = None, observe: bool = True,
          name: Optional[str] = None) -> WorldSpec:
    """Post-compose cg on level `at` (default: the observed level). The chain becomes
    chain[:at] + (cg,), so levels above `at` (never observed) are dropped. observe=True moves the
    observation port to the new level (its permutation is re-drawn for the new size)."""
    at = spec.k_obs if at is None else int(at)
    chain = spec.chain[:at] + (cg,)
    return spec.replace(chain=chain, observe_at=(len(chain) if observe else spec.k_obs),
                        outport=spec.outport.unbound(), inport=spec.inport.unbound(),
                        name=name or f"stack({spec.name})")


# ----------------------------------------------------------------------------- product
def product_level(*levels: Level, noise="independent", name: Optional[str] = None) -> Level:
    """Product of levels on tuple states; params {'0': p0, '1': p1, ...}; u is the concatenation."""
    n = len(levels)
    dims = [L.input_dim for L in levels]
    offs = np.concatenate([[0], np.cumsum(dims)]).astype(int)

    def init(p, key):
        return tuple(L.init(p[str(i)], jax.random.fold_in(key, i)) for i, L in enumerate(levels))

    def split_u(u):
        return [u[offs[i]:offs[i + 1]] for i in range(n)]

    step_xi, noise_dim = None, None
    if noise == "independent":
        def step(p, x, nz, u):
            us = split_u(u)
            return tuple(L.step(p[str(i)], x[i], nz.stream(i), us[i]) for i, L in enumerate(levels))
        if all(L.step_xi is not None for L in levels):
            nd = [int(L.noise_dim) for L in levels]
            no = np.concatenate([[0], np.cumsum(nd)]).astype(int)
            noise_dim = int(no[-1])

            def step_xi(p, x, xi, u):
                us = split_u(u)
                return tuple(L.step_xi(p[str(i)], x[i], xi[no[i]:no[i + 1]], us[i]) for i, L in enumerate(levels))
    elif noise == "shared":
        def step(p, x, nz, u):
            us = split_u(u)
            return tuple(L.step(p[str(i)], x[i], nz, us[i]) for i, L in enumerate(levels))
    elif isinstance(noise, tuple) and noise[0] == "correlated":
        rho = float(noise[1])
        if n != 2 or any(L.step_xi is None for L in levels) or levels[0].noise_dim != levels[1].noise_dim:
            raise ValueError("correlated product: two levels with step_xi and equal noise_dim")
        if not -1.0 <= rho <= 1.0:
            raise ValueError("correlated product: |rho| <= 1")
        d = int(levels[0].noise_dim)
        a, b = levels
        s = math.sqrt(max(0.0, 1.0 - rho * rho))

        def step(p, x, nz, u):
            us = split_u(u)
            z1, z2 = nz.stream(0).normal((d,)), nz.stream(1).normal((d,))
            return (a.step_xi(p["0"], x[0], z1, us[0]), b.step_xi(p["1"], x[1], rho * z1 + s * z2, us[1]))
    else:
        raise ValueError("product noise must be 'independent', 'shared' or ('correlated', rho)")

    cons = {}
    for i, L in enumerate(levels):
        cons.update(_prefixed(L.conserved, f"{i}.", (lambda i: (lambda x: x[i]))(i)))
    return Level(init=init, step=step, input_dim=int(offs[-1]), params={str(i): L.params for i, L in enumerate(levels)},
                 noise_dim=noise_dim, step_xi=step_xi, conserved=cons,
                 differentiable=all(L.differentiable for L in levels), opaque=any(L.opaque for L in levels),
                 name=name or " x ".join(L.name for L in levels))


def product(*specs: WorldSpec, noise="independent", inport: Optional[InputPort] = None,
            outport=None, name: Optional[str] = None) -> WorldSpec:
    """Product world. Chains are aligned level by level up to the highest observed level (a factor
    observed lower is carried up by identities; levels above a factor's observed level are
    dropped). Actuators are concatenated; the product is anonymised jointly (one permutation over
    all actuators, one over all observations), so the agent must discover the factorisation.
    Default inputs: the first factor's constraints with k summed (a zero-sum over the union lets
    inputs move mass between factors for additive kicks; with per-factor state-dependent kicks such
    as the Flow-Lenia kick, a command split across factors can create matter, see
    port/compose_demo.py); default observation: the first factor's port."""
    base = product_level(*[s.base for s in specs], noise=noise)
    K = max(s.k_obs for s in specs)
    chain = tuple(product_cg(*[(s.chain[i] if i < s.k_obs else identity()) for s in specs]) for i in range(K))
    if inport is None:
        offs = np.concatenate([[0], np.cumsum([s.base.input_dim for s in specs])]).astype(int)
        act = tuple(int(j) + int(o) for s, o in zip(specs, offs[:-1]) for j in s.inport.actuators(s.base.input_dim))
        ks = [s.inport.admissible.k for s in specs]
        adm = Admissible(**{**specs[0].inport.admissible.__dict__,
                            "k": None if any(k is None for k in ks) else int(sum(ks))})
        inport = InputPort(admissible=adm, actuable=act, noise=specs[0].inport.noise)
    return WorldSpec(base=base, chain=chain, inport=inport.unbound(),
                     outport=(outport or specs[0].outport).unbound(), observe_at=K,
                     burn_in=max(s.burn_in for s in specs), replay=specs[0].replay,
                     max_ticks=specs[0].max_ticks, name=name or " x ".join(s.name for s in specs))


# ----------------------------------------------------------------------------- stride
def stride_level(L: Level, n: int, name: Optional[str] = None) -> Level:
    """F^n: n steps per call, the input acting before the first; sub-step i draws Noise.substep(n, i)."""
    n = int(n)
    if n < 1:
        raise ValueError("stride: n >= 1")

    def step(p, x, nz, u):
        def body(xx, i):
            ui = jnp.where(i == 0, 1.0, 0.0) * u
            return L.step(p, xx, nz.substep(n, i), ui), None
        x, _ = jax.lax.scan(body, x, jnp.arange(n))
        return x

    return Level(init=L.init, step=step, input_dim=L.input_dim, params=L.params, conserved=dict(L.conserved),
                 differentiable=L.differentiable, opaque=L.opaque, name=name or f"{L.name}^{n}")


def stride(spec: WorldSpec, n: int, name: Optional[str] = None) -> WorldSpec:
    """Temporal coarse-graining: one tick = n level-0 steps; memories update once per tick;
    the burn-in is ceil(burn_in / n) strided ticks."""
    return spec.replace(base=stride_level(spec.base, n), burn_in=-(-spec.burn_in // int(n)),
                        inport=spec.inport.unbound(), outport=spec.outport.unbound(),
                        name=name or f"stride{n}({spec.name})")


# ----------------------------------------------------------------------------- couple
def couple(src: WorldSpec, dst: WorldSpec, wire: Callable, readout_noise: Optional[float] = None,
           readout_quantum: Optional[float] = None, saturate: bool = True, observe: str = "both",
           inport: Optional[InputPort] = None, outport=None, name: Optional[str] = None) -> WorldSpec:
    """Wire src's observed level into dst's input port.

    Each tick, before the laws run: y = src's observed level (flat, designer basis) read by a
    sensor with Gaussian noise `readout_noise` and value step `readout_quantum` (defaults: src's
    observation port numbers); u_dst = wire(y) in dst's actuator space; on dst's actuable
    coordinates it is saturated into dst's per-tick admissible set (saturate=True) and given dst's
    actuation noise. The agent acts on src's input port (default). The coupled level-0 state is
    (x_src, m_src, x_dst): src's tracking memory moves into level 0 because the wire reads it, which
    keeps level 0 Markov. Observation: 'both' (src level x dst level), 'src' or 'dst'.
    Noise streams of the coupled law: 0 src, 1 dst, 2 sensor, 3 dst actuation."""
    Ls, Ld = src.base, dst.base
    sch, dch = src.chain[:src.k_obs], dst.chain[:dst.k_obs]
    sig = src.outport.noise if readout_noise is None else float(readout_noise)
    q = src.outport.quantum if readout_quantum is None else readout_quantum
    dport = dst.inport
    act_d = np.asarray(dport.actuators(Ld.input_dim), int)
    Cd = dport.admissible
    nud = Ld.input_dim

    def wire_u(xs, ms, nz):
        y = flat(_chain_top(sch, xs, ms))
        if sig > 0:
            y = y + sig * nz.stream(2).normal(y.shape)
        if q:
            y = q * jnp.round(y / q)
        u = jnp.asarray(wire(y), jnp.float64).reshape(nud)
        a = u[act_d]
        if saturate:
            a = Cd.saturate(a)
        if dport.noise > 0:
            mask = a != 0
            a2 = a * (1.0 + dport.noise * nz.stream(3).normal(a.shape))
            if Cd.zero_sum:
                a2 = jnp.where(mask, a2 - a2.sum() / jnp.maximum(mask.sum(), 1), 0.0)
            a = a2
        return jnp.zeros((nud,)).at[act_d].set(a)

    def init(p, key):
        xs = Ls.init(p["src"], jax.random.fold_in(key, 0))
        xd = Ld.init(p["dst"], jax.random.fold_in(key, 1))
        return (xs, _chain_start(sch, xs), xd)

    def step(p, x, nz, u):
        xs, ms, xd = x
        ud = wire_u(xs, ms, nz)
        xs2 = Ls.step(p["src"], xs, nz.stream(0), u)
        xd2 = Ld.step(p["dst"], xd, nz.stream(1), ud)
        return (xs2, _chain_update(sch, ms, xs2), xd2)

    cons = {**_prefixed(Ls.conserved, "src.", lambda x: x[0]), **_prefixed(Ld.conserved, "dst.", lambda x: x[2])}
    diff = Ls.differentiable and Ld.differentiable and all(c.differentiable for c in sch)
    base = Level(init=init, step=step, input_dim=Ls.input_dim, params={"src": Ls.params, "dst": Ld.params},
                 conserved=cons, differentiable=diff, opaque=Ls.opaque or Ld.opaque or any(c.opaque for c in sch),
                 name=f"couple({Ls.name}->{Ld.name})")
    dcg = compose_all(dch)
    src_top = lambda x: _chain_top(sch, x[0], x[1])  # noqa: E731
    if observe == "both":
        phi = lambda x, m: (src_top(x), dcg.phi(x[2], m))  # noqa: E731
    elif observe == "dst":
        phi = lambda x, m: dcg.phi(x[2], m)  # noqa: E731
    elif observe == "src":
        phi = lambda x, m: src_top(x)  # noqa: E731
    else:
        raise ValueError("couple: observe must be 'both', 'src' or 'dst'")
    dmem = dcg.has_memory and observe != "src"
    cg = CoarseGrain(phi=phi, init_memory=(lambda x: dcg.init_memory(x[2])) if dmem else None,
                     update_memory=(lambda m, x: dcg.update_memory(m, x[2])) if dmem else None,
                     differentiable=dcg.differentiable, opaque=dcg.opaque, name=f"read({observe})")
    return WorldSpec(base=base, chain=(cg,), inport=(inport or src.inport).unbound(),
                     outport=(outport or src.outport).unbound(), observe_at=1,
                     burn_in=max(src.burn_in, dst.burn_in), replay=src.replay, max_ticks=src.max_ticks,
                     name=name or f"couple({src.name}->{dst.name})")


# ----------------------------------------------------------------------------- refine
def lifted(fine: Level, lift: Callable, input_dim: int, name: Optional[str] = None) -> Level:
    """Lifted actuation: the fine level driven by old actuator vectors u through lift(u), chosen so
    that psi(x + lift(u)) = psi(x) + u for additive kicks."""
    return Level(init=fine.init, step=lambda p, x, nz, u: fine.step(p, x, nz, lift(u)), input_dim=int(input_dim),
                 params=fine.params, conserved=dict(fine.conserved), differentiable=fine.differentiable,
                 opaque=fine.opaque, name=name or f"lifted({fine.name})")


def refine(spec: WorldSpec, fine: Level, psi, inport: Optional[InputPort] = None, check: Optional[dict] = None,
           tol: Optional[float] = None, name: Optional[str] = None) -> WorldSpec:
    """Extend downward: a level -1 `fine` with an (approximate) factor map psi: X_-1 -> X_0.

    The new world's law is fine's; its chain is (psi,) + old chain; the old level-0 law survives
    only as the reference for the commutation check. The input port must enter at level -1:
    inport=None keeps the old port declaration, which requires fine.input_dim == old input_dim
    (lifted actuation, e.g. via `lifted`); otherwise declare a new port on level -1 (fine
    actuation; the old port's meaning need not survive). check={...} runs commutation_error(fine,
    psi, old base, **check) and stores it in meta['refine_check']; with tol, a defect delta2 above
    tol raises ValueError."""
    cg = psi if isinstance(psi, CoarseGrain) else CoarseGrain.of(psi, name="psi")
    if cg.has_memory:
        raise ValueError("refine: psi must be memoryless (a factor map of states)")
    if inport is None:
        if fine.input_dim != spec.base.input_dim:
            raise ValueError("refine: fine.input_dim differs from the old input port; give a lifted level "
                             "or declare inport on level -1")
        inport = spec.inport
    meta = dict(spec.meta)
    if check is not None:
        rep = commutation_error(fine, cg, spec.base, **check)
        meta["refine_check"] = rep
        if tol is not None and float(np.max(rep.get("delta2", rep.get("delta2_pathwise")))) > tol:
            raise ValueError(f"refine: commutation defect {rep} above tol={tol}")
    return WorldSpec(base=fine, chain=(cg,) + spec.chain, inport=inport.unbound(), outport=spec.outport.unbound(),
                     observe_at=spec.k_obs + 1, burn_in=spec.burn_in, replay=spec.replay, max_ticks=spec.max_ticks,
                     public_notes=spec.public_notes, name=name or f"refine({spec.name})", meta=meta)


# ----------------------------------------------------------------------------- defects
def commutation_error(fine: Level, psi, coarse: Level, T=(1,), n: int = 2000, n_rep: int = 16, seed: int = 0,
                      mode: str = "both", x0=None, u=None, burn_in: int = 0,
                      params_fine=None, params_coarse=None) -> dict:
    """Defect of psi as a morphism fine -> coarse (psi o F_fine vs F_coarse o psi).

    States x: x0 (batched) if given, else n draws from fine.init (after `burn_in` free steps).
    distributional  delta2(T) = E|| E[psi x(T) | x] - E[y(T) | y = psi x] ||^2, Monte Carlo over
                    n_rep fresh-noise branches each, MC variance bias removed (as VW-0).
    pathwise        delta2_pathwise(T) = E|| psi x(T) - y(T) ||^2 with both levels driven by the
                    SAME Noise (a coupling): 0 iff psi is an exact factor map for this coupling,
                    and the root-mean-square defect obeys the triangle inequality under
                    composition, rms(psi2 o psi1) <= Lip(psi2) rms(psi1) + rms(psi2).
    u               optional actuator vector (or batch) applied at the first step to both levels
                    (checks lifted actuation: psi(F_f(x, u)) vs F_c(psi x, u))."""
    pf = fine.params if params_fine is None else params_fine
    pc = coarse.params if params_coarse is None else params_coarse
    Ts = sorted(set(int(t) for t in (T if isinstance(T, (list, tuple)) else (T,))))
    Tm = max(Ts)
    P = (lambda x: flat(psi.phi(x, ()))) if isinstance(psi, CoarseGrain) else (lambda x: flat(psi(x)))
    if x0 is None:
        ki = member_keys(make_key(_NS_CERT, 71, seed), n)
        x = jax.vmap(fine.init, in_axes=(None, 0))(pf, ki)
        if burn_in:
            kb = member_keys(make_key(_NS_CERT, 72, seed), n)
            x = jax.vmap(lambda xx, k: jax.tree_util.tree_map(lambda a: a[-1], fine.simulate(xx, k, T=burn_in, params=pf)))(x, kb)
    else:
        x = jax.tree_util.tree_map(jnp.asarray, x0)
    n = int(jax.tree_util.tree_leaves(x)[0].shape[0])
    if u is not None and fine.input_dim != coarse.input_dim:
        raise ValueError("commutation_error: u needs equal input dims")

    def U_of(B):
        U = jnp.zeros((B, Tm, fine.input_dim))
        if u is not None:
            uu = jnp.broadcast_to(jnp.asarray(u, jnp.float64), (B, fine.input_dim)) if np.ndim(u) == 1 else jnp.asarray(u)
            U = U.at[:, 0].set(uu)
        return U

    def run_f(xx, k, U):
        traj = fine.simulate(xx, k, U, params=pf)
        return jax.vmap(P)(traj)

    def run_c(yy, k, U):
        traj = coarse.simulate(yy, k, U, params=pc)
        return jax.vmap(flat)(traj)

    vf, vc = jax.jit(jax.vmap(run_f)), jax.jit(jax.vmap(run_c))
    y0 = jax.vmap(P)(x)
    yspec = jax.eval_shape(lambda: coarse.init(pc, jax.random.key(0)))
    y0s = jax.vmap(lambda v: _unflatten_like(v, yspec))(y0)
    out = {"T": Ts, "n": n}
    if mode in ("both", "pathwise"):
        kn = member_keys(make_key(_NS_CERT, 73, seed), n)
        Uu = U_of(n)
        df = np.asarray(vf(x, kn, Uu))
        dc = np.asarray(vc(y0s, kn, Uu))
        d2 = ((df - dc) ** 2).sum(-1).mean(0)
        out["delta2_pathwise"] = np.array([d2[t] for t in Ts])
        out["rms_pathwise"] = np.sqrt(out["delta2_pathwise"])
    if mode in ("both", "distributional"):
        sel = jnp.asarray(np.repeat(np.arange(n), n_rep))
        xr = jax.tree_util.tree_map(lambda a: a[sel], x)
        yr = jax.tree_util.tree_map(lambda a: a[sel], y0s)
        kf = member_keys(make_key(_NS_CERT, 74, seed), n * n_rep)
        kc = member_keys(make_key(_NS_CERT, 75, seed), n * n_rep)
        Ur = U_of(n * n_rep)
        yf = np.asarray(vf(xr, kf, Ur)).reshape(n, n_rep, Tm + 1, -1)
        yc = np.asarray(vc(yr, kc, Ur)).reshape(n, n_rep, Tm + 1, -1)
        raw = ((yf.mean(1) - yc.mean(1)) ** 2).sum(-1).mean(0)
        bias = (yf.var(1, ddof=1).sum(-1).mean(0) + yc.var(1, ddof=1).sum(-1).mean(0)) / n_rep
        out["delta2"] = np.array([raw[t] - bias[t] for t in Ts])
        out["raw"] = np.array([raw[t] for t in Ts])
        out["mc_bias"] = np.array([bias[t] for t in Ts])
    return out


def _unflatten_like(v, spec):
    """Inverse of flat for a pytree of ShapeDtypeStruct."""
    leaves, tdef = jax.tree_util.tree_flatten(spec)
    out, o = [], 0
    for l in leaves:
        sz = int(np.prod(l.shape)) if l.shape else 1
        out.append(v[o:o + sz].reshape(l.shape).astype(l.dtype))
        o += sz
    return jax.tree_util.tree_unflatten(tdef, out)
