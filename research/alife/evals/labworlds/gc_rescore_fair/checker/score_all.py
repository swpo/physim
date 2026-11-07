"""Independent checker: re-score every stored (suite, case, control) of the 12 GC suites in use from the saved
forecasts with blobround6_eval.score_case under 'plugin' and 'fair'. Forecast lookup follows the suites' own
scripts (vortex/scripts/suite.py, vortex/scripts2/suite2.py, gsuite/iter2/formation/fsuite run()).
Writes checker/out/<world>__<suite>.json = {cid: {control: {plugin: {agg, groups}, fair: {agg, groups}}}} and
checker/out/plugin_check.json (exact comparison of the full plugin report with the stored one)."""
import json, os, sys, time
from pathlib import Path
os.environ["OMP_NUM_THREADS"] = "1"
sys.path[:0] = ["/home/user/swpo/residency-environments/environments/physim",
                "/home/user/swpo/residency-environments/scripts/physim/labworlds"]
import numpy as np
from physim import blobround6_eval as sc

GC = Path("/home/user/evalwork/gc_suites")
OUT = GC / "rescore_fair" / "checker" / "out"
PM = {("phase_membrane", "main_iter1"): GC / "phase_membrane/suite",
      ("phase_membrane", "main_iter2"): GC / "phase_membrane/iter2/suite",
      ("phase_membrane", "formation"): GC / "phase_membrane/formation/suite",
      ("cips", "main_iter1"): GC / "cips/suite", ("cips", "main_iter2"): GC / "cips/iter2/suite",
      ("cips", "formation"): GC / "cips/formation/suite",
      ("rods", "main_iter1"): GC / "rods/suite", ("rods", "main_iter2"): GC / "rods/iter2/suite",
      ("rods", "formation"): GC / "rods/formation/suite"}
VX = {("vortex", "main"): GC / "vortex/suite", ("vortex", "formation"): GC / "vortex/formation",
      ("vortex", "long2"): GC / "vortex/long2"}


def npz(p):
    with np.load(p, allow_pickle=False) as z:
        n = len([k for k in z.files if k.startswith("query")])
        return [z[f"query{i}"].copy() for i in range(n)]


def persistence(truths_t0, case, m, rost):
    p = sc.PersistencePredictor(dict(zip(("device0", "device1", "global"), truths_t0)), roster=rost)
    return p.predict(case["actions"], case["queries"], n_samples=m)["samples"]


def eq(a, b):
    """exact equality of JSON-like trees (floats compared with ==)."""
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(eq(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b))
    return a == b


def two(case, pred, truth, groups, m, nt, rost):
    r = {e: sc.score_case(case, {"samples": pred}, {"samples": truth}, groups=groups, n_samples=m, n_truth=nt,
                          roster=rost, estimator=e) for e in ("plugin", "fair")}
    return r


def short(r):
    return dict(agg=r["joint_energy_equal_group_mean"], groups={g["id"]: g["energy_score"] for g in r["joint_energy"]})


check = {"n": 0, "exact": 0, "mismatch": []}
t0 = time.process_time()
for (w, lab), d in PM.items():
    s = json.loads((d / "suite.json").read_text())
    M, NT = s["forecast_members"], s["truth_members"]
    sham = next(c for c in s["cases"] if not c["request"]["actions"])
    t0s = [a[0, 0] for a in npz(d / sham["truth"])]
    ign = npz(d / "ignore_actions.npz")
    res = {}
    for c in s["cases"]:
        case, cid = c["request"], c["request"]["id"]
        sp = d / "controls" / cid / "scores.json"
        if not sp.exists():
            continue
        stored = json.loads(sp.read_text())
        groups = s["groups_by_horizon"][str(c["horizon"])] if "groups_by_horizon" in s else s["groups"]
        truth = npz(d / c["truth"])
        rost = sc.PublicRoster(n_ports=int(truth[0].shape[2]), device_slots=tuple(int(x["k"]) for x in s["devices"]))
        res[cid] = {}
        for name in stored:
            f = d / "controls" / cid / f"{name}.npz"
            if name == "initial_persistence":
                pred = persistence(t0s, case, M, rost)
            elif f.exists():
                pred = npz(f)
            elif name == "ignore_actions" or (name == "band_native" and c["family"] == "sham"):
                pred = [a[:, :truth[0].shape[1]] for a in ign]
            else:
                raise FileNotFoundError(f)
            r = two(case, pred, truth, groups, M, NT, rost)
            p = {k: v for k, v in r["plugin"].items() if k != "estimator"}
            check["n"] += 1
            if eq(p, stored[name]):
                check["exact"] += 1
            else:
                check["mismatch"].append([w, lab, cid, name])
            res[cid][name] = {e: short(r[e]) for e in r}
    (OUT / f"{w}__{lab}.json").write_text(json.dumps(res))
    print(w, lab, check["n"], check["exact"], round(time.process_time() - t0, 1), flush=True)

for (w, lab), d in VX.items():
    s = json.loads((d / "suite.json").read_text())
    stored = json.loads((d / "scores.json").read_text())
    groups = [dict(g, unit=("global mean and variance; frozen calibration scales" if g["id"].startswith("global")
                            else "native field units; frozen calibration scale")) for g in s["groups"]]
    sham = next(c for c in s["cases"] if not c["request"]["actions"])
    t0s = [a[0, 0] for a in npz(d / sham["truth"])]
    res = {}
    for c in s["cases"]:
        case, cid = c["request"], c["id"]
        truth = npz(d / c["truth"])
        rost = sc.PublicRoster(n_ports=int(truth[0].shape[2]), device_slots=(13, 19))
        res[cid] = {}
        for name in stored[cid]:
            if name == "initial_persistence":
                pred = persistence(t0s, case, 4, rost)
            else:
                if lab == "main":
                    if name == "ignore_actions":
                        f = d / "controls" / "ignore_actions.npz"
                    elif name == "independent_native" or name in ("adv0", "eps0", "k0", "kl0", "mu0"):
                        f = d / "ens" / c["program"] / ("native.npz" if name == "independent_native" else f"{name}.npz")
                    else:
                        f = d / "controls" / cid / f"{name}.npz"
                else:
                    if name == "ignore_actions" or (name == "native_b" and cid == sham["id"]):
                        f = d / "controls" / "ignore_actions.npz"
                    else:
                        f = d / "controls" / cid / f"{name}.npz"
                pred = [a[:4] for a in npz(f)]
            r = two(case, pred, truth, groups, 4, 2, rost)
            check["n"] += 1
            if eq(short(r["plugin"]), stored[cid][name]):
                check["exact"] += 1
            else:
                check["mismatch"].append([w, lab, cid, name])
            res[cid][name] = {e: short(r[e]) for e in r}
    (OUT / f"{w}__{lab}.json").write_text(json.dumps(res))
    print(w, lab, check["n"], check["exact"], round(time.process_time() - t0, 1), flush=True)
check["cpu_s"] = time.process_time() - t0
(OUT / "plugin_check.json").write_text(json.dumps(check, indent=1))
print(json.dumps(check)[:2000])
