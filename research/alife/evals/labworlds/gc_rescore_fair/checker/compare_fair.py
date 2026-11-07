"""Compare the checker's own fair/plugin scores (checker/out) with the rescorer's shadow scores (out/<w>/<suite>/{fair,plugin})."""
import json
from pathlib import Path
R = Path("/home/user/evalwork/gc_suites/rescore_fair")
res = {}
for f in sorted((R / "checker" / "out").glob("*__*.json")):
    w, lab = f.stem.split("__")
    mine = json.loads(f.read_text())
    for e in ("plugin", "fair"):
        d = R / "out" / w / lab / e
        n = bad = 0
        maxrel = 0.0
        for cid, ctl in mine.items():
            if w == "vortex":
                theirs = json.loads((d / "scores.json").read_text())[cid]
                th = {k: v for k, v in theirs.items()}
            else:
                raw = json.loads((d / "controls" / cid / "scores.json").read_text())
                th = {k: dict(agg=v["joint_energy_equal_group_mean"], groups={g["id"]: g["energy_score"] for g in v["joint_energy"]}) for k, v in raw.items()}
            assert set(th) == set(ctl), (w, lab, cid, set(th) ^ set(ctl))
            for k, v in ctl.items():
                n += 1
                a, b = v[e], th[k]
                if a != b:
                    bad += 1
                    maxrel = max(maxrel, abs(a["agg"] - b["agg"]) / abs(a["agg"]))
        res[f"{w}/{lab}/{e}"] = dict(n=n, differ=bad, max_rel=maxrel)
print(json.dumps(res, indent=0))
(R / "checker" / "out" / "compare_with_shadow.json").write_text(json.dumps(res, indent=1))
