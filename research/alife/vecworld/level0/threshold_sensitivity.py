"""Re-segment stored video frames (uint8, every 5 steps) of packaged worlds with stricter density
thresholds, to check that body counts, lifetimes and speeds are not artefacts of the screen.
Usage: python threshold_sensitivity.py NAME...  (needs scratch/frames_NAME.npz)"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as mt
HERE = os.path.dirname(os.path.abspath(__file__))
for name in sys.argv[1:]:
    d = np.load(os.path.join(HERE, "scratch", f"frames_{name}.npz"))
    F, every = d["frames"], int(d["every"])
    w = json.load(open(os.path.join(HERE, "worlds", name, "params.json")))
    scr = w["screen"]
    T = (len(F) - 1) * every
    res = []
    for fac in (1.0, 2.0, 4.0):
        thr = scr["threshold_on_blurred_Asum"] * fac
        tk = mt.Tracker(F.shape[2:], thr, scr["min_body_mass"], blur=scr["blur_px"])
        for n in range(0, len(F), 10 // every):
            tk.update(n * every, F[n].astype(float) / 127.5)
        s = tk.summary(T)
        tr = s.pop("tracks")
        long = [t for t in tr if t["life"] >= 0.25 * T]
        mref = float(np.median([t["mass"] for t in long])) if long else 0.0
        major = [t for t in tr if t["mass"] >= 0.3 * mref and t["life"] >= 100]
        res.append({"threshold": thr, "factor": fac,
                    "n_bodies_median_2nd_half": s["n_bodies_median_2nd_half"], "n_long_tracks": s["n_long_tracks"],
                    "long_track_median_life": s["long_track_median_life"],
                    "major_life_median": float(np.median([t["life"] for t in major])) if major else 0.0,
                    "major_speed_median": float(np.median([t["speed"] for t in major])) if major else 0.0,
                    "major_fissions": sum(t["start"] == "split" for t in major),
                    "major_fusions": sum(t["end"] == "merged" for t in major),
                    "occupancy_median_2nd_half": s["occupancy_median_2nd_half"]})
        print(name, json.dumps(res[-1]))
    p = os.path.join(HERE, "worlds", name, "metrics.json")
    m = json.load(open(p))
    m["threshold_sensitivity"] = res
    json.dump(m, open(p, "w"))
