"""Evolving protocells: N catalyst alleles, rare mutation patches, random dilution (fork of ad2-catalysts).

Fields: droplet material phi (Cahn-Hilliard, slow mobility), fuel u, catalyst alleles a_i
(i = 0..N-1) that replicate only inside droplets and mutually inhibit (winner-take-all per
droplet). Allele i has catalytic rate k_i, so droplets of different alleles grow and divide
at different speeds.

    prod   = u c^2 sum_i k_i a_i,          c = (1 + phi)/2
    dphi   = M lap(phi^3 - phi - kappa lap phi) + prod - kd c
    du     = Du lap u + F (1 - u) - prod
    da_i   = Dc lap a_i + r c a_i (1 - a_i - beta sum_{j!=i} a_j) - g (1 - c) a_i

Two stochastic events (seeded RNG, deterministic per seed):
  * mutation: at rate mut per unit time, a random point inside droplet material (c > 0.7)
    gets a disk of radius rm converted to a random other allele. The patch is a minority
    inside its droplet, so it is usually out-competed; it fixes only if it ends up in a
    daughter at division (segregation), or in a small droplet.
  * dilution: at rate dil per unit time, a random disk of radius rd is erased (material and
    catalyst removed; fuel untouched). Unbiased with respect to allele; it creates turnover.

All droplets start as allele 0 (the slowest); variation arises only by mutation.
"""
import numpy as np
from labkit import ops

META = {
    "name": "ad5-evolve",
    "family": "phase-field",
    "parent": "ad2-catalysts",
    "mutation": "N catalyst alleles with different rates, rare local mutation patches, random dilution disks",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["phi (droplet material)", "u (fuel)", "a0 (k=0.10)", "a1 (k=0.12)", "a2 (k=0.14)", "a3 (k=0.16)"],
    "matter": [0],
    "threshold": 0.0,
}

P = dict(M=0.03, kappa=1.0, k="0.10,0.12,0.14,0.16", kd=0.02, F=0.004, Du=2.0, Dc=0.05, r=0.05, beta=1.1,
         g=0.05, mut=0.002, rm=5.0, dil=0.0005, rd=10.0, dt=0.5, A=2.0, phi0=-0.95, noise=0.01, seeds=6, r0=6.0)


def kvec():
    return np.array([float(x) for x in str(P["k"]).split(",")])


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    N = len(kvec())
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    a = np.zeros((N, H, W))
    for _ in range(P["seeds"]):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
        a[0][m] = 0.9
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"rng": rng, "t": 0.0, "phi": phi, "u": np.ones((H, W)), "a": a, "k2": k2, "shape": (H, W),
            "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2,
            "denc": 1 + dt * P["Dc"] * k2, "events": []}


def step(s):
    phi, u, a, k2, dt, M = s["phi"], s["u"], s["a"], s["k2"], P["dt"], P["M"]
    sh, rng = s["shape"], s["rng"]
    c = np.clip((1 + phi) / 2, 0, 1)
    kv = kvec()
    prod = u * c ** 2 * np.tensordot(kv, a, 1)
    ph = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(phi ** 3 - phi - P["A"] * phi)
          + dt * ops.rfft2(prod - P["kd"] * c)) / s["den"]
    s["phi"] = ops.irfft2(ph, sh)
    s["u"] = ops.irfft2((ops.rfft2(u) + dt * ops.rfft2(P["F"] * (1 - u) - prod)) / s["denu"], sh)
    tot = a.sum(0)
    ra = P["r"] * c * a * (1 - a - P["beta"] * (tot - a)) - P["g"] * (1 - c) * a
    s["a"] = np.clip(ops.irfft2((ops.rfft2(a) + dt * ops.rfft2(ra)) / s["denc"], sh), 0, None)
    s["t"] += dt
    H, W = sh
    if rng.random() < P["mut"] * dt:
        ys, xs = np.nonzero(c > 0.7)
        if len(ys):
            j = rng.integers(len(ys))
            m = ops.disk(H, W, ys[j], xs[j], P["rm"])
            cur = int(np.argmax(s["a"][:, ys[j], xs[j]]))
            new = (cur + rng.integers(1, len(kv))) % len(kv)
            s["a"][:, m] = 0.0
            s["a"][new][m] = 0.9
            s["events"].append(("mut", s["t"], int(ys[j]), int(xs[j]), cur, int(new)))
    if rng.random() < P["dil"] * dt:
        y, x = rng.integers(0, H), rng.integers(0, W)
        m = ops.disk(H, W, y, x, P["rd"])
        s["phi"][m] = -1.0
        s["a"][:, m] = 0.0
        s["events"].append(("dil", s["t"], int(y), int(x)))
    return s


def fields(s):
    return np.concatenate([s["phi"][None], s["u"][None], s["a"]])


def damage(s, mask):
    s["phi"][mask] = -1.0
    s["a"][:, mask] = 0.0
    return s
