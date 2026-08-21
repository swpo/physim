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
BOND_DSTAR_MAX = 30.0  # px — V3: d*>30 = wrap/co-travel artifact, logged as bond_wrap_artifact
REPL_N = 4             # ncomp >= 4 => replicate (early exit)
A1_T = 300.0           # LOCKED in ../metrics.py
A2_T = 400.0
ASSAY_L = 64.0
POKE_AMP, POKE_SIG = 2.0, 3.0
REC = 5.0
WIN = 150.0


def _speed_and_pos(r, i, win=WIN):
    """(c_last, c_prev, pos): speeds over the last and the preceding win-tu
    windows (V3.1: c_prev enables the coast/steady discrimination)."""
    t = np.asarray(r["t"], float)
    pos, ts = [], []
    for k in range(len(t)):
        if r[f"ncomp{i}"][k] == 1 and len(r[f"pos{i}"][k]):
            pos.append(r[f"pos{i}"][k][0]); ts.append(t[k])
    if len(pos) < 4:
        return None, None, None
    pos = np.array(pos); ts = np.array(ts)
    def cfit(m):
        if m.sum() < 3:
            return None
        cy = np.polyfit(ts[m], pos[m, 0], 1)[0]
        cx = np.polyfit(ts[m], pos[m, 1], 1)[0]
        return float(np.hypot(cy, cx))
    c_last = cfit(ts >= ts[-1] - win)
    c_prev = cfit((ts >= ts[-1] - 2 * win) & (ts < ts[-1] - win))
    return c_last, c_prev, pos


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
    c, c_prev, _ = _speed_and_pos(r, i)
    a = [x[0] if len(x) else 0.0 for x in r[f"area{i}"]]
    pk = [x[0] if len(x) else 0.0 for x in r[f"peak{i}"]]
    extra = dict(area_end=float(a[-1]), peak_end=float(pk[-1]),
                 c=c, c_prev=c_prev, area_osc=_area_osc(r, i))
    if a[-1] >= DOMAIN_AREA:
        return "domain", extra      # spreading domain/labyrinth, not a blob
    if c is not None and c >= C_TRAVEL:
        # V3.1 steadiness gate: kicked ICs coast below onset (measured: below-
        # threshold M4 decays c 0.027->0.012->0.004; above locks). travel only
        # if speed is not collapsing across windows.
        if c_prev is None or c_prev < 1e-9 or c / c_prev >= STEADY_RATIO:
            return "travel", extra
        return "coast", extra       # decaying transient (kick relaxing back)
    return "persist", extra


def a1_poke(g, act, T=A1_T, dx=0.5, L=ASSAY_L, dress=0.0, kick_px=0.0):
    """One poke run. dress>0: identity channels driven by this act get a
    dress*W[c,act]-scaled copy of the u-bump (symmetric, kick_d=0) — the M1
    convention for taus where the bare u-poke dies (documented trap).
    kick_px>0 (V3.1): deterministic symmetry breaking so traveling regimes
    reveal themselves within T (BF5 lesson: symmetric states sit on the
    unstable symmetric branch). Dressed: channel bumps pasted displaced
    kick_px in -x (M1 kick convention). Bare: secondary u-bump amp 5% at
    +kick_px*2 in x."""
    N = int(round(L / dx))
    F = G.state_vacuum(g, N)
    F = G.poke(F, g, act, L / 2, L / 2, POKE_AMP, POKE_SIG, dx)
    if dress > 0:
        W = np.asarray(g["W"], float)
        na = len(g["acts"])
        cgrid = (np.arange(N) + 0.5) * dx
        dy = G.min_image(cgrid - L / 2, L)[:, None]
        dxx = G.min_image(cgrid - (L / 2 - kick_px), L)[None, :]
        bump = POKE_AMP * np.exp(-(dy ** 2 + dxx ** 2) / (2 * POKE_SIG ** 2))
        for c, ch in enumerate(g["chans"]):
            if ch["g"] == "id" and W[c, act] != 0.0:
                F[na + c] += dress * W[c, act] * bump
    elif kick_px > 0:
        F = G.poke(F, g, act, L / 2 + 2 * kick_px, L / 2,
                   0.05 * POKE_AMP, POKE_SIG, dx)
    r = G.run_genome(g, F=F, T=T, dx=dx, L=L, rec_tu=REC,
                     track_acts=[act], stop_explode_n=REPL_N)
    cls, extra = classify_a1(r, act)
    return dict(cls=cls, wall_s=round(r["wall_s"], 2), **extra)


