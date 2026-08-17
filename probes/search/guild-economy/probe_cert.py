"""probe_cert.py — CERTIFICATION probe for guild-economy candidates (final).

Full behavior cycle in 60k ticks (G5):
  t 0-40k   SETTLE: guilds form (~10k), market equilibrates (~30k)
  t 40k     fork twins, identical rng; KICK twin: flip 80% of recycler cells'
            allocation (a -> 1-a); CONTROL twin: untouched
  t 40k-60k relaxation of fr_site back to control's equilibrium

Measures:
  L1: impulse tau (R,W) at 40k          [twin decay, common noise]
  L2: block ACF tau of recycler share over 34-40k; guild patch stats;
      dwell/patch structure
  L3: relaxation fit (compact_top_fit) on kicked fr_site w/ tau3, r2
  drift guard: control tail slope must be < 0.03 over T2 (else settle bad)
Gates: G1 s12,s23>=5 | G2 relax r2>=0.85 + gap<=0.05 + drift ok | guilds_ok.
usage: probe_cert.py '{"tc": {...}, "seed": 0}'  (or import evaluate_cert)
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
        out[name] = {"n": int(n), "size_w": float((sizes * w).sum()),
                     "diam_w": float(np.sqrt((sizes * w).sum())),
                     "max": float(sizes.max()),
                     "sizes": [float(s) for s in sizes]}
    return out


def evaluate_cert(tc, seed=0, T1=30000, T2=20000, flip_frac=0.8,
                  rec_every=25, snap_ticks=(), keep_series=False):
    res = {"tc": dict(tc), "seed": seed,
           "protocol": "cert_v2_Wseed_T30k+20k_noskip"}
    t_start = time.time()
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    ts, fs, pur = [], [], []
    blocks = []
    snaps = {}
    for t in range(T1):
        step(state)
        if t % rec_every == 0:
            m = macro(state)
            ts.append(t); fs.append(m["fr_site"]); pur.append(m["purity"])
        if t >= T1 - 6000 and t % 20 == 0:
            blocks.append(block_series(state, p["L"]))
        if t in snap_ticks:
            snaps[t] = [x.copy() for x in state]
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
    res["contact_enrich"] = contact_enrichment(A, V)
    res["patches"] = {k: ({kk: vv for kk, vv in v.items() if kk != "sizes"}
                          if v else None)
                      for k, v in guild_patch_stats(A, V).items()}
    res["patch_sizes"] = {k: (v["sizes"] if v else [])
                          for k, v in guild_patch_stats(A, V).items()}
    res["tau_L2"] = block_tau(blocks, 20)
    pfin = m1["purity"]
    if pfin and pfin > 0:
        idx = np.where(np.asarray(pur) >= 0.9 * pfin)[0]
        res["t_form"] = float(ts[idx[0]]) if len(idx) else None
    res["tau_L1_R"] = impulse_tau(p, state, "R", seed)
    res["tau_L1_W"] = impulse_tau(p, state, "W", seed)
    guilds_ok = (bm["bimod"] >= 0.8 and 0.15 <= bm["share_lo"] <= 0.85
                 and m1["purity"] >= 0.75)
    res["guilds_ok"] = bool(guilds_ok)
    if not guilds_ok:
        res["fail"] = "no_guilds"
        res["runtime_s"] = round(time.time() - t_start, 1)
        return res, snaps
    # fork control/kick twins with identical rng
    fork_seed = int(rng.integers(2 ** 31))
    st_c = [x.copy() for x in state]
    st_k = [x.copy() for x in state]
    step_c = make_stepper(p, np.random.default_rng(fork_seed))
    step_k = make_stepper(p, np.random.default_rng(fork_seed))
    Vk, Ek, Rk, Wk, Ak = st_k
    rec = (Ak < 0.5) & (Vk > 0.05)
    sel = rec & (np.random.default_rng(seed + 999).random(Vk.shape) < flip_frac)
    Ak[sel] = 1.0 - Ak[sel]
    cfs, kfs = [], []
    for t in range(T2):
        step_c(st_c); step_k(st_k)
        if t % rec_every == 0:
            cfs.append(macro(st_c)["fr_site"])
            kfs.append(macro(st_k)["fr_site"])
        if (t + T1) in snap_ticks:
            snaps[t + T1] = [x.copy() for x in st_k]
    cfs = np.array(cfs); kfs = np.array(kfs)
    nt = len(cfs)
    res["fr_star"] = float(np.median(cfs[-nt // 3:]))
    res["ctrl_drift"] = float(np.median(cfs[-nt // 3:]) - np.median(cfs[:nt // 3]))
    res["kick_start"] = float(kfs[0])
    res["kick_end"] = float(np.median(kfs[-40:]))
    res["return_gap"] = float(abs(res["kick_end"] - res["fr_star"]))
    # L3 fit: hier_metrics.compact_top_fit on the FULL smoothed kicked series
    # (starts at the kick = max deviation; no window games).
    sm = smooth(kfs, 11)
    fit = compact_top_fit(sm, dt=rec_every)
    res["top_fit"] = {"model": fit["model"], "r2": fit["r2"],
                      "params": {k: (round(v, 1) if isinstance(v, float) else v)
                                 for k, v in fit["params"].items()},
                      "all": fit["all"]}
    tau3 = fit["params"].get("tau") if fit["model"] == "relaxation" else None
    res["tau_L3"] = float(tau3) if tau3 else None
    if keep_series:
        res["series_kick"] = [round(float(v), 4) for v in kfs]
        res["series_ctrl"] = [round(float(v), 4) for v in cfs]
    t1 = max(res.get("tau_L1_R") or 0, res.get("tau_L1_W") or 0) or None
    seps = {}
    if t1 and res["tau_L2"]:
        seps["s12"] = round(res["tau_L2"] / t1, 2)
    if res["tau_L2"] and tau3:
        seps["s23"] = round(tau3 / res["tau_L2"], 2)
    res["seps"] = seps
    res["drift_ok"] = bool(abs(res["ctrl_drift"]) <= 0.03)
    res["g2_ok"] = bool(fit["model"] == "relaxation" and fit["r2"] >= 0.85
                        and res["return_gap"] <= 0.05 and res["drift_ok"])
    res["g1_ok"] = bool(seps.get("s12", 0) >= 5 and seps.get("s23", 0) >= 5)
    res["pass"] = bool(res["g2_ok"] and res["g1_ok"])
    res["runtime_s"] = round(time.time() - t_start, 1)
    return res, snaps


if __name__ == "__main__":
    spec = json.loads(sys.argv[1])
    res, _ = evaluate_cert(spec["tc"], seed=spec.get("seed", 0))
    print(json.dumps(res, default=float))
