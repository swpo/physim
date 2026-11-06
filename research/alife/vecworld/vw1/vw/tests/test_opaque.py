"""Opaque blocks through pure_callback: they compose, run under jit/scan/vmap, stay deterministic by
key, and are refused by derivative-based certificates."""
import jax
import jax.numpy as jnp
import numpy as np
import pytest

import vw
from vw.toys import mass_ring_level, peak_init_np, peak_phi_np, peak_update_np


def tracker_world(n=32, batched=False):
    tr = vw.host_coarse_grain(peak_phi_np, (4,), peak_init_np, peak_update_np, (2,), batched=batched, name="peak")
    return vw.WorldSpec(base=mass_ring_level(n), chain=(tr,),
                        inport=vw.InputPort(admissible=vw.Admissible(k=4, lo=-1, hi=1, zero_sum=True)),
                        outport=vw.ObservePort(noise=0.05))


def test_opaque_tracker_matches_numpy_replay():
    w = vw.World(tracker_world(), 0)
    d = w.designer
    P = d.program_dense([(1, {0: 0.8, 1: -0.8}), (4, {5: 0.5, 9: -0.5})], 12)
    _, rec = d.rollout(d.ensemble(4, seed=1), P, T=12, rec=("x", "L1"))
    for b in range(4):
        X = rec["x"][b]
        m = peak_init_np(X[0])
        assert np.allclose(rec["L1"][b, 0], peak_phi_np(X[0], m))
        for t in range(1, 13):
            m = peak_update_np(m, X[t])
            assert np.allclose(rec["L1"][b, t], peak_phi_np(X[t], m))
    assert w.spec.opaque and not w.spec.differentiable


def test_opaque_blocks_refuse_derivatives():
    w = vw.World(tracker_world(), 0)
    with pytest.raises(vw.NotDifferentiable):
        w.designer.fisher(wrt=None, n=10)
    c = jax.tree_util.tree_map(lambda a: a[0], w.designer.ensemble(1, seed=0).carry)
    with pytest.raises(Exception, match="(?i)jvp|differentiat"):
        jax.grad(lambda x: w._clean(c._replace(x=x)).sum())(c.x)


def test_certificates_and_agent_api_run_on_opaque_worlds():
    w = vw.World(tracker_world(), 1)
    o = w.reset(0)
    assert o.shape == (4,)
    w.step({0: 0.5, 1: -0.5})
    cl = w.designer.closure((1, 2), (0, 1, 2), n_traj=300, n_oracle=100, n_rep=4, folds=2)
    assert np.all(np.isfinite(cl["Vu"]))


def test_batched_host_callback_equals_sequential():
    G = 8

    def block_max(x, m):
        return x.reshape(x.shape[:-1] + (G, -1)).max(-1)

    def spec(batched):
        return vw.WorldSpec(base=mass_ring_level(32), chain=(vw.host_coarse_grain(block_max, (G,), batched=batched),),
                            outport=vw.ObservePort(noise=0.0))
    ws, wb = vw.World(spec(False), 0), vw.World(spec(True), 0)
    _, rs = ws.designer.rollout(ws.designer.ensemble(5, seed=1), None, T=4, rec=("L1", "x"))
    _, rb = wb.designer.rollout(wb.designer.ensemble(5, seed=1), None, T=4, rec=("L1",))
    assert np.allclose(rs["L1"], rb["L1"])
    assert np.allclose(rs["L1"], rs["x"].reshape(5, 5, G, -1).max(-1))


def test_host_level_composes_and_is_deterministic_by_key():
    def init_fn(kd):
        return np.random.default_rng(kd.tolist()).normal(size=4)

    def step_fn(x, kd, u):
        return 0.9 * (x + u) + 0.1 * np.random.default_rng(kd.tolist()).normal(size=4)

    H = vw.host_level(init_fn, step_fn, (4,), 4, name="np-ar1")
    from vw.lingauss import ring
    r = ring()
    hs = vw.WorldSpec(base=H, chain=(vw.identity(),), inport=vw.InputPort(admissible=vw.Admissible(lo=-1, hi=1)),
                      outport=vw.ObservePort(noise=0.1), replay="full")
    pw = vw.stride(vw.product(hs, r.spec()), 2)
    w1, w2 = vw.World(pw, 3), vw.World(pw, 3)
    a = w1.run([(0, {0: 0.5})], [0, 1, 3], seed=2)
    b = w2.run([(0, {0: 0.5})], [0, 1, 3], seed=2)
    assert a.shape == (3, 4 + 6) and np.array_equal(a, b)
    assert pw.opaque and not pw.differentiable
    x0 = jnp.asarray(init_fn(np.array([0, 1], np.uint32)))
    t1 = H.simulate(x0, vw.make_key(5), T=3)
    t2 = H.simulate(x0, vw.make_key(5), T=3)
    assert np.array_equal(t1, t2)
