"""operators.py — l0-evolver variation operators on canonical genomes.

MUTATION (theory-coordinate jitter):
  - log-normal jitter on tau_c, D_c, Du_a (scale sigma_log)
  - additive jitter on lam_a (small) and k1_a CLAMPED to the bistable window
    (k1 s.t. cubic -u^3+lam u+k1 has 3 real roots: |k1| < 2*(lam/3)^{3/2}),
    with margin frac 0.98; vacuum u0 re-solved = root nearest old u0 (keeps
    the world on the same branch; reject if branch vanishes)
  - structural micro-move (p_struct): add/remove one W or K edge with small
    weight (add: |w| ~ U(0.02, 0.15) signed; remove: only edges NOT the last
    self-loop of a channel/act — never orphan a channel drive entirely? we
    allow orphaning W (channel goes silent -> x_c=0, harmless) but never
    remove the last K entry of an act (act would decouple from all chans ->
    guaranteed Turing soup at bistable k1; cheap-reject anyway).

MERGE (block composition), three coupling modes after direct-sum grafting:
  - share_chan (vvw-style): pick one "long-range" channel from each parent
    (largest tau*D among coupled chans, ties -> largest D), DELETE g2's copy,
    rewire: shared W row = avg-drive (0.5*w1_row | 0.5*w2_row), K columns of
    both acts point at the shared channel (each keeps its own K weight).
  - cross_edge (xv-style): keep all channels private; add W[c1, a2] = eta and
    (symmetric variant) W[c2, a1] = eta on the two parents' chosen slow
    channels (largest tau among coupled, i.e. the v-channels for Purwins refs).
  - slow_tanh (bfield-style): add ONE new shared channel x_new with
    g = tanh((z-thr)/sc), thr in the "blob-only fires" band, driven by both
    acts (W row = gamma each), K column small +-kap into both acts.
Lineage: child["provenance"] = {op, parents: [id1, id2], params}.
"""
import copy
import numpy as np
from engine import cubic_roots


def k1_window(lam):
    return 2.0 * (max(lam, 1e-9) / 3.0) ** 1.5


def resolve_vacuum(G):
    """Re-solve each act's vacuum as the root nearest the cached one.
    Returns False if any act loses bistability structure entirely."""
    ok = True
    for a, act in enumerate(G["acts"]):
        roots = cubic_roots(act["lam"], act["k1"])
        if not roots:
            return False
        old = G["u0"][a]
        G["u0"][a] = min(roots, key=lambda r: abs(r - old))
        if len(roots) < 3:
            ok = False
    return ok


