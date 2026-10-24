"""Single-operator mutations of m4 for screening (one operator at a time)."""
import copy
from screen import load

def base():
    return load("m4")

def kern_w(R=4.0, w=1.0, D=0.0):
    """S1 nonlocal: fast inhibitor w gets a ring-kernel drive instead of (most of) its diffusion."""
    g = base(); g["chans"][1]["kern"] = {"R": R, "w": w}; g["chans"][1]["D"] = D; return g

def kern_new(R=6.0, w=1.5, k=1.0, tau=1.0):
    """S1b nonlocal: add a ring-kernel channel (K=k) on top of m4."""
    g = base(); g["chans"].append(dict(tau=tau, D=0.0, g="id", thr=0.0, sc=1.0, kern={"R": R, "w": w}))
    g["W"].append([1.0]); g["K"][0].append(k); return g

def taxis(chi=1.0, c=0):
    """S2 chemotactic body flux of u up grad x_c (chi<0: down)."""
    g = base(); g["taxis"] = [[0, c, chi]]; return g

def ch_mem(M=1.0, k=1.0, h=0.5, Wd=2.0, tau=2.0, Km=0.0, D=0.0):
    """S3 Cahn-Hilliard membrane channel m deposited at the front (band g)."""
    g = base()
    g["chans"].append(dict(tau=tau, D=D, g="band", thr=0.0, sc=0.6, ch={"M": M, "k": k, "h": h}))
    g["W"].append([Wd]); g["K"][0].append(Km); return g

def porous(Dm=1.0, p=2.0, Du=0.2):
    """S4 degenerate diffusion: Du small + Dm z^p."""
    g = base(); g["acts"][0]["Du"] = Du; g["porous"] = [[0, Dm, p]]; return g

def adv(c=0, alpha=1.0):
    """S5 advection of all fields by -alpha grad x_c."""
    g = base(); g["adv"] = [c, alpha]; return g

def cell(beta=5.0, Km=0.0, Dc=4.0, tauc=5.0, beta_u=0.0, M=1.0, h=0.5, Wd=2.0, taum=2.0, Wc=1.0, chic=0.0):
    """Body u (m4) + CH membrane m (band deposit, chan 2) + cargo channel c (chan 3, driven by z,
    diffusing with Dc) whose diffusion is gated by m (perm beta). beta_u gates u by m too."""
    g = ch_mem(M=M, h=h, Wd=Wd, tau=taum, Km=Km)
    g["chans"].append(dict(tau=tauc, D=Dc, g="id", thr=0.0, sc=1.0))
    g["W"].append([Wc]); g["K"][0].append(0.0)
    na = 1
    g["perm"] = [[na + 3, 2, beta]] + ([[0, 2, beta_u]] if beta_u else [])
    if chic: g["taxis"] = [[0, 3, chic]]
    return g

def cellfb(kc=0.5, beta=5.0, **kw):
    """cell + cargo feeds back on the body: K[u, cargo] = -kc (cargo activates u)."""
    g = cell(beta=beta, **kw); g["K"][0][3] = -kc; return g

def cellpop(kc=0.25, Kg=1.0, Dg=100.0, taug=10.0, **kw):
    """cellfb + global depletion channel (fast-diffusing, slow, inhibits u): caps the population."""
    g = cellfb(kc=kc, **kw)
    g["chans"].append(dict(tau=taug, D=Dg, g="id", thr=0.0, sc=1.0))
    g["W"].append([1.0]); g["K"][0].append(Kg); return g

def cellwaste(kw=0.3, tw=40.0, Dw=2.0, bw=5.0, Kg=1.0, kc=0.25, **kw2):
    """cellpop + waste channel (slow, produced by the body, gated by the membrane, inhibits u).
    Trapped waste should age cells; division dilutes it."""
    g = cellpop(Kg=Kg, kc=kc, **kw2)
    g["chans"].append(dict(tau=tw, D=Dw, g="id", thr=0.0, sc=1.0))
    g["W"].append([1.0]); g["K"][0].append(kw)
    g["perm"].append([1 + 5, 3, bw])
    return g

def cellpop2(Kg=1.5, Dg=5.0, taug=100.0, **kw):
    """cellpop with a slow, local resource depletion (turnover by local starvation)."""
    return cellpop(Kg=Kg, Dg=Dg, taug=taug, **kw)
