"""gates -- the card's derived numbers, declared thresholds and verdicts (round 6, study cards).

Committed BEFORE the GPU run (HYPOTHESES.md gives the reasons). The thresholds were chosen after CPU runs at small
size of three worlds (foundry draw 4470, the pure-noise field, the non-interacting bodies) and before any full-size
card existed. numpy only; input = the JSON card of cardlib.analyse (after cardlib.strip).

TYPICAL STATE. Every ratio below is built from the MEDIANS over the test states of the per-state variances
(cardlib's *_med entries): in the CPU run of foundry draw 4470 one member of eight held a runaway body, sat seven
standard deviations from the climatology and carried the means. The mean-based values are kept with the suffix
_mean for h = 8; a world where the two differ is flagged in the tables.
THE CHEAP FAMILY is {climatology, persistence, the ridge}: ceilings use the best of the three (round 5 used the
ridge or climatology; the ridge extrapolates badly for a member far from the fit members).

Derived numbers per full level L in (grid, pop), horizons h in ticks:
  pf(h), ceil(h), gap(h)      predictable fraction, closure ceiling of the cheap family, closure gap
  w_theta(h)                  PL(eps = 1, h) / (V_clim - V_orc)(h): the share of the predictable variance that a
                              prior-sized error in the hidden part costs, given the state
  sigma_hat                   mean over h in (4, 8, 16) of min(clip(w_theta), clip(1 - ceil)): the card's screen for
                              the science share. A policy that simulates the public prior cannot lose more than
                              w_theta; a data-only fit of the level cannot lose more than 1 - ceil (the cheap
                              family is a lower bound on what a fit can do), and the null policy is the better of
                              the two. An upper screen: history that identifies the hidden part lowers the real share
  pl_ratio(eps, 8)            PL(eps, 8) / V_orc(8) for eps = 0.03 and 0.1 (round 5's screen)
  evidence(eps)               d * PL(eps, 1) / (2 V_orc(1)) nats per tick and member that one tick of the level
                              gives about a move of eps of the prior (Gaussian, independent-numbers approximation;
                              an index, not a certificate); ticks_to_3nats = 3 / evidence
  act_ms                      MS(aimed, 200 nats, h = 4) / V_orc(4): the loss of an input-blind oracle, in the
                              program's unit; aim_ratio = D(aimed) / D(blind) at h = 4
  xresp                       RD(4) / V_orc(4): how much the response to the aimed 200-nat input changes when the
                              hidden part moves by the prior (would an experiment tell the worlds apart)
Gates (all thresholds in TH):
  exam_worthy     some full level has pf(8) >= PF_MIN and sigma_hat >= SIGMA_HAT_MIN
  structure       NB_MIN <= bodies, slots rarely full, half-life >= HALF_LIFE_MIN ticks, and the bodies move
                  (net speed >= V_NET_MIN px per tick) or have events (>= EVENTS_MIN fusions + fissions per 100 ticks)
  interaction     on quiet steps the displacement of a body over 8 ticks is predictable (pf >= BODY_PF_MIN) and the
                  single-body law leaves at least 10% of it (ceiling <= BODY_CEIL_MAX)
  reading_worthy  structure and interaction
  actions         act_ms >= ACT_MS_MIN at the grid or the population level
  stationary      tick share <= TICK_SHARE_MAX and member share <= MEMBER_SHARE_MAX at the grid level (the late
                  window is compared separately, see late_vs_early)
  levels_add      the slot list improves the block view's cheap prediction at 8 ticks by >= CROSS_GAIN_MIN of the
                  variance, or the population level has pf(8) >= PF_MIN with a closure gap >= GAP_MIN
  learned_differs slow features of the fine view beat the hand block view by >= LEARNED_DCEIL_MIN in ceiling at
                  8 ticks in both orders of the halves, and are not the hand view (min R^2 < 0.9)
Verdict: 'dull: nothing predictable' (max pf(8) < PF_NOISE), 'dull: predictable by the cheap family' (no level
with a closure gap >= GAP_MIN at 8 ticks), 'dull: the hidden part has no weight' (closure gap but sigma_hat below
the bar), else 'exam-worthy' with '+ reading-worthy', '+ actions' appended when those gates pass.
A world of the CONTROL family that does not come out dull refutes the card.
"""
from __future__ import annotations

