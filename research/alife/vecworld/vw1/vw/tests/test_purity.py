"""Purity and determinism by key: pure step functions, jit = eager, vmap = loop, results depend only
on (params, state, key, input) and never on host-side episode state."""
import jax
import jax.numpy as jnp
import numpy as np

import vw
from vw.lingauss import ring
from vw.toys import mass_ring, mass_ring_level


def test_level_step_is_pure_jittable_and_vmappable():
    for L in (ring().level(), mass_ring_level(16)):
        p = L.params
        x = L.init(p, vw.make_key(1))
        u = jnp.zeros(L.input_dim).at[2].set(0.3).at[5].set(-0.3)
        nz = vw.Noise(vw.make_key(2), 7)
        a, b = L.step(p, x, nz, u), L.step(p, x, nz, u)
        c = jax.jit(L.step)(p, x, nz, u)
        assert np.array_equal(a, b) and np.allclose(a, c, atol=1e-14)
        assert not np.array_equal(a, L.step(p, x, vw.Noise(vw.make_key(2), 8), u))   # the clock matters
        keys = vw.member_keys(vw.make_key(3), 5)
        xs = jax.vmap(lambda k: L.step(p, x, vw.Noise(k, 0), u))(keys)
        for j in range(5):
            assert np.allclose(xs[j], L.step(p, x, vw.Noise(keys[j], 0), u), atol=1e-14)


def test_simulation_independent_of_host_episode_state():
    w = ring().world(0)
    d = w.designer
    e = d.ensemble(6, seed=4)
    P = d.program_dense([(0, {0: 0.5, 1: -0.5}), (3, {2: 1.0, 5: -1.0})], 6)
    _, r1 = d.rollout(e, P, T=6, rec=("obs", "x"))
    w.reset(1)
    w.step({3: 0.4, 4: -0.4})
    w.run([(1, {0: 0.5, 1: -0.5})], [3])
    _, r2 = d.rollout(e, P, T=6, rec=("obs", "x"))
    assert np.array_equal(r1["obs"], r2["obs"]) and np.array_equal(r1["x"], r2["x"])
    _, r3 = d.rollout(d.ensemble(6, seed=4), P, T=6, rec=("obs",))
    assert np.array_equal(r1["obs"], r3["obs"])


def test_determinism_by_key_across_instances():
    spec = mass_ring().replace(replay="full")
    prog = [(0, {0: 0.5, 1: -0.5}), (2, {3: 0.25, 2: -0.25})]
    a = vw.World(spec, 7).run(prog, [0, 2, 5], seed=3)
    b = vw.World(spec, 7).run(prog, [0, 2, 5], seed=3)
    c = vw.World(spec, 7).run(prog, [0, 2, 5], seed=4)
    assert np.array_equal(a, b) and not np.allclose(a, c)


def test_replicas_do_not_share_hidden_trajectories():
    """Same law, different world seeds, same episode seed: different hidden states (VW-0 shared them,
    which let an agent align replicas and read off the relative permutation)."""
    spec = ring().spec()
    w0, w1 = vw.World(spec, 0), vw.World(spec, 1)
    w0.reset(5), w1.reset(5)
    x0, x1 = w0.designer.state()["x_flat"], w1.designer.state()["x_flat"]
    assert not np.allclose(np.sort(x0), np.sort(x1))


def test_batch_member_equals_single_member_run():
    w = mass_ring().replace(replay="full")
    w = vw.World(w, 0)
    d = w.designer
    e = d.ensemble(8, seed=2)
    P = d.program_dense([(1, {0: 0.5, 1: -0.5})], 5)
    _, rb = d.rollout(e, P, T=5, rec=("obs", "x"))
    one = vw.Ensemble(w, jax.tree_util.tree_map(lambda a: a[3:4], e.carry), e.t)
    _, r1 = d.rollout(one, P, T=5, rec=("obs", "x"))
    assert np.allclose(rb["obs"][3], r1["obs"][0], atol=1e-14) and np.allclose(rb["x"][3], r1["x"][0], atol=1e-14)


def test_world_tick_is_a_pure_function_of_explicit_arguments():
    w = ring().world(0)
    c = w.designer.ensemble(1, seed=1).carry
    c1 = jax.tree_util.tree_map(lambda a: a[0], c)
    a = jnp.zeros(w.n_in).at[0].set(0.5).at[1].set(-0.5)
    t1 = w._tick(w.params, c1, a)
    t2 = jax.jit(w._tick)(w.params, c1, a)
    assert np.allclose(t1.x, t2.x, atol=1e-14) and int(t1.t) == 1
    assert np.array_equal(w._obs(t1), w._obs(t1))
