"""Pilot P0: when is block pooling the optimal learned coarse-graining? (closed form, CPU, ~1 min)

Level 0: x(t+1) = A x(t) + w(t), w ~ N(0, Q), on a ring of n sites.
  conservative     A = I - D Lap,            Q = s^2 Lap   (mass moves along bonds; total fixed)
  nonconservative  A = (1-g)(I - D Lap),     Q = s^2 I     (damped, locally forced)
Level 1: y = C_w x, C_w = kron(I_{n/b}, w^T): one block-local, translation-equivariant linear
feature per block (the hypothesis class "local + equivariant + width 1").
Candidates for w:
  uniform   block sum (pooling)
  pca       top eigenvector of the within-block covariance (optimal width-1 linear autoencoder,
            reconstruction loss)
  tica      top generalised eigenvector of (sym lag-tau autocovariance, covariance) within a block
            (slowest feature; the VAMP/TICA objective restricted to the class)
  closure   argmax over w of the closure ceiling c(tau) of the whole level-1 process (whole past,
            Kalman filter), the objective "level 1 predicts itself as well as level 0 would"
Metrics (Gaussian closed forms, as vw.lingauss): ceiling c(tau) = (V0 - Ve)/(V0 - Vu), gap
Gamma(tau) = 1/2 [logdet Se - logdet Su] (nats), predictive information
I1 = I(y_{<=t}; y_{t+1}) = 1/2 [logdet Cov y - logdet Se(1)] (non-triviality).
Run: /home/user/evalwork/vecworld/vw1/.venv/bin/python -B pilot_pooling.py
"""
import json
import math
import time

import numpy as np
from scipy.optimize import minimize

N = 64
TAUS = (1, 2, 4, 8, 16, 32)
OUT = "/home/user/evalwork/vecworld/program/track1/pooling.json"


def lap(n):
    I = np.eye(n)
    return 2 * I - np.roll(I, 1, 0) - np.roll(I, -1, 0)


def system(kind, n=N, D=0.2, g=0.05, s=1.0):
    L, I = lap(n), np.eye(n)
    if kind == "conservative":
        A, Q = I - D * L, s ** 2 * L
    else:
        A, Q = (1 - g) * (I - D * L), s ** 2 * I
    S = Q.copy()
    for _ in range(20000):  # stationary covariance (zero mode stays 0 in the conservative case)
        S_new = A @ S @ A.T + Q
        if np.max(np.abs(S_new - S)) < 1e-12:
            S = S_new
            break
        S = S_new
    return A, Q, S


