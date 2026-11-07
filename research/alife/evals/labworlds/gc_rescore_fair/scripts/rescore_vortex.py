"""Fed vortices (selection world): re-score the main suite (suite/, scripts/suite.py + specificity.py), the formation
suite and the long-horizon suite long2 (scripts2/suite2.py) with both estimators. Those report functions score
inline, so their post-scoring code is reproduced here verbatim (derive_main, derive_specificity, derive_suite2) and
checked by rebuilding the stored report.json / specificity.json bit for bit from the plugin scores.
usage: rescore_vortex.py"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

W = C.GC / "vortex"
OUT = C.OUT_ROOT / "vortex"
MEMBERS, N_TRUTH = 4, 2
MECH = ("adv0", "eps0", "k0", "kl0", "mu0")       # gcv.MECH: loaded from suite/ens/<program>/ like verify.py


def unit_groups(s):
    return [dict(g, unit=("global mean and variance; frozen calibration scales" if g["id"].startswith("global")
                          else "native field units; frozen calibration scale")) for g in s["groups"]]


def _boot(num, den, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(num), size=(n, len(num)))
    r = num[idx].mean(axis=1) / den[idx].mean(axis=1)
    return [float(np.quantile(r, 0.05)), float(np.quantile(r, 0.95))]


# ----------------------------------------------------------------------------- scoring

def rescore(label, sdir, rec):
    s = C.jload(sdir / "suite.json")
    stored = C.jload(sdir / "scores.json")
    groups = unit_groups(s)
    sham = next(c for c in s["cases"] if not c["request"]["actions"])
    sham_truth, _ = C.load_npz(sdir / sham["truth"])
    scores = {e: {} for e in C.ESTS}
    for c in s["cases"]:
        case, cid = c["request"], c["id"]
        truth, _ = C.load_npz(sdir / c["truth"])
        rost = C.roster_for(truth)
        for e in C.ESTS:
            scores[e][cid] = {}
        for name in s["controls"]:
            if name == "initial_persistence":
                pred, src = C.persistence_from_truth(sham_truth, case, MEMBERS, rost), f"persistence of {sham['truth']} t=0"
            else:
                if label == "main":
                    if name == "ignore_actions":
                        p = sdir / "controls" / "ignore_actions.npz"
                    elif name == "independent_native" or name in MECH:
                        p = sdir / "ens" / c["program"] / ("native.npz" if name == "independent_native" else f"{name}.npz")
                    else:
                        p = sdir / "controls" / cid / f"{name}.npz"
                else:
                    if name == "ignore_actions" or (name == "native_b" and cid == sham["id"]):
                        p = sdir / "controls" / "ignore_actions.npz"
                    else:
                        p = sdir / "controls" / cid / f"{name}.npz"
                if not p.exists():
                    continue
                pred, src = [a[:MEMBERS] for a in C.load_npz(p)[0]], p
            res = {e: C.score(case, pred, truth, groups, MEMBERS, N_TRUTH, rost, e) for e in C.ESTS}
            for e in C.ESTS:
                scores[e][cid][name] = dict(agg=res[e]["joint_energy_equal_group_mean"],
                                            groups={g["id"]: g["energy_score"] for g in res[e]["joint_energy"]})
            st = stored.get(cid, {}).get(name)
            rec.add(label, cid, c["program"], name, MEMBERS, res["plugin"], res["fair"], None, src,
                    spread=C.spread_terms(pred, truth, groups))
            rec.rows[-1]["stored_checked"] = st is not None
            rec.rows[-1]["plugin_matches_stored"] = st == scores["plugin"][cid][name]
            if st != scores["plugin"][cid][name]:
                d = C.diff(st, scores["plugin"][cid][name])
                rec.mismatches.append(dict(world="vortex", suite=label, case=cid, control=name, n_differences=len(d),
                                           max_rel_diff=C.max_rel(d), first=[[str(v) for v in x] for x in d[:3]]))
    return s, scores, stored


# ----------------------------------------------------------------------------- scripts/suite.py report()

def derive_main(s, scores):
    gids = [g["id"] for g in s["groups"]]
    ref = "independent_native"
    out = dict(n_cases=len(s["cases"]), members=MEMBERS, truth_members=N_TRUTH, aggregate={}, per_case={}, groups={},
               specificity={}, band={})
    for name in s["controls"]:
        ids = [c["id"] for c in s["cases"] if name in scores[c["id"]]]
        if not ids or name == ref:
            continue
        num = np.array([scores[i][name]["agg"] for i in ids])
        den = np.array([scores[i][ref]["agg"] for i in ids])
        out["aggregate"][name] = dict(cases=len(ids), ratio=float(num.mean() / den.mean()), ci90=_boot(num, den),
                                      cases_worse=int((num > den).sum()))
        out["groups"][name] = {g: float(np.mean([scores[i][name]["groups"][g] for i in ids]) /
                                        np.mean([scores[i][ref]["groups"][g] for i in ids])) for g in gids}
    for c in s["cases"]:
        r = scores[c["id"]]
        out["per_case"][c["id"]] = dict(program=c["program"], capability=c["capability"],
                                        **{k: r[k]["agg"] / r[ref]["agg"] for k in r if k != ref},
                                        reference=r[ref]["agg"])
    if all("native_b" in scores[c["id"]] for c in s["cases"]):
        ids = [c["id"] for c in s["cases"]]
        nat = np.array([scores[i][ref]["agg"] for i in ids])
        nb = np.array([scores[i]["native_b"]["agg"] for i in ids])
        nul = np.array([scores[i]["numerical_null"]["agg"] for i in ids]) if all("numerical_null" in scores[i] for i in ids) else None
        out["band"] = dict(native_b_over_native=float(nb.mean() / nat.mean()), ci90=_boot(nb, nat),
                           per_case=(nb / nat).round(3).tolist())
        if nul is not None:
            pooled = 0.5 * (nat + nb)
            out["band"]["null_over_pooled_native"] = float(nul.mean() / pooled.mean())
            out["band"]["null_over_pooled_ci90"] = _boot(nul, pooled)
            gb = {}
            for g in gids:
                a = np.array([scores[i][ref]["groups"][g] for i in ids])
                b = np.array([scores[i]["native_b"]["groups"][g] for i in ids])
                n = np.array([scores[i]["numerical_null"]["groups"][g] for i in ids])
                gb[g] = dict(native_b_over_native=float(b.mean() / a.mean()),
                             null_over_pooled=float(n.mean() / (0.5 * (a + b)).mean()),
                             null_per_case_max=float((n / (0.5 * (a + b))).max()))
            out["band"]["groups"] = gb
    sham = [c for c in s["cases"] if c["program"] == "sham"][0]["id"]
    caps = {}
    for c in s["cases"]:
        for name in c["deciding_controls"]:
            caps.setdefault((c["capability"], name), []).append(c)
    for (cap, name), cs in sorted(caps.items()):
        if name not in scores[sham]:
            continue
        r_sham = scores[sham][name]["agg"] / scores[sham][ref]["agg"]
        rows = []
        for c in cs:
            if name not in scores[c["id"]]:
                continue
            r = scores[c["id"]][name]["agg"] / scores[c["id"]][ref]["agg"]
            g = f"device{c['acting_device']}/{c['ports'][0]}"
            rg = scores[c["id"]][name]["groups"][g] / scores[c["id"]][ref]["groups"][g]
            rgs = scores[sham][name]["groups"][g] / scores[sham][ref]["groups"][g]
            rows.append(dict(case=c["id"], program=c["program"], ratio=r, group=g, group_ratio=rg, group_ratio_on_sham=rgs,
                             specificity=r / r_sham, group_specificity=rg / rgs))
        out["specificity"][f"{cap}:{name}"] = dict(ratio_on_sham=r_sham, programs=rows,
                                                   mean_ratio=float(np.mean([x["ratio"] for x in rows])),
                                                   specificity=float(np.mean([x["ratio"] for x in rows]) / r_sham),
                                                   group_specificity=float(np.mean([x["group_specificity"] for x in rows])))
    return out


# ----------------------------------------------------------------------------- scripts/specificity.py

def derive_specificity(suite, S):
    cases = {c["id"]: c for c in suite["cases"]}
    sham = [c for c in suite["cases"] if c["program"] == "sham"][0]["id"]

    def pooled(cid, gid=None):
        if gid is None:
            return 0.5 * (S[cid]["independent_native"]["agg"] + S[cid]["native_b"]["agg"])
        return 0.5 * (S[cid]["independent_native"]["groups"][gid] + S[cid]["native_b"]["groups"][gid])

    def ratio(cid, ctrl, gid=None):
        v = S[cid][ctrl]["agg"] if gid is None else S[cid][ctrl]["groups"][gid]
        return v / pooled(cid, gid)
    out, pairs = {}, {}
    for c in suite["cases"]:
        for ctrl in c["deciding_controls"]:
            pairs.setdefault((c["capability"], ctrl), []).append(c)
    for (cap, ctrl), cs in sorted(pairs.items()):
        r0 = ratio(sham, ctrl)
        rows = []
        for c in cs:
            g = f"device{c['acting_device']}/{c['ports'][0]}"
            rows.append(dict(program=c["program"], ratio=ratio(c["id"], ctrl), group=g, group_ratio=ratio(c["id"], ctrl, g),
                             group_ratio_no_action=ratio(sham, ctrl, g)))
        spec = np.mean([x["ratio"] for x in rows]) / r0
        gspec = np.mean([x["group_ratio"] / x["group_ratio_no_action"] for x in rows])
        out[f"{cap}:{ctrl}"] = dict(no_action=r0, programs=rows, specificity=spec, group_specificity=gspec)
    agg = {}
    for ctrl in ["ignore_actions", "wrong_probe_geometry", "initial_persistence", "numerical_null", "native_b", "adv0",
                 "eps0", "k0", "kl0", "mu0"]:
        ids = [cid for cid in cases if ctrl in S[cid]]
        num = np.array([S[cid][ctrl]["agg"] for cid in ids])
        den = np.array([pooled(cid) for cid in ids])
        agg[ctrl] = dict(cases=len(ids), ratio_pooled=float(num.mean() / den.mean()))
    out["aggregate_pooled"] = agg
    return C.jload_str(out)


# ----------------------------------------------------------------------------- scripts2/suite2.py report()

def derive_suite2(suite_label, s, scores):
    gids = [g["id"] for g in s["groups"]]
    sham = [x for x in s["cases"] if not x["request"]["actions"]][0]
    ref = "independent_native"
    out = dict(suite=suite_label, n_cases=len(s["cases"]), members=MEMBERS, truth_members=N_TRUTH, aggregate={},
               per_case={}, groups={}, specificity={}, band={})
    for name in s["controls"]:
        ids = [x["id"] for x in s["cases"] if name in scores[x["id"]]]
        if not ids or name == ref:
            continue
        num = np.array([scores[i][name]["agg"] for i in ids])
        den = np.array([scores[i][ref]["agg"] for i in ids])
        out["aggregate"][name] = dict(cases=len(ids), ratio=float(num.mean() / den.mean()), ci90=_boot(num, den),
                                      cases_worse=int((num > den).sum()))
        out["groups"][name] = {g: float(np.mean([scores[i][name]["groups"][g] for i in ids]) /
                                        np.mean([scores[i][ref]["groups"][g] for i in ids])) for g in gids}
    for x in s["cases"]:
        r = scores[x["id"]]
        out["per_case"][x["id"]] = dict(program=x["program"], capability=x["capability"],
                                        **{k: r[k]["agg"] / r[ref]["agg"] for k in r if k != ref}, reference=r[ref]["agg"],
                                        groups={k: {g: r[k]["groups"][g] / r[ref]["groups"][g] for g in gids}
                                                for k in r if k != ref})
    ids = [x["id"] for x in s["cases"]]
    if all("native_b" in scores[i] for i in ids):
        nat = np.array([scores[i][ref]["agg"] for i in ids])
        nb = np.array([scores[i]["native_b"]["agg"] for i in ids])
        out["band"] = dict(native_b_over_native=float(nb.mean() / nat.mean()), ci90=_boot(nb, nat),
                           per_case=(nb / nat).round(3).tolist(),
                           range=[float(min(1.0, (nb / nat).min())), float(max(1.0, (nb / nat).max()))])
        if all("numerical_null" in scores[i] for i in ids):
            nul = np.array([scores[i]["numerical_null"]["agg"] for i in ids])
            pooled = 0.5 * (nat + nb)
            out["band"]["null_over_pooled_native"] = float(nul.mean() / pooled.mean())
            out["band"]["null_over_pooled_ci90"] = _boot(nul, pooled)
            out["band"]["null_per_case"] = (nul / pooled).round(3).tolist()
            gb = {}
            for g in gids:
                a = np.array([scores[i][ref]["groups"][g] for i in ids])
                b = np.array([scores[i]["native_b"]["groups"][g] for i in ids])
                n = np.array([scores[i]["numerical_null"]["groups"][g] for i in ids])
                gb[g] = dict(native_b_over_native=float(b.mean() / a.mean()),
                             native_b_per_case=(b / a).round(3).tolist(),
                             null_over_pooled=float(n.mean() / (0.5 * (a + b)).mean()),
                             null_per_case=(n / (0.5 * (a + b))).round(3).tolist())
            out["band"]["groups"] = gb
    sid = sham["id"]
    caps = {}
    for x in s["cases"]:
        for name in x["deciding_controls"]:
            caps.setdefault(name, []).append(x)
    for name, cs in sorted(caps.items()):
        if name not in scores[sid]:
            continue
        r_sham = scores[sid][name]["agg"] / scores[sid][ref]["agg"]
        rows = []
        for x in cs:
            if name not in scores[x["id"]] or x["id"] == sid:
                continue
            r = scores[x["id"]][name]["agg"] / scores[x["id"]][ref]["agg"]
            g = f"device{x['acting_device']}/{x['ports'][0]}"
            rg = scores[x["id"]][name]["groups"][g] / scores[x["id"]][ref]["groups"][g]
            rgs = scores[sid][name]["groups"][g] / scores[sid][ref]["groups"][g]
            rows.append(dict(case=x["id"], program=x["program"], ratio=r, group=g, group_ratio=rg, group_ratio_on_sham=rgs,
                             specificity=r / r_sham, group_specificity=rg / rgs))
        if rows:
            out["specificity"][name] = dict(ratio_on_sham=r_sham, programs=rows,
                                            specificity=float(np.mean([z["ratio"] for z in rows]) / r_sham),
                                            group_specificity=float(np.mean([z["group_specificity"] for z in rows])))
    return out


def main():
    rec = C.Recorder("vortex")
    checks = {}
    for label, folder in (("main", "suite"), ("formation", "formation"), ("long2", "long2")):
        sdir = W / folder
        s, scores, stored = rescore(label, sdir, rec)
        checks[label] = {"scores.json": C.diff(stored, scores["plugin"])}
        for e in C.ESTS:
            d = OUT / label / e
            C.jdump(d / "scores.json", scores[e])
            if label == "main":
                rep = C.jload_str(derive_main(s, scores[e]))
                C.jdump(d / "report.json", rep)
                C.jdump(d / "specificity.json", derive_specificity(s, scores[e]))
            else:
                rep = C.jload_str(derive_suite2(label, s, scores[e]))
                C.jdump(d / "report.json", rep)
        checks[label]["report.json"] = C.diff(C.jload(sdir / "report.json"), C.jload(OUT / label / "plugin" / "report.json"))
        if label == "main":
            checks[label]["specificity.json"] = C.diff(C.jload(sdir / "specificity.json"),
                                                       C.jload(OUT / label / "plugin" / "specificity.json"))
    C.jdump(OUT / "rows.json", dict(rows=rec.rows, mismatches=rec.mismatches,
                                    report_checks={k: {f: [[str(x) for x in d] for d in v[:5]] for f, v in c.items()}
                                                   for k, c in checks.items()}))
    print("rows", len(rec.rows), "score mismatches", len(rec.mismatches))
    for k, c in checks.items():
        print(k, {f: len(v) for f, v in c.items()})


if __name__ == "__main__":
    main()
