"""Substrate-feedback enzyme condensates (c27), after Demarchi, Goychuk, Maryshev & Frey, PRL 130:128401 (2023)
(equations as transcribed in research/alife/LITERATURE.md section 2.4.3).

phi in [-1, 1]: condensate (enzyme) order parameter, Cahn-Hilliard with constant mobility M;
enzyme density c = c_lo + (1 - c_lo) (1 + phi) / 2.
s: substrate, p = 1 - s: product (s + p is uniform and conserved because both diffuse at D).
    dphi/dt = M lap( -phi + phi^3 - kappa lap phi + chi s )
    ds/dt   = D lap s - k1 c s + k2 (1 - s)
chi < 0: the enzyme is drawn toward substrate. Catalysis inside a condensate depletes s there, so a
condensate is pulled outward on every side; past a threshold in M |chi| the symmetric state is unstable and the
condensate self-propels toward fresh substrate (Demarchi et al.). The product recycles to substrate at k2
(closed chemistry: nothing is fed or removed).
Initial condition: phi = mean + noise everywhere (unstructured), s = 1.
Numerics: dx = 1, semi-implicit spectral (linear stabilisation A for CH; implicit diffusion for s).
WORLD_P (JSON) overrides P.
"""
import json, os
import numpy as np

P = dict(M=1.0, kappa=1.0, chi=-0.5, D=1.0, k1=0.2, k2=0.02, c_lo=0.1, mean=-0.45, noise=0.05, dt=0.05, A=2.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {
    "name": "frey-condensates",
    "family": "catalysis-induced-phase-separation",
    "parent": "Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3)",
    "mutation": "new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)",
    "size": (128, 128),
    "steps_per_frame": 100,
    "dt": P["dt"],
    "channels": ["condensate (1+phi)/2", "substrate s"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 0.0,
    "periodic": True,
}


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]; kx = 2 * np.pi * np.fft.fftfreq(W)[None, :]
    k2 = ky ** 2 + kx ** 2
    phi = P["mean"] + P["noise"] * rng.standard_normal((H, W))
    dt = P["dt"]
    return {"phi": phi, "s": np.ones((H, W)), "k2": k2,
            "denp": 1 + dt * P["M"] * k2 * (P["A"] + P["kappa"] * k2), "dens": 1 + dt * P["D"] * k2}


def step(st):
    phi, s, k2, dt = st["phi"], st["s"], st["k2"], P["dt"]
    mu_nl = phi ** 3 - (1 + P["A"]) * phi + P["chi"] * s      # -phi + phi^3 + chi s, minus the implicit A phi
    ph = (np.fft.fft2(phi) - dt * P["M"] * k2 * np.fft.fft2(mu_nl)) / st["denp"]
    c = P["c_lo"] + (1 - P["c_lo"]) * (1 + np.clip(phi, -1, 1)) / 2
    rs = -P["k1"] * c * s + P["k2"] * (1 - s)
    sh = (np.fft.fft2(s + dt * rs)) / st["dens"]
    st["phi"] = np.real(np.fft.ifft2(ph)); st["s"] = np.real(np.fft.ifft2(sh))
    return st


def fields(st):
    return np.stack([(1 + st["phi"]) / 2, st["s"]]).astype(np.float32)


def damage(st, mask):
    st["phi"][mask] = -1.0
    return st
