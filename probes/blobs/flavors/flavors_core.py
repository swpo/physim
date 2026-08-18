"""flavors_core.py — M3 FLAVORS shared physics core.

Architectures (option (a) family: two activators, shared long-range inhibitor w):
  arch "w"   : u1,u2,w              (3 fields; no slow inhibitor)
  arch "vw"  : u1,u2,shared v,w     (4 fields; shared slow inhibitor)
  arch "vvw" : u1,v1,u2,v2,w        (5 fields; private slow inhibitors)  [M0-faithful]

Equations (arch vvw; others drop/share v):
  du_i/dt = Du_i lap(u_i) + lam*u_i - u_i^3 - k3*v_i - k4_i*w + k1_i
  dv_i/dt = (u_i - v_i)/tau + Dv lap(v_i)
  dw/dt   = ((u1+u2)/2 - w)/theta + Dw lap(w)     [w relaxes to species-average]

Symmetric embedding: if params of species 1==2 and u1==u2 everywhere, each
species obeys EXACTLY the M0 single-species model. A LONE spot of one species
drives w at half weight (other species stays at background) => the effective
lone-spot long-range self-inhibition is k4/2; sweeps re-locate the island.

Conventions inherited from day0: periodic BC, 5-pt laplacian, explicit Euler,
dt = min(0.2/Dw, 0.02), L=96, threshold thr_i = u0_i + 0.45*(sqrt(lam)-u0_i).
"""
import numpy as np
from scipy import ndimage


def lap(X):
    return (np.roll(X, 1, 0) + np.roll(X, -1, 0)
            + np.roll(X, 1, 1) + np.roll(X, -1, 1) - 4.0 * X)


# ---------------------------------------------------------------- background
def background(p, guess=None, arch="vvw"):
    """Solve homogeneous steady state (u1,u2) by Newton; v_i=u_i (or mean), w=mean."""
    lam, k3 = p["lam"], p["k3"]
    k1 = np.array([p["k1_1"], p["k1_2"]]); k4 = np.array([p["k4_1"], p["k4_2"]])
    if guess is None:
        # per-species M0-like cubic root (most negative real root), then polish
        g = []
        for i in range(2):
            k3eff = k3 if arch != "w" else 0.0
            r = np.roots([-1.0, 0.0, lam - k3eff - k4[i], k1[i]])
            rr = sorted(x.real for x in r if abs(x.imag) < 1e-9)
            g.append(rr[0])
        u = np.array(g, float)
    else:
        u = np.array(guess, float)
    for _ in range(200):
        m = 0.5 * (u[0] + u[1])
        if arch == "w":
            f = lam * u - u**3 - k4 * m + k1
            J = np.array([[lam - 3*u[0]**2 - 0.5*k4[0], -0.5*k4[0]],
                          [-0.5*k4[1], lam - 3*u[1]**2 - 0.5*k4[1]]])
        elif arch == "vw":
            f = lam * u - u**3 - k3 * m - k4 * m + k1
            J = np.array([[lam - 3*u[0]**2 - 0.5*(k3+k4[0]), -0.5*(k3+k4[0])],
                          [-0.5*(k3+k4[1]), lam - 3*u[1]**2 - 0.5*(k3+k4[1])]])
        else:  # vvw
            f = lam * u - u**3 - k3 * u - k4 * m + k1
            J = np.array([[lam - 3*u[0]**2 - k3 - 0.5*k4[0], -0.5*k4[0]],
                          [-0.5*k4[1], lam - 3*u[1]**2 - k3 - 0.5*k4[1]]])
        try:
            du = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return None
        u = u + du
        if np.max(np.abs(du)) < 1e-12:
            break
    m = 0.5 * (u[0] + u[1])
    if not np.all(np.isfinite(u)) or np.max(np.abs(f)) > 1e-8:
        return None
    return dict(u1=u[0], u2=u[1], v1=u[0], v2=u[1], w=m,
                vshared=m)


