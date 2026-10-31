"""Scores, ratios and rewards for the fed-vortex lab bundle (see fedvortex_bundle.py).

Every predictor is scored with blobround6_eval.score_case on the bundle's frozen groups and retained truths.
The 64-member native reference gives (a) the native score of a 64-member predictor, from which the reward
follows (rewards.precision_reward, calibrated K), and (b) 16 independent 4-member slices: their mean is the
reference for every 4-member control and their spread is the native band. A control fails on a case when its
ratio to the slice mean exceeds the largest slice ratio on that case.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import fedvortex_bundle as FB
import numpy as np
from physim import blobround6_eval as scoring
from physim import labbundle as LB
from physim.rewards import DEFAULT_PRECISION, precision_reward

TARGETS = {   # program -> the mechanism controls it is designed to provoke
    "sham": ["ablate_body_gain", "ablate_adv0"],
    "feed_neck": ["ablate_body_gain", "ablate_k0"],
    "starve_neck": ["ablate_body_gain", "ablate_mu0"],
    "delayed_feed": ["ablate_body_gain", "ablate_mu0"],
    "feed_vortex": ["ablate_k0"],
    "starve_vortex": ["ablate_mu0"],
    "stir_cut": ["ablate_k0", "ablate_mu0"],
    "follow_vortex": ["ablate_adv0"],
    "feed_and_follow": ["ablate_adv0", "ablate_k0"],
}


def _load(path, n=None):
    with np.load(path, allow_pickle=False) as z:
        meta = json.loads(str(z["meta"]))
        arrays = [z[f"query{i}"].copy() for i in range(len(meta["queries"]))]
        cpu = float(z["cpu_s"])
    if n is not None:
        arrays = [a[:n] for a in arrays]
    return arrays, meta, cpu


def _boot(num, den, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(num), size=(n, len(num)))
    r = num[idx].mean(axis=1) / den[idx].mean(axis=1)
    return [float(np.quantile(r, 0.05)), float(np.quantile(r, 0.95))]


def report(out: Path, work: Path):
    bundle = LB.open_bundle(out, profile="evaluation")
    cases = bundle.suite["cases"]
    cdir = work / "controls"
    gids = [g["id"] for g in cases[0]["groups"]]
    rows, cpu = {}, 0.0
    ignore, _, c0 = _load(cdir / "ignore_actions.npz", FB.CONTROL_MEMBERS)
    cpu += c0
    sensors = ["device0", "device1", "global"]
    init = bundle.make_oracle().sample_truth([], [dict(sensor=s, t=[0]) for s in sensors], 1, truth_seed=0)["samples"]
    persistence = scoring.PersistencePredictor(dict(zip(sensors, [a[0, 0] for a in init])), roster=bundle.roster)

    def score(record, samples, n):
        r = scoring.score_case(record["request"], {"samples": samples}, truth, groups=record["groups"], n_samples=n,
                               n_truth=2, roster=bundle.roster, limits=bundle.limits)
        return r["joint_energy_equal_group_mean"], {g["id"]: g["energy_score"] for g in r["joint_energy"]}

    for i, record in enumerate(cases):
        cid, fam = record["request"]["id"], record["family"]
        truth = bundle.truth(record)
        ref_path = cdir / f"reference_{cid}.npz"
        if not ref_path.exists():
            continue
        ref, meta, c = _load(ref_path)
        cpu += c
        row = dict(family=fam, controls={})
        row["native64"] = score(record, ref, 64)
        slices = [score(record, [a[k * FB.SLICE:(k + 1) * FB.SLICE] for a in ref], FB.SLICE) for k in range(64 // FB.SLICE)]
        row["slices"] = slices
        row["native4_mean"] = float(np.mean([s[0] for s in slices]))
        row["native4_group_mean"] = {g: float(np.mean([s[1][g] for s in slices])) for g in gids}
        row["band"] = [min(s[0] for s in slices) / row["native4_mean"], max(s[0] for s in slices) / row["native4_mean"]]
        row["controls"]["ignore_actions"] = score(record, ignore, FB.CONTROL_MEMBERS)
        row["controls"]["initial_persistence"] = score(
            record, persistence.predict(record["request"]["actions"], record["request"]["queries"], FB.CONTROL_MEMBERS)["samples"],
            FB.CONTROL_MEMBERS)
        for name in FB.CONTROLS:
            p = cdir / f"{name}_{cid}.npz"
            if p.exists():
                arr, _, c = _load(p)
                cpu += c
                row["controls"][name] = score(record, arr, FB.CONTROL_MEMBERS)
        rows[cid] = row
    # No "independent_native" row: slices of the 64-member reference define the band; the
    # dt-halved null (its own seeds) is the independent check.
    names = ["ignore_actions", "initial_persistence"] + FB.CONTROLS
    res = dict(world="c53-fed-vortices", bundle_id=bundle.manifest["bundle_id"], cases_scored=len(rows),
               control_members=FB.CONTROL_MEMBERS, reference_members=64, per_case={}, aggregate={}, groups={},
               targeted={}, simulation_cpu_h=cpu / 3600)
    for cid, row in rows.items():
        res["per_case"][cid] = dict(family=row["family"], native64=row["native64"][0], native4=row["native4_mean"],
                                    band=row["band"],
                                    ratio={k: v[0] / row["native4_mean"] for k, v in row["controls"].items()})
    for name in names:
        have = [c for c in rows if name in rows[c]["controls"]]
        if not have:
            continue
        num = np.array([rows[c]["controls"][name][0] for c in have])
        den = np.array([rows[c]["native4_mean"] for c in have])
        fails = [c for c in have if res["per_case"][c]["ratio"][name] > rows[c]["band"][1]]
        res["aggregate"][name] = dict(cases=len(have), ratio=float(num.mean() / den.mean()), ci90=_boot(num, den),
                                      cases_beyond_band=len(fails), cases_within_band=[rows[c]["family"] for c in have if c not in fails])
        res["groups"][name] = {}
        for g in gids:
            gn = np.array([rows[c]["controls"][name][1][g] for c in have])
            gd = np.array([rows[c]["native4_group_mean"][g] for c in have])
            res["groups"][name][g] = dict(ratio=float(gn.mean() / gd.mean()), ci90=_boot(gn, gd))
    # group-level native band: each slice's case-mean group score over the slice mean
    res["group_band"] = {}
    for g in gids:
        per_slice = np.array([[rows[c]["slices"][k][1][g] for c in rows] for k in range(64 // FB.SLICE)]).mean(axis=1)
        res["group_band"][g] = [float(per_slice.min() / per_slice.mean()), float(per_slice.max() / per_slice.mean())]
    agg_band = np.array([[rows[c]["slices"][k][0] for c in rows] for k in range(64 // FB.SLICE)]).mean(axis=1)
    res["aggregate_band"] = [float(agg_band.min() / agg_band.mean()), float(agg_band.max() / agg_band.mean())]
    for cid, row in rows.items():
        for name in TARGETS.get(row["family"], []):
            if name in row["controls"]:
                r = row["controls"][name][0] / row["native4_mean"]
                res["targeted"].setdefault(row["family"], {})[name] = dict(ratio=r, band_max=row["band"][1],
                                                                          fails=bool(r > row["band"][1]))
    # per (case, group): which naive controls stay inside the group's native band, and where the null leaves it
    res["group_reliance"] = {}
    for g in gids:
        d = {}
        for name in ("ignore_actions", "wrong_probe_geometry", "numerical_null", "ablate_body_gain"):
            inside, beyond = [], []
            for c, row in rows.items():
                if name not in row["controls"]:
                    continue
                sl = np.array([s[1][g] for s in row["slices"]])
                r = row["controls"][name][1][g] / sl.mean()
                (beyond if r > sl.max() / sl.mean() else inside).append(row["family"])
            d[name] = dict(inside_band=inside, beyond_band=len(beyond))
        res["group_reliance"][g] = d
    s64 = np.array([rows[c]["native64"][0] for c in rows])
    worst = float(s64.max())
    rule_k = math.floor(-math.log10(2 * worst)) if worst > 0 else None
    res["reward"] = dict(
        native64_primary=float(s64.mean()), K=DEFAULT_PRECISION,
        native64_reward=precision_reward(float(s64.mean()), DEFAULT_PRECISION),
        persistence4_primary=float(np.mean([rows[c]["controls"]["initial_persistence"][0] for c in rows])),
        worst_native_case=worst, calibration_rule_K=rule_k,
        scale_factor_for_K2=float(2 * worst / 1e-2),
        note="PhySim rule: largest integer K with 10^-K >= 2 x worst native case energy (reward-calibration.json).")
    res["reward"]["persistence4_reward"] = precision_reward(res["reward"]["persistence4_primary"], DEFAULT_PRECISION)
    for name in names:
        have = [c for c in rows if name in rows[c]["controls"]]
        if have and len(have) == len(rows):
            res["reward"][f"{name}_reward_4member"] = precision_reward(
                float(np.mean([rows[c]["controls"][name][0] for c in have])), DEFAULT_PRECISION)
    (work / "report.json").write_text(json.dumps(res, indent=1) + "\n")
    write_md(res, work / "report.md", gids)
    return res


def write_md(res, path, gids):
    L = [f"# c53 fed vortices: lab bundle controls ({res['cases_scored']} cases)", "",
         f"Ratios = control score / mean of 16 independent 4-member native slices; native band (aggregate) "
         f"{res['aggregate_band'][0]:.2f}-{res['aggregate_band'][1]:.2f}.", "",
         "| control | cases | aggregate ratio | 90% CI | cases beyond the native band |", "|---|---|---|---|---|"]
    for k, a in res["aggregate"].items():
        L.append(f"| {k} | {a['cases']} | {a['ratio']:.2f} | {a['ci90'][0]:.2f}-{a['ci90'][1]:.2f} | {a['cases_beyond_band']}/{a['cases']} |")
    L += ["", "Per case (ratio; band = slice min-max):", "",
          "| case | program | native64 | band | " + " | ".join(k for k in res["aggregate"] if k != "independent_native") + " |",
          "|---" * (4 + len(res["aggregate"]) - 1) + "|"]
    for cid, r in res["per_case"].items():
        L.append(f"| {cid} | {r['family']} | {r['native64']:.4f} | {r['band'][0]:.2f}-{r['band'][1]:.2f} | " + " | ".join(
            (f"{r['ratio'][k]:.2f}" if k in r["ratio"] else "-") for k in res["aggregate"] if k != "independent_native") + " |")
    L += ["", "Per group (ratio; group band in the first row):", "", "| control | " + " | ".join(gids) + " |",
          "|---" * (len(gids) + 1) + "|",
          "| native band | " + " | ".join(f"{res['group_band'][g][0]:.2f}-{res['group_band'][g][1]:.2f}" for g in gids) + " |"]
    for k, gr in res["groups"].items():
        if k == "independent_native":
            continue
        L.append(f"| {k} | " + " | ".join(f"{gr[g]['ratio']:.2f}" for g in gids) + " |")
    L += ["", "Targeted programs: mechanism control ratio vs the case's native band maximum", "",
          "| program | control | ratio | band max | fails |", "|---|---|---|---|---|"]
    for fam, d in res["targeted"].items():
        for k, v in d.items():
            L.append(f"| {fam} | {k} | {v['ratio']:.2f} | {v['band_max']:.2f} | {'yes' if v['fails'] else 'NO'} |")
    L += ["", "Per group: programs on which a control stays inside that group's per-case native band", "",
          "| group | ignore_actions inside | wrong_probe_geometry inside | null beyond band (cases) | body_gain inside |",
          "|---|---|---|---|---|"]
    for g, d in res["group_reliance"].items():
        L.append(f"| {g} | {', '.join(d['ignore_actions']['inside_band']) or '-'} | "
                 f"{', '.join(d['wrong_probe_geometry']['inside_band']) or '-'} | {d['numerical_null']['beyond_band']} | "
                 f"{', '.join(d['ablate_body_gain']['inside_band']) or '-'} |")
    rw = res["reward"]
    L += ["", f"Reward (K={rw['K']:g}): native 64-member primary energy {rw['native64_primary']:.4f} -> reward "
          f"{rw['native64_reward']:.3f}; initial persistence {rw['persistence4_primary']:.3f} -> {rw['persistence4_reward']:.3f}. "
          f"Worst native case {rw['worst_native_case']:.4f}; PhySim's rule gives K = {rw['calibration_rule_K']}. "
          f"Scales x{rw['scale_factor_for_K2']:.0f} would make K=2 calibrated.",
          "", f"Simulation CPU in cached control ensembles: {res['simulation_cpu_h']:.2f} h."]
    path.write_text("\n".join(L) + "\n")
