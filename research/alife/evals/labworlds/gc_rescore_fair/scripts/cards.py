"""The showcase page's cards (build_gc.py WORLDS[*]['order']): where each card's score block comes from, rebuilt from a
suite report folder (stored, plugin shadow or fair shadow) the way the world's fact-sheet script built it, and tagged
with build_gc.verdict(). card_scores(get) -> {card: {ratio, ratio_na, spec, pr, pr_na, pspec, tag}}."""
from __future__ import annotations

GC_PAGE_ORDER = {
    "vortex": ["media2/S_steer", "media2/S_wide", "I_follow", "D_starve_neck", "long2/media/HD_wide", "E_feed",
               "H_inherit", "H_carry", "long2/media/H_seed"],
    "phase_membrane": ["media2/probe_wide", "media2/sink_site", "I_wide_A", "B_links_core", "media2/follow_B",
                       "media2/follow_B_feed", "BD_links_bath"],
    "cips": ["media2/steer_p", "media2/keep_empty", "I_enter_exit", "I_wide_C4", "B_s_core", "B_s_bath", "E_cut_C4",
             "media2/moat_C4", "D_cut_neck"],
    "rods": ["media2/S_steer", "I_I_seed_E1", "B_B_wipe_slow", "media2/W_pour_follow", "M_M_follow_swim",
             "D_D_follow_div", "Wd_Wd_label_div"],
}
# card -> (suite label, method, args); methods mirror the worlds' fact-sheet scripts
CARDS = {
    ("vortex", "media2/S_steer"): ("formation", "mscore", ("S_steer", "k0", "device0/om")),
    ("vortex", "media2/S_wide"): ("formation", "mscore", ("S_wide", "k0", "device1/om")),
    ("vortex", "I_follow"): ("main", "vortex_pooled", ("I_follow", "I", "k0")),
    ("vortex", "D_starve_neck"): ("main", "vortex_pooled", ("D_starve_neck", "D", "adv0")),
    ("vortex", "long2/media/HD_wide"): ("long2", "mscore", ("HD_wide", "adv0", "device1/om")),
    ("vortex", "E_feed"): ("main", "vortex_pooled", ("E_feed", "E", "k0")),
    ("vortex", "H_inherit"): ("main", "vortex_pooled", ("H_inherit", "H", "eps0")),
    ("vortex", "H_carry"): ("main", "vortex_pooled", ("H_carry", "H", "eps0")),
    ("vortex", "long2/media/H_seed"): ("long2", "mscore", ("H_seed", "eps0", "device1/b")),
    ("phase_membrane", "media2/probe_wide"): ("formation", "pm2", ("probe_wide", "S", "a0")),
    ("phase_membrane", "media2/sink_site"): ("formation", "pm2", ("sink_site", "S", "a0")),
    ("phase_membrane", "I_wide_A"): ("main_iter1", "pm1", ("wide_A", "I", "a0")),
    ("phase_membrane", "B_links_core"): ("main_iter1", "pm1", ("links_core", "B", "chi0")),
    ("phase_membrane", "media2/follow_B"): ("main_iter2", "pm2", ("follow_B", "D", "DS2")),
    ("phase_membrane", "media2/follow_B_feed"): ("main_iter2", "pm2", ("follow_B_feed", "D", "DS2")),
    ("phase_membrane", "BD_links_bath"): ("main_iter1", "pm1", ("links_bath", "BD", "twin")),
    ("cips", "media2/steer_p"): ("formation", "cips_f", ("steer_p",)),
    ("cips", "media2/keep_empty"): ("formation", "cips_f", ("keep_empty",)),
    ("cips", "I_enter_exit"): ("main_iter1", "spec_row", ("enter_exit", "I")),
    ("cips", "I_wide_C4"): ("main_iter1", "spec_row", ("wide_C4", "I")),
    ("cips", "B_s_core"): ("main_iter1", "spec_row", ("s_core", "B")),
    ("cips", "B_s_bath"): ("main_iter1", "spec_row", ("s_bath", "B")),
    ("cips", "E_cut_C4"): ("main_iter1", "spec_row", ("cut_C4", "E")),
    ("cips", "media2/moat_C4"): ("main_iter2", "spec_row", ("moat_C4", "E")),
    ("cips", "D_cut_neck"): ("main_iter1", "spec_row", ("cut_neck", "D")),
    ("rods", "media2/S_steer"): ("formation", "rods_row", ("S_steer", "S:a0")),
    ("rods", "I_I_seed_E1"): ("main_iter1", "rods_row", ("I_seed_E1", "I:a0")),
    ("rods", "B_B_wipe_slow"): ("main_iter1", "rods_row", ("B_wipe_slow", "B:chis0")),
    ("rods", "media2/W_pour_follow"): ("main_iter2", "rods_row", ("W_pour_follow", "W:walloff")),
    ("rods", "M_M_follow_swim"): ("main_iter1", "rods_row", ("M_follow_swim", "M:mar0")),
    ("rods", "D_D_follow_div"): ("main_iter1", "rods_row", ("D_follow_div", "D:passive")),
    ("rods", "Wd_Wd_label_div"): ("main_iter1", "rods_row", ("Wd_label_div", "Wd:kappa0")),
}
OVERRIDES = {"D_cut_neck": ("global", "whole-world (ratio artefact)")}   # build_gc.OVERRIDES


