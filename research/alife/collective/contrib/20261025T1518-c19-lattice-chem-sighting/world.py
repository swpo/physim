"""Lattice artificial chemistry after Ono & Ikegami (ECAL'99, adap-org/9905002), c19.

Integer particle counts per site on a periodic square lattice, five species:
W water, X substrate (food), A autocatalyst, M membrane, Y waste. Total particle number is conserved.
Moves: every particle attempts a hop with probability p_i per step to one of 4 neighbours, accepted
with min(1, exp(-(E_i(target) - E_i(here)))), where E_i(x) = eps * sum_j phi_ij <n_j>_3x3(x) / n0
(pairwise repulsion with neighbours; hops are drawn as sequential binomials, so counts stay >= 0).
Reactions per site (Poisson numbers of events, capped by the reactant counts):
    X + 2A -> 3A        (autocatalysis, ka X A^2 / n0^2)
    X + 2A -> M + 2A    (membrane made by A, km X A^2 / n0^2)
    A -> Y,  M -> Y     (decay, kdA, kdM)
    Y -> X              (recharge, ky: the resource regrows from waste; closed mass)
The membrane only forms and holds A if the repulsions make M sit between A and W:
phi_AW large, phi_AM and phi_MW intermediate, and an orientation bonus lam |grad(rho_A - rho_W)| for M. No body is planted: A starts as uniform noise.
WORLD_P (JSON) overrides P.
"""
import json, os
import numpy as np

META = {
    "name": "lattice-chem",
    "family": "lattice-artificial-chemistry",
    "parent": None,
    "mutation": "new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["A (autocatalyst)", "M (membrane)", "X (food)", "Y (waste)"],
    "matter": [0],
    "smooth": 1.0,
    "periodic": True,
    "radial_channels": [0, 1, 2],
}
SP = ["W", "X", "A", "M", "Y"]
P = dict(n0=20.0, W0=10.0, X0=8.0, A0=1.0, Y0=1.0, eps=5.0,
         pW=0.5, pX=0.5, pA=0.2, pM=0.1, pY=0.5,
         ka=0.4, km=0.15, kdA=0.01, kdM=0.01, ky=0.02,
         phi_AW=1.5, phi_AM=0.5, phi_MW=0.5, phi_MM=-0.1, phi_AA=0.0, phi_base=0.2, phi_X=0.0, lam=25.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def phimat():
    n = len(SP); F = np.full((n, n), P["phi_base"])
    W, X, A, M, Y = range(5)
    def put(i, j, v): F[i, j] = F[j, i] = P["phi_base"] + v
    put(A, W, P["phi_AW"]); put(A, M, P["phi_AM"]); put(M, W, P["phi_MW"]); put(M, M, P["phi_MM"]); put(A, A, P["phi_AA"])
    for j in range(5): put(X, j, P["phi_X"]); put(Y, j, P["phi_X"])
    return F


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    n = np.stack([rng.poisson(P[k + "0"] if k != "M" else 0.0, (H, W)) if k != "M" else np.zeros((H, W), np.int64)
                  for k in SP]).astype(np.int64)
    return {"n": n, "rng": rng, "F": phimat(), "t": 0}


def box(a):
    return sum(np.roll(np.roll(a, i, -2), j, -1) for i in (-1, 0, 1) for j in (-1, 0, 1)) / 9.0


def step(s):
    n, rng, F = s["n"], s["rng"], s["F"]
    # --- hops
    rho = box(n.astype(float)) / P["n0"]
    E = P["eps"] * np.einsum("ij,jhw->ihw", F, rho)
    # oriented membrane (mean field of Ono-Ikegami's oriented M): an M particle that points its head to W
    # and its tail to A gains energy in proportion to the A-W contrast across it
    d = rho[2] - rho[0]
    gx = 0.5 * (np.roll(d, -1, -1) - np.roll(d, 1, -1)); gy = 0.5 * (np.roll(d, -1, -2) - np.roll(d, 1, -2))
    E[3] -= P["lam"] * np.hypot(gx, gy)
    mob = np.array([P["pW"], P["pX"], P["pA"], P["pM"], P["pY"]])
    dirs = [(1, -2), (-1, -2), (1, -1), (-1, -1)]
    out = np.zeros_like(n); inc = np.zeros_like(n)
    left = n.copy(); used = np.zeros(E.shape)
    for k, (sh, ax) in enumerate(dirs):
        dE = np.roll(E, -sh, ax) - E  # energy at the target minus here
        acc = np.minimum(1.0, np.exp(-dE)) * mob[:, None, None] / 4
        # sequential binomials: probability for this direction conditional on not having taken an earlier one
        cond = np.clip(acc / np.maximum(1 - used, 1e-9), 0, 1); used = used + acc
        m = rng.binomial(left, cond)
        left -= m; out += m; inc += np.roll(m, sh, ax)
    n = n - out + inc
    # --- reactions
    W, X, A, M, Y = range(5)
    n0 = P["n0"]
    a2 = n[A] * np.maximum(n[A] - 1, 0) / n0 ** 2
    ra = rng.poisson(P["ka"] * n[X] * a2); ra = np.minimum(ra, n[X])
    n[X] -= ra; n[A] += ra
    rm = rng.poisson(P["km"] * n[X] * a2); rm = np.minimum(rm, n[X])
    n[X] -= rm; n[M] += rm
    da = rng.binomial(n[A], P["kdA"]); dm = rng.binomial(n[M], P["kdM"])
    n[A] -= da; n[M] -= dm; n[Y] += da + dm
    dy = rng.binomial(n[Y], P["ky"]); n[Y] -= dy; n[X] += dy
    s["n"] = n; s["t"] += 1
    return s


def fields(s):
    n = s["n"].astype(np.float32)
    return np.stack([n[2], n[3], n[1], n[4]])


def stats(s):
    n = s["n"]
    return {k: int(n[i].sum()) for i, k in enumerate(SP)}
