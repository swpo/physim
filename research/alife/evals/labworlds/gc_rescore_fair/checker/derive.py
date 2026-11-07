"""Checker's own derivations from checker/out/*.json (scores under both estimators): control tables, specificity
figures and the page tags they feed, written to checker/out/derived.json. Formulas re-implemented from
labworlds/pmcips.report, phase_membrane/formation/scripts/gsuite.report, cips/scripts2/formation.report,
vortex/scripts2/suite2.report + mscore.score_block, vortex/scripts/specificity.py, build_gc.verdict."""
import json
from pathlib import Path
import numpy as np
GC = Path("/home/user/evalwork/gc_suites")
O = GC / "rescore_fair" / "checker" / "out"
SC = {f.stem: json.loads(f.read_text()) for f in O.glob("*__*.json")}
SUITES = {"phase_membrane__formation": GC / "phase_membrane/formation/suite", "cips__formation": GC / "cips/formation/suite",
          "cips__main_iter2": GC / "cips/iter2/suite", "phase_membrane__main_iter1": GC / "phase_membrane/suite",
          "phase_membrane__main_iter2": GC / "phase_membrane/iter2/suite", "rods__formation": GC / "rods/formation/suite"}


def boot(num, den, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(num), size=(n, len(num)))
    r = num[idx].mean(axis=1) / den[idx].mean(axis=1)
    return [float(np.quantile(r, 0.05)), float(np.quantile(r, 0.95))]


def agg(key, e, c, k):
    return SC[key][c][k][e]["agg"]


def grp(key, e, c, k, g):
    return SC[key][c][k][e]["groups"][g]


def pm_table(key, e):
    s = json.loads((SUITES[key] / "suite.json").read_text())
    S = SC[key]
    ref, band = "independent_native", "band_native"
    have = lambda k: [c for c in S if k in S[c] and ref in S[c]]
    bc = have(band)
    bci = boot(np.array([agg(key, e, c, band) for c in bc]), np.array([agg(key, e, c, ref) for c in bc])) if bc else [1.0, 1.0]
    rows = {}
    for k in s["controls"]:
        cs = have(k)
        if not cs or k == ref:
            continue
        num, den = np.array([agg(key, e, c, k) for c in cs]), np.array([agg(key, e, c, ref) for c in cs])
        ci = boot(num, den)
        rows[k] = dict(n=len(cs), ratio=float(num.mean() / den.mean()), ci90=ci, worse=int((num > den).sum()),
                       separated=(bool(ci[0] > bci[1]) if k != band else None))
    gids = [g["id"] for g in s["groups"]] if "groups" in s else None
    gnull = {}
    if gids and "numerical_null" in rows:
        cs = have("numerical_null")
        for g in gids:
            gnull[g] = float(np.mean([grp(key, e, c, "numerical_null", g) for c in cs]) / np.mean([grp(key, e, c, ref, g) for c in cs]))
    bg = {}
    if gids and bc:
        for g in gids:
            bg[g] = boot(np.array([grp(key, e, c, band, g) for c in bc]), np.array([grp(key, e, c, ref, g) for c in bc]))
    return dict(band_ci90=bci, rows=rows, null_groups=gnull, band_groups_ci90=bg)


def sens_ratio(key, e, c, k, dev=None):
    if dev is None:
        return agg(key, e, c, k) / agg(key, e, c, "independent_native")
    gs = SC[key][c][k][e]["groups"]
    g0 = SC[key][c]["independent_native"][e]["groups"]
    return float(np.mean([v for i, v in gs.items() if i.startswith(dev + "/")])) / float(np.mean([v for i, v in g0.items() if i.startswith(dev + "/")]))


def spec_pm(key, e, cid, sham, ctl, dev):
    r, r0 = sens_ratio(key, e, cid, ctl), sens_ratio(key, e, sham, ctl)
    ra, ra0 = sens_ratio(key, e, cid, ctl, dev), sens_ratio(key, e, sham, ctl, dev)
    card = dict(ratio=round(r, 2), ratio_na=round(r0, 2), spec=round(r / r0, 2), pr=round(ra, 2), pr_na=round(ra0, 2))
    card["pspec_card"] = card["pr"] / card["pr_na"]          # build_gc: pspec from the rounded fact-sheet numbers
    card["spec_exact"], card["pspec_exact"] = r / r0, ra / ra0
    return card


