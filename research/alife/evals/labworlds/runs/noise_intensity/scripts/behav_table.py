"""Table of the behaviour packs (out/behav/*/*/summary.json) -> out/behaviour.json and stdout."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "out"
KEYS = ("components_final", "components_mean", "persistent_tracks", "splits", "persistent_splits", "max_generation",
        "merges", "nucleations", "occupancy_final")
rows = []
for f in sorted(OUT.glob("behav/*/*/summary.json")):
    d = json.loads(f.read_text())
    s = d["summary"]
    r = dict(world=d["world"], level=d["level"], seed=d["seed"], status=d["status"], cpu_s=round(d["cpu_s"]),
             **{k: (round(s[k], 3) if isinstance(s.get(k), float) else s.get(k)) for k in KEYS})
    r["splits_after_t"] = s.get("splits_after_t")
    if "signs" in s:
        r["signs"] = s["signs"]
    rows.append(r)
rows.sort(key=lambda r: (r["world"], r["seed"], r["level"]))
(OUT / "behaviour.json").write_text(json.dumps(rows, indent=1))
for r in rows:
    print(json.dumps(r))
