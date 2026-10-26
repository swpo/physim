"""Spatial Hash Chemistry (Sayama 2019, Artificial Life 25(2):104-116; arXiv:1806.06628) as a labkit world.

Particles of types 1..1000 in the unit square (cut-off boundaries), 10 random initial particles.
Per step: (1) each particle moves by a randomly oriented vector with half-normal length (sigma 0.15),
clipped to the square; (2) for each particle position (snapshot at the step start, random order):
N = live particles within R = 0.05 (newborns of this step included); s = random k-subset of N,
k ~ U{1..|N|}; with probability 1/|s|: f = fitness(s); with prob 1-f all of s die; otherwise with
prob f(1-|N|/dmax) overall, copies of all of s are added at the same positions; (3) each particle
mutates to a uniformly random type with prob 0.01; (4) the order of particles is shuffled.
fitness modes (WORLD_P env or P dict):
  mode 0 (default): f = (H(sorted types) mod 1e5)/1e5, H a fixed 64-bit hash (splitmix-style), the
          consistent landscape of the paper;
  mode 1: f ~ U[lo, 1] drawn afresh at every evaluation (Sayama's control; lo = 0.2 biased, 0 fair);
  mode 2: f(s) = mean of the singleton hash fitnesses of the members (additive, no cardinality leap).
Every replication event is logged (step, multiset key, size), as are deaths and mutation counts; the
analysis scripts (o_measure.py) read these logs.
fields(): channel 0 = particle density on a 128^2 raster, channel 1 = density of the most common type,
channel 2 = density of all other types.
"""
import os, json
import numpy as np
from numba import njit

