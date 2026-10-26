"""Swift-Hohenberg localized spots with a slow linear inhibitor (drift-bifurcation route).

u_t = r u - (q0^2 + lap)^2 u + b u^2 - u^3 - kap v
v_t = (u - v)/tau + Dv lap v
Pseudo-spectral, semi-implicit (linear part exact in Fourier space). Localized hexagonal
'spots' of SH sit in the snaking region (b>0, r<0). The slow inhibitor v (Krischer &
Mikhailov 1994; Ohta et al.) makes a resting spot unstable to drift when tau*kap is large
enough; at larger r spots self-replicate at their edges. Start: uniform noise.
WORLD_P overrides any key of P.
"""
import json, os
import numpy as np

P = dict(N=256, L=160.0, dt=0.1, r=-0.2, b=1.6, q0=1.0, kap=0.0, tau=10.0, Dv=0.0,
         noise0=1.0, PYR=0, g=0.0, Dr=1.0, ar=0.01, cr=0.05, R0=1.0, smooth_px=1.5, spf=50, INIT="noise")
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {
    "name": "sh-spots-inhibitor",
    "family": "swift-hohenberg",
    "parent": None,
    "mutation": "Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor for a drift bifurcation; new class",
    "size": (int(P["N"]), int(P["N"])),
    "steps_per_frame": int(P["spf"]),
    "dt": P["dt"],
    "channels": ["u (SH field)", "v (slow inhibitor)", "R (resource)"],
    "matter": [0],
    "threshold": 0.4,
    "smooth": 1.5,
    "periodic": True,
}


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    k = 2 * np.pi * np.fft.fftfreq(W, d=P["L"] / W)
    KX, KY = np.meshgrid(k, 2 * np.pi * np.fft.fftfreq(H, d=P["L"] / H))
    K2 = KX ** 2 + KY ** 2
    Lu = P["r"] - (P["q0"] ** 2 - K2) ** 2
    from scipy import ndimage
    n = ndimage.gaussian_filter(rng.standard_normal((H, W)), P["smooth_px"], mode="wrap")
    u = P["noise0"] * n / n.std()
    if P["INIT"] == "spot":
        yy, xx = np.mgrid[0:H, 0:W] * (P["L"] / W)
        u = 2.0 * np.exp(-((yy - P["L"] / 2) ** 2 + (xx - P["L"] / 2 - 0.3) ** 2) / 2.0)
    v = u.copy() if (P["PYR"] and not P.get("V0", 0)) else np.zeros((H, W))   # c40 review: V0=1 starts v at 0
    R = P["R0"] * np.ones((H, W))
    return {"u": u, "v": v, "R": R, "K2": K2, "Lu": Lu, "rng": rng, "t": 0.0}


def step(s):
    dt = P["dt"]
    u, v = s["u"], s["v"]
    R = s["R"]
    fb = P["kap"] * (v - u) if P["PYR"] else -P["kap"] * v   # PYR=1: low-pass Pyragas-type feedback, no static shift
    N = P["b"] * u ** 2 - u ** 3 + fb + P["g"] * R * u
    uh = (np.fft.fft2(u) + dt * np.fft.fft2(N)) / (1 - dt * s["Lu"])
    s["u"] = np.real(np.fft.ifft2(uh))
    vh = (np.fft.fft2(v) + dt * np.fft.fft2(s["u"]) / P["tau"]) / (1 + dt / P["tau"] + dt * P["Dv"] * s["K2"])
    s["v"] = np.real(np.fft.ifft2(vh))
    if P["g"]:
        Rh = (np.fft.fft2(R) + dt * np.fft.fft2(P["ar"] * (1 - R) - P["cr"] * u * u * R)) / (1 + dt * P["Dr"] * s["K2"])
        s["R"] = np.real(np.fft.ifft2(Rh))
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["u"], s["v"], s["R"]])


def damage(s, mask):
    s["u"][mask] = 0.0
    return s
