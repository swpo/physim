"""Score-derived numbers quoted in the page's caveats and 'short of the claim' lines, recomputed from the plugin and fair
shadow reports. Each spec names the card (or world gap line), the quoted fragment, and how the fact-sheet scripts
computed it; the plugin value, printed at the quoted precision, is checked against the published text.
Writes results/page_numbers.json. usage: page_numbers.py"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cards as K  # noqa: E402
import paths as P  # noqa: E402

RES = P.GC / "rescore_fair" / "results"
SENS = ("device0", "device1", "global")


def rep(get, w, s):
    return get(w, s, "report.json")


def pc(get, w, s, cid):
    return rep(get, w, s)["per_case"][cid]


def raw(get, w, s, cid):
    return get(w, s, f"controls/{cid}/scores.json")


def gmean(sc, dev):
    g = {x["id"]: x["energy_score"] for x in sc["joint_energy"]}
    return float(np.mean([v for k, v in g.items() if k.startswith(dev + "/")]))


def vcells(get, s):
    """vortex mfacts3 / review3 rule: null / pooled native per group-case above max(1, the group's widest native_b/native)."""
    nb = rep(get, "vortex", s)["band"]["groups"]
    cells = []
    for g, v in nb.items():
        hi = max(1.0, max(v["native_b_per_case"]))
        cells += [(g, i, x, hi) for i, x in enumerate(v["null_per_case"]) if x > hi]
    return cells, 3 * len(nb)


def vband(get, s):
    b = rep(get, "vortex", s)["band"]
    return [b["null_over_pooled_native"], *b["null_over_pooled_ci90"], min(b["null_per_case"]), max(b["null_per_case"]),
            *b["range"]]


def vcell(get, s, g, i):
    cells, _ = vcells(get, s)
    c = [x for x in cells if x[0] == g and x[1] == i]
    v = rep(get, "vortex", s)["band"]["groups"][g]
    return [v["null_per_case"][i], max(1.0, max(v["native_b_per_case"])), bool(c)]


def top_groups(get, s, cid, ctrl, n=4):
    g = pc(get, "vortex", s, cid)["groups"][ctrl]
    return sorted(g.items(), key=lambda kv: -kv[1])[:n]


def pm_row(get, s, cap, prog):
    return next(r for r in get("phase_membrane", s, "specificity.json")["specificity"][cap]["programs"] if r["program"] == prog)


def cips_row(get, s, cap, prog):
    return next(r for r in get("cips", s, "specificity.json")["specificity"][cap]["programs"] if r["program"] == prog)


def cips_frow(get, prog):
    return next(r for r in get("cips", "formation", "specificity.json")["programs"] if r["program"] == prog)


def cid_of(get, w, s, prog):
    return next(c["request"]["id"] for c in get(w, s, "suite.json")["cases"] if c["family"] == prog)


def own_dev1(get, prog, ctl):
    """cips: the control's own device-1 group-mean energy on a program over its no-action value (iteration 1)."""
    a = raw(get, "cips", "main_iter1", cid_of(get, "cips", "main_iter1", prog))[ctl]
    b = raw(get, "cips", "main_iter1", "c001")[ctl]
    return gmean(a, "device1") / gmean(b, "device1")


def native_dev1(get, prog):
    return gmean(raw(get, "cips", "main_iter1", cid_of(get, "cips", "main_iter1", prog))["independent_native"], "device1")


def rods_group_ratio(get, s, cid, ctl, gid):
    sc = raw(get, "rods", s, cid)
    g = lambda k: {x["id"]: x["energy_score"] for x in sc[k]["joint_energy"]}[gid]  # noqa: E731
    return g(ctl) / g("independent_native")


SPECS = [
    # ---------------------------------------------------------------- vortex formation (S_steer, S_wide)
    ("vortex:media2/S_steer", 2, "k0 separates on the no-action program too (17.7x); specificity 1.22 (acting probe 2.13)",
     lambda g: [pc(g, "vortex", "formation", "c001")["k0"],
                pc(g, "vortex", "formation", "c002")["k0"] / pc(g, "vortex", "formation", "c001")["k0"],
                pc(g, "vortex", "formation", "c002")["groups"]["k0"]["device0/om"] / pc(g, "vortex", "formation", "c001")["groups"]["k0"]["device0/om"]],
     [1, 2, 2]),
    ("vortex:media2/S_steer", 3, "null 0.99 of pooled native [0.91, 1.09], per case 0.88-1.11; band 0.51-1.44 per case",
     lambda g: vband(g, "formation"), [2, 2, 2, 2, 2, 2, 2]),
    ("vortex:media2/S_steer", 3, "5 of 27 group-case cells exceed their band",
     lambda g: [len(vcells(g, "formation")[0]), vcells(g, "formation")[1]], [0, 0]),
    ("vortex:media2/S_steer", 3, "global vorticity on the no-action case 1.97 (band at most 1.56) [exceeds?]",
     lambda g: vcell(g, "formation", "global/om", 0), [2, 2, None]),
    ("vortex:media2/S_steer", 3, "global fuel there 1.37 (at most 1.36) [exceeds?]",
     lambda g: vcell(g, "formation", "global/Y", 0), [2, 2, None]),
    ("vortex:media2/S_steer", 3, "S_steer device 1 vorticity 1.16 (at most 1.00) [exceeds?]",
     lambda g: vcell(g, "formation", "device1/om", 1), [2, 2, None]),
    ("vortex:media2/S_steer", 3, "S_steer device 1 fuel 1.18 (at most 1.03) [exceeds?]",
     lambda g: vcell(g, "formation", "device1/Y", 1), [2, 2, None]),
    ("vortex:media2/S_steer", 3, "S_steer device 1 eating 1.07 (at most 1.00) [exceeds?]",
     lambda g: vcell(g, "formation", "device1/eat", 1), [2, 2, None]),
    ("vortex:media2/S_wide", 3, "ignore-actions control 4.2x, wrong geometry 2.6x on this case",
     lambda g: [pc(g, "vortex", "formation", "c003")["ignore_actions"], pc(g, "vortex", "formation", "c003")["wrong_probe_geometry"]],
     [1, 1]),
    ("vortex:media2/S_wide", 4, "k0's ratio here (13.4x) lower than on the no-action program (17.7x), specificity 0.76",
     lambda g: [pc(g, "vortex", "formation", "c003")["k0"], pc(g, "vortex", "formation", "c001")["k0"],
                pc(g, "vortex", "formation", "c003")["k0"] / pc(g, "vortex", "formation", "c001")["k0"]], [1, 1, 2]),
    # ---------------------------------------------------------------- vortex main
    ("vortex:I_follow", 2, "the neutral twin (eps0) already fails 2.7x on the no-action program (pooled reference)",
     lambda g: [g("vortex", "main", "specificity.json")["H:eps0"]["no_action"]], [1]),
    ("vortex:H_inherit", 4, "the 5.05 'no-action' ratio of that group (device0/b, pooled)",
     lambda g: [next(x for x in g("vortex", "main", "specificity.json")["H:eps0"]["programs"]
                     if x["program"] == "H_inherit")["group_ratio_no_action"]], [2]),
    # ---------------------------------------------------------------- vortex long2
    ("vortex:long2/media/HD_wide", 2, "adv0 scores 1.53 on no action, 1.73 here (specificity 1.13)",
     lambda g: [pc(g, "vortex", "long2", "c001")["adv0"], pc(g, "vortex", "long2", "c003")["adv0"],
                pc(g, "vortex", "long2", "c003")["adv0"] / pc(g, "vortex", "long2", "c001")["adv0"]], [2, 2, 2]),
    ("vortex:long2/media/HD_wide", 2, "separates through global/Y 7.2x, global/eat 5.1x, global/b 2.0x, global/a 2.0x",
     lambda g: [v for _, v in top_groups(g, "long2", "c003", "adv0")], [1, 1, 1, 1]),
    ("vortex:long2/media/HD_wide", 3, "null 0.96 of pooled [0.95, 0.98], per case 0.95-0.98, band 0.95-1.00",
     lambda g: vband(g, "long2"), [2, 2, 2, 2, 2, 2, 2]),
    ("vortex:long2/media/HD_wide", 3, "9 of 45 group-case cells exceed their band",
     lambda g: [len(vcells(g, "long2")[0]), vcells(g, "long2")[1]], [0, 0]),
    ("vortex:long2/media/HD_wide", 3, "global vorticity on H_seed 1.34 (band at most 1.11)",
     lambda g: vcell(g, "long2", "global/om", 1), [2, 2, None]),
    ("vortex:long2/media/HD_wide", 3, "acting group device1/om on HD_wide stays inside its band",
     lambda g: vcell(g, "long2", "device1/om", 2), [3, 3, None]),
    ("vortex:long2/media/H_seed", 5, "acting group device1/b is one of them (1.052 against 1.041)",
     lambda g: vcell(g, "long2", "device1/b", 1), [3, 3, None]),
    ("vortex:long2/media/HD_wide", 4, "wrong probe geometry 1.00, ignore actions 1.01 (1.07 on HD_wide, above that case's 1.00); initial persistence 2.63",
     lambda g: [rep(g, "vortex", "long2")["aggregate"]["wrong_probe_geometry"]["ratio"],
                rep(g, "vortex", "long2")["aggregate"]["ignore_actions"]["ratio"],
                pc(g, "vortex", "long2", "c003")["ignore_actions"], pc(g, "vortex", "long2", "c003")["native_b"],
                rep(g, "vortex", "long2")["aggregate"]["initial_persistence"]["ratio"]], [2, 2, 2, 2, 2]),
    ("vortex:long2/media/HD_wide", 4, "at 2 tu ignore actions 1.77 on H_seed, 5.59 on HD_wide; wrong geometry 3.14 (no action), 2.41 (HD_wide); 0.63-1.13 from 5 tu",
     lambda g: (lambda d: [d["H_seed"]["2"]["ignore_actions"]["agg"], d["HD_wide"]["2"]["ignore_actions"]["agg"],
                           d["sham"]["2"]["wrong_probe_geometry"]["agg"], d["HD_wide"]["2"]["wrong_probe_geometry"]["agg"],
                           min(d[p][t][n]["agg"] for p in d for t in d[p] if int(t) >= 5 for n in ("ignore_actions", "wrong_probe_geometry")),
                           max(d[p][t][n]["agg"] for p in d for t in d[p] if int(t) >= 5 for n in ("ignore_actions", "wrong_probe_geometry"))])
     (g("vortex", "long2", "pertime_scores.json")), [2, 2, 2, 2, 2, 2]),
    ("vortex:long2/media/H_seed", 4, "eps0 separates through global/eat 5.1x, global/Y 3.7x, global/b 3.4x, global/om 2.5x; no action 1.60 (specificity 0.97)",
     lambda g: [v for _, v in top_groups(g, "long2", "c002", "eps0")] + [
         pc(g, "vortex", "long2", "c001")["eps0"], pc(g, "vortex", "long2", "c002")["eps0"] / pc(g, "vortex", "long2", "c001")["eps0"]],
     [1, 1, 1, 1, 2, 2]),
    # ---------------------------------------------------------------- phase_membrane
    ("phase_membrane:B_links_core", 2, "aggregate specificity of chi0 0.79-1.09; acting-device specificity 0.66-1.42",
     lambda g: (lambda rows: [min(r["specificity"] for r in rows), max(r["specificity"] for r in rows),
                              min(r["specificity_acting"] for r in rows), max(r["specificity_acting"] for r in rows)])
     (g("phase_membrane", "main_iter1", "specificity.json")["specificity"]["B"]["programs"]), [2, 2, 2, 2]),
    ("phase_membrane:media2/follow_B", 3, "DS2's device-0 ratio there 16.7; probe ratio 2.9; device 1 gives 4.1 against 10.1",
     lambda g: (lambda r: [r["ratio_acting_sham"], r["ratio_acting"], r["by_device"]["device1"]["ratio"],
                           r["by_device"]["device1"]["ratio_sham"]])(pm_row(g, "main_iter2", "D", "follow_B")), [1, 1, 1, 1]),
    ("gaps:phase_membrane", None, "S: the dt-halved null is flagged (formation null over native, global groups; band)",
     lambda g: [rep(g, "phase_membrane", "formation")["aggregate"]["numerical_null"]["ratio"],
                *[rep(g, "phase_membrane", "formation")["groups"]["numerical_null"][x]["ratio"] for x in ("global/S", "global/K", "global/L", "global/phi")],
                *rep(g, "phase_membrane", "formation")["band_aggregate_ci90"]], [2, 2, 2, 2, 2, 2, 2]),
    # ---------------------------------------------------------------- cips formation
    ("cips:media2/steer_p", 1, "dt-halved null on this case 0.931 (1.093/0.895/1.043 by sensor); band_native here 1.01",
     lambda g: (lambda d: [d["ratio"], *[d["by_sensor"][s] for s in SENS], cips_frow(g, "steer_p")["band_native"]])
     (g("cips", "formation", "diagnostics/scores.json")["steer_p:numerical_null"]), [3, 3, 3, 3, 2]),
    ("cips:media2/steer_p", 2, "at device 0 chi0 scores 38.4x the native reference, the forecast that ignores the pulse 38.1x",
     lambda g: [pc(g, "cips", "formation", "c002")["ablate_chi0_sensors"]["device0"],
                pc(g, "cips", "formation", "c002")["ignore_actions_sensors"]["device0"]], [1, 1]),
    ("cips:media2/steer_p", 7, "null aggregate 1.03 against the native band 1.01-1.13 (inside); no action 1.05, keep_empty 0.98",
     lambda g: [rep(g, "cips", "formation")["aggregate"]["numerical_null"]["ratio"],
                min(pc(g, "cips", "formation", c)["band_native"] for c in ("c001", "c002")),
                max(pc(g, "cips", "formation", c)["band_native"] for c in ("c001", "c002")),
                pc(g, "cips", "formation", "c001")["numerical_null"], pc(g, "cips", "formation", "c003")["numerical_null"]],
     [2, 2, 2, 2, 2]),
    ("cips:media2/keep_empty", 2, "second native ensemble on this case 0.909 (0.624/0.706/1.131); its null 0.98",
     lambda g: (lambda d: [d["ratio"], *[d["by_sensor"][s] for s in SENS], pc(g, "cips", "formation", "c003")["numerical_null"]])
     (g("cips", "formation", "diagnostics/scores.json")["keep_empty:band_native"]), [3, 3, 3, 3, 2]),
    # ---------------------------------------------------------------- cips main (iteration 1 cards)
    ("cips:I_enter_exit", 0, "chi0 ratio here 107.8, no action 109.8, global groups ~140; acting device 1.71x",
     lambda g: [pc(g, "cips", "main_iter1", "c004")["ablate_chi0"], pc(g, "cips", "main_iter1", "c001")["ablate_chi0"],
                pc(g, "cips", "main_iter1", "c004")["ablate_chi0_sensors"]["global"],
                cips_row(g, "main_iter1", "I", "enter_exit")["specificity_acting"]], [1, 1, 0, 2]),
    ("cips:I_wide_C4", 0, "specificity 0.76, 0.89 at device 0; enter_exit 1.71 at device 0",
     lambda g: [cips_row(g, "main_iter1", "I", "wide_C4")["specificity"], cips_row(g, "main_iter1", "I", "wide_C4")["specificity_acting"],
                cips_row(g, "main_iter1", "I", "enter_exit")["specificity_acting"]], [2, 2, 2]),
    ("cips:B_s_core", 2, "specificity 0.99, 1.04 at device 0; s_bath 1.51, 2.21 at device 0",
     lambda g: [cips_row(g, "main_iter1", "B", "s_core")["specificity"], cips_row(g, "main_iter1", "B", "s_core")["specificity_acting"],
                cips_row(g, "main_iter1", "B", "s_bath")["specificity"], cips_row(g, "main_iter1", "B", "s_bath")["specificity_acting"]],
     [2, 2, 2, 2]),
    ("cips:E_cut_C4", 1, "kF0 specificity cut_C4 0.68 (0.38 at device 0), wide_C4 0.73 (0.27), feed_neck 1.11 (1.22), cut_neck 1.24 (1.54)",
     lambda g: [x for p in ("cut_C4", "wide_C4", "feed_neck", "cut_neck")
                for x in (cips_row(g, "main_iter1", "E", p)["specificity"], cips_row(g, "main_iter1", "E", p)["specificity_acting"])],
     [2] * 8),
    ("cips:E_cut_C4", 1, "kF0's own device-1 energy on the neck programs 0.97-1.01x its no-action value",
     lambda g: [own_dev1(g, "feed_neck", "ablate_kF0"), own_dev1(g, "cut_neck", "ablate_kF0")], [2, 2]),
    ("cips:E_cut_C4", 1, "independent_native device-1 score 0.034-0.042 on the neck programs against 0.052 with no action",
     lambda g: [min(native_dev1(g, p) for p in ("feed_neck", "cut_neck", "hold_neck")),
                max(native_dev1(g, p) for p in ("feed_neck", "cut_neck", "hold_neck")),
                gmean(raw(g, "cips", "main_iter1", "c001")["independent_native"], "device1")], [3, 3, 3]),
    ("cips:E_cut_C4", 1, "acting-device native band reaches 1.36 on cut_neck",
     lambda g: [cips_row(g, "main_iter1", "D", "cut_neck")["band_acting"]], [2]),
    ("cips:E_cut_C4", 2, "D's control (d0) ratio here 21.7 against 30.7 with no action",
     lambda g: [pc(g, "cips", "main_iter1", "c008")["ablate_d0"], pc(g, "cips", "main_iter1", "c001")["ablate_d0"]], [1, 1]),
    ("cips:E_cut_C4", 3, "null fails on this case at device 0 (ratio 2.0; 1.23 aggregate)",
     lambda g: [pc(g, "cips", "main_iter1", "c008")["numerical_null_sensors"]["device0"], pc(g, "cips", "main_iter1", "c008")["numerical_null"]],
     [1, 2]),
    ("cips:media2/moat_C4", 2, "ignore_actions 14.41x (11.13x at device 0); kF0 195.65x, 8.39x at device 0 (no action 78.56x)",
     lambda g: (lambda m: [m["ignore_actions"]["aggregate"], m["ignore_actions"]["device0"], m["kF0"]["aggregate"], m["kF0"]["device0"],
                           m["kF0_no_action"]["device0"]])(g("cips", "main_iter2", "specificity.json")["moat"]), [2, 2, 2, 2, 2]),
    ("cips:media2/moat_C4", 3, "null 1.3x (1.3/1.3/1.29 by sensor), above the native band 1.19x",
     lambda g: (lambda m: [m["numerical_null"]["aggregate"], *[m["numerical_null"][s] for s in SENS], m["band_native"]["aggregate"],
                           m["numerical_null"]["aggregate"] > m["band_native"]["aggregate"]])
     (g("cips", "main_iter2", "specificity.json")["moat"]), [2, 2, 2, 2, 2, None]),
    ("gaps:cips", None, "The moat case's dt-halved null exceeds its band (null / band on moat_C4, unrounded)",
     lambda g: [pc(g, "cips", "main_iter2", "c012")["numerical_null"], pc(g, "cips", "main_iter2", "c012")["band_native"]], [3, 3]),
    ("cips:D_cut_neck", 1, "d0 aggregate cut_neck 1.25, hold_neck 1.51, feed_neck 1.14; device 1: 1.57, 1.08, 1.17; cut_C4 0.71, 0.81",
     lambda g: [cips_row(g, "main_iter1", "D", p)["specificity"] for p in ("cut_neck", "hold_neck", "feed_neck")] +
               [cips_row(g, "main_iter1", "D", p)["specificity_acting"] for p in ("cut_neck", "hold_neck", "feed_neck")] +
               [cips_row(g, "main_iter1", "D", "cut_C4")["specificity"], cips_row(g, "main_iter1", "D", "cut_C4")["specificity_acting"]],
     [2] * 8),
    ("cips:D_cut_neck", 1, "d0's own device-1 energy 1.03x (cut_neck), 0.78x (hold_neck), 0.93x (feed_neck) its no-action value",
     lambda g: [own_dev1(g, p, "ablate_d0") for p in ("cut_neck", "hold_neck", "feed_neck")], [2, 2, 2]),
    # ---------------------------------------------------------------- rods
    ("rods:media2/S_steer", 2, "dt-halved null: no action 1.02, this case 0.98; native band (70 subsets) 0.975-1.078",
     lambda g: [pc(g, "rods", "formation", "c001")["numerical_null"], pc(g, "rods", "formation", "c002")["numerical_null"],
                g("rods", "formation", "band.json")["band_aggregate"][0], g("rods", "formation", "band.json")["band_aggregate"][2]],
     [2, 2, 3, 3]),
    ("rods:media2/W_pour_follow", 1, "device 1 cargo ratio 1.35 vs 1.36 (walloff, this case vs no action)",
     lambda g: [rods_group_ratio(g, "main_iter2", "c015", "ablate_walloff", "device1/c"),
                rods_group_ratio(g, "main_iter2", "c001", "ablate_walloff", "device1/c")], [2, 2]),
    ("rods:media2/W_pour_follow", 4, "second native ensemble on this case 1.13, above the 0.91-0.96 of the first iteration's band cases",
     lambda g: [pc(g, "rods", "main_iter2", "c015")["band_native"],
                min(pc(g, "rods", "main_iter1", c)["band_native"] for c in ("c001", "c007")),
                max(pc(g, "rods", "main_iter1", c)["band_native"] for c in ("c001", "c007"))], [2, 2, 2]),
]


def fmt(v, d):
    if d is None:
        return str(v)
    return f"{v:.{d}f}"


def main():
    out = []
    for card, idx, label, fn, dec in SPECS:
        read = set()

        def logged(e):
            base = P.getter(e)

            def get(w, s, name):
                read.add(f"{P.folder(w, s, 'stored')}/{name.split('/')[0] if name.startswith('controls/') else name}")
                return base(w, s, name)
            return get
        vals = {e: fn(logged(e)) for e in ("plugin", "fair")}
        if card.startswith("gaps:"):
            sys.path.insert(0, "/home/user/evalwork/showcase/page")
            import build_gc
            text = next(W for W in build_gc.WORLDS if W["key"] == card[5:])["gaps"]
        else:
            w, c = card.split(":", 1)
            text = K.published(w, c, P.GC)["caveats"][idx]
        old = [fmt(v, d) for v, d in zip(vals["plugin"], dec)]
        new = [fmt(v, d) for v, d in zip(vals["fair"], dec)]
        found = [o in text or (o.endswith("0") and o.rstrip("0").rstrip(".") in text) for o, d in zip(old, dec) if d is not None]
        pub = (f"/home/user/evalwork/showcase/page/build_gc.py WORLDS gaps" if card.startswith("gaps:") else
               K.published_path(*card.split(":", 1), P.GC))
        out.append(dict(card=card, caveat_index=idx, quote=label, text=text, old=old, new=new,
                        old_found_in_text=all(found), changed=old != new, published_in=pub,
                        recomputed_from=sorted(read), shadow="rescore_fair/out/<world>/<suite>/{plugin,fair}/ (same file names)"))
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "page_numbers.json").write_text(json.dumps(out, indent=1) + "\n")
    for o in out:
        print(("   " if o["old_found_in_text"] else "?? ") + f"{o['card']}#{o['caveat_index']}: {o['quote']}\n      old {o['old']}\n      new {o['new']}")


if __name__ == "__main__":
    main()
