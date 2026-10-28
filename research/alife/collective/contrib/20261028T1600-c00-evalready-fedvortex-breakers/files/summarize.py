"""table of the noise battery: labkit summary + splits.py sign analysis + field means from the rendered frames"""
import json, glob, os, re
import numpy as np

D = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs"
rows = []
for p in sorted(glob.glob(D + "/*_s*")):
    name = os.path.basename(p)
    mt = re.match(r"([A-Z])([0-9.]+)_s(\d+)", name)
    if not mt or not os.path.exists(p + "/metrics.json"):
        continue
    form, sd, seed = mt.group(1), float(mt.group(2)), int(mt.group(3))
    m = json.load(open(p + "/metrics.json"))
    S = m["summary"]
    sp = json.load(open(p + "/splits.json")) if os.path.exists(p + "/splits.json") else {}
    F = np.load(p + "/frames.npz")
    r = F["render"].astype(np.float32)
    late = r[len(r) // 2:]
    n_late = np.mean(m["series"]["n_comp"][len(m["series"]["n_comp"]) // 2:])
    sp_t = [s["t"] for s in sp.get("splits", [])]
    rows.append(dict(form=form, sd=sd, seed=seed, status=m["status"],
                     n_final=S["components_final"], n_late=round(float(n_late), 1),
                     psplits=S["persistent_splits"], psplits_after300=sum(t > 300 for t in sp_t),
                     gen=S["max_generation"], merges=S["merges"], ms=S["merge_split_ratio"], nucl=S["nucleations"],
                     same=sp.get("daughters_same_sign"), other=sp.get("daughters_other_sign"), unk=sp.get("sign_unknown"),
                     mg_same=sp.get("merges_same_sign"), mg_opp=sp.get("merges_opposite_sign"),
                     moving=S["moving_tracks"], maxBL=round(S["max_body_lengths"], 1), vmax=round(S["max_speed"], 3),
                     occ=round(S["occupancy_final"], 3), Ylate=round(float(late[:, 1].mean()), 3),
                     absw_late=round(float(late[:, 0].mean()), 4), absw_max=round(float(late[:, 0].max()), 3),
                     sdw_late=round(float(late[:, 2].std()), 3) if False else None))
keys = ["form", "sd", "seed", "status", "n_final", "n_late", "psplits", "psplits_after300", "gen", "merges", "ms", "nucl",
        "same", "other", "unk", "mg_same", "mg_opp", "moving", "maxBL", "vmax", "occ", "Ylate", "absw_late", "absw_max"]
print("| " + " | ".join(keys) + " |")
print("|" + "---|" * len(keys))
for r in sorted(rows, key=lambda r: (r["form"] if r["sd"] > 0 else "0", r["sd"], r["seed"])):
    print("| " + " | ".join(str(r[k]) for k in keys) + " |")
json.dump(rows, open(os.path.dirname(D) + "/out/noise_battery.json", "w"), indent=1)