def spec_vortex_formation(e, program, ctl, probe):
    key = "vortex__formation"
    s = json.loads((GC / "vortex/formation/suite.json").read_text())
    cid = next(c["id"] for c in s["cases"] if c["program"] == program)
    sham = next(c["id"] for c in s["cases"] if not c["request"]["actions"])
    r = agg(key, e, cid, ctl) / agg(key, e, cid, "independent_native")
    r0 = agg(key, e, sham, ctl) / agg(key, e, sham, "independent_native")
    pr = grp(key, e, cid, ctl, probe) / grp(key, e, cid, "independent_native", probe)
    pr0 = grp(key, e, sham, ctl, probe) / grp(key, e, sham, "independent_native", probe)
    card = dict(ratio=round(r, 3), ratio_na=round(r0, 3), spec=round(r / r0, 3), pr=round(pr, 3), pr_na=round(pr0, 3))
    card["pspec_card"] = card["pr"] / card["pr_na"]
    card["spec_exact"], card["pspec_exact"] = r / r0, pr / pr0
    return card


def vortex_formation_table(e):
    key = "vortex__formation"
    S = SC[key]
    ids = sorted(S)
    ref = "independent_native"
    nat = np.array([agg(key, e, i, ref) for i in ids]); nb = np.array([agg(key, e, i, "native_b") for i in ids])
    nul = np.array([agg(key, e, i, "numerical_null") for i in ids]); pooled = 0.5 * (nat + nb)
    rows = {}
    for k in ["ignore_actions", "wrong_probe_geometry", "initial_persistence", "numerical_null", "k0", "native_b"]:
        cs = [i for i in ids if k in S[i]]
        num, den = np.array([agg(key, e, i, k) for i in cs]), np.array([agg(key, e, i, ref) for i in cs])
        rows[k] = dict(n=len(cs), ratio=float(num.mean() / den.mean()), ci90=boot(num, den))
    return dict(rows=rows, band_range=[float(min(1.0, (nb / nat).min())), float(max(1.0, (nb / nat).max()))],
                null_over_pooled=float(nul.mean() / pooled.mean()), null_ci90=boot(nul, pooled),
                null_per_case=(nul / pooled).round(3).tolist())


def verdict(spec, pspec):
    return "specific" if (spec or 0) >= 1.5 else "at the probe" if (pspec or 0) >= 1.5 else "whole-world"


out = {"control_tables": {}, "specificity": {}}
for e in ("plugin", "fair"):
    for key in ("cips__main_iter2", "cips__formation", "phase_membrane__formation"):
        out["control_tables"].setdefault(key, {})[e] = pm_table(key, e)
    out["control_tables"].setdefault("vortex__formation", {})[e] = vortex_formation_table(e)
    sp = out["specificity"]
    sp.setdefault("phase_membrane:probe_wide", {})[e] = spec_pm("phase_membrane__formation", e, "c003", "c001", "ablate_a0", "device1")
    sp.setdefault("phase_membrane:sink_site", {})[e] = spec_pm("phase_membrane__formation", e, "c008", "c001", "ablate_a0", "device1")
    sp.setdefault("cips:steer_p", {})[e] = spec_pm("cips__formation", e, "c002", "c001", "ablate_chi0", "device0")
    sp.setdefault("cips:keep_empty", {})[e] = spec_pm("cips__formation", e, "c003", "c001", "ablate_chi0", "device1")
    sp.setdefault("vortex:S_steer", {})[e] = spec_vortex_formation(e, "S_steer", "k0", "device0/om")
    for k, v in sp.items():
        v[e]["tag"] = verdict(v[e]["spec"], v[e]["pspec_card"])
(O / "derived.json").write_text(json.dumps(out, indent=1))
for key, t in out["control_tables"].items():
    print("==", key)
    for e in ("plugin", "fair"):
        tt = t[e]
        if "rows" in tt and "band_ci90" in tt:
            print(e, "band", [round(x, 4) for x in tt["band_ci90"]])
        for k, r in tt["rows"].items():
            print(f"  {e:6s} {k:24s} {r['ratio']:.4f} [{r['ci90'][0]:.4f}, {r['ci90'][1]:.4f}] sep={r.get('separated')}")
        if key == "vortex__formation":
            print(" ", e, "band", tt["band_range"], "null", round(tt["null_over_pooled"], 4), [round(x, 3) for x in tt["null_ci90"]], tt["null_per_case"])
for k, v in out["specificity"].items():
    print(k, {e: {a: (round(b, 4) if isinstance(b, float) else b) for a, b in v[e].items()} for e in v})
