"""Stage 2: re-run chosen rules for longer on several initial seeds.
Usage: python confirm.py WORKER NWORKERS STEPS IDS_FILE
IDS_FILE: JSON list of entries {"i": run index} or {"i":..., "params": {...}} (mutants).
Writes confirm/results_wW.jsonl and confirm/frames/{tag}.npz (uint8 snapshots)."""
import json
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search as se

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "confirm")


def main():
    w, nw, steps = map(int, sys.argv[1:4])
    ents = json.load(open(sys.argv[4]))
    os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
    res_path = os.path.join(OUT, f"results_w{w}.jsonl")
    done = set()
    if os.path.exists(res_path):
        for line in open(res_path):
            done.add(json.loads(line)["tag"])
    jobs = []
    for e in ents:
        for si, sd in enumerate(e.get("seeds", [None, 1, 2])):
            jobs.append((e, si, sd))
    fts = tuple(int(steps * f) for f in (0.1, 0.25, 0.4, 0.55, 0.7, 0.85, 1.0))
    for n, (e, si, sd) in enumerate(jobs):
        if n % nw != w:
            continue
        cfg = se.config_for(e["i"])
        name = e.get("name", str(e["i"]))
        if "params" in e:
            cfg["params"] = e["params"]
        if sd is not None:
            cfg["init"]["seed"] = int(77000 + 1000 * sd + e["i"])
        tag = f"{name}_s{si}"
        if tag in done:
            continue
        t0 = time.time()
        A, summ, tk, frames = se.simulate(cfg, steps, frame_ts=fts, abort=False)
        tracks = summ.pop("tracks")
        rec = {"tag": tag, "name": name, "i": e["i"], "seed_idx": si, "init": cfg["init"],
               "secs": round(time.time() - t0, 1), **summ,
               "series": [{k: s[k] for k in ("t", "n", "occ", "merge", "split", "contacts", "max_body_frac")}
                          for s in tk.series[::5]],
               "long_tracks": [x for x in tracks if x["life"] >= 0.25 * steps]}
        np.savez_compressed(os.path.join(OUT, "frames", f"{tag}.npz"), **{f"t{t}": f for t, f in frames.items()})
        with open(res_path, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(tag, summ["status"], "nb", summ["n_bodies_median_2nd_half"], "long", summ["n_long_tracks"],
              "len", round(summ["long_track_median_lengths"], 1), "ev", summ["merges"], summ["splits"],
              summ["contact_events"], "occ", round(summ["occupancy_median_2nd_half"], 2),
              "score", round(summ["score"], 3), rec["secs"], "s", flush=True)


if __name__ == "__main__":
    main()
