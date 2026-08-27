"""operators_lib.py — l0-evolver variation operators on LIB-FORMAT genomes.

Operates on l0/lib/genome.py's canonical format (act={lam,k1,Du,u0};
chan={tau,D,g:"id"|"tanh",thr,sc}; W,K,bilin,provenance) — the shared format,
NOT forked. My earlier evolve/operators.py (own-format) passed the history-
reconstruction gates (results.json val_gate rows); this is the same algebra
ported to lib + the sampler's MEASURED k1 lesson (fold-distance log-jitter,
cf. lib/sampler.py v3: plain additive k1 jitter fails G0b ~50%% because all
certified refs sit at fold distance ~0.03).

MUTATION mutate(g, rng):
  log-normal on tau/D/Du (+tanh thr/sc), fold-distance log-jitter on k1
  (sign-preserving), small lognormal on lam, u0 continuation (nearest root),
  p_struct: add/remove one W or K edge (small |w| ~ logU[0.02,0.2]); never
  removes an act's last K edge or a chan's last W edge; bilin coeff jitter.

MERGE merge(g1, g2, mode, rng):
  block direct-sum (bilin indices offset), then ONE coupling move:
  - share_chan : fuse both blocks' long-range channels (max tau*D id-chan of
    act0) into one; K columns rewired, W row = per-parent old weights
    (rescale opt). Reconstructs vvw from iso-species (gate V1).
  - cross_edge : W[slow_chan_1, act0_of_2] = eta (+ symmetric). Reconstructs
    xv/rotor from two M4 worlds (gate V2).
  - slow_tanh  : add shared deposit channel g=tanh (thr>0: linearly dead,
    vacuum-exact) driven by both blocks' act0, K column +-kap into both.
    bfield-flavored composition (M6 lineage).
"""
import copy
import numpy as np

from . import genome as G


# ---------------------------------------------------------------- mutation
def _mul(rng, x, sigma):
    return float(x * np.exp(sigma * rng.standard_normal()))


def mutate(g, rng, sigma=0.15, sigma_d=0.4, p_struct=0.15):
    C = copy.deepcopy(g)
    moves = []
    for ci, ch in enumerate(C["chans"]):
        if rng.random() < 0.5:
            ch["tau"] = max(_mul(rng, ch["tau"], sigma), 0.05)
            moves.append(f"tau{ci}")
        if rng.random() < 0.5:
            ch["D"] = max(_mul(rng, ch["D"], sigma), 0.005)
            moves.append(f"D{ci}")
        if ch["g"] == "tanh":
            if rng.random() < 0.3:
                ch["thr"] = max(_mul(rng, ch["thr"], sigma), 0.05)
                moves.append(f"thr{ci}")
            if rng.random() < 0.3:
                ch["sc"] = max(_mul(rng, ch["sc"], sigma), 0.02)
                moves.append(f"sc{ci}")
    for ai, a in enumerate(C["acts"]):
        lam_old = a["lam"]
        if rng.random() < 0.3:
            a["lam"] = max(_mul(rng, a["lam"], sigma / 3), 0.3)
            moves.append(f"lam{ai}")
        if rng.random() < 0.5:
            a["Du"] = max(_mul(rng, a["Du"], sigma), 0.05)
            moves.append(f"Du{ai}")
        if rng.random() < 0.5 or a["lam"] != lam_old:
            # fold-distance log-jitter (sampler v3 lesson), sign preserved
            k1max_old = np.sqrt(4 * lam_old ** 3 / 27.0)
            r = a["k1"] / k1max_old if k1max_old > 0 else 0.0
            delta = max(1.0 - abs(r), 1e-4)
            delta = min(float(delta * np.exp(sigma_d * rng.standard_normal())), 0.9)
            k1max = np.sqrt(4 * a["lam"] ** 3 / 27.0)
            a["k1"] = float(np.sign(r) * (1.0 - delta) * k1max) if r != 0 else a["k1"]
            moves.append(f"k1{ai}")
        # u0 continuation
        rr = G.cubic_roots(a["lam"], a["k1"])
        if not rr:
            return None, dict(op="mutate", moves=moves, fail="root_lost")
        a["u0"] = G.polish_root(a["lam"], a["k1"],
                                min(rr, key=lambda x: abs(x - a["u0"])))
    for b in C.get("bilin", []):
        if rng.random() < 0.3:
            b[3] = _mul(rng, b[3], sigma)
            moves.append("bilin")
    if rng.random() < p_struct:
        W = np.asarray(C["W"], float)
        K = np.asarray(C["K"], float)
        nc, na = W.shape
        which = rng.choice(["addW", "addK", "delW", "delK"])
        amp = float(np.exp(rng.uniform(np.log(0.02), np.log(0.2)))
                    * (1 if rng.random() < 0.8 else -1))
        if which == "addW":
            zs = [(c, a) for c in range(nc) for a in range(na) if W[c, a] == 0.0]
            if zs:
                c, a = zs[rng.integers(len(zs))]
                W[c, a] = amp
                moves.append(f"addW[{c},{a}]={amp:.3f}")
        elif which == "addK":
            zs = [(a, c) for a in range(na) for c in range(nc) if K[a, c] == 0.0]
            if zs:
                a, c = zs[rng.integers(len(zs))]
                K[a, c] = amp
                moves.append(f"addK[{a},{c}]={amp:.3f}")
        elif which == "delW":
            cand = [(c, a) for c in range(nc) for a in range(na)
                    if W[c, a] != 0.0 and (np.abs(W[c]) > 0).sum() > 1]
            if cand:
                c, a = cand[rng.integers(len(cand))]
                W[c, a] = 0.0
                moves.append(f"delW[{c},{a}]")
        else:
            cand = [(a, c) for a in range(na) for c in range(nc)
                    if K[a, c] != 0.0 and (np.abs(K[a]) > 0).sum() > 1]
            if cand:
                a, c = cand[rng.integers(len(cand))]
                K[a, c] = 0.0
                moves.append(f"delK[{a},{c}]")
        C["W"] = W.tolist()
        C["K"] = K.tolist()
    if not moves:
        return mutate(g, rng, sigma, sigma_d, p_struct)
    C["provenance"] = dict(kind="evolve", op="mutate",
                           parents=[g.get("id", "?")], moves=moves)
    return C, dict(op="mutate", moves=moves)


