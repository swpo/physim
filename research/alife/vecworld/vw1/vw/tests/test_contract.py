"""Contract tests ported from spec/tests/test_contract.py: agent API, card, anonymisation, constraint
enforcement (nothing charged), replay, common random numbers, conservation."""
import jax.numpy as jnp
import numpy as np
import pytest

import vw
from vw.lingauss import ClosedForms, ring


def toy(n0=6, n1=6, inputs=None, observation=None, **kw):
    """Deterministic identity world: level 0 never moves on its own; Phi = first n1 coordinates."""
    base = vw.Level(init=lambda p, k: jnp.zeros(n0), step=lambda p, x, nz, u: x + u, input_dim=n0)
    return vw.WorldSpec(base=base, chain=(vw.CoarseGrain.of(lambda x: x[:n1]),),
                        inport=vw.InputPort(admissible=inputs or vw.Admissible(lo=-10, hi=10)),
                        outport=observation or vw.ObservePort(), **kw)


def test_card_reveals_no_structure():
    spec = ring().spec().replace(name="ring/objects12-K12-stride20")
    w = vw.World(spec, 0)
    c = w.card()
    assert c["n_in"] == 24 and c["n_obs"] == 6 and c["contract"] == "VW-1"
    flat = repr(c)
    for leak in ("in_map", "out_map", "objects", "K12", "stride", "ring", "n0", spec.base.name, spec.chain[0].name):
        assert leak not in flat, leak
    assert "n0" not in c and "name" not in c


def test_permutation_semantics():
    w = vw.World(toy(), world_seed=5)
    assert sorted(w.in_map) == list(range(6)) and sorted(w.out_map) == list(range(6))
    assert not np.array_equal(w.in_map, np.arange(6))
    w.reset(0)
    o = w.step({2: 1.5})
    st = w.designer.state()
    assert st["x_flat"][w.in_map[2]] == 1.5 and np.count_nonzero(st["x_flat"]) == 1
    assert np.allclose(o, st["observed"][w.out_map])


def test_dense_and_sparse_inputs_agree():
    a, b = vw.World(toy(), 1), vw.World(toy(), 1)
    a.reset(0), b.reset(0)
    v = np.zeros(6)
    v[[1, 4]] = [0.5, -2.0]
    assert np.allclose(a.step(v), b.step({1: 0.5, 4: -2.0}))


@pytest.mark.parametrize("bad", [
    {0: 0.5, 1: -0.25, 2: -0.25},   # 3 non-zeros > k=2
    {0: 1.5, 1: -1.5},              # out of bound
    {0: 0.5, 1: -0.4},              # not zero-sum
    {"a": 1.0},                     # bad key
    {30: 1.0, 0: -1.0},             # out of range
    {0: float("nan"), 1: 0.0},      # not finite
    np.zeros(5),                    # wrong dense length
])
def test_violations_rejected_without_charge(bad):
    w = ring().world(0)
    w.reset(3)
    w.step({0: 0.5, 1: -0.5})
    before = (w.ticks_used, w.t, w.designer.state()["x_flat"].copy(), w._spent)
    with pytest.raises(vw.InputViolation) as e:
        w.step(bad)
    assert "rejected" in str(e.value) or "format" in str(e.value)
    after = (w.ticks_used, w.t, w.designer.state()["x_flat"], w._spent)
    assert before[0] == after[0] and before[1] == after[1] and np.array_equal(before[2], after[2])
    assert before[3] == after[3]


def test_other_constraint_families():
    C = vw.Admissible(k=3, lo=-1, hi=1, total=1.0, min_interval=3, quantum=0.25, episode_budget=1.5)
    w = vw.World(toy(inputs=C), 0)
    w.reset(0)
    with pytest.raises(vw.InputViolation, match="total"):
        w.step({0: 0.75, 1: 0.5})
    with pytest.raises(vw.InputViolation, match="quantum"):
        w.step({0: 0.3})
    w.step({0: 0.75})                                # t=0 -> 1
    with pytest.raises(vw.InputViolation, match="interval"):
        w.step({1: 0.25})                            # t=1 < 0 + 3
    w.step(None), w.step(None)                       # t=3
    with pytest.raises(vw.InputViolation, match="budget"):
        w.step({1: 1.0})                             # 0.75 + 1.0 > 1.5
    w.step({1: 0.75})
    assert w.ticks_used == 4


def test_budget_exhaustion_charges_nothing():
    w = vw.World(ring().spec().replace(max_ticks=5), 0)
    w.reset(0)
    for _ in range(3):
        w.step()
    with pytest.raises(vw.BudgetExhausted):
        w.run([], [3], seed=1)
    assert w.ticks_used == 3 and w.t == 3
    w.step(), w.step()
    with pytest.raises(vw.BudgetExhausted):
        w.step()
    assert w.ticks_used == 5


def test_run_equals_steps_and_validates_whole_program():
    w = vw.World(ring().spec().replace(replay="full"), 2)
    prog = [(0, {0: 0.5, 3: -0.5}), (2, {5: 1.0, 7: -1.0}), (6, {1: -0.2, 2: 0.2})]
    out = w.run(prog, [0, 1, 3, 7, 9], seed=11)
    o = [w.reset(11)]
    pd = dict(prog)
    for t in range(9):
        o.append(w.step(pd.get(t)))
    assert np.allclose(out, np.stack([o[q] for q in [0, 1, 3, 7, 9]]), atol=1e-12)
    used = w.ticks_used
    bad = prog + [(8, {0: 0.5, 1: -0.6})]
    with pytest.raises(vw.InputViolation, match="t=8"):
        w.run(bad, [9], seed=11)
    with pytest.raises(vw.InputViolation, match="after the last query"):
        w.run([(5, {0: 0.5, 1: -0.5})], [5], seed=11)
    with pytest.raises(vw.InputViolation, match="two program entries"):
        w.run([(1, {0: 0.5, 1: -0.5}), (1, {2: 0.5, 3: -0.5})], [5], seed=11)
    assert w.ticks_used == used


