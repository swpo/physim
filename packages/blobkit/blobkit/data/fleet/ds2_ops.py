"""ds2_ops.py — v2 operator alphabet (phase 6, takeaway T1: structural moves).

New ops on lib-format genomes (v1 ops REUSED from evolve/operators_lib.py):
  O1 mint_bilin : add ONE bilinear vertex [act i, chan c, chan c2, coef],
     coef ~ +-logU[0.1,1.5]; channel pick biased 60% to act i's own channels
     (W[c,i]!=0 or K[i,c]!=0), 40% fully random. delete_bilin removes one.
     PURE move: no other dial is touched -> child-parent deltas are causal.
  O2 add_chan  : append a fresh channel (tau~logU[0.5,300] — slow allowed,
     D~logU[0.01,30], g id .7|tanh .3) wired to ONE act (W=1,
     K=+-logU[0.05,1.5], sign + p .8). PURE move. Vacuum-exact by deviation
     form (x_new=0 at vacuum; no k1 refold needed).
  O3 dup_act   : duplicate species i with its channel wiring; mode "shared"
     (same channels — full niche overlap) or "split" (private copies of i's
     fast driven channels, slowest stays shared — the vvw construction).
     New act's dials jittered (speciation needs divergence).
VERTEX TRACKING: genome["vtags"] = list of string uids parallel to bilin.
  Sim/funnel ignore it; deepcopy keeps it; merges here concat+verify it.
  ensure_vtags() backfills founder tags on old genomes.
MERGE WRAPPER merge_v2: v1 merges + bilin-preservation assert (count & coef
  multiset) + vtag concat. v1 gate (share_chan remap) kept in gates_main.
"""
import copy
import numpy as np

import genome as G
import operators_lib as OP


def _logu(rng, a, b):
    return float(np.exp(rng.uniform(np.log(a), np.log(b))))


def _sgn(rng, p_pos=0.5):
    return 1.0 if rng.random() < p_pos else -1.0


# ---------------------------------------------------------------- vtags
def ensure_vtags(g, origin=None):
    """Backfill vtags parallel to bilin. Founder tags name the source genome."""
    bil = g.get("bilin", []) or []
    vt = list(g.get("vtags", []) or [])
    src = origin or g.get("id", "unk")
    while len(vt) < len(bil):
        vt.append(f"fdr_{src}_{len(vt)}")
    g["vtags"] = vt[:len(bil)]
    return g


def _own_chans(g, i):
    W = np.asarray(g["W"], float)
    K = np.asarray(g["K"], float)
    own = [c for c in range(len(g["chans"]))
           if W[c, i] != 0.0 or K[i, c] != 0.0]
    return own or list(range(len(g["chans"])))


# ---------------------------------------------------------------- O1 mint
def mint_bilin(g, rng, uid, tries=12):
    """Add one vertex. Returns (child, info) or (None, info)."""
    C = ensure_vtags(copy.deepcopy(g))
    na, nc = len(C["acts"]), len(C["chans"])
    if nc < 1:
        return None, dict(op="mint_bilin", fail="no_chans")
    have = {(b[0], min(b[1], b[2]), max(b[1], b[2])) for b in C["bilin"]}
    for _ in range(tries):
        i = int(rng.integers(na))
        if rng.random() < 0.6:
            pool = _own_chans(C, i)
            mode = "own"
        else:
            pool = list(range(nc))
            mode = "rand"
        c = int(pool[rng.integers(len(pool))])
        c2 = int(pool[rng.integers(len(pool))])
        if (i, min(c, c2), max(c, c2)) in have:
            continue
        coef = _sgn(rng) * _logu(rng, 0.1, 1.5)
        C["bilin"].append([i, c, c2, float(coef)])
        C["vtags"].append(uid)
        C["provenance"] = dict(kind="evolve_v2", op="mint_bilin",
                               parents=[g.get("id", "?")],
                               vertex=dict(uid=uid, i=i, c=c, c2=c2,
                                           coef=float(coef), bias=mode))
        return C, dict(op="mint_bilin", uid=uid, i=i, c=c, c2=c2,
                       coef=float(coef), bias=mode)
    return None, dict(op="mint_bilin", fail="no_free_slot")


