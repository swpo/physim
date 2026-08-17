"""probe.py — standardized candidate evaluation, guild-economy search (v4).

Control-twin protocol:
  SETTLE  T1=24k from 12 mixed-allocation founder blobs (shared segment).
  Fork with IDENTICAL rng: CONTROL continues T2; KICK run gets flip-kick
  (flip_frac of recycler cells: a -> 1-a, biomass untouched -> pure
  allocation-market perturbation) then continues T2.
  fr* := median of control tail;  top law fit on kicked run's smoothed fr_b.

Layers & clocks:
  L1 fields (fast): impulse tau of R,W twin-run decay        [tau1 ~60-160]
  L2 guilds (med):  8x8-block recycler-share ACF tau, patch  [tau2 ~500-1200]
  L3 market (slow): relaxation tau of global fr_b after kick [tau3 target >5*tau2]

Gates: G1 s12>=5 (time) AND s23>=5 (time) or length fallback 64/patch_diam>=5
       G2 relaxation r2>=0.85, return |end-fr*|<=0.05
       guilds_ok: bimod>=0.8, 0.15<=share_lo<=0.85, purity>=0.75, ncell>=3000
"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np


def smooth(x, k=11):
    if len(x) < k + 4:
        return np.asarray(x)
    return np.convolve(x, np.ones(k) / k, mode="valid")


def radial_corr_len(F):
    f = F - F.mean()
    if f.std() < 1e-9:
        return None
    ps = np.abs(np.fft.fft2(f)) ** 2
    ac = np.real(np.fft.ifft2(ps))
    ac /= ac[0, 0]
    prof = 0.5 * (ac[0, :] + ac[:, 0])
    below = np.where(prof[:len(prof) // 2] < 1 / np.e)[0]
    return float(below[0]) if len(below) else None


def guild_patch_stats(A, V):
    from scipy import ndimage
    out = {}
    for name, mask in (("rec", (A < 0.5) & (V > 0.05)),
                       ("pro", (A >= 0.5) & (V > 0.05))):
        lab, n = ndimage.label(mask)
        if n == 0:
            out[name] = None
            continue
        sizes = np.atleast_1d(ndimage.sum(np.ones_like(lab), lab, range(1, n + 1)))
        w = sizes / sizes.sum()
        out[name] = {"n": int(n),
                     "size_w": float((sizes * w).sum()),
                     "diam_w": float(np.sqrt((sizes * w).sum())),
                     "max": float(sizes.max())}
    return out


def clone_state(state):
    return [x.copy() for x in state]


def evaluate(tc, seed=0, T1=24000, T2=26000, flip_frac=0.8, rec_every=25,
             snap_ticks=(), do_impulse=True, keep_series=False):
    res = {"tc": dict(tc), "seed": seed, "protocol": f"twinflip{flip_frac}"}
    t_start = time.time()
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    ts, fr_b, pur = [], [], []
    blocks = []
    snaps = {}
    for t in range(T1):
        step(state)
        if t % rec_every == 0:
            m = macro(state)
            ts.append(t); fr_b.append(m["fr_b"]); pur.append(m["purity"])
        if t >= T1 - 6000 and t % 20 == 0:
            blocks.append(block_series(state, p["L"]))
        if t in snap_ticks:
            snaps[t] = clone_state(state)
        if state[0].sum() < 1e-9 and t > 3000:
            break
    m1 = macro(state)
    res["settle"] = {k: (round(float(v), 4) if np.isfinite(v) else None)
                     for k, v in m1.items()}
    if m1["ncell"] < 3000 or not np.isfinite(m1["fr_b"]):
        res["fail"] = "extinct_or_sparse"
        res["runtime_s"] = round(time.time() - t_start, 1)
        return res, snaps
    V, E, R, W, A = state
    bm = bimodality(A, V)
    res["bimod"] = {k: round(v, 3) for k, v in bm.items()}
    ce = contact_enrichment(A, V)
    res["contact_enrich"] = round(ce, 3) if ce else None
    res["patches"] = guild_patch_stats(A, V)
    res["len_W"] = radial_corr_len(W)
    res["tau_L2"] = block_tau(blocks, 20)
    pfin = m1["purity"]
    if pfin and pfin > 0:
        idx = np.where(np.asarray(pur) >= 0.9 * pfin)[0]
        res["t_form"] = float(ts[idx[0]]) if len(idx) else None
    if do_impulse:
        res["tau_L1_R"] = impulse_tau(p, state, "R", seed)
        res["tau_L1_W"] = impulse_tau(p, state, "W", seed)
    guilds_ok = (bm["bimod"] >= 0.8 and 0.15 <= bm["share_lo"] <= 0.85
                 and m1["purity"] >= 0.75)
    res["guilds_ok"] = bool(guilds_ok)
    if not guilds_ok:
        res["fail"] = "no_guilds"
        res["runtime_s"] = round(time.time() - t_start, 1)
        return res, snaps
    # fork twins with identical rng
    seed_fork = int(rng.integers(2 ** 31))
    st_c = clone_state(state)
    st_k = clone_state(state)
    rng_c = np.random.default_rng(seed_fork)
    rng_k = np.random.default_rng(seed_fork)
    step_c = make_stepper(p, rng_c)
    step_k = make_stepper(p, rng_k)
    Vk, Ek, Rk, Wk, Ak = st_k
    rec = (Ak < 0.5) & (Vk > 0.05)
    sel = rec & (np.random.default_rng(seed + 999).random(Vk.shape) < flip_frac)
    Ak[sel] = 1.0 - Ak[sel]
    cfr, kfr = [], []
    for t in range(T2):
        step_c(st_c); step_k(st_k)
        if t % rec_every == 0:
            cfr.append(macro(st_c)["fr_b"])
            kfr.append(macro(st_k)["fr_b"])
        if (t + T1) in snap_ticks:
            snaps[t + T1] = clone_state(st_k)
    cfr = np.array(cfr); kfr = np.array(kfr)
    res["fr_star"] = float(np.median(cfr[-len(cfr) // 3:]))
    res["sd_fr_ctrl"] = float(np.std(cfr[-len(cfr) // 3:]))
    res["kick_start"] = float(kfr[0])
    res["kick_end"] = float(np.median(kfr[-40:]))
    res["return_gap"] = float(abs(res["kick_end"] - res["fr_star"]))
    sm = smooth(kfr, 11)
    fit = compact_top_fit(sm, dt=rec_every)
    res["top_fit"] = {"model": fit["model"], "r2": fit["r2"],
                      "params": {k: (round(v, 1) if isinstance(v, float) else v)
                                 for k, v in fit["params"].items()},
                      "all": fit["all"]}
    tau3 = fit["params"].get("tau") if fit["model"] == "relaxation" else None
    res["tau_L3"] = float(tau3) if tau3 else None
    if keep_series:
        res["series_kick"] = [round(float(v), 4) for v in kfr]
        res["series_ctrl"] = [round(float(v), 4) for v in cfr]
    t1 = max(res.get("tau_L1_R") or 0, res.get("tau_L1_W") or 0) or None
    seps = {}
    if t1 and res["tau_L2"]:
        seps["s12"] = round(res["tau_L2"] / t1, 2)
    if res["tau_L2"] and tau3:
        seps["s23"] = round(tau3 / res["tau_L2"], 2)
    pd = res["patches"]
    if pd.get("rec") and pd.get("pro"):
        diam = max(pd["rec"]["diam_w"], pd["pro"]["diam_w"])
        seps["s23_len"] = round(p["L"] / diam, 2)
    res["seps"] = seps
    res["g2_ok"] = bool(fit["model"] == "relaxation" and fit["r2"] >= 0.85
                        and res["return_gap"] <= 0.05)
    res["g1_ok"] = bool(seps.get("s12", 0) >= 5 and seps.get("s23", 0) >= 5)
    res["pass"] = bool(res["g2_ok"] and res["g1_ok"])
    res["runtime_s"] = round(time.time() - t_start, 1)
    return res, snaps
