"""Self-propelled swarmalators with local coupling (c21; new class swarmalator).

After O'Keeffe, Ha & Strogatz (2017) swarmalators: particles that both swarm and synchronize, here
with finite-range coupling and the phase doubling as the heading (a Kuramoto-Vicsek hybrid).
Particle i: position x_i, phase theta_i (heading e(theta_i)), natural frequency omega_i ~ N(0, sw).
  dx_i/dt  = v0 e(theta_i) + (1/n_i) sum_{|r_ij|<R} rhat_ij [ a (1 + J cos(theta_j - theta_i)) - b exp(-r_ij/l) ]
  dth_i/dt = omega_i + (K/n_i) sum_{|r_ij|<R} sin(theta_j - theta_i) + sqrt(2 Dth) xi_i
Like phases attract more (J), short-range repulsion b, phase sync K within R. Attraction and sync are
averaged over the n_i neighbours; with repsum=1 the repulsion is summed instead, so flocks keep a finite density. Periodic box, uniform
random positions and phases. Channels: particle density, and density-weighted cos/sin of the phase.
WORLD_P (JSON) overrides P."""
import numpy as np, json as _json, os as _os
from scipy.spatial import cKDTree

P = dict(N=1200, L=60.0, R=3.0, v0=0.5, a=0.3, J=1.0, b=3.0, l=0.5, K=1.0, sw=0.6, Dth=0.02, dt=0.05, grid=128, blur=1.0, repsum=0)
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))
META = {"name": "swarmalator", "family": "swarmalator", "parent": "new class (O'Keeffe-Ha-Strogatz swarmalators, local coupling, phase = heading)",
        "mutation": "none", "size": (int(P["grid"]), int(P["grid"])), "steps_per_frame": 40, "dt": P["dt"],
        "channels": ["particle density", "density x cos(phase)", "density x sin(phase)"], "matter": [0], "smooth": 1.0,
        "periodic": True, "domain": (P["L"], P["L"])}


def init(seed, size):
    rng = np.random.default_rng(seed); N = int(P["N"])
    return {"x": rng.uniform(0, P["L"], (N, 2)), "th": rng.uniform(0, 2 * np.pi, N), "w": P["sw"] * rng.standard_normal(N), "rng": rng}


def step(s):
    x, th, L = s["x"], s["th"], P["L"]; N = len(th)
    pr = cKDTree(x, boxsize=L).query_pairs(P["R"], output_type="ndarray")
    i, j = pr[:, 0], pr[:, 1]
    d = x[j] - x[i]; d -= L * np.round(d / L); r = np.sqrt((d ** 2).sum(1)) + 1e-9
    dth = th[j] - th[i]
    n = np.maximum(np.bincount(i, minlength=N) + np.bincount(j, minlength=N), 1)
    att = d / r[:, None] * (P["a"] * (1 + P["J"] * np.cos(dth)))[:, None]
    rep = d / r[:, None] * (P["b"] * np.exp(-r / P["l"]))[:, None]
    fa = np.column_stack([np.bincount(i, att[:, k], N) - np.bincount(j, att[:, k], N) for k in (0, 1)]) / n[:, None]
    fr = np.column_stack([np.bincount(i, rep[:, k], N) - np.bincount(j, rep[:, k], N) for k in (0, 1)])
    f = fa - (fr if P["repsum"] else fr / n[:, None])  # repsum=1: repulsion summed over neighbours (finite packing density)
    sn = np.sin(dth); ph = (np.bincount(i, sn, N) - np.bincount(j, sn, N)) / n
    e = np.column_stack([np.cos(th), np.sin(th)])
    s["x"] = (x + P["dt"] * (P["v0"] * e + f)) % L
    s["th"] = th + P["dt"] * (s["w"] + P["K"] * ph) + np.sqrt(2 * P["Dth"] * P["dt"]) * s["rng"].standard_normal(N)
    return s


def fields(s):
    from scipy import ndimage
    g = int(P["grid"]); rng_ = [[0, P["L"]], [0, P["L"]]]
    out = []
    for wgt in (None, np.cos(s["th"]), np.sin(s["th"])):
        h, _, _ = np.histogram2d(s["x"][:, 1], s["x"][:, 0], bins=g, range=rng_, weights=wgt)
        out.append(ndimage.gaussian_filter(h, P["blur"], mode="wrap"))
    return np.stack(out).astype(np.float32)


def particles(s):
    return np.column_stack([s["x"], np.floor(np.mod(s["th"], 2 * np.pi) / (2 * np.pi) * 6)])
