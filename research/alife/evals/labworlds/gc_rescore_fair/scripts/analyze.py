"""Collect the re-scoring: change per control and member count, every control table and specificity figure old
against new, ranking changes, the page's cards and tags. Writes results/summary.json, results/rescore_table.csv and
results/figures_old_new.json (every numeric leaf of every rebuilt report, plugin against fair). usage: analyze.py"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cards as K  # noqa: E402
import paths as P  # noqa: E402

RES = P.GC / "rescore_fair" / "results"
WORLDS = ("vortex", "phase_membrane", "cips", "rods")
REPORT_FILES = {"vortex": ("report.json", "specificity.json"), "phase_membrane": ("report.json", "specificity.json"),
                "cips": ("report.json", "specificity.json"), "rods": ("report.json", "band.json")}
NATIVE = {"independent_native", "native_b", "band_native", "numerical_null", "true_simulator_m2"}
NAIVE = {"ignore_actions", "wrong_probe_geometry"}
DETERMINISTIC = {"initial_persistence", "initial_persistence_m64"}
DECIDING = {  # (world, suite) -> deciding controls named by the suite's capability map
    "vortex": {"adv0", "eps0", "k0", "kl0", "mu0"},
}


def cls(control):
    if control in NATIVE:
        return "native ensemble (true simulator)"
    if control in NAIVE:
        return "naive action control"
    if control in DETERMINISTIC:
        return "initial persistence (all members equal)"
    return "mechanism control"


def jl(p):
    return json.loads(Path(p).read_text())


def rel(a, b):
    return (a - b) / a if a else None


# ----------------------------------------------------------------------------- inputs

def load_rows():
    rows, checks = [], {}
    for w in WORLDS:
        d = jl(P.OUT / w / "rows.json")
        rows += d["rows"]
        checks[w] = dict(score_mismatches=d["mismatches"], report_rebuild_differences=d["report_checks"])
    b = jl(P.OUT / "bundles" / "rows.json")
    for r in b["rows"]:
        r["suite"] = r["suite"] + " (bundle proof)"
    rows += b["rows"]
    checks["bundles"] = dict(score_mismatches=b["mismatches"], truth_checks=b["truth_checks"])
    return rows, checks


# ----------------------------------------------------------------------------- (1) size of the change

def change_tables(rows):
    ident = 0.0
    for r in rows:
        if r.get("spread"):
            m = r["members"]
            for g, v in r["spread"].items():
                ident = max(ident, abs((r["groups_plugin"][g] - r["groups_fair"][g]) - v["S"] / (2 * m)))
    per = defaultdict(list)
    for r in rows:
        per[(r["world"], r["suite"], r["control"], r["members"])].append(r)
    table = []
    for (w, s, c, m), rs in sorted(per.items()):
        p = np.array([x["agg_plugin"] for x in rs])
        f = np.array([x["agg_fair"] for x in rs])
        gids = list(rs[0]["groups_plugin"])
        gp = {g: float(np.mean([x["groups_plugin"][g] for x in rs])) for g in gids}
        gf = {g: float(np.mean([x["groups_fair"][g] for x in rs])) for g in gids}
        grel = {g: (gp[g] - gf[g]) / gp[g] if gp[g] else 0.0 for g in gids}
        spread_share = None
        if rs[0].get("spread"):
            # mean distinct-pair spread S over 2 x cross term A: the fraction of the cross term the spread term removes
            spread_share = float(np.mean([np.mean([v["S"] / (2 * v["A"]) for v in x["spread"].values() if v["A"] > 0])
                                          for x in rs]))
        table.append(dict(world=w, suite=s, control=c, control_class=cls(c), members=m, cases=len(rs),
                          mean_plugin=float(p.mean()), mean_fair=float(f.mean()), abs_change=float((p - f).mean()),
                          rel_change=float(1 - f.mean() / p.mean()), rel_change_case_min=float(np.min(1 - f / p)),
                          rel_change_case_max=float(np.max(1 - f / p)),
                          group_rel_change_min=float(min(grel.values())), group_rel_change_max=float(max(grel.values())),
                          groups={g: dict(plugin=gp[g], fair=gf[g], abs_change=gp[g] - gf[g], rel_change=grel[g]) for g in gids},
                          mean_spread_over_2A=spread_share,
                          sources=sorted({x["source"] for x in rs})[:3] + (["..."] if len({x["source"] for x in rs}) > 3 else [])))
    by_m = defaultdict(list)
    for r in rows:
        by_m[(r["members"], cls(r["control"]))].append(r)
    members = []
    for (m, c), rs in sorted(by_m.items()):
        rc = np.array([1 - x["agg_fair"] / x["agg_plugin"] for x in rs])
        ac = np.array([x["agg_plugin"] - x["agg_fair"] for x in rs])
        gr = np.array([(x["groups_plugin"][g] - x["groups_fair"][g]) / x["groups_plugin"][g]
                       for x in rs for g in x["groups_plugin"] if x["groups_plugin"][g] > 0])
        members.append(dict(members=m, control_class=c, scores=len(rs), rel_change_median=float(np.median(rc)),
                            rel_change_min=float(rc.min()), rel_change_max=float(rc.max()),
                            abs_change_median=float(np.median(ac)), abs_change_max=float(ac.max()),
                            group_rel_change_min=float(gr.min()), group_rel_change_max=float(gr.max()),
                            bias_in_units_of_spread=(1 / (2 * m)) if c != "initial persistence (all members equal)" else 0.0))
    return table, members, ident


# ----------------------------------------------------------------------------- report figures, old vs new

def flatten(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from flatten(v, f"{path}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from flatten(v, f"{path}[{i}]")
    else:
        yield path, x


def report_figures():
    out = []
    for (w, label) in P.SUITE_DIRS:
        files = ["report.json"] + (["specificity.json"] if (P.folder(w, label, "plugin") / "specificity.json").exists() else []) \
            + (["band.json"] if (P.folder(w, label, "plugin") / "band.json").exists() else [])
        for f in files:
            a = dict(flatten(jl(P.folder(w, label, "plugin") / f)))
            b = dict(flatten(jl(P.folder(w, label, "fair") / f)))
            for k in a:
                if isinstance(a[k], (int, float, bool)) and a[k] != b.get(k):
                    out.append(dict(world=w, suite=label, file=f, path=k, old=a[k], new=b.get(k),
                                    source=str(P.folder(w, label, "stored") / f)))
    if (P.OUT / "cips" / "formation" / "plugin" / "diagnostics" / "scores.json").exists():
        a = dict(flatten(jl(P.OUT / "cips" / "formation" / "plugin" / "diagnostics" / "scores.json")))
        b = dict(flatten(jl(P.OUT / "cips" / "formation" / "fair" / "diagnostics" / "scores.json")))
        out += [dict(world="cips", suite="formation", file="diagnostics/scores.json", path=k, old=a[k], new=b[k],
                     source=str(P.GC / "cips/formation/suite/diagnostics/scores.json")) for k in a if a[k] != b[k]]
    return out


def control_tables():
    """Every suite's aggregate control table (ratio to independent_native), old against new."""
    out = {}
    for (w, label) in P.SUITE_DIRS:
        rep = {e: jl(P.folder(w, label, e) / "report.json") for e in ("plugin", "fair")}
        rows = {}
        for k, a in rep["plugin"]["aggregate"].items():
            b = rep["fair"]["aggregate"][k]
            row = dict(ratio_old=a["ratio"], ratio_new=b["ratio"], ci90_old=a.get("ci90"), ci90_new=b.get("ci90"))
            for extra in ("cases_worse", "separated", "min_case", "max_case", "cases", "n_cases"):
                if extra in a:
                    row[f"{extra}_old"], row[f"{extra}_new"] = a[extra], b[extra]
            rows[k] = row
        t = dict(controls=rows, source=str(P.folder(w, label, "stored") / "report.json"))
        for e, tag in (("plugin", "old"), ("fair", "new")):
            r = rep[e]
            if "band_aggregate_ci90" in r:
                t[f"band_ci90_{tag}"] = r["band_aggregate_ci90"]
                t[f"not_to_rely_on_{tag}"] = r.get("not_to_rely_on")
            if r.get("band"):
                t[f"band_{tag}"] = {k: v for k, v in r["band"].items() if k != "groups"}
            if "null_band_groups_above_1_1" in r:
                t[f"null_band_groups_above_1_1_{tag}"] = r["null_band_groups_above_1_1"]
        if w == "vortex" and label == "main":
            sp = {e: jl(P.folder(w, label, e) / "specificity.json")["aggregate_pooled"] for e in ("plugin", "fair")}
            t["pooled_reference"] = {k: dict(ratio_old=sp["plugin"][k]["ratio_pooled"], ratio_new=sp["fair"][k]["ratio_pooled"])
                                     for k in sp["plugin"]}
            t["pooled_source"] = str(P.folder(w, label, "stored") / "specificity.json")
        order = {tag: [k for k, _ in sorted(rows.items(), key=lambda kv: kv[1][f"ratio_{tag}"])] for tag in ("old", "new")}
        t["order_old"], t["order_new"], t["order_changed"] = order["old"], order["new"], order["old"] != order["new"]
        out[f"{w}/{label}"] = t
    return out


