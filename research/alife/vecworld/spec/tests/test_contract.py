"""Contract tests: agent API, constraint enforcement, anonymisation, noise, composition plumbing."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vecworld as vw  # noqa: E402
from lingauss import ClosedForms, ring  # noqa: E402


def toy(n0=6, n1=6, inputs=None, **kw):
    """Deterministic identity world: level 0 never moves on its own; Phi = first n1 coords."""
    return vw.WorldSpec(n0=n0, n1=n1, law=lambda h, xi: h, coarse=lambda h, m: h[:, :n1].copy(),
                        init=lambda rng: np.zeros(n0),
                        inputs=inputs or vw.InputConstraints(lo=-10, hi=10), **kw)


def test_card_reveals_no_structure():
    w = ring().world(0)
    c = w.card()
    assert c["n_in"] == 24 and c["n_obs"] == 6 and c["contract"] == "VW-0"
    flat = repr(c)
    assert "in_map" not in flat and "out_map" not in flat and "n0" not in c


def test_permutation_semantics():
    w = vw.VectorWorld(toy(), world_seed=5)
    assert sorted(w.in_map) == list(range(6)) and sorted(w.out_map) == list(range(6))
    assert not np.array_equal(w.in_map, np.arange(6))       # seed 5 gives a non-trivial permutation
    w.reset(0)
    o = w.step({2: 1.5})
    st = w.designer.state()
    assert st["h0"][w.in_map[2]] == 1.5 and np.count_nonzero(st["h0"]) == 1
    assert np.allclose(o, st["h1"][w.out_map])


def test_dense_and_sparse_inputs_agree():
    a, b = vw.VectorWorld(toy(), 1), vw.VectorWorld(toy(), 1)
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
    before = (w.ticks_used, w.t, w.designer.state()["h0"].copy())
    with pytest.raises(vw.InputViolation) as e:
        w.step(bad)
    assert "rejected" in str(e.value) or "format" in str(e.value)
    after = (w.ticks_used, w.t, w.designer.state()["h0"])
    assert before[0] == after[0] and before[1] == after[1] and np.array_equal(before[2], after[2])


def test_other_constraint_families():
    C = vw.InputConstraints(k=3, lo=-1, hi=1, total=1.0, min_interval=3, quantum=0.25, episode_budget=1.5)
    w = vw.VectorWorld(toy(inputs=C), 0)
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
    spec = ring().spec()
    spec.max_ticks = 5
    w = vw.VectorWorld(spec, 0)
    w.reset(0)
    for _ in range(3):
        w.step()
    with pytest.raises(vw.BudgetExhausted):
        w.run([], [3], seed=1)                       # needs 3 more ticks
    assert w.ticks_used == 3 and w.t == 3
    w.step(), w.step()
    with pytest.raises(vw.BudgetExhausted):
        w.step()
    assert w.ticks_used == 5


def test_run_equals_steps_and_validates_whole_program():
    spec = ring().spec()
    spec.replay = "full"
    w = vw.VectorWorld(spec, 2)
    prog = [(0, {0: 0.5, 3: -0.5}), (2, {5: 1.0, 7: -1.0}), (6, {1: -0.2, 2: 0.2})]
    out = w.run(prog, [0, 1, 3, 7, 9], seed=11)
    o = [w.reset(11)]
    pd = dict(prog)
    for t in range(9):
        o.append(w.step(pd.get(t)))
    assert np.allclose(out, np.stack([o[q] for q in [0, 1, 3, 7, 9]]))
    used = w.ticks_used
    bad = prog + [(8, {0: 0.5, 1: -0.6})]           # last entry not zero-sum
    with pytest.raises(vw.InputViolation, match="t=8"):
        w.run(bad, [9], seed=11)
    with pytest.raises(vw.InputViolation, match="after the last query"):
        w.run([(5, {0: 0.5, 1: -0.5})], [5], seed=11)
    with pytest.raises(vw.InputViolation, match="two program entries"):
        w.run([(1, {0: 0.5, 1: -0.5}), (1, {2: 0.5, 3: -0.5})], [5], seed=11)
    assert w.ticks_used == used


def test_max_queries():
    spec = toy(observation=vw.ObservationSpec(max_queries=2))
    w = vw.VectorWorld(spec, 0)
    w.run([], [1, 2], seed=0)
    with pytest.raises(vw.InputViolation, match="max_queries"):
        w.run([], [1, 2, 3], seed=0)


def test_replay_modes():
    def two(mode):
        spec = ring().spec()
        spec.replay = mode
        w = vw.VectorWorld(spec, 0)
        w.reset(4)
        h_a = w.designer.state()["h0"]
        oa = [w.step() for _ in range(3)]
        w.reset(4)
        h_b = w.designer.state()["h0"]
        ob = [w.step() for _ in range(3)]
        return np.array_equal(h_a, h_b), np.allclose(oa, ob)
    assert two("full") == (True, True)
    assert two("initial") == (True, False)
    assert two("none") == (False, False)


def test_noise_is_independent_of_ensemble_size():
    w = ring().world(0)
    d = w.designer
    a, b = d.ensemble(1, seed=9), d.ensemble(40, seed=9)
    for _ in range(5):
        a.step(), b.step()
    assert np.allclose(a.h0[0], b.h0[0]) and np.allclose(a.observe()[0], b.observe()[0])


def test_branches_share_noise_and_linear_response_is_exact():
    lg = ring()
    w = lg.world(0)
    w.reset(1)
    w.step({0: 0.5, 1: -0.5})
    d = w.designer
    br = d.branch(rep=3)
    a = np.zeros((3, w.n_in))
    a[1, 4], a[1, 9] = 1.0, -1.0
    br.step(a)
    for _ in range(4):
        br.step()
    assert np.allclose(br.h0[0], br.h0[2])                 # identical noise, same input
    cf = ClosedForms(lg, w)
    G = cf.Ca @ np.linalg.matrix_power(lg.A, 5) @ cf.Ba     # input at tick t, observed 5 ticks later
    assert np.allclose(br.h1_agent()[1] - br.h1_agent()[0], G @ a[1])
    fr = d.branch(rep=2, fresh=True)
    fr.step()
    assert not np.allclose(fr.h0[0], fr.h0[1])


def test_sampled_inputs_are_admissible():
    rng = np.random.default_rng(0)
    for C in [vw.InputConstraints(k=2, zero_sum=True), vw.InputConstraints(k=5, lo=0, hi=2, total=3),
              vw.InputConstraints(k=4, lo=-1, hi=1, zero_sum=True, quantum=0.25, total=2),
              vw.InputConstraints(k=3, lo=-0.5, hi=0.5)]:
        for _ in range(200):
            a = C.sample(rng, 17)
            assert a and not C.violations(a, 0, None, 0.0)


def test_conservation_with_zero_sum_inputs_and_actuation_noise():
    lg = ring(conserve=True)
    spec = lg.spec()
    spec.inputs = vw.InputConstraints(k=4, lo=-1, hi=1, zero_sum=True, noise=0.3)
    w = vw.VectorWorld(spec, 0)
    w.reset(0)
    m0 = w.designer.state()["h0"].sum()
    rng = np.random.default_rng(1)
    for _ in range(20):
        w.step(spec.inputs.sample(rng, w.n_in))
    assert abs(w.designer.state()["h0"].sum() - m0) < 1e-9
    assert w.designer.invariant_drift(T=30, B=8)["total"] < 1e-9


def test_sign_flip_option():
    w = vw.VectorWorld(toy(observation=vw.ObservationSpec(sign_flip=True)), 3)
    w.reset(0)
    o = w.step({0: 1.0})
    st = w.designer.state()
    assert set(np.unique(w.out_sign)) <= {-1.0, 1.0}
    assert np.allclose(o, st["h1"][w.out_map] * w.out_sign)


def test_composition_plumbing():
    a, b = toy(4, 2), toy(3, 3)
    p = vw.product(a, b)
    assert (p.n0, p.n1, p.n_u) == (7, 5, 7)
    h = np.arange(7.0)[None]
    assert np.allclose(p.coarse(h, np.zeros((1, 0))), [[0, 1, 4, 5, 6]])
    # stack: level 2 = sum of level 1
    lg = ring()
    st = vw.stack(lg.spec(), lambda h1, m: h1.sum(1, keepdims=True), 1)
    ws, wr = vw.VectorWorld(st, 0), vw.VectorWorld(lg.spec(), 0)
    e = ws.designer.ensemble(3, seed=1)
    assert np.allclose(e.h1()[:, 0], (e.h0 @ lg.C.T).sum(1))
    # stride: one strided tick = s ticks
    s3 = vw.VectorWorld(vw.stride(lg.spec(), 3), 0)
    x = s3.designer.ensemble(2, seed=2)
    y = wr.designer.from_states(x.h0)
    x.step()                                          # strided noise = 3 sub-tick blocks
    z = y.h0
    rng_noise = vw._rng(vw._S_PROC, *x.seed, 0).standard_normal((2, 3 * lg.Lq.shape[1]))
    for i in range(3):
        z = z @ lg.A.T + rng_noise[:, i * lg.Lq.shape[1]:(i + 1) * lg.Lq.shape[1]] @ lg.Lq.T
    assert np.allclose(x.h0, z)
    # refine with lifted actuation: psi(x + lift(u)) = psi(x) + u
    from lingauss import lumpable_refinement
    Af, Psi, Qf, Lam = lumpable_refinement(lg)
    rf = vw.refine(lg.spec(), law=lambda h, xi: h @ Af.T, n_fine=48, psi=lambda x: x @ Psi.T,
                   init=lambda rng: np.zeros(48), noise_dim=0, lift=lambda u: u @ Lam.T)
    wf = vw.VectorWorld(rf, 0)
    assert wf.n_in == 24
    xs = np.random.default_rng(0).standard_normal((1, 48))
    u = np.random.default_rng(1).standard_normal((1, 24))
    assert np.allclose(rf.kick(xs, u) @ Psi.T, xs @ Psi.T + u)


def test_diffusive_coupling_conserves():
    J = vw.diffusive_coupling([3, 3, 3], [(0, 1), (1, 2)], coords=[0], kappa=0.2)
    h = np.random.default_rng(0).standard_normal((4, 9))
    assert np.allclose(J(h).sum(1), 0)
