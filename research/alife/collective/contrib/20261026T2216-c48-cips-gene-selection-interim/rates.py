"""c48: per-capita birth rate by kind in the cips-gene runs. Between consecutive 100 t logs, a rise in the number of
bodies of a kind counts as births of that kind, unless a swap hit a body or a removal happened in that interval
(those intervals are excluded and reported). Exposure = sum over logs of the bodies of that kind x 100 t.
usage: python rates.py run.json ... [--from T0]"""
import sys, json
args = [a for a in sys.argv[1:] if not a.startswith("--")]; t0 = 6000
if "--from" in sys.argv: t0 = float(sys.argv[sys.argv.index("--from") + 1]); args = [a for a in args if a != sys.argv[sys.argv.index("--from") + 1]]
res = {}
for r in args:
    d = json.load(open(r)); L = d["log"]
    sw = {x[0] // 100 for x in d.get("swap_log", [])}; wl = {x[0] // 100 for x in d.get("wash_log", [])}
    def kc(b):
        return (sum(1 for x in b if x[1] >= 0.5 and x[1] > x[2]), sum(1 for x in b if x[2] >= 0.5 and x[2] > x[1]))
    B = [0, 0]; E = [0.0, 0.0]; skipped = 0; drops = [0, 0]
    for a, b in zip(L, L[1:]):
        if a["t"] < t0: continue
        ka, kb = kc(a["bodies"]), kc(b["bodies"])
        for j in (0, 1): E[j] += ka[j] * (b["t"] - a["t"])
        if any(int(x) in sw or int(x) in wl for x in range(a["t"] // 100, b["t"] // 100 + 1)):
            skipped += 1; continue
        for j in (0, 1):
            if kb[j] > ka[j]: B[j] += kb[j] - ka[j]
            if kb[j] < ka[j]: drops[j] += ka[j] - kb[j]
    res[r.replace(".json", "")] = {"births_g1": B[0], "births_g2": B[1], "exposure_g1": E[0], "exposure_g2": E[1],
        "rate_g1_per_1000t": round(1000 * B[0] / max(E[0], 1), 3), "rate_g2_per_1000t": round(1000 * B[1] / max(E[1], 1), 3),
        "unexplained_drops": drops, "intervals_skipped": skipped}
print(json.dumps(res, indent=1))
