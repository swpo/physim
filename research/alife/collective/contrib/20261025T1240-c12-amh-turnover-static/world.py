"""active-model-h (c12): Cahn-Hilliard fluid with Stokes hydrodynamics and an active interfacial stress.

phi (order parameter, -1 solvent / +1 droplet) is advected by an incompressible Stokes flow u:
    d phi/dt + u . grad phi = M lap mu,   mu = -phi + phi^3 - kappa lap phi
    eta lap u - grad p + f = 0, div u = 0,  f = -phi grad mu + div sigma_a,
    sigma_a = -zeta (grad phi grad phi - |grad phi|^2 I / 2)   (zeta > 0 extensile, < 0 contractile, Active Model H)
Optional turnover (Model-A reaction) -eps (phi - phi_t) bounds domain growth chemically. Pseudo-spectral on a periodic
square, Stokes solved exactly in Fourier with the transverse projector; CH stiff term semi-implicit.
WORLD_P (JSON) overrides P."""
import json, os, numpy as np
P = dict(M=0.1, kappa=1.0, eta=1.0, zeta=-1.0, eps=0.0, phi_t=-0.4, phi0=-0.4, noise=0.05, dx=1.0, dt=0.05, S=2.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))
META = {"name": "active-model-h", "family": "active-model-h", "size": (128, 128), "steps_per_frame": 200, "dt": P["dt"],
        "channels": ["phi + 1", "flow speed |u|"], "matter": [0], "threshold": 0.5, "smooth": 0.5, "periodic": True,
        "radial_channels": [0, 1]}


def init(seed, size):
    rng = np.random.default_rng(seed); H, W = size
    phi = P["phi0"] + P["noise"] * rng.standard_normal((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, P["dx"]); kx = 2 * np.pi * np.fft.fftfreq(W, P["dx"])
    KY, KX = np.meshgrid(ky, kx, indexing="ij"); k2 = KY ** 2 + KX ** 2
    deal = (np.abs(KY) < (2 / 3) * np.abs(ky).max()) & (np.abs(KX) < (2 / 3) * np.abs(kx).max())
    return {"phi": phi, "KY": KY, "KX": KX, "k2": k2, "deal": deal, "u": np.zeros((2, H, W))}


def grad(fk, s):
    return np.fft.ifft2(1j * s["KY"] * fk).real, np.fft.ifft2(1j * s["KX"] * fk).real


def step(s):
    phi, KY, KX, k2, dt = s["phi"], s["KY"], s["KX"], s["k2"], P["dt"]
    D = s["deal"]
    pk = np.fft.fft2(phi) * D
    gy, gx = grad(pk, s)
    mu = -phi + phi ** 3 - P["kappa"] * np.fft.ifft2(-k2 * pk).real
    my, mx = grad(np.fft.fft2(mu) * D, s)
    fy, fx = -phi * my, -phi * mx
    z = P["zeta"]
    if z != 0:  # div sigma_a, sigma_a = -zeta (g g - |g|^2/2 I)
        syy = -z * (gy * gy - 0.5 * (gy * gy + gx * gx)); sxx = -syy; sxy = -z * gy * gx
        fy = fy + np.fft.ifft2(D * (1j * KY * np.fft.fft2(syy) + 1j * KX * np.fft.fft2(sxy))).real
        fx = fx + np.fft.ifft2(D * (1j * KY * np.fft.fft2(sxy) + 1j * KX * np.fft.fft2(sxx))).real
    Fy, Fx = np.fft.fft2(fy) * D, np.fft.fft2(fx) * D
    kk = np.where(k2 == 0, 1, k2)
    dot = (KY * Fy + KX * Fx) / kk
    uy = np.fft.ifft2(np.where(k2 == 0, 0, (Fy - KY * dot) / (P["eta"] * kk))).real
    ux = np.fft.ifft2(np.where(k2 == 0, 0, (Fx - KX * dot) / (P["eta"] * kk))).real
    adv = uy * gy + ux * gx
    nl = np.fft.fft2(phi ** 3 - phi) * s["deal"]
    rhs = np.fft.fft2(phi) + dt * (-P["M"] * k2 * nl + P["M"] * P["S"] * k2 * pk - np.fft.fft2(adv) * s["deal"] - P["eps"] * np.fft.fft2(phi - P["phi_t"]))
    pk = rhs / (1 + dt * P["M"] * (P["kappa"] * k2 ** 2 + P["S"] * k2))
    s["phi"] = np.fft.ifft2(pk).real; s["u"] = np.stack([uy, ux])
    return s


def fields(s):
    return np.stack([s["phi"] + 1, np.hypot(*s["u"])]).astype(np.float32)


def stats(s):
    return {"mean_phi": round(float(s["phi"].mean()), 4), "umax": round(float(np.hypot(*s["u"]).max()), 4)}
