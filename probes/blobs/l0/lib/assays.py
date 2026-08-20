"""lib/assays.py — nonlinear assay battery A1/A2/A3 -> behavior descriptor.

Blob existence is SUBCRITICAL/homoclinic: linear screens cannot see blobs, so
probes are mandatory. All assays run IMEX-FFT dx=0.5 dt=0.02 L=96 (program conv).

A1 POKE (per act): vacuum + Gaussian poke (amp=2 sig=3) on act i at center.
   T=400, rec 5. Classes:
     die        ncomp_i -> 0
     persist    ncomp_i==1 at end, |c| < C_TRAVEL
     travel     ncomp_i==1 at end, |c| >= C_TRAVEL (speed from last 150 tu)
     replicate  ncomp_i >= REPL_N (early exit)
     blowup     non-finite fields
   Multi-act genomes: poke each act separately (lone-species behavior), plus
   an all-acts-poked run for interaction censoring.
   Outputs per act: class, area_end, peak_end, c, area_osc (breathing amplitude
   ratio over last 150 tu), t_settle.

A2 PAIR (only if A1 gives a persist/travel act): two pokes of the SAME act at
   d0 in {8,12,16,20} along x. T=600. Classes per d0: merge (ncomp 2->1),
   repel (d grows monotonically > d0+2 and keeps growing at end),
   bond (d converges: |d(T)-d(T-150)| < 0.05 and d stable), die, replicate.
   d* = final separation for bond class. Compare d* (and consecutive-shell
   spacing if two d0 lock at different shells) to G0c predicted wavelength.

A3 DIAL (only for A1-persist acts): tau of the HEAVIEST identity channel
   (largest tau among g="id" channels driving that act) +-20%. Re-run A1 poke.
   Outcomes: motility onset (persist->travel either direction), death, replication,
   nothing. Records (class_minus, class_0, class_plus) -> "drift-family" flag if
   any transition to travel.

BEHAVIOR DESCRIPTOR (MAP-Elites cell key):
   (n_act, n_chan_id, n_chan_tanh, tails_osc?, chem_box?, poke_class_joined,
    pair_class@12, motility_flag)
"""
import numpy as np

import genome as G

C_TRAVEL = 0.01        # px/tu — above M4 translation-lock noise 1e-4 x100
SEP_RATE_EPS = 0.002   # px/tu — pair separation 'settled' threshold
DOMAIN_AREA = 150.0    # px^2 — 'persist' above this = spreading domain (labyrinth caveat class)
REPL_N = 4             # ncomp >= 4 => replicate (early exit)
A1_T = 300.0           # LOCKED in ../metrics.py
A2_T = 400.0
ASSAY_L = 64.0
POKE_AMP, POKE_SIG = 2.0, 3.0
REC = 5.0
WIN = 150.0


def _speed_and_pos(r, i, win=WIN):
    t = np.asarray(r["t"], float)
    pos, ts = [], []
    for k in range(len(t)):
        if r[f"ncomp{i}"][k] == 1 and len(r[f"pos{i}"][k]):
            pos.append(r[f"pos{i}"][k][0]); ts.append(t[k])
    if len(pos) < 4:
        return None, None
    pos = np.array(pos); ts = np.array(ts)
    m = ts >= ts[-1] - win
    if m.sum() < 3:
        return None, None
    cy = np.polyfit(ts[m], pos[m, 0], 1)[0]
    cx = np.polyfit(ts[m], pos[m, 1], 1)[0]
    return float(np.hypot(cy, cx)), pos


def _area_osc(r, i, win=WIN):
    t = np.asarray(r["t"], float)
    a = np.array([x[0] if len(x) else 0.0 for x in r[f"area{i}"]])
    m = (t >= t[-1] - win) & (a > 0)
    if m.sum() < 3:
        return None
    aa = a[m]
    return float((aa.max() - aa.min()) / max(aa.mean(), 1e-9))


def classify_a1(r, i):
    nc = r[f"ncomp{i}"]
    if r["status"] == "blowup":
        return "blowup", {}
    if r["status"] == "replicated" or (len(nc) and nc[-1] >= REPL_N):
        return "replicate", {}
    if r["status"] == "died" or (len(nc) and nc[-1] == 0):
        return "die", {}
    if nc[-1] > 1:
        return "multi", {}       # settled 2-3 spots (splitting w/o cascade)
    c, _ = _speed_and_pos(r, i)
    a = [x[0] if len(x) else 0.0 for x in r[f"area{i}"]]
    pk = [x[0] if len(x) else 0.0 for x in r[f"peak{i}"]]
    extra = dict(area_end=float(a[-1]), peak_end=float(pk[-1]),
                 c=c, area_osc=_area_osc(r, i))
    if a[-1] >= DOMAIN_AREA:
        return "domain", extra      # spreading domain/labyrinth, not a blob
    if c is not None and c >= C_TRAVEL:
        return "travel", extra
    return "persist", extra