A1_ORDER = {"travel": 0, "persist": 1, "coast": 2, "multi": 3, "domain": 4,
            "replicate": 5, "die": 6, "blowup": 7}


def a1_panel(g, act, T=A1_T, dx=0.5, L=ASSAY_L, kick_px=0.0):
    """LOCKED protocol: bare poke; if not alive-single, dressed poke (0.6).
    Returns best outcome (A1_ORDER) + which variant produced it. Rationale
    (measured 2026-02-19): bare u-poke dies for ALL certified tau=5.7 refs
    (M1 trap); dressed 0.6 revives all four refs; full dressing (1.0) kills
    even M0. Fixed panel = honest screening (same ICs for every candidate).
    kick_px used by the A3 ladder (V3.1) to break symmetry for drift detection."""
    r_bare = a1_poke(g, act, T=T, dx=dx, L=L, dress=0.0, kick_px=kick_px)
    r_bare["variant"] = "bare"
    if r_bare["cls"] in ("travel", "persist", "coast"):
        return r_bare
    r_dr = a1_poke(g, act, T=T, dx=dx, L=L, dress=0.6, kick_px=kick_px)
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
            # V3 wrap filter (stage-2 lock): co-traveling/scattered pairs on the
            # torus register huge stable seps (stage-1: d*=131.9 at d0=8).
            cls = "bond" if dstar <= BOND_DSTAR_MAX else "bond_wrap_artifact"
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


A3_LADDER = (0.01, 0.02, 0.05)   # V3: drift windows are +-1%-scale (M4: 2% wide)
A3_KICK_PX = 0.5                 # V3.1: ladder pokes carry a kd=0.5px kick (BF5
                                 # lesson: symmetric ICs mask traveling regimes)
STEADY_RATIO = 0.7               # V3.1: c_last/c_prev >= this => steady travel
A3_T = 400.0                     # V3.1: ladder pokes run longer (coast decays)


def a3_dial(g, act, T=A1_T):
    """V3 adaptive tau ladder (stage-2 lock; replaces the +-20% dial that found
    0 onsets in 200 stage-1 candidates). Walk tau of the heaviest id channel
    outward +-{1,2,5}% per side; stop a side early at the first class change
    (transition located). Plain tau dial (statics move too — coarse probe)."""
    import copy
    c = heaviest_id_channel(g, act)
    if c is None:
        return dict(cls="no_dial")
    out = dict(chan=c, tau0=g["chans"][c]["tau"], ladder=list(A3_LADDER))
    classes = {}
    for sgn, tag in ((-1, "minus"), (+1, "plus")):
        for rel in A3_LADDER:
            g2 = copy.deepcopy(g)
            g2["chans"][c]["tau"] *= (1.0 + sgn * rel)
            a1 = a1_panel(g2, act, T=A3_T, kick_px=A3_KICK_PX)
            key = f"{tag}{int(rel*100)}"
            classes[key] = a1["cls"]
            if a1["cls"] in ("travel", "coast"):
                out[f"c_{key}"] = a1.get("c")
            # V3.1 walk rule: continue through persist/coast (coast = near-onset
            # hint, keep climbing); stop the side on travel (onset FOUND) or on
            # hard failure (die/replicate/domain/multi/blowup = island edge).
            if a1["cls"] not in ("persist", "coast"):
                break
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
        act_probed = a3_rec.get("act", 0)
        base = a1_by_act.get(act_probed, {}).get("cls", "na")
        vals = set(cl.values())
        if "travel" in vals and base != "travel":
            mot = "onset"
        elif base == "travel":
            mot = "already"
        elif "coast" in vals:
            mot = "near_onset"      # V3.1: decaying kicked transient on ladder
        elif vals - {"persist"}:
            mot = "fragile"
        else:
            mot = "robust_static"
    return (n_act, n_id, n_tanh, int(osc), int(chem), poke, pair12, mot)


