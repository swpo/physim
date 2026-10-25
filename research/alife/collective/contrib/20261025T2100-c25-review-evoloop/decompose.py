"""Decompose each kind's change in loop number, per time window, into its own breeding (on-kind births), mutation
inflow (births of kind k from parents of another kind, plus conversions of living loops into k), outflow
(conversions out of k) and deaths, from an evo_track.py JSON. Per-capita own-net rate r_k = (on-kind births - deaths)
per 1000 loop-steps of kind k: under selection the sweeping kind has a higher r_k than the kind it replaces in the
same window; under pure mutation pressure its r_k is not higher and its gain comes from inflow.
usage: decompose.py trk.json [window] [min_mean_loops]"""
import sys, json, numpy as np, collections
d = json.load(open(sys.argv[1])); W = int(sys.argv[2]) if len(sys.argv) > 2 else 20000; MIN = float(sys.argv[3]) if len(sys.argv) > 3 else 5
T = d["T"]; cen = d["census"]
def nmean(k, lo, hi):
    xs = [dict(zip(c["areas"], c["counts"])).get(k, 0) for c in cen if lo <= c["t"] < hi]
    return float(np.mean(xs)) if xs else 0.0
rows = []
for lo in range(0, T, W):
    hi = lo + W; tal = collections.defaultdict(lambda: collections.Counter())
    for e in d["events"]:
        if not (lo <= e["t"] < hi): continue
        if e["type"] == "birth":
            if e["parent_area"] is None: tal[e["area"]]["orphan"] += 1
            elif e["parent_area"] == e["area"]: tal[e["area"]]["own"] += 1
            else: tal[e["area"]]["inflow"] += 1
        elif e["type"] == "death": tal[e["area"]]["death"] += 1
        elif e["type"] == "convert": tal[e["to"]]["conv_in"] += 1; tal[e["from"]]["conv_out"] += 1
    for k, c in sorted(tal.items()):
        n = nmean(k, lo, hi)
        if n < MIN: continue
        ls = n * W / 1000.0
        rows.append(dict(window=[lo, hi], kind=k, mean_loops=round(n, 1), own=c["own"], inflow=c["inflow"], conv_in=c["conv_in"], conv_out=c["conv_out"], deaths=c["death"],
                         own_birth_rate=round(c["own"] / ls, 2), death_rate=round(c["death"] / ls, 2), own_net_rate=round((c["own"] - c["death"]) / ls, 2),
                         inflow_rate=round((c["inflow"] + c["conv_in"]) / ls, 2)))
for r in rows: print(r)
json.dump(rows, open(sys.argv[1].replace(".json", "_decomp.json"), "w"), indent=0)
