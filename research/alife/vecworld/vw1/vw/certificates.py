"""vw.certificates -- designer certificates for any World (ported from spec/vecworld.py, VW-0).

Simulation is JAX (batched ensembles, common random numbers); the statistics are numpy float64.
Conventions as spec/DESIGN.md section 6: conditional on an open-loop program, pasts are windows
W_p(t) = o(t-p+1..t), several horizons tau and block futures.

closure                ceiling c(tau, p), gap Gamma(tau, p) (Gaussian proxy, Wishart corrected),
                       block gaps, Atay split; oracle by Monte Carlo over fresh-noise branches
leak                   readability of level 0 from level-k pasts (prior-whitened posterior spectrum)
input_capacity         one-tick response of the noise-free observed future (shared-noise branch
                       pairs) whitened by the level-k-only prediction error; zero-sum worlds are
                       probed along an orthonormal basis of the zero-sum subspace (admissible
                       directions, so conserving kicks respond; VW-0 probed single coordinates)
observation_capacity   rate r(p) = I(o(t+1); X(t+1) | W_p(t)) and the channel bound
invariant_drift        declared conserved quantities under free evolution
fisher                 Fisher information of the observed trajectory about declared level-0
                       parameters, by autodiff (pathwise derivatives with common random numbers):
                         linear   = J^T S^-1 J       (J = d E[o]/d theta, S = Cov o): a lower bound
                                    on the Fisher information for ANY observation law (it is the
                                    Cramer-Rao inequality applied to the statistic o itself)
                         gaussian = linear + 1/2 tr(S^-1 dS_i S^-1 dS_j): exact when o is Gaussian
                       computed on the unclipped, unquantised channel (quantisation has no
                       derivative); requires a differentiable world (no opaque blocks)
certify                all of the above plus provisional admission flags
"""
from __future__ import annotations

import math
from typing import Optional, Sequence

import jax
import jax.numpy as jnp
import numpy as np
from jax.flatten_util import ravel_pytree
from scipy.special import digamma

from .ports import Admissible
from .world import _NS_CERT, _ST_DYN, World, make_key, member_keys


class NotDifferentiable(TypeError):
    """A certificate needs derivatives through a block that does not have them (opaque blocks)."""


# ----------------------------------------------------------------------------- statistics
def logdet(S: np.ndarray, dof: Optional[float] = None) -> float:
    """log det S; with dof, the Wishart-unbiased version for S = (residual scatter)/dof."""
    sign, ld = np.linalg.slogdet(S)
    if sign <= 0:
        return -math.inf
    if dof is None or not math.isfinite(dof):
        return float(ld)
    q = S.shape[0]
    i = np.arange(1, q + 1)
    return float(ld - (q * math.log(2.0 / dof) + digamma((dof - i + 1) / 2.0).sum()))


def ols_residuals(X: np.ndarray, Y: np.ndarray):
    """Least-squares residuals of Y on [1, X]; returns (E, dof)."""
    N = Y.shape[0]
    Xc = np.ones((N, 1)) if X.shape[1] == 0 else np.column_stack([np.ones(N), X])
    coef, _, rank, _ = np.linalg.lstsq(Xc, Y, rcond=None)
    return Y - Xc @ coef, N - rank


def within_cov(Y: np.ndarray):
    """Y (N, R, q): average within-group covariance (ddof 1); returns (S, dof)."""
    N, R, _ = Y.shape
    D = Y - Y.mean(1, keepdims=True)
    return np.einsum("nri,nrj->ij", D, D) / (N * (R - 1)), N * (R - 1)


def inv_sqrt(S: np.ndarray, floor: float = 1e-12) -> np.ndarray:
    w, U = np.linalg.eigh((S + S.T) / 2)
    w = np.maximum(w, floor * max(w.max(), 1e-300))
    return (U / np.sqrt(w)) @ U.T


