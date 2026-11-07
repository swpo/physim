"""vw.nats -- information budgets for Gaussian input channels (EXAM.md section 3).

If an agent command u enters as a shift E u before (or into) Gaussian noise of covariance S that
is present at every tick, the path laws with and without the command differ by

    KL(P_u || P_0) = sum_t c(u_t),     c(u) = 1/2 (E u)^T S^+ (E u)      (Gaussian chain rule)

whatever the downstream dynamics (data processing), and the same sum bounds the KL of any level
and port. A component of E u outside range(S) has no counterpart in the no-input law: its cost is
infinite and the command is rejected. With S public, every charge is a public function of the
command, so admissibility is publicly decidable.

NatsBudget      the public declaration: metric M = E^T S^+ E (agent coordinates), the infinite-cost
                directions, and caps per tick, per episode and in total.
NatsAccountant  the per-agent counters. check() / check_program() raise InputViolation before
                anything runs (nothing is charged); charge() after a command has run.

Closed forms and certificates: shift_kl (the path KL of a program of shifts), gaussian_kl,
shift_llr (per-path log-likelihood ratio of observed residuals; its mean under P_u estimates the
KL, as in program/track2/checks/kl_ring.py), kl_check (Monte Carlo mean against the charge), and
card_guarantee (what a charge C guarantees; the chi-square bound is informative only below ~2 nats).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np

from .ports import InputViolation


def _psd_pinv(S: np.ndarray, rtol: float = 1e-10):
    """(pseudo-inverse, orthonormal basis of the null space) of a symmetric PSD matrix."""
    S = (np.asarray(S, float) + np.asarray(S, float).T) / 2
    w, U = np.linalg.eigh(S)
    keep = w > rtol * max(float(w.max()), 1e-300)
    Ur = U[:, keep]
    return (Ur / w[keep]) @ Ur.T, U[:, ~keep]


@dataclass(frozen=True)
class NatsBudget:
    """Public input-information budget (agent coordinates).

    metric   (n_in, n_in) PSD matrix M: c(u) = 1/2 u^T M u nats
    null     (n_in, r) orthonormal directions of infinite cost (E u outside range(S)); may be empty
    tick     per-tick cap c_max (None: none)
    episode  per-episode cap kappa_ep (None: none)
    total    cap over the whole investigation kappa_tot (None: none)
    tol      absolute tolerance of the caps (nats) and relative tolerance of the null test
    """
    metric: np.ndarray
    null: Optional[np.ndarray] = None
    tick: Optional[float] = None
    episode: Optional[float] = None
    total: Optional[float] = None
    tol: float = 1e-9
    note: str = ""

    def __post_init__(self):
        M = np.asarray(self.metric, float)
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            raise ValueError("NatsBudget: metric must be square")
        if not np.allclose(M, M.T, atol=1e-12 * max(1.0, np.abs(M).max())):
            raise ValueError("NatsBudget: metric must be symmetric")
        if np.linalg.eigvalsh(M).min() < -1e-9 * max(1.0, np.abs(M).max()):
            raise ValueError("NatsBudget: metric must be positive semi-definite")
        object.__setattr__(self, "metric", M)
        nul = np.zeros((M.shape[0], 0)) if self.null is None else np.asarray(self.null, float).reshape(M.shape[0], -1)
        object.__setattr__(self, "null", nul)
        for k in ("tick", "episode", "total"):
            v = getattr(self, k)
            if v is not None and not v >= 0:
                raise ValueError(f"NatsBudget: {k} cap must be >= 0")

    # ---- constructors ----
    @staticmethod
    def from_cov(cov, embed=None, **caps) -> "NatsBudget":
        """Inputs enter as a shift E u before Gaussian noise of covariance cov (public)."""
        S = np.atleast_2d(np.asarray(cov, float))
        E = np.eye(S.shape[0]) if embed is None else np.asarray(embed, float)
        Si, N = _psd_pinv(S)
        M = E.T @ Si @ E
        # agent directions whose image has a component in null(S): infinite cost
        if N.shape[1]:
            B = N.T @ E                                   # (r, n_in)
            _, s, Vt = np.linalg.svd(B, full_matrices=False)
            nul = Vt[s > 1e-10 * max(1.0, s.max(initial=0.0))].T
        else:
            nul = np.zeros((E.shape[1], 0))
        return NatsBudget(metric=(M + M.T) / 2, null=nul, **caps)

    @staticmethod
    def isotropic(n_in: int, sigma: float, **caps) -> "NatsBudget":
        """Shift u (identity embedding) before N(0, sigma^2 I): c(u) = |u|^2 / (2 sigma^2)."""
        return NatsBudget(metric=np.eye(n_in) / float(sigma) ** 2, **caps)

    @property
    def n_in(self) -> int:
        return self.metric.shape[0]

    # ---- costs ----
    def cost(self, u) -> float:
        """Nats of one command (dense vector or {coord: value}); inf outside the noise range."""
        v = self._dense(u)
        if self.null.shape[1]:
            nrm = float(np.linalg.norm(v))
            if nrm > 0 and float(np.linalg.norm(self.null.T @ v)) > 1e-9 * nrm:
                return math.inf
        return 0.5 * float(v @ self.metric @ v)

    def _dense(self, u) -> np.ndarray:
        if u is None:
            return np.zeros(self.n_in)
        if isinstance(u, dict):
            v = np.zeros(self.n_in)
            for j, x in u.items():
                v[int(j)] = float(x)
            return v
        v = np.asarray(u, float).reshape(-1)
        if v.shape != (self.n_in,):
            raise InputViolation(f"format: a dense input must have shape ({self.n_in},), got {v.shape}")
        return v

    def program_cost(self, program) -> float:
        """Total nats of a program [(t, u), ...] (or {t: u})."""
        items = program.items() if isinstance(program, dict) else (program or [])
        return float(sum(self.cost(u) for _, u in items))

    def public(self) -> dict:
        return {"unit": "nats", "cost": "1/2 u^T M u per tick", "metric": self.metric.tolist(),
                "infinite_cost_directions": self.null.T.tolist(), "tick_cap": self.tick,
                "episode_cap": self.episode, "total_cap": self.total, "note": self.note}


class NatsAccountant:
    """Counters for one agent (or one exam episode). Every decision uses only the command, the
    public budget and the counters."""

    def __init__(self, budget: NatsBudget):
        self.budget = budget
        self.episode_used = 0.0
        self.total_used = 0.0
        self.n_episodes = 0
        self.n_commands = 0

    def new_episode(self):
        self.episode_used = 0.0
        self.n_episodes += 1

    def violations(self, c: float, episode_used: Optional[float] = None, total_used: Optional[float] = None) -> list:
        b = self.budget
        e = self.episode_used if episode_used is None else episode_used
        T = self.total_used if total_used is None else total_used
        msgs = []
        if not math.isfinite(c):
            msgs.append("nats: the command has a component outside the range of the input-channel noise "
                        "(infinite KL)")
            return msgs
        if b.tick is not None and c > b.tick + b.tol:
            msgs.append(f"nats: command costs {c:.6g} > per-tick cap {b.tick:g}")
        if b.episode is not None and e + c > b.episode + b.tol:
            msgs.append(f"nats: episode total would be {e + c:.6g} > episode cap {b.episode:g}")
        if b.total is not None and T + c > b.total + b.tol:
            msgs.append(f"nats: investigation total would be {T + c:.6g} > total cap {b.total:g}")
        return msgs

    def check(self, u, where: str = "") -> float:
        """Raise InputViolation if u is not admissible now; return its cost. Charges nothing."""
        c = self.budget.cost(u)
        msgs = self.violations(c)
        if msgs:
            raise InputViolation(f"{where}input rejected, nothing charged: " + "; ".join(msgs))
        return c

    def check_program(self, program, where: str = "", episode_used: Optional[float] = None) -> float:
        """Validate a whole program (cumulative caps) before any of it runs; return its cost."""
        items = sorted(program.items() if isinstance(program, dict) else list(program or []), key=lambda e: int(e[0]))
        e = self.episode_used if episode_used is None else float(episode_used)
        T = self.total_used
        tot = 0.0
        for t, u in items:
            c = self.budget.cost(u)
            msgs = self.violations(c, e, T)
            if msgs:
                raise InputViolation(f"{where}program entry t={int(t)}: input rejected, nothing charged: "
                                     + "; ".join(msgs))
            e, T, tot = e + c, T + c, tot + c
        return tot

    def charge(self, u) -> float:
        c = self.budget.cost(u)
        if c > 0:
            self.episode_used += c
            self.total_used += c
            self.n_commands += 1
        return c

    def usage(self) -> dict:
        b = self.budget
        return {"episode_nats": self.episode_used, "total_nats": self.total_used,
                "episode_left": None if b.episode is None else max(b.episode - self.episode_used, 0.0),
                "total_left": None if b.total is None else max(b.total - self.total_used, 0.0),
                "episodes": self.n_episodes, "commands": self.n_commands}


# ----------------------------------------------------------------------------- closed forms
def shift_kl(shifts, cov) -> float:
    """Path KL of x' = g(x) + s_t + xi, xi ~ N(0, cov), against s = 0 (same initial law):
    1/2 sum_t s_t^T cov^+ s_t (inf if some s_t leaves range(cov))."""
    Si, N = _psd_pinv(np.atleast_2d(cov))
    tot = 0.0
    for s in np.atleast_2d(np.asarray(shifts, float)):
        if N.shape[1] and np.linalg.norm(N.T @ s) > 1e-9 * max(np.linalg.norm(s), 1e-300):
            return math.inf
        tot += 0.5 * float(s @ Si @ s)
    return tot


def gaussian_kl(m0, S0, m1, S1) -> float:
    """KL(N(m0, S0) || N(m1, S1)) for non-singular covariances."""
    m0, m1 = np.asarray(m0, float), np.asarray(m1, float)
    S0, S1 = np.atleast_2d(S0), np.atleast_2d(S1)
    d = m0.size
    L1 = np.linalg.cholesky(S1)
    A = np.linalg.solve(L1, S0)
    tr = float(np.trace(np.linalg.solve(L1.T, A)))
    dm = np.linalg.solve(L1, m1 - m0)
    ld0 = np.linalg.slogdet(S0)[1]
    ld1 = 2.0 * np.log(np.diag(L1)).sum()
    return 0.5 * (tr + float(dm @ dm) - d + ld1 - ld0)


def shift_llr(residuals, shifts, cov) -> np.ndarray:
    """Per-path log-likelihood ratio log dP_u/dP_0 of observed residuals r_t = x_{t+1} - g(x_t)
    (leading axes: paths; then time, then dimension), for shifts s_t (time, dimension)."""
    Si, _ = _psd_pinv(np.atleast_2d(cov))
    r = np.asarray(residuals, float)
    s = np.asarray(shifts, float)
    a = np.einsum("...ti,ij,...tj->...t", r, Si, r)
    b = np.einsum("...ti,ij,...tj->...t", r - s, Si, r - s)
    return 0.5 * (a - b).sum(-1)


def kl_check(llr, charge: float) -> dict:
    """Monte Carlo certificate: mean LLR under P_u against the declared charge."""
    llr = np.asarray(llr, float).reshape(-1)
    m, se = float(llr.mean()), float(llr.std(ddof=1) / math.sqrt(llr.size))
    return {"charge_nats": float(charge), "mc_nats": m, "mc_se": se,
            "z": (m - charge) / se if se > 0 else math.nan, "n": int(llr.size)}


def card_guarantee(C: float) -> dict:
    """What an episode charge C guarantees for every level and port."""
    return {"kl_nats": float(C),
            "chi2_mean_shift_in_sd": math.sqrt(math.expm1(2 * C)) if C < 350 else math.inf,
            "linear_gaussian_mean_shift_in_sd": math.sqrt(2 * C),
            "chi2_bound_informative": bool(C <= 2.0)}
