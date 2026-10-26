"""(c27) One row per front cut across all twinrepair runs: repair (ring closure >= 0.9, area back to pre-cut),
death, and swimming after repair (motion.py's stretch from +340 to the first split/merge/loss)."""
import json, glob, subprocess, sys, numpy as np
rows = []
mot = {}
for fn in sorted(glob.glob("tr/*/result.json")):
    r = json.load(open(fn))
    have_tracks = all("tracks" in c for c in r["cells"])
    if have_tracks:
        out = subprocess.run([sys.executable, "motion.py", fn], capture_output=True, text=True).stdout
        for line in out.splitlines():
            d = json.loads(line); mot[(d["file"], d["cell"])] = d
    for c in r["cells"]:
        if c["mode"] != "front": continue
        tag = fn.split("/")[1]; d, t = c["cut"], c["twin"]
        m = mot.get((tag, c["cell"]), {})
        rows.append({"run": tag, "seed": r["seed"], "cell": c["cell"], "area": c["area"], "wound_S": "kept" if c["damage"].get("keep_S") else "bath",
                     "erased_frac": round(c["damage"]["erased_frac"], 2), "erased_L_frac": round(c["damage"]["erased_L_frac"], 2),
                     "closure_after_cut": d.get("closure_t", [[0, None]])[0][1], "closure_ge_0.9_at": d.get("first_closure_ge_0p9"),
                     "area_back_at": d.get("area_back_to_start_at"), "cut_lost_at": d["lost_at"], "twin_lost_at": t["lost_at"],
                     "cut_ring_ge_1.5_2nd_half": d["frac_ring_ge_1p5_2nd_half"],
                     "swim_after_repair_BL": m.get("cut", {}).get("net_BL"), "twin_swim_BL": m.get("twin", {}).get("net_BL"),
                     "stretch": m.get("cut", {}).get("stretch")})
for x in rows: print(json.dumps(x))
rep = [x for x in rows if x["cut_lost_at"] is None or (x["twin_lost_at"] is not None and x["cut_lost_at"] >= x["twin_lost_at"] - 200) or (x["cut_lost_at"] or 0) > 600]
dead = [x for x in rows if x not in rep]
print(f"front cuts: {len(rows)}; repaired (survive the repair window, +600): {len(rep)}; died early: {len(dead)} at {[x['cut_lost_at'] for x in dead]} with closure after cut {[x['closure_after_cut'] for x in dead]}")
print("closure after cut, repaired:", sorted([x['closure_after_cut'] for x in rep if x['closure_after_cut'] is not None]))
json.dump(rows, open("table.json", "w"), indent=1)