def whiten_basis(S: np.ndarray, tol: float = 1e-9, n_pc: Optional[int] = None) -> np.ndarray:
    """W (n, r) with W^T S W = I on the numerical support of S (top n_pc directions if given)."""
    w, U = np.linalg.eigh((S + S.T) / 2)
    order = np.argsort(w)[::-1]
    w, U = w[order], U[:, order]
    keep = w > tol * w[0]
    if n_pc is not None:
        keep[n_pc:] = False
    return U[:, keep] / np.sqrt(w[keep])


def leak_spectrum(S_post: np.ndarray, S_prior: np.ndarray, tol: float = 1e-9, n_pc: Optional[int] = None) -> np.ndarray:
    W = whiten_basis(S_prior, tol, n_pc)
    return np.sort(np.linalg.eigvalsh(W.T @ S_post @ W))


def waterfill(gains, power: float):
    """Capacity (nats) of parallel channels y_i = sqrt(g_i) x_i + N(0,1) with sum E x_i^2 <= power."""
    g = np.sort(np.asarray(gains, float))[::-1]
    g = g[g > 1e-300]
    if power <= 0 or g.size == 0 or not math.isfinite(power):
        return (0.0 if power <= 0 or g.size == 0 else math.inf), 0
    inv = 1.0 / g
    for n in range(g.size, 0, -1):
        mu = (power + inv[:n].sum()) / n
        if mu > inv[n - 1]:
            break
    p = np.maximum(mu - inv, 0.0)
    return float(0.5 * np.sum(np.log1p(g * p))), int((p > 0).sum())


def input_basis(C: Admissible, n_in: int) -> np.ndarray:
    """Orthonormal basis (n_in, r) of the admissible directions: 1-perp under zero_sum, else I."""
    if C.zero_sum:
        Q, _ = np.linalg.qr(np.column_stack([np.ones(n_in), np.eye(n_in)[:, : n_in - 1]]))
        return Q[:, 1:]
    return np.eye(n_in)


def capacity_from_response(Gb: np.ndarray, basis: np.ndarray, S_noise: np.ndarray, C: Admissible, n_in: int,
                           max_pairs: int = 4000, seed: int = 0) -> dict:
    """Input-capacity numbers from the response Gb (n_out, r) to the basis directions (n_in, r) and
    the agent-relevant noise covariance S_noise of the same level-k future block."""
    Wn = inv_sqrt(S_noise)
    Rb = Wn @ Gb
    sv = np.linalg.svd(Rb, compute_uv=False)
    R = Rb @ basis.T                      # whitened response on the admissible subspace
    b, rho, ba = C.amplitude(), C.l2_radius(n_in), C.atom_amplitude()
    cap, n_act = waterfill(sv ** 2, rho ** 2)
    if C.zero_sum:
        pairs = [(i, j) for i in range(n_in) for j in range(i + 1, n_in)]
        if len(pairs) > max_pairs:
            sel = np.random.default_rng(seed).choice(len(pairs), max_pairs, replace=False)
            pairs = [pairs[s] for s in sel]
        I = np.array([p[0] for p in pairs])
        J = np.array([p[1] for p in pairs])
        snr = ba ** 2 * ((R[:, I] - R[:, J]) ** 2).sum(0)
    else:
        snr = ba ** 2 * (R ** 2).sum(0)
    d_exc = C.excitable_dim(n_in)
    d_vis = int((b * sv >= 1.0).sum())
    return {"excitable_dim_per_tick": d_exc, "singular_values": sv, "visible_dim": d_vis,
            "visible_dim_per_tick": min(d_exc, d_vis), "capacity_bits_upper": cap / math.log(2),
            "capacity_channels": n_act, "l2_radius": rho,
            "atom_snr_median": float(np.median(snr)), "atom_snr_min": float(snr.min()),
            "atom_snr_max": float(snr.max()), "atom_visible_frac": float((snr >= 1.0).mean()),
            "command_bits_upper": C.command_bits(n_in), "response": Gb @ basis.T}


