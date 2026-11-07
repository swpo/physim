"""Checker: a few more page caveat numbers from own scores (cips formation null per case, cips moat null vs band,
phase_membrane B_links_core chi0 specificity ranges)."""
import json
from pathlib import Path
import numpy as np
GC = Path("/home/user/evalwork/gc_suites")
O = GC / "rescore_fair/checker/out"
SC = {f.stem: json.loads(f.read_text()) for f in O.glob("*__*.json")}
E = ("plugin", "fair")


def ratio(key, e, c, k, dev=None):
    S = SC[key][c]
    if dev is None:
        return S[k][e]["agg"] / S["independent_native"][e]["agg"]
    m = lambda kk: np.mean([v for g, v in S[kk][e]["groups"].items() if g.startswith(dev + "/")])
    return float(m(k) / m("independent_native"))


def fam(p):
    return {c["family"]: c["request"]["id"] for c in json.loads((p / "suite.json").read_text())["cases"]}


out = {}
f = fam(GC / "cips/formation/suite")
out["cips_formation_null_case"] = {e: {p: ratio("cips__formation", e, f[p], "numerical_null") for p in ("sham", "keep_empty")} for e in E}
f = fam(GC / "cips/iter2/suite")
out["cips_moat_null_vs_band"] = {e: dict(null=ratio("cips__main_iter2", e, f["moat_C4"], "numerical_null"),
                                         null_by_sensor=[ratio("cips__main_iter2", e, f["moat_C4"], "numerical_null", d) for d in ("device0", "device1", "global")],
                                         band=ratio("cips__main_iter2", e, f["moat_C4"], "band_native")) for e in E}
sp = json.loads((GC / "phase_membrane/suite/specificity.json").read_text())["specificity"]["B"]
f = fam(GC / "phase_membrane/suite")
rows = {e: [] for e in E}
for r in sp["programs"]:
    for e in E:
        s = ratio("phase_membrane__main_iter1", e, r["case"], "ablate_chi0") / ratio("phase_membrane__main_iter1", e, f["sham"], "ablate_chi0")
        a = ratio("phase_membrane__main_iter1", e, r["case"], "ablate_chi0", r["acting"]) / ratio("phase_membrane__main_iter1", e, f["sham"], "ablate_chi0", r["acting"])
        rows[e].append((r["program"], round(s, 2), round(a, 2)))
out["pm_B_chi0"] = {e: dict(spec=[min(x[1] for x in rows[e]), max(x[1] for x in rows[e])],
                            acting=[min(x[2] for x in rows[e]), max(x[2] for x in rows[e])], rows=rows[e]) for e in E}
(O / "check4.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=0)[:3000])