def mutate(G, rng, sigma_log=0.15, sigma_k1=0.05, sigma_lam=0.05,
           p_struct=0.15, w_new=(0.02, 0.15)):
    """Return (child, opinfo) or (None, reason) if the move broke the vacuum."""
    C = copy.deepcopy(G)
    moves = []
    # continuous jitters (each dial mutated with prob 0.5)
    for c, ch in enumerate(C["chans"]):
        if rng.random() < 0.5:
            f = float(np.exp(sigma_log * rng.standard_normal()))
            ch["tau"] = max(ch["tau"] * f, 0.05)
            moves.append(("tau", c, f))
        if rng.random() < 0.5:
            f = float(np.exp(sigma_log * rng.standard_normal()))
            ch["D"] = max(ch["D"] * f, 0.01)
            moves.append(("D", c, f))
        if ch["g"]["kind"] == "tanh" and rng.random() < 0.3:
            f = float(np.exp(sigma_log * rng.standard_normal()))
            ch["g"]["sc"] = max(ch["g"]["sc"] * f, 0.02)
            moves.append(("g_sc", c, f))
    for a, act in enumerate(C["acts"]):
        if rng.random() < 0.5:
            f = float(np.exp(sigma_log * rng.standard_normal()))
            act["Du"] = max(act["Du"] * f, 0.05)
            moves.append(("Du", a, f))
        if rng.random() < 0.3:
            d = float(sigma_lam * rng.standard_normal())
            act["lam"] = max(act["lam"] + d, 0.3)
            moves.append(("lam", a, d))
        if rng.random() < 0.5:
            d = float(sigma_k1 * rng.standard_normal())
            act["k1"] = act["k1"] + d
            moves.append(("k1", a, d))
        # clamp k1 into bistable window (with margin)
        w = 0.98 * k1_window(act["lam"])
        act["k1"] = float(np.clip(act["k1"], -w, w))
    # structural micro-move
    if rng.random() < p_struct:
        W = np.asarray(C["W"], float)
        K = np.asarray(C["K"], float)
        which = rng.choice(["addW", "addK", "delW", "delK"])
        nz_w = [(c, a) for c in range(W.shape[0]) for a in range(W.shape[1]) if abs(W[c, a]) > 1e-14]
        z_w = [(c, a) for c in range(W.shape[0]) for a in range(W.shape[1]) if abs(W[c, a]) <= 1e-14]
        nz_k = [(a, c) for a in range(K.shape[0]) for c in range(K.shape[1]) if abs(K[a, c]) > 1e-14]
        z_k = [(a, c) for a in range(K.shape[0]) for c in range(K.shape[1]) if abs(K[a, c]) <= 1e-14]
        amp = float(rng.uniform(*w_new)) * (1 if rng.random() < 0.5 else -1)
        if which == "addW" and z_w:
            c, a = z_w[rng.integers(len(z_w))]
            W[c, a] = amp
            moves.append(("addW", (c, a), amp))
        elif which == "addK" and z_k:
            a, c = z_k[rng.integers(len(z_k))]
            K[a, c] = amp
            moves.append(("addK", (a, c), amp))
        elif which == "delW" and len(nz_w) > 1:
            c, a = nz_w[rng.integers(len(nz_w))]
            W[c, a] = 0.0
            moves.append(("delW", (c, a), 0.0))
        elif which == "delK":
            # never orphan an act's K row completely
            cand = [(a, c) for (a, c) in nz_k
                    if (np.abs(K[a]) > 1e-14).sum() > 1]
            if cand:
                a, c = cand[rng.integers(len(cand))]
                K[a, c] = 0.0
                moves.append(("delK", (a, c), 0.0))
        C["W"] = W.tolist()
        C["K"] = K.tolist()
    if not moves:
        return mutate(G, rng, sigma_log, sigma_k1, sigma_lam, p_struct, w_new)
    if resolve_vacuum(C) is False:
        return None, {"op": "mutate", "moves": moves, "fail": "vacuum_lost"}
    C["provenance"] = {"op": "mutate",
                       "parents": [G.get("provenance", {}).get("id", G.get("provenance", {}).get("ref", "?"))],
                       "moves": [[str(m[0]), str(m[1]), float(m[2])] for m in moves]}
    return C, {"op": "mutate", "moves": moves}


# ------------------------------------------------------------------- merging
def _block_merge(G1, G2):
    """Direct sum: acts/chans concatenated, W/K block-diagonal."""
    n1a, n1c = len(G1["acts"]), len(G1["chans"])
    n2a, n2c = len(G2["acts"]), len(G2["chans"])
    W = np.zeros((n1c + n2c, n1a + n2a))
    K = np.zeros((n1a + n2a, n1c + n2c))
    W[:n1c, :n1a] = np.asarray(G1["W"], float)
    W[n1c:, n1a:] = np.asarray(G2["W"], float)
    K[:n1a, :n1c] = np.asarray(G1["K"], float)
    K[n1a:, n1c:] = np.asarray(G2["K"], float)
    return {"acts": copy.deepcopy(G1["acts"]) + copy.deepcopy(G2["acts"]),
            "chans": copy.deepcopy(G1["chans"]) + copy.deepcopy(G2["chans"]),
            "W": W, "K": K,
            "u0": list(G1["u0"]) + list(G2["u0"])}, (n1a, n1c, n2a, n2c)


def _longrange_chan(G, act_local):
    """Index of the coupled channel with largest tau*D (the 'w-like' one)."""
    W = np.asarray(G["W"], float); K = np.asarray(G["K"], float)
    best, bs = None, -1
    for c, ch in enumerate(G["chans"]):
        if abs(K[act_local, c]) > 1e-14:
            s = ch["tau"] * ch["D"]
            if s > bs:
                best, bs = c, s
    return best


def _slow_chan(G, act_local):
    """Index of the coupled channel with largest tau (the 'v-like' one)."""
    W = np.asarray(G["W"], float); K = np.asarray(G["K"], float)
    best, bs = None, -1
    for c, ch in enumerate(G["chans"]):
        if abs(K[act_local, c]) > 1e-14 and ch["tau"] > bs:
            best, bs = c, ch["tau"]
    return best


