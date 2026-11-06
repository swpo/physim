"""Checker: (a) one certificate number (closure gap, ring world) from vw.closure against my own
joint-Gaussian computation (no Kalman code reused); (b) the note's Prop. 7 table by the same
independent route; (c) vw.fisher (autodiff) against my own finite differences, both of the exact
moments (own numpy implementation) and of the library's own Monte Carlo statistic with fixed keys.
Run from vw1/check: ../.venv/bin/python -B cert_fisher_check.py  -> cert_fisher.json"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VW1 = os.path.dirname(HERE)
VEC = os.path.dirname(VW1)
sys.path.insert(0, VW1)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from scipy.linalg import solve_discrete_lyapunov  # noqa: E402

import vw  # noqa: E402
from vw import certificates as CT  # noqa: E402
from vw.lingauss import ParamLG, ring  # noqa: E402

out = {}


def ld(S):
    s, v = np.linalg.slogdet(S)
    assert s > 0
    return v


def cond_var(S, a, b):
    """Var(z_a | z_b) for a joint Gaussian with covariance S (index arrays a, b)."""
    if len(b) == 0:
        return S[np.ix_(a, a)]
    Sbb = S[np.ix_(b, b)]
    X = np.linalg.solve(Sbb, S[np.ix_(b, a)])
    V = S[np.ix_(a, a)] - S[np.ix_(a, b)] @ X
    return (V + V.T) / 2


def joint_cov(A, Sig, Cs, Rs, T):
    """Covariance of stacked (z_0..z_{T-1}), z_t = [Cs[k] x_t + noise_k]_k for a stationary AR(1) x."""
    blocks = {}
    Ap = [np.eye(A.shape[0])]
    for _ in range(T):
        Ap.append(A @ Ap[-1])
    rows = []
    for i in range(T):
        row = []
        for j in range(T):
            Cx = Ap[i - j] @ Sig if i >= j else Sig @ Ap[j - i].T
            row.append(np.block([[Ck @ Cx @ Cl.T + (Rk if (i == j and k == l) else 0 * np.eye(Ck.shape[0], Cl.shape[0]))
                                  for l, Cl in enumerate(Cs)] for k, (Ck, Rk) in enumerate(zip(Cs, Rs))]))
        rows.append(row)
    del blocks
    return np.block(rows)


def gap_window(A, Q, C, r, p, tau=1):
    """VW-0 gap Gamma(tau, p) = 1/2 logdet Var(o_{t+tau} | o_{t-p+1..t}) - 1/2 logdet E Var(o_{t+tau} | x_t)."""
    Sig = solve_discrete_lyapunov(A, Q)
    m = C.shape[0]
    R = r ** 2 * np.eye(m)
    T = p + tau
    S = joint_cov(A, Sig, [C], [R], T)
    fut = np.arange((T - 1) * m, T * m)
    past = np.arange(0, p * m)
    Se = cond_var(S, fut, past)
    M = sum(np.linalg.matrix_power(A, s) @ Q @ np.linalg.matrix_power(A, s).T for s in range(tau))
    Su = C @ M @ C.T + R
    return 0.5 * (ld(Se) - ld(Su))


def split_window(A, Q, C, r, p):
    """Prop. 7 at tau = 1 with window p: gap, and the coarse-graining part I(x_t; o_{t+1} | y_{t-p+1..t})
    from a joint Gaussian over (y noiseless, o noisy)."""
    Sig = solve_discrete_lyapunov(A, Q)
    m = C.shape[0]
    R = r ** 2 * np.eye(m)
    T = p + 1
    S = joint_cov(A, Sig, [C, C], [np.zeros((m, m)), R], T)      # per tick: [y_t, o_t]
    per = 2 * m
    fut_o = np.arange(p * per + m, p * per + 2 * m)
    past_o = np.concatenate([np.arange(t * per + m, t * per + 2 * m) for t in range(p)])
    past_y = np.concatenate([np.arange(t * per, t * per + m) for t in range(p)])
    Su = C @ Q @ C.T + R
    gap = 0.5 * (ld(cond_var(S, fut_o, past_o)) - ld(Su))
    cg = 0.5 * (ld(cond_var(S, fut_o, past_y)) - ld(Su))
    return gap, cg


# ---------------------------------------------------------------- (a) closure certificate, ring
lgr = ring()
w = lgr.world(0)
cl = CT.closure(w, horizons=(1, 2), pasts=(0, 1, 4, 16), n_traj=20000, n_oracle=4000, n_rep=16, seed=0)
mine = {p: gap_window(lgr.A, lgr.Q, lgr.C, lgr.r, p) for p in (1, 4, 16)}
from vw.lingauss import ClosedForms  # noqa: E402
cf = ClosedForms(lgr, w).closure((1, 2), (0, 1, 4, 16))
P = list(cl["pasts"])
out["closure_ring_tau1"] = {
    str(p): {"vw_closure_estimate": float(cl["gap_nats"][0, P.index(p)]), "se": float(cl["se"]["gap_nats"][0, P.index(p)]),
             "mine_joint_gaussian": mine[p], "vw_lingauss_closed_form": float(cf["gap_nats"][0, P.index(p)])}
    for p in (1, 4, 16)}
out["closure_ring_tau2_p16_mine"] = gap_window(lgr.A, lgr.Q, lgr.C, lgr.r, 16, tau=2)
out["closure_ring_tau2_p16_vw"] = float(cl["gap_nats"][1, P.index(16)])

# ---------------------------------------------------------------- (b) Prop. 7 table (VW-0 matrices)
sys.path.insert(0, os.path.join(VEC, "spec"))
import lingauss as LG0  # noqa: E402
models = {"ring": LG0.ring(), "random": LG0.random_lg()}
models["stack(ring)"] = LG0.ring().stacked(np.kron(np.eye(3), np.ones((1, 2))))
tab = {}
for k, mdl in models.items():
    rows = {}
    for p in (40, 80):
        g, c = split_window(mdl.A, mdl.Q, mdl.C, mdl.r, p)
        rows[p] = (g, c, g - c)
    tab[k] = {"gap": rows[80][0], "cg_part": rows[80][1], "port_part": rows[80][2],
              "change_p40_to_p80": float(np.max(np.abs(np.array(rows[80]) - np.array(rows[40]))))}
out["prop7_split_mine_window80"] = tab

# ---------------------------------------------------------------- (c) Fisher
TIMES = (1, 2, 4)
plg = ParamLG()
wf = vw.World(plg.spec(), 0)


def my_moments(beta, gamma):
    n = plg.n
    M = np.asarray(plg.M)
    v = np.asarray(plg.v)
    C = np.asarray(plg.C)
    A = (1 - gamma) * M
    Sig = solve_discrete_lyapunov(A, plg.sigma ** 2 * np.eye(n))
    mu = np.linalg.solve(np.eye(n) - A, beta * v)
    nb = C.shape[0]
    m = np.tile(C @ mu, len(TIMES))
    S = np.zeros((nb * len(TIMES),) * 2)
    for i, ti in enumerate(TIMES):
        for j, tj in enumerate(TIMES):
            Cx = np.linalg.matrix_power(A, ti - tj) @ Sig if ti >= tj else Sig @ np.linalg.matrix_power(A, tj - ti).T
            S[i * nb:(i + 1) * nb, j * nb:(j + 1) * nb] = C @ Cx @ C.T + (plg.r ** 2 * np.eye(nb) if i == j else 0)
    return m, S


def gauss_fisher_fd(moments, th, h):
    m0, S0 = moments(*th)
    Si = np.linalg.inv(S0)
    dm, dS = [], []
    for i in range(len(th)):
        e = np.zeros(len(th))
        e[i] = h
        mp, Sp = moments(*(th + e))
        mm, Sm = moments(*(th - e))
        dm.append((mp - mm) / (2 * h))
        dS.append((Sp - Sm) / (2 * h))
    J = np.stack(dm, 1)
    lin = J.T @ Si @ J
    cov = np.array([[0.5 * np.trace(Si @ dS[i] @ Si @ dS[j]) for j in range(len(th))] for i in range(len(th))])
    return lin + cov, lin


th0 = np.array([float(plg.params["beta"]), float(plg.params["gamma"])])
G_exact, L_exact = gauss_fisher_fd(my_moments, th0, 1e-6)
G_cf, L_cf = plg.fisher_closed_form(TIMES)
N, SEED = 20000, 1
F = wf.designer.fisher(times=TIMES, n=N, seed=SEED)

# FD of the library's own Monte Carlo statistic with the SAME keys as vw.fisher
ki = vw.member_keys(CT._cert_key(wf, 81, SEED), N)
kd = jax.vmap(lambda k: jax.random.fold_in(k, 6))(ki)
tsel = jnp.asarray(TIMES)


@jax.jit
def Ymc(beta, gamma):
    p = {"beta": jnp.asarray(beta), "gamma": jnp.asarray(gamma)}
    c = jax.vmap(wf._init_member, in_axes=(None, 0, 0))(p, ki, kd)
    A = jnp.zeros((max(TIMES), N, wf.n_in))
    _, rec = wf._rollout_fn(p, c, A, ("obs_continuous",))
    o = rec["obs_continuous"][tsel]
    return jnp.swapaxes(o, 0, 1).reshape(N, -1)


def mc_moments(beta, gamma):
    Y = np.asarray(Ymc(beta, gamma))
    return Y.mean(0), np.cov(Y.T, ddof=1)


G_mcfd, L_mcfd = gauss_fisher_fd(mc_moments, th0, 1e-5)
rel = lambda a, b: float(np.max(np.abs(np.asarray(a) - np.asarray(b)) / np.sqrt(np.outer(np.diag(b), np.diag(b)))))  # noqa: E731
out["fisher"] = {
    "names": F["names"], "theta": th0.tolist(),
    "exact_mine_fd_gaussian": G_exact.tolist(), "exact_mine_fd_linear": L_exact.tolist(),
    "lingauss_closed_form_gaussian": np.asarray(G_cf).tolist(),
    "vw_fisher_gaussian": np.asarray(F["gaussian"]).tolist(), "vw_fisher_linear": np.asarray(F["linear"]).tolist(),
    "fd_of_library_mc_statistic_gaussian": G_mcfd.tolist(),
    "rel_err_mine_vs_lingauss_cf": rel(G_cf, G_exact),
    "rel_err_vw_fisher_vs_exact": rel(F["gaussian"], G_exact),
    "rel_err_vw_fisher_linear_vs_exact_linear": rel(F["linear"], L_exact),
    "rel_err_autodiff_vs_fd_same_keys": rel(F["gaussian"], G_mcfd),
    "rel_err_autodiff_linear_vs_fd_same_keys": rel(F["linear"], L_mcfd),
    "n": N}
F40 = wf.designer.fisher(times=TIMES, n=40000, chunk=20000, seed=1)
out["fisher"]["library_test_config_gamma_gamma"] = float(F40["gaussian"][1, 1])
out["fisher"]["exact_gamma_gamma"] = float(G_exact[1, 1])
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "cert_fisher.json"), "w"), indent=1)
