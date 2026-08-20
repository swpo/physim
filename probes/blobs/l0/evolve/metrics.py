"""metrics.py — LOCKED assay battery + MAP-Elites descriptor (l0-evolver).

LOCKED 2026-02-19 BEFORE any certification battery / evolution run.
Screening doctrine: these are SCREENING metrics (T=400 tu pokes), not
certification. Published worlds get full-length certification separately.

Assays (IMEX-FFT dx=0.5 dt=0.02, L=64 unless noted; L=64 is the M2-audit
periodic-image-safe pair box):
  A1 poke  : Gaussian seed on act a (amp=2, sig=3, relaxed channels,
             kick_d=1.5px in -x) -> class in
             {die, static, travel, replicate, blowup}; c from last-half slope.
  A2 pair  : two symmetric pokes at d0 in {12, 16} (screening pair; full
             {8,12,16,20} for elites) -> {repel, bond(d*), merge, die,
             replicate, blowup}. bond: last-quarter sep std < 0.15 and
             3 < d* < 24; repel: sep_end > min(d0+6, 24); merge: ncomp 2->1.
  A3 dial  : tau of the slowest coupled channel * {0.8, 1.2} -> A1 travel
             flags -> motility class in
             {static, mobile, onset_up, onset_down, fragile}.
  osc      : late-half relative peak-amplitude std > 2% with a dominant
             FFT line -> period; else None.

Descriptor (MAP-Elites cell key):
  (n_act, n_chan, tails_osc, poke_sig, motility, bond_sig, osc)
  tails_osc = any act has G0c tail with wavelength in [3,30] and Re mu in
  [0.1,1.5] ("chemistry band"); poke_sig = "|".join(per-act A1 class);
  bond_sig = "|".join(per-d0 A2 class of the FIRST persistent act);
  osc = bool(period).
Cell quality (elite ranking within a cell): margin = -g0a_maxgrowth
(background stability margin; bigger = more robust world).

Thresholds LOCKED: c_thr=0.005 px/tu (travel), amp=2.0 sig=3.0 kick=1.5px,
T_poke=400, T_pair=600, sep plateau std 0.15, late window = last 25%%.

AMENDMENT v1.1 (2026-02-19, BEFORE any evolution/battery-certification data;
only 3 ref batteries existed, re-run after): added A4 CROSS assay for
n_act>=2 genomes — one poke per act pair (a0,a1) at d0=10 with kick (90,0.5)
on a0 -> class in {die, merge?, repel, cross_bond, rotor, drift}; rotor if
|revs| >= 0.75 in T=800 AND sep plateau; cross_bond if sep plateau w/o
rotation. Descriptor extended with cross_sig (n_act<2 -> "na"). Rationale:
merge research question is about cross-species physics; locking a battery
blind to it would make the comparison vacuous. c_thr/T/etc unchanged.

AMENDMENT v1.2 (2026-02-19, same sitting, still zero evolution rows) —
budget shortcuts that do NOT change any class definition:
  (i) battery skips A3 when the base poke class is 'travel' (motility_class
      is already fully determined = 'mobile'; dial info unused there);
 (ii) assay runs use engine stop_dead=True — early exit once every seeded
      act reports ncomp==0 on 3 consecutive records AND all u-fields are
      within 0.5*(thr-u0) of vacuum (world classifies 'die' either way;
      G0a-stable vacuum cannot re-nucleate from sub-threshold residue).
(iii) assay accounting for yield curves: n_assays = number of nonlinear
      sim runs consumed (A1 pokes + A2 pairs + A3 dial-pokes + A4); the
      shared currency with l0-sampler's curves.
FROZEN after this point.

AMENDMENT v1.3 (2026-02-19): l0-sampler landed lib/ (genome.py, funnel.py,
assays.py, their own LOCKED ../metrics.py) while this file's battery was
being validated. Per coordination mandate (do not fork the genome format),
EVOLUTION uses the sampler's lib battery verbatim (A1 panel bare/dressed0.6,
A2 {8,12,16,20}, A3 dial, their descriptor 8-tuple + shared archive.json),
plus THIS file's A4 cross assay ported to the lib stack in assays_x.py
(d0=10, T=800, L=64, per-act dressing = A1 winning variant, kick (90,0.5)
on the first act, same class thresholds: |revs|>=0.75 & sep_std<0.15 ->
rotor). This engine's A1-A3 (v1.2) remain the record for the val_gate and
battery_ref_v12 rows only; no evolution row uses them. Parity: ref_XV via
assays_x -> cls=rotor omega=-0.011063 sep=8.438 (certified -0.011067/8.439).
"""
import numpy as np
from engine import run, funnel_g0, genome_vacuum, min_image

C_THR = 0.005
T_POKE = 400.0
T_PAIR = 600.0
D0_SCREEN = (12.0, 16.0)
D0_FULL = (8.0, 12.0, 16.0, 20.0)