def test_run_continues_episode_and_respects_interval():
    C = vw.Admissible(lo=-1, hi=1, min_interval=2)
    w = vw.World(toy(inputs=C), 0)
    w.reset(0)
    w.step({0: 1.0})                                 # input at t=0
    with pytest.raises(vw.InputViolation, match="interval"):
        w.run([(0, {1: 1.0})], [1])                  # would be at t=1
    o = w.run([(1, {1: 1.0})], [2])                  # at t=2: fine
    assert w.t == 3 and np.isclose(o[0][list(w.out_map).index(w.in_map[1])], 1.0)


def test_max_queries():
    w = vw.World(toy(observation=vw.ObservePort(max_queries=2)), 0)
    w.run([], [1, 2], seed=0)
    with pytest.raises(vw.InputViolation, match="max_queries"):
        w.run([], [1, 2, 3], seed=0)


def test_replay_modes():
    def two(mode):
        w = vw.World(ring().spec().replace(replay=mode), 0)
        w.reset(4)
        h_a = w.designer.state()["x_flat"]
        oa = [w.step() for _ in range(3)]
        w.reset(4)
        h_b = w.designer.state()["x_flat"]
        ob = [w.step() for _ in range(3)]
        return np.array_equal(h_a, h_b), np.allclose(oa, ob)
    assert two("full") == (True, True)
    assert two("initial") == (True, False)
    assert two("none") == (False, False)


def test_noise_is_independent_of_ensemble_size():
    d = ring().world(0).designer
    a, b = d.ensemble(1, seed=9), d.ensemble(40, seed=9)
    for _ in range(5):
        a, b = a.step(), b.step()
    assert np.allclose(a.x_flat()[0], b.x_flat()[0]) and np.allclose(a.observe()[0], b.observe()[0])


def test_branches_share_noise_and_linear_response_is_exact():
    lg = ring()
    w = lg.world(0)
    w.reset(1)
    w.step({0: 0.5, 1: -0.5})
    d = w.designer
    br = d.branch(rep=3)
    a = np.zeros((3, w.n_in))
    a[1, 4], a[1, 9] = 1.0, -1.0
    br = br.step(a)
    for _ in range(4):
        br = br.step()
    x = br.x_flat()
    assert np.allclose(x[0], x[2])                   # identical noise, same input
    cf = ClosedForms(lg, w)
    G = cf.Ca @ np.linalg.matrix_power(lg.A, 5) @ cf.Ba
    assert np.allclose(br.clean()[1] - br.clean()[0], G @ a[1])
    fr = d.branch(rep=2, fresh=True).step()
    assert not np.allclose(fr.x_flat()[0], fr.x_flat()[1])


def test_sampled_inputs_are_admissible():
    rng = np.random.default_rng(0)
    for C in [vw.Admissible(k=2, zero_sum=True), vw.Admissible(k=5, lo=0, hi=2, total=3),
              vw.Admissible(k=4, lo=-1, hi=1, zero_sum=True, quantum=0.25, total=2),
              vw.Admissible(k=3, lo=-0.5, hi=0.5)]:
        for _ in range(200):
            a = C.sample(rng, 17)
            assert a and not C.violations(a)


def test_conservation_with_zero_sum_inputs_and_actuation_noise():
    spec = ring(conserve=True).spec()
    spec = spec.replace(inport=vw.InputPort(admissible=vw.Admissible(k=4, lo=-1, hi=1, zero_sum=True), noise=0.3))
    w = vw.World(spec, 0)
    w.reset(0)
    m0 = w.designer.state()["x_flat"].sum()
    rng = np.random.default_rng(1)
    for _ in range(20):
        w.step(spec.inport.admissible.sample(rng, w.n_in))
    assert abs(w.designer.state()["x_flat"].sum() - m0) < 1e-9
    assert w.designer.invariant_drift(T=30, B=8)["total"] < 1e-9


def test_sign_flip_option():
    w = vw.World(toy(observation=vw.ObservePort(sign_flip=True)), 3)
    w.reset(0)
    o = w.step({0: 1.0})
    st = w.designer.state()
    assert set(np.unique(w.out_sign)) <= {-1.0, 1.0} and (w.out_sign < 0).any()
    assert np.allclose(o, st["observed"][w.out_map] * w.out_sign)


def test_quantised_and_clipped_observation():
    w = vw.World(toy(observation=vw.ObservePort(noise=0.01, quantum=0.5, clip=(-1.0, 1.0))), 0)
    w.reset(0)
    o = w.step({0: 3.0, 1: 0.3})
    assert np.all(np.abs(o) <= 1.0) and np.allclose(o / 0.5, np.round(o / 0.5))


def test_apparatus_change_and_lower_observation_level():
    spec = ring().spec()
    w = vw.World(spec, 2)
    w2 = vw.World(spec.with_ports(outport=vw.ObservePort(noise=0.5, quantum=0.1)), 2)
    assert w2.card()["observation"]["noise"] == 0.5 and np.array_equal(w.in_map, w2.in_map)
    w0 = vw.World(spec.replace(observe_at=0), 2)          # observe level 0 itself (a leaky apparatus)
    assert w0.n_obs == 24 and w0.reset(0).shape == (24,)
    with pytest.raises(ValueError):
        spec.replace(observe_at=2)