# ----------------------------------------------------------------------------- specificity rows and tags

def tag(spec, acting):
    if (spec or 0) >= 1.5:
        return "specific"
    if (acting or 0) >= 1.5:
        return "at the probe"
    return "whole-world"


def specificity_rows():
    out = []

    def add(w, label, f, key, prog, spec_o, spec_n, act_o, act_n, extra=None):
        out.append(dict(world=w, suite=label, file=f, key=key, program=prog, specificity_old=spec_o, specificity_new=spec_n,
                        acting_specificity_old=act_o, acting_specificity_new=act_n,
                        tag_old=tag(spec_o, act_o), tag_new=tag(spec_n, act_n), **(extra or {}),
                        source=str(P.folder(w, label, "stored") / f)))

    for (w, label) in P.SUITE_DIRS:
        g = {e: P.getter(e) for e in ("plugin", "fair")}
        if w == "vortex":
            rp, rf = g["plugin"](w, label, "report.json")["specificity"], g["fair"](w, label, "report.json")["specificity"]
            for key in rp:
                for a, b in zip(rp[key]["programs"], rf[key]["programs"]):
                    add(w, label, "report.json (first native as reference)", key, a["program"], a["specificity"],
                        b["specificity"], a["group_specificity"], b["group_specificity"])
                add(w, label, "report.json (first native as reference)", key, "(capability)", rp[key]["specificity"],
                    rf[key]["specificity"], rp[key]["group_specificity"], rf[key]["group_specificity"])
            if label == "main":
                sp, sf = g["plugin"](w, label, "specificity.json"), g["fair"](w, label, "specificity.json")
                for key in sp:
                    if key == "aggregate_pooled":
                        continue
                    for a, b in zip(sp[key]["programs"], sf[key]["programs"]):
                        add(w, label, "specificity.json (pooled native reference)", key, a["program"],
                            a["ratio"] / sp[key]["no_action"], b["ratio"] / sf[key]["no_action"],
                            a["group_ratio"] / a["group_ratio_no_action"], b["group_ratio"] / b["group_ratio_no_action"])
                    add(w, label, "specificity.json (pooled native reference)", key, "(capability)", sp[key]["specificity"],
                        sf[key]["specificity"], sp[key]["group_specificity"], sf[key]["group_specificity"])
        elif w == "rods":
            rp, rf = g["plugin"](w, label, "report.json")["specificity"], g["fair"](w, label, "report.json")["specificity"]
            for key in rp:
                for a, b in zip(rp[key]["programs"], rf[key]["programs"]):
                    add(w, label, "report.json", key, a["program"], a["specificity"], b["specificity"],
                        a["specificity_acting"], b["specificity_acting"],
                        dict(cargo_specificity_old=a.get("specificity_cargo"), cargo_specificity_new=b.get("specificity_cargo")))
                add(w, label, "report.json", key, "(capability mean)", rp[key]["mean_specificity"], rf[key]["mean_specificity"],
                    rp[key]["mean_specificity_acting"], rf[key]["mean_specificity_acting"])
        elif w == "cips" and label == "formation":
            rp, rf = g["plugin"](w, label, "specificity.json"), g["fair"](w, label, "specificity.json")
            for a, b in zip(rp["programs"], rf["programs"]):
                add(w, label, "specificity.json", f"S:{rp['control']}", a["program"], a["specificity"], b["specificity"],
                    a["specificity_acting"], b["specificity_acting"])
        else:
            rp, rf = g["plugin"](w, label, "specificity.json")["specificity"], g["fair"](w, label, "specificity.json")["specificity"]
            for cap in rp:
                for a, b in zip(rp[cap]["programs"], rf[cap]["programs"]):
                    add(w, label, "specificity.json", f"{cap}:{rp[cap]['control']}", a["program"], a["specificity"],
                        b["specificity"], a["specificity_acting"], b["specificity_acting"])
                add(w, label, "specificity.json", f"{cap}:{rp[cap]['control']}", "(capability mean)",
                    rp[cap]["mean_specificity"], rf[cap]["mean_specificity"], rp[cap]["mean_specificity_acting"],
                    rf[cap]["mean_specificity_acting"])
    return out


