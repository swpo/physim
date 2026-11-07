"""Tests of the fed-vortex port (cheap: 64^2, a few steps). Run: python -m pytest -q test_vortex.py

The numpy source is loaded with WORLD_P {"eps": 0.2, "mut_dt": 0.2, "lab_t": 0.1}, so labelling (t = 0.1)
and mutations (every 0.2 after it) fall within the first 40 native steps."""
import importlib.util
import json
import os
import sys

import _paths
import jax
import jax.numpy as jnp
import numpy as np
import pytest

import vw
import vortex_jax as VJ
import vortex_world as VW

FAST = {"eps": 0.2, "mut_dt": 0.2, "lab_t": 0.1}


@pytest.fixture(scope="module")
def src():
    os.environ["WORLD_P"] = json.dumps(FAST)
    sys.path.insert(0, _paths.LAB)
    from labkit import ops
    ops.WORKERS = 1
    spec = importlib.util.spec_from_file_location("srcworld_fast", _paths.SRC_SEL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_native_step_matches_source_with_events(src):
    H = 64
    s = src.init(3, (H, H))
    log = []

    class Rng:
        def __init__(self, r):
            self.r = r

        def random(self):
            u = self.r.random()
            log.append(u)
            return u
    s["mrng"] = Rng(s["mrng"])
    cfg = VJ.Config(H=H, W=H, lab_t=FAST["lab_t"], mut_dt=FAST["mut_dt"])
    ns = jax.jit(lambda x, u: VJ.make_native_step(cfg)({k: jnp.asarray(v) for k, v in VJ.THETA.items()}, x, u,
                                                        jnp.zeros((H, H))))
    n_mut = 0
    for i in range(40):
        x = {f: jnp.asarray(s[f]) for f in VJ.FIELDS} | {"t": jnp.asarray(s["t"])}
        before = len(log)
        s = src.step(s)
        u = log[-1] if len(log) > before else 0.5
        n_mut += len(log) > before
        y = ns(x, u)
        for f in VJ.FIELDS:
            scale = max(np.abs(s[f]).max(), 1e-300)
            assert np.abs(np.asarray(y[f]) - s[f]).max() <= 1e-13 * scale, (i, f)
        assert float(y["t"]) == s["t"]
    assert n_mut >= 3 and np.abs(s["b"]).max() > 0.1          # labelling and mutations happened


def test_channel_law_and_budget():
    cfg = VJ.Config(H=64, W=64, G=4)
    keys = vw.member_keys(vw.make_key(5), 3000)
    E = np.asarray(jax.vmap(lambda k: VJ.channel(cfg, vw.Noise(k, 3), jnp.zeros(cfg.m)))(keys))
    assert abs(E.std() / cfg.sigma_a - 1) < 0.02 and np.abs(E.mean(0)).max() < 5 * cfg.sigma_a / np.sqrt(3000)
    b = VW.nats_budget(cfg, tick=10.0)
    u = np.zeros(cfg.m)
    u[3] = 2 * cfg.sigma_a
    assert b.cost(u) == pytest.approx(2.0)
    basis = VJ.stir_basis(cfg)
    assert np.abs(basis.sum(1)).max() < 1e-9                          # zero mean: curl of a periodic force


def test_world_levels_and_stack():
    cfg = VJ.Config(H=64, W=64, G=4, n_sub=10)
    specs, parts = VW.build(cfg)
    w = vw.World(specs["kinds"], world_seed=0)
    d = w.designer
    ens = d.ensemble(2, seed=1)
    ens, r = d.rollout(ens, T=2, rec=("L1", "L2", "obs"))
    K = parts["tracker"].K
    assert r["L1"].shape == (2, 3, K * vw.objects.NF) and r["L2"].shape == (2, 3, 2) and r["obs"].shape == (2, 3, 2)
    np.testing.assert_allclose(r["L2"], np.asarray(VW.kinds(jnp.asarray(r["L1"]), K)))
    assert w.n_in == cfg.m and list(w.in_map) == list(range(cfg.m))
    p = np.asarray(jax.vmap(parts["phi_pooled"].phi, in_axes=(0, None))(ens.x, ()))
    assert p.shape == (2, 4 * 4 * 4)
