"""Per-kind demography from evo_track.py output: births (on-kind / off-kind), deaths, conversions, fecundity."""
import json, sys, collections, numpy as np
def analyze(path, tmin=0, tmax=None):
    r = json.load(open(path)); ev = r["events"]; tmax = tmax or r["T"]
    ev = [e for e in ev if tmin <= e["t"] <= tmax and e["t"] > 0]
    B = collections.Counter(); Bon = collections.Counter(); D = collections.Counter(); C = collections.Counter()
    off = collections.Counter(); kids = collections.defaultdict(list); ages = collections.defaultdict(list); orphan = 0
    for e in ev:
        if e["type"] == "birth":
            if e["parent"] is None: orphan += 1; continue
            B[e["parent_area"]] += 1
            if e["area"] == e["parent_area"]: Bon[e["parent_area"]] += 1
            else: off[(e["parent_area"], e["area"])] += 1
        elif e["type"] == "death":
            D[e["area"]] += 1; kids[e["area"]].append(e["kids"]); ages[e["area"]].append(e["age"])
        elif e["type"] == "convert":
            C[(e["from"], e["to"])] += 1
    kinds = sorted(set(B) | set(D))
    rows = []
    for k in kinds:
        rows.append({"kind": k, "births_by_parents": B[k], "on_kind": Bon[k], "breed_true": round(Bon[k] / B[k], 3) if B[k] else None,
                     "deaths": D[k], "mean_kids_at_death": round(float(np.mean(kids[k])), 2) if kids[k] else None,
                     "mean_age_at_death": round(float(np.mean(ages[k]))) if ages[k] else None,
                     "births_per_1000_loop_steps": round(1000 * B[k] / sum(ages[k]), 2) if ages[k] and sum(ages[k]) else None})
    nb = sum(B.values()); noff = sum(off.values()); nconv = sum(C.values())
    return {"file": path, "window": [tmin, tmax], "births_with_parent": nb, "orphan_births": orphan, "off_kind_daughters": noff,
            "conversions_of_living": nconv, "conversions_per_off_kind_birth": round(nconv / noff, 2) if noff else None,
            "per_kind": rows, "top_off_kind": [[a, b, n] for (a, b), n in off.most_common(12)], "top_conversions": [[a, b, n] for (a, b), n in C.most_common(8)],
            "final_census": r["census"][-1]}
if __name__ == "__main__":
    if sys.argv[1] == "--json":
        json.dump([analyze(p) for p in sys.argv[3:]], open(sys.argv[2], "w"), indent=1); sys.exit()
    for p in sys.argv[1:]:
        a = analyze(p); print(json.dumps({k: v for k, v in a.items() if k != "per_kind"}))
        for row in a["per_kind"]:
            if row["births_by_parents"] + row["deaths"] >= 10: print("   ", row)