import numpy as np

H_MID = (4, 8, 16)
TH = dict(PF_MIN=0.3, PF_NOISE=0.1, GAP_MIN=0.05, SIGMA_HAT_MIN=0.15, NB_MIN=2.0, SLOTS_FULL_MAX=0.05,
          HALF_LIFE_MIN=16.0, V_NET_MIN=0.05, EVENTS_MIN=2.0, BODY_PF_MIN=0.3, BODY_CEIL_MAX=0.9, ACT_MS_MIN=0.1,
          TICK_SHARE_MAX=0.1, MEMBER_SHARE_MAX=0.3, CROSS_GAIN_MIN=0.02, LEARNED_DCEIL_MIN=0.05, LEARNED_R2_MAX=0.9,
          LATE_DMEAN_MAX=0.5, LATE_LOGSD_MAX=0.35, LATE_COUNT_LO=0.67, LATE_COUNT_HI=1.5, LATE_SIGMA_HAT=0.1,
          ROBUST_ABS=0.05, ROBUST_REL=0.25)
LEVELS = ("grid", "pop")


def _f(x):
    return float("nan") if x is None else float(x)


def _at(lst, hz, h):
    return _f(lst[list(hz).index(h)]) if (lst is not None and h in hz) else float("nan")


def _level(card, L):
    if L == "grid":
        return card["grid"]
    p = card["pop"]
    if p.get("empty"):
        return None
    out = dict(p["lin"])
    out.update(hz=p["hz"], pl=p["pl"], act=p["act"], xresp=p["xresp"], tick_share=p["tick_share"],
               member_share=p.get("member_share"), d=int(np.sum(p["live"])))
    return out


