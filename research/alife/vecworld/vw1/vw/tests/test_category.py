"""Category laws of the composition operators, checked pathwise (shared noise) where they hold
pathwise and in distribution where they hold only in distribution."""
import jax
import jax.numpy as jnp
import numpy as np
import pytest

import vw
from vw.lingauss import ClosedForms, LinearGaussian, lumpable_level, random_lg, ring
from vw.toys import mass_ring

PROG = [(0, {0: 0.5, 3: -0.5}), (2, {5: 1.0, 7: -1.0}), (5, {1: -0.2, 2: 0.2})]


def _key(*i):
    return vw.make_key(99, *i)


# ----------------------------------------------------------------------------- memoryful test maps
def ema_blocks(alpha=0.3):
    """24 -> 12: block sums and their exponential moving average (memory)."""
    C = jnp.asarray(np.kron(np.eye(6), np.ones((1, 4))))
    return vw.CoarseGrain(phi=lambda x, m: jnp.concatenate([C @ x, m]), init_memory=lambda x: C @ x,
                          update_memory=lambda m, x: (1 - alpha) * m + alpha * (C @ x), name="ema")


def running_max():
    """12 -> 12: pairwise sums and their running maximum (memory)."""
    return vw.CoarseGrain(phi=lambda y, m: jnp.concatenate([y[:6] + y[6:], m]), init_memory=lambda y: y[:6] + y[6:],
                          update_memory=lambda m, y: jnp.maximum(m, y[:6] + y[6:]), name="max")


def summary(beta=0.5):
    """12 -> 4: three group sums and a smoothed grand total (memory)."""
    return vw.CoarseGrain(phi=lambda z, m: jnp.concatenate([z.reshape(3, 4).sum(1), m]),
                          init_memory=lambda z: z.sum()[None],
                          update_memory=lambda m, z: (1 - beta) * m + beta * z.sum()[None], name="sum")


def bare(lg):
    return vw.WorldSpec(base=lg.level(), chain=(), inport=vw.InputPort(admissible=lg.inputs),
                        outport=vw.ObservePort(noise=0.2), replay="full")


def _obs(spec, seed=0, prog=PROG, q=(0, 1, 3, 6, 9)):
    return vw.World(spec, 3).run(prog, list(q), seed=seed)


# ----------------------------------------------------------------------------- identity, associativity
def test_identity_coarse_graining_is_a_unit():
    spec = ring().spec().replace(replay="full")
    w0, w1 = vw.World(spec, 3), vw.World(vw.stack(spec, vw.identity()), 3)
    assert np.array_equal(w0.in_map, w1.in_map) and np.array_equal(w0.out_map, w1.out_map)
    assert np.array_equal(w0.run(PROG, [0, 1, 4, 9], seed=7), w1.run(PROG, [0, 1, 4, 9], seed=7))
    b = bare(ring())
    a = ema_blocks()
    ref = _obs(vw.stack(b, a))
    for c in (vw.compose(vw.identity(), a), vw.compose(a, vw.identity())):
        assert np.allclose(_obs(vw.stack(b, c)), ref, atol=1e-13)


def test_stacking_is_associative():
    b = bare(ring())
    a, m, s = ema_blocks(), running_max(), summary()
    left = vw.stack(b, vw.compose(vw.compose(a, m), s))
    right = vw.stack(b, vw.compose(a, vw.compose(m, s)))
    chain = vw.stack(vw.stack(vw.stack(b, a), m), s)
    o = _obs(left)
    assert o.shape == (5, 4)
    assert np.allclose(o, _obs(right), atol=1e-12)
    assert np.allclose(o, _obs(chain), atol=1e-12)
    assert len(vw.World(chain, 0).spec.chain) == 3            # three levels, observed at the top


