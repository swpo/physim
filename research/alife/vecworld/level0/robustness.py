"""Robustness record for a packaged world: the stage-2 screens on 3 initial seeds (4000 steps)
and a run with flow noise. Usage: python robustness.py NAME RUN_INDEX SEED_IDX [NOISE_STD]
Writes worlds/NAME/robustness.json."""
import glob
import json
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search as se

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ["n_bodies_median_2nd_half", "n_long_tracks", "long_track_median_life", "long_track_median_speed",
        "long_track_median_lengths", "long_track_median_net_lengths", "long_track_median_body_len",
        "merges", "splits", "contact_events", "contacts_per_body_mean", "occupancy_median_2nd_half",
        "max_body_frac_final", "mass_rel_drift", "score"]


def main():
    name, i, sd = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    std = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    out = {"seeds_4000_steps": []}
    for f in glob.glob(os.path.join(HERE, "confirm", "results_w*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if r["i"] == i:
                out["seeds_4000_steps"].append({"seed_idx": r["seed_idx"], "init_seed": r["init"]["seed"],
                                                **{k: r[k] for k in KEYS}})
    out["seeds_4000_steps"].sort(key=lambda r: r["seed_idx"])
    cfg = se.config_for(i)
    if sd:
        cfg["init"]["seed"] = int(77000 + 1000 * sd + i)
    cfg["params"] = dict(cfg["params"], noise={"mode": "flow", "std": std, "seed": 1})
    A, summ, tk, _ = se.simulate(cfg, 4000, abort=False)
    out["flow_noise_4000_steps"] = {"noise": cfg["params"]["noise"],
                                    "note": "F += std*N(0,1) per cell, axis and step; displacement noise dt*std px/step",
                                    **{k: summ[k] for k in KEYS}}
    with open(os.path.join(HERE, "worlds", name, "robustness.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(name, json.dumps(out["flow_noise_4000_steps"]))


if __name__ == "__main__":
    main()
