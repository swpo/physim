"""Checker: every program-level specificity row of the pm/cips/rods suites recomputed from own scores (plugin must
reproduce the stored rounded row; fair gives the new row); tag changes with the build_gc rule (>= 1.5 on the
rounded figures) compared with summary.json specificity / specificity_tag_changes."""
import json
from pathlib import Path
import numpy as np
GC = Path("/home/user/evalwork/gc_suites")
R = GC / "rescore_fair"
O = R / "checker/out"
SC = {f.stem: json.loads(f.read_text()) for f in O.glob("*__*.json")}
SUITES = {("phase_membrane", "main_iter1"): GC / "phase_membrane/suite", ("phase_membrane", "main_iter2"): GC / "phase_membrane/iter2/suite",
          ("phase_membrane", "formation"): GC / "phase_membrane/formation/suite", ("cips", "main_iter1"): GC / "cips/suite",
          ("cips", "main_iter2"): GC / "cips/iter2/suite", ("cips", "formation"): GC / "cips/formation/suite",
          ("rods", "main_iter1"): GC / "rods/suite", ("rods", "main_iter2"): GC / "rods/iter2/suite", ("rods", "formation"): GC / "rods/formation/suite"}


def ratio(key, e, c, k, dev=None):
    S = SC[key][c]
    if dev is None:
        return S[k][e]["agg"] / S["independent_native"][e]["agg"]
    m = lambda kk: np.mean([v for g, v in S[kk][e]["groups"].items() if g.startswith(dev + "/")])
    return float(m(k) / m("independent_native"))


def tag(s, a):
    return "specific" if s >= 1.5 else "at the probe" if a >= 1.5 else "whole-world"


summ = json.loads((R / "results/summary.json").read_text())
theirs = {(x["world"], x["suite"], x["key"].split(":")[-1].removeprefix("ablate_"), x["program"]): x for x in summ["specificity"]}
n = plugin_bad = 0
changes, disagree, factors = [], [], []
for (w, lab), d in SUITES.items():
    key = f"{w}__{lab}"
    fam = {c["family"]: c["request"]["id"] for c in json.loads((d / "suite.json").read_text())["cases"]}
    sham = fam["sham"]
    if w == "rods":
        sp = json.loads((d / "report.json").read_text())["specificity"]
        blocks = [(v["control"], v["programs"]) for v in sp.values()]
    else:
        sp = json.loads((d / "specificity.json").read_text())
        blocks = [(sp["control"], sp["programs"])] if "programs" in sp else [(v["control"], v["programs"]) for v in sp["specificity"].values()]
    for ctl, rows in blocks:
        k = f"ablate_{ctl}"
        for r in rows:
            if r["case"] == sham:
                continue
            n += 1
            v = {}
            for e in ("plugin", "fair"):
                s = round(ratio(key, e, r["case"], k) / ratio(key, e, sham, k), 2)
                a = round(ratio(key, e, r["case"], k, r["acting"]) / ratio(key, e, sham, k, r["acting"]), 2)
                v[e] = (s, a, tag(s, a))
            if (v["plugin"][0], v["plugin"][1]) != (r["specificity"], r["specificity_acting"]):
                plugin_bad += 1
            factors.append(v["fair"][0] / v["plugin"][0])
            if v["plugin"][2] != v["fair"][2]:
                changes.append([w, lab, ctl, r["program"], v["plugin"], v["fair"]])
            t = theirs.get((w, lab, ctl, r["program"]))
            if t is None or abs(t["specificity_new"] - v["fair"][0]) > 0.0051 or t["tag_new"] != v["fair"][2]:
                disagree.append([w, lab, ctl, r["program"], v["fair"], None if t is None else (t["specificity_new"], t["tag_new"])])
out = dict(rows=n, plugin_rows_not_reproduced=plugin_bad, tag_changes=changes, disagree_with_summary=disagree,
           fair_over_plugin_factor=[min(factors), float(np.median(factors)), max(factors)])
(O / "check5.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=0))
