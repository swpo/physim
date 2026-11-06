"""Fisher-information certificate by autodiff, calibrated on a linear-Gaussian world with closed form."""
import numpy as np
import pytest

import vw
from vw.lingauss import ParamLG, ring

TIMES = (1, 2, 4)


@pytest.fixture(scope="module", params=[0.5, 0.0], ids=["beta0.5", "beta0"])
def est(request):
    plg = ParamLG(beta=request.param)          # beta = 0: gamma acts only through the covariance
    w = vw.World(plg.spec(), 0)
    F = w.designer.fisher(times=TIMES, n=40000, chunk=20000, seed=1)
    gauss, lin = plg.fisher_closed_form(TIMES)
    return plg, w, F, gauss, lin


def test_fisher_matches_closed_form(est):
    plg, w, F, gauss, lin = est
    assert F["names"] == ["beta", "gamma"]
    scale = np.sqrt(np.outer(np.diag(gauss), np.diag(gauss)))
    assert np.all(np.abs(F["gaussian"] - gauss) <= 0.06 * scale), (F["gaussian"], gauss)
    assert np.all(np.abs(F["linear"] - lin) <= 0.06 * scale), (F["linear"], lin)


def test_linear_fisher_is_a_lower_bound_and_exact_for_mean_parameters(est):
    plg, w, F, gauss, lin = est
    assert np.linalg.eigvalsh(gauss - lin).min() > -1e-9                    # closed form: linear <= full
    assert np.linalg.eigvalsh(F["gaussian"] - F["linear"]).min() > -1e-9 * np.abs(gauss).max()
    assert abs(lin[0, 0] - gauss[0, 0]) < 1e-9 * gauss[0, 0]                # beta enters the mean only
    if float(plg.params["beta"]) == 0.0:                                     # gamma: covariance only
        assert lin[1, 1] < 1e-9 * gauss[1, 1] and F["linear"][1, 1] < 0.01 * gauss[1, 1]
        assert abs(F["covariance_term"][1, 1] - gauss[1, 1]) < 0.06 * gauss[1, 1]
    assert np.all(F["crb"] > 0)


def test_fisher_parameter_paths_in_composed_worlds():
    plg = ParamLG()
    alone = vw.World(plg.spec(), 0).designer.fisher(wrt=["gamma"], times=TIMES, n=20000, seed=2)
    pw = vw.World(vw.product(plg.spec(), ring().spec()), 0)
    both = pw.designer.fisher(wrt=["0/gamma"], times=TIMES, n=20000, seed=2)
    exact = plg.fisher_closed_form(TIMES)[0][1, 1]
    assert both["names"] == ["0/gamma"]
    assert abs(alone["gaussian"][0, 0] - exact) < 0.06 * exact
    assert abs(both["gaussian"][0, 0] - exact) < 0.08 * exact                # an independent factor adds nothing
    st = vw.World(vw.stride(plg.spec(), 2), 0).designer.fisher(wrt=["beta"], times=(1, 2), n=4000, seed=3)
    assert st["gaussian"].shape == (1, 1) and st["gaussian"][0, 0] > 0