def Cw(w, n=N):
    b = len(w)
    return np.kron(np.eye(n // b), np.asarray(w, float)[None, :])


def certs(A, Q, S, C, taus=TAUS, rel_r=1e-3):
    Vy = C @ S @ C.T
    r2 = max((rel_r ** 2) * np.trace(Vy) / C.shape[0], 1e-10)
    R = r2 * np.eye(C.shape[0])
    F = S.copy()  # filtered cov of x(t) | y(<=t): iterate predict/update to stationarity
    for _ in range(5000):
        P = A @ F @ A.T + Q
        K = P @ C.T @ np.linalg.inv(C @ P @ C.T + R)
        F_new = P - K @ C @ P
        if np.max(np.abs(F_new - F)) < 1e-11:
            F = F_new
            break
        F = F_new
    M, Ap, out = np.zeros_like(A), np.eye(len(A)), {}
    c, gap, Ve_l, Vu_l = [], [], [], []
    V0 = np.trace(Vy + R)
    for t in range(1, max(taus) + 1):
        M = A @ M @ A.T + Q
        Ap = A @ Ap
        if t == 1:
            Se1 = C @ (Ap @ F @ Ap.T + M) @ C.T + R
            I1 = 0.5 * (np.linalg.slogdet(Vy + R)[1] - np.linalg.slogdet(Se1)[1])
        if t in taus:
            Su = C @ M @ C.T + R
            Se = C @ (Ap @ F @ Ap.T + M) @ C.T + R
            Ve, Vu = np.trace(Se), np.trace(Su)
            c.append(float((V0 - Ve) / (V0 - Vu)) if (V0 - Vu) > 1e-8 * max(V0, 1e-300) + 1e-9 else float('nan'))
            gap.append(0.5 * (np.linalg.slogdet(Se)[1] - np.linalg.slogdet(Su)[1]))
    return {"ceiling": c, "gap_nats": gap, "pred_info_nats": float(I1)}


def block_cov(S, b, lagA=None):
    B = S[:b, :b] if lagA is None else (lagA @ S)[:b, :b]
    return B


def candidates(A, Q, S, b, tau_star):
    out = {"uniform": np.ones(b) / math.sqrt(b)}
    ev, V = np.linalg.eigh(block_cov(S, b))
    out["pca"] = V[:, -1] * np.sign(V[:, -1].sum() or 1.0)
    out["pca_eig_ratio"] = float(ev[-1] / ev[-2]) if b > 1 else None
    Ct = np.linalg.matrix_power(A, tau_star) @ S
    Ct = 0.5 * (Ct + Ct.T)[:b, :b]
    C0 = S[:b, :b]
    Lc = np.linalg.cholesky(C0 + 1e-12 * np.eye(b))
    Li = np.linalg.inv(Lc)
    e2, U = np.linalg.eigh(Li @ Ct @ Li.T)
    wt = Li.T @ U[:, -1]
    out["tica"] = wt / np.linalg.norm(wt) * np.sign(wt.sum() or 1.0)

    def neg(wv):
        wv = wv / (np.linalg.norm(wv) + 1e-15)
        return -certs(A, Q, S, Cw(wv), taus=(tau_star,))["ceiling"][0]

    best = None
    starts = [np.ones(b), out["pca"], out["tica"]] + [np.random.default_rng(i).standard_normal(b) for i in range(2)]
    for x0 in starts:
        r = minimize(neg, x0, method="Nelder-Mead", options={"maxiter": 400 * b, "xatol": 1e-6, "fatol": 1e-9})
        if best is None or r.fun < best.fun:
            best = r
    wc = best.x / np.linalg.norm(best.x)
    out["closure"] = wc * np.sign(wc.sum() or 1.0)
    return out


def cos_to_uniform(w):
    w = np.asarray(w, float)
    return float(abs(w.sum()) / (math.sqrt(len(w)) * np.linalg.norm(w)))


def main():
    t0 = time.time()
    res = {"what": __doc__.split("\n")[0], "n_sites": N, "taus": TAUS, "systems": {}}
    for kind, D, g in (("conservative", 0.2, 0.0), ("nonconservative", 0.2, 0.05), ("nonconservative_fastdecay", 0.05, 0.5)):
        A, Q, S = system("conservative" if kind == "conservative" else "nonconservative", D=D, g=g)
        sysres = {"D": D, "gamma": g, "pooling_sweep": {}, "b8": {}}
        # 1. pooling sweep over block size (degeneracy at both ends)
        for b in (1, 2, 4, 8, 16, 32, 64):
            r = certs(A, Q, S, Cw(np.ones(b)))
            sysres["pooling_sweep"][b] = {"ceiling": [round(v, 4) for v in r["ceiling"]],
                                         "gap_nats": [round(v, 4) for v in r["gap_nats"]],
                                         "pred_info_nats": round(r["pred_info_nats"], 4)}
        # 2. candidates for b = 8 and b = 4
        for b in (4, 8):
            cand = candidates(A, Q, S, b, tau_star=4)
            row = {"pca_top_eig_ratio": cand.pop("pca_eig_ratio")}
            for name, w in cand.items():
                r = certs(A, Q, S, Cw(w))
                row[name] = {"w": [round(v, 3) for v in w], "cos_to_uniform": round(cos_to_uniform(w), 4),
                             "ceiling": [round(v, 4) for v in r["ceiling"]],
                             "gap_nats": [round(v, 4) for v in r["gap_nats"]],
                             "pred_info_nats": round(r["pred_info_nats"], 4)}
            # flatness of the objective: ceiling at tau=4 over random positive and random signed w
            rng = np.random.default_rng(0)
            cpos = [certs(A, Q, S, Cw(rng.uniform(0, 1, b)), taus=(4,))["ceiling"][0] for _ in range(40)]
            csig = [certs(A, Q, S, Cw(rng.standard_normal(b)), taus=(4,))["ceiling"][0] for _ in range(40)]
            row["random_w_ceiling_tau4"] = {"positive_median": round(float(np.median(cpos)), 4),
                                            "positive_min": round(float(np.min(cpos)), 4),
                                            "signed_median": round(float(np.median(csig)), 4),
                                            "signed_min": round(float(np.min(csig)), 4)}
            sysres[f"b{b}"] = row
        res["systems"][kind] = sysres
        print(kind, "done", round(time.time() - t0, 1), "s", flush=True)
    res["wall_seconds"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
