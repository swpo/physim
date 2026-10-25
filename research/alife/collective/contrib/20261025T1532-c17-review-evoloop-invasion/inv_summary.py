"""Summarise census/inv{8,15}_s{seed}.json: time of first side-4 majority after insertion, final shares,
and a one-sided sign test over seeds where the arms disagree. Seeds whose population already had a side-4
majority (or side-11 share < 0.5) at the first census are excluded, as in c16's invasion finding."""
import json, glob, math, os
res = {}
for f in sorted(glob.glob("census/inv8_s*.json")):
    s = int(f.split("_s")[1].split(".")[0]); arms = {}
    for m in (8, 15):
        d = json.load(open(f"census/inv{m}_s{s}.json")); c = d["census"]
        maj = [r["t"] - d["t_ins"] for r in c if r["hist"][4] > 0.5 * r["n"]]
        arms[m] = {"t_major": maj[0] if maj else None, "first_side11": round(c[0]["hist"][11] / max(c[0]["n"], 1), 2),
                   "final_n": c[-1]["n"], "final_side4": round(c[-1]["hist"][4] / max(c[-1]["n"], 1), 2), "final_side11": round(c[-1]["hist"][11] / max(c[-1]["n"], 1), 2)}
    arms["usable"] = arms[15]["first_side11"] >= 0.5
    res[s] = arms
use = [s for s in res if res[s]["usable"]]
inv = sum(res[s][8]["t_major"] is not None for s in use); neu = sum(res[s][15]["t_major"] is not None for s in use)
oi = sum(res[s][8]["t_major"] is not None and res[s][15]["t_major"] is None for s in use)
on = sum(res[s][8]["t_major"] is None and res[s][15]["t_major"] is not None for s in use)
n = oi + on; p = sum(math.comb(n, k) for k in range(oi, n + 1)) / 2 ** n if n else 1.0
out = {"usable_seeds": len(use), "excluded": [s for s in res if s not in use], "side4_majority_invader": inv, "side4_majority_neutral": neu,
       "only_invader": oi, "only_neutral": on, "sign_test_p_one_sided": p,
       "steps_to_majority_invader": sorted(res[s][8]["t_major"] for s in use if res[s][8]["t_major"] is not None),
       "steps_to_majority_neutral": sorted(res[s][15]["t_major"] for s in use if res[s][15]["t_major"] is not None), "per_seed": res}
json.dump(out, open("invasion_summary.json", "w"), indent=1)
print({k: v for k, v in out.items() if k != "per_seed"})
