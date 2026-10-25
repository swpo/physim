"""Readout for the kstrail twin comparison: body counts over time and travel (labkit metrics).

python readout.py <seed dirs...>  -> one row per seed dir (needs metrics.json)."""
import json
import sys


def row(d):
    m = json.load(open(d + "/metrics.json"))
    n = m["series"]["n_comp"]
    mt = m["motion_top"]
    idx = [int(round(f * (len(n) - 1))) for f in (0.25, 0.5, 0.75, 1.0)]
    return {"run": d, "n_comp_t150_300_450_600": [n[i] for i in idx],
            "tracks_scored": len(mt), "travel_ge5BL": sum(x["body_lengths"] >= 5 for x in mt),
            "median_BL": sorted(x["body_lengths"] for x in mt)[len(mt) // 2] if mt else 0,
            "max_speed": round(max((x["speed"] for x in mt), default=0), 3),
            "median_size": round(sorted(x["size"] for x in mt)[len(mt) // 2], 1) if mt else 0}


if __name__ == "__main__":
    rows = [row(d) for d in sys.argv[1:]]
    for r in rows:
        print(json.dumps(r))