META = {
    "name": "hash-chemistry-v2", "family": "hash-chemistry", "parent": None,
    "mutation": "reproduction of Sayama 2019 Hash Chemistry (positive control for O)",
    "size": (128, 128), "steps_per_frame": 20, "dt": 1.0,
    "channels": ["density", "top_type", "other_types"], "matter": [0],
    "threshold": None, "smooth": 1.0, "periodic": False, "domain": (1.0, 1.0),
}
P = dict(mode=0, lo=0.2, salt=12345, ntypes=1000, n0=10, sigma=0.15, R=0.05, dmax=100.0, mu=0.01,
         cap=400000, maxev=10_000_000, resalt=0, crowd=0.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


@njit
def _mix(z):
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return z ^ (z >> np.uint64(31))


@njit
def mkey(sorted_types, salt):
    h = np.uint64(salt) * np.uint64(0x9E3779B97F4A7C15) + np.uint64(len(sorted_types))
    for t in sorted_types:
        h = _mix(h ^ (np.uint64(t) + np.uint64(0x632BE59BD9B4E019)))
    return h


@njit
def fit_hash(key):
    return (key % np.uint64(100000)) / 1e5


@njit
def _seed(s):
    np.random.seed(s)


@njit
def nb_step(t, x, y, ty, alive, n, head, nxt, neigh, sub, tbuf, ctr, rep_t, rep_k, rep_s, die_t, die_s,
            mode, lo, salt, ntypes, sigma, R, dmax, mu, fsalt, crowd):
    """One step. ctr = [nrep, ndie, overflow]. Returns (n, mutations)."""
    cap = len(x); maxev = len(rep_t)
    G = int(1.0 / R); cs = 1.0 / G
    if n == 0:
        return 0, 0
    for i in range(n):
        L = abs(np.random.normal()) * sigma
        a = 2 * np.pi * np.random.random()
        x[i] = min(1.0, max(0.0, x[i] + L * np.cos(a)))
        y[i] = min(1.0, max(0.0, y[i] + L * np.sin(a)))
    head[:] = -1
    for i in range(n):
        c = min(G - 1, int(x[i] / cs)) * G + min(G - 1, int(y[i] / cs))
        nxt[i] = head[c]; head[c] = i
    order = np.random.permutation(n)
    px = x[:n].copy(); py = y[:n].copy()
    for oi in range(n):
        j = order[oi]
        fx = px[j]; fy = py[j]
        gx = min(G - 1, int(fx / cs)); gy = min(G - 1, int(fy / cs))
        m = 0
        for ax in range(max(0, gx - 1), min(G, gx + 2)):
            for ay in range(max(0, gy - 1), min(G, gy + 2)):
                q = head[ax * G + ay]
                while q >= 0:
                    if alive[q]:
                        dx = x[q] - fx; dy = y[q] - fy
                        if dx * dx + dy * dy <= R * R:
                            neigh[m] = q; m += 1
                    q = nxt[q]
        if m == 0:
            continue
        k = 1 + np.random.randint(m)
        if np.random.random() >= 1.0 / k:
            continue
        for a in range(k):
            b = a + np.random.randint(m - a)
            tmp = neigh[a]; neigh[a] = neigh[b]; neigh[b] = tmp
            sub[a] = neigh[a]
        for a in range(k):
            tbuf[a] = ty[sub[a]]
        st = np.sort(tbuf[:k])
        key = mkey(st, salt)
        if mode == 0:
            f = fit_hash(mkey(st, fsalt)) if fsalt != salt else fit_hash(key)
        elif mode == 1:
            f = lo + (1.0 - lo) * np.random.random()
        else:
            f = 0.0
            one = np.empty(1, np.int64)
            for a in range(k):
                one[0] = st[a]
                f += fit_hash(mkey(one, salt))
            f /= k
        if crowd > 0.0:
            # kill-the-winner: fitness falls with the share of the neighbourhood that has the subset's commonest type
            best = 0; cur = 1; bt = st[0]
            for a in range(1, k + 1):
                if a < k and st[a] == st[a - 1]:
                    cur += 1
                else:
                    if cur > best:
                        best = cur; bt = st[a - 1]
                    cur = 1
            same = 0
            for a in range(m):
                if ty[neigh[a]] == bt:
                    same += 1
            f = f * (1.0 - crowd * same / m)
        r = np.random.random()
        if r < 1.0 - f:
            for a in range(k):
                alive[sub[a]] = False
            if ctr[1] < maxev:
                die_t[ctr[1]] = t; die_s[ctr[1]] = k; ctr[1] += 1
        elif r < 1.0 - f + f * (1.0 - m / dmax):
            if n + k > cap:
                ctr[2] = 1
                continue
            for a in range(k):
                q = sub[a]
                x[n] = x[q]; y[n] = y[q]; ty[n] = ty[q]; alive[n] = True
                c = min(G - 1, int(x[n] / cs)) * G + min(G - 1, int(y[n] / cs))
                nxt[n] = head[c]; head[c] = n
                n += 1
            if ctr[0] < maxev:
                rep_t[ctr[0]] = t; rep_k[ctr[0]] = key; rep_s[ctr[0]] = k; ctr[0] += 1
            else:
                ctr[2] = 2
    cnt = 0
    for i in range(n):
        if alive[i] and np.random.random() < mu:
            ty[i] = 1 + np.random.randint(ntypes); cnt += 1
    w = 0
    for i in range(n):
        if alive[i]:
            x[w] = x[i]; y[w] = y[i]; ty[w] = ty[i]; w += 1
    n = w
    perm = np.random.permutation(n)
    x[:n] = x[:n][perm]; y[:n] = y[:n][perm]; ty[:n] = ty[:n][perm]
    alive[:n] = True; alive[n:] = False
    return n, cnt


def init(seed, size=None, p=None):
    p = dict(P, **(p or {}))
    _seed(int(seed))
    cap, maxev = int(p["cap"]), int(p["maxev"])
    S = dict(p=p, t=0, x=np.empty(cap), y=np.empty(cap), ty=np.zeros(cap, np.int64), alive=np.zeros(cap, np.bool_),
             head=np.empty(int(1 / p["R"]) ** 2, np.int64), nxt=np.empty(cap, np.int64), neigh=np.empty(cap, np.int64),
             sub=np.empty(cap, np.int64), tbuf=np.empty(cap, np.int64), ctr=np.zeros(3, np.int64),
             rep_t=np.empty(maxev, np.int32), rep_k=np.empty(maxev, np.uint64), rep_s=np.empty(maxev, np.int32),
             die_t=np.empty(maxev, np.int32), die_s=np.empty(maxev, np.int32), mut=[], pop=[], size=size or META["size"])
    n0 = int(p["n0"])
    S["x"][:n0] = np.random.random(n0); S["y"][:n0] = np.random.random(n0)
    S["ty"][:n0] = 1 + np.random.randint(0, p["ntypes"], n0); S["alive"][:n0] = True
    S["n"] = n0; S["pop"].append(n0)
    return S


def step(S):
    p = S["p"]
    n, cnt = nb_step(S["t"], S["x"], S["y"], S["ty"], S["alive"], S["n"], S["head"], S["nxt"], S["neigh"], S["sub"],
                     S["tbuf"], S["ctr"], S["rep_t"], S["rep_k"], S["rep_s"], S["die_t"], S["die_s"],
                     int(p["mode"]), float(p["lo"]), int(p["salt"]), int(p["ntypes"]), float(p["sigma"]),
                     float(p["R"]), float(p["dmax"]), float(p["mu"]), int(p["salt"]) + (S["t"] // int(p["resalt"]) if p["resalt"] else 0), float(p["crowd"]))
    S["n"] = n; S["t"] += 1; S["mut"].append(cnt); S["pop"].append(n)
    return S


def logs(S):
    nr, nd = S["ctr"][0], S["ctr"][1]
    return dict(rep_t=S["rep_t"][:nr].copy(), rep_k=S["rep_k"][:nr].copy(), rep_s=S["rep_s"][:nr].copy(),
                die_t=S["die_t"][:nd].copy(), die_s=S["die_s"][:nd].copy(), mut_n=np.array(S["mut"], np.int64),
                pop=np.array(S["pop"]), overflow=int(S["ctr"][2]))


def particles(S):
    n = S["n"]
    return np.stack([S["x"][:n], S["y"][:n], S["ty"][:n].astype(float)], 1)


def fields(S):
    H, W = S["size"]; n = S["n"]
    out = np.zeros((3, H, W))
    if n == 0:
        return out
    ix = np.minimum(H - 1, (S["y"][:n] * H).astype(int)); jx = np.minimum(W - 1, (S["x"][:n] * W).astype(int))
    ty = S["ty"][:n]
    np.add.at(out[0], (ix, jx), 1.0)
    top = np.bincount(ty).argmax()
    m = ty == top
    np.add.at(out[1], (ix[m], jx[m]), 1.0); np.add.at(out[2], (ix[~m], jx[~m]), 1.0)
    return out
