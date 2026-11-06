"""Closed-form check of Propositions 7 and 11 in ../CATEGORY.md (chain rule for the closure gap) on the VW-0
linear-Gaussian family (spec/lingauss.py). Run with -B so nothing is written into spec/.

For a world X -> Y = C X -> O = Y + r*eta (one-step future, whole pasts):
  Gamma_X(O)  = I(X_t; O_{t+1} | O_past)                      (the VW-0 gap at tau=1, p=inf)
  defect      = I(X_t; O_{t+1} | Y_past)  (noiseless level-1 past; the coarse-graining's share)
  port part   = Gamma_X(O) - defect = I(Y_past; O_{t+1} | O_past)  (observation noise's share)
For a refinement X_{-1} -> X_0 = Psi X_{-1}:
  refinement defect = I(X_{-1,t}; O_{t+1} | X_0 past)  (0 for an exactly lumpable refinement)
"""
import json, math, os, sys
import numpy as np

SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "spec")
sys.path.insert(0, os.path.abspath(SPEC))
import lingauss as lg  # noqa: E402


def ld(S):
    s, v = np.linalg.slogdet(S)
    assert s > 0
    return v


def filt_noiseless(A, Q, H, Sigma, iters=20000, tol=1e-15):
    """Steady filtered covariance of x_t given the noiseless history H x_0..H x_t."""
    Pp = Sigma.copy()
    for _ in range(iters):
        S = H @ Pp @ H.T
        Pf = Pp - Pp @ H.T @ np.linalg.pinv(S, rcond=1e-12, hermitian=True) @ H @ Pp
        Pf = (Pf + Pf.T) / 2
        Pn = A @ Pf @ A.T + Q
        if np.max(np.abs(Pn - Pp)) < tol * max(1.0, np.abs(Pn).max()):
            return Pf
        Pp = Pn
    raise RuntimeError("no convergence")


def split(model, name):
    w = model.world(0)
    cf = lg.ClosedForms(model, w)
    A, Q, Sig = model.A, model.Q, model.Sigma
    C, R = cf.Ca, cf.R
    gap = 0.5 * (ld(cf.Se(1, math.inf)) - ld(cf.Su(1)))
    PY = filt_noiseless(A, Q, C, Sig)
    defect = 0.5 * (ld(C @ (A @ PY @ A.T + Q) @ C.T + R) - ld(cf.Su(1)))
    return {"world": name, "gap_X_O": gap, "coarse_graining_defect": defect, "port_part": gap - defect}


def refinement_defect(base, eta):
    Af, Psi, Qf, Lam = lg.lumpable_refinement(base, eta=eta)
    fine = base.refined(Af, Psi, Qf, Lam)
    w = fine.world(0)
    cf = lg.ClosedForms(fine, w)
    C, R = cf.Ca, cf.R                     # C here is (base C) @ Psi in agent coordinates
    P = filt_noiseless(Af, Qf, Psi, fine.Sigma)
    num = ld(C @ (Af @ P @ Af.T + Qf) @ C.T + R)
    den = ld(cf.Su(1))
    gap_fine = 0.5 * (ld(cf.Se(1, math.inf)) - den)
    cfb = lg.ClosedForms(base, base.world(0))
    gap_base = 0.5 * (ld(cfb.Se(1, math.inf)) - ld(cfb.Su(1)))
    return {"eta": eta, "refinement_defect": 0.5 * (num - den), "gap_fine": gap_fine, "gap_base": gap_base,
            "gap_fine_minus_base": gap_fine - gap_base}


if __name__ == "__main__":
    ring = lg.ring()
    rnd = lg.random_lg()
    out = {"split_tau1_pinf_nats": [split(ring, "ring"), split(rnd, "random"),
                                    split(ring.stacked(np.kron(np.eye(3), np.ones((1, 2)))), "stack(ring)")],
           "refinement_tau1_pinf_nats": [refinement_defect(ring, 0.0), refinement_defect(ring, 0.3)]}
    print(json.dumps(out, indent=1))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gap_split.json"), "w") as f:
        json.dump(out, f, indent=1)
