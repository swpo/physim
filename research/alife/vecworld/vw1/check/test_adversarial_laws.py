"""Checker's adversarial cases for two category laws (run from vw1/: pytest -p no:cacheprovider check/).

Stacking: nonlinear transducers with pytree memories and outputs, memory updates that read the
lower level's output computed with the lower level's NEW memory, a memoryless map between two
memoryful ones, identities inserted, every bracketing, nested stack() calls and stack(at=k).
All are compared with a numpy re-implementation of Definition 4 (cascade semantics) applied to the
recorded level-0 trajectory, not only with each other.

Stride: a nonlinear level with a tuple state, two draws per step from split keys plus an extra
noise stream, input entering inside a nonlinearity; compared with a hand-written loop over
Noise(key, 6t + k), at a clock near the 32-bit wrap, inside products, and at world level with a
memoryful chain, an odd burn-in and a program.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
from vw.lingauss import ring  # noqa: E402

PROG = [(0, {0: 0.5, 3: -0.5}), (2, {5: 1.0, 7: -1.0}), (5, {1: -0.2, 2: 0.2}), (9, {4: 0.3, 8: -0.3})]
RNG = np.random.default_rng(42)
W1 = RNG.normal(size=(6, 24)) * 0.4
W2 = RNG.normal(size=(5, 5)) * 0.6
W3 = RNG.normal(size=(5, 12)) * 0.5


# ---------------------------------------------------------------- transducers (jax) + numpy twins
def cg_a():
    """24 -> {'s': 6, 'q': 6}; memory (ema 6, cumulative energy scalar)."""
    def phi(x, m):
        e, c = m
        return {"s": jnp.tanh(jnp.asarray(W1) @ x) + 0.5 * e, "q": x[:6] * x[6:12] + c}
    return vw.CoarseGrain(phi=phi,
                          init_memory=lambda x: (jnp.asarray(W1) @ x, jnp.sum(x ** 2) * 0.01),
                          update_memory=lambda m, x: (0.7 * m[0] + 0.3 * jnp.sin(jnp.asarray(W1) @ x),
                                                      m[1] + 0.01 * jnp.sum(x ** 2)), name="A")


def np_a():
    def phi(x, m):
        e, c = m
        return {"q": x[:6] * x[6:12] + c, "s": np.tanh(W1 @ x) + 0.5 * e}
    return phi, (lambda x: (W1 @ x, np.sum(x ** 2) * 0.01)), \
        (lambda m, x: (0.7 * m[0] + 0.3 * np.sin(W1 @ x), m[1] + 0.01 * np.sum(x ** 2)))


def flat_a(y):          # jax flattens dict leaves in sorted key order: 'q' then 's'
    return np.concatenate([np.ravel(y["q"]), np.ravel(y["s"])])


def cg_b():
    """memoryless {'q','s'} -> 12, nonlinear mixing of the two leaves."""
    return vw.CoarseGrain.of(lambda y: jnp.concatenate([jnp.sin(y["s"]) * y["q"], y["s"] - y["q"] ** 2]), name="B")


def np_b():
    return lambda y, m: np.concatenate([np.sin(y["s"]) * y["q"], y["s"] - y["q"] ** 2]), None, None


def cg_c():
    """12 -> 5 + 5; order-sensitive recurrent memory m' = tanh(W2 m + W3 z_new)."""
    return vw.CoarseGrain(phi=lambda z, m: jnp.concatenate([jnp.asarray(W3) @ z - m, m]),
                          init_memory=lambda z: jnp.tanh(jnp.asarray(W3) @ z),
                          update_memory=lambda m, z: jnp.tanh(jnp.asarray(W2) @ m + jnp.asarray(W3) @ z), name="Cc")


def np_c():
    return (lambda z, m: np.concatenate([W3 @ z - m, m])), (lambda z: np.tanh(W3 @ z)), \
        (lambda m, z: np.tanh(W2 @ m + W3 @ z))


def cg_d():
    """10 -> 4; readout multiplies by its memory (running max of |z|)."""
    return vw.CoarseGrain(phi=lambda z, m: z[:4] * m + m ** 2,
                          init_memory=lambda z: jnp.abs(z[:4]),
                          update_memory=lambda m, z: jnp.maximum(m, jnp.abs(z[:4])), name="D")


def np_d():
    return (lambda z, m: z[:4] * m + m ** 2), (lambda z: np.abs(z[:4])), (lambda m, z: np.maximum(m, np.abs(z[:4])))