def r(x, d):
    return None if x is None else round(x, d)


def card_numbers(world, card, get):
    """get(world, suite_label, filename) -> parsed JSON from the report folder being read."""
    label, method, args = CARDS[(world, card)]
    if method == "mscore":            # vortex scripts2/mscore.py score_block, from report.json per_case
        program, control, probe = args
        rep, s = get(world, label, "report.json"), get(world, label, "suite.json")
        cid = [c["id"] for c in s["cases"] if c["program"] == program][0]
        sham = [c["id"] for c in s["cases"] if not c["request"]["actions"]][0]
        pc, ps = rep["per_case"][cid], rep["per_case"][sham]
        ratio, r0 = pc.get(control), ps.get(control)
        pr, pr0 = pc["groups"].get(control, {}).get(probe), ps["groups"].get(control, {}).get(probe)
        return dict(ratio=r(ratio, 3), ratio_na=r(r0, 3), spec=r(ratio / r0, 3), probe=probe, pr=r(pr, 3), pr_na=r(pr0, 3))
    if method == "vortex_pooled":     # vortex scripts/facts.py, from suite/specificity.json (pooled native reference)
        program, cap, ctrl = args
        sp = get(world, label, "specificity.json")[f"{cap}:{ctrl}"]
        row = next(x for x in sp["programs"] if x["program"] == program)
        return dict(ratio=r(row["ratio"], 2), ratio_na=r(sp["no_action"], 2), spec=r(row["ratio"] / sp["no_action"], 2),
                    probe=row["group"], pr=r(row["group_ratio"], 2), pr_na=r(row["group_ratio_no_action"], 2))
    if method in ("pm1", "pm2"):      # phase_membrane make_facts.py / media2 facts2.py
        program, cap, ctl = args
        s, rep, sp = get(world, label, "suite.json"), get(world, label, "report.json"), get(world, label, "specificity.json")
        cid = next(c["request"]["id"] for c in s["cases"] if c["family"] == program)
        row = next(x for x in sp["specificity"][cap]["programs"] if x["program"] == program)
        return dict(ratio=r(rep["per_case"][cid][f"ablate_{ctl}"], 2), ratio_na=row["ratio_sham"], spec=row["specificity"],
                    probe=row["acting"], pr=row["ratio_acting"], pr_na=row["ratio_acting_sham"])
    if method == "spec_row":          # cips make_facts.py (iteration 1) and make_facts2.py moat_C4 (iter2)
        program, cap = args
        sp = get(world, label, "specificity.json")
        row = next(x for x in sp["specificity"][cap]["programs"] if x["program"] == program)
        return dict(ratio=row["ratio"], ratio_na=row["ratio_sham"], spec=row["specificity"], probe=row["acting"],
                    pr=row["ratio_acting"], pr_na=row["ratio_acting_sham"])
    if method == "cips_f":            # cips make_facts2.py, formation/suite/specificity.json programs
        (program,) = args
        row = next(x for x in get(world, label, "specificity.json")["programs"] if x["program"] == program)
        return dict(ratio=row["ratio"], ratio_na=row["ratio_sham"], spec=row["specificity"], probe=row["acting"],
                    pr=row["ratio_acting"], pr_na=row["ratio_acting_sham"])
    if method == "rods_row":          # rods make_facts.py / make_facts2.py, report.json specificity rows
        program, key = args
        row = next(x for x in get(world, label, "report.json")["specificity"][key]["programs"] if x["program"] == program)
        return dict(ratio=row["ratio"], ratio_na=row["ratio_sham"], spec=row["specificity"], probe=row["acting"],
                    pr=row["ratio_acting"], pr_na=row["ratio_acting_sham"])
    raise ValueError(method)