# ------------------------------------------------------------------ merging
def _pid(g):
    return g.get("id", g.get("provenance", {}).get("ref", "?"))


def _block_merge(g1, g2):
    n1a, n1c = len(g1["acts"]), len(g1["chans"])
    n2a, n2c = len(g2["acts"]), len(g2["chans"])
    W = np.zeros((n1c + n2c, n1a + n2a))
    K = np.zeros((n1a + n2a, n1c + n2c))
    W[:n1c, :n1a] = np.asarray(g1["W"], float)
    W[n1c:, n1a:] = np.asarray(g2["W"], float)
    K[:n1a, :n1c] = np.asarray(g1["K"], float)
    K[n1a:, n1c:] = np.asarray(g2["K"], float)
    bil = [list(b) for b in g1.get("bilin", [])]
    bil += [[b[0] + n1a, b[1] + n1c, b[2] + n1c, b[3]] for b in g2.get("bilin", [])]
    M = dict(id="m", acts=copy.deepcopy(g1["acts"]) + copy.deepcopy(g2["acts"]),
             chans=copy.deepcopy(g1["chans"]) + copy.deepcopy(g2["chans"]),
             W=W, K=K, bilin=bil, provenance={})
    return M, (n1a, n1c, n2a, n2c)


def _longrange_chan(g, act=0):
    W = np.asarray(g["W"], float); K = np.asarray(g["K"], float)
    best, bs = None, -1.0
    for c, ch in enumerate(g["chans"]):
        if ch["g"] == "id" and abs(K[act, c]) > 1e-14 and abs(W[c, act]) > 1e-14:
            s = ch["tau"] * ch["D"]
            if s > bs:
                best, bs = c, s
    return best


def _slow_chan(g, act=0):
    W = np.asarray(g["W"], float); K = np.asarray(g["K"], float)
    best, bs = None, -1.0
    for c, ch in enumerate(g["chans"]):
        if ch["g"] == "id" and abs(K[act, c]) > 1e-14 and abs(W[c, act]) > 1e-14:
            if ch["tau"] > bs:
                best, bs = c, ch["tau"]
    return best


