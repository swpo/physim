"""Q3 check: what hydrodynamic theory predicts for our closure certificate (closed form, numpy only).

World: the conservative linear ring of track 1's pilot P0 (x' = (I - D Lap) x + xi, Cov xi = sigma^2 Lap;
D = 0.2, sigma = 1), i.e. linear fluctuating hydrodynamics on a lattice. Coarse-graining: sums over G = 8
blocks of b sites. Ceiling c(tau) = (V0 - Ve) / (V0 - Vu) with the whole level-1 past (stationary Kalman
filter, noiseless block sums) and with the present value only.

Three questions:
 A. Under the stationary (equilibrium-fluctuation) law, does the ceiling at fixed macroscopic time
    s = D tau / b^2 improve as the block grows? (Diffusive scaling says no: the curve should collapse.)
 B. Under a law with a macroscopic profile on top of the fluctuations (the setting of the hydrodynamic
    limit), does the deficit 1 - c fall as 1/b?
 C. Fluctuation-response at level 1: for which pushes does the passive level-1 correlation function
    predict the level-1 response?

Run: python q3_hydro_scaling.py   (about 6 CPU-seconds; writes q3_hydro_scaling.json)
"""
import json
import time

import numpy as np

D, SIG, G = 0.2, 1.0, 8


def modes(n):
    """Real orthonormal Fourier basis without the k = 0 mode, and the Laplacian eigenvalues."""
    i = np.arange(n)
    cols, lam, kk = [], [], []
    for k in range(1, n // 2 + 1):
        l = 2 - 2 * np.cos(2 * np.pi * k / n)
        if 2 * k == n:
            cols.append(np.cos(np.pi * i) / np.sqrt(n)); lam.append(l); kk.append(k)
        else:
            cols.append(np.sqrt(2 / n) * np.cos(2 * np.pi * k * i / n)); lam.append(l); kk.append(k)
            cols.append(np.sqrt(2 / n) * np.sin(2 * np.pi * k * i / n)); lam.append(l); kk.append(k)
    return np.stack(cols, 1), np.array(lam), np.array(kk)


def riccati(a, Q, H, tol=1e-12):
    """Stationary prediction covariance for x' = diag(a) x + xi, y = H x (noiseless), by plain iteration
    from the stationary prior; returns the filtered covariance Cov(x_t | y_<=t)."""
    P = np.diag(Q / (1 - a ** 2))
    for it in range(200000):
        S = H @ P @ H.T
        K = P @ H.T @ np.linalg.pinv(S, rcond=1e-12, hermitian=True)
        Pf = P - K @ H @ P
        Pf = (Pf + Pf.T) / 2
        Pn = (a[:, None] * Pf) * a[None, :] + np.diag(Q)
        if np.max(np.abs(Pn - P)) < tol * np.abs(Pn).max():
            return Pf, it
        P = Pn
    raise RuntimeError("no convergence")


def world(b):
    n = G * b
    V, lam, kk = modes(n)
    a = 1 - D * lam                      # mode multipliers
    q = SIG ** 2 * lam                   # mode noise variances (conservative noise)
    c = q / (1 - a ** 2)                 # stationary mode variances = sigma^2 / (D (2 - D lam))
    Phi = np.kron(np.eye(G), np.ones((1, b)))
    return n, V, lam, kk, a, q, c, Phi @ V, Phi


def ceilings(b, s_list):
    n, V, lam, kk, a, q, c, H, Phi = world(b)
    C = np.diag(c)
    Pf_inf, iters = riccati(a, q, H)
    Sy = H @ C @ H.T
    Pf_0 = C - C @ H.T @ np.linalg.pinv(Sy, rcond=1e-12, hermitian=True) @ H @ C
    out = {"b": b, "n": n, "riccati_iterations": iters, "rows": []}
    for s in s_list:
        tau = int(round(s * b * b / D))
        at = a ** tau
        N = q * (1 - a ** (2 * tau)) / (1 - a ** 2)          # accumulated noise per mode
        Vu = np.trace(H @ np.diag(N) @ H.T)
        V0 = np.trace(Sy)

        def Ve(P):
            return np.trace(H @ ((at[:, None] * P) * at[None, :] + np.diag(N)) @ H.T)
        out["rows"].append({"s": s, "tau": tau, "Vu_over_V0": Vu / V0,
                            "c_whole_past": (V0 - Ve(Pf_inf)) / (V0 - Vu),
                            "c_present_only": (V0 - Ve(Pf_0)) / (V0 - Vu)})
    return out


def profile_deficit(b, s_list, amp=1.0, kmax=2):
    """One-shot prediction from y_0 when a random macroscopic profile (modes k <= kmax, per-site variance
    amp^2) sits on top of the equilibrium fluctuations."""
    n, V, lam, kk, a, q, c, H, Phi = world(b)
    low = kk <= kmax
    ct = c + amp ** 2 * n / low.sum() * low
    C = np.diag(ct)
    Sy = H @ C @ H.T
    P0 = C - C @ H.T @ np.linalg.pinv(Sy, rcond=1e-12, hermitian=True) @ H @ C
    rows = []
    for s in s_list:
        tau = int(round(s * b * b / D))
        at = a ** tau
        N = q * (1 - a ** (2 * tau)) / (1 - a ** 2)
        Vu = np.trace(H @ np.diag(N) @ H.T)
        V0 = np.trace(H @ np.diag(at ** 2 * ct + N) @ H.T)
        Ve = np.trace(H @ ((at[:, None] * P0) * at[None, :] + np.diag(N)) @ H.T)
        rows.append({"s": s, "tau": tau, "deficit": (Ve - Vu) / (V0 - Vu)})
    return {"b": b, "amp": amp, "rows": rows}


def fdt(b, s_list):
    """Level-1 response to a level-0 push u against the passive prediction C_y(tau) C_y(0)^-1 Phi u."""
    n, V, lam, kk, a, q, c, H, Phi = world(b)
    Sy = H @ np.diag(c) @ H.T
    Syi = np.linalg.pinv(Sy, rcond=1e-12, hermitian=True)
    pushes = {}
    u = np.zeros(n); u[:b] = 1 / b; u[4 * b:5 * b] = -1 / b; pushes["block-uniform, blocks 0 and 4"] = u
    u = np.zeros(n); u[b // 2] = 1; u[4 * b + b // 2] = -1; pushes["single sites at block centres"] = u
    u = np.zeros(n); u[b - 1] = 1; u[4 * b] = -1; pushes["single sites at block edges"] = u
    u = np.zeros(n); u[3 * b // 4] = 1; u[b // 4] = -1; pushes["two sites inside block 0"] = u
    lift = np.diag(c) @ H.T @ Syi @ (Phi @ pushes["block-uniform, blocks 0 and 4"])
    out = {"b": b, "pushes": {}}
    ref = None
    for name, u in list(pushes.items()) + [("Markov-projection lift of the same block push", None)]:
        uh = lift if u is None else V.T @ u
        rows = []
        for s in s_list:
            tau = int(round(s * b * b / D))
            at = a ** tau
            resp = H @ (at * uh)
            pred = H @ np.diag(at * c) @ H.T @ Syi @ (H @ uh)
            rows.append({"s": s, "tau": tau, "response_norm": float(np.linalg.norm(resp)),
                         "fdt_rel_error": float(np.linalg.norm(resp - pred) / max(np.linalg.norm(resp), 1e-300))})
        out["pushes"][name] = rows
    return out


if __name__ == "__main__":
    t0 = time.process_time()
    S = [0.05, 0.2, 0.8]
    res = {"world": {"D": D, "sigma": SIG, "blocks": G, "law": "x' = (I - D Lap) x + xi, Cov xi = sigma^2 Lap",
                     "macro_time": "s = D tau / b^2", "total_mass": "conditioned to 0 (k = 0 mode removed)"},
           "A_stationary": [ceilings(b, S) for b in (2, 4, 8, 16, 32)],
           "B_profile": [profile_deficit(b, S) for b in (2, 4, 8, 16, 32, 64)],
           "C_fdt": fdt(16, S)}
    res["cpu_seconds"] = round(time.process_time() - t0, 1)
    with open(__file__.replace(".py", ".json"), "w") as f:
        json.dump(res, f, indent=1)
    for r in res["A_stationary"]:
        print("A b=%2d" % r["b"], " ".join("s=%.2f c_inf=%.4f c_0=%.4f" % (x["s"], x["c_whole_past"], x["c_present_only"]) for x in r["rows"]))
    for r in res["B_profile"]:
        print("B b=%2d" % r["b"], " ".join("s=%.2f def=%.5f" % (x["s"], x["deficit"]) for x in r["rows"]))
    for k, rows in res["C_fdt"]["pushes"].items():
        print("C", k, " ".join("s=%.2f |R|=%.4f err=%.3f" % (x["s"], x["response_norm"], x["fdt_rel_error"]) for x in rows))
    print("cpu", res["cpu_seconds"])
