"""lib/sampler.py — stage-1 candidate generators.

STRATEGY "uniform": random genome in sane dial ranges, random topology.
  n_act ~ {1:.6, 2:.4}; per act lam~logU[1,3.5], k1 ~ U(-1.15,1.15)*k1max(lam)
  (k1max = sqrt(4 lam^3/27): |k1|<k1max iff bistable, so ~87%% pass G0b — honest
  G0b rejection rate retained), Du~logU[.4,2.5].
  n_chan ~ {2:.45, 3:.4, 4:.15}; per chan: slow-memory w.p. .12 (tau~logU[20,400])
  else tau~logU[.3,10]; D~logU[.3,30]; g=tanh w.p. .18 (thr~logU[.3,1.2],
  sc~logU[.2,1]).
  W: each chan gets a primary act (W=1 canonical normalization); off entries
  nonzero w.p. .35, mag~logU[.05,.8], sign + w.p. .8.
  K: primary-act entry mag~logU[.2,3] sign + w.p. .85 (negative K = channel
  EXCITES its act — rare but sampled); off entries nonzero w.p. .3,
  mag~logU[.05,1.5], sign + w.p. .8.
  u0 designation IS A GENE: uniform choice among G0a-stable root combos.

STRATEGY "jitter": reference genome (M0/M4/VVW/XV/BFIELD equal weight), every
  positive dial multiplied by lognormal(sigma=0.15); k1 additive N(0,0.05);
  W cross entries (not the 1.0/0.5 primaries) jittered too. u0 by continuation
  (polish from reference u0). Structural moves belong to l0-evolver.
"""
import copy
import numpy as np

import genome as G
import funnel as FU


def _logu(rng, a, b):
    return float(np.exp(rng.uniform(np.log(a), np.log(b))))


def sample_uniform(rng):
    n_act = 1 if rng.random() < 0.6 else 2
    n_chan = rng.choice([2, 3, 4], p=[0.45, 0.4, 0.15])
    acts = []
    for _ in range(n_act):
        lam = _logu(rng, 1.0, 3.5)
        k1max = np.sqrt(4 * lam ** 3 / 27.0)
        k1 = float(rng.uniform(-1.15, 1.15) * k1max)
        acts.append(dict(lam=lam, k1=k1, Du=_logu(rng, 0.4, 2.5), u0=0.0))
    chans, W = [], []
    for c in range(n_chan):
        if rng.random() < 0.12:
            tau = _logu(rng, 20.0, 400.0)
        else:
            tau = _logu(rng, 0.3, 10.0)
        D = _logu(rng, 0.3, 30.0)
        if rng.random() < 0.18:
            ch = dict(tau=tau, D=D, g="tanh", thr=_logu(rng, 0.3, 1.2),
                      sc=_logu(rng, 0.2, 1.0))
        else:
            ch = dict(tau=tau, D=D, g="id", thr=0.0, sc=1.0)
        chans.append(ch)
        prim = int(rng.integers(n_act))
        row = [0.0] * n_act
        row[prim] = 1.0
        for a in range(n_act):
            if a != prim and rng.random() < 0.35:
                row[a] = float(_logu(rng, 0.05, 0.8)
                               * (1 if rng.random() < 0.8 else -1))
        W.append(row)
    K = []
    for i in range(n_act):
        row = [0.0] * n_chan
        for c in range(n_chan):
            if W[c][i] == 1.0:      # this chan's primary act
                row[c] = float(_logu(rng, 0.2, 3.0)
                               * (1 if rng.random() < 0.85 else -1))
            elif rng.random() < 0.3:
                row[c] = float(_logu(rng, 0.05, 1.5)
                               * (1 if rng.random() < 0.8 else -1))
        K.append(row)
    g = dict(id="u", acts=acts, chans=chans, W=W, K=K, bilin=[],
             provenance=dict(kind="uniform"))
    # u0 gene: uniform choice among stable designations
    tried = FU.enumerate_vacua(g)
    if tried is None:
        return g, "no_real_root"
    stable = [t for t in tried if t[1] < 0.0]
    if not stable:
        # keep best (unstable) designation so the funnel logs its margin
        u0s = tried[0][0]
        why = "no_stable_root"
    else:
        u0s = stable[int(rng.integers(len(stable)))][0]
        why = None
    for i, u in enumerate(u0s):
        g["acts"][i]["u0"] = G.polish_root(acts[i]["lam"], acts[i]["k1"], u)
    return g, why