# ----------------------------------------------------------------------------- rankings

def ranking_flips(rows):
    by = defaultdict(dict)
    for r in rows:
        if "(bundle proof)" in r["suite"]:
            continue
        by[(r["world"], r["suite"], r["case"], r["program"])][r["control"]] = r
    flips, persistence = [], []
    for (w, s, c, prog), d in by.items():
        names = sorted(d)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                po = d[a]["agg_plugin"] - d[b]["agg_plugin"]
                fo = d[a]["agg_fair"] - d[b]["agg_fair"]
                if np.sign(po) != np.sign(fo):
                    flips.append(dict(world=w, suite=s, case=c, program=prog, a=a, b=b,
                                      a_old=d[a]["agg_plugin"], b_old=d[b]["agg_plugin"], a_new=d[a]["agg_fair"],
                                      b_new=d[b]["agg_fair"], both_native_equivalent=a in NATIVE | {"ignore_actions"} and b in NATIVE | {"ignore_actions"}))
        if "initial_persistence" in d and "independent_native" in d:
            p, n = d["initial_persistence"], d["independent_native"]
            persistence.append(dict(world=w, suite=s, case=c, program=prog, ratio_old=p["agg_plugin"] / n["agg_plugin"],
                                    ratio_new=p["agg_fair"] / n["agg_fair"]))
        for k in d:
            if cls(k) == "mechanism control" and "independent_native" in d:
                pass
    return flips, persistence


