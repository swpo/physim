"""Excitable chemotactic agents (c39; new class excitable-chemotaxis): a Dictyostelium-like relay world.

Agents i (positions x_i, periodic box L) each carry a FitzHugh-Nagumo excitable state (a_i, r_i):
    da/dt = (a - a^3/3 - r + g u(x_i)) / tau,   dr/dt = eps (a + beta - gam r)
and fire spontaneously at rate pf while at rest (a weak random pacemaker). A firing agent (a > 0) secretes
the signal u at rate ks into its own pixel; u diffuses and decays:
    du/dt = Du lap u - ku u + ks sum_i [a_i > 0] delta(x - x_i)
so excitation relays from agent to agent as waves. Agents move only while excited (a > 0, adaptation: the
refractory tail of a wave does not pull them back), up the signal gradient with saturating speed
    dx/dt = v0 grad u / (|grad u| + c0) [a > 0] + F_pair + sqrt(2 Dx) xi,
with a soft pair force F_pair: repulsion krep (1 - r/r0) below r0 and adhesion kad between r0 and r1.
Nothing marks an individual: aggregates, streams and mounds must come from relay + chemotaxis.
After the relay-chemotaxis models of Dictyostelium aggregation (Dallon & Othmer 1997; Hofer, Sherratt &
Maini 1995). Uniform random positions and resting states. Channels: agent density, signal u, excited
fraction. WORLD_P (JSON) overrides P."""
import numpy as np, json as _json, os as _os
from scipy.spatial import cKDTree
from scipy import ndimage

P = dict(N=6000, L=128.0, dt=0.1, tau=0.1, eps=0.08, beta=0.7, gam=0.8, g=1.1, pf=2e-4, ks=1.2, Du=2.0, ku=0.3,
         v0=1.0, c0=0.02, Dx=0.01, krep=2.0, r0=1.0, kad=0.0, r1=1.8, blur=1.0, Ksat=1.0)
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))
G = int(P["L"])
META = {"name": "dicty-relay", "family": "excitable-chemotaxis", "parent": None,
        "mutation": "new class: agents with FitzHugh-Nagumo relay of a diffusing signal and chemotaxis while excited",
        "size": (G, G), "steps_per_frame": 50, "dt": P["dt"],
        "channels": ["agent density", "signal u", "excited fraction"], "matter": [0], "threshold": 0.5, "smooth": 1.0, "periodic": True}


def init(seed, size):
    rng = np.random.default_rng(seed); N = int(P["N"])
    return {"x": rng.uniform(0, P["L"], (N, 2)), "a": np.full(N, -1.2) + 0.05 * rng.standard_normal(N),
            "r": np.full(N, -0.62), "u": np.zeros((G, G)), "rng": rng}


def _lap(u):
    return np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4 * u


def step(s):
    x, a, r, u, rng, dt, L = s["x"], s["a"], s["r"], s["u"], s["rng"], P["dt"], P["L"]
    N = len(a)
    iy = np.floor(x[:, 1]).astype(int) % G; ix = np.floor(x[:, 0]).astype(int) % G
    ul = u[iy, ix]; ul = ul / (1 + ul / P["Ksat"])
    # spontaneous firing of resting agents
    kick = (rng.random(N) < P["pf"] * dt) & (a < -1.0)
    a = a + kick * 1.5
    h = dt / 5
    for _ in range(5):
        a2 = a + h * (a - a ** 3 / 3 - r + P["g"] * ul) / P["tau"]
        r = r + h * P["eps"] * (a + P["beta"] - P["gam"] * r)
        a = np.clip(a2, -3, 3)
    exc = a > 0
    # signal
    src = np.bincount(iy[exc] * G + ix[exc], minlength=G * G).reshape(G, G)
    u = u + dt * (P["Du"] * _lap(u) - P["ku"] * u + P["ks"] * src)
    u = np.maximum(u, 0)
    # chemotaxis while excited
    gy = (np.roll(u, -1, 0) - np.roll(u, 1, 0)) * 0.5; gx = (np.roll(u, -1, 1) - np.roll(u, 1, 1)) * 0.5
    gxl, gyl = gx[iy, ix], gy[iy, ix]; gn = np.hypot(gxl, gyl) + P["c0"]
    v = np.zeros((N, 2)); v[exc, 0] = P["v0"] * gxl[exc] / gn[exc]; v[exc, 1] = P["v0"] * gyl[exc] / gn[exc]
    # pair forces
    pr = cKDTree(x, boxsize=L).query_pairs(max(P["r0"], P["r1"] if P["kad"] > 0 else P["r0"]), output_type="ndarray")
    if len(pr):
        i, j = pr[:, 0], pr[:, 1]
        d = x[j] - x[i]; d -= L * np.round(d / L); rr = np.sqrt((d ** 2).sum(1)) + 1e-9
        mag = np.where(rr < P["r0"], -P["krep"] * (1 - rr / P["r0"]), P["kad"])
        fv = d / rr[:, None] * mag[:, None]
        f = np.column_stack([np.bincount(i, fv[:, k], N) - np.bincount(j, fv[:, k], N) for k in (0, 1)])
        v = v + f
    x = (x + dt * v + np.sqrt(2 * P["Dx"] * dt) * rng.standard_normal((N, 2))) % L
    s.update(x=x, a=a, r=r, u=u)
    return s


def fields(s):
    rng_ = [[0, P["L"]], [0, P["L"]]]
    h, _, _ = np.histogram2d(s["x"][:, 1], s["x"][:, 0], bins=G, range=rng_)
    e, _, _ = np.histogram2d(s["x"][:, 1], s["x"][:, 0], bins=G, range=rng_, weights=(s["a"] > 0).astype(float))
    hb = ndimage.gaussian_filter(h, P["blur"], mode="wrap"); eb = ndimage.gaussian_filter(e, P["blur"], mode="wrap")
    return np.stack([hb, s["u"], eb / np.maximum(hb, 0.05)]).astype(np.float32)


def stats(s):
    return {"excited": int((s["a"] > 0).sum()), "umax": round(float(s["u"].max()), 3)}
