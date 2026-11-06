"""lingauss.py -- the linear-Gaussian VW-0 family, with closed-form certificates.

    x(t+1) = A (x(t) + K u(t)) + w(t),   w ~ N(0, Q)        level 0 (u: actuator vector)
    h1(t)  = C x(t)                                         level 1 (linear projection)
    o(t)   = P_out h1(t) + r eta(t),     eta ~ N(0, I)      observation

x(0) is drawn from the stationary law N(0, Sigma), Sigma = A Sigma A^T + Q. Because inputs
enter the mean only, every closure, leak and capacity number below is independent of the
open-loop program, which the calibration also checks.

Closed forms (agent coordinates C_a = P_out C, B_a = K[:, in_map]):
  oracle error       Su(tau)   = C_a M_tau C_a^T + R,           M_tau = sum_{s<tau} A^s Q A^sT
  window-p error     Se(tau,p) = C_a (A^tau F_p A^tauT + M_tau) C_a^T + R
                     F_p = Kalman filtered covariance after p updates from the stationary
                     prior (identical to Gaussian conditioning on the window; p=inf: steady state)
  leak               generalised eigenvalues of (F_p, Sigma) on the support of Sigma
  response           G_tau = C_a A^tau B_a
"""
from __future__ import annotations

import math
from typing import Optional

import numpy as np

from vecworld import (InputConstraints, ObservationSpec, VectorWorld, WorldSpec, capacity_from_response,
                      closure_tables, leak_spectrum, logdet)


def stationary_cov(A: np.ndarray, Q: np.ndarray, tol: float = 1e-15, max_iter: int = 200) -> np.ndarray:
    """Sigma = A Sigma A^T + Q by doubling (also works when A has unit modes that Q never excites)."""
    S, Ak = Q.copy(), A.copy()
    for _ in range(max_iter):
        S_new = S + Ak @ S @ Ak.T
        Ak = Ak @ Ak
        if np.max(np.abs(S_new - S)) <= tol * max(1.0, np.abs(S_new).max()):
            return (S_new + S_new.T) / 2
        S = S_new
    raise RuntimeError("stationary_cov did not converge (A unstable on the excited subspace?)")