def a1_poke(g, act, T=A1_T, dx=0.5, L=ASSAY_L, dress=0.0):
    """One poke run. dress>0: identity channels driven by this act get a
    dress*W[c,act]-scaled copy of the u-bump (symmetric, kick_d=0) — the M1
    convention for taus where the bare u-poke dies (documented trap)."""
    N = int(round(L / dx))
    F = G.state_vacuum(g, N)
    F = G.poke(F, g, act, L / 2, L / 2, POKE_AMP, POKE_SIG, dx)
    if dress > 0:
        W = np.asarray(g["W"], float)
        bump = F[act] - g["acts"][act]["u0"]
        na = len(g["acts"])
        for c, ch in enumerate(g["chans"]):
            if ch["g"] == "id" and W[c, act] != 0.0:
                F[na + c] += dress * W[c, act] * bump
    r = G.run_genome(g, F=F, T=T, dx=dx, L=L, rec_tu=REC,
                     track_acts=[act], stop_explode_n=REPL_N)
    cls, extra = classify_a1(r, act)
    return dict(cls=cls, wall_s=round(r["wall_s"], 2), **extra)


A1_ORDER = {"travel": 0, "persist": 1, "multi": 2, "domain": 3,
            "replicate": 4, "die": 5, "blowup": 6}


def a1_panel(g, act, T=A1_T, dx=0.5, L=ASSAY_L):
    """LOCKED protocol: bare poke; if not alive-single, dressed poke (0.6).
    Returns best outcome (A1_ORDER) + which variant produced it. Rationale
    (measured 2026-02-19): bare u-poke dies for ALL certified tau=5.7 refs
    (M1 trap); dressed 0.6 revives all four refs; full dressing (1.0) kills
    even M0. Fixed panel = honest screening (same ICs for every candidate)."""
    r_bare = a1_poke(g, act, T=T, dx=dx, L=L, dress=0.0)
    r_bare["variant"] = "bare"
    if r_bare["cls"] in ("travel", "persist"):
        return r_bare
    r_dr = a1_poke(g, act, T=T, dx=dx, L=L, dress=0.6)
    r_dr["variant"] = "dressed0.6"
    best = min((r_bare, r_dr), key=lambda r: A1_ORDER.get(r["cls"], 9))
    best["bare_cls"] = r_bare["cls"]
    return best


def a2_pair(g, act, d0, T=A2_T, dx=0.5, L=ASSAY_L, dress=0.0):
    N = int(round(L / dx))
    F = G.state_vacuum(g, N)
    x1, x2 = L / 2 - d0 / 2, L / 2 + d0 / 2
    F0 = F[act].copy()
    F = G.poke(F, g, act, x1, L / 2, POKE_AMP, POKE_SIG, dx)
    F = G.poke(F, g, act, x2, L / 2, POKE_AMP, POKE_SIG, dx)
    if dress > 0:
        W = np.asarray(g["W"], float)
        bump = F[act] - F0
        na = len(g["acts"])
        for c, ch in enumerate(g["chans"]):
            if ch["g"] == "id" and W[c, act] != 0.0:
                F[na + c] += dress * W[c, act] * bump
    r = G.run_genome(g, F=F, T=T, dx=dx, L=L, rec_tu=REC,
                     track_acts=[act], stop_explode_n=REPL_N,
                     ref_pos={act: [(x1, L / 2), (x2, L / 2)]})
    nc = r[f"ncomp{act}"]
    if r["status"] == "blowup":
        return dict(cls="blowup", d0=d0)
    if r["status"] == "replicated":
        return dict(cls="replicate", d0=d0)
    if r["status"] == "died" or nc[-1] == 0:
        return dict(cls="die", d0=d0)
    if nc[-1] == 1:
        return dict(cls="merge", d0=d0, wall_s=round(r["wall_s"], 2))
    # separation series over records with ncomp==2
    t = np.asarray(r["t"], float)
    seps, ts = [], []
    for k in range(len(t)):
        if nc[k] == 2 and len(r[f"pos{act}"][k]) == 2:
            d = r[f"pos{act}"][k][0] - r[f"pos{act}"][k][1]
            seps.append(float(np.hypot(*d))); ts.append(t[k])
    if len(seps) < 5:
        return dict(cls="odd", d0=d0)
    seps = np.array(seps); ts = np.array(ts)
    m = ts >= ts[-1] - WIN
    rate = float(np.polyfit(ts[m], seps[m], 1)[0])       # px/tu, last window
    dstar = float(seps[m].mean())
    moved = float(seps.max() - seps.min())
    if abs(rate) < SEP_RATE_EPS:
        if moved > 0.5 or abs(dstar - d0) > 0.3:
            cls = "bond"          # converged to a preferred separation != d0
        else:
            cls = "static"        # never moved: neutral or pinned
    elif rate > 0:
        cls = "repel"             # still separating at end
    else:
        cls = "approach"          # still closing at end (slow merge/bond)
    return dict(cls=cls, d0=d0, d_star=dstar, d_end=float(seps[-1]),
                sep_rate=rate, moved=moved, wall_s=round(r["wall_s"], 2))


