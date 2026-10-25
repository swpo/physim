"""Active phase-field crystal (Menzel and Loewen 2013): localized crystallites that rest or travel.

phi: conserved density (mean psi_bar). P: polarization, transported and relaxing.
    d phi/dt = lap[(eps + (1 + lap)^2) phi + phi^3] - v0 div P
    d P/dt   = C1 lap P - Dr C1 P - v0 grad phi
Spectral, periodic. The stiff part -k^2 (1 - k^2)^2 of the phi equation and the P relaxation are implicit;
the eps term, phi^3 and the v0 couplings are explicit. Units: lattice wavenumber 1, dx = pi/4.
Individuals = localized crystallite patches in a liquid of uniform density (coexistence regime).
WORLD_P (JSON) overrides P.
"""
import numpy as np
import json as _json, os as _os

META = {
    "name": "apfc",
    "family": "active-pfc",
    "parent": "new class (Menzel & Loewen 2013 active phase-field crystal)",
    "mutation": "none (benchmark model)",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 0.1,
    "channels": ["crystal amplitude (smoothed (phi - mean)^2)", "density phi", "|P|"],
    "matter": [0],
    "smooth": 1.0,
    "periodic": True,
}
P = dict(eps=-1.5, psi=-0.75, v0=0.25, C1=0.1, Dr=0.5, dx=np.pi / 4, dt=0.1, amp=0.5, ic="noise", kappa=0.0, psi0=-0.75)
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    phi = P["psi"] + P["amp"] * rng.standard_normal((H, W))
    phi += P["psi"] - phi.mean()
    ky = 2 * np.pi * np.fft.fftfreq(H, d=P["dx"]); kx = 2 * np.pi * np.fft.fftfreq(W, d=P["dx"])
    KY, KX = np.meshgrid(ky, kx, indexing="ij"); k2 = KX ** 2 + KY ** 2
    g = np.exp(-k2 * 4.0)  # smoothing kernel for the amplitude readout (length ~ 2 = one third of a lattice spacing)
    return {"phi": phi, "Px": np.zeros((H, W)), "Py": np.zeros((H, W)), "KX": KX, "KY": KY, "k2": k2, "g": g, "t": 0}


def step(s):
    dt, v0, C1, Dr = P["dt"], P["v0"], P["C1"], P["Dr"]
    k2, KX, KY = s["k2"], s["KX"], s["KY"]
    ph = np.fft.fft2(s["phi"]); px = np.fft.fft2(s["Px"]); py = np.fft.fft2(s["Py"])
    nl = np.fft.fft2(s["phi"] ** 3)
    expl = -k2 * (P["eps"] * ph + nl) - 1j * v0 * (KX * px + KY * py)
    if P["kappa"]:  # non-conserved exchange with a bath at density psi0 (feed for the liquid, decay for the peaks)
        expl = expl + P["kappa"] * np.fft.fft2(P["psi0"] - s["phi"])
    ph_new = (ph + dt * expl) / (1 + dt * k2 * (1 - k2) ** 2)
    px_new = (px - dt * 1j * v0 * KX * ph) / (1 + dt * C1 * (k2 + Dr))
    py_new = (py - dt * 1j * v0 * KY * ph) / (1 + dt * C1 * (k2 + Dr))
    s["phi"] = np.fft.ifft2(ph_new).real; s["Px"] = np.fft.ifft2(px_new).real; s["Py"] = np.fft.ifft2(py_new).real
    s["t"] += 1
    return s


def fields(s):
    d = s["phi"] - s["phi"].mean()
    amp = np.fft.ifft2(np.fft.fft2(d * d) * s["g"]).real
    return np.stack([amp, s["phi"], np.hypot(s["Px"], s["Py"])]).astype(np.float32)


def stats(s):
    return {"mean_phi": round(float(s["phi"].mean()), 4), "max_P": round(float(np.hypot(s["Px"], s["Py"]).max()), 3)}