def closure_tables(Se, Se_dof, Su, Su_dof, horizons, pasts, Seb=None, Seb_dof=None, Sub=None, Sub_dof=None,
                   blocks=()) -> dict:
    """Closure numbers from error covariances (dof None: exact closed form)."""
    H, P = list(horizons), list(pasts)
    V0 = np.array([np.trace(Se[(h, 0)]) if (h, 0) in Se else np.nan for h in H])
    Vu = np.array([np.trace(Su[h]) for h in H])
    Ve = np.array([[np.trace(Se[(h, p)]) for p in P] for h in H])
    gap = np.array([[0.5 * (logdet(Se[(h, p)], Se_dof.get((h, p))) - logdet(Su[h], Su_dof.get(h)))
                     for p in P] for h in H])
    with np.errstate(divide="ignore", invalid="ignore"):
        ceiling = (V0[:, None] - Ve) / (V0[:, None] - Vu[:, None])
        predictable = (V0[:, None] - Ve) / V0[:, None]
    out = {"horizons": H, "pasts": P, "V0": V0, "Vu": Vu, "Ve": Ve, "gap_nats": gap,
           "ceiling": ceiling, "predictable": predictable}
    if 1 in H and 1 in P:
        i, j1, jm = H.index(1), P.index(1), len(P) - 1
        out["atay"] = {"leak": gap[i, j1], "residual": gap[i, jm], "memory": gap[i, j1] - gap[i, jm], "p_max": P[jm]}
    if blocks:
        out["blocks"] = list(blocks)
        out["block_gap_nats"] = np.array(
            [[0.5 * (logdet(Seb[(L, p)], (Seb_dof or {}).get((L, p))) - logdet(Sub[L], (Sub_dof or {}).get(L)))
              for p in P] for L in blocks])
    return out


_TABLE_KEYS = ("V0", "Vu", "Ve", "gap_nats", "ceiling", "predictable", "block_gap_nats")


def _avg_tables(tabs: list, keys) -> dict:
    out = dict(tabs[0])
    for k in keys:
        if k in tabs[0]:
            out[k] = np.mean([t[k] for t in tabs], axis=0)
    if "atay" in tabs[0]:
        out["atay"] = {k: (float(np.mean([t["atay"][k] for t in tabs])) if k != "p_max" else tabs[0]["atay"][k])
                       for k in tabs[0]["atay"]}
    return out


def _rng(*ints):
    return np.random.default_rng([0x565731, *[int(i) for i in ints]])


def _cert_key(w: World, *ints):
    return make_key(_NS_CERT, w.world_seed, *ints)


def _window(obs: np.ndarray, t0: int, p: int) -> np.ndarray:
    n = obs.shape[0]
    return obs[:, t0 + 1 - p:t0 + 1, :].reshape(n, -1) if p > 0 else np.zeros((n, 0))