# ----------------------------------------------------------------------------- product
def test_product_of_independent_levels_is_the_pair():
    A, B = ring().level(), random_lg().level()
    P = vw.product_level(A, B)
    k0, kn = _key(1), _key(2)
    x0 = P.init(P.params, k0)
    assert np.array_equal(x0[0], A.init(None, jax.random.fold_in(k0, 0)))
    assert np.array_equal(x0[1], B.init(None, jax.random.fold_in(k0, 1)))
    U = jnp.asarray(np.random.default_rng(0).normal(size=(7, A.input_dim + B.input_dim)))
    tr = P.simulate(x0, kn, U)
    ta = A.simulate(x0[0], jax.random.fold_in(kn, 0), U[:, :A.input_dim])
    tb = B.simulate(x0[1], jax.random.fold_in(kn, 1), U[:, A.input_dim:])
    assert np.array_equal(tr[0], ta) and np.array_equal(tr[1], tb)
    # the product world observes the pair of level-1 states and conserves each factor's invariant
    r, rl = ring(), random_lg()
    w = vw.World(vw.product(r.spec(), rl.spec()), 4)
    d = w.designer
    _, rec = d.rollout(d.ensemble(3, seed=1), None, T=3, rec=("x", "L1"))
    x = rec["x"]
    assert np.allclose(rec["L1"], np.concatenate([x[..., :24] @ r.C.T, x[..., 24:] @ rl.C.T], -1))
    assert set(w.spec.base.conserved) == {"0.total", "1.total"}
    assert w.n_in == 24 + 12 and w.card()["inputs"]["k"] == 2 + 3


def test_product_gap_is_additive_in_closed_form():
    r, rl = ring(), random_lg()
    g = lambda lg, w: ClosedForms(lg, w).closure((1, 2, 4), (0, 1, 4))["gap_nats"]  # noqa: E731
    wcat = vw.World(vw.product(r.spec(), rl.spec()), 4)
    assert np.allclose(g(LinearGaussian.concat(r, rl), wcat), g(r, r.world(0)) + g(rl, rl.world(0)), atol=1e-10)


def test_correlated_and_shared_noise_products():
    A = ring().level()
    k0, kn = _key(3), _key(4)
    x0 = vw.product_level(A, A).init({"0": None, "1": None}, k0)
    T = 5
    ind = vw.product_level(A, A).simulate(x0, kn, T=T)
    c0 = vw.product_level(A, A, noise=("correlated", 0.0)).simulate(x0, kn, T=T)
    assert np.allclose(ind[0], c0[0], atol=1e-14) and np.allclose(ind[1], c0[1], atol=1e-14)
    same = (x0[0], x0[0])
    for P in (vw.product_level(A, A, noise=("correlated", 1.0)), vw.product_level(A, A, noise="shared")):
        tr = P.simulate(same, kn, T=T)
        assert np.allclose(tr[0], tr[1], atol=1e-13)
    # correlation of the one-step noise is the declared rho
    P = vw.product_level(A, A, noise=("correlated", 0.6))
    z = (jnp.zeros(24), jnp.zeros(24))
    keys = vw.member_keys(_key(5), 6000)
    x1 = jax.vmap(lambda k: P.step(P.params, z, vw.Noise(k, 0), jnp.zeros(48)))(keys)
    a, b = np.asarray(x1[0]), np.asarray(x1[1])
    corr = np.mean([np.corrcoef(a[:, i], b[:, i])[0, 1] for i in range(24)])
    assert abs(corr - 0.6) < 0.02
    with pytest.raises(ValueError):
        vw.product_level(A, random_lg().level(), noise=("correlated", 0.5))


# ----------------------------------------------------------------------------- stride
def test_stride_composes_multiplicatively():
    L = ring().level()
    x0 = L.init(None, _key(6))
    U = jnp.asarray(np.random.default_rng(1).normal(size=(4, 24)))
    a = vw.stride_level(vw.stride_level(L, 2), 3).simulate(x0, _key(7), U)
    b = vw.stride_level(L, 6).simulate(x0, _key(7), U)
    c = vw.stride_level(vw.stride_level(L, 3), 2).simulate(x0, _key(7), U)
    assert np.allclose(a, b, atol=1e-12) and np.allclose(c, b, atol=1e-12)
    assert np.array_equal(vw.stride_level(L, 1).simulate(x0, _key(7), U), L.simulate(x0, _key(7), U))
    spec = ring().spec().replace(replay="full", burn_in=6)
    o1 = vw.World(vw.stride(vw.stride(spec, 2), 3), 1).run(PROG, [0, 2, 6], seed=3)
    o2 = vw.World(vw.stride(spec, 6), 1).run(PROG, [0, 2, 6], seed=3)
    assert np.allclose(o1, o2, atol=1e-12)


def test_stride_commutes_with_product():
    A, B = ring().level(), random_lg().level()
    P = vw.product_level(A, B)
    x0 = P.init(P.params, _key(8))
    U = jnp.asarray(np.random.default_rng(2).normal(size=(3, 40)))
    s1 = vw.stride_level(P, 4).simulate(x0, _key(9), U)
    s2 = vw.product_level(vw.stride_level(A, 4), vw.stride_level(B, 4)).simulate(x0, _key(9), U)
    assert np.allclose(s1[0], s2[0], atol=1e-12) and np.allclose(s1[1], s2[1], atol=1e-12)


