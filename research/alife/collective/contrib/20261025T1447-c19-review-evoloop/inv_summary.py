"""c19: summarise the invasion replication (invasion/inv_s<seed>_m<8|15>.json from c16's invade.py).
A seed is usable when side 11 holds the majority at the first census after insertion in both arms
(c16's exclusion rule: the residents must still be the founders' kind). Reports, per arm, whether
and when side 4 became the majority."""
import json, glob, re
rows = {}
for f in sorted(glob.glob("invasion/inv_s*_m*.json")):
    s, m = map(int, re.findall(r"inv_s(\d+)_m(\d+)", f)[0]); d = json.load(open(f))
    c = d["census"]; first = c[0]
    t4 = next((r["t"] for r in c if r["n"] and r["hist"][4] / r["n"] > 0.5), None)
    rows.setdefault(s, {})[m] = {"side11_first": round(first["hist"][11] / max(first["n"], 1), 2), "t_side4_majority": t4,
                                 "final_n": c[-1]["n"], "final_side4": round(c[-1]["hist"][4] / max(c[-1]["n"], 1), 2),
                                 "final_hist": c[-1]["hist"]}
out = {"per_seed": rows}; inv = neu = only_inv = only_neu = 0; usable = []
for s, r in rows.items():
    if 8 not in r or 15 not in r: continue
    ok = r[8]["side11_first"] > 0.5 and r[15]["side11_first"] > 0.5
    if not ok: continue
    usable.append(s); a, b = r[8]["t_side4_majority"] is not None, r[15]["t_side4_majority"] is not None
    inv += a; neu += b; only_inv += a and not b; only_neu += b and not a
out.update(usable_seeds=usable, side4_majority_invader=inv, side4_majority_neutral=neu, only_invader=only_inv, only_neutral=only_neu)
json.dump(out, open("invasion_summary.json", "w"), indent=1)
print({k: v for k, v in out.items() if k != "per_seed"})
for s, r in rows.items(): print(s, {m: (x["side11_first"], x["t_side4_majority"], x["final_side4"]) for m, x in r.items()})
