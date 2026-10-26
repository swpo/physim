"""Parametrically pumped oscillons on a consumed, regrowing pump energy (c47; new class: parametric-oscillon).

A damped wave field u (second order in time: inertia, not diffusion) is driven parametrically at 2*Om, below its
natural frequency 1 (detuned, Om < 1), with a softening cubic and a hardening quintic, so small amplitudes are off
resonance and decay while large amplitudes pull themselves into resonance (bistable: localized oscillons on a quiet
background). The pump strength is h*E, where E is a pump energy that the oscillation consumes (k u^2 E) and that
regrows (kE (1-E)) and diffuses:

    u_tt + g u_t = c2 lap u - (1 + h E cos(2 Om t)) u + a u^3 - b u^5
    E_t = DE lap E + kE (1 - E) - k u^2 E

A = sqrt(u^2 + (u_t/Om)^2) is the oscillation envelope (the rendered matter channel). Numerics: periodic, dx=1,
spectral Laplacian for u (explicit, semi-implicit damping), implicit spectral diffusion for E. Start: smoothed random
field over the whole box (correlation 2 px, std amp), u_t=0, E=1.
Parametric oscillons: Umbanhowar, Melo & Swinney (Nature 1996) in vibrated granular layers; Barashenkov et al. for the
parametrically driven damped NLS. The consumed pump is this world's addition.
"""
import json, os
import numpy as np

META = {"name": "param-oscillon", "family": "parametric-oscillon",
        "mutation": "new class: damped wave field with detuned parametric pumping drawn from a consumed, regrowing energy field",
        "size": (128, 128), "steps_per_frame": 1000, "dt": 0.02,
        "channels": ["A", "E"], "matter": [0], "threshold": 0.5}
P = dict(g=0.1, h=0.48, Om=0.9, a=1.0, b=0.3, c2=1.0, DE=1.0, kE=0.01, k=0.05, amp=0.8, rf=2.0, dt=0.02)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(seed); H, W = size
    u = gaussian_filter(rng.standard_normal((H, W)), P["rf"], mode="wrap"); u = P["amp"] * u / u.std()
    ky = np.fft.fftfreq(H) * 2 * np.pi; kx = np.fft.fftfreq(W) * 2 * np.pi
    k2 = ky[:, None] ** 2 + kx[None, :] ** 2
    return {"u": u, "v": np.zeros((H, W)), "E": np.ones((H, W)), "t": 0.0, "k2": k2,
            "LE": 1.0 / (1 + P["dt"] * P["DE"] * k2)}


def step(s):
    dt, u, v, E = P["dt"], s["u"], s["v"], s["E"]
    F = -(1 + P["h"] * E * np.cos(2 * P["Om"] * s["t"])) * u + P["a"] * u ** 3 - P["b"] * u ** 5
    lap = np.real(np.fft.ifft2(-s["k2"] * np.fft.fft2(u))) * P["c2"]
    v = (v + dt * (lap + F)) / (1 + P["g"] * dt)
    s["u"] = u + dt * v; s["v"] = v
    E = E + dt * (P["kE"] * (1 - E) - P["k"] * u * u * E)
    s["E"] = np.real(np.fft.ifft2(np.fft.fft2(E) * s["LE"]))
    s["t"] += dt
    return s


def fields(s):
    return np.stack([np.sqrt(s["u"] ** 2 + (s["v"] / P["Om"]) ** 2), s["E"]])
