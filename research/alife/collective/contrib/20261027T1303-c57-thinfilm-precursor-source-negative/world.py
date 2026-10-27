"""c57 loop 2: optional Zwicker-style source ks V exp(-((h-ha)/wprec)^2): liquid made only in the thin precursor
film (the dilute phase), reaching drops by lubrication flow, decayed inside drops at kd. Qev 0 switches off the
chemical-potential exchange.
c57: FED active thin-film drops. c24's active polar thin film plus a non-conserved mass exchange with a vapour V:
  dh/dt = -div jC + Jev - kd (h - ha) [h > ha],   Jev = Qev (mu_v - dF/dh),  mu_v = cv (V - Vs)
  dV/dt = DV lap V + kV (1 - V) - Jev
Condensation follows the film's own chemical potential (thermodynamically consistent exchange, as in Thiele's
evaporating films); the drive is the decay kd of liquid inside drops (a chemical reaction turning liquid into an
inert, removed product) against a regrowing vapour, as in Zwicker et al.'s active emulsions (Nat Phys 2017).
Original c24 docstring follows.

Active polar thin-film drops (c24; new class thin-film), after Trinschek, Stegemerten, John & Thiele
(PRE 101, 062802, 2020) and Stegemerten, John & Thiele (Soft Matter 18, 5823, 2022).

Fields on a 2D periodic substrate: film height h and height-integrated polarization P = h p (2 components).
Free energy  F = int [ gam/2 |grad h|^2 + fw(h) + h fspo(h, p^2) + h cp/2 |grad p|^2 + chpa/2 p . grad h ]
  fw   = A/(2 h^2) (2 ha^3/(5 h^3) - 1)                 (partial wetting, precursor film ha)
  fspo = -csp/2 (1 - 2 kappa(h)) p^2 + csp/4 p^4,  kappa = (ha/h)^6   (polar order inside drops only)
Dynamics (gradient dynamics plus active fluxes, eqs 11-16 of the 2022 paper), eta = 1:
  dh/dt = -div(jC),   dP/dt = -div(p jC + jD) - Qnc dF/dP
  jC = -(h^3/3) [grad dF/dh + (P_b/h) grad dF/dP_b] + (h^3/3) [div sigma_a + mu0 P],  sigma_a = -ca p p
  jD_a = -h M grad dF/dP_a
Stiff parts (gam h^3/3 k^4 on h; M h cp k^4 + Qnc cp k^2 on P) are treated semi-implicitly with the domain maxima.
Twin (twin=1): the passive flux -(h^3/3) grad dF/dh is replaced by -Dtw grad h; active and polar fluxes are kept.
Initial condition: flat film h0 + noise, P = small noise, both unstructured over the whole domain.
WORLD_P (JSON) overrides P.
"""
import json, os
import numpy as np

META = {"name": "fed-thinfilm", "family": "thin-film", "parent": "collective/contrib/20261025T1915-c24-thinfilm-sighting",
        "mutation": "non-conserved film: condensation from a consumed, regrowing vapour along the film's own chemical potential, and decay of liquid inside drops",
        "size": (128, 128), "steps_per_frame": 200, "dt": 0.25,
        "channels": ["height above precursor h - ha", "|p| polar order", "p_x", "p_y", "vapour V"], "matter": [0],
        "threshold": 0.5, "smooth": 0.5, "periodic": True}
P = dict(dx=1.0, dt=0.25, gam=1.0, A=1.0, ha=1.0, csp=0.05, cp=0.5, chpa=0.2, ca=0.0, mu0=0.004,
         M=1.0, Qnc=1.0, twin=0, Dtw=1.0, h0=2.0, hnoise=0.05, pnoise=0.1, hcap=12.0,
         Qev=0.1, cv=1.5, Vs=0.8, DV=1.0, kV=0.02, kd=0.004, V0=1.0, ks=0.0, wprec=0.3)  # loop-1 defaults; pack_m2 used WORLD_P {"h0":2.0,"Qev":0,"kV":0.02,"DV":1.0,"ks":0.005,"kd":0.001,"chpa":0.2,"ca":0.3,"mu0":0.004}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


try:
    import scipy.fft as _fft
    _W = {"workers": int(os.environ.get("OMP_NUM_THREADS", "1"))}
except ImportError:  # pragma: no cover
    _fft = np.fft; _W = {}


def F(f):
    return _fft.rfft2(f, **_W)


