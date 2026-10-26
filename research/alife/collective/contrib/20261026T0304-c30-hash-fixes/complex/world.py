"""Complex Hash Chemistry: explicit multiset complexes that contest their neighbours (c30).

Entities are complexes: a sorted multiset of 1..KMAX particle types (1..1000) at a position in the
unit square (cut-off boundaries). Each step every complex moves by a randomly oriented half-normal
step (sigma), then, for every complex in random order: pick one random other complex within R; if
there is none, nothing happens. The two contest; the winner makes a copy of itself with probability
1 - m/dmax (m = complexes within R) placed at its own position, and the loser dies with probability
pdie. Copies mutate: each member type is redrawn with prob mu, one random type is inserted with
prob mu_ins (if size < KMAX), one member is deleted with prob mu_del (if size > 1). The kind of a
complex is its composition, hashed by mkey (Hash Chemistry's key).

Contest rules (P['rule']):
  'zerosum'    P(A beats B) = h(A,B) = 1 - h(B,A), h a hash of the ordered pair: non-transitive,
               a resident ties itself (0.5), so about half of all mutants beat it;
  'transitive' P(A beats B) = f(A) / (f(A) + f(B)), f = Sayama's hash fitness of one complex: a static
               landscape with a ceiling (the matched control);
  'neutral'    P = 1/2 (identical events, no selection: the in-world neutral twin);
  'feature'    correlated non-transitive: every type t has hashed Gaussian attack and vulnerability
               vectors a_t, v_t in R^D; a complex's phenotype is the mean over its members;
               P(A beats B) = 1 / (1 + exp(-beta (a_A.v_B - a_B.v_A))). Antisymmetric like 'zerosum',
               but a mutation moves the phenotype only by about 1/size, so advantages are heritable.
"""
import os, json
import numpy as np
from numba import njit

META = {"name": "complex-hash-chemistry", "family": "hash-chemistry", "parent": "collective/contrib/20261026T0009-c30-hash-chemistry-o-calibration/world.py",
        "mutation": "particles bound into explicit complexes that move, contest a neighbour and replicate with type/insert/delete mutations",
        "size": (128, 128), "steps_per_frame": 25, "dt": 1.0, "channels": ["complexes", "top_kind", "mean_size"], "matter": [0],
        "threshold": None, "smooth": 1.0, "periodic": False, "domain": (1.0, 1.0)}
P = dict(rule="zerosum", ntypes=1000, n0=500, kmax=16, sigma=0.05, R=0.05, dmax=30.0, pdie=0.5, mu=0.01, mu_ins=0.02,
         mu_del=0.02, salt=12345, fsalt=777, D=3, beta=3.0, cap=200000, maxev=20_000_000)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))
RULES = {"zerosum": 0, "transitive": 1, "neutral": 2, "feature": 3}


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
def nb_step(t, x, y, comp, ln, key, alive, n, head, nxt, neigh, ctr, rep_t, rep_k, rep_s, die_t, die_s,
            rule, ntypes, kmax, sigma, R, dmax, pdie, mu, mu_ins, mu_del, salt, fsalt, feat, beta):
    cap = len(x); maxev = len(rep_t)
    G = int(1.0 / R); cs = 1.0 / G
    if n == 0:
        return 0
    for i in range(n):
        L = abs(np.random.normal()) * sigma; a = 2 * np.pi * np.random.random()
        x[i] = min(1.0, max(0.0, x[i] + L * np.cos(a))); y[i] = min(1.0, max(0.0, y[i] + L * np.sin(a)))
    head[:] = -1
    for i in range(n):
        c = min(G - 1, int(x[i] / cs)) * G + min(G - 1, int(y[i] / cs)); nxt[i] = head[c]; head[c] = i
    order = np.random.permutation(n)
    tmpc = np.empty(kmax + 1, np.int64)
    for oi in range(n):
        i = order[oi]
        if not alive[i]:
            continue
        gx = min(G - 1, int(x[i] / cs)); gy = min(G - 1, int(y[i] / cs)); m = 0
        for ax in range(max(0, gx - 1), min(G, gx + 2)):
            for ay in range(max(0, gy - 1), min(G, gy + 2)):
                q = head[ax * G + ay]
                while q >= 0:
                    if alive[q] and q != i:
                        dx = x[q] - x[i]; dy = y[q] - y[i]
                        if dx * dx + dy * dy <= R * R:
                            neigh[m] = q; m += 1
                    q = nxt[q]
        if m == 0:
            continue
        j = neigh[np.random.randint(m)]
        ka = key[i]; kb = key[j]
        if rule == 2 or ka == kb:
            pa = 0.5
        elif rule == 3:
            D = feat.shape[1] // 2; g = 0.0
            for d in range(D):
                aa = 0.0; va = 0.0; ab = 0.0; vb = 0.0
                for q in range(ln[i]):
                    aa += feat[comp[i, q], d]; va += feat[comp[i, q], D + d]
                for q in range(ln[j]):
                    ab += feat[comp[j, q], d]; vb += feat[comp[j, q], D + d]
                g += (aa / ln[i]) * (vb / ln[j]) - (ab / ln[j]) * (va / ln[i])
            pa = 1.0 / (1.0 + np.exp(-beta * g))
        elif rule == 1:
            fa = fit_hash(_mix(ka + np.uint64(fsalt))); fb = fit_hash(_mix(kb + np.uint64(fsalt)))
            pa = fa / (fa + fb) if fa + fb > 0 else 0.5
        elif ka < kb:
            pa = fit_hash(_mix(ka ^ _mix(kb + np.uint64(fsalt))))
        else:
            pa = 1.0 - fit_hash(_mix(kb ^ _mix(ka + np.uint64(fsalt))))
        if np.random.random() < pa:
            w = i; l = j
        else:
            w = j; l = i
        if np.random.random() < pdie:
            alive[l] = False
            if ctr[1] < maxev:
                die_t[ctr[1]] = t; die_s[ctr[1]] = ln[l]; ctr[1] += 1
        if np.random.random() < 1.0 - (m + 1) / dmax and n < cap:
            L0 = ln[w]
            for a in range(L0):
                tmpc[a] = comp[w, a]
            for a in range(L0):
                if np.random.random() < mu:
                    tmpc[a] = 1 + np.random.randint(ntypes)
            if L0 < kmax and np.random.random() < mu_ins:
                tmpc[L0] = 1 + np.random.randint(ntypes); L0 += 1
            if L0 > 1 and np.random.random() < mu_del:
                d = np.random.randint(L0); tmpc[d] = tmpc[L0 - 1]; L0 -= 1
            srt = np.sort(tmpc[:L0])
            comp[n, :L0] = srt; ln[n] = L0; key[n] = mkey(srt, salt)
            x[n] = x[w]; y[n] = y[w]; alive[n] = True
            c = min(G - 1, int(x[n] / cs)) * G + min(G - 1, int(y[n] / cs)); nxt[n] = head[c]; head[c] = n
            if ctr[0] < maxev:
                rep_t[ctr[0]] = t; rep_k[ctr[0]] = key[n]; rep_s[ctr[0]] = L0; ctr[0] += 1
            n += 1
    wv = 0
    for i in range(n):
        if alive[i]:
            x[wv] = x[i]; y[wv] = y[i]; comp[wv] = comp[i]; ln[wv] = ln[i]; key[wv] = key[i]; wv += 1
    n = wv
    alive[:n] = True; alive[n:] = False
    return n