def deciding_vs_native(rows):
    """Smallest mechanism-control ratio to independent_native per suite, old and new (any below 1?)."""
    out = {}
    by = defaultdict(dict)
    for r in rows:
        if "(bundle proof)" not in r["suite"]:
            by[(r["world"], r["suite"], r["case"])][r["control"]] = r
    for (w, s, c), d in by.items():
        n = d.get("independent_native")
        for k, r in d.items():
            if cls(k) != "mechanism control" or n is None:
                continue
            key = f"{w}/{s}"
            ro, rn = r["agg_plugin"] / n["agg_plugin"], r["agg_fair"] / n["agg_fair"]
            cur = out.get(key)
            if cur is None or ro < cur["ratio_old"]:
                out[key] = dict(case=c, control=k, ratio_old=ro, ratio_new=rn)
    return out


def bundle_reference(rows):
    """The bundles' 2-member true-simulator forecasts against the suite's 4-member independent native."""
    nat = {(r["world"], r["suite"], r["case"]): r for r in rows if r["control"] == "independent_native"}
    out = {}
    for r in rows:
        if r["control"] != "true_simulator_m2":
            continue
        s = r["suite"].replace(" (bundle proof)", "")
        n = nat[(r["world"], s, r["case"])]
        out.setdefault(r["bundle"], dict(world=r["world"], suite=s, m2_old=[], m2_new=[], ref_old=[], ref_new=[]))
        o = out[r["bundle"]]
        o["m2_old"].append(r["agg_plugin"])
        o["m2_new"].append(r["agg_fair"])
        o["ref_old"].append(n["agg_plugin"])
        o["ref_new"].append(n["agg_fair"])
    for b, o in out.items():
        for k in ("m2_old", "m2_new", "ref_old", "ref_new"):
            o[k] = float(np.mean(o[k]))
        o["m2_over_ref4_old"] = o["m2_old"] / o["ref_old"]
        o["m2_over_ref4_new"] = o["m2_new"] / o["ref_new"]
        o["source"] = f"/home/user/evalwork/bundles/work/prove/{b}/oracle_grade_m2/grade.json"
    return out


# ----------------------------------------------------------------------------- the page