def derive(card: dict) -> dict:
    d = {}
    for L in LEVELS:
        lv = _level(card, L)
        if lv is None:
            continue
        hz = lv["hz"]
        vc, vo = np.array(lv["v_clim_med"], float), np.array(lv["v_orc_med"], float)
        ceil = np.array([_f(v) for v in lv["ceil_med"]])
        pred = vc - vo
        for h in hz:
            i = hz.index(h)
            d[f"{L}.pf{h}"] = _f(lv["pf_med"][i])
            d[f"{L}.ceil{h}"] = ceil[i]
            d[f"{L}.gap{h}"] = _f(lv["gap_med"][i])
        for k in ("pf", "ceil", "gap", "ceil_raw"):
            d[f"{L}.{k}8_mean"] = _at(lv[k], hz, 8)
        d[f"{L}.ceil8_se"] = _at(lv.get("ceil_med_se"), hz, 8)
        d[f"{L}.pf8_se"] = _at(lv.get("pf_med_se"), hz, 8)
        pl1 = np.array(lv["pl"]["1.0"]["pl_med"], float) if "1.0" in lv["pl"] else np.full(len(hz), np.nan)
        with np.errstate(divide="ignore", invalid="ignore"):
            w = np.where(pred > 1e-9, pl1 / pred, np.nan)
        sh = []
        for h in H_MID:
            if h in hz:
                i = hz.index(h)
                d[f"{L}.w_theta{h}"] = float(w[i])
                sh.append(min(np.clip(w[i], 0, 1), np.clip(1 - ceil[i], 0, 1)) if np.isfinite(w[i]) and np.isfinite(ceil[i]) else np.nan)
        d[f"{L}.sigma_hat"] = float(np.nanmean(sh)) if np.isfinite(sh).any() else float("nan")
        nd = int(lv.get("d") or (len(card["grid"]["mean"]) * card["grid_shape"][0] * card["grid_shape"][1] if L == "grid" else 1))
        for e in ("0.03", "0.1", "1.0"):
            if e in lv["pl"]:
                d[f"{L}.pl_ratio{e}_8"] = _at(lv["pl"][e]["pl_over_vorc_med"], hz, 8)
                d[f"{L}.pl_ratio{e}_8_mean"] = _at(lv["pl"][e]["pl_over_vorc"], hz, 8)
                ev = nd * _at(lv["pl"][e]["pl_med"], hz, 1) / max(2.0 * _at(lv["v_orc_med"], hz, 1), 1e-12)
                d[f"{L}.evidence{e}"] = float(ev)
                d[f"{L}.ticks_to_3nats{e}"] = float(3.0 / ev) if ev > 0 else float("inf")
        a = lv["act"]
        if "aimed_200" in a:
            d[f"{L}.act_ms"] = _at(a["aimed_200"]["MS_over_vorc_med"], hz, 4)
            d[f"{L}.act_ms_mean"] = _at(a["aimed_200"]["MS_over_vorc"], hz, 4)
            d[f"{L}.act_D_floor"] = _at(a["aimed_200"]["D_over_floor"], hz, 4)
            if "blind_200" in a:
                d[f"{L}.aim_ratio"] = _at(a["aimed_200"]["D_med"], hz, 4) / max(_at(a["blind_200"]["D_med"], hz, 4), 1e-12)
            for n in ("aimed_50", "aimed_800"):
                if n in a:
                    d[f"{L}.act_ms_{n[6:]}"] = _at(a[n]["MS_over_vorc_med"], hz, 4)
        d[f"{L}.xresp"] = _at(lv["xresp"]["RD_over_vorc_med"], hz, 4)
        d[f"{L}.tick_share"] = _f(lv.get("tick_share"))
        d[f"{L}.member_share"] = _f(lv.get("member_share"))
    s = card["structure"]
    for k in ("nb_mean", "nb_std", "body_frac", "rg", "v_net", "half_life_ticks", "events100", "births100", "deaths100",
              "slots_full_share", "wavelength_px", "cv_cell", "moved", "events100_per_body", "body_speed_len"):
        d["s." + k] = _f(s.get(k))
    b = card["bodies"]
    hz = b["hz"]
    for part in ("disp", "mass"):
        d[f"b.pf_{part}8"] = _at(b["single"][part]["pf_med"], hz, 8)
        d[f"b.ceil_{part}8"] = _at(b["single"][part]["ceil_med"], hz, 8)
        d[f"b.ceil_{part}8_mean"] = _at(b["single"][part]["ceil"], hz, 8)
        d[f"b.ceil_pers_{part}8"] = _at(b["single"][part]["ceil_pers_med"], hz, 8)
        if "field" in b:
            d[f"b.ceil_field_{part}8"] = _at(b["field"][part]["ceil_med"], hz, 8)
        for h in (1, 4, 16):
            d[f"b.ceil_{part}{h}"] = _at(b["single"][part]["ceil_med"], hz, h)
    d["b.quiet8"] = _at(b["quiet_share"], hz, 8)
    d["b.n_test8"] = _f(b["n_rows_fit_test"][hz.index(8)][1]) if 8 in hz else float("nan")
    c = card["cross"]
    d["x.bodies_to_grid8"] = _at(c["bodies_to_grid"]["gain"], hz, 8)
    d["x.grid_to_bodies8"] = _at(c["grid_to_bodies"]["gain"], hz, 8)
    if "grid_to_pop" in c:
        d["x.grid_to_pop8"] = _at(c["grid_to_pop"]["gain"], hz, 8)
        d["x.pop_over_pers8"] = _at(c["pop_over_persistence"]["gain"], hz, 8)
    if "learned" in card:
        le = card["learned"]
        dc = [_at(le[t]["learned"]["ceil_med"], hz, 8) - _at(le[t]["hand"]["ceil_med"], hz, 8) for t in ("AB", "BA")]
        dp = [_at(le[t]["learned"]["pf_med"], hz, 8) - _at(le[t]["hand"]["pf_med"], hz, 8) for t in ("AB", "BA")]
        dg = [_at(le[t]["learned"]["gap_med"], hz, 8) - _at(le[t]["hand"]["gap_med"], hz, 8) for t in ("AB", "BA")]
        d["l.dceil8_AB"], d["l.dceil8_BA"] = dc
        d["l.dpf8_AB"], d["l.dpf8_BA"] = dp
        d["l.dgap8_AB"], d["l.dgap8_BA"] = dg
        d["l.r2_min"] = float(min(min(le[t]["r2_on_hand"]) for t in ("AB", "BA")))
        for h in (16, 32):
            d[f"l.dceil{h}_AB"] = _at(le["AB"]["learned"]["ceil_med"], hz, h) - _at(le["AB"]["hand"]["ceil_med"], hz, h)
            d[f"l.dceil{h}_BA"] = _at(le["BA"]["learned"]["ceil_med"], hz, h) - _at(le["BA"]["hand"]["ceil_med"], hz, h)
    k = card["pop"].get("kind_share_law", {})
    if k.get("law"):
        for h in (8, 32):
            d[f"k.law{h}"], d[f"k.const{h}"], d[f"k.lin{h}"], d[f"k.pf{h}"] = (_at(k[n], k["hz"], h) for n in ("law", "const", "lin", "pf"))
    t = card["twins"]
    d["t.l1_8"] = _at(t["l1"], card["grid"]["hz"], 8)
    d["t.doubling"] = _f(t["doubling_ticks_2_8"])
    tm = card["timing"]
    d["cost.s_per_member_tick"] = (tm["main_s"] + tm["branch_s"]) / (tm["main_member_ticks"] + tm["branch_member_ticks"])
    return d


