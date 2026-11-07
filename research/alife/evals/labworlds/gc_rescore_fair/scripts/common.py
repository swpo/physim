"""Shared helpers for re-scoring the saved GC-suite forecasts with the plugin and fair ensemble estimators.

Nothing here simulates: forecasts and truths are read from the frozen suites' .npz files, and the deterministic
initial-persistence forecast is rebuilt from the no-action truth's t=0 readout (checked against the stored scores).
All output goes under OUT_ROOT; the suites themselves are only read.
"""
from __future__ import annotations

import json
import math
import os
import shutil
import sys
from pathlib import Path

os.environ["PHYSIM_PIN"] = ""          # the live tree (ad6d2eb), which has the estimator argument
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
ENV = "/home/user/swpo/residency-environments/environments/physim"
LWS = "/home/user/swpo/residency-environments/scripts/physim/labworlds"
for p in (LWS, ENV):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402
from physim import blobround6_eval as scoring  # noqa: E402

assert Path(scoring.__file__).resolve().is_relative_to(Path(ENV).resolve()), scoring.__file__
assert scoring.ESTIMATORS == ("fair", "plugin")

GC = Path("/home/user/evalwork/gc_suites")
OUT_ROOT = GC / "rescore_fair" / "out"
ESTS = ("plugin", "fair")
NEW_KEYS = ("estimator",)               # keys the patched score_case adds to its report


def load_npz(path):
    with np.load(path, allow_pickle=False) as z:
        n = sum(1 for k in z.files if k.startswith("query"))
        arrs = [z[f"query{i}"].copy() for i in range(n)]
        meta = json.loads(str(z["meta"])) if "meta" in z.files else None
    return arrs, meta


def roster_for(truth, device_slots=(13, 19)):
    return scoring.PublicRoster(n_ports=int(truth[0].shape[2]), device_slots=tuple(device_slots))


def score(case, pred, truth, groups, members, n_truth, roster, est):
    return scoring.score_case(case, {"samples": pred}, {"samples": truth}, groups=groups, n_samples=members,
                              n_truth=n_truth, roster=roster, estimator=est)


def persistence_from_truth(sham_truth, case, members, roster):
    """PersistencePredictor of the default-pose t=0 readout, taken from the no-action truth (deterministic at t=0)."""
    init = [a[0, 0] for a in sham_truth]
    for a in sham_truth:                 # every truth member reads the same at t=0
        assert np.array_equal(a[:, 0], np.broadcast_to(a[0, 0], a[:, 0].shape))
    p = scoring.PersistencePredictor(dict(zip(("device0", "device1", "global"), init)), roster=roster)
    return p.predict(case["actions"], case["queries"], n_samples=members)["samples"]


def strip(report):
    return {k: v for k, v in report.items() if k not in NEW_KEYS}