def page():
    st, pl, fa = (K.card_scores(P.getter(x)) for x in ("stored", "plugin", "fair"))
    cards, changes = {}, []
    for key in pl:
        w, card = key.split(":", 1)
        pub = K.published(w, card, P.GC)
        fields = ("ratio", "ratio_na", "spec", "pr", "pr_na", "pspec", "tag")
        cards[key] = dict(suite=pl[key]["suite"], probe=pl[key]["probe"],
                          published={f: pub[f] for f in fields}, new={f: fa[key][f] for f in fields},
                          plugin_rebuild_matches_published=all(pub[f] == pl[key][f] for f in fields if f != "pspec"),
                          source=f"{P.GC / w / (card.rsplit('/', 1)[0] if '/' in card else 'media')}/"
                                 f"{card.rsplit('/', 1)[-1]}_facts.json")
        if pub["tag"] != fa[key]["tag"]:
            changes.append(dict(card=key, old=pub["tag"], new=fa[key]["tag"], spec_old=pub["spec"], spec_new=fa[key]["spec"],
                                pspec_old=pub["pspec"], pspec_new=fa[key]["pspec"]))
    held = {"vortex": ["S", "I", "D", "E", "H"], "phase_membrane": ["S", "I", "B", "D", "BD"],
            "cips": ["S", "I", "B", "E", "D"], "rods": ["S", "I", "B", "W", "M", "D", "Wd"]}
    summary = {}
    for w, order in K.GC_PAGE_ORDER.items():
        def cap(card):
            d = jl(Path(cards[f"{w}:{card}"]["source"]))
            if "/" not in card:
                return card.split("_")[0]
            c = d["capability"].split()[0].rstrip(":")
            return {"Inherited": "Wd"}.get(c, c)
        caps = {card: cap(card) for card in order}
        for which in ("published", "new"):
            singled = sorted({caps[c] for c in order if cards[f"{w}:{c}"][which]["tag"] not in ("whole-world", "whole-world (ratio artefact)")},
                             key=held[w].index)
            summary.setdefault(w, {})[f"singled_out_{which}"] = singled
        summary[w]["shown"] = sorted(set(caps.values()) & set(held[w]), key=held[w].index)
        summary[w]["changed"] = summary[w]["singled_out_published"] != summary[w]["singled_out_new"]
    return cards, changes, summary