def psd_factor(S: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    w, U = np.linalg.eigh((S + S.T) / 2)
    keep = w > tol * max(w.max(), 1e-300)
    return U[:, keep] * np.sqrt(w[keep])


class LinearGaussian:
    def __init__(self, A, C, Q, r: float, K=None, actuable=None, inputs: Optional[InputConstraints] = None,
                 name: str = "lingauss", replay: str = "initial", max_ticks: Optional[int] = None):
        self.A, self.C, self.Q = np.asarray(A, float), np.asarray(C, float), np.asarray(Q, float)
        self.n0, self.n1 = self.A.shape[0], self.C.shape[0]
        self.r = float(r)
        self.K = np.eye(self.n0) if K is None else np.asarray(K, float)
        self.n_u = self.K.shape[1]
        self.actuable = actuable
        self.inputs = inputs or InputConstraints()
        self.name, self.replay, self.max_ticks = name, replay, max_ticks
        self.Sigma = stationary_cov(self.A, self.Q)
        self.Lq = psd_factor(self.Q)
        self.Fs = psd_factor(self.Sigma)

    def spec(self) -> WorldSpec:
        A, Lq, C, Fs, K = self.A, self.Lq, self.C, self.Fs, self.K
        ident = self.n_u == self.n0 and np.array_equal(K, np.eye(self.n0))
        return WorldSpec(
            n0=self.n0, n1=self.n1,
            law=lambda h, xi: h @ A.T + xi @ Lq.T,
            coarse=lambda h, m: h @ C.T,
            init=lambda rng: Fs @ rng.standard_normal(Fs.shape[1]),
            noise_dim=Lq.shape[1], n_u=self.n_u, actuable=self.actuable,
            kick=None if ident else (lambda h, u: h + u @ K.T),
            inputs=self.inputs, observation=ObservationSpec(noise=self.r),
            replay=self.replay, max_ticks=self.max_ticks, name=self.name,
            invariants={"total": lambda h: h.sum(1)})

    def world(self, world_seed: int = 0) -> VectorWorld:
        return VectorWorld(self.spec(), world_seed)

    # ---- composition in closed form ----
    @staticmethod
    def concat(a: "LinearGaussian", b: "LinearGaussian", inputs=None, name=None) -> "LinearGaussian":
        from scipy.linalg import block_diag
        acta = np.arange(a.n_u) if a.actuable is None else np.asarray(a.actuable)
        actb = np.arange(b.n_u) if b.actuable is None else np.asarray(b.actuable)
        kw = dict(a.inputs.__dict__)
        kw["k"] = None if (a.inputs.k is None or b.inputs.k is None) else a.inputs.k + b.inputs.k
        return LinearGaussian(block_diag(a.A, b.A), block_diag(a.C, b.C), block_diag(a.Q, b.Q), a.r,
                              K=block_diag(a.K, b.K), actuable=np.concatenate([acta, actb + a.n_u]),
                              inputs=inputs or InputConstraints(**kw), name=name or f"{a.name}+{b.name}")

    def stacked(self, C2, name=None) -> "LinearGaussian":
        return LinearGaussian(self.A, np.asarray(C2) @ self.C, self.Q, self.r, K=self.K, actuable=self.actuable,
                              inputs=self.inputs, name=name or f"stack({self.name})")

    def refined(self, Af, Psi, Qf, Lam, name=None) -> "LinearGaussian":
        """Level -1 with x_f(t+1) = Af (x_f + Lam K u) + w_f, coarse-grained by C Psi."""
        return LinearGaussian(Af, self.C @ Psi, Qf, self.r, K=np.asarray(Lam) @ self.K, actuable=self.actuable,
                              inputs=self.inputs, name=name or f"refine({self.name})")


class ClosedForms:
    """Exact certificate values for a LinearGaussian instantiated as `world` (its permutations)."""

    def __init__(self, lg: LinearGaussian, world: VectorWorld):
        self.lg, self.w = lg, world
        self.Ca = lg.C[world.out_map] * world.out_sign[:, None]
        self.Ba = lg.K[:, world.in_map]
        self.R = lg.r ** 2 * np.eye(lg.n1)
        self._M = {0: np.zeros((lg.n0, lg.n0))}
        self._F = {0: lg.Sigma.copy()}
        self._Fp = lg.Sigma.copy()          # predicted covariance before the next update

    def M(self, tau: int) -> np.ndarray:
        A, Q = self.lg.A, self.lg.Q
        while max(self._M) < tau:
            s = max(self._M)
            self._M[s + 1] = A @ self._M[s] @ A.T + Q
        return self._M[tau]

    def F(self, p) -> np.ndarray:
        """Filtered covariance of x(t) given o(t-p+1..t), from the stationary prior."""
        A, Q, C, R = self.lg.A, self.lg.Q, self.Ca, self.R
        if p == math.inf or p is None:
            Pp = self.lg.Sigma.copy()
            for _ in range(100000):
                S = C @ Pp @ C.T + R
                Pf = Pp - Pp @ C.T @ np.linalg.solve(S, C @ Pp)
                Pn = A @ Pf @ A.T + Q
                if np.max(np.abs(Pn - Pp)) < 1e-14 * max(1.0, np.abs(Pn).max()):
                    return (Pf + Pf.T) / 2
                Pp = Pn
            raise RuntimeError("Riccati iteration did not converge")
        while max(self._F) < p:
            S = C @ self._Fp @ C.T + R
            Pf = self._Fp - self._Fp @ C.T @ np.linalg.solve(S, C @ self._Fp)
            Pf = (Pf + Pf.T) / 2
            self._F[max(self._F) + 1] = Pf
            self._Fp = A @ Pf @ A.T + Q
        return self._F[p]

    def Su(self, tau: int) -> np.ndarray:
        return self.Ca @ self.M(tau) @ self.Ca.T + self.R

    def Se(self, tau: int, p) -> np.ndarray:
        Ak = np.linalg.matrix_power(self.lg.A, tau)
        return self.Ca @ (Ak @ self.F(p) @ Ak.T + self.M(tau)) @ self.Ca.T + self.R

    def Se_block(self, L: int, p, Pf: Optional[np.ndarray] = None) -> np.ndarray:
        """Error covariance of [o(t+1),...,o(t+L)] given the window (Pf=0: given x(t))."""
        A = self.lg.A
        Pf = self.F(p) if Pf is None else Pf
        n1 = self.lg.n1
        X = {}
        for j in range(1, L + 1):
            Aj = np.linalg.matrix_power(A, j)
            X[j] = Aj @ Pf @ Aj.T + self.M(j)
        out = np.zeros((L * n1, L * n1))
        for i in range(1, L + 1):
            for j in range(1, i + 1):
                blk = self.Ca @ np.linalg.matrix_power(A, i - j) @ X[j] @ self.Ca.T
                if i == j:
                    blk = blk + self.R
                out[(i - 1) * n1:i * n1, (j - 1) * n1:j * n1] = blk
                out[(j - 1) * n1:j * n1, (i - 1) * n1:i * n1] = blk.T
        return out

    def Su_block(self, L: int) -> np.ndarray:
        return self.Se_block(L, 0, Pf=np.zeros_like(self.lg.Sigma))

    def Se_window(self, tau: int, p: int) -> np.ndarray:
        """Brute-force Gaussian conditioning on the stacked window (cross-check of Se)."""
        A, S, C, R = self.lg.A, self.lg.Sigma, self.Ca, self.R

        def acov(d):
            return C @ np.linalg.matrix_power(A, d) @ S @ C.T + (R if d == 0 else 0)
        n = self.lg.n1
        if p == 0:
            return acov(0)
        Spp = np.zeros((p * n, p * n))
        for i in range(p):
            for j in range(p):
                Spp[i * n:(i + 1) * n, j * n:(j + 1) * n] = acov(i - j) if i >= j else acov(j - i).T
        Sfp = np.concatenate([acov(tau + p - 1 - j) for j in range(p)], 1)
        return acov(0) - Sfp @ np.linalg.solve(Spp, Sfp.T)

    # ---- certificates ----
    def closure(self, horizons=(1, 2, 4, 8, 16), pasts=(0, 1, 2, 4, 8, 16), blocks=()) -> dict:
        horizons, pasts = sorted(set(horizons)), sorted(set(pasts) | {0})
        Se = {(h, p): self.Se(h, p) for h in horizons for p in pasts}
        Su = {h: self.Su(h) for h in horizons}
        Seb = {(L, p): self.Se_block(L, p) for L in blocks for p in pasts}
        Sub = {L: self.Su_block(L) for L in blocks}
        tab = closure_tables(Se, {}, Su, {}, horizons, pasts, Seb, {}, Sub, {}, blocks)
        inf = {"Ve": [np.trace(self.Se(h, math.inf)) for h in horizons],
               "gap_nats": [0.5 * (logdet(self.Se(h, math.inf)) - logdet(self.Su(h))) for h in horizons]}
        if 1 in horizons:
            g1 = 0.5 * (logdet(self.Se(1, 1)) - logdet(self.Su(1)))
            ginf = inf["gap_nats"][horizons.index(1)]
            inf["atay"] = {"leak": g1, "residual": ginf, "memory": g1 - ginf}
        tab["p_inf"] = inf
        return tab

    def leak(self, pasts=(0, 1, 2, 4, 8, 16), threshold: float = 0.5) -> dict:
        pasts = sorted(set(pasts))
        mus = [leak_spectrum(self.F(p), self.lg.Sigma) for p in pasts]
        info = np.array([-0.5 * np.log(np.clip(m, 1e-300, None)).sum() for m in mus])
        dims = np.array([int((m < threshold).sum()) for m in mus])
        r = mus[0].size
        return {"pasts": pasts, "rank": r, "mu": mus, "info_nats": info, "dim": dims,
                "hidden_frac": 1.0 - dims / r, "threshold": threshold,
                "inf": {"mu": leak_spectrum(self.F(math.inf), self.lg.Sigma)}}

    def response(self, L: int) -> np.ndarray:
        A = self.lg.A
        return np.concatenate([self.Ca @ np.linalg.matrix_power(A, s) @ self.Ba for s in range(1, L + 1)], 0)

    def input_capacity(self, L: int = 8, p: int = 8) -> dict:
        out = capacity_from_response(self.response(L), self.Se_block(L, p), self.lg.inputs, self.w.n_in)
        out.update({"L": L, "p": p, "response": self.response(L)})
        return out

    def observation_capacity(self, pasts=(1, 16)) -> dict:
        r2, n = self.lg.r ** 2, self.lg.n1
        rates = [0.5 * (logdet(self.Se(1, p)) - n * math.log(r2)) / math.log(2) for p in sorted(set(pasts))]
        v1 = np.diag(self.Ca @ self.lg.Sigma @ self.Ca.T)
        return {"pasts": sorted(set(pasts)), "rate_bits": np.array(rates),
                "rate_bits_inf": 0.5 * (logdet(self.Se(1, math.inf)) - n * math.log(r2)) / math.log(2),
                "channel_bits_upper": float(0.5 * np.log2(1 + v1 / r2).sum()), "resolution_var": r2}

    def commutation_delta2(self, coarse: "LinearGaussian", Psi: np.ndarray, T: int = 1) -> float:
        """E|| Psi Af^T x - A^T Psi x ||^2 under the fine stationary law (free evolution)."""
        D = Psi @ np.linalg.matrix_power(self.lg.A, T) - np.linalg.matrix_power(coarse.A, T) @ Psi
        return float(np.trace(D @ self.lg.Sigma @ D.T))

    # ---- the exact level-1 reference predictor for exam items (known law, level-1 data only) ----
    def kalman_predict(self, item: dict) -> np.ndarray:
        A, Q, C, R, Ba = self.lg.A, self.lg.Q, self.Ca, self.R, self.Ba
        n_in = self.w.n_in
        past = item["past_obs"]
        P = past.shape[0] - 1
        ap = np.zeros((P, n_in))
        for t, a in item["past_program"]:
            for j, v in a.items():
                ap[t, j] = v
        qs = item["query_times"]
        af = np.zeros((max(qs), n_in))
        for t, a in item["program"]:
            for j, v in a.items():
                af[t, j] = v
        mu, S = np.zeros(self.lg.n0), self.lg.Sigma.copy()

        def update(mu, S, y):
            Sy = C @ S @ C.T + R
            Kg = S @ C.T @ np.linalg.inv(Sy)
            return mu + Kg @ (y - C @ mu), S - Kg @ C @ S

        mu, S = update(mu, S, past[0])
        for t in range(P):
            mu, S = A @ (mu + Ba @ ap[t]), A @ S @ A.T + Q
            mu, S = update(mu, S, past[t + 1])
        out, m = {}, mu.copy()
        for s in range(max(qs)):
            m = A @ (m + Ba @ af[s])
            if s + 1 in qs:
                out[s + 1] = C @ m
        return np.stack([out[q] for q in qs])


# --------------------------------------------------------------------------- toy worlds
def ring(n: int = 24, n_blocks: int = 6, D: float = 0.2, gamma: float = 0.05, sigma: float = 0.3,
         r: float = 0.2, conserve: bool = False, k: int = 2, b: float = 1.0, zero_sum: bool = True,
         total: Optional[float] = None, name: Optional[str] = None) -> LinearGaussian:
    """Damped diffusion on a ring of n sites, observed as n_blocks block sums. conserve=True:
    no damping and zero-sum noise, so total mass is exactly conserved (singular Sigma)."""
    I = np.eye(n)
    Lap = 2 * I - np.roll(I, 1, 0) - np.roll(I, -1, 0)
    g = 0.0 if conserve else gamma
    A = (1 - g) * (I - D * Lap)
    Q = sigma ** 2 * ((I - np.ones((n, n)) / n) if conserve else I)
    C = np.kron(np.eye(n_blocks), np.ones((1, n // n_blocks)))
    inp = InputConstraints(k=k, lo=-b, hi=b, zero_sum=zero_sum, total=total)
    return LinearGaussian(A, C, Q, r, inputs=inp, name=name or ("ring-conserved" if conserve else "ring"))


def random_lg(n0: int = 16, n1: int = 4, rho: float = 0.9, sigma: float = 0.3, r: float = 0.2,
              n_act: int = 12, k: int = 3, b: float = 0.5, seed: int = 1) -> LinearGaussian:
    """A generic non-normal stable system with correlated noise and a dense random projection;
    only n_act of the n0 coordinates are actuable."""
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((n0, n0)) / math.sqrt(n0)
    A *= rho / np.max(np.abs(np.linalg.eigvals(A)))
    G = rng.standard_normal((n0, n0)) / math.sqrt(n0)
    Q = sigma ** 2 * (G @ G.T + 0.1 * np.eye(n0))
    C = rng.standard_normal((n1, n0)) / math.sqrt(n0)
    return LinearGaussian(A, C, Q, r, actuable=np.arange(n_act),
                          inputs=InputConstraints(k=k, lo=-b, hi=b), name="random")


def lumpable_refinement(lg: LinearGaussian, kappa: float = 0.5, sigma_int: float = 0.2, eta: float = 0.0):
    """Split every level-0 site in two. Psi = pair sums, Lam = Psi^T/2 (Psi Lam = I).
    Af = Lam A Psi + kappa*K_int + eta*Lam*Dif, with K_int the projector on pair differences and
    Dif the pair-difference map. eta=0: exactly lumpable (Psi Af = A Psi, Psi Qf Psi^T = Q),
    so level 1 is unchanged in distribution; eta != 0 lets internal differences leak upward."""
    n = lg.n0
    Psi = np.kron(np.eye(n), np.ones((1, 2)))
    Dif = np.kron(np.eye(n), np.array([[1.0, -1.0]]))
    Lam = Psi.T / 2
    Kint = Dif.T @ Dif / 2
    Af = Lam @ lg.A @ Psi + kappa * Kint + eta * Lam @ Dif
    Qf = Lam @ lg.Q @ Lam.T + sigma_int ** 2 * Kint
    return Af, Psi, Qf, Lam