def _pid(G):
    pr = G.get("provenance", {})
    return pr.get("id", pr.get("ref", "?"))


def merge_share_chan(G1, G2, rng=None, rescale=None):
    """vvw-style: fuse the two parents' long-range channels into ONE shared
    channel. rescale=None keeps each parent's own drive weight (use when the
    parents are already 'half-drive species', e.g. certified iso wweight=0.5);
    rescale=0.5 halves both (turns two full-drive singles into the M3
    avg-drive convention — certified subtlety: this RELOCATES their islands)."""
    M, (n1a, n1c, n2a, n2c) = _block_merge(G1, G2)
    c1 = _longrange_chan(G1, 0)
    c2 = _longrange_chan(G2, 0)
    if c1 is None or c2 is None:
        return None, {"op": "merge_share_chan", "fail": "no_longrange_chan"}
    c2g = n1c + c2
    W, K = M["W"], M["K"]
    # shared channel params = parent1's copy (typically identical refs)
    # rewire: every act that pointed at c2g now points at c1 (same K weight)
    for a in range(n1a + n2a):
        if abs(K[a, c2g]) > 1e-14:
            K[a, c1] = K[a, c2g]
            K[a, c2g] = 0.0
    r = 1.0 if rescale is None else rescale
    newrow = np.zeros(n1a + n2a)
    newrow[:n1a] = r * W[c1, :n1a]
    newrow[n1a:] = r * W[c2g, n1a:]
    W[c1] = newrow
    # delete channel c2g
    keep = [c for c in range(W.shape[0]) if c != c2g]
    M["W"] = W[keep].tolist()
    M["K"] = K[:, keep].tolist()
    M["chans"] = [ch for i, ch in enumerate(M["chans"]) if i != c2g]
    M["provenance"] = {"op": "merge_share_chan", "parents": [_pid(G1), _pid(G2)],
                       "shared": int(c1), "rescale": rescale}
    return M, M["provenance"]


def merge_cross_edge(G1, G2, rng=None, eta=0.1, symmetric=True):
    """xv-style: private blocks + weak cross edge(s) on the slow channels."""
    M, (n1a, n1c, n2a, n2c) = _block_merge(G1, G2)
    c1 = _slow_chan(G1, 0)
    c2 = _slow_chan(G2, 0)
    if c1 is None or c2 is None:
        return None, {"op": "merge_cross_edge", "fail": "no_slow_chan"}
    W = M["W"]
    W[c1, n1a] = eta            # parent1's v driven by parent2's act 0
    if symmetric:
        W[n1c + c2, 0] = eta    # parent2's v driven by parent1's act 0
    M["W"] = np.asarray(W).tolist()
    M["K"] = np.asarray(M["K"]).tolist()
    M["provenance"] = {"op": "merge_cross_edge", "parents": [_pid(G1), _pid(G2)],
                       "eta": eta, "symmetric": symmetric}
    return M, M["provenance"]


def merge_slow_tanh(G1, G2, rng=None, tau_b=60.0, D_b=0.5, gamma=0.05,
                    kap=0.02, thr=0.5, sc=0.4):
    """bfield-style: new shared slow saturating channel coupling both blocks.
    thr sits above vacuum fluctuations -> only blob cores deposit."""
    M, (n1a, n1c, n2a, n2c) = _block_merge(G1, G2)
    W = np.asarray(M["W"], float); K = np.asarray(M["K"], float)
    nc = W.shape[0]
    Wn = np.zeros((nc + 1, W.shape[1])); Wn[:nc] = W
    Kn = np.zeros((K.shape[0], nc + 1)); Kn[:, :nc] = K
    Wn[nc, 0] = gamma
    Wn[nc, n1a] = gamma
    Kn[0, nc] = kap
    Kn[n1a, nc] = kap
    M["W"] = Wn.tolist(); M["K"] = Kn.tolist()
    M["chans"] = M["chans"] + [dict(tau=tau_b, D=D_b,
                                    g={"kind": "tanh", "thr": thr, "sc": sc})]
    M["provenance"] = {"op": "merge_slow_tanh", "parents": [_pid(G1), _pid(G2)],
                       "tau_b": tau_b, "D_b": D_b, "gamma": gamma, "kap": kap,
                       "thr": thr, "sc": sc}
    return M, M["provenance"]


MERGE_OPS = {"share_chan": merge_share_chan,
             "cross_edge": merge_cross_edge,
             "slow_tanh": merge_slow_tanh}