# ----------------------------------------------------------------------------- closure
def closure(w: World, horizons=(1, 2, 4, 8, 16), pasts=(0, 1, 2, 4, 8, 16), blocks=(), n_traj: int = 20000,
            n_oracle: int = 4000, n_rep: int = 16, programs=None, n_programs: int = 0, rate: float = 0.5,
            folds: int = 8, seed: int = 0) -> dict:
    """Level-k-only linear predictor (window p) versus the oracle with privileged (x(t), m(t))
    (Monte Carlo over n_rep fresh-noise branches), conditional on open-loop programs."""
    d = w.designer
    horizons, pasts, blocks = sorted(set(horizons)), sorted(set(pasts) | {0}), sorted(set(blocks))
    t0 = max(max(pasts) - 1, 0)
    taus = sorted(set(horizons) | set(range(1, (max(blocks) if blocks else 0) + 1)))
    H = t0 + max(taus)
    rng = _rng(11, seed)
    progs = [[]] if programs is None else [list(p) for p in programs]
    progs += [d.random_program(rng, H, rate) for _ in range(n_programs)]
    n_or = min(n_oracle, n_traj)
    per, per_se = [], []
    for pi, prog in enumerate(progs):
        P = d.program_dense(prog, H)
        ens = d.ensemble(n_traj, seed=(11, seed, pi))
        ens, rec = d.rollout(ens, P, T=t0, rec=("obs",))
        past = rec["obs"]
        orc = ens.clone(rep=n_rep, idx=np.arange(n_or), keys=member_keys(_cert_key(w, 11, seed, pi), n_or * n_rep))
        _, fr = d.rollout(ens, P, T=max(taus), rec=("obs",))
        _, ofr = d.rollout(orc, P, T=max(taus), rec=("obs",))
        Y = {s: fr["obs"][:, s] for s in taus}
        Yo = {s: ofr["obs"][:, s].reshape(n_or, n_rep, -1) for s in taus}
        Yb = {L: np.concatenate([Y[s] for s in range(1, L + 1)], 1) for L in blocks}
        Yob = {L: np.concatenate([Yo[s] for s in range(1, L + 1)], 2) for L in blocks}
        fold_m = np.array_split(_rng(12, seed, pi).permutation(n_traj), folds)
        fold_o = np.array_split(_rng(13, seed, pi).permutation(n_or), folds)
        tabs = []
        for f in range(folds + 1):
            im = np.arange(n_traj) if f == folds else fold_m[f]
            io = np.arange(n_or) if f == folds else fold_o[f]
            Se, Sed, Seb, Sebd = {}, {}, {}, {}
            cols = [Y[s][im] for s in horizons] + [Yb[L][im] for L in blocks]
            widths = [c.shape[1] for c in cols]
            Ybig = np.concatenate(cols, 1)
            for p in pasts:
                E, dof = ols_residuals(_window(past[im], t0, p), Ybig)
                o = 0
                for c, wd in enumerate(widths):
                    Ec = E[:, o:o + wd]
                    o += wd
                    S = Ec.T @ Ec / dof
                    if c < len(horizons):
                        Se[(horizons[c], p)], Sed[(horizons[c], p)] = S, dof
                    else:
                        L = blocks[c - len(horizons)]
                        Seb[(L, p)], Sebd[(L, p)] = S, dof
            Su, Sud, Sub, Subd = {}, {}, {}, {}
            for s in horizons:
                Su[s], Sud[s] = within_cov(Yo[s][io])
            for L in blocks:
                Sub[L], Subd[L] = within_cov(Yob[L][io])
            tabs.append(closure_tables(Se, Sed, Su, Sud, horizons, pasts, Seb, Sebd, Sub, Subd, blocks))
        full, fl = tabs[-1], tabs[:-1]
        se = {k: np.std([t[k] for t in fl], axis=0, ddof=1) / math.sqrt(folds) for k in _TABLE_KEYS if k in full}
        per.append(full)
        per_se.append(se)
    out = _avg_tables(per, _TABLE_KEYS)
    out["se"] = {k: np.sqrt(np.sum([s[k] ** 2 for s in per_se], axis=0)) / len(per_se) for k in per_se[0]}
    out["per_program"] = per
    out["n_programs"] = len(progs)
    return out