def delete_bilin(g, rng):
    C = ensure_vtags(copy.deepcopy(g))
    if not C["bilin"]:
        return None, dict(op="delete_bilin", fail="no_vertex")
    j = int(rng.integers(len(C["bilin"])))
    gone = C["bilin"].pop(j)
    tag = C["vtags"].pop(j)
    C["provenance"] = dict(kind="evolve_v2", op="delete_bilin",
                           parents=[g.get("id", "?")],
                           removed=dict(uid=tag, term=gone))
    return C, dict(op="delete_bilin", uid=tag, term=gone)


# ---------------------------------------------------------------- O2 chan
def add_chan(g, rng, max_fields=14):
    C = ensure_vtags(copy.deepcopy(g))
    na, nc = len(C["acts"]), len(C["chans"])
    if na + nc + 1 > max_fields:
        return None, dict(op="add_chan", fail="field_cap")
    tau = _logu(rng, 0.5, 300.0)
    D = _logu(rng, 0.01, 30.0)
    if rng.random() < 0.3:
        ch = dict(tau=tau, D=D, g="tanh", thr=_logu(rng, 0.3, 1.2),
                  sc=_logu(rng, 0.2, 1.0))
    else:
        ch = dict(tau=tau, D=D, g="id", thr=0.0, sc=1.0)
    a = int(rng.integers(na))
    kval = _sgn(rng, 0.8) * _logu(rng, 0.05, 1.5)
    W = np.asarray(C["W"], float)
    K = np.asarray(C["K"], float)
    Wn = np.zeros((nc + 1, na)); Wn[:nc] = W; Wn[nc, a] = 1.0
    Kn = np.zeros((na, nc + 1)); Kn[:, :nc] = K; Kn[a, nc] = kval
    C["chans"].append(ch)
    C["W"], C["K"] = Wn.tolist(), Kn.tolist()
    C["provenance"] = dict(kind="evolve_v2", op="add_chan",
                           parents=[g.get("id", "?")],
                           chan=dict(**ch, act=a, K=float(kval)))
    return C, dict(op="add_chan", act=a, tau=tau, D=D, g=ch["g"],
                   K=float(kval))


