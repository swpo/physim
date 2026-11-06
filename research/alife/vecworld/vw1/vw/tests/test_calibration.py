"""Calibration tests ported from spec/tests/test_calibration.py: closed forms are self-consistent and
the generic estimators (running on the JAX worlds) recover them, also on composed worlds."""
import json
import math

import jax.numpy as jnp
import numpy as np
import pytest

import vw
from vw.lingauss import ClosedForms, LinearGaussian, lumpable_level, random_lg, ring

HOR, PAS = (1, 2, 4, 8), (0, 1, 4, 8)


@pytest.fixture(scope="module", params=["ring", "ring-conserved", "random"])
def lgw(request):
    lg = {"ring": ring(), "ring-conserved": ring(conserve=True), "random": random_lg()}[request.param]
    return lg, lg.world(1)


def _refined(eta, world_seed=1):
    r = ring()
    lgf, fine, Psi = lumpable_level(r, eta=eta)
    spec = vw.refine(r.spec(), fine, vw.CoarseGrain.of(lambda x: jnp.asarray(Psi) @ x))
    return lgf, vw.World(spec, world_seed)


def composed():
    r, rl = ring(), random_lg()
    C2 = np.kron(np.eye(3), np.ones((1, 2)))
    return {
        "product": (LinearGaussian.concat(r, rl), vw.World(vw.product(r.spec(), rl.spec()), 4)),
        "stack": (r.stacked(C2), vw.World(vw.stack(r.spec(), vw.CoarseGrain.of(lambda y: jnp.asarray(C2) @ y)), 5)),
        "refine-leaky": _refined(0.3),
    }


def test_kalman_equals_window_conditioning(lgw):
    lg, w = lgw
    cf = ClosedForms(lg, w)
    for tau, p in [(1, 1), (2, 3), (5, 6), (1, 8)]:
        assert np.allclose(cf.Se(tau, p), cf.Se_window(tau, p), atol=1e-9)


def test_closed_form_structure(lgw):
    lg, w = lgw
    cf = ClosedForms(lg, w)
    t = cf.closure(HOR, PAS, blocks=(3,))
    assert np.all(np.diff(t["gap_nats"], axis=1) <= 1e-10)
    assert np.all(t["gap_nats"] >= -1e-10)
    for h in HOR:
        assert np.linalg.eigvalsh(cf.Se(h, 8) - cf.Su(h)).min() > -1e-10
    assert np.all(t["block_gap_nats"][0] >= t["gap_nats"][0] - 1e-10)
    a = t["p_inf"]["atay"]
    assert a["memory"] >= -1e-12 and a["residual"] >= -1e-12
    lk = cf.leak(PAS)
    assert all(np.all((m > 0) & (m <= 1 + 1e-9)) for m in lk["mu"])


def test_composition_identities():
    r, rl = ring(), random_lg()
    g = lambda lg, w: ClosedForms(lg, w).closure(HOR, PAS)["gap_nats"]  # noqa: E731
    wcat = vw.World(vw.product(r.spec(), rl.spec()), 4)
    assert np.allclose(g(LinearGaussian.concat(r, rl), wcat), g(r, r.world(0)) + g(rl, rl.world(0)), atol=1e-10)
    f, wf = _refined(0.0)
    assert np.allclose(g(f, wf), g(r, r.world(1)), atol=1e-10)
    f2, wf2 = _refined(0.3)
    assert np.all(g(f2, wf2)[:, -1] > g(r, r.world(1))[:, -1] + 1e-3)


def _z_ok(est, cf, se, zmax=5.0, floor=0.0):
    est, cf, se = map(np.asarray, (est, cf, se))
    return np.all(np.abs(est - cf) <= zmax * se + floor)