def main():
    rows, checks = load_rows()
    table, members, ident = change_tables(rows)
    figs = report_figures()
    ctab = control_tables()
    spec = specificity_rows()
    flips, persistence = ranking_flips(rows)
    cards, tag_changes, page_summary = page()
    caveats = jl(RES / "page_numbers.json") if (RES / "page_numbers.json").exists() else None
    summary = dict(
        what=("Every saved forecast of the GC suites in use re-scored with blobround6_eval.score_case(estimator='plugin') "
              "and (estimator='fair') from /home/user/swpo/residency-environments ad6d2eb; reports rebuilt with each suite's "
              "own report code (vortex: its post-scoring code reproduced in scripts/rescore_vortex.py) on shadow folders "
              "under rescore_fair/out/<world>/<suite>/{plugin,fair}."),
        suites_in_use={f"{w}/{s}": str(d) for (w, s), d in P.SUITE_DIRS.items()},
        checks=dict(plugin_reproduces_stored=checks, scores_rescored=len(rows),
                    plugin_minus_fair_equals_spread_over_2m_max_abs_error=ident),
        change_by_member_count=members,
        change_by_control=table,
        control_tables=ctab,
        specificity=spec,
        specificity_tag_changes=[s for s in spec if s["tag_old"] != s["tag_new"]],
        ranking=dict(per_case_flips=flips, aggregate_order_changes={k: dict(old=v["order_old"], new=v["order_new"])
                                                                    for k, v in ctab.items() if v["order_changed"]},
                     persistence_over_native=dict(min_old=min(x["ratio_old"] for x in persistence),
                                                  min_new=min(x["ratio_new"] for x in persistence), cases=persistence),
                     weakest_mechanism_control=deciding_vs_native(rows),
                     bundle_true_simulator_m2=bundle_reference(rows)),
        page=dict(cards=cards, tag_changes=tag_changes, summary_table=page_summary, caveat_numbers=caveats,
                  source="/home/user/evalwork/showcase/page/build_gc.py (WORLDS order, norm(), verdict())"),
        figures_file=str(RES / "figures_old_new.json"),
    )
    flags = []
    for k, t in ctab.items():
        for c, r in t["controls"].items():
            if "separated_old" in r and r["separated_old"] != r["separated_new"]:
                flags.append(dict(suite=k, control=c, separated_old=r["separated_old"], separated_new=r["separated_new"],
                                  ratio_old=r["ratio_old"], ratio_new=r["ratio_new"], ci90_old=r["ci90_old"], ci90_new=r["ci90_new"],
                                  band_ci90_old=t.get("band_ci90_old"), band_ci90_new=t.get("band_ci90_new"), source=t["source"]))
    summary["findings"] = dict(
        page_tag_changes=tag_changes,
        page_singled_out_changes={w: v for w, v in page_summary.items() if v["changed"]},
        page_caveat_numbers_changed=sum(1 for x in (caveats or []) if x["changed"]),
        page_caveat_numbers_checked=len(caveats or []),
        suite_separation_flag_changes=flags,
        suite_row_tag_changes_off_page=[x for x in spec if x["tag_old"] != x["tag_new"]
                                        and not (x["world"], x["suite"], x["program"]) in
                                        {("phase_membrane", "formation", "probe_wide"), ("cips", "formation", "steer_p")}],
        notes=[
            "No agent forecasts for these suites are saved on this machine (the only rollout run, bundles/runs/"
            "mech-fedvortex-qwen9b, is on the older fedvortex bundle, not a GC suite). The saved reference forecasts are the "
            "suites' own controls plus the bundle proofs' 2-member true-simulator and 64-member persistence forecasts "
            "(bundles/work/prove/<bundle>/{oracle_grade_m2,naive_grade}), re-scored here against the same truths.",
            "The page's first-round cards quote the first-round main suites (phase_membrane/suite, cips/suite, rods/suite), "
            "not the refrozen iter2 suites (template_gc.html says so), so both were re-scored.",
            "vortex/long is superseded by long2 on the page (cards use long2/media) and was not re-scored.",
            "Initial persistence has identical members, so its spread term is zero under both estimators and its scores "
            "are unchanged; it was rebuilt from the no-action truth's t=0 readout and matches the stored scores bit for bit.",
        ])
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    (RES / "figures_old_new.json").write_text(json.dumps(figs, indent=0) + "\n")
    with open(RES / "rescore_table.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["world", "suite", "case", "program", "control", "control_class", "members", "group", "plugin", "fair",
                     "abs_change", "rel_change", "spread_S", "cross_A", "plugin_matches_stored", "source"])
        for r in rows:
            wr.writerow([r["world"], r["suite"], r["case"], r["program"], r["control"], cls(r["control"]), r["members"],
                         "aggregate", repr(r["agg_plugin"]), repr(r["agg_fair"]), repr(r["agg_plugin"] - r["agg_fair"]),
                         repr(rel(r["agg_plugin"], r["agg_fair"])), "", "", r["plugin_matches_stored"] if r["stored_checked"] else "n/a",
                         r["source"]])
            for g in r["groups_plugin"]:
                sp = (r.get("spread") or {}).get(g, {})
                wr.writerow([r["world"], r["suite"], r["case"], r["program"], r["control"], cls(r["control"]), r["members"], g,
                             repr(r["groups_plugin"][g]), repr(r["groups_fair"][g]),
                             repr(r["groups_plugin"][g] - r["groups_fair"][g]), repr(rel(r["groups_plugin"][g], r["groups_fair"][g])),
                             repr(sp.get("S", "")), repr(sp.get("A", "")),
                             r["plugin_matches_stored"] if r["stored_checked"] else "n/a", r["source"]])
    print("rows", len(rows), "identity err", ident, "figures", len(figs), "tag changes (page)", tag_changes)
    print("suite-row tag changes", [(s["world"], s["suite"], s["key"], s["program"], s["tag_old"], s["tag_new"])
                                   for s in spec if s["tag_old"] != s["tag_new"]])
    print("aggregate order changes", {k: (v["order_old"], v["order_new"]) for k, v in ctab.items() if v["order_changed"]})
    print("page summary", page_summary)


if __name__ == "__main__":
    main()
