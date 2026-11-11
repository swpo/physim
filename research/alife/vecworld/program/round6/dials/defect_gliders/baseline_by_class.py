"""baseline_by_class -- the zero point of the dial by item class, recomputed from the round-5 ladder's saved
per-item scores (round5/ladder/results/job/n4/scores.npz: 8 pilot truths x 48 items, 4 hidden parameters;
those truths are PILOT_NEVER_REUSE_AS_EXAM). numpy only, seconds. Writes results/baseline_by_class.json.
L = mean over items of the fair energy score summed over the five horizons (1, 2, 4, 8, 16 ticks);
sigma = (L(P0) - L(C)) / (L(K) - L(C)); screen = (L(plugPM) - L(O)) / (L(K) - L(O)) (state given)."""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "round5", "ladder", "results", "job", "n4", "scores.npz")
z = np.load(SRC, allow_pickle=True)
cls = np.concatenate([z[f"t{i}|classes"] for i in range(8)])
out = {"source": "round5/ladder/results/job/n4/scores.npz", "PILOT_NEVER_REUSE_AS_EXAM": True, "n_items": int(len(cls)), "views": {}}
for view in ("block", "pop"):
    L = lambda p: np.concatenate([z[f"t{i}|{view}|{p}"] for i in range(8)])
    out["views"][view] = {}
    for c in ("all", "a", "b", "c", "d", "cd"):
        sel = np.ones(len(cls), bool) if c == "all" else np.isin(cls, list(c))
        g = {p: float(L(p)[sel].sum(1).mean()) for p in ("K", "C", "P0", "O", "plugPM", "D@32", "S@2")}
        out["views"][view][c] = {"n": int(sel.sum()), "L": g, "sigma_P0": (g["P0"] - g["C"]) / (g["K"] - g["C"]),
                                 "C_skill_vs_O": (g["K"] - g["C"]) / (g["K"] - g["O"]),
                                 "state_given_screen": (g["plugPM"] - g["O"]) / (g["K"] - g["O"]),
                                 "K_minus_C_per_horizon": (L("K") - L("C"))[sel].mean(0).tolist(),
                                 "K_minus_O_per_horizon": (L("K") - L("O"))[sel].mean(0).tolist(),
                                 "P0_minus_C_per_horizon": (L("P0") - L("C"))[sel].mean(0).tolist()}
        print(view, c, {k: round(v, 4) for k, v in out["views"][view][c].items() if isinstance(v, float)})
json.dump(out, open(os.path.join(HERE, "results", "baseline_by_class.json"), "w"), indent=1)
