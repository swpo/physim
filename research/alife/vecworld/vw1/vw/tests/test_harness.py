"""Tests for the exam harness v0: vw.secret, vw.nats, vw.scoring, vw.harness (new modules; existing
behaviour untouched)."""
import math

import jax
import numpy as np
import pytest

import vw
from vw.harness import HistoryExam, Lab, ProgramMix, blind_random, no_input
from vw.lingauss import ring
from vw.nats import (NatsAccountant, NatsBudget, card_guarantee, gaussian_kl, kl_check, shift_kl, shift_llr)
from vw.ports import BudgetExhausted, InputViolation
from vw.scoring import (cells_ok, crps_fair, energy_fair, energy_loo, energy_v1, oes, paired_gap, skill_report,
                        variogram, variogram_loo)
from vw.secret import Secret


# ----------------------------------------------------------------------------- secret
def test_secret_keys_are_not_public_keys():
    s = Secret(bytes(range(32)))
    k = jax.random.key_data(s.key("episode", 0))
    for ints in [(0,), (0, 0), (2, 0, 0), (0, 0, 0)]:
        assert not np.array_equal(k, jax.random.key_data(vw.make_key(*ints)))
    assert np.array_equal(k, jax.random.key_data(Secret(bytes(range(32))).key("episode", 0)))
    assert not np.array_equal(k, jax.random.key_data(Secret(bytes(range(1, 33))).key("episode", 0)))
    assert not np.array_equal(k, jax.random.key_data(s.key("episode", 1)))
    assert not np.array_equal(k, jax.random.key_data(s.key("exam", 0)))
    ks = s.keys(3, "x")
    assert np.array_equal(jax.random.key_data(ks[1]), jax.random.key_data(s.key("x", 1)))


def test_secret_entropy_and_hygiene():
    with pytest.raises(ValueError):
        Secret(b"\x00" * 15)                     # 120 bits
    s = Secret()
    assert s.bits == 256 and s.hex() not in repr(s)
    assert s.child("a").hex() != s.child("b").hex() != s.hex()
    assert 0 <= s.label("item", 3) < 2 ** 62 and s.label("item", 3) != s.label("item", 4)
    assert s.salted_hash(b"theta") != Secret().salted_hash(b"theta")
    with pytest.raises(TypeError):
        s.key(True)
    assert s.key("a", 1) is not None and not np.array_equal(jax.random.key_data(s.key("a", 1)),
                                                             jax.random.key_data(s.key("a1")))


# ----------------------------------------------------------------------------- nats
def test_nats_costs_and_null_directions():
    b = NatsBudget.isotropic(3, 0.5)
    assert b.cost([1.0, 0, 0]) == pytest.approx(2.0)
    assert b.cost({2: -0.5}) == pytest.approx(0.5)
    # zero-sum (conserved) noise: mass-changing inputs have infinite cost, zero-sum ones are finite
    n = 4
    S = np.eye(n) - np.ones((n, n)) / n
    c = NatsBudget.from_cov(S)
    assert math.isinf(c.cost([1.0, 0, 0, 0]))
    assert c.cost([1.0, -1.0, 0, 0]) == pytest.approx(0.5 * 2.0)
    assert c.null.shape == (4, 1)
    # embedding: u enters through E
    E = np.array([[1.0], [1.0]])
    e = NatsBudget.from_cov(np.diag([1.0, 4.0]), embed=E)
    assert e.cost([2.0]) == pytest.approx(0.5 * (4 + 1))


def test_accountant_caps_reject_before_charging():
    b = NatsBudget.isotropic(2, 1.0, tick=1.0, episode=1.5, total=2.0)
    a = NatsAccountant(b)
    a.new_episode()
    assert a.check([1.0, 0.0]) == pytest.approx(0.5)
    with pytest.raises(InputViolation, match="per-tick"):
        a.check([1.5, 0.0])
    a.charge([1.0, 0.0])
    a.charge([1.0, 0.0])
    assert a.check([1.0, 0.0]) == pytest.approx(0.5)      # 1.5 = the episode cap: allowed
    with pytest.raises(InputViolation, match="episode"):
        a.check([1.2, 0.0])
    assert a.episode_used == pytest.approx(1.0)
    a.new_episode()
    a.charge([1.0, 1.0])                         # 1.0 nats, total 2.0
    with pytest.raises(InputViolation, match="total"):
        a.check_program([(0, [0.1, 0.0])])
    assert a.total_used == pytest.approx(2.0) and a.usage()["total_left"] == pytest.approx(0.0)
    a2 = NatsAccountant(b)
    with pytest.raises(InputViolation, match="t=3"):
        a2.check_program([(0, [1.0, 0]), (1, [1.0, 0]), (2, [1.0, 0]), (3, [1.0, 0])])
    assert a2.total_used == 0.0