# ---------------------------------------------------------------- O3 dup
def dup_act(g, rng, max_act=4, max_fields=14, sigma=0.15, sigma_d=0.4,
            mode=None, src=None):
    """Duplicate species. mode "shared": new act rides the SAME channels.
    mode "split": private jittered copies of its driven channels; the
    LONGEST-RANGE one (max tau*D — the mediator) stays shared (vvw topology).
    mode/src/sigma/sigma_d overridable for gates (sigma=sigma_d=0 => exact)."""
    C = ensure_vtags(copy.deepcopy(g))
    na, nc = len(C["acts"]), len(C["chans"])
    if na + 1 > max_act:
        return None, dict(op="dup_act", fail="act_cap")
    i = int(rng.integers(na)) if src is None else int(src)
    W = np.asarray(C["W"], float)
    K = np.asarray(C["K"], float)
    if mode is None:
        mode = "split" if rng.random() < 0.5 else "shared"
    driven = [c for c in range(nc) if W[c, i] != 0.0]
    # split: private copies of i's driven chans; max-range chan stays shared
    dup_cs = []
    if mode == "split" and len(driven) >= 2:
        keep = max(driven, key=lambda c: C["chans"][c]["tau"] * C["chans"][c]["D"])
        dup_cs = [c for c in driven if c != keep]
        if na + 1 + nc + len(dup_cs) > max_fields:
            dup_cs = []
    if not dup_cs:
        mode = "shared"
    if mode == "shared" and na + 1 + nc > max_fields:
        return None, dict(op="dup_act", fail="field_cap")
    j = na
    # new act = jittered copy of act i
    a = copy.deepcopy(C["acts"][i])
    lam_old = a["lam"]
    a["lam"] = max(float(a["lam"] * np.exp(sigma / 3 * rng.standard_normal())), 0.3)
    k1max_old = np.sqrt(4 * lam_old ** 3 / 27.0)
    r = a["k1"] / k1max_old if k1max_old > 0 else 0.0
    delta = max(1.0 - abs(r), 1e-4)
    delta = min(float(delta * np.exp(sigma_d * rng.standard_normal())), 0.9)
    k1max = np.sqrt(4 * a["lam"] ** 3 / 27.0)
    if r != 0:
        a["k1"] = float(np.sign(r) * (1.0 - delta) * k1max)
    a["Du"] = max(float(a["Du"] * np.exp(sigma * rng.standard_normal())), 0.05)
    rr = G.cubic_roots(a["lam"], a["k1"])
    if not rr:
        return None, dict(op="dup_act", fail="root_lost")
    a["u0"] = G.polish_root(a["lam"], a["k1"],
                            min(rr, key=lambda x: abs(x - a["u0"])))
    C["acts"].append(a)
    # wiring: new column in W, new row in K
    Wn = np.zeros((nc, na + 1)); Wn[:, :na] = W
    Kn = np.zeros((na + 1, nc)); Kn[:na] = K
    Wn[:, j] = W[:, i]
    Kn[j] = K[i]
    remap = {}
    chans_new, wrows, kcols = [], [], []
    for c in dup_cs:                      # private copies for the new act
        ch = copy.deepcopy(C["chans"][c])
        ch["tau"] = max(float(ch["tau"] * np.exp(sigma * rng.standard_normal())), 0.05)
        ch["D"] = max(float(ch["D"] * np.exp(sigma * rng.standard_normal())), 0.005)
        chans_new.append(ch)
        remap[c] = nc + len(chans_new) - 1
        wr = np.zeros(na + 1); wr[j] = W[c, i]
        wrows.append(wr)
        kc = np.zeros(na + 1); kc[j] = K[i, c]
        kcols.append(kc)
        Wn[c, j] = 0.0                    # detach new act from the originals
        Kn[j, c] = 0.0
    if chans_new:
        Wn = np.vstack([Wn] + [w[None, :] for w in wrows])
        Kn = np.hstack([Kn] + [k[:, None] for k in kcols])
        C["chans"] = C["chans"] + chans_new
    # bilin copies for the new act (remapped to private chans in split mode)
    newb, newt = [], []
    for b, tag in zip(list(C["bilin"]), list(C["vtags"])):
        if b[0] == i:
            newb.append([j, remap.get(b[1], b[1]), remap.get(b[2], b[2]), b[3]])
            newt.append(tag + "_d")
    C["bilin"] += newb
    C["vtags"] += newt
    C["W"], C["K"] = Wn.tolist(), Kn.tolist()
    C["provenance"] = dict(kind="evolve_v2", op="dup_act",
                           parents=[g.get("id", "?")], src_act=i, mode=mode,
                           dup_chans=dup_cs)
    return C, dict(op="dup_act", src_act=i, mode=mode, n_dup_chans=len(dup_cs),
                   n_dup_bilin=len(newb))


# ---------------------------------------------------------------- merges v2
def _coef_multiset(g):
    return sorted(round(float(b[3]), 12) for b in g.get("bilin", []))


def merge_v2(mode, g1, g2, rng=None, **kw):
    """v1 merge + vtag concat + bilin-preservation verification."""
    p1 = ensure_vtags(copy.deepcopy(g1))
    p2 = ensure_vtags(copy.deepcopy(g2))
    child, info = OP.MERGE_OPS[mode](p1, p2, rng=rng, **kw)
    if child is None:
        return None, info
    want = _coef_multiset(p1) + _coef_multiset(p2)
    got = _coef_multiset(child)
    if sorted(want) != got or len(child["bilin"]) != len(p1["bilin"]) + len(p2["bilin"]):
        return None, dict(op="merge_" + mode, fail="bilin_not_preserved",
                          want=want, got=got)
    child["vtags"] = list(p1["vtags"]) + list(p2["vtags"])
    probs = G.validate(child)
    if probs:
        return None, dict(op="merge_" + mode, fail="validate", probs=probs)
    return child, info


def mutate_v2(g, rng, **kw):
    """v1 kernel on a vtag-ensured copy; vtags ride through mutate's own
    deepcopy (v1 mutate never changes bilin count, only coefs)."""
    return OP.mutate(ensure_vtags(copy.deepcopy(g)), rng, **kw)
