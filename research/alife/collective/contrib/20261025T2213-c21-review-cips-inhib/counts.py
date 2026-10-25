"""(c21) Body counts from labkit metrics series (one frame = 10 t here): count at t=1500, 3000 (and 4500, 6000
if present), peak, merges and persistent splits. usage: counts.py metrics.json [...]"""
import sys, json
for fn in sys.argv[1:]:
    m = json.load(open(fn)); n = m["series"]["n_comp"]; su = m["summary"]; dtf = su["time"] / (su["frames"] - 1)
    at = lambda t: n[int(round(t / dtf))] if int(round(t / dtf)) < len(n) else None
    print(f"{fn}: n(1500) {at(1500)} n(3000) {at(3000)} n(4500) {at(4500)} n(6000) {at(6000)} peak {max(n)} merges {su['merges']} persistent_splits {su['persistent_splits']}")
