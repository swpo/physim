"""Random search over Flow-Lenia rules for worlds with several persistent, moving, interacting
bodies. Usage: python search.py WORKER NWORKERS I0 I1 [STEPS]
Run i draws its rule and initial state from seed (2026, i); results go to
search/results_wWORKER.jsonl (one line per run; finished runs are skipped on restart) and
small float16 snapshots to search/frames/i.npz."""
import json
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flowlenia as fl
import metrics as mt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "search")
SIZE = 128
SNAP_EVERY = 10


def config_for(i):
    rng = np.random.default_rng([2026, i])
    stratum = "paper" if i % 4 == 0 else "shrunk"
    C = int(rng.choice([1, 2, 3], p=[0.2, 0.6, 0.2]))
    k = int(rng.choice([10, 15, 20])) if C > 1 else int(rng.choice([10, 15]))
    M = None
    if C == 2 and rng.uniform() < 0.4 and k in (10, 20):
        M = [[3, 2], [2, 3]] if k == 10 else [[5, 5], [5, 5]]       # the paper's matrices
    R_scale = 1.0 if stratum == "paper" else float(rng.uniform(0.3, 0.7))
    params = fl.sample_params(rng, C=C, k=k, M=M, R_scale=R_scale)
    L = int(np.clip(round(40 * R_scale), 12, 40))
    n_p = int(np.clip(round(0.2 * SIZE * SIZE / L ** 2), 2, 10))
    init = {"seed": int(1000 + i), "n_patches": n_p, "L": L, "size": SIZE}
    return {"i": i, "stratum": stratum, "params": params, "init": init}


def thresholds(params, A0):
    """Body segmentation: A_sum blurred by a Gaussian of 8% of the largest kernel radius
    (1-4 px), thresholded at 0.05 theta_A; bodies need >= 0.4% of the total mass (>= 5)."""
    R_eff = (params["R"] + 15) * max(params["r"]) * params["R_scale"]
    blur = float(np.clip(0.08 * R_eff, 1.0, 4.0))
    thr = 0.05 * params["theta_A"]
    m_min = max(5.0, 0.004 * float(A0.sum()))
    return thr, m_min, blur


def simulate(cfg, steps, snap_every=SNAP_EVERY, frame_ts=(), abort=True, A0=None, on_snap=None):
    p, ini = cfg["params"], cfg["init"]
    if A0 is None:
        A0 = fl.init_patches(ini["seed"], p["C"], ini["size"], ini["size"], ini["n_patches"], ini["L"])
    thr, m_min, blur = thresholds(p, A0)
    tk = mt.Tracker(A0.shape[1:], thr, m_min, blur=blur)
    tk.update(0, A0)
    A = A0
    frames = {}
    status = "ok"
    sea = 0
    for t in range(steps):
        A = fl.step(A, p, t)
        if (t + 1) in frame_ts:
            frames[t + 1] = np.round(np.clip(A, 0, 2.0) * 127.5).astype(np.uint8)
        if (t + 1) % snap_every == 0:
            lab, comps, ids = tk.update(t + 1, A)
            if on_snap is not None:
                on_snap(t + 1, A, lab, comps, ids)
            s = tk.series[-1]
            if not np.isfinite(A).all():
                status = "nan"
                break
            if abort and t + 1 >= 600:
                sea = sea + 1 if s["occ"] > 0.6 else 0
                if sea >= 20:
                    status = "sea"
                    break
                if t + 1 >= 1000 and all(x["n"] == 0 for x in tk.series[-30:]):
                    status = "dissolved"
                    break
    summ = tk.summary(steps)
    summ["status"] = status
    summ["steps_done"] = t + 1
    summ["mass_rel_drift"] = float(np.abs(A.sum(axis=(1, 2)) - A0.sum(axis=(1, 2))).max() / A0.sum(axis=(1, 2)).max())
    summ["score"] = mt.score(summ) if status == "ok" else 0.0
    return A, summ, tk, frames


def main():
    w, nw, i0, i1 = map(int, sys.argv[1:5])
    steps = int(sys.argv[5]) if len(sys.argv) > 5 else 2000
    os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
    res_path = os.path.join(OUT, f"results_w{w}.jsonl")
    done = set()
    if os.path.exists(res_path):
        for line in open(res_path):
            try:
                done.add(json.loads(line)["i"])
            except Exception:
                pass
    fts = (steps // 4, steps // 2, 3 * steps // 4, steps)
    for i in range(i0, i1):
        if i % nw != w or i in done:
            continue
        cfg = config_for(i)
        t0 = time.time()
        A, summ, tk, frames = simulate(cfg, steps, frame_ts=fts)
        summ.pop("tracks")
        rec = {"i": i, "stratum": cfg["stratum"], "C": cfg["params"]["C"], "k": cfg["params"]["k"],
               "R": cfg["params"]["R"], "R_scale": cfg["params"]["R_scale"], "M": cfg["params"]["M"],
               "init": cfg["init"], "secs": round(time.time() - t0, 1), **summ,
               "series_n": [s["n"] for s in tk.series[::10]]}
        np.savez_compressed(os.path.join(OUT, "frames", f"{i}.npz"),
                            **{f"t{t}": f.sum(0) if f.shape[0] > 3 else f for t, f in frames.items()})
        with open(res_path, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(i, cfg["stratum"], rec["C"], rec["k"], round(rec["R_scale"], 2), summ["status"],
              "nb", summ["n_bodies_median_2nd_half"], "long", summ["n_long_tracks"],
              "len", round(summ["long_track_median_lengths"], 1), "ev", summ["merges"], summ["splits"],
              summ["contact_events"], "occ", round(summ["occupancy_median_2nd_half"], 2),
              "score", round(summ["score"], 3), rec["secs"], "s", flush=True)


if __name__ == "__main__":
    main()
