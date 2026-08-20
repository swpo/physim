"""refs.py — REFERENCE GENOMES: exact maps of the certified worlds into the
canonical l0 genome (deviation form). Purwins -> genome: x_c = (chan - u0),
k1_genome = k1_purwins - sum_c K[c]*u0 (u0 = certified vacuum; NOTE it is the
MIDDLE root of the genome cubic — vacuum branch is explicit, see engine.py).

Certified anchors used for behavior parity:
  M0   (dx=1 heritage; here run at dx=0.5 conventions): persistent static blob.
  M4   (A=tau*Dv=4): static blob tau<=5.748; PAIR travels tau>5.636; bond d*~14.8.
  vvw  (M3 arch, M5-prep continuum pair A' d=0.65 / B d=0.75): repulsion, sizes
       A'~36px vs B~25px at dx=0.5.
  xv   (M7 rotor): tau1=5.7, tau2=2.5, eta=0.1, d0=8 -> omega=0.0111, sep=8.44.
"""
import numpy as np
from engine import cubic_roots

M0P = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=3.0, theta=0.7,
           Du=1.0, Dv=1.0, Dw=20.0)


def _vac_purwins(lam, k1p, ksum):
    """Most negative root of -u^3 + (lam-ksum) u + k1p (M0 convention)."""
    r = np.roots([-1.0, 0.0, lam - ksum, k1p])
    return float(sorted(x.real for x in r if abs(x.imag) < 1e-9)[0])


def genome_M0(tau=None, Dv=None, k1p=None, k4=None, Du=None, prov=None):
    p = dict(M0P)
    if tau is not None: p["tau"] = tau
    if Dv is not None: p["Dv"] = Dv
    if k1p is not None: p["k1"] = k1p
    if k4 is not None: p["k4"] = k4
    if Du is not None: p["Du"] = Du
    u0 = _vac_purwins(p["lam"], p["k1"], p["k3"] + p["k4"])
    k1g = p["k1"] - (p["k3"] + p["k4"]) * u0
    return {"acts": [dict(lam=p["lam"], k1=k1g, Du=p["Du"])],
            "chans": [dict(tau=p["tau"], D=p["Dv"], g={"kind": "id"}),
                      dict(tau=p["theta"], D=p["Dw"], g={"kind": "id"})],
            "W": [[1.0], [1.0]],
            "K": [[p["k3"], p["k4"]]],
            "u0": [u0],
            "provenance": prov or {"ref": "M0", "purwins": p}}


def genome_M4(tau=5.0, **kw):
    """A=4 family: Dv = 4/tau."""
    g = genome_M0(tau=tau, Dv=4.0 / tau, **kw)
    g["provenance"]["ref"] = f"M4_tau{tau}"
    return g


# iso-line vacuum solves ub^3 + 0.4*ub + 1.0 = 0 (M3 derivation); the M3
# summary rounds it to -0.86756 — we keep full precision (vacuum residual gate)
ISO_UB = float(sorted(x.real for x in np.roots([1.0, 0.0, 0.4, 1.0])
                      if abs(x.imag) < 1e-12)[0])   # -0.8675592413901124


def genome_iso(d, tau=3.0, Dv=1.0, Du=0.65, wweight=0.5, prov=None):
    """Single species on the M3 iso-line, w driven at weight wweight (0.5 =
    lone-species-in-shared-world; the certified A'=d0.65 / B=d0.75 dials)."""
    lam, k3, theta, Dw = 2.0, 1.0, 0.7, 20.0
    k1p = -1.0 + d * ISO_UB
    k4 = 1.4 + d
    u0 = ISO_UB   # by construction of the iso-line
    k1g = k1p - (k3 + k4) * u0
    return {"acts": [dict(lam=lam, k1=k1g, Du=Du)],
            "chans": [dict(tau=tau, D=Dv, g={"kind": "id"}),
                      dict(tau=theta, D=Dw, g={"kind": "id"})],
            "W": [[1.0], [wweight]],
            "K": [[k3, k4]],
            "u0": [u0],
            "provenance": prov or {"ref": f"iso_d{d}", "d": d, "wweight": wweight}}


def genome_vvw_cert():
    """The certified continuum flavor pair A'(d=0.65)+B(d=0.75), 2 acts+3 chans."""
    lam, k3, tau, theta, Dv, Dw, Du = 2.0, 1.0, 3.0, 0.7, 1.0, 20.0, 0.65
    u0 = ISO_UB
    acts, K = [], []
    for d in (0.65, 0.75):
        k1p = -1.0 + d * ISO_UB
        k4 = 1.4 + d
        acts.append(dict(lam=lam, k1=k1p - (k3 + k4) * u0, Du=Du))
        K.append([0.0, 0.0, k4])  # placeholder, fix below
    K[0] = [k3, 0.0, 1.4 + 0.65]
    K[1] = [0.0, k3, 1.4 + 0.75]
    return {"acts": acts,
            "chans": [dict(tau=tau, D=Dv, g={"kind": "id"}),
                      dict(tau=tau, D=Dv, g={"kind": "id"}),
                      dict(tau=theta, D=Dw, g={"kind": "id"})],
            "W": [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]],
            "K": K,
            "u0": [u0, u0],
            "provenance": {"ref": "vvw_cert_ApB"}}


def genome_xv_cert(tau1=5.7, tau2=2.5, eta=0.1):
    """The certified M7 rotor heterodimer world, 2 acts + 4 chans."""
    p = dict(M0P)
    u0 = _vac_purwins(p["lam"], p["k1"], p["k3"] + p["k4"])
    k1g = p["k1"] - (p["k3"] + p["k4"]) * u0
    acts = [dict(lam=p["lam"], k1=k1g, Du=p["Du"]) for _ in range(2)]
    chans = [dict(tau=tau1, D=4.0 / tau1, g={"kind": "id"}),   # v1
             dict(tau=p["theta"], D=p["Dw"], g={"kind": "id"}),  # w1
             dict(tau=tau2, D=4.0 / tau2, g={"kind": "id"}),   # v2
             dict(tau=p["theta"], D=p["Dw"], g={"kind": "id"})]  # w2
    W = [[1.0, eta], [1.0, 0.0], [eta, 1.0], [0.0, 1.0]]
    K = [[p["k3"], p["k4"], 0.0, 0.0], [0.0, 0.0, p["k3"], p["k4"]]]
    return {"acts": acts, "chans": chans, "W": W, "K": K, "u0": [u0, u0],
            "provenance": {"ref": f"xv_cert_t{tau1}_t{tau2}_e{eta}"}}