def test_stride_equals_matrix_power():
    lg = ring(sigma=0.0)
    L = vw.stride_level(lg.level(), 5)
    x0 = jnp.asarray(np.random.default_rng(3).normal(size=24))
    u = np.zeros(24)
    u[3] = 1.0
    x1 = L.step(None, x0, vw.Noise(_key(1), 0), jnp.asarray(u))
    assert np.allclose(x1, np.linalg.matrix_power(lg.A, 5) @ (np.asarray(x0) + u))


# ----------------------------------------------------------------------------- refinement
def test_exact_refinement_has_zero_commutation_error():
    r = ring()
    _, fine, Psi = lumpable_level(r, eta=0.0)
    psi = vw.CoarseGrain.of(lambda x: jnp.asarray(Psi) @ x)
    rep = vw.commutation_error(fine, psi, r.level(), T=(1, 4), n=1000, n_rep=8)
    assert rep["delta2_pathwise"].max() < 1e-24
    assert np.abs(rep["delta2"]).max() < 0.05 * rep["mc_bias"].max()     # zero up to MC noise
    u = np.zeros(24)
    u[[2, 9]] = [0.7, -0.7]
    assert vw.commutation_error(fine, psi, r.level(), T=(1, 2), n=200, u=u, mode="pathwise")["delta2_pathwise"].max() < 1e-24
    spec = vw.refine(r.spec(), fine, psi, check=dict(T=(1,), n=500, n_rep=4), tol=1e-6)
    assert spec.meta["refine_check"]["delta2_pathwise"][0] < 1e-24
    assert len(spec.chain) == 2 and spec.k_obs == 2


def test_exact_refinement_is_invisible_at_level_one_pathwise():
    """Coupled initial states (h0 = Psi x) and shared member keys: the refined world's observations
    equal the base world's, tick by tick, under the same program."""
    r = ring()
    _, fine, Psi = lumpable_level(r, eta=0.0)
    psi = vw.CoarseGrain.of(lambda x: jnp.asarray(Psi) @ x)
    wf, wc = vw.World(vw.refine(r.spec(), fine, psi), 1), vw.World(r.spec(), 1)
    assert np.array_equal(wf.in_map, wc.in_map) and np.array_equal(wf.out_map, wc.out_map)
    x = jax.vmap(fine.init, in_axes=(None, 0))(None, vw.member_keys(_key(10), 16))
    keys = vw.member_keys(_key(11), 16)
    ef, ec = wf.designer.from_states(x, keys=keys), wc.designer.from_states(x @ jnp.asarray(Psi).T, keys=keys)
    P = wf.designer.program_dense(PROG, 8)
    _, of = wf.designer.rollout(ef, P, T=8)
    _, oc = wc.designer.rollout(ec, P, T=8)
    assert np.allclose(of["obs"], oc["obs"], atol=1e-11)


def test_leaky_refinement_commutation_matches_closed_form():
    r = ring()
    lgf, fine, Psi = lumpable_level(r, eta=0.3)
    psi = vw.CoarseGrain.of(lambda x: jnp.asarray(Psi) @ x)
    wf = vw.World(vw.refine(r.spec(), fine, psi), 0)
    exact = ClosedForms(lgf, wf).commutation_delta2(r, Psi, 1)
    rep = vw.commutation_error(fine, psi, r.level(), T=(1,), n=3000, n_rep=16)
    assert abs(rep["delta2_pathwise"][0] - exact) < 0.08 * exact          # T = 1: pathwise = distributional
    assert abs(rep["delta2"][0] - exact) < 0.1 * exact
    with pytest.raises(ValueError, match="commutation defect"):
        vw.refine(r.spec(), fine, psi, check=dict(T=(1,), n=500, n_rep=4), tol=1e-3)
    with pytest.raises(ValueError, match="input"):
        vw.refine(r.spec(), vw.Level(init=fine.init, step=lambda p, x, nz, u: x, input_dim=48), psi)