def _speed(pos_list, ts):
    """Late-half mean speed of blob 0 (unwrapped)."""
    n = len(pos_list)
    if n < 4:
        return None
    i0 = n // 2
    p0, p1 = pos_list[i0], pos_list[-1]
    if len(p0) == 0 or len(p1) == 0:
        return None
    dtu = ts[-1] - ts[i0]
    if dtu <= 0:
        return None
    return float(np.hypot(*(p1[0] - p0[0])) / dtu)


def _poke_class(r, act, n0=1):
    nc = r["ncomp"][act]
    if r["status"] == "blowup":
        return "blowup", None
    late = nc[len(nc) // 4:]
    if nc[-1] == 0:
        return "die", None
    if nc.max() > n0 and (late > n0).sum() >= 2:
        return "replicate", None
    c = _speed(r["pos"][act], r["t"])
    if c is None:
        return "die", None
    return ("travel" if c > C_THR else "static"), c


def _osc(r, act):
    pk = [p[0] if p else np.nan for p in r["peak"][act]]
    pk = np.array(pk, float)
    n = len(pk)
    seg = pk[n // 2:]
    seg = seg[np.isfinite(seg)]
    if len(seg) < 16:
        return None
    rel = seg.std() / max(abs(seg.mean()), 1e-9)
    if rel < 0.02:
        return None
    f = np.fft.rfft(seg - seg.mean())
    a = np.abs(f)
    if len(a) < 4:
        return None
    k = 1 + int(np.argmax(a[1:]))
    if a[k] < 3 * np.median(a[1:]):
        return None
    dt_rec = r["t"][1] - r["t"][0] if len(r["t"]) > 1 else 5.0
    period = len(seg) * dt_rec / k
    return float(period)


def a1_poke(G, act=0, L=64.0, T=T_POKE, kick=(0.0, 1.5), noise=0.0, seed=0):
    r = run(G, L=L, T=T, seeds=[(act, L / 2, L / 2, 2.0, 3.0)],
            kick=kick, noise=noise, seed=seed, stop_dead=True)
    cls, c = _poke_class(r, act)
    out = dict(cls=cls, c=c, act=act,
               area_end=(r["area"][act][-1][0] if r["area"][act] and r["area"][act][-1] else None),
               peak_end=(r["peak"][act][-1][0] if r["peak"][act] and r["peak"][act][-1] else None),
               period=_osc(r, act), wall_s=r["wall_s"])
    # cross-act leakage: any other act light up?
    out["others"] = [int(r["ncomp"][a][-1]) for a in range(len(G["acts"]))]
    return out


def a2_pair(G, act=0, d0=12.0, L=64.0, T=T_PAIR, seed=0):
    c0 = L / 2
    r = run(G, L=L, T=T,
            seeds=[(act, c0 - d0 / 2, c0, 2.0, 3.0), (act, c0 + d0 / 2, c0, 2.0, 3.0)],
            kick=None, noise=0.0, seed=seed, stop_dead=True)
    nc = r["ncomp"][act]
    if r["status"] == "blowup":
        return dict(cls="blowup", d0=d0)
    if nc[-1] == 0:
        return dict(cls="die", d0=d0)
    if nc.max() > 2:
        return dict(cls="replicate", d0=d0)
    if nc[-1] == 1:
        return dict(cls="merge", d0=d0)
    seps = []
    for p in r["pos"][act]:
        if len(p) == 2:
            seps.append(float(np.hypot(*min_image(p[1] - p[0], L))))
    if len(seps) < 8:
        return dict(cls="die", d0=d0)
    s = np.array(seps)
    tail = s[3 * len(s) // 4:]
    d_end = float(tail.mean())
    if d_end > min(d0 + 6.0, 24.0):
        return dict(cls="repel", d0=d0, sep_end=d_end)
    if tail.std() < 0.15 and 3.0 < d_end < 24.0:
        return dict(cls="bond", d0=d0, dstar=d_end, sep_std=float(tail.std()))
    return dict(cls="drift", d0=d0, sep_end=d_end, sep_std=float(tail.std()))


def _slowest_coupled_chan(G, act=0):
    W = np.asarray(G["W"], float); K = np.asarray(G["K"], float)
    best, bt = None, -1
    for c, ch in enumerate(G["chans"]):
        if abs(K[act, c]) > 1e-14 and abs(W[c, act]) > 1e-14 and ch["tau"] > bt:
            best, bt = c, ch["tau"]
    return best


def a3_dial(G, act=0, seed=0):
    import copy
    c = _slowest_coupled_chan(G, act)
    if c is None:
        return dict(cls="nochan")
    flags = {}
    for f in (0.8, 1.2):
        G2 = copy.deepcopy(G)
        G2["chans"][c]["tau"] *= f
        p = a1_poke(G2, act=act, seed=seed)
        flags[f] = p["cls"]
    return dict(cls_lo=flags[0.8], cls_hi=flags[1.2], chan=c)


def motility_class(base_cls, dial):
    if dial.get("cls") == "nochan":
        return "nochan"
    lo, hi = dial["cls_lo"], dial["cls_hi"]
    trav = {"travel"}
    bad = {"die", "replicate", "blowup"}
    if base_cls == "travel":
        return "mobile"
    if base_cls == "static":
        if hi in trav:
            return "onset_up"
        if lo in trav:
            return "onset_down"
        if lo in bad and hi in bad:
            return "fragile"
        return "static"
    return "na"


def a4_cross(G, a0=0, a1=1, d0=10.0, L=64.0, T=800.0, seed=0):
    """Cross-species encounter: poke a0 (kicked) + a1 at d0. LOCKED v1.1."""
    c0 = L / 2
    r = run(G, L=L, T=T,
            seeds=[(a0, c0 - d0 / 2, c0, 2.0, 3.0), (a1, c0 + d0 / 2, c0, 2.0, 3.0)],
            kick=(90.0, 0.5), noise=0.0, seed=seed, stop_dead=True)
    if r["status"] == "blowup":
        return dict(cls="blowup", pair=(a0, a1))
    nc0, nc1 = r["ncomp"][a0], r["ncomp"][a1]
    if nc0[-1] == 0 or nc1[-1] == 0:
        return dict(cls="die", pair=(a0, a1))
    if nc0.max() > 1 or nc1.max() > 1:
        return dict(cls="replicate", pair=(a0, a1))
    p0s, p1s, ts = [], [], []
    for i, t in enumerate(r["t"]):
        if len(r["pos"][a0][i]) == 1 and len(r["pos"][a1][i]) == 1:
            p0s.append(r["pos"][a0][i][0]); p1s.append(r["pos"][a1][i][0]); ts.append(t)
    if len(ts) < 12:
        return dict(cls="die", pair=(a0, a1))
    d = np.array([min_image(np.array(b) - np.array(a), L) for a, b in zip(p0s, p1s)])
    ang = np.unwrap(np.arctan2(d[:, 0], d[:, 1]))
    sep = np.hypot(d[:, 0], d[:, 1])
    n = len(ts); i0 = n // 2
    revs = float((ang[-1] - ang[0]) / (2 * np.pi))
    sep_m, sep_s = float(sep[i0:].mean()), float(sep[i0:].std())
    omega = float(np.polyfit(ts[i0:], ang[i0:], 1)[0])
    out = dict(pair=(a0, a1), revs=revs, omega=omega, sep_mean=sep_m,
               sep_std=sep_s, sep0=float(sep[0]))
    plateau = sep_s < 0.15 and 3.0 < sep_m < 24.0
    if abs(revs) >= 0.75 and plateau:
        out["cls"] = "rotor"
    elif plateau:
        out["cls"] = "cross_bond"
    elif sep_m > min(d0 + 6.0, 24.0):
        out["cls"] = "repel"
    else:
        out["cls"] = "drift"
    return out


def battery(G, full_pair=False, seed=0):
    """Full screening battery -> (descriptor, evidence). Skips A2/A3 if no
    act persists. Budget: 1-2 min for 1-2 act genomes."""
    ev = {}
    fun = funnel_g0(G)
    ev["funnel"] = fun
    if not (fun["g0a_pass"] and fun["g0b_pass"]):
        ev["reject"] = "funnel"
        return None, ev
    na = len(G["acts"])
    pokes = []
    for a in range(na):
        pokes.append(a1_poke(G, act=a, seed=seed))
    ev["a1"] = pokes
    poke_sig = "|".join(p["cls"] for p in pokes)
    persist = [a for a, p in enumerate(pokes) if p["cls"] in ("static", "travel")]
    tails = fun["g0c_tails"]
    tosc = any(t and t["wavelength"] and 3 <= t["wavelength"] <= 30
               and 0.1 <= t["re"] <= 1.5 for t in tails)
    if not persist:
        desc = (na, len(G["chans"]), tosc, poke_sig, "na", "na", "na", False)
        ev["descriptor"] = list(desc)
        return desc, ev
    a0 = persist[0]
    d0s = D0_FULL if full_pair else D0_SCREEN
    pair = [a2_pair(G, act=a0, d0=d, seed=seed) for d in d0s]
    ev["a2"] = pair
    bond_sig = "|".join(p["cls"] for p in pair)
    if pokes[a0]["cls"] == "travel":
        dial = None
        mot = "mobile"
    else:
        dial = a3_dial(G, act=a0, seed=seed)
        ev["a3"] = dial
        mot = motility_class(pokes[a0]["cls"], dial)
    osc = bool(pokes[a0]["period"])
    if len(persist) >= 2:
        cr = a4_cross(G, a0=persist[0], a1=persist[1], seed=seed)
        ev["a4"] = cr
        cross_sig = cr["cls"]
    else:
        cross_sig = "na"
    desc = (na, len(G["chans"]), tosc, poke_sig, mot, bond_sig, cross_sig, osc)
    ev["descriptor"] = list(desc)
    ev["margin"] = -fun["g0a_maxgrowth"]
    return desc, ev