# ----------------------------------------------------------------------------- leak
def leak(w: World, pasts=(0, 1, 2, 4, 8, 16), n_traj: int = 20000, program=None, n_pc: Optional[int] = None,
         threshold: float = 0.5, seed: int = 0) -> dict:
    """Gaussian-proxy posterior of (flattened) level 0 at t given o(t-p+1..t), prior-whitened."""
    d = w.designer
    pasts = sorted(set(pasts))
    t0 = max(max(pasts) - 1, 0)
    P = d.program_dense(program or [], t0 + 1)
    ens = d.ensemble(n_traj, seed=(21, seed))
    _, rec = d.rollout(ens, P, T=t0, rec=("obs", "x"))
    past = rec["obs"]
    h = rec["x"][:, t0]
    Sh = np.cov(h.T, ddof=1).reshape(h.shape[1], h.shape[1])
    W = whiten_basis(Sh, n_pc=n_pc)
    Z = (h - h.mean(0)) @ W
    r = Z.shape[1]
    mus, info, dims = [], [], []
    for p in pasts:
        E, dof = ols_residuals(_window(past, t0, p), Z)
        S = E.T @ E / dof
        mu = np.sort(np.linalg.eigvalsh(S))
        mus.append(mu)
        info.append(0.5 * (logdet(np.eye(r), n_traj - 1) - logdet(S, dof)))
        dims.append(int((mu < threshold).sum()))
    return {"pasts": pasts, "rank": r, "mu": mus, "info_nats": np.array(info), "dim": np.array(dims),
            "threshold": threshold, "hidden_frac": 1.0 - np.array(dims) / max(r, 1)}


# ----------------------------------------------------------------------------- input capacity
def input_capacity(w: World, L: int = 8, p: int = 8, n_states: int = 8, n_traj: int = 20000,
                   delta: Optional[float] = None, program=None, seed: int = 0) -> dict:
    d = w.designer
    C, n = w.inport.admissible, w.n_in
    delta = C.amplitude() if delta is None else delta
    t0 = max(p - 1, 0)
    P = d.program_dense(program or [], t0 + L)
    base = d.ensemble(n_states, seed=(31, seed))
    base, _ = d.rollout(base, P, T=t0, rec=())
    basis = input_basis(C, n)
    nb = basis.shape[1]
    cp = base.clone(rep=nb + 1)                      # shared noise within each state's group
    Pm = np.repeat(P[None], cp.B, axis=0)
    for s in range(n_states):
        Pm[s * (nb + 1) + 1 + np.arange(nb), t0, :] += delta * basis.T
    _, rec = d.rollout(cp, Pm, T=L, rec=("clean",))
    Yr = rec["clean"][:, 1:].reshape(n_states, nb + 1, L, -1)
    G = ((Yr[:, 1:] - Yr[:, :1]) / delta).mean(0)    # (nb, L, n_obs)
    Gb = G.reshape(nb, -1).T                          # (L*n_obs, nb)
    ens = d.ensemble(n_traj, seed=(32, seed))
    _, rec = d.rollout(ens, P, T=t0 + L, rec=("obs",))
    X = _window(rec["obs"], t0, p)
    Yb = rec["obs"][:, t0 + 1:t0 + L + 1].reshape(n_traj, -1)
    E, dof = ols_residuals(X, Yb)
    out = capacity_from_response(Gb, basis, E.T @ E / dof, C, n, seed=seed)
    out.update({"L": L, "p": p, "basis": basis})
    return out


# ----------------------------------------------------------------------------- observation capacity
def observation_capacity(w: World, pasts=(1, 16), n_traj: int = 20000, program=None, seed: int = 0) -> dict:
    d = w.designer
    pasts = sorted(set(pasts))
    var = w.outport.resolution_var
    t0 = max(max(pasts) - 1, 0)
    P = d.program_dense(program or [], t0 + 1)
    ens = d.ensemble(n_traj, seed=(41, seed))
    _, rec = d.rollout(ens, P, T=t0 + 1, rec=("obs", "clean"))
    past = rec["obs"]
    y = rec["obs"][:, t0 + 1]
    n_obs = y.shape[1]
    rates = []
    for p in pasts:
        E, dof = ols_residuals(_window(past, t0, p), y)
        rates.append(math.inf if var <= 0 else 0.5 * (logdet(E.T @ E / dof, dof) - n_obs * math.log(var)))
    v1 = rec["clean"][:, t0].var(0, ddof=1)
    raw = math.inf if var <= 0 else float(0.5 * np.log2(1 + v1 / var).sum())
    return {"pasts": pasts, "rate_bits": np.array(rates) / math.log(2), "channel_bits_upper": raw, "resolution_var": var}


