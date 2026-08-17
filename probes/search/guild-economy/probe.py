"""probe.py — standardized candidate evaluation for guild-economy search.

Protocol per candidate:
  Phase 1 (settle, T1=16k): unperturbed; record macro series, L2 blocks.
  L1 impulse taus at end of settle (twin runs, common noise).
  Phase 2 (kick at T1): multiply recycler-guild V,E by keep; run T2=20k;
  fit smoothed fr_b recovery with compact_top_fit -> top law (tau, r2).
Gates evaluated here: viability, guilds (bimod), G2 fit, timescale ladder.
"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np


def smooth(x, k=9):
    if len(x) < k + 4:
        return np.asarray(x)
    return np.convolve(x, np.ones(k) / k, mode="valid")


def purity_tau(ts, pur, final):
    """First time purity reaches 90% of its final settled value."""
    if final < 1e-6:
        return None
    thr = 0.9 * final
    idx = np.where(np.asarray(pur) >= thr)[0]
    return float(ts[idx[0]]) if len(idx) else None


def evaluate(tc, seed=0, T1=16000, T2=20000, keep=0.35, rec_every=25,
             want_snaps=None, do_impulse=True):
    res = {"tc": dict(tc), "seed": seed, "keep": keep}
    t_start = time.time()
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    ts, fr_b, fr_e, pur, vt = [], [], [], [], []
    blocks = []
    snaps = {}
    for t in range(T1):
        step(state)
        if t % rec_every == 0:
            m = macro(state)
            ts.append(t); fr_b.append(m["fr_b"]); fr_e.append(m["fr_e"])
            pur.append(m["purity"]); vt.append(m["Vtot"])
        if t >= T1 - 6000 and t % 20 == 0:
            blocks.append(block_series(state, p["L"]))
        if want_snaps and t in want_snaps:
            snaps[t] = [x.copy() for x in state]
        if state[0].sum() < 1e-9 and t > 3000:
            break
    m1 = macro(state)
    res["settle"] = {k: (round(float(v), 4) if isinstance(v, (int, float)) and np.isfinite(v) else None)
                     for k, v in m1.items()}
    if m1["ncell"] < 400 or not np.isfinite(m1["fr_b"]):
        res["fail"] = "extinct_or_sparse"; res["runtime_s"] = round(time.time() - t_start, 1)
        return res, snaps
    V, E, R, W, A = state
    bm = bimodality(A, V)
    res["bimod"] = {k: round(v, 3) for k, v in bm.items()}
    ce = contact_enrichment(A, V)
    res["contact_enrich"] = round(ce, 3) if ce else None
    bt = block_tau(blocks, 20)
    res["tau_L2_block"] = bt
    res["tau_L2_form"] = purity_tau(ts, pur, m1["purity"])
    res["fr_star_settle"] = float(np.median(fr_b[-160:]))
    res["fr_e_star"] = float(np.median(fr_e[-160:]))
    res["sd_fr_settle"] = float(np.std(fr_b[-160:]))
    # theory prediction for fr_e (uses settled P_e)
    P_e = m1["P_e"]
    q = tc["rho"] * tc["yW"] - 0.3 * tc["leak"] / max(P_e, 1e-9)
    res["fr_e_theory"] = float(q / (1 + q)) if q > 0 else 0.0
    if do_impulse:
        res["tau_L1_R"] = impulse_tau(p, state, "R", seed)
        res["tau_L1_W"] = impulse_tau(p, state, "W", seed)
    # guild check before kick
    guilds_ok = (bm["bimod"] >= 0.8 and 0.12 <= bm["share_lo"] <= 0.88
                 and m1["purity"] >= 0.7)
    res["guilds_ok"] = bool(guilds_ok)
    if not guilds_ok:
        res["fail"] = "no_guilds"; res["runtime_s"] = round(time.time() - t_start, 1)
        return res, snaps
    # KICK: cull recycler guild biomass
    rec = (A < 0.5) & (V > 0.05)
    V[rec] *= keep; E[rec] *= keep
    kfr = []
    for t in range(T2):
        step(state)
        if t % rec_every == 0:
            kfr.append(macro(state)["fr_b"])
        if want_snaps and (t + T1) in want_snaps:
            snaps[t + T1] = [x.copy() for x in state]
    kfr = np.array(kfr)
    res["kick_start"] = float(kfr[0]); res["kick_end"] = float(np.median(kfr[-40:]))
    res["return_gap"] = float(abs(res["kick_end"] - res["fr_star_settle"]))
    sm = smooth(kfr, 9)
    fit = compact_top_fit(sm, dt=rec_every)
    res["top_fit"] = {"model": fit["model"], "r2": fit["r2"],
                      "params": {k: (round(v, 1) if isinstance(v, float) else v)
                                 for k, v in fit["params"].items()},
                      "all": fit["all"]}
    tau3 = fit["params"].get("tau") if fit["model"] == "relaxation" else None
    res["tau_L3"] = float(tau3) if tau3 else None
    # separations
    t1 = max(res.get("tau_L1_R") or 0, res.get("tau_L1_W") or 0) or None
    seps = {}
    if t1 and bt:
        seps["s12"] = round(bt / t1, 2)
    if bt and tau3:
        seps["s23"] = round(tau3 / bt, 2)
    res["seps"] = seps
    res["runtime_s"] = round(time.time() - t_start, 1)
    # gate summary (G1 time-only here; length argument handled in analysis)
    res["g2_ok"] = bool(fit["model"] == "relaxation" and fit["r2"] >= 0.85
                        and res["return_gap"] < 0.06)
    res["g1_time_ok"] = bool(seps.get("s12", 0) >= 5 and seps.get("s23", 0) >= 5)
    return res, snaps


if __name__ == "__main__":
    tc = json.loads(sys.argv[1]) if len(sys.argv) > 1 else dict(
        rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
    res, _ = evaluate(tc, seed=int(sys.argv[2]) if len(sys.argv) > 2 else 0)
    print(json.dumps(res, indent=1, default=float))