def fold_distances(g):
    """Per-act fold distance 1-|k1/k1max|, k1max=sqrt(4 lam^3/27) (V3 fix 5:
    logged for EVERY candidate — stage-1 hint: alive uniforms at 0.038 & 0.556,
    certified refs all at 0.027-0.03)."""
    out = []
    for a in g["acts"]:
        k1max = np.sqrt(4.0 * a["lam"] ** 3 / 27.0)
        out.append(float(1.0 - abs(a["k1"]) / k1max))
    return out


def shell_ratios(a2_recs, funnel_rec, act):
    """V3 fix 4: d*/wl_G0c per bond outcome (documented band ~[1.2,1.5] for the
    first shell — order-of-shell physics, not a tight constant; controller audit
    1.208-1.210 vs stage-1 batch 1.348+-0.075)."""
    tails = funnel_rec.get("g0c") or []
    wl = None
    if act < len(tails) and tails[act]:
        wl = tails[act].get("wavelength")
    if not wl:
        return []
    return [dict(d0=r["d0"], d_star=r.get("d_star"), ratio=r["d_star"] / wl)
            for r in a2_recs if r["cls"] == "bond" and r.get("d_star")]


def battery(g, funnel_rec, quick=False):
    """Full A1->A2->A3 battery. Returns (descriptor, records dict)."""
    recs = dict(a1={}, a2=[], a3=None)
    n_act = len(g["acts"])
    for i in range(n_act):
        recs["a1"][i] = a1_panel(g, i, T=A1_T if not quick else 200.0)
    # choose the best act for pair/dial probes: prefer travel > persist
    cand = [i for i in range(n_act)
            if recs["a1"][i]["cls"] in ("persist", "travel", "coast")]
    if cand:
        act = cand[0]
        dress = 0.6 if recs["a1"][act].get("variant") == "dressed0.6" else 0.0
        d0s = (12,) if quick else (8, 12, 16, 20)
        for d0 in d0s:
            recs["a2"].append(a2_pair(g, act, d0, dress=dress))
        recs["a3"] = a3_dial(g, act)
        recs["a3"]["act"] = act
    recs["fold_dist"] = fold_distances(g)
    if cand:
        recs["shell_ratios"] = shell_ratios(recs["a2"], funnel_rec, act)
    desc = descriptor(g, funnel_rec, recs["a1"], recs["a2"], recs["a3"])
    return desc, recs


