"""assay_v2.py — LOCKED adaptive-horizon soup assay (M4; 2026-02-25).
Locked together with metrics_v2.py after seeds-1-2 validation; do not edit.

run_assay(genome): T0=2500 soup chunk -> decide EXTEND(x2, cap 20000) vs STOP
after each chunk (continuation, never re-simulated; soup_sim_v2 parity-gated
vs one long run). EXTEND iff ANY of
  (a) slow channel (tau>=30) still trending: |d<|x|>/dt| * window / amp
      > TREND_FRAC over the last 25%% of the post-burn window;
  (b) any species organism-count trend nonzero: |Theil-Sen slope| * window
      > max(ORG_TREND_ABS, ORG_TREND_REL * mean_n);
  (c) coarse-observable ACFs unconverged: tau_slow > (T-BURN)/5 or censored
      — grants AT MOST ONE doubling (stationary-slow worlds stay cheap;
      trend criteria may chain to cap).
Score = metrics_v2.full_battery at final T; horizon report says why.

CLI: python3 assay_v2.py <world|genome.json> [--seed N] [--tag x] [--L x]
     [--workers n] [--t0 2500] [--cap 20000] [--save-npz] [--results PATH]
Appends a row (kind="assay_v2", tag v2_<tag>) to results.json by default.
"""
import argparse, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
from .soup import sim_cpu as SS2               # [blobkit edit E12]
from . import metrics_v2 as MV2
from . import genome as G

RESULTS = os.environ.get("BLOBKIT_RESULTS", "results.json")  # [blobkit edit E14b]
T0_DEFAULT, T_CAP = 2500.0, 20000.0