def init(seed, size=None, p=None):
    p = dict(P, **(p or {})); _seed(int(seed)); np.random.seed(int(seed))   # (fix) seed numpy too
    cap, maxev, kmax = int(p["cap"]), int(p["maxev"]), int(p["kmax"])
    S = dict(p=p, t=0, x=np.empty(cap), y=np.empty(cap), comp=np.zeros((cap, kmax), np.int64), ln=np.zeros(cap, np.int64),
             key=np.zeros(cap, np.uint64), alive=np.zeros(cap, np.bool_), head=np.empty(int(1 / p["R"]) ** 2, np.int64),
             nxt=np.empty(cap, np.int64), neigh=np.empty(cap, np.int64), ctr=np.zeros(3, np.int64),
             rep_t=np.empty(maxev, np.int32), rep_k=np.empty(maxev, np.uint64), rep_s=np.empty(maxev, np.int32),
             die_t=np.empty(maxev, np.int32), die_s=np.empty(maxev, np.int32), pop=[], msize=[], size=size or META["size"])
    n0 = int(p["n0"])
    S["x"][:n0] = np.random.random(n0); S["y"][:n0] = np.random.random(n0)
    for i in range(n0):
        S["comp"][i, 0] = 1 + np.random.randint(p["ntypes"]); S["ln"][i] = 1
        S["key"][i] = mkey(S["comp"][i, :1].copy(), np.int64(p["salt"]))
    S["alive"][:n0] = True; S["n"] = n0
    rng = np.random.default_rng(int(p["fsalt"]))          # the type features: fixed by fsalt, not by the run seed
    S["feat"] = rng.normal(size=(int(p["ntypes"]) + 1, 2 * int(p["D"])))
    return S


def step(S):
    p = S["p"]
    S["n"] = nb_step(S["t"], S["x"], S["y"], S["comp"], S["ln"], S["key"], S["alive"], S["n"], S["head"], S["nxt"], S["neigh"],
                     S["ctr"], S["rep_t"], S["rep_k"], S["rep_s"], S["die_t"], S["die_s"], RULES[p["rule"]], int(p["ntypes"]),
                     int(p["kmax"]), float(p["sigma"]), float(p["R"]), float(p["dmax"]), float(p["pdie"]), float(p["mu"]),
                     float(p["mu_ins"]), float(p["mu_del"]), int(p["salt"]), int(p["fsalt"]), S["feat"], float(p["beta"]))
    S["t"] += 1; S["pop"].append(S["n"]); S["msize"].append(float(S["ln"][:S["n"]].mean()) if S["n"] else 0.0)
    return S


def logs(S):
    nr, nd = S["ctr"][0], S["ctr"][1]
    return dict(rep_t=S["rep_t"][:nr].copy(), rep_k=S["rep_k"][:nr].copy(), rep_s=S["rep_s"][:nr].copy(),
                die_t=S["die_t"][:nd].copy(), die_s=S["die_s"][:nd].copy(), pop=np.array(S["pop"]), msize=np.array(S["msize"]))


def particles(S):
    n = S["n"]
    return np.stack([S["x"][:n], S["y"][:n], (S["key"][:n] % np.uint64(1000)).astype(float)], 1)


def fields(S):
    H, W = S["size"]; n = S["n"]; out = np.zeros((3, H, W))
    if n == 0:
        return out
    ix = np.minimum(H - 1, (S["y"][:n] * H).astype(int)); jx = np.minimum(W - 1, (S["x"][:n] * W).astype(int))
    np.add.at(out[0], (ix, jx), 1.0)
    u, c = np.unique(S["key"][:n], return_counts=True); top = u[c.argmax()]; msk = S["key"][:n] == top
    np.add.at(out[1], (ix[msk], jx[msk]), 1.0); np.add.at(out[2], (ix, jx), S["ln"][:n].astype(float))
    out[2] /= np.maximum(out[0], 1)
    return out
