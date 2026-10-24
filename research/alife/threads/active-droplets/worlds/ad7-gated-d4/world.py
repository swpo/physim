"""Gated protocells: heritable membrane thickness under a permeability/retention trade-off.

Forks: ad5-evolve (alleles, mutation patches, dilution) + ad3-membrane (self-made amphiphile
shell) + fisim-beyond-laplacian's membrane-gated diffusion div(D e^{-beta m} grad c).

Fields: phi (Cahn-Hilliard droplet material, slow M), fuel u, amphiphile psi, catalyst
alleles a_i. All alleles catalyse equally (k); allele i differs only in amphiphile output kp_i.
The amphiphile shell gates diffusion of everything that crosses it:

    fuel      du   = div(Du e^{-bu psi} grad u) + F (1 - u) - prod          (small molecule: weak gate)
    catalyst  da_i = div(Dc e^{-bc psi} grad a_i) + r c a_i (1 - a_i - beta sum_j!=i a_j) - g (1-c) a_i
    psi       dpsi = Dp div(grad psi - chi psi grad|grad phi|^2) + prod * sum_i kp_i a_i / sum_i a_i - gp psi
    phi       dphi = M lap(phi^3 - phi - kappa lap phi) + prod - kd c,   prod = k u c^2 sum_i a_i

Catalyst diffuses (Dc) and dies outside droplets, so a leaky droplet loses its catalyst and
then dissolves. A thick shell retains catalyst but starves the droplet of fuel.
Mutation patches and dilution disks as in ad5. All droplets start as allele 0 (thinnest).
Variable-coefficient diffusion: implicit with the ungated D, explicit correction (stable).
"""
import numpy as np
from labkit import ops

META = {
    "name": "ad7-gated-d4",
    "family": "phase-field",
    "parent": "ad7-gated",
    "mutation": "4x dilution rate (dil 0.0005 -> 0.002): turnover so non-dividing droplets are replaced",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.5,
    "channels": ["phi (droplet material)", "u (fuel)", "psi (amphiphile)", "a0 (kp=0)", "a1 (kp=0.5)", "a2 (kp=1.5)", "a3 (kp=4)"],
    "matter": [0],
    "threshold": 0.0,
}

P = dict(M=0.03, kappa=1.0, k=0.15, kd=0.02, F=0.004, Du=2.0, bu=0.5, Dc=0.3, bc=3.0, r=0.05, beta=1.1, g=0.05,
         kp="0.0,0.5,1.5,4.0", Dp=0.3, chi=8.0, gp=0.01, mut=0.002, rm=5.0, dil=0.002, rd=10.0,
         dt=0.5, A=2.0, phi0=-0.95, noise=0.01, seeds=6, r0=6.0, allele0=0)


def kpvec():
    return np.array([float(x) for x in str(P["kp"]).split(",")])


def gated_div(c, D):
    """div(D grad c) with face-averaged D (conservative 5-point)."""
    out = np.zeros_like(c)
    for ax in (-2, -1):
        Df = 0.5 * (D + np.roll(D, -1, ax))
        fl = Df * (np.roll(c, -1, ax) - c)
        out += fl - np.roll(fl, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    N = len(kpvec())
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    a = np.zeros((N, H, W))
    for _ in range(P["seeds"]):
        m = ops.disk(H, W, rng.integers(0, H), rng.integers(0, W), P["r0"])
        phi[m] = 0.9
        a[P["allele0"]][m] = 0.9
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt, M = P["dt"], P["M"]
    return {"rng": rng, "t": 0.0, "phi": phi, "u": np.ones((H, W)), "psi": np.zeros((H, W)), "a": a,
            "k2": k2, "shape": (H, W), "events": [],
            "den": 1 + dt * M * k2 * (P["A"] + P["kappa"] * k2), "denu": 1 + dt * P["Du"] * k2,
            "denc": 1 + dt * P["Dc"] * k2, "denp": 1 + dt * P["Dp"] * k2}


def lap_fd(x):
    return ops.laplacian(x)


def step(s):
    phi, u, psi, a, k2, dt, M = s["phi"], s["u"], s["psi"], s["a"], s["k2"], P["dt"], P["M"]
    sh, rng = s["shape"], s["rng"]
    c = np.clip((1 + phi) / 2, 0, 1)
    tot = a.sum(0)
    prod = P["k"] * u * c ** 2 * tot
    ph = (ops.rfft2(phi) - dt * M * k2 * ops.rfft2(phi ** 3 - phi - P["A"] * phi)
          + dt * ops.rfft2(prod - P["kd"] * c)) / s["den"]
    s["phi"] = ops.irfft2(ph, sh)
    # gated fuel: implicit ungated Du, explicit (gated - ungated) correction
    Dgu = P["Du"] * np.exp(-P["bu"] * psi)
    ru = gated_div(u, Dgu) - P["Du"] * lap_fd(u) + P["F"] * (1 - u) - prod
    s["u"] = ops.irfft2((ops.rfft2(u) + dt * ops.rfft2(ru)) / s["denu"], sh)
    Dgc = P["Dc"] * np.exp(-P["bc"] * psi)
    ra = (np.stack([gated_div(ai, Dgc) for ai in a]) - P["Dc"] * np.stack([lap_fd(ai) for ai in a])
          + P["r"] * c * a * (1 - a - P["beta"] * (tot - a)) - P["g"] * (1 - c) * a)
    s["a"] = np.clip(ops.irfft2((ops.rfft2(a) + dt * ops.rfft2(ra)) / s["denc"], sh), 0, None)
    kpm = np.tensordot(kpvec(), a, 1) / np.maximum(tot, 1e-6)
    gy, gx = ops.grad(phi)
    vy, vx = ops.grad(gy ** 2 + gx ** 2)
    rp = -P["Dp"] * P["chi"] * ops.upwind_flux_div(psi, vy, vx) + prod * kpm - P["gp"] * psi
    s["psi"] = np.clip(ops.irfft2((ops.rfft2(psi) + dt * ops.rfft2(rp)) / s["denp"], sh), 0, None)
    s["t"] += dt
    H, W = sh
    N = a.shape[0]
    if N > 1 and rng.random() < P["mut"] * dt:
        ys, xs = np.nonzero(c > 0.7)
        if len(ys):
            j = rng.integers(len(ys))
            m = ops.disk(H, W, ys[j], xs[j], P["rm"])
            cur = int(np.argmax(s["a"][:, ys[j], xs[j]]))
            new = (cur + rng.integers(1, N)) % N
            s["a"][:, m] = 0.0
            s["a"][new][m] = 0.9
            s["events"].append(("mut", s["t"], int(ys[j]), int(xs[j]), cur, int(new)))
    if rng.random() < P["dil"] * dt:
        y, x = rng.integers(0, H), rng.integers(0, W)
        m = ops.disk(H, W, y, x, P["rd"])
        s["phi"][m] = -1.0
        s["a"][:, m] = 0.0
        s["psi"][m] = 0.0
        s["events"].append(("dil", s["t"], int(y), int(x)))
    return s


def fields(s):
    return np.concatenate([s["phi"][None], s["u"][None], s["psi"][None], s["a"]])


def damage(s, mask):
    s["phi"][mask] = -1.0
    s["a"][:, mask] = 0.0
    s["psi"][mask] = 0.0
    return s