def verdict(card, spec, pspec):
    prog = card.rsplit("/", 1)[-1]
    if prog in OVERRIDES:
        return OVERRIDES[prog][1]
    if (spec or 0) >= 1.5:
        return "specific"
    if (pspec or 0) >= 1.5:
        return "at the probe"
    return "whole-world"


def card_scores(get):
    out = {}
    for world, order in GC_PAGE_ORDER.items():
        for card in order:
            c = card_numbers(world, card, get)
            c["pspec"] = c["pr"] / c["pr_na"] if c.get("pr") and c.get("pr_na") else None
            c["tag"] = verdict(card, c["spec"], c["pspec"])
            c["suite"] = CARDS[(world, card)][0]
            out[f"{world}:{card}"] = c
    return out


def published_path(world, card, gc):
    folder, prog = (card.rsplit("/", 1) if "/" in card else ("media", card))
    return str(gc / world / folder / f"{prog}_facts.json")


def published(world, card, gc):
    """The score block as build_gc.norm() reads it from the published fact sheet."""
    import json
    folder, prog = (card.rsplit("/", 1) if "/" in card else ("media", card))
    d = json.loads((gc / world / folder / f"{prog}_facts.json").read_text())
    f = lambda x: None if x is None else float(max(x) if isinstance(x, (list, tuple)) else x)  # noqa: E731
    if d.get("suite") is not None and isinstance(d.get("without_mechanism"), dict) and "name" in d["without_mechanism"]:
        s = d["score"]
        out = dict(ratio=f(s["ratio"]), ratio_na=f(s["ratio_no_action"]), spec=f(s["specificity"]),
                   pr=f(s.get("probe_ratio")), pr_na=f(s.get("probe_ratio_no_action")))
    elif world == "vortex":
        s = d["score"]
        out = dict(ratio=f(s["ratio_this_case"]), ratio_na=f(s["ratio_on_no_action"]), spec=f(s["specificity_this_case"]),
                   pr=f(s.get("acting_group_ratio")), pr_na=f(s.get("acting_group_ratio_on_no_action")))
    elif world == "phase_membrane":
        s = d["score"]
        out = dict(ratio=f(s["score_ratio"]), ratio_na=f(s["same_control_on_no_action"]), spec=f(s["specificity"]),
                   pr=f(s.get("acting_device_ratio")), pr_na=f(s.get("acting_device_ratio_no_action")))
    elif world == "cips":
        s = d["scores"]
        out = dict(ratio=f(s["ratio"]), ratio_na=f(s["ratio_no_action"]), spec=f(s["specificity"]),
                   pr=f(s.get("ratio_acting")), pr_na=f(s.get("ratio_acting_no_action")))
    else:
        s = d["score"]
        out = dict(ratio=f(s["ratio_this_case"]), ratio_na=f(s["ratio_no_action_case"]), spec=f(s["specificity"]),
                   pr=f(s.get("acting_device_ratio")), pr_na=f(s.get("acting_device_ratio_no_action")))
    out["pspec"] = out["pr"] / out["pr_na"] if out.get("pr") and out.get("pr_na") else None
    out["tag"] = verdict(card, out["spec"], out["pspec"])
    out["caveats"] = d.get("caveats") or []
    if isinstance(out["caveats"], str):
        out["caveats"] = [out["caveats"]]
    return out
