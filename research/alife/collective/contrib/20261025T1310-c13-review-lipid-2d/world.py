"""lipid-2d (c12): implicit-solvent amphiphiles (Cooke-Kremer-Deserno 3-bead lipids) in 2D, overdamped Langevin.

Each lipid is a head bead H and two tail beads T1, T2: FENE bonds H-T1-T2, a harmonic H-T2 spring (rest 4 sigma)
that keeps it straight, WCA repulsion between all beads (b_HH = b_HT = 0.95, b_TT = 1), and a broad attraction
between tail beads only, -eps cos^2(pi (r - r_c) / (2 w_c)) for r_c < r < r_c + w_c (and -eps inside r_c).
No solvent particles: the hydrophobic effect is the tail attraction. From a random gas the lipids should
self-assemble into micelles, bilayer segments and closed bilayer rings (2D vesicles); the boundary is the
material itself. WORLD_P (JSON) overrides P.

Membrane chemistry (off by default): a fraction 1 - fa of the lipids start as precursors whose tails are
hydrophilic (type 2: no tail attraction). Each frame a precursor whose tail beads touch n active tail beads
(within rcat) of other lipids converts at rate kcat n (autocatalytic membrane growth); active lipids revert at
rate kdeg. Intramolecular pairs have no WCA (bonds only). Bead types: 0 head, 1 active tail, 2 precursor tail.
"""
import json, os, numpy as np
from numba import njit

P = dict(fa=1.0, kcat=0.0, kdeg=0.0, rcat=1.6, L=80.0, N=800, kT=0.55, eps=1.0, wc=1.5, dt=0.006, sub=50, kfene=30.0, rinf=1.5, kbend=10.0, bh=1.3, dmax=0.1)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {"name": "lipid-2d", "family": "lipid-particle", "size": (128, 128), "steps_per_frame": 1,
        "dt": P["dt"] * P["sub"], "channels": ["lipid heads", "lipid tails"], "matter": [1], "threshold": 0.5,
        "smooth": 1.0, "periodic": True, "radial_channels": [0, 1]}