def iF(fh, shape):
    return _fft.irfft2(fh, s=shape, **_W)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    h = P["h0"] + P["hnoise"] * rng.standard_normal((H, W))
    Px = P["pnoise"] * rng.standard_normal((H, W)); Py = P["pnoise"] * rng.standard_normal((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=P["dx"])[:, None]; kx = 2 * np.pi * np.fft.rfftfreq(W, d=P["dx"])[None, :]
    return {"V": P["V0"] + 0 * h, "h": h, "Px": Px, "Py": Py, "ikx": 1j * kx, "iky": 1j * ky, "k2": kx ** 2 + ky ** 2, "t": 0.0}


def step(s):
    p_ = P; dt = p_["dt"]; sh = s["h"].shape; ikx, iky, k2 = s["ikx"], s["iky"], s["k2"]
    h = np.maximum(s["h"], 0.5 * p_["ha"]); Px, Py = s["Px"], s["Py"]
    ha, A, csp, cp, chpa, ca = p_["ha"], p_["A"], p_["csp"], p_["cp"], p_["chpa"], p_["ca"]
    kap = (ha / h) ** 6
    P2 = Px ** 2 + Py ** 2
    px, py = Px / h, Py / h
    Hh, PXh, PYh = F(h), F(Px), F(Py)
    hx, hy, laph = iF(ikx * Hh, sh), iF(iky * Hh, sh), iF(-k2 * Hh, sh)
    dFdh = (-p_["gam"] * laph + A / h ** 3 - A * ha ** 3 / h ** 6
            - 0.5 * csp * P2 * (-1 + 14 * kap) / h ** 2 - 0.75 * csp * P2 ** 2 / h ** 4)
    if chpa:
        dFdh = dFdh - 0.5 * chpa * (Px * hx + Py * hy) / h ** 2 - 0.5 * chpa * iF(ikx * F(px) + iky * F(py), sh)
    # elastic energy h cp/2 |grad p|^2 with p = P/h (as in the papers): E_a = div(h grad p_a)
    G = F(px); pxx, pxy = iF(ikx * G, sh), iF(iky * G, sh)
    G = F(py); pyx, pyy = iF(ikx * G, sh), iF(iky * G, sh)
    Ex = iF(ikx * F(h * pxx) + iky * F(h * pxy), sh); Ey = iF(ikx * F(h * pyx) + iky * F(h * pyy), sh)
    dFdh = dFdh + 0.5 * cp * (pxx ** 2 + pxy ** 2 + pyx ** 2 + pyy ** 2) + cp * (px * Ex + py * Ey) / h
    dFdPx = -csp * (1 - 2 * kap) * Px / h + csp * P2 * Px / h ** 3 - cp * Ex / h + 0.5 * chpa * hx / h
    dFdPy = -csp * (1 - 2 * kap) * Py / h + csp * P2 * Py / h ** 3 - cp * Ey / h + 0.5 * chpa * hy / h
    Q = h ** 3 / 3.0
    if ca:  # (div sigma)_b = d_a sigma_ab, sigma_ab = -ca p_a p_b
        XX, XY, YY = F(px * px), F(px * py), F(py * py)
        dsx = -ca * iF(ikx * XX + iky * XY, sh); dsy = -ca * iF(ikx * XY + iky * YY, sh)
    else:
        dsx = dsy = 0.0
    G = F(dFdh); gFh_x, gFh_y = iF(ikx * G, sh), iF(iky * G, sh)
    G = F(dFdPx); gPx_x, gPx_y = iF(ikx * G, sh), iF(iky * G, sh)
    G = F(dFdPy); gPy_x, gPy_y = iF(ikx * G, sh), iF(iky * G, sh)
    if p_["twin"]:  # Laplacian twin: the passive lubrication flux of h is replaced by linear diffusion Dtw grad h
        jx = -p_["Dtw"] * hx + Q * (dsx + p_["mu0"] * Px - px * gPx_x - py * gPy_x)
        jy = -p_["Dtw"] * hy + Q * (dsy + p_["mu0"] * Py - px * gPx_y - py * gPy_y)
    else:
        jx = Q * (-(gFh_x + px * gPx_x + py * gPy_x) + dsx + p_["mu0"] * Px)
        jy = Q * (-(gFh_y + px * gPx_y + py * gPy_y) + dsy + p_["mu0"] * Py)
    hM = h * p_["M"]
    Rh = -(ikx * F(jx) + iky * F(jy))
    RPx = -(ikx * F(px * jx - hM * gPx_x) + iky * F(px * jy - hM * gPx_y)) - p_["Qnc"] * F(dFdPx)
    RPy = -(ikx * F(py * jx - hM * gPy_x) + iky * F(py * jy - hM * gPy_y)) - p_["Qnc"] * F(dFdPy)
    k4 = k2 * k2
    Sh = p_["gam"] * min(Q.max(), p_["hcap"] ** 3 / 3) * k4
    hc = min(h.max(), p_["hcap"]); pm = min(float(np.max(px * px + py * py)), 4.0)
    SP = (p_["M"] * hc + hc ** 3 / 3 * pm) * cp * k4 + p_["Qnc"] * cp * k2  # P diffusion and advective elastic stiffness
    V = s["V"]
    Jev = p_["Qev"] * (p_["cv"] * (V - p_["Vs"]) - dFdh)
    if p_["ks"]:  # Zwicker-style production in the dilute (precursor) film only, from vapour V
        Jev = Jev + p_["ks"] * V * np.exp(-((h - ha) / p_["wprec"]) ** 2)
    Rh = Rh + F(Jev - p_["kd"] * np.maximum(h - ha, 0.0))
    Sh = Sh + p_["Qev"] * p_["gam"] * k2
    s["V"] = iF((F(V) + dt * F(p_["kV"] * (1 - V) - Jev)) / (1 + dt * p_["DV"] * k2), sh)
    s["h"] = iF(Hh + dt * Rh / (1 + dt * Sh), sh)
    s["Px"] = iF(PXh + dt * RPx / (1 + dt * SP), sh)
    s["Py"] = iF(PYh + dt * RPy / (1 + dt * SP), sh)
    s["t"] += dt
    return s


def fields(s):
    h = s["h"]; px, py = s["Px"] / h, s["Py"] / h
    return np.stack([h - P["ha"], np.hypot(px, py), px, py, s["V"]]).astype(np.float32)


def damage(s, mask):
    s["h"][mask] = P["ha"]; s["Px"][mask] = 0.0; s["Py"][mask] = 0.0
    return s


def stats(s):
    return {"hmax": round(float(s["h"].max()), 3), "mass": round(float(s["h"].mean()), 5),
            "pmax": round(float(np.hypot(s["Px"], s["Py"]).max()), 4), "Vmean": round(float(s["V"].mean()), 4)}
