"""Chaos curve, objects gap decomposition at tau = 1, comparison with the old page, summary.json and
the check plot, from the fresh VW-1 data and run_closure.py outputs.

usage: python -B finalize.py   -> results/summary.json, results/closure_check.png
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/fresh/closure/scripts")
import closure_lib as CL  # noqa: E402

AN, LW, RES = CL.AN, CL.LW, CL.RES
T0 = time.time()
D, cat, metas = CL.load_data()
J = cat["Y"].shape[0]
TEST = metas[0]["test_ticks"]
R = metas[0]["R"]
TX = metas[0]["ext_ticks"]
TB = metas[0]["branch_ticks"]
HZ = [1, 2, 4, 8, 16, 32]
import os  # noqa: E402
CLO = {phi: json.load(open(f"{RES}/closure_{phi}.json")) for phi in ("coarse", "objects")
       if os.path.exists(f"{RES}/closure_{phi}.json")}
ITM = {phi: np.load(f"{RES}/closure_{phi}_items.npz") for phi in ("coarse", "objects")
       if os.path.exists(f"{RES}/closure_{phi}_items.npz")}
K, NF, NS = 12, LW.NF, LW.NS
EXTRA = LW.SLOT_EXTRA                           # cy, cx, age, event, uid
EVI = EXTRA.index("event")
EV = LW.EV


def slot_events(tab_row):
    """event code per slot from one TAB record (K*(NS-NF) + 5)."""
    return tab_row[:K * (NS - NF)].reshape(K, NS - NF)[:, EVI]


# ----------------------------------------------------------------------------- chaos curve
def chaos(phi):
    sl = slice(0, CL.N_COARSE) if phi == "coarse" else slice(CL.N_COARSE, None)
    eff, sd = ITM[phi]["eff"], ITM[phi]["sd"]
    Y = cat["Y"][..., sl][..., eff].astype(float) / sd[eff]              # (J, T+1, q)
    Bb = cat["B"][..., sl][..., eff].astype(float) / sd[eff]             # (J, nT, R-1, TB, q)
    Xx = cat["X"][..., sl][..., eff].astype(float) / sd[eff]             # (J, R-1, TX, q)
    q = Y.shape[-1]
    # replicate futures: all test ticks, h = 1..TB
    F = np.stack([np.concatenate([np.stack([Y[:, t + h] for h in range(1, TB + 1)], 1)[:, None],
                                  Bb[:, i].transpose(0, 1, 2, 3)], 1) for i, t in enumerate(TEST)], 1)  # (J, nT, R, TB, q)
    var_short = ((F - F.mean(2, keepdims=True)) ** 2).sum((2, 4)) / (R - 1) / q              # (J, nT, TB)
    t0 = TEST[0]
    G = np.concatenate([np.stack([Y[:, t0 + h] for h in range(1, TX + 1)], 1)[:, None], Xx], 1)   # (J, R, TX, q)
    var_long = ((G - G.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / q                  # (J, TX)
    # natural spreads: (a) unconditional variance over all states = 1 by the standardisation;
    # (b) same trajectory, states >= 100 ticks apart (keeps conserved masses and the glider count's slow drift)
    allY = Y.reshape(-1, q)
    nat_uncond = float((allY.var(0)).mean())
    pairs = [(a, b) for a in range(0, Y.shape[1], 10) for b in range(0, Y.shape[1], 10) if b - a >= 100]
    nat_same = np.array([np.mean([0.5 * ((Y[j, a] - Y[j, b]) ** 2).mean() for a, b in pairs]) for j in range(J)])
    # (c) different trajectories, same time
    rng = np.random.default_rng(3)
    nat_diff = float(np.mean([0.5 * ((Y[j, t] - Y[k, t]) ** 2).mean() for j, k, t in
                              ((j, k, t) for j in range(J) for k in range(J) if k != j for t in TEST)]))
    curve_long = var_long.mean(0)
    curve_short = var_short.mean((0, 1))

    def crossing(c, level):
        idx = np.flatnonzero(c >= level)
        if idx.size == 0:
            return None
        i = int(idx[0])
        if i == 0:
            return 1.0
        # log-linear interpolation between ticks i and i+1 (1-based horizons)
        a, b = np.log(c[i - 1]), np.log(c[i])
        return float(i + (np.log(level) - a) / (b - a))
    levels = {"half_natural": 0.5 * nat_uncond, "0.9_natural": 0.9 * nat_uncond, "natural": nat_uncond,
              "same_trajectory_natural": float(nat_same.mean())}
    cross = {k: crossing(curve_long, v) for k, v in levels.items()}
    boots = {k: [] for k in levels}
    for b in range(400):
        pick = rng.choice(J, J, replace=True)
        c = var_long[pick].mean(0)
        nat_b = {"half_natural": 0.5 * nat_uncond, "0.9_natural": 0.9 * nat_uncond, "natural": nat_uncond,
                 "same_trajectory_natural": float(nat_same[pick].mean())}
        for k in levels:
            x = crossing(c, nat_b[k])
            boots[k].append(np.nan if x is None else x)
    cross_se = {k: (float(np.nanstd(v)) if np.isfinite(v).any() else None) for k, v in boots.items()}
    cross_never = {k: int(np.isnan(v).sum()) for k, v in boots.items()}
    # early growth: log-linear fit of the oracle spread over h in [1, 16] (all test ticks)
    hh = np.arange(1, TB + 1)
    fit_rng = (hh >= 2) & (hh <= 16)
    slope = float(np.polyfit(hh[fit_rng], np.log(curve_short[fit_rng]), 1)[0])
    # bootstrap SE of the short curve (over trajectories)
    bs = np.array([var_short[rng.choice(J, J, replace=True)].mean((0, 1)) for _ in range(400)])
    bl = np.array([var_long[rng.choice(J, J, replace=True)].mean(0) for _ in range(400)])
    return {"q": int(q), "horizons_short": hh.tolist(), "oracle_spread_short": curve_short,
            "oracle_spread_short_se": bs.std(0), "n_states_short": int(J * len(TEST)),
            "horizons_long": list(range(1, TX + 1)), "oracle_spread_long": curve_long,
            "oracle_spread_long_se": bl.std(0), "n_states_long": int(J), "long_from_test_tick": t0,
            "natural_spread_unconditional": nat_uncond, "natural_spread_same_trajectory_ge100": float(nat_same.mean()),
            "natural_spread_same_trajectory_se": float(nat_same.std() / np.sqrt(J)),
            "natural_spread_other_trajectory_same_time": nat_diff,
            "crossing_horizon_ticks": cross, "crossing_horizon_se": cross_se, "crossing_not_reached_in_bootstrap": cross_never,
            "growth_rate_per_tick_log_spread_h2_16": slope, "e_folding_ticks": 1.0 / slope,
            "doubling_ticks": float(np.log(2) / slope),
            "ratio_to_natural_at": {str(h): float(curve_long[h - 1] / nat_uncond) for h in (1, 2, 4, 8, 16, 32, 48, 64, 96)
                                    if h <= TX},
            "note": "oracle spread = within-replicate unbiased variance over R = 6 copies of the same privileged state "
                    "(base continuation + 5 fresh-noise clones), mean over the view's coordinates, standardised units "
                    "(1 = the unconditional variance); short curve: all test states, h <= 32; long curve: first test "
                    "tick only, h <= 96. Crossings: first horizon at which the mean curve reaches the level "
                    "(log-linear interpolation), bootstrap over trajectories."}


# ----------------------------------------------------------------------------- gap split
def gap_split():
    it = ITM["objects"]
    names = [str(x) for x in it["names"]]
    items, eff, sd = it["items"], it["eff"], it["sd"]
    # back to all K*NF coordinates (constant coordinates: zero error), standardised units
    f_, p_ = it["FUT1"].astype(float), it["P1"].astype(float)              # (n, R, q_eff), (npred, n, q_eff)
    FUT1 = np.zeros(f_.shape[:2] + (K * NF,))
    FUT1[..., eff] = f_
    P1 = np.zeros(p_.shape[:2] + (K * NF,))
    P1[..., eff] = p_
    best1 = CLO["objects"]["best_name"][0]
    Yraw = cat["Y"][..., CL.N_COARSE:]
    Braw = cat["B"][..., CL.N_COARSE:]
    n = len(items)
    pres_t = np.zeros((n, K), bool)
    pres_1 = np.zeros((n, R, K), bool)
    ev_1 = np.zeros((n, R, K))
    for a, (j, i, t) in enumerate(items):
        pres_t[a] = Yraw[j, t].reshape(K, NF)[:, 0] > 0.5
        pres_1[a, 0] = Yraw[j, t + 1].reshape(K, NF)[:, 0] > 0.5
        ev_1[a, 0] = slot_events(cat["TAB"][j, t + 1])
        for r in range(1, R):
            pres_1[a, r] = Braw[j, i, r - 1, 0].reshape(K, NF)[:, 0] > 0.5
            ev_1[a, r] = slot_events(cat["BTAB"][j, i, r - 1, 0])
    # sanity: the slot table's presence agrees with the event codes (dead/fused slots have presence 0)
    live = np.broadcast_to(pres_t[:, None], pres_1.shape) | pres_1                 # slot-ticks counted (checker's rule)
    changed = pres_1 != pres_t[:, None]
    kind = np.full(pres_1.shape, "none", object)
    kind[(ev_1 == EV["fusion"]) | (ev_1 == EV["fused"])] = "fusion"
    kind[ev_1 == EV["fission"]] = "fission"
    kind[(ev_1 == EV["birth"]) | ((kind == "none") & changed & pres_1)] = "appearance"
    kind[(ev_1 == EV["death"]) | ((kind == "none") & changed & ~pres_1)] = "loss"
    event = kind != "none"
    grp = {"identity": [0, 1, 2], "position": [3, 4, 5, 6], "shape": [7, 8, 9], "velocity": [10, 11]}

    def split(pname, reps):
        P = P1[names.index(pname)]                                              # (n, q)
        e = ((FUT1 - P[:, None]) ** 2).reshape(n, R, K, NF)                    # per replicate, slot, feature
        # unbiased per-sample oracle error: leave-one-out replicate mean, rescaled by (R-1)/R
        loo = (FUT1.sum(1, keepdims=True) - FUT1) / (R - 1)
        eo = (((FUT1 - loo) ** 2) * (R - 1) / R).reshape(n, R, K, NF)
        m = np.zeros((n, R), bool)
        m[:, reps] = True
        L = live & m[:, :, None]
        Ev = event & L
        No = ~event & L
        tot = e[L].sum()
        res = {"predictor": pname, "replicates_used": "base continuation only" if reps == [0] else f"all {R}",
               "slot_ticks": {"event": int(Ev.sum()), "none": int(No.sum())},
               "share_slot_ticks_with_event": float(Ev.sum() / L.sum()),
               "share_of_error_on_event_slots": float(e[Ev].sum() / tot),
               "share_of_error_excluded_slots(absent at t and t+1)": float(e[~L & m[:, :, None]].sum() / e[m].sum()),
               "share_of_error_by_group": {k: {g: float(e[M][:, idx].sum() / tot) for g, idx in grp.items()}
                                           for k, M in (("event", Ev), ("none", No))},
               "by_kind": {}}
        for kd in ("fusion", "fission", "appearance", "loss"):
            Mk = (kind == kd) & L
            res["by_kind"][kd] = {"share_slot_ticks": float(Mk.sum() / L.sum()), "share_of_error": float(e[Mk].sum() / tot)}
        if reps != [0]:
            gap = e - eo
            res["oracle_error_share_on_event_slots"] = float(eo[Ev].sum() / eo[L].sum())
            res["share_of_gap(best - oracle)_on_event_slots"] = float(gap[Ev].sum() / gap[L].sum())
            res["mean_sq_err_per_slot_tick"] = {"event": float(e[Ev].sum() / Ev.sum()), "none": float(e[No].sum() / No.sum()),
                                                "oracle_event": float(eo[Ev].sum() / Ev.sum()),
                                                "oracle_none": float(eo[No].sum() / No.sum())}
        return res
    # bootstrap SE (over trajectories) of the two headline shares, base-continuation version, best predictor
    out = {"tau": 1, "best_predictor_tau1": best1,
           "event_definition": "slot present at t or t+1 (checker's rule); event = tracker code at t+1 is fusion/fused "
                               "(fusion), fission (fission, parent or child), birth or presence 0->1 (appearance), "
                               "death or presence 1->0 (loss)",
           "best_base": split(best1, [0]), "best_all": split(best1, list(range(R))),
           "ar1_base": split("ar1", [0]), "ar1_all": split("ar1", list(range(R)))}
    rng = np.random.default_rng(4)
    item_j = items[:, 0]
    P = P1[names.index(best1)]
    e = ((FUT1 - P[:, None]) ** 2).reshape(n, R, K, NF).sum(-1)
    bs_t, bs_e = [], []
    for b in range(400):
        pick = rng.choice(np.unique(item_j), np.unique(item_j).size, replace=True)
        idx = np.concatenate([np.flatnonzero(item_j == jj) for jj in pick])
        L, Ev, eb = live[idx], event[idx] & live[idx], e[idx]
        bs_t.append(Ev.sum() / L.sum())
        bs_e.append(eb[Ev].sum() / eb[L].sum())
    out["best_all_se"] = {"share_slot_ticks_with_event": float(np.std(bs_t)), "share_of_error_on_event_slots": float(np.std(bs_e))}
    # high-precision reference: AR(1) (folds as analyze.closure) against the base continuation at EVERY tick
    Yf = cat["Y"][..., CL.N_COARSE:].astype(float)
    Z = np.zeros_like(Yf)
    Z[..., eff] = Yf[..., eff] / sd[eff]
    folds = np.arange(J) % AN.NFOLD
    cnt = {"event": 0, "none": 0}
    acc = {"event": 0.0, "none": 0.0}
    kinds = {kd: [0, 0.0] for kd in ("fusion", "fission", "appearance", "loss")}
    per_traj = []
    for f in range(AN.NFOLD):
        tr = np.flatnonzero(folds != f)
        mu = Z[tr].reshape(-1, K * NF).mean(0)
        a_ = (Z[tr, :-1] - mu).reshape(-1, K * NF)
        b_ = (Z[tr, 1:] - mu).reshape(-1, K * NF)
        rho = (a_ * b_).sum(0) / np.maximum((a_ * a_).sum(0), 1e-12)
        for j in np.flatnonzero(folds == f):
            P = mu + rho * (Z[j, :-1] - mu)
            e = ((Z[j, 1:] - P) ** 2).reshape(-1, K, NF).sum(-1)               # (T, K)
            pt = Yf[j, :-1].reshape(-1, K, NF)[..., 0] > 0.5
            p1 = Yf[j, 1:].reshape(-1, K, NF)[..., 0] > 0.5
            ev = cat["TAB"][j, 1:, :K * (NS - NF)].reshape(-1, K, NS - NF)[..., EVI]
            Lv = pt | p1
            evt = (ev != 0) | (pt != p1)
            cnt["event"] += int((evt & Lv).sum())
            cnt["none"] += int((~evt & Lv).sum())
            acc["event"] += float(e[evt & Lv].sum())
            acc["none"] += float(e[~evt & Lv].sum())
            per_traj.append((float(e[evt & Lv].sum()), float(e[Lv].sum()), int((evt & Lv).sum()), int(Lv.sum())))
            kd = np.full(ev.shape, "none", object)
            kd[(ev == EV["fusion"]) | (ev == EV["fused"])] = "fusion"
            kd[ev == EV["fission"]] = "fission"
            kd[(ev == EV["birth"]) | ((kd == "none") & (pt != p1) & p1)] = "appearance"
            kd[(ev == EV["death"]) | ((kd == "none") & (pt != p1) & ~p1)] = "loss"
            for k_ in kinds:
                m_ = (kd == k_) & Lv
                kinds[k_][0] += int(m_.sum())
                kinds[k_][1] += float(e[m_].sum())
    tot_e, tot_n = acc["event"] + acc["none"], cnt["event"] + cnt["none"]
    pt_ = np.array(per_traj)
    bs1, bs2 = [], []
    for b in range(400):
        pk = pt_[rng.choice(len(pt_), len(pt_), replace=True)]
        bs1.append(pk[:, 2].sum() / pk[:, 3].sum())
        bs2.append(pk[:, 0].sum() / pk[:, 1].sum())
    out["ar1_base_every_tick"] = {"slot_ticks": cnt, "share_slot_ticks_with_event": cnt["event"] / tot_n,
                                  "share_slot_ticks_with_event_se": float(np.std(bs1)),
                                  "share_of_error_on_event_slots": acc["event"] / tot_e,
                                  "share_of_error_on_event_slots_se": float(np.std(bs2)),
                                  "by_kind": {k_: {"share_slot_ticks": v[0] / tot_n, "share_of_error": v[1] / tot_e}
                                              for k_, v in kinds.items()},
                                  "note": "AR(1) toward the training mean (folds by trajectory as analyze.closure, rho "
                                          "from all one-tick pairs), error against the base continuation at every tick "
                                          "t = 0..T-1 of every trajectory; bootstrap over trajectories"}
    return out


# ----------------------------------------------------------------------------- best-of set from per-item errors
def recompute(phi, extra=None):
    """Ceiling, bootstrap SE (400, as analyze.closure) and the selection check from the per-item
    errors of run_closure (+ optional extra predictors' per-item errors on the same items)."""
    it = ITM[phi]
    names = [str(x) for x in it["names"]]
    err = {nm: it["err"][k].astype(float) for k, nm in enumerate(names)}
    for nm, e in (extra or {}).items():
        err[nm] = e.astype(float)
    names = list(err)
    orac, item_j = it["orac"].astype(float), it["item_j"]
    nH = orac.shape[1]

    def summ(idx):
        V = np.stack([err[nm][idx].mean(0) for nm in names])
        v0, vu = err["mean"][idx].mean(0), orac[idx].mean(0)
        return V, v0, vu
    V, V0, Vu = summ(np.arange(len(item_j)))
    best = V.min(0)
    rng = np.random.default_rng(0)
    uj = np.unique(item_j)
    bc = []
    for b in range(400):
        pick = rng.choice(uj, uj.size, replace=True)
        idx = np.concatenate([np.flatnonzero(item_j == q) for q in pick])
        Vb, v0b, vub = summ(idx)
        bc.append((v0b - Vb.min(0)) / (v0b - vub))
    rng = np.random.default_rng(1)
    sel = []
    for s in range(200):
        half = rng.permutation(uj)[: uj.size // 2]
        A = np.isin(item_j, half)
        cs = []
        for tr_m, te_m in ((A, ~A), (~A, A)):
            Vt, _, _ = summ(np.flatnonzero(tr_m))
            ch = Vt.argmin(0)
            Ve, v0e, vue = summ(np.flatnonzero(te_m))
            cs.append((v0e - Ve[ch, np.arange(nH)]) / (v0e - vue))
        sel.append(np.mean(cs, 0))
    return {"names": names, "V": {nm: V[k] for k, nm in enumerate(names)}, "V0": V0, "V_oracle": Vu, "V_best": best,
            "best_name": [names[k] for k in V.argmin(0)], "ceiling": (V0 - best) / (V0 - Vu), "ceiling_se": np.std(bc, 0),
            "selection_checked_ceiling": np.mean(sel, 0), "selection_checked_sd": np.std(sel, 0)}


# ----------------------------------------------------------------------------- comparison and summary
OLD_PAGE = {"coarse": [0.99, 0.95, 0.79, 0.34, 0.04, 0.01], "objects": [0.81, 0.63, 0.51, 0.26, 0.13, 0.04]}
vw0 = json.load(open(f"{CL._paths.INT_DIR}/results/A_gliders_certificates.json"))
summary = {"what": "Fresh closure ceilings c = (V0 - Vbest)/(V0 - Voracle) of the VW-1 A_gliders 'both' world "
                   "(MapWorld(specs['both']), <Phi_coarse, Phi_objects>), level-1 data only, new runs",
           "data": {"J_trajectories": J, "T_free_ticks": int(cat["Y"].shape[1] - 1), "burn_in_ticks": 50,
                    "test_ticks": TEST, "n_test_states": int(J * len(TEST)), "replicates_R": R,
                    "replicate_ticks": TB, "chaos_extension_ticks": TX,
                    "designer_seeds": [m["designer_seed"] for m in metas], "members_per_seed": [m["J"] for m in metas],
                    "world_seed": 0, "stride_substeps_per_tick": 20, "level0": "Flow-Lenia 2 x 128 x 128 float64, noise 0.5",
                    "member_ticks_simulated": int(sum(sum(m["member_ticks"].values()) for m in metas)),
                    "simulation_wall_seconds_per_process": [m["timing_s"]["total_s"] for m in metas],
                    "s_per_member_tick": [m["s_per_member_tick"] for m in metas],
                    "source": [f"{RES}/sim_{m['tag']}.npz" for m in metas]},
           "estimator": "integrate/analyze.closure (VW-0 code; MLP on; HORIZONS 1..32) + JAX residual MLP 'rmlp' "
                        "in the best-of set (closure_lib.closure_ext, checked equal to analyze.closure with the MLP off); "
                        "bootstrap SE over trajectories (400)",
           "horizons_ticks": HZ}
import os  # noqa: E402
PL = f"{RES}/closure_coarse_patchlong_items.npz"
for phi in ("coarse", "objects"):
    c = CLO[phi]
    r0 = vw0[f"closure_{phi}"]
    rc = recompute(phi)
    assert np.allclose(rc["ceiling"], c["ceiling"], atol=1e-6), (phi, rc["ceiling"], c["ceiling"])
    ex = {}
    if phi == "coarse" and os.path.exists(PL):
        pl = np.load(PL)
        assert np.array_equal(pl["items"], ITM[phi]["items"])
        assert float(np.abs(pl["orac"] - ITM[phi]["orac"]).max()) < 1e-6
        ex = {"patchnet_long": pl["err"]}
    rc = recompute(phi, ex)
    z = [(a - b) / np.hypot(s1, s2) for a, b, s1, s2 in zip(rc["ceiling"], r0["ceiling"], rc["ceiling_se"], r0["ceiling_se"])]
    summary[phi] = {
        "ceiling": rc["ceiling"], "ceiling_se": rc["ceiling_se"], "V0": rc["V0"], "V_oracle": rc["V_oracle"],
        "V_best": rc["V_best"], "best_name": rc["best_name"], "n_eff_coords": c["n_eff_coords"],
        "n_test_states": c["n_test_states"], "V_by_predictor": rc["V"],
        "selection_checked_ceiling_all": rc["selection_checked_ceiling"],
        "ceiling_main_run": c["ceiling"], "ceiling_main_run_se": c["ceiling_se"], "best_name_main_run": c["best_name"],
        "extra_predictors_added_after_main_run": list(ex),
        "depth_gain": c["depth_gain"], "depth_gain_se": c["depth_gain_se"],
        "ceiling_vw0_predictor_set_only": c["vw0_set_only"]["ceiling"],
        "ceiling_vw0_predictor_set_only_se": c["vw0_set_only"]["ceiling_se"],
        "best_name_vw0_predictor_set_only": c["vw0_set_only"]["best_name"],
        "selection_checked_ceiling": c["selection_check"]["ceiling_mean"],
        "learning_curve": c["learning_curve"],
        "rmlp_validation_gain_over_baseline": [x["val_gain"] for x in c["rmlp_info"]],
        "old_page": OLD_PAGE[phi], "vw0_json_ceiling": r0["ceiling"], "vw0_json_ceiling_se": r0["ceiling_se"],
        "vw0_V_oracle": r0["V_oracle"], "vw0_best_name": r0["best_name"],
        "z_fresh_vs_vw0": z,
        "z_fresh_vw0_predictor_set_vs_vw0": [(a - b) / np.hypot(s1, s2) for a, b, s1, s2 in
                                             zip(c["vw0_set_only"]["ceiling"], r0["ceiling"], c["vw0_set_only"]["ceiling_se"],
                                                 r0["ceiling_se"])],
        "source": f"{RES}/closure_{phi}.json"}
    print(phi, "ceiling", np.round(c["ceiling"], 3).tolist(), "old", OLD_PAGE[phi], "z", np.round(z, 1).tolist(), flush=True)
for phi in ("coarse", "objects"):
    lc = summary[phi]["learning_curve"]
    verdict = []
    for d_, se_, sat in zip(lc["dV_half_minus_all"], lc["dV_half_minus_all_se"], lc["saturated"]):
        verdict.append("non-monotone: V(1/2) < V(all) by more than 2 SE (fit-to-fit variance of the learned "
                       "predictors dominates at this horizon); saturation undetermined" if d_ < -2 * se_ else
                       "saturated" if sat else "still falling: V(all) below V(1/2) by more than 2 SE and 2%")
    summary[phi]["learning_curve_verdict"] = verdict
summary["old_page_claims"] = {
    "coarse_ceiling": OLD_PAGE["coarse"], "objects_ceiling": OLD_PAGE["objects"],
    "objects_gap_tau1": {"share_slot_ticks_with_event": 0.16, "share_of_error_on_event_slots": 0.75,
                         "velocity_on_event_free_slots": 0.20, "predictor": "ar1", "n_test_states": 72},
    "coarse_repro_matched_size": {"tau1": 0.986, "tau2": 0.942},
    "chaos": "by 32 ticks even inputs on empty cells push twin runs apart by as much as natural variability (inputs section)"}
summary["chaos"] = {phi: chaos(phi) for phi in ("coarse", "objects")}
for phi in ("coarse", "objects"):
    ch = summary["chaos"][phi]
    print(phi, "chaos crossing", ch["crossing_horizon_ticks"], "e-fold", round(ch["e_folding_ticks"], 2), flush=True)
summary["objects_gap_tau1"] = gap_split()
g = summary["objects_gap_tau1"]
print("gap: base", g["best_base"]["share_slot_ticks_with_event"], g["best_base"]["share_of_error_on_event_slots"],
      "all", g["best_all"]["share_slot_ticks_with_event"], g["best_all"]["share_of_error_on_event_slots"], flush=True)
# level-1 statistics of the fresh base runs with the VW-0 helper analyze.objects_stats (read only), for context
D2 = {"Yo": [cat["Y"][j, :, CL.N_COARSE:].astype(float) for j in range(J)],
      "tab": [cat["TAB"][j, :, :K * (NS - NF)].reshape(-1, K, NS - NF).astype(float) for j in range(J)],
      "glob": [cat["TAB"][j, :, K * (NS - NF):].astype(float) for j in range(J)]}
summary["objects_stats_fresh"] = AN.objects_stats(D2, K, 20)
summary["objects_stats_vw0"] = {k: vw0["objects_stats"][k] for k in ("objects_per_tick", "events_per_100_ticks",
                                                                    "speed_px_per_tick", "track_life_ticks", "rg_median_px")}
print("objects stats fresh", json.dumps(CL.jsonable({k: summary["objects_stats_fresh"][k] for k in
                                                     ("objects_per_tick", "events_per_100_ticks", "speed_px_per_tick")})), flush=True)
summary["files"] = {"summary": f"{RES}/summary.json", "plot": f"{RES}/closure_check.png",
                    "closure": [f"{RES}/closure_coarse.json", f"{RES}/closure_objects.json"],
                    "scripts": "/home/user/evalwork/vecworld/vw1/fresh/closure/scripts/"}
json.dump(CL.jsonable(summary), open(f"{RES}/summary.json", "w"), indent=1)

# ----------------------------------------------------------------------------- check plot
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.style.use("dark_background")
fig, ax = plt.subplots(2, 2, figsize=(12, 8.6))
col = {"coarse": "#4cc9f0", "objects": "#f8961e"}
a = ax[0, 0]
for phi in ("coarse", "objects"):
    s = summary[phi]
    a.errorbar(HZ, s["ceiling"], yerr=s["ceiling_se"], color=col[phi], marker="o", capsize=3, label=f"{phi} fresh (VW-1)")
    a.plot(HZ, OLD_PAGE[phi], color=col[phi], ls="--", marker="s", mfc="none", alpha=0.7, label=f"{phi} old page (VW-0)")
    a.plot(HZ, s["ceiling_vw0_predictor_set_only"], color=col[phi], ls=":", marker="x", alpha=0.8,
           label=f"{phi} fresh, VW-0 predictor set")
a.set_xscale("log", base=2)
a.set_xticks(HZ)
a.set_xticklabels(HZ)
a.set_ylim(-0.05, 1.05)
a.set_xlabel("horizon (ticks)")
a.set_ylabel("closure ceiling c")
a.set_title(f"closure ceilings, J={J}, {J * len(TEST)} test states, R={R}")
a.legend(fontsize=8)
a = ax[0, 1]
for phi in ("coarse", "objects"):
    ch = summary["chaos"][phi]
    a.plot(ch["horizons_long"], ch["oracle_spread_long"], color=col[phi], label=f"{phi}: oracle spread ({J} states)")
    a.plot(ch["horizons_short"], ch["oracle_spread_short"], color=col[phi], ls=":", label=f"{phi}: all {J * len(TEST)} states")
    a.axhline(ch["natural_spread_same_trajectory_ge100"], color=col[phi], ls="--", lw=0.8, alpha=0.7)
a.axhline(1.0, color="w", ls="--", lw=0.8, label="unconditional spread (=1)")
a.set_yscale("log")
a.set_xlabel("ticks since the copies split")
a.set_ylabel("within-replicate variance (standardised)")
a.set_title("chaos: copies of one state with fresh noise\n(dashed colour: same-trajectory spread, >=100 ticks apart)")
a.legend(fontsize=7)
a = ax[1, 0]
for phi in ("coarse", "objects"):
    lc = summary[phi]["learning_curve"]
    for fr, ls in (("0.25", ":"), ("0.5", "--"), ("1.0", "-")):
        n_tr = np.mean(lc["fit_trajectories_per_fold"][fr])
        cc = lc["ceiling"][fr]
        a.plot(HZ, cc, color=col[phi], ls=ls, marker=".", label=f"{phi}: {n_tr:.1f} fit traj/fold")
a.set_xscale("log", base=2)
a.set_xticks(HZ)
a.set_xticklabels(HZ)
a.set_xlabel("horizon (ticks)")
a.set_ylabel("ceiling of the refitted best-of set")
a.set_title("learning curve (fits on 1/4, 1/2, all fit trajectories)")
a.legend(fontsize=7)
a = ax[1, 1]
labs, sl, se = [], [], []
for k, nm in (("best_base", "best, base"), ("best_all", "best, all reps"), ("ar1_base", "AR(1), base"), ("ar1_all", "AR(1), all reps"),
              ("ar1_base_every_tick", "AR(1), base,\nevery tick")):
    labs.append(nm)
    sl.append(g[k]["share_slot_ticks_with_event"])
    se.append(g[k]["share_of_error_on_event_slots"])
xx = np.arange(len(labs))
a.bar(xx - 0.2, sl, 0.4, color="#90be6d", label="share of slot-ticks with an event at t+1")
a.bar(xx + 0.2, se, 0.4, color="#f94144", label="share of squared error on those slots")
for x0, v in zip(xx - 0.2, sl):
    a.text(x0, v + 0.01, f"{v:.2f}", ha="center", fontsize=8)
for x0, v in zip(xx + 0.2, se):
    a.text(x0, v + 0.01, f"{v:.2f}", ha="center", fontsize=8)
a.set_xticks(xx)
a.set_xticklabels(labs, fontsize=8)
a.set_ylim(0, 1)
a.set_title(f"objects gap at tau = 1 (best = {g['best_predictor_tau1']}; {J * len(TEST)} test states, last bar all ticks)")
a.legend(fontsize=7, loc="upper left")
fig.tight_layout()
fig.savefig(f"{RES}/closure_check.png", dpi=110)
print("saved", f"{RES}/summary.json", f"{RES}/closure_check.png", round(time.time() - T0, 1), "s")
