"""Checker: compare own control tables with summary.json control_tables; recount per-case order flips; per-case
ratio-rise ranges; a few more page card figures (vortex I_follow pooled probe, cips B_s_bath)."""
import json
from pathlib import Path
import numpy as np
R = Path("/home/user/evalwork/gc_suites/rescore_fair")
O = R / "checker" / "out"
SC = {f.stem: json.loads(f.read_text()) for f in O.glob("*__*.json")}
summ = json.loads((R / "results/summary.json").read_text())
der = json.loads((O / "derived.json").read_text())["control_tables"]
res = {"table_diffs": []}
for key in ("cips__main_iter2", "cips__formation", "phase_membrane__formation", "vortex__formation"):
    t = summ["control_tables"][key.replace("__", "/")]["controls"]
    for k, row in der[key]["plugin"]["rows"].items():
        for e, sfx in (("plugin", "old"), ("fair", "new")):
            mine = der[key][e]["rows"][k]
            th = t[k]
            for a, b in (("ratio", f"ratio_{sfx}"), ("ci90", f"ci90_{sfx}")):
                tv = th.get(b)
                ok = tv is not None and np.allclose(mine[a], tv, rtol=1e-12, atol=0)
                if not ok:
                    res["table_diffs"].append([key, k, e, a, mine[a], tv])
            if "separated" in mine and mine["separated"] is not None and th.get(f"separated_{sfx}") != mine["separated"]:
                res["table_diffs"].append([key, k, e, "separated", mine["separated"], th.get(f"separated_{sfx}")])
NATLIKE = {"independent_native", "band_native", "native_b", "numerical_null"}
flips = []
for key, S in SC.items():
    for c, ctl in S.items():
        ks = sorted(ctl)
        for i, a in enumerate(ks):
            for b in ks[i + 1:]:
                po = ctl[a]["plugin"]["agg"] - ctl[b]["plugin"]["agg"]
                fo = ctl[a]["fair"]["agg"] - ctl[b]["fair"]["agg"]
                if po * fo < 0:
                    gap = abs(ctl[a]["plugin"]["agg"] / ctl[b]["plugin"]["agg"] - 1)
                    flips.append([key, c, a, b, round(gap, 4)])
res["flips"] = len(flips)
res["flips_not_both_native_like"] = [f for f in flips if not ({f[2], f[3]} <= NATLIKE)]
res["flip_gap_range"] = [min(f[4] for f in flips), max(f[4] for f in flips)]
# per-case ratio rise (fair ratio / plugin ratio), non-native controls; ignore_actions on no-action cases is a native ensemble
rise = []
for key, S in SC.items():
    for c, ctl in S.items():
        n = ctl["independent_native"]
        sham = all(abs(ctl["ignore_actions"]["plugin"]["agg"] - 0) >= 0 for _ in [0]) if "ignore_actions" in ctl else False
        for k, v in ctl.items():
            if k in NATLIKE:
                continue
            f = (v["fair"]["agg"] / n["fair"]["agg"]) / (v["plugin"]["agg"] / n["plugin"]["agg"])
            rise.append((f, key, c, k))
rise.sort()
res["per_case_rise_all_non_native"] = [rise[0], rise[-1]]
# vortex main pooled probe (I_follow, I:k0) and cips main_iter1 B_s_bath (B:chis0)
vs = json.loads(Path("/home/user/evalwork/gc_suites/vortex/suite/suite.json").read_text())
vid = {c["program"]: c for c in vs["cases"]}
S = SC["vortex__main"]
def pr(e, cid, k, g=None):
    if g is None:
        return S[cid][k][e]["agg"] / (0.5 * (S[cid]["independent_native"][e]["agg"] + S[cid]["native_b"][e]["agg"]))
    return S[cid][k][e]["groups"][g] / (0.5 * (S[cid]["independent_native"][e]["groups"][g] + S[cid]["native_b"][e]["groups"][g]))
c = vid["I_follow"]; g = f"device{c['acting_device']}/{c['ports'][0]}"; sh = vid["sham"]["id"]
res["vortex_I_follow_probe_spec"] = {e: round(pr(e, c["id"], "k0", g), 2) / round(pr(e, sh, "k0", g), 2) for e in ("plugin", "fair")}
cs = json.loads(Path("/home/user/evalwork/gc_suites/cips/suite/suite.json").read_text())
cf = {x["family"]: x["request"]["id"] for x in cs["cases"]}
S2 = SC["cips__main_iter1"]
r = lambda e, cid: S2[cid]["ablate_chis0"][e]["agg"] / S2[cid]["independent_native"][e]["agg"]
res["cips_B_s_bath_spec"] = {e: r(e, cf["s_bath"]) / r(e, cf["sham"]) for e in ("plugin", "fair")}
(O / "check3.json").write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res, indent=0, default=str)[:4000])
