"""Tests for the membrane world (fast, 32^2 or 64^2):  python -m pytest -q test_membrane.py"""
import _paths  # noqa: F401
import jax
import jax.numpy as jnp
import numpy as np
import pytest

import vw
from vw.nats import kl_check, shift_llr
import membrane_jax as MJ
import membrane_world as MW


def _np_state(H, seed=3):
    SW = _paths.load_source()
    s = SW.init(seed, (H, H))
    return SW, {f: s[f].copy() for f in MJ.FIELDS}


@pytest.mark.parametrize("dt", [0.5, 1.0])
def test_native_step_matches_source(dt):
    SW, s = _np_state(32)
    SW.P["dt"] = dt
    cfg = MJ.Config(H=32, W=32, G=4, dt=dt)
    q = {k: jnp.asarray(v) for k, v in MJ.THETA.items()}
    ns = jax.jit(lambda x: MJ.make_native_step(cfg)(q, x, jnp.zeros((32, 32))))
    x = {f: jnp.asarray(v) for f, v in s.items()}
    for _ in range(5):
        x = ns(x)
        s = SW.step(s)
        for f in MJ.FIELDS:
            assert np.abs(np.asarray(x[f]) - s[f]).max() <= 1e-14 * max(np.abs(s[f]).max(), 1.0)


def test_level_tick_is_n_native_steps_without_noise():
    cfg = MJ.Config(H=32, W=32, G=4, n_sub=4, sigma_a=0.0)
    lev = MJ.make_level(cfg)
    q = lev.params
    x = lev.init(q, jax.random.key(0))
    y = lev.step(q, x, vw.Noise(jax.random.key(1), 0), jnp.zeros(cfg.m))
    ns = MJ.make_native_step(cfg)
    z = x
    for _ in range(4):
        z = ns(q, z, jnp.zeros((32, 32)))
    for f in MJ.FIELDS:
        np.testing.assert_allclose(np.asarray(y[f]), np.asarray(z[f]), rtol=0, atol=1e-14)


def test_channel_kl_matches_charge():
    cfg = MJ.Config(H=32, W=32, G=4, sigma_a=0.02)
    U = np.zeros((2, cfg.m))
    U[0, 3], U[1, 7] = 0.03, -0.05
    draw = jax.jit(jax.vmap(jax.vmap(lambda k, t, u: MJ.channel(cfg, vw.Noise(k, t), u), in_axes=(None, 0, 0)),
                            in_axes=(0, None, None)))
    Ut = np.asarray(draw(vw.member_keys(vw.make_key(1, 2), 3000), jnp.arange(2), jnp.asarray(U)))
    charge = MW.nats_budget(cfg).program_cost([(t, U[t]) for t in range(2)])
    kl = kl_check(shift_llr(Ut, U, cfg.sigma_a ** 2 * np.eye(cfg.m)), charge)
    assert abs(charge - (0.03 ** 2 + 0.05 ** 2) / (2 * 0.02 ** 2)) < 1e-12
    assert abs(kl["z"]) < 4


def test_input_adds_substrate_and_is_bump_shaped():
    cfg = MJ.Config(H=32, W=32, G=4, n_sub=2, sigma_a=0.0)
    lev = MJ.make_level(cfg)
    q = lev.params
    x = lev.init(q, jax.random.key(0))
    u = jnp.zeros(cfg.m).at[5].set(0.05)
    nz = vw.Noise(jax.random.key(1), 0)
    dS = np.asarray(lev.step(q, x, nz, u)["S"] - lev.step(q, x, nz, jnp.zeros(cfg.m))["S"])
    target = (0.05 * MJ.bump_basis(cfg)[5]).reshape(32, 32)
    assert np.unravel_index(np.argmax(dS), dS.shape) == np.unravel_index(np.argmax(target), target.shape)
    assert 0.7 < dS.sum() / target.sum() < 1.05


def test_cells_field_sums_to_phi():
    cfg = MJ.Config(H=32, W=32, G=4)
    x = MJ.make_init(cfg)({k: jnp.asarray(v) for k, v in MJ.THETA.items()}, jax.random.key(2))
    x["K"] = x["K"] * 3.0                                   # exceed 1 somewhere: the split clips K
    F = np.asarray(MW.cells_field(x))
    assert (F >= 0).all()
    np.testing.assert_allclose(F.sum(0), np.asarray(x["phi"]), atol=1e-15)


def test_population_level_two():
    K = 4
    p2 = MW.phi_population(K, tick_time=10.0, W=3, m_div=50.0)

    def y1(masses):
        T = np.zeros((K, vw.objects.NF))
        for i, m in enumerate(masses):
            if m is not None:
                T[i, 0], T[i, 1] = 1.0, m
        return jnp.asarray(np.concatenate([T.ravel(), np.zeros(5)]))
    seq = [y1([100, 50, None, None]), y1([60, 50, 40, None]), y1([60, 50, 40, 70]), y1([60, 50, 40, 70]),
           y1([60, None, 40, 70]), y1([60, 55, 40, 70])]
    m = p2.init_memory(seq[0])
    np.testing.assert_allclose(np.asarray(p2.phi(seq[0], m)), [2, 75, 0])
    outs = []
    for y in seq[1:]:
        m = p2.update_memory(m, y)
        outs.append(np.asarray(p2.phi(y, m)))
    np.testing.assert_allclose(outs[0], [3, 50, 0])                                  # new slot of 40 < m_div
    np.testing.assert_allclose(outs[1], [4, 55, 100 * 1 / ((3 + 4) * 10)])           # new slot of 70 counts
    np.testing.assert_allclose(outs[2], [4, 55, 100 * 1 / ((3 + 4 + 4) * 10)])
    np.testing.assert_allclose(outs[4], [4, 56.25, 100 * 1 / ((4 + 3 + 4) * 10)])    # W = 3: tick 2 dropped, slot 1 refilled
    L1 = np.stack([np.asarray(y) for y in seq])[None]
    np.testing.assert_allclose(MW.level2_from_level1(L1, K, 10.0, W=3, m_div=50.0)[0],
                               np.stack([np.asarray(p2.phi(seq[0], p2.init_memory(seq[0])))] + outs))


def test_world_runs_and_levels_stack():
    cfg = MJ.Config(H=64, W=64, G=8, n_sub=4)
    specs, parts = MW.build(cfg)
    w = MW.MapWorld(specs["population"], world_seed=0)
    d = w.designer
    ens = d.ensemble(2, seed=0)
    ens, r = d.rollout(ens, T=3, rec=("L1", "L2", "ev"))
    K = parts["tracker"].K
    assert r["L1"].shape == (2, 4, K * 12 + 5) and r["L2"].shape == (2, 4, 3) and r["ev"].shape == (2, 4, K, 2)
    T = r["L1"][..., :K * 12].reshape(2, 4, K, 12)
    np.testing.assert_allclose(r["L2"][..., 0], (T[..., 0] > 0.5).sum(-1))
    # the same numbers through plain vw.World (vmap batching)
    w2 = vw.World(specs["population"], world_seed=0)
    e2 = w2.designer.ensemble(2, seed=0)
    _, r2 = w2.designer.rollout(e2, T=3, rec=("L2",))
    np.testing.assert_allclose(r2["L2"], r["L2"], rtol=1e-9, atol=1e-9)
    assert w.card()["n_in"] == cfg.m and w.card()["n_obs"] == 3