REF_NAMES = ["M0", "M4", "VVW", "XV", "BFIELD"]


def jitter_genome(rng, g, sigma=0.15, sigma_d=0.4):
    """Generic theory-coord jitter of ANY genome (refs or elites): log-jitter
    every positive dial, log-jitter each act's fold distance, snap u0 to the
    nearest root (continuation). Mutates and returns g (caller deep-copies)."""
    def mul(x):
        return float(x * np.exp(sigma * rng.standard_normal()))
    for a in g["acts"]:
        lam_old = a["lam"]
        k1max_old = np.sqrt(4 * lam_old ** 3 / 27.0)
        r = a["k1"] / k1max_old
        delta = max(1.0 - abs(r), 1e-4)
        delta = float(delta * np.exp(sigma_d * rng.standard_normal()))
        delta = min(delta, 0.9)
        r_new = np.sign(r) * (1.0 - delta) if r != 0 else (1.0 - delta)
        a["lam"] = mul(a["lam"])
        a["Du"] = mul(a["Du"])
        k1max = np.sqrt(4 * a["lam"] ** 3 / 27.0)
        a["k1"] = float(r_new * k1max)
        a["u0"] = float(a["u0"] * np.sqrt(a["lam"] / lam_old))
    for ch in g["chans"]:
        ch["tau"] = mul(ch["tau"])
        ch["D"] = mul(ch["D"])
        if ch["g"] == "tanh":
            ch["thr"] = mul(ch["thr"])
            ch["sc"] = mul(ch["sc"])
    W = np.asarray(g["W"], float)
    for c in range(W.shape[0]):
        for a in range(W.shape[1]):
            if W[c, a] not in (0.0, 1.0, 0.5):
                W[c, a] = mul(W[c, a]) if W[c, a] > 0 else -mul(-W[c, a])
    g["W"] = W.tolist()
    K = np.asarray(g["K"], float)
    for i in range(K.shape[0]):
        for c in range(K.shape[1]):
            if K[i, c] != 0.0:
                K[i, c] = mul(K[i, c]) if K[i, c] > 0 else -mul(-K[i, c])
    g["K"] = K.tolist()
    ok = True
    for a in g["acts"]:
        rr = G.cubic_roots(a["lam"], a["k1"])
        if not rr:
            ok = False
            continue
        a["u0"] = min(rr, key=lambda x: abs(x - a["u0"]))
    return g, (None if ok else "root_lost")


def sample_jitter(rng, sigma=0.15, sigma_d=0.4):
    """Theory-coord jitter. MEASURED LADDER (2026-02-19): plain k1 jitter fails
    G0b ~50%; additive r=k1/k1max jitter still fails ~50% because ALL certified
    refs sit at fold distance delta=1-|r| ~ 0.027-0.03 (blobs live NEAR THE
    CUBIC FOLD). v3: log-jitter the fold distance itself, delta' = delta *
    exp(sigma_d*N) — candidates stay bistable BY CONSTRUCTION and explore
    [~0.4x, ~2.5x] the reference's fold margin. u0 continuation: u0 ~ sqrt(lam)
    scaling then Newton-polish; sign of r preserved."""
    name = REF_NAMES[int(rng.integers(len(REF_NAMES)))]
    g = copy.deepcopy(G.REFS[name]())
    g["provenance"] = dict(kind="jitter", ref=name, sigma=sigma, sigma_d=sigma_d)
    g["id"] = f"j_{name}"
    return jitter_genome(rng, g, sigma=sigma, sigma_d=sigma_d)
