"""Summarise stage-1 search results: fractions per stratum and the top runs by score.
Usage: python analyze.py [N_TOP]"""
import glob
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(pattern):
    rs = []
    for f in sorted(glob.glob(pattern)):
        for line in open(f):
            rs.append(json.loads(line))
    return rs


def classify(r):
    ok = r["status"] == "ok"
    loc = ok and r["occupancy_median_2nd_half"] < 0.35 and r["n_bodies_median_2nd_half"] >= 1
    several = loc and r["n_bodies_median_2nd_half"] >= 3 and r["max_body_frac_final"] < 0.6
    persist = several and r["n_long_tracks"] >= 3
    moving = persist and r["long_track_median_lengths"] >= 3
    inter = moving and (r["merges"] + r["splits"] + r["contact_events"]) >= 3
    return {"ok": ok, "localized": loc, "several": several, "persistent": persist, "moving": moving,
            "interacting": inter}


def main():
    ntop = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    rs = load(os.path.join(HERE, "search", "results_w*.jsonl"))
    print("runs", len(rs), "cpu_s", round(sum(r["secs"] for r in rs)))
    out = {"n_runs": len(rs), "cpu_seconds": sum(r["secs"] for r in rs), "strata": {}}
    for st in ("paper", "shrunk", "all"):
        sub = [r for r in rs if st == "all" or r["stratum"] == st]
        if not sub:
            continue
        cl = [classify(r) for r in sub]
        fr = {k: float(np.mean([c[k] for c in cl])) for k in cl[0]}
        stat = {s: int(sum(r["status"] == s for r in sub)) for s in ("ok", "sea", "dissolved", "nan")}
        out["strata"][st] = {"n": len(sub), "fractions": fr, "status": stat}
        print(st, len(sub), stat, {k: round(v, 3) for k, v in fr.items()})
        for C in (1, 2, 3):
            s2 = [classify(r) for r in sub if r["C"] == C]
            if s2:
                print("   C", C, len(s2), {k: round(float(np.mean([c[k] for c in s2])), 3) for k in ("localized", "several", "persistent", "moving", "interacting")})
    rs.sort(key=lambda r: -r["score"])
    print("top by score:")
    for r in rs[:ntop]:
        print(r["i"], r["stratum"], "C", r["C"], "k", r["k"], "Rs", round(r["R_scale"], 2), "nb", r["n_bodies_median_2nd_half"],
              "long", r["n_long_tracks"], "len", round(r["long_track_median_lengths"], 1),
              "mv3", round(r["long_track_frac_moving3"], 2), "ev", r["merges"], r["splits"], r["contact_events"],
              "occ", round(r["occupancy_median_2nd_half"], 2), "dom", round(r["max_body_frac_final"], 2),
              "score", round(r["score"], 3))
    out["top"] = [r["i"] for r in rs[:ntop]]
    with open(os.path.join(HERE, "search", "summary.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