def test_shift_kl_closed_forms_and_mc():
    S = np.array([[1.0, 0.3], [0.3, 0.5]])
    s = np.array([0.4, -0.2])
    assert shift_kl([s], S) == pytest.approx(gaussian_kl(s, S, np.zeros(2), S))
    assert NatsBudget.from_cov(S).cost(s) == pytest.approx(shift_kl([s], S))
    # Monte Carlo log-likelihood ratio of a nonlinear chain x' = sin(x) + s_t + xi
    rng = np.random.default_rng(0)
    T, n = 3, 20000
    sh = np.array([[0.5, 0.0], [0.0, -0.3], [0.2, 0.2]])
    Lc = np.linalg.cholesky(S)
    x = rng.standard_normal((n, 2))
    res = np.zeros((n, T, 2))
    for t in range(T):
        xn = np.sin(x) + sh[t] + rng.standard_normal((n, 2)) @ Lc.T
        res[:, t] = xn - np.sin(x)
        x = xn
    chk = kl_check(shift_llr(res, sh, S), shift_kl(sh, S))
    assert abs(chk["z"]) < 4
    g = card_guarantee(8.0)
    assert g["linear_gaussian_mean_shift_in_sd"] == pytest.approx(4.0) and not g["chi2_bound_informative"]


# ----------------------------------------------------------------------------- scoring
def _es_exact_gauss(m, d, rng, n=400000):
    """ES of N(0, I_d) at y = m*1 (RMS norm), by large Monte Carlo."""
    X = rng.standard_normal((n, d))
    Xp = rng.standard_normal((n, d))
    y = np.full(d, m)
    return (np.linalg.norm(X - y, axis=1).mean() - 0.5 * np.linalg.norm(X - Xp, axis=1).mean()) / math.sqrt(d)


def test_fair_energy_unbiased_v1_biased():
    rng = np.random.default_rng(1)
    d, m, reps = 3, 4, 6000
    y = np.full((1, d), 0.7)
    X = rng.standard_normal((reps, m, d))
    Y = np.broadcast_to(y, (reps, 1, d))
    exact = _es_exact_gauss(0.7, d, rng)
    f, v = energy_fair(X, Y), energy_v1(X, Y)
    se = f.std() / math.sqrt(reps)
    assert abs(f.mean() - exact) < 4 * se
    exx = np.linalg.norm(rng.standard_normal((200000, d)) - rng.standard_normal((200000, d)), axis=1).mean() / math.sqrt(d)
    assert (v - f).mean() == pytest.approx(exx / (2 * m), rel=0.05)


def test_loo_matches_brute_force_and_vs_fairness():
    rng = np.random.default_rng(2)
    Y = rng.standard_normal((5, 3))
    brute = np.mean([energy_fair(np.delete(Y, r, 0), Y[r:r + 1]) for r in range(5)])
    assert energy_loo(Y) == pytest.approx(brute)
    brute_v1 = np.mean([energy_v1(np.delete(Y, r, 0), Y[r:r + 1]) for r in range(5)])
    assert energy_loo(Y, fair=False) == pytest.approx(brute_v1)
    vb = np.mean([variogram(np.delete(Y, r, 0), Y[r:r + 1]) for r in range(5)])
    assert variogram_loo(Y) == pytest.approx(vb)
    # fair VS is unbiased in m; the plug-in is biased upward
    reps, d = 4000, 4
    yv = rng.standard_normal((reps, 1, d))
    small = rng.standard_normal((reps, 3, d))
    big = rng.standard_normal((reps, 200, d))
    f3, f200 = variogram(small, yv), variogram(big, yv)
    p3 = variogram(small, yv, fair=False)
    se = np.sqrt(f3.var() / reps + f200.var() / reps)
    assert abs(f3.mean() - f200.mean()) < 4 * se
    assert p3.mean() - f200.mean() > 4 * se
    # CRPS is the 1-d energy score
    X1 = rng.standard_normal((7, 1))
    assert crps_fair(X1, Y[:2, :1])[0] == pytest.approx(energy_fair(X1, Y[:2, :1]))


def test_skill_report_references():
    rng = np.random.default_rng(3)
    n, c = 50, 3
    orc = 1 + 0.1 * rng.standard_normal((n, c))
    clim = orc + 1 + 0.1 * rng.standard_normal((n, c))
    mid = (orc + clim) / 2
    rep = skill_report({"climatology": clim, "oracle": orc, "mid": mid}, n_boot=300)
    assert rep["aggregate"]["oracle"] == pytest.approx(1) and rep["aggregate"]["climatology"] == pytest.approx(0)
    assert rep["aggregate"]["mid"] == pytest.approx(0.5)
    assert np.allclose(oes(mid, clim, orc), 0.5)
    assert rep["aggregate_pooled"]["mid"] == pytest.approx(0.5) and rep["aggregate_floor0"]["mid"] == pytest.approx(0.5)
    bad = clim + 2.0                             # worse than climatology everywhere
    rep2 = skill_report({"climatology": clim, "oracle": orc, "bad": bad}, n_boot=100)
    assert rep2["aggregate"]["bad"] == pytest.approx(-2.0, abs=0.05) and rep2["aggregate_floor0"]["bad"] == 0.0
    g = paired_gap(rep, "oracle", "mid")
    assert g["gap"] == pytest.approx(0.5) and g["se"] > 0
    flat = clim.copy()
    flat[:, 0] = orc[:, 0]                       # no denominator in cell 0
    assert list(cells_ok(flat, orc)) == [False, True, True]


