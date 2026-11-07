"""Add fragment-robust event counts to worlds/NAME/metrics.json: 'major' bodies are tracks
with median mass >= 30% of the median mass of the long-lived bodies and life >= 100 steps;
a major fission is the birth of such a body by split, a major fusion the end of such a body
by merging. Usage: python major_events.py NAME..."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for name in sys.argv[1:]:
    p = os.path.join(HERE, "worlds", name, "metrics.json")
    m = json.load(open(p))
    T = m["steps"]
    tr = m["tracks"]
    long = [t for t in tr if t["life"] >= 0.25 * T]
    mref = float(np.median([t["mass"] for t in long])) if long else float(np.median([t["mass"] for t in tr]))
    major = [t for t in tr if t["mass"] >= 0.3 * mref and t["life"] >= 100]
    moving = [t for t in major if t["life"] > 0]
    out = {"definition": "major body: track median mass >= 0.3 x median mass of long-lived bodies, life >= 100 steps",
           "ref_body_mass": mref,
           "n_major_tracks": len(major),
           "major_fissions": sum(t["start"] == "split" for t in major),
           "major_fusions": sum(t["end"] == "merged" for t in major),
           "major_vanish": sum(t["end"] == "vanish" for t in major),
           "major_appear": sum(t["start"] == "appear" for t in major),
           "major_life_median": float(np.median([t["life"] for t in major])),
           "major_life_p90": float(np.percentile([t["life"] for t in major], 90)),
           "major_speed_median_px_per_step": float(np.median([t["speed"] for t in moving])),
           "major_body_len_median_px": float(np.median([t["body_len"] for t in major])),
           "major_lengths_travelled_median": float(np.median([t["lengths_travelled"] for t in major])),
           "major_net_lengths_median": float(np.median([t["net_lengths"] for t in major])),
           "major_frac_travel_ge3_lengths": float(np.mean([t["lengths_travelled"] >= 3 for t in major])),
           "fragment_tracks": len(tr) - len(major)}
    m["major_events"] = out
    json.dump(m, open(p, "w"))
    print(name, json.dumps(out))