def gates(d: dict) -> dict:
    g = {}
    ok = lambda v: v is not None and np.isfinite(v)
    lv = [L for L in LEVELS if ok(d.get(f"{L}.pf8"))]
    pf_max = max([d[f"{L}.pf8"] for L in lv], default=float("nan"))
    g["predictable"] = bool(any(d[f"{L}.pf8"] >= TH["PF_MIN"] for L in lv))
    g["closure_gap"] = bool(any(d[f"{L}.pf8"] >= TH["PF_MIN"] and d[f"{L}.gap8"] >= TH["GAP_MIN"] for L in lv))
    sig = {L: d.get(f"{L}.sigma_hat", float("nan")) for L in lv if d[f"{L}.pf8"] >= TH["PF_MIN"]}
    best = max(sig, key=lambda L: -1.0 if not ok(sig[L]) else sig[L]) if sig else None
    g["sigma_hat_best"] = float(sig[best]) if best and ok(sig[best]) else float("nan")
    g["sigma_hat_level"] = best
    g["exam_worthy"] = bool(best is not None and ok(sig[best]) and sig[best] >= TH["SIGMA_HAT_MIN"])
    g["structure"] = bool(d["s.nb_mean"] >= TH["NB_MIN"] and d["s.slots_full_share"] <= TH["SLOTS_FULL_MAX"]
                          and ok(d["s.half_life_ticks"]) and d["s.half_life_ticks"] >= TH["HALF_LIFE_MIN"]
                          and (d["s.v_net"] >= TH["V_NET_MIN"] or d["s.events100"] >= TH["EVENTS_MIN"]))
    g["interaction"] = bool(ok(d.get("b.pf_disp8")) and ok(d.get("b.ceil_disp8")) and d["b.pf_disp8"] >= TH["BODY_PF_MIN"]
                            and d["b.ceil_disp8"] <= TH["BODY_CEIL_MAX"])
    g["reading_worthy"] = bool(g["structure"] and g["interaction"])
    g["actions"] = bool(any(ok(d.get(f"{L}.act_ms")) and d[f"{L}.act_ms"] >= TH["ACT_MS_MIN"] for L in lv))
    g["stationary"] = bool(ok(d.get("grid.tick_share")) and d["grid.tick_share"] <= TH["TICK_SHARE_MAX"]
                           and (not ok(d.get("grid.member_share")) or d["grid.member_share"] <= TH["MEMBER_SHARE_MAX"]))
    g["levels_add"] = bool((ok(d.get("x.bodies_to_grid8")) and d["x.bodies_to_grid8"] >= TH["CROSS_GAIN_MIN"])
                           or (ok(d.get("pop.pf8")) and d["pop.pf8"] >= TH["PF_MIN"] and d["pop.gap8"] >= TH["GAP_MIN"]))
    g["learned_differs"] = bool(ok(d.get("l.dceil8_AB")) and min(d["l.dceil8_AB"], d["l.dceil8_BA"]) >= TH["LEARNED_DCEIL_MIN"]
                                and d["l.r2_min"] < TH["LEARNED_R2_MAX"])
    if not ok(pf_max) or pf_max < TH["PF_NOISE"]:
        v = "dull: nothing predictable"
    elif not g["closure_gap"]:
        v = "dull: predictable by the cheap family" if g["predictable"] else "dull: little predictable"
    elif not g["exam_worthy"]:
        v = "dull: the hidden part has no weight"
    else:
        v = "exam-worthy" + (" + reading-worthy" if g["reading_worthy"] else "") + (" + actions" if g["actions"] else "")
    g["verdict"] = v
    g["dull"] = v.startswith("dull")
    return g