# ----------------------------------------------------------------------------- invariants
def invariant_drift(w: World, T: int = 100, B: int = 64, seed: int = 0, program=None) -> dict:
    d = w.designer
    ens = d.ensemble(B, seed=(51, seed))
    I0 = ens.invariants()
    P = d.program_dense(program, T) if program else None
    ens, _ = d.rollout(ens, P, T=T, rec=())
    I1 = ens.invariants()
    return {k: float(np.abs(I1[k] - I0[k]).max()) for k in I0}


# ----------------------------------------------------------------------------- Fisher information
def _paths(tree, prefix=""):
    if isinstance(tree, dict):
        out = []
        for k in sorted(tree):
            out += _paths(tree[k], f"{prefix}{k}/")
        return out
    if tree is None:
        return []
    return [prefix[:-1]]


def _get(tree, path):
    for part in path.split("/"):
        tree = tree[part]
    return tree


def _set(tree, path, value):
    head, _, rest = path.partition("/")
    new = dict(tree)
    new[head] = value if not rest else _set(tree[head], rest, value)
    return new


def fisher(w: World, wrt: Optional[Sequence[str]] = None, program=None, times=(1, 2, 4), n: int = 20000,
           chunk: Optional[int] = None, seed: int = 0) -> dict:
    """Fisher information of (o(t) for t in times) about level-0 parameters, by autodiff.

    wrt      parameter paths into world.params ('gamma', '0/gamma' for products...); default all
    program  open-loop program (list of (t, input)); inputs are conditioned on, not estimated
    Returns {'linear', 'gaussian' (d x d), 'names', 'theta', 'crb' (Cramer-Rao standard errors from
    'gaussian'), 'times', 'n'}."""
    spec = w.spec
    if not spec.differentiable:
        raise NotDifferentiable("fisher: the world contains a non-differentiable (opaque) block on the path "
                                "from level 0 to the observed level")
    params = w.params
    paths = list(wrt) if wrt else _paths(params)
    if not paths:
        raise ValueError("fisher: the world declares no parameters")
    theta0 = {p: jnp.asarray(_get(params, p), jnp.float64) for p in paths}
    vec0, unravel = ravel_pytree(theta0)
    times = sorted(set(int(t) for t in times))
    H = max(times)
    d = w.designer
    P = d.program_dense(program or [], H)
    chunk = n if chunk is None else int(chunk)
    ki_all = member_keys(_cert_key(w, 81, seed), n)
    kd_all = jax.vmap(lambda k: jax.random.fold_in(k, _ST_DYN))(ki_all)
    tsel = jnp.asarray(times)

    def g(vec, ki, kd):
        p = params
        for path, val in unravel(vec).items():
            p = _set(p, path, val)
        c = jax.vmap(w._init_member, in_axes=(None, 0, 0))(p, ki, kd)
        A = jnp.broadcast_to(jnp.asarray(P)[:, None, :], (H, ki.shape[0], w.n_in))
        _, rec = w._rollout_fn(p, c, A, ("obs_continuous",))
        o = rec["obs_continuous"][tsel]                       # (q, B, n_obs)
        return jnp.swapaxes(o, 0, 1).reshape(ki.shape[0], -1)

    gj = jax.jit(lambda v, ki, kd: (g(v, ki, kd), jax.jacfwd(g)(v, ki, kd)))
    D = vec0.shape[0]
    S1 = S2 = J1 = M = None
    N = 0
    for s in range(0, n, chunk):
        Y, Jn = gj(vec0, ki_all[s:s + chunk], kd_all[s:s + chunk])
        Y, Jn = np.asarray(Y), np.asarray(Jn)                 # (b, m), (b, m, D)
        if S1 is None:
            m = Y.shape[1]
            S1, S2, J1, M = np.zeros(m), np.zeros((m, m)), np.zeros((m, D)), np.zeros((D, m, m))
        S1 += Y.sum(0)
        S2 += Y.T @ Y
        J1 += Jn.sum(0)
        M += np.einsum("bmd,bk->dmk", Jn, Y)
        N += Y.shape[0]
    ybar, Jbar = S1 / N, J1 / N
    Sig = (S2 - N * np.outer(ybar, ybar)) / (N - 1)
    dSig = np.stack([(M[i] + M[i].T - N * (np.outer(Jbar[:, i], ybar) + np.outer(ybar, Jbar[:, i]))) / (N - 1)
                     for i in range(D)])
    Si = np.linalg.inv(Sig)
    lin = Jbar.T @ Si @ Jbar
    A_ = np.einsum("mk,dkl->dml", Si, dSig)
    cov = 0.5 * np.einsum("iml,jlm->ij", A_, A_)
    gauss = lin + cov
    names = []
    for pth in paths:
        sz = int(np.size(theta0[pth]))
        names += [pth] if sz == 1 else [f"{pth}[{i}]" for i in range(sz)]
    try:
        crb = np.sqrt(np.diag(np.linalg.inv(gauss)))
    except np.linalg.LinAlgError:
        crb = np.full(D, np.inf)
    return {"linear": lin, "gaussian": gauss, "covariance_term": cov, "names": names, "theta": np.asarray(vec0),
            "crb": crb, "times": times, "n": N, "dmean": Jbar, "cov_obs": Sig}


