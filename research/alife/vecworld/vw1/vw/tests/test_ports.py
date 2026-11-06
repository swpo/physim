"""Constraint enforcement: the zero-sum tolerance case from the VW-0 review (an accepted input must
never create mass in a conserving world), canonicalisation, value steps, saturation for couplings."""
import numpy as np
import pytest

import vw
from vw.lingauss import ring
from vw.toys import additive_kick, mass_ring, pool_kick


def _near_tolerance_command(w, src_cell, snk_cell, amp=0.45, slack=9e-10):
    inv = np.empty(w.inport.n_u, int)
    inv[w.in_map] = np.arange(w.n_in)
    return {int(inv[snk_cell]): amp, int(inv[src_cell]): -amp + slack}


@pytest.mark.parametrize("kick", ["additive", "pool"])
def test_accepted_near_zero_sum_never_creates_mass(kick):
    """VW-0 review: sum = 9e-10 with l1 = 0.9 < 1 passed the check (tol * max(1, l1)) and the kick
    then took its non-conserving branch, creating matter every tick. In VW-1 the accepted command is
    canonicalised to an exact zero sum before it reaches the world."""
    spec = mass_ring(kick=additive_kick if kick == "additive" else pool_kick,
                     inputs=vw.Admissible(k=8, lo=-1, hi=1, total=4, zero_sum=True))
    w = vw.World(spec, 0)
    w.reset(5)
    x = w.designer.state()["x_flat"]
    order = np.argsort(x)
    cmd = _near_tolerance_command(w, order[0], order[1])
    v = np.array(list(cmd.values()))
    assert abs(v.sum()) > 5e-10 and np.abs(v).sum() < 1
    assert not w.inport.admissible.violations(cmd)                       # accepted
    can = w.inport.admissible.canonical(cmd)
    assert abs(sum(can.values())) < 1e-16
    m0 = x.sum()
    for _ in range(25):
        w.step(cmd)
    x1 = w.designer.state()["x_flat"]
    assert abs(x1.sum() - m0) < 1e-12 * m0                                # no mass created
    if kick == "pool":
        assert x1.min() >= 0.0                                            # cannot remove what is not there
    # the same through a program, and the uncanonicalised slack would have been visible
    w.run([(t, cmd) for t in range(25)], [25], seed=5)
    assert abs(w.designer.state()["x_flat"].sum() - m0) < 1e-12 * m0
    assert 25 * 9e-10 > 1e3 * 1e-12 * m0


def test_zero_sum_outside_tolerance_rejected():
    w = vw.World(mass_ring(), 0)
    w.reset(0)
    with pytest.raises(vw.InputViolation, match="zero-sum"):
        w.step({0: 0.45, 1: -0.45 + 2e-9})
    assert w.ticks_used == 0


def test_pool_kick_conserves_for_any_input():
    import jax
    import jax.numpy as jnp
    rng = np.random.default_rng(0)
    for _ in range(50):
        x = jnp.asarray(rng.exponential(1.0, 16) * (rng.random(16) < 0.6))
        u = jnp.asarray(rng.normal(0, 2, 16) * (rng.random(16) < 0.4))
        y = jax.jit(pool_kick)(x, u)
        assert abs(float(y.sum() - x.sum())) < 1e-12 and float(y.min()) >= 0


def test_value_step_with_zero_sum():
    C = vw.Admissible(k=4, lo=-1, hi=1, zero_sum=True, quantum=0.25)
    assert not C.violations({0: 0.5, 1: -0.25, 2: -0.25 + 1e-9})
    assert C.violations({0: 0.5, 1: -0.25})                              # quanta sum to 1
    can = C.canonical({0: 0.5, 1: -0.25, 2: -0.25 + 1e-9})
    assert can == {0: 0.5, 1: -0.25, 2: -0.25}


def test_canonical_is_identity_without_zero_sum_or_quantum():
    C = vw.Admissible(k=3, lo=-1, hi=1)
    a = {0: 0.3, 4: -0.7}
    assert C.canonical(a) == a


def test_saturate_maps_into_admissible_set():
    import jax
    rng = np.random.default_rng(3)
    for C in [vw.Admissible(k=3, lo=-1, hi=1, zero_sum=True, total=1.5),
              vw.Admissible(k=2, lo=0, hi=2, total=3), vw.Admissible(k=4, lo=-1, hi=1, zero_sum=True, quantum=0.25),
              vw.Admissible(lo=-0.5, hi=0.5)]:
        f = jax.jit(C.saturate)
        for _ in range(100):
            a = np.asarray(f(rng.normal(0, 2, 10)))
            d = {int(j): float(a[j]) for j in np.flatnonzero(a)}
            assert not C.violations(d), (C, d, C.violations(d))


def test_inputs_reach_only_actuable_coordinates():
    lg = ring()
    spec = lg.spec().replace(inport=vw.InputPort(admissible=vw.Admissible(k=2, lo=-1, hi=1, zero_sum=True),
                                                 actuable=tuple(range(0, 24, 3))))
    w = vw.World(spec, 4)
    assert w.n_in == 8 and set(w.in_map) == set(range(0, 24, 3))
    assert w.card()["n_in"] == 8