def reference(xs, twins):
    """Definition 4 cascade on a level-0 trajectory xs (T+1, 24): returns the top level (T+1, d)."""
    mem, out = [None] * len(twins), []
    for t, x in enumerate(xs):
        y = x
        for j, (phi, m0, upd) in enumerate(twins):
            if m0 is not None:
                mem[j] = m0(y) if t == 0 else upd(mem[j], y)
            y = phi(y, mem[j])
        out.append(flat_a(y) if isinstance(y, dict) else np.asarray(y))
    return np.stack(out)


def base_spec(burn_in=0):
    lg = ring()
    return vw.WorldSpec(base=lg.level(), chain=(), inport=vw.InputPort(admissible=lg.inputs),
                        outport=vw.ObservePort(noise=0.0), replay="full", burn_in=burn_in)


def top_and_x(spec, T=12, B=3):
    w = vw.World(spec, 5)
    d = w.designer
    P = d.program_dense(PROG, T)
    _, rec = d.rollout(d.ensemble(B, seed=9), P, T=T, rec=("x", "clean"))
    inv = np.argsort(w.out_map)
    return rec["x"], rec["clean"][..., inv] * w.out_sign[inv], w


def test_stacking_associativity_adversarial():
    a, b, c, d = cg_a(), cg_b(), cg_c(), cg_d()
    I = vw.identity()
    C = vw.compose
    base = base_spec()
    brackets = {
        "((ab)c)d": C(C(C(a, b), c), d),
        "a(b(cd))": C(a, C(b, C(c, d))),
        "(ab)(cd)": C(C(a, b), C(c, d)),
        "a((bc)d)": C(a, C(C(b, c), d)),
        "all": vw.compose_all([a, b, c, d]),
        "with ids": C(C(I, a), C(C(b, I), C(I, C(c, C(d, I))))),
    }
    specs = {k: vw.stack(base, v) for k, v in brackets.items()}
    specs["nested stacks"] = vw.stack(vw.stack(vw.stack(vw.stack(base, a), b), c), d)
    specs["mixed"] = vw.stack(vw.stack(base, C(a, b)), C(c, d))
    twins = [np_a(), np_b(), np_c(), np_d()]
    ref_x = None
    tops = {}
    for k, s in specs.items():
        x, top, w = top_and_x(s)
        if ref_x is None:
            ref_x = x
        assert np.array_equal(x, ref_x), k                       # same level-0 path in every world
        ref = np.stack([reference(x[i], twins) for i in range(x.shape[0])])
        assert top.shape == ref.shape == (3, 13, 4), (k, top.shape)
        assert np.allclose(top, ref, rtol=1e-12, atol=1e-12), (k, np.abs(top - ref).max())
        tops[k] = top
    for k in tops:
        assert np.allclose(tops[k], tops["((ab)c)d"], rtol=0, atol=1e-12), k
    # stack(at=2) on the 4-level chain drops levels 3, 4 and equals stacking e on level 2 directly
    e = vw.CoarseGrain.of(lambda z: jnp.cumsum(z)[::3], name="E")
    four = specs["nested stacks"]
    s_at = vw.stack(four, e, at=2)
    assert len(s_at.chain) == 3 and s_at.k_obs == 3
    x, top, _ = top_and_x(s_at)
    ref = np.stack([reference(x[i], twins[:2] + [((lambda z, m: np.cumsum(z)[::3]), None, None)])
                    for i in range(x.shape[0])])
    assert np.allclose(top, ref, rtol=1e-12, atol=1e-12)
    # a broken cascade (memory of c fed the OLD output of the levels below) must be detected
    bad = [np_a(), np_b(), (np_c()[0], np_c()[1], None), np_d()]
    x, top, _ = top_and_x(specs["all"])
    alt = []
    for i in range(x.shape[0]):
        mem, rows, prev = [None] * 4, [], None
        for t, xx in enumerate(x[i]):
            y, ys = xx, []
            for j, (phi, m0, upd) in enumerate(twins):
                if m0 is not None:
                    if t == 0:
                        mem[j] = m0(y)
                    else:
                        mem[j] = upd(mem[j], prev[j] if j == 2 else y)   # stale input to c
                ys.append(y)
                y = phi(y, mem[j])
            prev = ys
            rows.append(np.asarray(y))
        alt.append(np.stack(rows))
    assert not np.allclose(top, np.stack(alt), atol=1e-6)        # the comparison has power
    del bad


# ---------------------------------------------------------------- stride
def nl_level():
    def init(p, key):
        k1, k2 = jax.random.split(key)
        return (jax.random.normal(k1, (5,)), jax.random.uniform(k2, ()))

    def step(p, x, nz, u):
        v, s = x
        k1, k2 = jax.random.split(nz.rng())
        v2 = jnp.tanh(1.5 * v + u + 0.3 * jax.random.normal(k1, (5,))) * (1.0 + 0.1 * jax.random.uniform(k2, (5,)))
        s2 = 0.9 * s + jnp.sum(v2) * nz.stream(3).normal()
        return (v2, s2)
    return vw.Level(init=init, step=step, input_dim=5, name="nl")


