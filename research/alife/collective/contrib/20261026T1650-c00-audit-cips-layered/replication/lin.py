"""Recompute labkit lineage (persistent splits, generations) from a pack's frames.npz with other K windows,
and list the founder->deepest-generation chain with each track's area range.
usage: python lin.py PACKDIR DT_FRAME K1 [K2 ...]"""
import sys, json
import numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import metrics as M
from labkit.run import _normalize_matter, _segment_frames, _default_min_area

pk, dtf = sys.argv[1], float(sys.argv[2])
Ks = [int(x) for x in sys.argv[3:]]
mat = np.load(pk + "/frames.npz")["matter"].astype(np.float64)
T, H, W = mat.shape
mn, thr, lo, hi = _normalize_matter(mat, {"smooth": 1.0}, True, 0.5)
comps, links = _segment_frames(mn, thr, _default_min_area(H, W), True)
tracks, events = M.track(comps, links, (H, W), True)
out = {"T_frames": T, "dt_frame": dtf, "n_tracks": len(tracks),
       "merges": sum(e["type"] == "merge" for e in events), "splits": sum(e["type"] == "split" for e in events),
       "nucleations": sum(1 for t in tracks if not t["parents"] and t["start"] > 0)}
for K in Ks:
    lin = M.lineage_stats(tracks, events, T, dtf, (H, W), True, K=K)
    gen = lin["generation"]
    ps = sorted(lin["persistent_splits"], key=lambda e: e["frame"])
    out[f"K{K}"] = {"K_time": K * dtf, "persistent_splits": len(ps), "remerged_splits": len(lin["remerged_splits"]),
                    "max_generation": lin["max_generation"],
                    "splits": [(e["frame"] * dtf, e["parent"], e["children"], gen[e["children"][0]]) for e in ps]}
# track table
tt = []
for t in tracks:
    a = np.array(t["area"])
    tt.append({"id": t["id"], "start": t["start"] * dtf, "end": t["end"] * dtf, "birth": t["birth"], "parents": t["parents"],
               "children": t["children"], "area_min": float(a.min()), "area_max": float(a.max()),
               "cy": [float(x) for x in t["cy"]], "cx": [float(x) for x in t["cx"]], "area": [float(x) for x in a]})
out["tracks"] = tt
json.dump(out, open(pk + "/lineage_audit.json", "w"))
print({k: v for k, v in out.items() if k != "tracks"})
for t in tt:
    if t["end"] - t["start"] >= 5 * dtf:
        print(t["id"], t["birth"], t["parents"], "->", t["children"], f"t {t['start']:.0f}-{t['end']:.0f}", f"area {t['area_min']:.0f}-{t['area_max']:.0f}")