# ----------------------------------------------------------------------------- bundle
def certify(w: World, horizons=(1, 2, 4, 8, 16), pasts=(0, 1, 2, 4, 8, 16), n_traj: int = 20000,
            n_programs: int = 2, L: int = 8, seed: int = 0, thresholds: Optional[dict] = None,
            fisher_wrt: Optional[Sequence[str]] = None) -> dict:
    """All certificates plus provisional admission flags (thresholds as VW-0)."""
    th = {"predictable_min": 0.1, "ceiling_min": 0.5, "hidden_frac_min": 0.5, "atom_snr_min": 1.0,
          "invariant_tol": 1e-6}
    th.update(thresholds or {})
    cl = closure(w, horizons, pasts, blocks=(L,), n_traj=n_traj, n_programs=n_programs, seed=seed)
    lk = leak(w, pasts, n_traj=n_traj, seed=seed)
    ic = input_capacity(w, L=L, p=max(pasts), n_traj=n_traj, seed=seed)
    oc = observation_capacity(w, (1, max(pasts)), n_traj=n_traj, seed=seed)
    i1 = cl["horizons"].index(min(cl["horizons"]))
    drift = invariant_drift(w) if w.spec.base.conserved else {}
    flags = {
        "invariants_conserved": bool(all(v <= th["invariant_tol"] for v in drift.values())),
        "finite_resolution": w.outport.resolution_var > 0,
        "nontrivial": bool(cl["predictable"][i1, -1] >= th["predictable_min"]),
        "is_a_level": bool(cl["ceiling"][i1, -1] >= th["ceiling_min"]),
        "level0_hidden": bool(lk["hidden_frac"][-1] >= th["hidden_frac_min"]),
        "inputs_visible": bool(ic["atom_snr_max"] >= th["atom_snr_min"]),
    }
    out = {"contract": "VW-1", "world": w.spec.name, "closure": cl, "leak": lk, "input_capacity": ic,
           "observation_capacity": oc, "invariant_drift": drift, "flags": flags, "thresholds": th}
    if fisher_wrt is not None and w.spec.differentiable:
        out["fisher"] = fisher(w, fisher_wrt, n=min(n_traj, 20000), seed=seed)
    return out


def jsonable(obj):
    """Recursively convert numpy/jax containers to plain JSON types (inf/nan -> strings)."""
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, (np.ndarray, jax.Array)):
        return jsonable(np.asarray(obj).tolist())
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return f if math.isfinite(f) else str(f)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj
