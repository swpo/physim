"""Package one chosen level-0 world: params.json, init.npz, metrics.json, and raw frames for
the video (scratch, deleted after rendering).
Usage: python package.py NAME ENTRY_JSON STEPS
ENTRY_JSON: {"i": run index, optional "params": {...}, "seed_idx": k, "note": "..."}"""
import json
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flowlenia as fl
import search as se

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME_EVERY = 5


def main():
    name, ent, steps = sys.argv[1], json.loads(sys.argv[2]), int(sys.argv[3])
    out = os.path.join(HERE, "worlds", name)
    os.makedirs(out, exist_ok=True)
    os.makedirs(os.path.join(HERE, "scratch"), exist_ok=True)
    cfg = se.config_for(ent["i"])
    if "params" in ent:
        cfg["params"] = ent["params"]
    sd = ent.get("seed_idx", 0)
    if sd:
        cfg["init"]["seed"] = int(77000 + 1000 * sd + ent["i"])
    p, ini = cfg["params"], cfg["init"]
    A0 = fl.init_patches(ini["seed"], p["C"], ini["size"], ini["size"], ini["n_patches"], ini["L"])
    thr, m_min, blur = se.thresholds(p, A0)
    np.savez_compressed(os.path.join(out, "init.npz"), A0=A0, seed=ini["seed"],
                        n_patches=ini["n_patches"], L=ini["L"], size=ini["size"])
    world = {"name": name, "law": "Flow-Lenia (flowlenia.step)", "params": p,
             "init": {**ini, "generator": "flowlenia.init_patches(seed, C, size, size, n_patches, L)",
                      "file": "init.npz (A0, float64, shape (C, H, W))"},
             "search_run": ent["i"], "stratum": cfg["stratum"],
             "screen": {"blur_px": blur, "threshold_on_blurred_Asum": thr, "min_body_mass": m_min},
             "note": ent.get("note", "")}
    with open(os.path.join(out, "params.json"), "w") as f:
        json.dump(world, f, indent=1)
    frames, snaps = [], []
    frames.append(np.round(np.clip(A0, 0, 2.0) * 127.5).astype(np.uint8))

    def on_snap(t, A, lab, comps, ids):
        snaps.append({"t": t, "bodies": [{"id": int(i), "cy": round(c["cy"], 2), "cx": round(c["cx"], 2),
                                          "mass": round(c["mass"], 2), "rg": round(c["rg"], 2)}
                                         for c, i in zip(comps, ids)]})

    fts = set(range(FRAME_EVERY, steps + 1, FRAME_EVERY))
    t0 = time.time()
    # simulate() keeps uint8 frames at frame_ts
    A, summ, tk, fr = se.simulate(cfg, steps, frame_ts=fts, abort=False, A0=A0, on_snap=on_snap)
    secs = time.time() - t0
    frames += [fr[t] for t in sorted(fr)]
    tracks = summ.pop("tracks")
    m0 = A0.sum(axis=(1, 2))
    metrics = {"steps": steps, "dt": p["dt"], "grid": [p["C"], ini["size"], ini["size"]],
               "wall_seconds_incl_screens": round(secs, 1),
               "mass_initial_per_channel": m0.tolist(),
               "mass_final_per_channel": A.sum(axis=(1, 2)).tolist(),
               "summary": summ, "tracks": tracks,
               "events": [{"t": e[0], "kind": e[1], "ids": e[2]} for e in tk.events],
               "series": tk.series}
    with open(os.path.join(out, "metrics.json"), "w") as f:
        json.dump(metrics, f)
    np.savez_compressed(os.path.join(HERE, "scratch", f"frames_{name}.npz"), frames=np.stack(frames),
                        every=FRAME_EVERY)
    with open(os.path.join(HERE, "scratch", f"snaps_{name}.json"), "w") as f:
        json.dump(snaps, f)
    np.savez_compressed(os.path.join(out, f"state_t{steps}.npz"), A=A)
    print(name, json.dumps({k: v for k, v in summ.items()}), round(secs, 1), "s", flush=True)


if __name__ == "__main__":
    main()