def hand_stride(L, x, key, U, n, t0=0):
    """x(t+1) = L.step^n with Noise(key, n*t + k) and the input at k = 0 only."""
    xs = [x]
    for t, u in enumerate(U):
        for k in range(n):
            # the library's clock is an int64 that fold_in truncates to 32 bits (documented wrap)
            x = L.step(None, x, vw.Noise(key, (n * (t0 + t) + k) % 2 ** 32), u if k == 0 else jnp.zeros_like(u))
        xs.append(x)
    return jax.tree_util.tree_map(lambda *a: jnp.stack(a), *xs)


def test_stride_composition_adversarial():
    L = nl_level()
    key, k0 = vw.make_key(77, 1), vw.make_key(77, 2)
    x0 = L.init(None, k0)
    U = jnp.asarray(np.random.default_rng(3).normal(size=(5, 5)))
    S = vw.stride_level
    runs = {"(2)3": S(S(L, 2), 3), "(3)2": S(S(L, 3), 2), "6": S(L, 6), "((1)6)1": S(S(S(L, 1), 6), 1)}
    ref = hand_stride(L, x0, key, U, 6)
    for k, Ls in runs.items():
        tr = Ls.simulate(x0, key, U)
        for a, b in zip(jax.tree_util.tree_leaves(tr), jax.tree_util.tree_leaves(ref)):
            assert np.allclose(a, b, rtol=1e-13, atol=1e-13), (k, np.abs(np.asarray(a) - np.asarray(b)).max())
    # the comparison has power: input at every sub-step, or clock 6t+k with k reversed, differ
    bad = [x0]
    x = x0
    for t, u in enumerate(U):
        for k in range(6):
            x = L.step(None, x, vw.Noise(key, 6 * t + (5 - k)), u if k == 0 else jnp.zeros(5))
        bad.append(x)
    assert not np.allclose(np.stack([b[0] for b in bad]), ref[0], atol=1e-6)
    # a clock near the 32-bit wrap: a single strided tick at t = 2**31 + 5
    t_big = 2 ** 31 + 5
    xa = S(S(L, 2), 3).step(None, x0, vw.Noise(key, t_big), U[0])
    xb = S(L, 6).step(None, x0, vw.Noise(key, t_big), U[0])
    xc = hand_stride(L, x0, key, U[:1], 6, t0=t_big)
    for a, b, c in zip(jax.tree_util.tree_leaves(xa), jax.tree_util.tree_leaves(xb), jax.tree_util.tree_leaves(xc)):
        assert np.allclose(a, b, atol=1e-13) and np.allclose(a, np.asarray(c)[-1], atol=1e-13)
    # inside products (the factor streams fold in before or after the sub-step clock)
    L2 = ring().level()
    P = vw.product_level(L, L2)
    xp = (x0, L2.init(None, vw.make_key(77, 3)))
    Up = jnp.asarray(np.random.default_rng(4).normal(size=(4, 5 + 24)))
    t1 = S(S(P, 3), 2).simulate(xp, key, Up)
    t2 = vw.product_level(S(L, 6), S(L2, 6)).simulate(xp, key, Up)
    t3 = vw.product_level(S(S(L, 2), 3), S(L2, 6)).simulate(xp, key, Up)
    for a, b, c in zip(jax.tree_util.tree_leaves(t1), jax.tree_util.tree_leaves(t2), jax.tree_util.tree_leaves(t3)):
        assert np.allclose(a, b, atol=1e-12) and np.allclose(a, c, atol=1e-12)


def test_stride_world_level_with_memory_and_odd_burn_in():
    a = cg_a()
    for burn in (0, 7, 13):
        spec = vw.stack(base_spec(burn_in=burn), vw.compose(a, cg_b())).replace(
            outport=vw.ObservePort(noise=0.3))
        o = {k: vw.World(s, 2).run(PROG, [0, 1, 4, 9, 11], seed=4)
             for k, s in {"(2)3": vw.stride(vw.stride(spec, 2), 3), "(3)2": vw.stride(vw.stride(spec, 3), 2),
                          "6": vw.stride(spec, 6)}.items()}
        assert np.allclose(o["(2)3"], o["6"], atol=1e-12) and np.allclose(o["(3)2"], o["6"], atol=1e-12), burn
    w0 = vw.World(spec, 2).run(PROG, [0, 3, 10], seed=1)
    w1 = vw.World(vw.stride(spec, 1), 2).run(PROG, [0, 3, 10], seed=1)
    assert np.allclose(w0, w1, atol=1e-13)