def bg_stability(p, bg, arch="vvw", kmax=3.0, nk=121):
    """Max Re(eig) of linearization over wavenumbers k; returns (max_growth, k_at_max, growth_at_k0)."""
    lam, k3, tau, theta = p["lam"], p["k3"], p["tau"], p["theta"]
    k4 = [p["k4_1"], p["k4_2"]]
    Du = [p["Du_1"], p["Du_2"]]; Dv, Dw = p["Dv"], p["Dw"]
    fu = [lam - 3 * bg["u1"]**2, lam - 3 * bg["u2"]**2]
    ks = np.linspace(0, kmax, nk)
    worst = -np.inf; kworst = 0.0; g0 = None
    for k in ks:
        q = k * k
        if arch == "vvw":
            A = np.zeros((5, 5))
            # order u1,u2,v1,v2,w
            A[0, 0] = fu[0] - Du[0]*q; A[0, 2] = -k3; A[0, 4] = -k4[0]
            A[1, 1] = fu[1] - Du[1]*q; A[1, 3] = -k3; A[1, 4] = -k4[1]
            A[2, 0] = 1/tau; A[2, 2] = -1/tau - Dv*q
            A[3, 1] = 1/tau; A[3, 3] = -1/tau - Dv*q
            A[4, 0] = 0.5/theta; A[4, 1] = 0.5/theta; A[4, 4] = -1/theta - Dw*q
        elif arch == "vw":
            A = np.zeros((4, 4))
            # order u1,u2,v,w ; v relaxes to mean
            A[0, 0] = fu[0] - Du[0]*q; A[0, 2] = -k3; A[0, 3] = -k4[0]
            A[1, 1] = fu[1] - Du[1]*q; A[1, 2] = -k3; A[1, 3] = -k4[1]
            A[2, 0] = 0.5/tau; A[2, 1] = 0.5/tau; A[2, 2] = -1/tau - Dv*q
            A[3, 0] = 0.5/theta; A[3, 1] = 0.5/theta; A[3, 3] = -1/theta - Dw*q
        else:  # "w"
            A = np.zeros((3, 3))
            A[0, 0] = fu[0] - Du[0]*q; A[0, 2] = -k4[0]
            A[1, 1] = fu[1] - Du[1]*q; A[1, 2] = -k4[1]
            A[2, 0] = 0.5/theta; A[2, 1] = 0.5/theta; A[2, 2] = -1/theta - Dw*q
        g = np.max(np.linalg.eigvals(A).real)
        if k == 0:
            g0 = g
        if g > worst:
            worst = g; kworst = k
    return worst, kworst, g0


# ---------------------------------------------------------------- simulation
def default_params():
    return dict(lam=2.0, k3=1.0, tau=3.0, theta=0.7,
                Du_1=1.0, Du_2=1.0, Dv=1.0, Dw=20.0,
                k1_1=-0.7, k1_2=-0.7, k4_1=1.5, k4_2=1.5)


def make_state(p, L=96, arch="vvw", spots=(), bg=None):
    """spots: list of (species(1|2), y, x, amp, sigma). Returns stacked field array F."""
    if bg is None:
        bg = background(p, arch=arch)
    if bg is None:
        return None, None
    x = np.arange(L); X, Y = np.meshgrid(x, x, indexing="ij")
    if arch == "vvw":
        F = np.empty((5, L, L))
        F[0] = bg["u1"]; F[1] = bg["u2"]; F[2] = bg["v1"]; F[3] = bg["v2"]; F[4] = bg["w"]
    elif arch == "vw":
        F = np.empty((4, L, L))
        F[0] = bg["u1"]; F[1] = bg["u2"]; F[2] = bg["vshared"]; F[3] = bg["w"]
    else:
        F = np.empty((3, L, L))
        F[0] = bg["u1"]; F[1] = bg["u2"]; F[2] = bg["w"]
    for (sp, y, x0, amp, sig) in spots:
        dx = (X - y + L/2) % L - L/2
        dy = (Y - x0 + L/2) % L - L/2
        F[sp - 1] += amp * np.exp(-(dx**2 + dy**2) / (2 * sig**2))
    return F, bg


def stepper(p, arch="vvw"):
    """Returns (step(F, dt, rng, noise) -> F) closure. Noise added to activators only."""
    lam, k3, tau, theta = p["lam"], p["k3"], p["tau"], p["theta"]
    k11, k12 = p["k1_1"], p["k1_2"]; k41, k42 = p["k4_1"], p["k4_2"]
    Du1, Du2, Dv, Dw = p["Du_1"], p["Du_2"], p["Dv"], p["Dw"]
    if arch == "vvw":
        D = np.array([Du1, Du2, Dv, Dv, Dw]).reshape(5, 1, 1)
        def step(F, dt, rng=None, noise=0.0):
            Lp = (np.roll(F, 1, 1) + np.roll(F, -1, 1)
                  + np.roll(F, 1, 2) + np.roll(F, -1, 2) - 4.0 * F)
            u1, u2, v1, v2, w = F
            R = np.empty_like(F)
            R[0] = lam*u1 - u1**3 - k3*v1 - k41*w + k11
            R[1] = lam*u2 - u2**3 - k3*v2 - k42*w + k12
            R[2] = (u1 - v1)/tau
            R[3] = (u2 - v2)/tau
            R[4] = (0.5*(u1 + u2) - w)/theta
            F = F + dt*(D*Lp + R)
            if noise > 0.0:
                F[:2] += noise*np.sqrt(dt)*rng.standard_normal(F[:2].shape)
            return F
    elif arch == "vw":
        D = np.array([Du1, Du2, Dv, Dw]).reshape(4, 1, 1)
        def step(F, dt, rng=None, noise=0.0):
            Lp = (np.roll(F, 1, 1) + np.roll(F, -1, 1)
                  + np.roll(F, 1, 2) + np.roll(F, -1, 2) - 4.0 * F)
            u1, u2, v, w = F
            R = np.empty_like(F)
            R[0] = lam*u1 - u1**3 - k3*v - k41*w + k11
            R[1] = lam*u2 - u2**3 - k3*v - k42*w + k12
            R[2] = (0.5*(u1 + u2) - v)/tau
            R[3] = (0.5*(u1 + u2) - w)/theta
            F = F + dt*(D*Lp + R)
            if noise > 0.0:
                F[:2] += noise*np.sqrt(dt)*rng.standard_normal(F[:2].shape)
            return F
    else:  # "w"
        D = np.array([Du1, Du2, Dw]).reshape(3, 1, 1)
        def step(F, dt, rng=None, noise=0.0):
            Lp = (np.roll(F, 1, 1) + np.roll(F, -1, 1)
                  + np.roll(F, 1, 2) + np.roll(F, -1, 2) - 4.0 * F)
            u1, u2, w = F
            R = np.empty_like(F)
            R[0] = lam*u1 - u1**3 - k41*w + k11
            R[1] = lam*u2 - u2**3 - k42*w + k12
            R[2] = (0.5*(u1 + u2) - w)/theta
            F = F + dt*(D*Lp + R)
            if noise > 0.0:
                F[:2] += noise*np.sqrt(dt)*rng.standard_normal(F[:2].shape)
            return F
    return step