def js(o):
    if isinstance(o, dict):
        return {k: js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [js(v) for v in o]
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def horizon_criteria(rec, genome, D=None):
    """Evaluate extend criteria. (a)/(b) from the record (cheap); (c) from
    the battery's own d2 (ALL coarse observables incl. tracked bond/angle
    series — the emergent-timescale detector itself decides if the window
    supports the slowest mode)."""
    from .metrics_v1 import window_mask, BURN  # [blobkit edit E13]
    from . import metrics_v1 as MV1
    out = dict(a_mem=False, b_org=False, c_acf=False, detail={})
    # (a) slow-channel trend (charging/discharging memory)
    trends = {}
    for c in rec.get("memch", []):
        tr = MV2.mem_trend(rec, c)
        trends[int(c)] = tr["trend_frac"]
        if abs(tr["trend_frac"]) > MV2.TREND_FRAC:
            out["a_mem"] = True
    out["detail"]["mem_trend_frac"] = trends
    # (b) organism-count trend per species (last 25% window)
    ct, n_i, spans, _ = MV2.org_counts(rec)
    cm = window_mask(ct)
    orgs = {}
    for i in n_i:
        x = n_i[i][cm].astype(float)
        tt = ct[cm]
        if len(x) < 8:
            continue
        k0 = int(0.75 * len(x))
        if len(x) - k0 < 4:
            k0 = max(len(x) - 4, 0)
        sl = MV2.robust_slope(tt[k0:], x[k0:])
        win = max(tt[-1] - tt[k0], 1e-9)
        d = abs(sl) * win
        floor = max(MV2.ORG_TREND_ABS, MV2.ORG_TREND_REL * max(x.mean(), 1.0))
        orgs[i] = round(float(d), 2)
        if d > floor:
            out["b_org"] = True
    out["detail"]["org_trend"] = orgs
    # (c) slowest measured coarse observable vs window (battery d2)
    t = np.asarray(rec["t"])
    window = float(t[-1] - BURN)
    lim = window / 5.0
    tau_slow = (D or {}).get("d2", {}).get("tau_slow")
    cens = (D or {}).get("d2", {}).get("censored", False)
    out["detail"]["tau_slow"] = tau_slow
    out["detail"]["acf_lim"] = round(lim, 1)
    if tau_slow is not None and (tau_slow > lim or cens):
        out["c_acf"] = True
    return out


def run_assay(genome, seed=1, L=128.0, workers=2, t0=T0_DEFAULT, cap=T_CAP,
              tag=None, results_path=RESULTS, save_npz=None, kicks=None,
              verbose=True):
    """Adaptive-horizon assay. Returns metrics_v2 battery dict + horizon."""
    t_wall0 = time.time()
    tag = tag or genome.get("id", "anon")
    S = SS2.init_soup(genome, L=L, seed=seed, workers=workers, kicks=kicks)
    T = float(t0)
    traj, decisions = [], []
    n_ext, c_used = 0, 0
    why = None
    out = None
    while True:
        status = SS2.advance(S, T)
        rec = SS2.snapshot_rec(S)
        if status != "ok":
            why = status
            break
        # battery at every decision point (checkpoint score + d2 for crit c)
        out = MV2.full_battery(dict(rec), genome=genome)
        traj.append((rec["T"], round(out["interest"], 2)))
        crit = horizon_criteria(rec, genome, D=out["D"])
        fired = [k for k in ("a_mem", "b_org", "c_acf") if crit[k]]
        decisions.append(dict(T=T, fired=fired,
                              detail=crit["detail"]))
        if verbose:
            print(f"[assay_v2 {tag} s{seed}] T={T:.0f} "
                  f"interest={out['interest']:.1f} fired={fired}", flush=True)
        if not fired:
            why = "converged" if n_ext else "static"
            break
        if T >= cap:
            why = "cap"
            break
        # criterion (c) alone grants at most ONE doubling
        if fired == ["c_acf"]:
            if c_used >= 1:
                why = "converged"
                break
            c_used += 1
        T = min(T * 2, cap)
        n_ext += 1
    rec = SS2.snapshot_rec(S)
    if out is None or rec["T"] != traj[-1][0]:
        out = MV2.full_battery(dict(rec), genome=genome)
        traj.append((rec["T"], round(out["interest"], 2)))
    out["horizon"] = dict(T_used=rec["T"], why_stopped=why,
                          n_extensions=n_ext, decisions=decisions,
                          interest_trajectory=traj,
                          wall_total=round(time.time() - t_wall0, 1))
    out["summary"] = MV2.lean_summary(out)
    out["summary"]["horizon"] = dict(T_used=rec["T"], why=why, next=n_ext)
    if save_npz:
        SS2.save_run(rec, save_npz)
    if results_path:
        row = dict(kind="assay_v2", world=genome.get("id"), tag=f"v2_{tag}",
                   seed=seed, T=rec["T"], L=L, dtype=rec["dtype"],
                   status=rec["status"], wall_sim=rec["wall_s"],
                   wall_total=round(time.time() - t_wall0, 1),
                   metrics="metrics_v2", horizon=js(out["horizon"]),
                   battery=js(dict(C=out["C"], interest=out["interest"],
                                   flags=out["flags"])),
                   summary=js(out["summary"]))
        G.append_result(row, path=results_path)
    return out


def main():
    from . import worlds                       # [blobkit edit E14]
    ap = argparse.ArgumentParser()
    ap.add_argument("world")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--L", type=float, default=128.0)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--t0", type=float, default=T0_DEFAULT)
    ap.add_argument("--cap", type=float, default=T_CAP)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--save-npz", default=None)
    ap.add_argument("--results", default=RESULTS)
    a = ap.parse_args()
    if a.world in worlds.WORLDS:
        g = worlds.WORLDS[a.world]()
        kicks = worlds.KICKS.get(g["id"])
    else:
        g = json.load(open(a.world))
        kicks = None
    out = run_assay(g, seed=a.seed, L=a.L, workers=a.workers, t0=a.t0,
                    cap=a.cap, tag=a.tag or g.get("id"),
                    results_path=a.results, save_npz=a.save_npz, kicks=kicks)
    print(json.dumps(js(dict(tag=a.tag or g.get("id"), seed=a.seed,
                             interest=out["interest"],
                             horizon=out["horizon"]["T_used"],
                             why=out["horizon"]["why_stopped"],
                             C={k: round(v, 3) for k, v in out["C"].items()},
                             flags=out["flags"]))))


if __name__ == "__main__":
    main()