# ------------------------------------------------------- V4 (stage-3) additions
def a2_cross(g, act_i, act_j, d0, T=A2_T, dx=0.5, L=ASSAY_L, dress=0.6):
    """Cross-species encounter: poke act_i at x1, act_j at x2 (d0 apart).
    Both dressed (symmetric channel shadows). Classes (V4):
      cross_bond(d*) | repel | approach | kill_i | kill_j | both_die |
      replicate | blowup | static.
    Flavor conservation checked via per-act ncomp (no conversion possible
    architecturally unless a dead act re-nucleates: logged as spawn_i/j)."""
    N = int(round(L / dx))
    F = G.state_vacuum(g, N)
    x1, x2 = L / 2 - d0 / 2, L / 2 + d0 / 2
    W = np.asarray(g["W"], float)
    na = len(g["acts"])
    for act, xx in ((act_i, x1), (act_j, x2)):
        F0 = F[act].copy()
        F = G.poke(F, g, act, xx, L / 2, POKE_AMP, POKE_SIG, dx)
        if dress > 0:
            bump = F[act] - F0
            for c, ch in enumerate(g["chans"]):
                if ch["g"] == "id" and W[c, act] != 0.0:
                    F[na + c] += dress * W[c, act] * bump
    r = G.run_genome(g, F=F, T=T, dx=dx, L=L, rec_tu=REC,
                     track_acts=[act_i, act_j], stop_explode_n=REPL_N,
                     ref_pos={act_i: [(x1, L / 2)], act_j: [(x2, L / 2)]})
    out = dict(d0=d0, act_i=act_i, act_j=act_j, status=r["status"],
               wall_s=round(r["wall_s"], 2))
    if r["status"] == "blowup":
        out["cls"] = "blowup"; return out
    if r["status"] == "replicated":
        out["cls"] = "replicate"; return out
    ni = r[f"ncomp{act_i}"]; nj = r[f"ncomp{act_j}"]
    ai, aj = int(ni[-1]), int(nj[-1])
    out["ncomp_end"] = [ai, aj]
    if ai == 0 and aj == 0:
        out["cls"] = "both_die"; return out
    if ai == 0:
        out["cls"] = "kill_i"; return out
    if aj == 0:
        out["cls"] = "kill_j"; return out
    if ai > 1 or aj > 1:
        out["cls"] = "replicate"; return out
    t = np.asarray(r["t"], float)
    seps, ts = [], []
    for k in range(len(t)):
        if ni[k] == 1 and nj[k] == 1 and len(r[f"pos{act_i}"][k]) and len(r[f"pos{act_j}"][k]):
            d = r[f"pos{act_i}"][k][0] - r[f"pos{act_j}"][k][0]
            seps.append(float(np.hypot(*d))); ts.append(t[k])
    if len(seps) < 5:
        out["cls"] = "odd"; return out
    seps = np.array(seps); ts = np.array(ts)
    m = ts >= ts[-1] - WIN
    rate = float(np.polyfit(ts[m], seps[m], 1)[0])
    dstar = float(seps[m].mean())
    moved = float(seps.max() - seps.min())
    out.update(d_star=dstar, sep_rate=rate, moved=moved, d_end=float(seps[-1]))
    if abs(rate) < SEP_RATE_EPS:
        if moved > 0.5 or abs(dstar - d0) > 0.3:
            out["cls"] = "cross_bond" if dstar <= BOND_DSTAR_MAX else "bond_wrap_artifact"
        else:
            out["cls"] = "static"
    elif rate > 0:
        out["cls"] = "repel"
    else:
        out["cls"] = "approach"
    return out


def stack_probe(g, act, n, spacing, T=2000.0, dx=0.5, L=96.0, dress=0.6,
                noise=0.0, seed=0):
    """V4 stack-safety probe (machine-v2 relevance): park an n-stack of act
    blobs at the given spacing along x, run T with NO kick, measure:
      ncomp trajectory (census integrity), per-blob unwrapped positions ->
      COM net displacement, max |single-blob drift|, spacing mean/std over
      the last 300tu. shuttle = |COM drift| > 2px or max blob drift > 4px.
    Classes: stack_parked | stack_shuttles | stack_collapsed(ncomp<n) |
    stack_replicates(ncomp>n) | die | blowup."""
    N = int(round(L / dx))
    F = G.state_vacuum(g, N)
    W = np.asarray(g["W"], float)
    na = len(g["acts"])
    x0 = L / 2 - spacing * (n - 1) / 2.0
    refs = []
    for j in range(n):
        xx = x0 + j * spacing
        F0 = F[act].copy()
        F = G.poke(F, g, act, xx, L / 2, POKE_AMP, POKE_SIG, dx)
        if dress > 0:
            bump = F[act] - F0
            for c, ch in enumerate(g["chans"]):
                if ch["g"] == "id" and W[c, act] != 0.0:
                    F[na + c] += dress * W[c, act] * bump
        refs.append((xx, L / 2))
    r = G.run_genome(g, F=F, T=T, dx=dx, L=L, rec_tu=10.0,
                     track_acts=[act], stop_explode_n=max(REPL_N, n + 2),
                     noise=noise, seed=seed, ref_pos={act: refs})
    nc = r[f"ncomp{act}"]
    out = dict(n=n, spacing=spacing, status=r["status"], T=T,
               wall_s=round(r["wall_s"], 2), ncomp_end=int(nc[-1]) if len(nc) else 0)
    if r["status"] == "blowup":
        out["cls"] = "blowup"; return out
    if len(nc) == 0 or nc[-1] == 0:
        out["cls"] = "die"; return out
    if nc[-1] < n:
        out["cls"] = "stack_collapsed"; return out
    if nc[-1] > n:
        out["cls"] = "stack_replicates"; return out
    t = np.asarray(r["t"], float)
    # records with full census
    P = [(tt, p) for tt, p, m in zip(t, r[f"pos{act}"], nc) if m == n and len(p) == n]
    if len(P) < 5:
        out["cls"] = "odd"; return out
    ts = np.array([x[0] for x in P])
    pos = np.array([x[1] for x in P])          # (nrec, n, 2) unwrapped [y,x]
    com = pos.mean(axis=1)
    com_net = float(np.hypot(*(com[-1] - com[0])))
    blob_net = [float(np.hypot(*(pos[-1, j] - pos[0, j]))) for j in range(n)]
    # spacing along the chain: consecutive x-sorted distances, last 300tu
    m = ts >= ts[-1] - 300.0
    sp_means, sp_stds = [], []
    for j in range(n - 1):
        d = np.hypot(pos[m, j + 1, 0] - pos[m, j, 0],
                     pos[m, j + 1, 1] - pos[m, j, 1])
        sp_means.append(float(d.mean())); sp_stds.append(float(d.std()))
    out.update(com_net=com_net, blob_net=blob_net,
               spacing_mean=sp_means, spacing_std=sp_stds)
    out["cls"] = ("stack_shuttles"
                  if (com_net > 2.0 or max(blob_net) > 4.0) else "stack_parked")
    return out