def late_vs_early(c_early: dict, c_late: dict) -> dict:
    """Do the statistics at late time equal those early? Grid channel means and sds (in early sd units), the
    body count, the events, pf(8), ceil(8) and sigma_hat."""
    ge, gl = c_early["grid"], c_late["grid"]
    mu_e, sd_e = np.array(ge["mean"], float), np.array(ge["std"], float)
    mu_l, sd_l = np.array(gl["mean"], float), np.array(gl["std"], float)
    live = np.array(ge["live"], bool) & np.array(gl["live"], bool)
    dm = np.where(live, (mu_l - mu_e) / np.maximum(sd_e, 1e-300), 0.0)
    ls = np.where(live, np.log(np.maximum(sd_l, 1e-300) / np.maximum(sd_e, 1e-300)), 0.0)
    de, dl = derive(c_early), derive(c_late)
    nb_e, nb_l = de["s.nb_mean"], dl["s.nb_mean"]
    ratio = nb_l / nb_e if nb_e > 0.5 else (1.0 if nb_l <= 0.5 else float("inf"))
    out = dict(d_mean=dm.tolist(), log_sd_ratio=ls.tolist(), count_ratio=float(ratio),
               events_early=de["s.events100"], events_late=dl["s.events100"],
               pf8=[de.get("grid.pf8"), dl.get("grid.pf8")], ceil8=[de.get("grid.ceil8"), dl.get("grid.ceil8")],
               sigma_hat=[de.get("grid.sigma_hat"), dl.get("grid.sigma_hat")],
               verdict=[gates(de)["verdict"], gates(dl)["verdict"]])
    sh = [v for v in out["sigma_hat"]]
    out["same"] = bool(np.abs(dm).max() <= TH["LATE_DMEAN_MAX"] and np.abs(ls).max() <= TH["LATE_LOGSD_MAX"]
                       and TH["LATE_COUNT_LO"] <= ratio <= TH["LATE_COUNT_HI"]
                       and (not np.isfinite(sh).all() or abs(sh[0] - sh[1]) <= TH["LATE_SIGMA_HAT"]))
    return out


def robust(a: float, b: float) -> bool:
    """Two estimates of one card entry agree: within ROBUST_ABS or within ROBUST_REL of the larger magnitude."""
    if a is None or b is None or not (np.isfinite(a) and np.isfinite(b)):
        return bool((a is None or not np.isfinite(a)) and (b is None or not np.isfinite(b)))
    return bool(abs(a - b) <= max(TH["ROBUST_ABS"], TH["ROBUST_REL"] * max(abs(a), abs(b))))