def diff(a, b, path=""):
    """List of (path, a, b) where two JSON-like trees differ (exact comparison of numbers)."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((f"{path}/{k}", a.get(k, "<missing>"), b.get(k, "<missing>")))
            else:
                out += diff(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, f"len {len(a)}", f"len {len(b)}"))
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                out += diff(x, y, f"{path}[{i}]")
    elif isinstance(a, float) or isinstance(b, float):
        if not (a == b or (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b))):
            out.append((path, a, b))
    elif a != b:
        out.append((path, a, b))
    return out


def max_rel(d):
    vals = [abs(x - y) / max(abs(x), abs(y), 1e-300) for _, x, y in d
            if isinstance(x, (int, float)) and isinstance(y, (int, float))]
    return max(vals) if vals else 0.0


def jdump(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, allow_nan=False) + "\n")


def jload(path):
    return json.loads(Path(path).read_text())


def shadow(src_suite_dir, dst):
    """A fresh shadow folder holding a copy of suite.json (reports read it; scores are written by the caller)."""
    dst = Path(dst)
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    shutil.copy2(Path(src_suite_dir) / "suite.json", dst / "suite.json")
    return dst


def spread_terms(pred, truth, groups):
    """Per group: cross term A (mean pred-truth distance) and mean spread over distinct member pairs S, so that
    energy(plugin) = A - 0.5 (m-1)/m S and energy(fair) = A - 0.5 S (the score_case group selection, RMS norm)."""
    out = {}
    for g in groups:
        def sel(arrays):
            return np.column_stack([arrays[s["query"]][:, s["time_index"], s["port"], s["slot"]]
                                    for s in g["selectors"]]) / np.asarray(g["scales"])
        x, y = sel(pred), sel(truth)
        m = len(x)
        a = scoring._mean_rms_distance(x, y)
        allpairs = scoring._mean_rms_distance(x, x)
        out[g["id"]] = dict(A=a, S=allpairs * m / (m - 1) if m > 1 else 0.0)
    return out


class Recorder:
    """Collects one row per (suite, case, control): scores under both estimators and the plugin check."""

    def __init__(self, world):
        self.world = world
        self.rows = []
        self.mismatches = []

    def add(self, suite, case_id, program, control, members, plugin, fair, stored, source, spread=None, note=None):
        """plugin/fair/stored: score_case reports (dicts); stored may be None when nothing was saved."""
        if stored is not None:
            d = diff(strip(stored), strip(plugin))
            if d:
                self.mismatches.append(dict(world=self.world, suite=suite, case=case_id, control=control,
                                            n_differences=len(d), max_rel_diff=max_rel(d),
                                            first=[[str(v) for v in x] for x in d[:3]]))
        gp = {x["id"]: x["energy_score"] for x in plugin["joint_energy"]}
        gf = {x["id"]: x["energy_score"] for x in fair["joint_energy"]}
        self.rows.append(dict(world=self.world, suite=suite, case=case_id, program=program, control=control,
                              members=members, agg_plugin=plugin["joint_energy_equal_group_mean"],
                              agg_fair=fair["joint_energy_equal_group_mean"], groups_plugin=gp, groups_fair=gf,
                              stored_checked=stored is not None,
                              plugin_matches_stored=(stored is not None and not diff(strip(stored), strip(plugin))),
                              spread=spread, source=str(source), note=note))


def pmcips_rescore(world, label, suite_dir, out_dir, rec, members_key="forecast_members"):
    """Re-score every stored (case, control) of a labeval/pmcips-format suite (controls/<case>/scores.json).
    Writes out_dir/<est>/suite.json and controls/<case>/scores.json for both estimators."""
    suite_dir = Path(suite_dir)
    suite = jload(suite_dir / "suite.json")
    M, NT = suite[members_key], suite["truth_members"]
    dst = {e: shadow(suite_dir, Path(out_dir) / e) for e in ESTS}
    sham = next(c for c in suite["cases"] if not c["request"]["actions"])
    sham_truth, _ = load_npz(suite_dir / sham["truth"])
    ignore = load_npz(suite_dir / "ignore_actions.npz")[0] if (suite_dir / "ignore_actions.npz").exists() else None
    for entry in suite["cases"]:
        case, cid = entry["request"], entry["request"]["id"]
        sp = suite_dir / "controls" / cid / "scores.json"
        if not sp.exists():
            continue
        stored = jload(sp)
        groups = suite["groups_by_horizon"][str(entry["horizon"])] if "groups_by_horizon" in suite else suite["groups"]
        truth, _ = load_npz(suite_dir / entry["truth"])
        nt = truth[0].shape[1]
        rost = roster_for(truth, [d["k"] for d in suite["devices"]])
        res = {e: {} for e in ESTS}
        for name in stored:
            npz = suite_dir / "controls" / cid / f"{name}.npz"
            if name == "initial_persistence":
                pred, src = persistence_from_truth(sham_truth, case, M, rost), f"persistence of {sham['truth']} t=0"
            elif npz.exists():
                pred, src = load_npz(npz)[0], npz
            elif name in ("ignore_actions", "band_native"):
                pred, src = [a[:, :nt] for a in ignore], suite_dir / "ignore_actions.npz"
            else:
                raise FileNotFoundError(npz)
            assert all(len(a) == M for a in pred), (cid, name, [a.shape for a in pred])
            for e in ESTS:
                res[e][name] = score(case, pred, truth, groups, M, NT, rost, e)
            rec.add(label, cid, entry["family"], name, M, res["plugin"][name], res["fair"][name], stored[name], src,
                    spread=spread_terms(pred, truth, groups))
        for e in ESTS:
            jdump(dst[e] / "controls" / cid / "scores.json", res[e])
    return suite, dst


def jload_str(obj):
    """Round-trip through JSON, as the suites' report writers did (numpy scalars become floats)."""
    return json.loads(json.dumps(obj))