def heaviest_id_channel(g, act):
    """Largest-tau identity channel with W[c,act]!=0 (the 'slow inhibitor')."""
    W = np.asarray(g["W"], float)
    best, bc = None, None
    for c, ch in enumerate(g["chans"]):
        if ch["g"] == "id" and W[c, act] != 0.0:
            if best is None or ch["tau"] > best:
                best, bc = ch["tau"], c
    return bc


def a3_dial(g, act, rel=0.2, T=A1_T):
    import copy
    c = heaviest_id_channel(g, act)
    if c is None:
        return dict(cls="no_dial")
    out = dict(chan=c, tau0=g["chans"][c]["tau"])
    classes = {}
    for tag, f in (("minus", 1 - rel), ("plus", 1 + rel)):
        g2 = copy.deepcopy(g)
        g2["chans"][c]["tau"] *= f
        # A=tau*D fixed? NO — plain tau dial (M4 lesson: statics change too; this
        # is a coarse motility probe, not a controlled-statics dial).
        a1 = a1_panel(g2, act, T=T)
        classes[tag] = a1["cls"]
        if a1["cls"] == "travel":
            out[f"c_{tag}"] = a1.get("c")
    out["classes"] = classes
    return out


def descriptor(g, funnel_rec, a1_by_act, a2_recs, a3_rec):
    n_act = len(g["acts"])
    n_id = sum(1 for c in g["chans"] if c["g"] == "id")
    n_tanh = len(g["chans"]) - n_id
    osc = bool(funnel_rec.get("g0c_any_osc"))
    chem = bool(funnel_rec.get("g0c_any_chem"))
    poke = "|".join(a1_by_act[i]["cls"] for i in sorted(a1_by_act))
    pair12 = next((r["cls"] for r in a2_recs if r["d0"] == 12), "na")
    mot = "na"
    if a3_rec and "classes" in a3_rec:
        cl = a3_rec["classes"]
        base = next((a1_by_act[i]["cls"] for i in sorted(a1_by_act)), "na")
        vals = set(cl.values())
        if "travel" in vals and base != "travel":
            mot = "onset"
        elif base == "travel":
            mot = "already"
        elif vals - {base}:
            mot = "fragile"
        else:
            mot = "robust_static"
    return (n_act, n_id, n_tanh, int(osc), int(chem), poke, pair12, mot)


def battery(g, funnel_rec, quick=False):
    """Full A1->A2->A3 battery. Returns (descriptor, records dict)."""
    recs = dict(a1={}, a2=[], a3=None)
    n_act = len(g["acts"])
    for i in range(n_act):
        recs["a1"][i] = a1_panel(g, i, T=A1_T if not quick else 200.0)
    # choose the best act for pair/dial probes: prefer travel > persist
    cand = [i for i in range(n_act) if recs["a1"][i]["cls"] in ("persist", "travel")]
    if cand:
        act = cand[0]
        dress = 0.6 if recs["a1"][act].get("variant") == "dressed0.6" else 0.0
        d0s = (12,) if quick else (8, 12, 16, 20)
        for d0 in d0s:
            recs["a2"].append(a2_pair(g, act, d0, dress=dress))
        recs["a3"] = a3_dial(g, act)
        recs["a3"]["act"] = act
    desc = descriptor(g, funnel_rec, recs["a1"], recs["a2"], recs["a3"])
    return desc, recs