@njit
def forces(x, typ, L, eps, wc, kfene, rinf, kbend, N, bh):
    n = x.shape[0]; F = np.zeros_like(x); rc_t = 2 ** (1 / 6) * 1.0; rcut = max(rc_t + wc, 2 ** (1 / 6) * bh)
    nc = int(L // rcut); cs = L / nc
    head = -np.ones(nc * nc, np.int64); nxt = -np.ones(n, np.int64)
    for i in range(n):
        cx = int(x[i, 0] / cs) % nc; cy = int(x[i, 1] / cs) % nc; c = cx * nc + cy
        nxt[i] = head[c]; head[c] = i
    for i in range(n):
        cx = int(x[i, 0] / cs) % nc; cy = int(x[i, 1] / cs) % nc
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                c = ((cx + dx) % nc) * nc + (cy + dy) % nc; j = head[c]
                while j >= 0:
                    if j > i and j // 3 != i // 3:
                        rx = x[j, 0] - x[i, 0]; ry = x[j, 1] - x[i, 1]
                        rx -= L * np.round(rx / L); ry -= L * np.round(ry / L)
                        r2 = rx * rx + ry * ry
                        if r2 < rcut * rcut:
                            r = np.sqrt(r2); f = 0.0  # f = -dV/dr
                            b = 1.0 if (typ[i] > 0 and typ[j] > 0) else (bh if (typ[i] == 0 and typ[j] == 0) else 0.5 * (1.0 + bh))
                            if r < 2 ** (1 / 6) * b:
                                s6 = (b / r) ** 6; f += 24 * (2 * s6 * s6 - s6) / r
                            if typ[i] == 1 and typ[j] == 1 and r > rc_t:
                                a = np.pi * (r - rc_t) / (2 * wc)
                                f += -eps * np.pi / wc * np.cos(a) * np.sin(a)  # attraction: f < 0
                            F[i, 0] -= f * rx / r; F[i, 1] -= f * ry / r
                            F[j, 0] += f * rx / r; F[j, 1] += f * ry / r
                    j = nxt[j]
    for m in range(N):  # bonds
        for (a, b2, kind) in ((3 * m, 3 * m + 1, 0), (3 * m + 1, 3 * m + 2, 0), (3 * m, 3 * m + 2, 1)):
            rx = x[b2, 0] - x[a, 0]; ry = x[b2, 1] - x[a, 1]
            rx -= L * np.round(rx / L); ry -= L * np.round(ry / L)
            r = np.sqrt(rx * rx + ry * ry) + 1e-12
            if kind == 0:
                q = min(r / rinf, 0.99); f = -kfene * r / (1 - q * q)
            else:
                f = -kbend * (r - 4.0)
            F[a, 0] -= f * rx / r; F[a, 1] -= f * ry / r
            F[b2, 0] += f * rx / r; F[b2, 1] += f * ry / r
    return F


@njit
def contacts(x, typ, L, rc, N):
    """number of active tail beads within rc of each lipid's two tail beads (other lipids only)"""
    n = x.shape[0]; nc = max(1, int(L // rc)); cs = L / nc; out = np.zeros(N, np.int64)
    head = -np.ones(nc * nc, np.int64); nxt = -np.ones(n, np.int64)
    for i in range(n):
        if typ[i] == 1:
            c = (int(x[i, 0] / cs) % nc) * nc + int(x[i, 1] / cs) % nc; nxt[i] = head[c]; head[c] = i
    for m in range(N):
        for i in (3 * m + 1, 3 * m + 2):
            cx = int(x[i, 0] / cs) % nc; cy = int(x[i, 1] / cs) % nc
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    j = head[((cx + dx) % nc) * nc + (cy + dy) % nc]
                    while j >= 0:
                        if j // 3 != m:
                            rx = x[j, 0] - x[i, 0]; ry = x[j, 1] - x[i, 1]
                            rx -= L * np.round(rx / L); ry -= L * np.round(ry / L)
                            if rx * rx + ry * ry < rc * rc: out[m] += 1
                        j = nxt[j]
    return out


def init(seed, size):
    rng = np.random.default_rng(seed); N, L = P["N"], P["L"]
    c = rng.uniform(0, L, (N, 2)); th = rng.uniform(0, 2 * np.pi, N)
    d = np.stack([np.cos(th), np.sin(th)], 1)
    x = np.concatenate([c[:, None, :] + k * 1.0 * d[:, None, :] for k in range(3)], 1).reshape(-1, 2) % L
    act = rng.random(N) < P["fa"]
    typ = np.zeros(3 * N, np.int64); typ[1::3] = np.where(act, 1, 2); typ[2::3] = np.where(act, 1, 2)
    return {"x": x, "typ": typ, "rng": rng, "size": size}


def step(s):
    x, typ, rng = s["x"], s["typ"], s["rng"]; dt, kT = P["dt"], P["kT"]
    for _ in range(P["sub"]):
        F = forces(x, typ, P["L"], P["eps"], P["wc"], P["kfene"], P["rinf"], P["kbend"], P["N"], P["bh"])
        d = F * dt + np.sqrt(2 * kT * dt) * rng.standard_normal(x.shape)
        nd = np.sqrt((d ** 2).sum(1))[:, None]; d = np.where(nd > P["dmax"], d * P["dmax"] / nd, d)
        x = (x + d) % P["L"]
    s["x"] = x
    if P["kcat"] > 0 or P["kdeg"] > 0:  # membrane chemistry: precursor -> lipid at an existing bilayer; lipid -> precursor
        T = dt * P["sub"]; n_act = contacts(x, typ, P["L"], P["rcat"], P["N"])
        u = rng.random(P["N"]); act = typ[1::3] == 1
        conv = (~act) & (n_act > 0) & (u < 1 - np.exp(-P["kcat"] * n_act * T))
        deg = act & (u < 1 - np.exp(-P["kdeg"] * T))
        for m in np.nonzero(conv)[0]: typ[3 * m + 1] = typ[3 * m + 2] = 1
        for m in np.nonzero(deg)[0]: typ[3 * m + 1] = typ[3 * m + 2] = 2
    return s


def fields(s):
    H, W = s["size"]; L = P["L"]; out = np.zeros((2, H, W), np.float32)
    ix = (s["x"] / L * W).astype(int) % W
    for ch, t in ((0, 0), (1, 1)):
        m = (s["typ"] == 0) if t == 0 else (s["typ"] == 1)
        np.add.at(out[ch], (ix[m, 1] % H, ix[m, 0]), 1.0)
    from scipy.ndimage import gaussian_filter
    return np.stack([gaussian_filter(o, 1.0, mode="wrap") for o in out]).astype(np.float32)


def stats(s):
    return {"N": int(P["N"])}