def test_defects_compose_by_the_triangle_inequality():
    """rms(psi2 o psi1) <= Lip(psi2) rms(psi1) + rms(psi2), with all three levels on shared noise."""
    r = ring()
    lg1, L1, Psi1 = lumpable_level(r, eta=0.3)
    lg2, L2, Psi2 = lumpable_level(lg1, eta=0.3)
    p1 = vw.CoarseGrain.of(lambda x: jnp.asarray(Psi1) @ x)
    p2 = vw.CoarseGrain.of(lambda x: jnp.asarray(Psi2) @ x)
    x = jax.vmap(L2.init, in_axes=(None, 0))(None, vw.member_keys(_key(12), 2000))
    kw = dict(T=(1,), mode="pathwise", seed=4)
    d21 = vw.commutation_error(L2, p2, L1, x0=x, **kw)["rms_pathwise"][0]
    d10 = vw.commutation_error(L1, p1, r.level(), x0=x @ jnp.asarray(Psi2).T, **kw)["rms_pathwise"][0]
    d20 = vw.commutation_error(L2, vw.compose(p2, p1), r.level(), x0=x, **kw)["rms_pathwise"][0]
    lip = np.linalg.norm(Psi1, 2)
    assert d21 > 0 and d10 > 0
    assert d20 <= lip * d21 + d10 + 1e-12


# ----------------------------------------------------------------------------- couple
def test_couple_with_zero_wire_is_the_independent_product():
    s, d = ring(), random_lg()
    C = vw.couple(s.spec(), d.spec(), wire=lambda y: jnp.zeros(16), saturate=True, readout_noise=0.0)
    P = vw.product_level(s.level(), d.level())
    x0 = C.base.init(C.base.params, _key(13))
    U = jnp.asarray(np.random.default_rng(4).normal(size=(5, 24)))
    tc = C.base.simulate(x0, _key(14), U)
    tp = P.simulate((x0[0], x0[2]), _key(14), jnp.concatenate([U, jnp.zeros((5, 16))], 1))
    assert np.array_equal(tc[0], tp[0]) and np.array_equal(tc[2], tp[1])


def test_couple_deterministic_cascade():
    s, d = ring(sigma=0.0), ring(sigma=0.0, gamma=0.1)
    W = np.random.default_rng(5).normal(size=(24, 6)) * 0.3
    C = vw.couple(s.spec(), d.spec(), wire=lambda y: jnp.asarray(W) @ y, saturate=False, readout_noise=0.0)
    xs, xd = np.random.default_rng(6).normal(size=(2, 24))
    U = np.random.default_rng(7).normal(size=(6, 24))
    tr = C.base.simulate((jnp.asarray(xs), ((),), jnp.asarray(xd)), _key(15), jnp.asarray(U))
    for t in range(6):
        wire_in = W @ (s.C @ xs)                      # the wire reads src before the laws run
        xs, xd = s.A @ (xs + U[t]), d.A @ (xd + wire_in)
        assert np.allclose(tr[0][t + 1], xs) and np.allclose(tr[2][t + 1], xd)


def test_couple_one_step_covariance():
    s, d = ring(sigma=0.3), ring(sigma=0.2)
    W = np.random.default_rng(8).normal(size=(24, 6)) * 0.3
    rr = 0.5
    C = vw.couple(s.spec(), d.spec(), wire=lambda y: jnp.asarray(W) @ y, saturate=False, readout_noise=rr)
    x0 = C.base.init(C.base.params, _key(16))
    keys = vw.member_keys(_key(17), 20000)
    x1 = jax.vmap(lambda k: C.base.step(C.base.params, x0, vw.Noise(k, 0), jnp.zeros(24)))(keys)
    Xd = np.asarray(x1[2])
    S_emp = np.cov(Xd.T)
    S_cf = rr ** 2 * d.A @ W @ W.T @ d.A.T + d.Q
    assert np.abs(S_emp - S_cf).max() < 0.05 * np.abs(S_cf).max()
    cross = np.asarray(x1[0]).T @ (Xd - Xd.mean(0)) / Xd.shape[0]
    assert np.abs(cross).max() < 0.05 * np.abs(S_cf).max()


def test_coupled_world_conserves_dst_mass_with_saturated_zero_sum_wire():
    src, dst = ring(), mass_ring(n=32, G=8)
    W = np.random.default_rng(9).normal(size=(32, 6))
    C = vw.couple(src.spec(), dst, wire=lambda y: jnp.asarray(W) @ y, saturate=True, observe="both")
    w = vw.World(C, 2)
    assert w.n_in == 24 and w.n_obs == 6 + 8
    o = w.reset(0)
    assert o.shape == (14,)
    w.step({0: 0.5, 1: -0.5})
    drift = w.designer.invariant_drift(T=20, B=8)
    assert drift["dst.mass"] < 1e-12
