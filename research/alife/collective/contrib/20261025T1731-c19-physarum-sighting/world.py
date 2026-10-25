"""Physarum transport agents (Jones 2010, "Characteristics of pattern formation and evolution in
approximations of Physarum transport networks", Artificial Life 16:127), c19.

N agents on a periodic 2D plane, each with a position and a heading. Every step each agent samples the
trail field T at three sensors a distance SO ahead (left, centre, right at +-SA); it keeps its heading
if the centre is strongest, turns by RA towards the stronger side otherwise (random turn if both sides
beat the centre), moves SS forward, and deposits dep onto T. T diffuses (3x3 mean, weight dw) and decays
(factor 1 - kd). Agents start uniformly at random with random headings: nothing is planted.
The only coupling between agents is through the trail they lay.
WORLD_P (JSON) overrides P.
"""
import json, os
import numpy as np

META = {
    "name": "physarum",
    "family": "physarum-agents",
    "parent": None,
    "mutation": "new class: Jones-type chemotactic agents that sense, follow and lay a diffusing trail",
    "size": (128, 128),
    "steps_per_frame": 10,
    "dt": 1.0,
    "channels": ["agent density", "trail"],
    "matter": [0],
    "smooth": 1.5,
    "periodic": True,
}
P = dict(frac=0.15, SO=9.0, SA=45.0, RA=45.0, SS=1.0, dep=5.0, kd=0.1, dw=1.0, jitter=0.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    n = int(P["frac"] * H * W)
    return {"x": rng.uniform(0, W, n), "y": rng.uniform(0, H, n), "a": rng.uniform(0, 2 * np.pi, n),
            "T": np.zeros((H, W)), "rng": rng, "H": H, "W": W}


def _sample(T, x, y, H, W):
    return T[np.floor(y).astype(int) % H, np.floor(x).astype(int) % W]


def step(s):
    T, x, y, a, rng, H, W = s["T"], s["x"], s["y"], s["a"], s["rng"], s["H"], s["W"]
    SA, RA, SO = np.deg2rad(P["SA"]), np.deg2rad(P["RA"]), P["SO"]
    F = _sample(T, x + SO * np.cos(a), y + SO * np.sin(a), H, W)
    L = _sample(T, x + SO * np.cos(a + SA), y + SO * np.sin(a + SA), H, W)
    R = _sample(T, x + SO * np.cos(a - SA), y + SO * np.sin(a - SA), H, W)
    both = (L > F) & (R > F)
    turn = np.where(both, np.where(rng.random(a.size) < 0.5, RA, -RA),
                    np.where((L > F) & (L > R), RA, np.where((R > F) & (R > L), -RA, 0.0)))
    a = a + turn + P["jitter"] * rng.standard_normal(a.size)
    x = (x + P["SS"] * np.cos(a)) % W
    y = (y + P["SS"] * np.sin(a)) % H
    iy, ix = np.floor(y).astype(int) % H, np.floor(x).astype(int) % W
    np.add.at(T, (iy, ix), P["dep"])
    Tm = sum(np.roll(np.roll(T, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1)) / 9.0
    T = (1 - P["dw"]) * T + P["dw"] * Tm
    s["T"] = T * (1 - P["kd"]); s["x"], s["y"], s["a"] = x, y, a
    return s


def fields(s):
    H, W = s["H"], s["W"]
    rho = np.bincount((np.floor(s["y"]).astype(int) % H) * W + (np.floor(s["x"]).astype(int) % W), minlength=H * W).reshape(H, W)
    return np.stack([rho, s["T"]]).astype(np.float32)


def stats(s):
    return {"trail_max": round(float(s["T"].max()), 2)}