def thresholds(p, bg):
    lam = p["lam"]
    return (bg["u1"] + 0.45*(np.sqrt(lam) - bg["u1"]),
            bg["u2"] + 0.45*(np.sqrt(lam) - bg["u2"]))


def measure(F, thr):
    """Per-species: ncomp, area, centroid, peak amplitude above background threshold."""
    out = []
    for i in range(2):
        m = F[i] > thr[i]
        a = int(m.sum())
        if a == 0:
            out.append(dict(ncomp=0, area=0, cy=None, cx=None, umax=float(F[i].max())))
            continue
        lab, nc = ndimage.label(m)
        cy, cx = ndimage.center_of_mass(m)
        out.append(dict(ncomp=int(nc), area=a, cy=float(cy), cx=float(cx),
                        umax=float(F[i].max())))
    return out


def run(p, arch="vvw", L=96, T=400.0, spots=((1, 48, 48, 2.0, 3.0),),
        noise=0.0, seed=0, rec_every_tu=10.0, snap_at=(), dt=None):
    """Generic run. Returns dict with per-species series + final measures (+snaps)."""
    if dt is None:
        dt = min(0.2 / max(p["Du_1"], p["Du_2"], p["Dv"], p["Dw"]), 0.02)
    F, bg = make_state(p, L=L, arch=arch, spots=spots)
    if F is None:
        return dict(status="no_bg")
    thr = thresholds(p, bg)
    step = stepper(p, arch=arch)
    rng = np.random.default_rng(seed)
    steps = int(round(T / dt))
    rec = max(int(round(rec_every_tu / dt)), 1)
    ser = {"t": [], "a1": [], "a2": [], "n1": [], "n2": [],
           "c1": [], "c2": [], "m1": [], "m2": []}
    snaps = {}
    snap_steps = {int(round(s / dt)): s for s in snap_at}
    for t in range(steps + 1):
        if t in snap_steps:
            snaps[snap_steps[t]] = F.copy()
        if t % rec == 0:
            if not np.isfinite(F).all():
                return dict(status="blowup", t_tu=t * dt, bg=bg)
            mm = measure(F, thr)
            ser["t"].append(round(t * dt, 2))
            for i, s in enumerate(mm, 1):
                ser[f"a{i}"].append(s["area"]); ser[f"n{i}"].append(s["ncomp"])
                ser[f"c{i}"].append((s["cy"], s["cx"])); ser[f"m{i}"].append(round(s["umax"], 4))
        if t < steps:
            F = step(F, dt, rng, noise)
    return dict(status="ok", bg=bg, thr=thr, series=ser, F=F, snaps=snaps, dt=dt)


def persistence_verdict(ser, key="a1", nkey="n1", tail_frac=0.25):
    """Day0-style: single component, bounded stable area over the tail."""
    a = np.array(ser[key]); n = np.array(ser[nkey])
    k = max(int(len(a) * (1 - tail_frac)), 0)
    tail = a[k:]; ntail = n[k:]
    if tail.min() < 8:
        return "dead_or_tiny"
    if ntail.max() > 1:
        return "split"
    if tail.max() > 600:
        return "domain"
    if (tail.max() - tail.min()) > max(6, 0.3 * tail.mean()):
        return "unsteady"
    return "persistent"
