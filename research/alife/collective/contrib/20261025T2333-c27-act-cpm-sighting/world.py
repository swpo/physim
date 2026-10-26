"""Act-CPM (c27; new class cellular-potts): Cellular Potts model with the actin-inspired activity term of
Niculescu, Textor & de Boer (PLoS Comput Biol 2015).

Lattice sigma (0 = medium, 1..N = cells). Metropolis copy attempts (one MCS = H*W attempts, T = temperature):
    H = sum_<x,x'> J(sigma, sigma') [sigma != sigma'] + lam_A sum_c (A_c - A0)^2 + lam_P sum_c (P_c - P0)^2
    Delta H_act(u -> v) = -(lam_act / max_act) (GM(u) - GM(v)),
GM = geometric mean of the activity over the Moore neighbourhood pixels that belong to the same cell (0 if any is 0).
A successful copy into v sets act(v) = max_act; every MCS all activities fall by 1. Protrusions into recently
active pixels are favoured, which makes cells polarise and crawl (Niculescu et al. 2015).
Initial condition: N cells planted as 3x3 seeds at random positions (a random scatter of labels does not
condense: each label stays split into 3-7 fragments, since nothing pulls fragments together), activities random.
WORLD_P (JSON) overrides P.
"""
import json, os
import numpy as np
from numba import njit

P = dict(N=40, fill=0.35, T=20.0, Jcm=20.0, Jcc=40.0, lamA=50.0, A0=140.0, lamP=2.0, P0=140.0,
         lam_act=600.0, max_act=30, mcs_per_step=1)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {
    "name": "act-cpm",
    "family": "cellular-potts",
    "parent": None,
    "mutation": "new class: Cellular Potts model with the Act (actin activity memory) term of Niculescu et al. 2015, cells planted as 3x3 seeds",
    "size": (128, 128),
    "steps_per_frame": 10,
    "dt": 1.0,
    "channels": ["cell (sigma > 0)", "activity act/max", "cell boundary"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 0.0,
    "periodic": True,
}

DY = np.array([-1, -1, -1, 0, 0, 1, 1, 1], np.int64)
DX = np.array([-1, 0, 1, -1, 1, -1, 0, 1], np.int64)


@njit
def _gm(sig, act, y, x, c, H, W, maxact):
    if c == 0:
        return 0.0
    s = 0.0; n = 0
    for k in range(-1, 9):
        if k == -1:
            yy, xx = y, x
        else:
            yy = (y + DY[k]) % H; xx = (x + DX[k]) % W
        if sig[yy, xx] == c:
            a = act[yy, xx]
            if a <= 0:
                return 0.0
            s += np.log(a); n += 1
    return np.exp(s / n) if n > 0 else 0.0


@njit
def _mcs(sig, act, area, perim, seed_arr, T, Jcm, Jcc, lamA, A0, lamP, P0, lam_act, maxact):
    H, W = sig.shape
    np.random.seed(seed_arr[0]); seed_arr[0] = (seed_arr[0] * 1103515245 + 12345) % 2147483647
    for it in range(H * W):
        y = np.random.randint(H); x = np.random.randint(W)
        k = np.random.randint(8)
        ys = (y + DY[k]) % H; xs = (x + DX[k]) % W
        t = sig[y, x]; s = sig[ys, xs]
        if s == t:
            continue
        if t > 0 and area[t] <= 1:
            continue  # no cell deletion
        dH = 0.0
        dPs = 0; dPt = 0
        for q in range(8):
            yn = (y + DY[q]) % H; xn = (x + DX[q]) % W
            n = sig[yn, xn]
            # adhesion: bonds of pixel (y,x) before (label t) and after (label s)
            if n != t:
                dH -= (Jcc if (n > 0 and t > 0) else Jcm) if (n > 0 or t > 0) else 0.0
            if n != s:
                dH += (Jcc if (n > 0 and s > 0) else Jcm) if (n > 0 or s > 0) else 0.0
            # perimeter (number of unlike Moore neighbours) changes for s and t
            if n == t: dPt += 1   # t loses x: neighbours of t that were interior bonds become boundary
            else: dPt -= 1
            if n == s: dPs -= 1
            else: dPs += 1
        if s > 0:
            dH += lamA * ((area[s] + 1 - A0) ** 2 - (area[s] - A0) ** 2)
            dH += lamP * ((perim[s] + dPs - P0) ** 2 - (perim[s] - P0) ** 2)
        if t > 0:
            dH += lamA * ((area[t] - 1 - A0) ** 2 - (area[t] - A0) ** 2)
            dH += lamP * ((perim[t] + dPt - P0) ** 2 - (perim[t] - P0) ** 2)
        if lam_act > 0:
            gu = _gm(sig, act, ys, xs, s, H, W, maxact)
            gv = _gm(sig, act, y, x, t, H, W, maxact)
            dH -= lam_act / maxact * (gu - gv)
        if dH <= 0 or np.random.random() < np.exp(-dH / T):
            sig[y, x] = s
            if s > 0:
                area[s] += 1; perim[s] += dPs
                act[y, x] = maxact
            else:
                act[y, x] = 0
            if t > 0:
                area[t] -= 1; perim[t] += dPt
    for i in range(H):
        for j in range(W):
            if act[i, j] > 0:
                act[i, j] -= 1


def _perims(sig, N):
    per = np.zeros(N + 1, np.int64)
    for dy, dx in zip(DY, DX):
        diff = sig != np.roll(np.roll(sig, -dy, 0), -dx, 1)
        np.add.at(per, sig[diff], 1)
    per[0] = 0
    return per


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    N = int(P["N"])
    sig = np.zeros((H, W), np.int64)
    for c in range(1, N + 1):
        y, x = rng.integers(H), rng.integers(W)
        sig[np.ix_([(y + d) % H for d in (-1, 0, 1)], [(x + d) % W for d in (-1, 0, 1)])] = c
    act = np.where(sig > 0, rng.integers(0, int(P["max_act"]) + 1, (H, W)), 0).astype(np.int64)
    area = np.bincount(sig.ravel(), minlength=N + 1).astype(np.int64); area[0] = 0
    return {"sig": sig, "act": act, "area": area, "perim": _perims(sig, N), "seed": np.array([int(seed) * 7919 + 17], np.int64), "t": 0}


def step(s):
    for _ in range(int(P["mcs_per_step"])):
        _mcs(s["sig"], s["act"], s["area"], s["perim"], s["seed"], float(P["T"]), float(P["Jcm"]), float(P["Jcc"]),
             float(P["lamA"]), float(P["A0"]), float(P["lamP"]), float(P["P0"]), float(P["lam_act"]), int(P["max_act"]))
    s["t"] += 1
    return s


def fields(s):
    sig = s["sig"]
    bd = np.zeros(sig.shape, bool)
    for dy, dx in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        bd |= sig != np.roll(np.roll(sig, dy, 0), dx, 1)
    cell = (sig > 0) & ~bd
    return np.stack([cell, s["act"] / float(P["max_act"]), bd & (sig > 0)]).astype(np.float32)


def damage(s, mask):
    s["sig"][mask] = 0; s["act"][mask] = 0
    N = int(P["N"])
    s["area"][:] = np.bincount(s["sig"].ravel(), minlength=N + 1)[:N + 1]; s["area"][0] = 0
    s["perim"][:] = _perims(s["sig"], N)
    return s