def _check_estimators(lg, w, N=8000, n_or=2000, L=6, p=4):
    d, cf = w.designer, ClosedForms(lg, w)
    cl = d.closure(HOR, PAS, blocks=(3,), n_traj=N, n_oracle=n_or, n_rep=16, n_programs=1, seed=3)
    cc = cf.closure(HOR, PAS, blocks=(3,))
    for k in ("Ve", "Vu", "gap_nats", "block_gap_nats"):
        assert _z_ok(cl[k], cc[k], cl["se"][k], floor=0.01), k
    lk, lc = d.leak(PAS, n_traj=N, seed=3), cf.leak(PAS)
    assert np.allclose(lk["info_nats"], lc["info_nats"], rtol=0.03, atol=0.02)
    assert max(np.max(np.abs(a - b)) for a, b in zip(lk["mu"], lc["mu"])) < 0.03
    assert np.all(np.abs(lk["dim"] - lc["dim"]) <= 1)
    ic, icc = d.input_capacity(L=L, p=p, n_states=2, n_traj=N, seed=3), cf.input_capacity(L=L, p=p)
    assert np.allclose(ic["response"], icc["response"], atol=1e-9)        # exact with common noise
    assert np.allclose(ic["singular_values"], icc["singular_values"], rtol=0.08, atol=1e-3 * icc["singular_values"][0])
    assert abs(ic["capacity_bits_upper"] - icc["capacity_bits_upper"]) < 0.08 * icc["capacity_bits_upper"]
    oc, occ = d.observation_capacity((1, 8), n_traj=N, seed=3), cf.observation_capacity((1, 8))
    assert np.allclose(oc["rate_bits"], occ["rate_bits"], atol=0.08)


def test_estimators_recover_closed_forms(lgw):
    _check_estimators(*lgw)


@pytest.mark.parametrize("which", ["product", "stack", "refine-leaky"])
def test_estimators_recover_closed_forms_on_composed_worlds(which):
    lg, w = composed()[which]
    _check_estimators(lg, w)


def test_closure_independent_of_program():
    lg = random_lg()
    w = lg.world(2)
    d = w.designer
    prog = d.random_program(np.random.default_rng(5), 24, rate=1.0)
    assert len(prog) > 10
    cl = d.closure((1, 4), (0, 1, 4), n_traj=8000, n_oracle=2000, programs=[prog], seed=4)
    cc = ClosedForms(lg, w).closure((1, 4), (0, 1, 4))
    assert _z_ok(cl["gap_nats"], cc["gap_nats"], cl["se"]["gap_nats"], floor=0.01)


def test_exam_reference_matches_closed_form():
    lg = ring()
    w = lg.world(0)
    cf = ClosedForms(lg, w)
    ex = vw.Exam(w, n_items=80, prefix=8, horizon=8, queries=(1, 4, 8), exam_seed=1)
    assert "x" not in ex.public()[0] and "h0" not in ex.public()[0]
    sc = ex.score(n_rep=32, references={"kalman": cf.kalman_predict}, ceiling="kalman")
    for i, q in enumerate(sc["queries"]):
        assert abs(sc["mse"]["kalman"][i] - np.trace(cf.Se(q, 9))) < 4 * sc["mse_se"]["kalman"][i] + 0.05
        assert abs(sc["oracle"][i] - np.trace(cf.Su(q))) < 0.06 * np.trace(cf.Su(q))
        assert sc["mse"]["persistence"][i] > sc["mse"]["kalman"][i]


def test_commutation_error():
    r = ring()
    for eta, tol in ((0.0, 0.02), (0.3, 0.1)):
        lgf, fine, Psi = lumpable_level(r, eta=eta)
        wf = vw.World(vw.refine(r.spec(), fine, vw.CoarseGrain.of(lambda x, P=Psi: jnp.asarray(P) @ x)), 0)
        est = vw.commutation_error(fine, vw.CoarseGrain.of(lambda x, P=Psi: jnp.asarray(P) @ x), r.level(),
                                   T=(1,), n=3000, n_rep=16, mode="distributional")
        exact = ClosedForms(lgf, wf).commutation_delta2(r, Psi, 1)
        assert abs(est["delta2"][0] - exact) < tol * max(exact, 0.2)


def test_waterfill():
    cap, n = vw.waterfill([4.0, 1.0, 0.01], 1.0)
    assert n == 2 and math.isclose(cap, 0.5 * (math.log(1 + 4 * 0.875) + math.log(1 + 0.125)))


def test_certify_bundle_and_flags():
    w = ring(conserve=True).world(0)
    c = w.designer.certify(horizons=(1, 4), pasts=(0, 1, 4), n_traj=4000, n_programs=1, L=4)
    f = c["flags"]
    assert f["finite_resolution"] and f["nontrivial"] and f["is_a_level"] and f["level0_hidden"]
    assert f["inputs_visible"] and f["invariants_conserved"]
    c2 = random_lg().world(0).designer.certify(horizons=(1, 4), pasts=(0, 1, 4), n_traj=4000, n_programs=0, L=4)
    assert not c2["flags"]["inputs_visible"]
    json.dumps(vw.jsonable(c))