# ----------------------------------------------------------------------------- lab and exam
def _ring_world():
    lg = ring(n=8, n_blocks=4, k=None, zero_sum=False)
    spec = lg.spec().replace(inport=vw.InputPort(admissible=vw.Admissible(lo=-2, hi=2), in_map=tuple(range(8))),
                        outport=vw.ObservePort(noise=0.2, out_map=tuple(range(4)), out_sign=(1.0,) * 4))
    return vw.World(spec, 0)


def test_lab_secret_episodes_and_budgets():
    w = _ring_world()
    nb = NatsBudget.isotropic(8, 0.3, tick=1.0, episode=1.5, total=2.5)
    lab = Lab(w, Secret(bytes(range(16))), nats=nb, max_ticks=40, reset_cost=1)
    o0 = lab.reset(7)
    assert lab.ticks_used == 1
    assert not np.allclose(o0, w.reset(7))       # not the public-key episode
    x0 = lab._ep.x_flat()
    lab.reset(7)                                 # replay='initial': a label names a start
    assert np.allclose(lab._ep.x_flat(), x0)
    lab.reset(8)
    assert not np.allclose(lab._ep.x_flat(), x0)
    u = {0: 0.3 * math.sqrt(2.0) * 0.99}         # ~0.98 nats
    lab.step(u)
    before = dict(lab.usage())
    with pytest.raises(InputViolation, match="episode"):
        lab.step(u)
    with pytest.raises(InputViolation, match="per-tick"):
        lab.step({0: 1.0})
    with pytest.raises(InputViolation, match="episode"):
        lab.run([(0, u), (1, u)], [2])
    assert lab.usage() == before                 # nothing ran, nothing charged
    lab.run([(0, u)], [1, 2], label=9)            # new episode
    with pytest.raises(InputViolation, match="total"):
        lab.run([(0, u)], [1], label=10)
    with pytest.raises(BudgetExhausted):
        lab.run([], [100], label=11)
    assert lab.usage()["ticks_used"] == before["ticks_used"] + 3
    assert "information_budget" in lab.card() and "secret" in lab.card()["keys"]


def test_lab_rejects_unaccountable_ports():
    w = _ring_world()
    with pytest.raises(ValueError):
        Lab(vw.World(w.spec.replace(replay="full"), 0), Secret())
    noisy = w.spec.replace(inport=vw.InputPort(admissible=vw.Admissible(lo=-2, hi=2), noise=0.1))
    with pytest.raises(ValueError):
        Lab(vw.World(noisy, 0), Secret(), nats=NatsBudget.isotropic(8, 0.3))


def test_history_exam_end_to_end():
    w = _ring_world()
    nb = NatsBudget.isotropic(8, 0.3, tick=1.0, episode=3.0)
    mix = ProgramMix({"a": no_input, "b": blind_random(nb, k=2, rate=0.5)})
    sec = Secret(bytes(range(32)))
    ex = HistoryExam(w, sec, mix, n_items=8, prefix=4, queries={1: [1, 3], 2: [3]}, R=5,
                     derived={2: lambda o: np.asarray(o).sum(-1, keepdims=True)}, nats=nb, n_clim=32)
    assert sorted(it.klass for it in ex.items) == ["a"] * 4 + ["b"] * 4
    pub = ex.public()[0]
    assert set(pub) == {"id", "history", "prefix_program", "program", "queries"}
    assert pub["history"].shape == (5, 4) and ex.truths[1].shape == (8, 5, 2, 4) and ex.truths[2].shape == (8, 5, 1, 1)
    for it in ex.items:
        assert nb.program_cost(it.program) <= 3.0 + 1e-9
    # the same secret gives the same exam; another secret another one
    ex2 = HistoryExam(w, sec, mix, n_items=8, prefix=4, queries={1: [1, 3], 2: [3]}, R=5,
                      derived={2: lambda o: np.asarray(o).sum(-1, keepdims=True)}, nats=nb, n_clim=32)
    assert np.allclose(ex2.truths[1], ex.truths[1])
    # a predictor that returns the replicate truths' own law (resampled truths) scores near the oracle
    def clim_pred(item, n, seed):
        r = np.random.default_rng(seed)
        i = r.integers(32, size=n)
        return {1: ex.clim[1][i], 2: ex.clim[2][i]}
    sc = ex.score(ex.collect(clim_pred, 16, 0))
    refs = ex.references()
    assert refs["oracle"]["es"].shape == (8, 3) and np.isnan(refs["oracle"]["vs"][:, 2]).all()
    rep = ex.report({"clim16": sc}, valid=np.ones(3, bool), n_boot=100)
    assert abs(rep["aggregate"]["clim16"]) < 0.5
    with pytest.raises(ValueError):
        ex.collect(lambda item, n, seed: {1: np.zeros((n, 1, 4)), 2: np.zeros((n, 1, 1))}, 4, 0)