def radial_profile(g, act, T=400.0, dx=0.5, L=64.0, dress=0.6, variant=None):
    """V4 mechanism probe: relax a single blob, return the angle-averaged
    radial profile of (u-u0) and each channel deviation. Detects SIGN-CHANGING
    monotone tails (two-exponential mechanism: attraction without complex mu —
    G0c reports osc/mono but not tail-coefficient signs).
    Returns dict: r (px), u_prof, zero_crossings (radii where u-u0 changes
    sign outside the core), u_min_r/u_min_val (first minimum), cls of the run."""
    N = int(round(L / dx))
    F = G.state_vacuum(g, N)
    F0 = F[act].copy()
    F = G.poke(F, g, act, L / 2, L / 2, POKE_AMP, POKE_SIG, dx)
    use_dress = dress if variant == "dressed" else 0.0
    if use_dress > 0:
        W = np.asarray(g["W"], float)
        na = len(g["acts"])
        bump = F[act] - F0
        for c, ch in enumerate(g["chans"]):
            if ch["g"] == "id" and W[c, act] != 0.0:
                F[na + c] += use_dress * W[c, act] * bump
    r = G.run_genome(g, F=F, T=T, dx=dx, L=L, rec_tu=T, track_acts=[act],
                     stop_explode_n=REPL_N, save_fields=True)
    cls, extra = classify_a1(r, act)
    out = dict(cls=cls, variant=variant or "bare")
    if r["fields"] is None or cls in ("die", "blowup", "replicate"):
        return out
    u0 = g["acts"][act]["u0"]
    dev = r["fields"][act] - u0
    c = (np.arange(N) + 0.5) * dx
    dy = G.min_image(c - L / 2, L)[:, None]
    dxx = G.min_image(c - L / 2, L)[None, :]
    rr = np.hypot(dy, dxx)
    rbins = np.arange(0.0, L / 2, dx)
    prof = np.zeros(len(rbins) - 1)
    for k in range(len(rbins) - 1):
        m = (rr >= rbins[k]) & (rr < rbins[k + 1])
        prof[k] = dev[m].mean() if m.any() else np.nan
    rc = 0.5 * (rbins[:-1] + rbins[1:])
    # zero crossings outside the core (start after the peak)
    ipk = int(np.nanargmax(prof))
    zc = []
    for k in range(ipk + 1, len(prof) - 1):
        if np.isfinite(prof[k]) and np.isfinite(prof[k + 1]) and prof[k] * prof[k + 1] < 0:
            zc.append(float(rc[k]))
    # first minimum beyond first zero crossing
    umin_r, umin_v = None, None
    if zc:
        k0 = int(np.searchsorted(rc, zc[0]))
        if k0 < len(prof) - 2:
            seg = prof[k0:]
            j = int(np.nanargmin(seg))
            umin_r, umin_v = float(rc[k0 + j]), float(seg[j])
    out.update(r=rc.tolist(), u_prof=[float(x) for x in prof],
               zero_crossings=zc, u_min_r=umin_r, u_min_val=umin_v,
               area_end=extra.get("area_end"))
    return out