def merge_share_chan(g1, g2, rng=None, rescale=None):
    M, (n1a, n1c, n2a, n2c) = _block_merge(g1, g2)
    c1 = _longrange_chan(g1, 0)
    c2 = _longrange_chan(g2, 0)
    if c1 is None or c2 is None:
        return None, dict(op="merge_share_chan", fail="no_longrange_chan")
    c2g = n1c + c2
    W, K = M["W"], M["K"]
    for a in range(n1a + n2a):
        if abs(K[a, c2g]) > 1e-14:
            K[a, c1] = K[a, c2g]
            K[a, c2g] = 0.0
    r = 1.0 if rescale is None else rescale
    newrow = np.zeros(n1a + n2a)
    newrow[:n1a] = r * W[c1, :n1a]
    newrow[n1a:] = r * W[c2g, n1a:]
    W[c1] = newrow
    keep = [c for c in range(W.shape[0]) if c != c2g]
    remap = {c: i for i, c in enumerate(keep)}
    bil = []
    for (i, c, c2_, coef) in M["bilin"]:
        c_n = remap.get(c, remap.get(c1) if c == c2g else None)
        c2n = remap.get(c2_, remap.get(c1) if c2_ == c2g else None)
        if c == c2g:
            c_n = remap[c1]
        if c2_ == c2g:
            c2n = remap[c1]
        bil.append([i, c_n, c2n, coef])
    M["W"] = W[keep].tolist()
    M["K"] = K[:, keep].tolist()
    M["chans"] = [ch for i, ch in enumerate(M["chans"]) if i != c2g]
    M["bilin"] = bil
    M["provenance"] = dict(kind="evolve", op="merge_share_chan",
                           parents=[_pid(g1), _pid(g2)], rescale=rescale)
    return M, M["provenance"]


def merge_cross_edge(g1, g2, rng=None, eta=0.1, symmetric=True):
    M, (n1a, n1c, n2a, n2c) = _block_merge(g1, g2)
    c1 = _slow_chan(g1, 0)
    c2 = _slow_chan(g2, 0)
    if c1 is None or c2 is None:
        return None, dict(op="merge_cross_edge", fail="no_slow_chan")
    M["W"][c1, n1a] = eta
    if symmetric:
        M["W"][n1c + c2, 0] = eta
    M["W"] = np.asarray(M["W"]).tolist()
    M["K"] = np.asarray(M["K"]).tolist()
    M["provenance"] = dict(kind="evolve", op="merge_cross_edge",
                           parents=[_pid(g1), _pid(g2)], eta=eta,
                           symmetric=symmetric)
    return M, M["provenance"]


def merge_slow_tanh(g1, g2, rng=None, tau_b=60.0, D_b=0.5, gamma=0.05,
                    kap=0.05, thr=0.5, sc=0.4):
    M, (n1a, n1c, n2a, n2c) = _block_merge(g1, g2)
    W = np.asarray(M["W"], float); K = np.asarray(M["K"], float)
    nc = W.shape[0]
    Wn = np.zeros((nc + 1, W.shape[1])); Wn[:nc] = W
    Kn = np.zeros((K.shape[0], nc + 1)); Kn[:, :nc] = K
    Wn[nc, 0] = gamma
    Wn[nc, n1a] = gamma
    Kn[0, nc] = kap
    Kn[n1a, nc] = kap
    M["W"] = Wn.tolist(); M["K"] = Kn.tolist()
    M["chans"] = M["chans"] + [dict(tau=tau_b, D=D_b, g="tanh",
                                    thr=thr, sc=sc)]
    M["provenance"] = dict(kind="evolve", op="merge_slow_tanh",
                           parents=[_pid(g1), _pid(g2)], tau_b=tau_b, D_b=D_b,
                           gamma=gamma, kap=kap, thr=thr, sc=sc)
    return M, M["provenance"]


MERGE_OPS = dict(share_chan=merge_share_chan, cross_edge=merge_cross_edge,
                 slow_tanh=merge_slow_tanh)


# --------------------------------------------------- extra reference genomes
def ref_iso(d, tau=3.0, Dv=1.0, Du=0.65, wweight=0.5):
    """Continuum iso-line species (M5-prep canon: A'=d0.65, B=d0.75) as a
    lib-format 1-act genome; w driven at wweight (0.5 = lone-in-shared-world).
    share_chan-merging two of these reconstructs the certified vvw pair."""
    lam, k3, theta, Dw = 2.0, 1.0, 0.7, 20.0
    ub = float(sorted(x.real for x in np.roots([1.0, 0.0, 0.4, 1.0])
                      if abs(x.imag) < 1e-12)[0])
    k1p = -1.0 + d * ub
    k4 = 1.4 + d
    k1g = k1p - (k3 + k4) * ub
    return dict(id=f"ref_iso_d{d}",
                acts=[dict(lam=lam, k1=k1g, Du=Du, u0=G.polish_root(lam, k1g, ub))],
                chans=[dict(tau=tau, D=Dv, g="id", thr=0.0, sc=1.0),
                       dict(tau=theta, D=Dw, g="id", thr=0.0, sc=1.0)],
                W=[[1.0], [wweight]],
                K=[[k3, k4]],
                bilin=[],
                provenance=dict(kind="reference", source=f"M5-prep iso d={d}",
                                orig=dict(d=d, wweight=wweight)))
