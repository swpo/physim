"""Do bodies nucleate at the initial random field's largest maxima?
Rebuilds the claim world's initial field for SEED, finds its local maxima (periodic), and compares them with the
first position of every founder track (no parents) in PACKDIR/lineage_audit.json.
usage: python s_check.py SEED PACKDIR"""
import sys, json, importlib.util
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/physim/research/alife")
spec = importlib.util.spec_from_file_location("w", "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py")
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, pk = int(sys.argv[1]), sys.argv[2]
s = w.init(seed, w.META["size"]); e = s["e"]; H, W = e.shape
xi = (e - w.P["e0"]) / w.P["noise"]
mx = ndimage.maximum_filter(xi, size=5, mode="wrap")
pk_mask = (xi == mx)
ys, xs = np.nonzero(pk_mask)
vals = xi[ys, xs]; order = np.argsort(-vals)
peaks = [(int(ys[i]), int(xs[i]), float(vals[i])) for i in order]
L = json.load(open(pk + "/lineage_audit.json"))
founders = [t for t in L["tracks"] if not t["parents"] and t["end"] - t["start"] >= 500]
def pdist(a, b):
    dy = abs(a[0] - b[0]); dy = min(dy, H - dy); dx = abs(a[1] - b[1]); dx = min(dx, W - dx); return (dy * dy + dx * dx) ** 0.5
rows = []
for f in founders:
    c = (f["cy"][0], f["cx"][0])
    d = [pdist(c, p[:2]) for p in peaks]
    j = int(np.argmin(d))
    rows.append({"track": f["id"], "start_t": f["start"], "pos": [round(c[0], 1), round(c[1], 1)], "xi_at_pos": float(xi[int(round(c[0])) % H, int(round(c[1])) % W]),
                 "nearest_peak_rank": j + 1, "nearest_peak_xi": peaks[j][2], "dist_px": round(d[j], 1)})
nf = len(rows)
top = set(r["nearest_peak_rank"] for r in rows if r["dist_px"] < 12)
res = {"seed": seed, "n_peaks": len(peaks), "peak_xi_top12": [round(p[2], 2) for p in peaks[:12]], "founders": rows,
       "founders_within_12px_of_a_top_nf_peak": sum(1 for r in rows if r["dist_px"] < 12 and r["nearest_peak_rank"] <= nf),
       "top_nf_peaks_that_nucleated": len([k for k in top if k <= nf]), "nf": nf,
       "e_init_max": float(e.max()), "frac_px_e_gt_0.15": float((e > 0.15).mean())}
json.dump(res, open(pk + f"/s_check_seed{seed}.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "founders"}))
for r in rows: print(r)
