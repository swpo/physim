"""make_summary -- collects the design-phase numbers into results/summary.json and prints the tables of DESIGN.md.
numpy-free; reads results/screen_*.json, views_*.json, surrogate.json, dose_XW.json, check_zero.json, probe.json,
baseline_by_class.json. Every entry names its source file and key."""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda f: json.load(open(os.path.join(HERE, "results", f)))
NAMES = {"a": "none", "c": "mix aimed 200", "d": "mix regional 300", "s": "designed push 200", "q": "designed squeeze 200"}
sur = {(r["file"]): r for r in R("surrogate.json")["rows"]}
out = {"what": "design-phase numbers of round6/dials/defect_gliders (CPU only; tiny sizes: 6 hidden states x 5 replicates; pilot seeds, never an exam)",
       "PILOT_NEVER_REUSE_AS_EXAM": True, "candidates": [], "sources": "results/<file> named in every row"}
rows = []
for f in sorted(glob.glob(os.path.join(HERE, "results", "screen_*.json"))):
    d = json.load(open(f))
    for cls, v in d["programs"].items():
        s = sur.get(f"fut_{d['cand']}_{d['eta']:g}_{cls}.npz")
        row = {"cand": d["cand"], "eta": d["eta"], "program": NAMES[cls], "source": os.path.basename(f) + f" [programs.{cls}]",
               "state_given_screen": v["screen_pooled"], "se": v["screen_pooled_se_jackknife_states"],
               "pair_rms_max": v["pair_rms_max"], "c0_change": sum(v["c0_mass_change_frac_true_mean_per_state"]) / len(v["c0_mass_change_frac_true_mean_per_state"]),
               "history_only_share_LLR": None if s is None else s["share_pooled"], "history_only_share_LLR_se": None if s is None else s["share_se_jackknife_states"],
               "kept_fraction": None if s is None or abs(v["screen_pooled"]) < 0.01 else s["kept_fraction"],
               "RES_closed": None if s is None or "generic_residual" not in s else {k: [x["closed_pooled"], x["closed_se_jackknife_states"]] for k, x in s["generic_residual"].items() if k != "what"}}
        rows.append(row)
out["candidates"] = rows
v = R("views_XW_4.json")
out["XW_eta4_horizons_1_to_16"] = {"source": "views_XW_4.json, surrogate.json rows fut16_XW_4_*", "programs": {
    NAMES[c]: {"block_state_given": [v["programs"][c]["block"]["screen_pooled"], v["programs"][c]["block"]["screen_se_jackknife_states"]],
               "block_state_given_per_horizon": v["programs"][c]["block"]["screen_per_horizon"],
               "pop_state_given": [v["programs"][c]["pop"]["screen_pooled"], v["programs"][c]["pop"]["screen_se_jackknife_states"]],
               "pop_INC_share": [v["programs"][c]["pop"]["surrogate_share_pooled"], v["programs"][c]["pop"]["surrogate_share_se_jackknife_states"]],
               "block_LLR_share": [sur[f"fut16_XW_4_{c}.npz"]["share_pooled"], sur[f"fut16_XW_4_{c}.npz"]["share_se_jackknife_states"]],
               "LLR_skill_vs_O_true_public": [sur[f"fut16_XW_4_{c}.npz"]["skill_LLR_true_vs_O"], sur[f"fut16_XW_4_{c}.npz"]["skill_LLR_public_vs_O"]],
               "RES_closed": {k: [x["closed_pooled"], x["closed_se_jackknife_states"]] for k, x in sur[f"fut16_XW_4_{c}.npz"]["generic_residual"].items() if k != "what"},
               "RES_share_left": {k: x["share_left"] for k, x in sur[f"fut16_XW_4_{c}.npz"]["generic_residual"].items() if k != "what"}}
    for c in ("c", "d")}}
x = out["XW_eta4_horizons_1_to_16"]["programs"]
sa, sd = x[NAMES["c"]]["block_LLR_share"][0], x[NAMES["d"]]["block_LLR_share"][0]
out["forecast_block_view_eta4"] = {
    "note": "LLR surrogate shares; classes none and blind taken as 0 (blind not run); an estimate from 6 states, not a measurement of sigma",
    "share_triggered_classes": (sa + sd) / 2, "share_full_mix": (sa + sd) / 4,
    "share_left_after_RES_per_class_n1_n2_n3": {NAMES[c]: [x[NAMES[c]]["RES_share_left"][k] for k in ("n1", "n2", "n3")] for c in ("c", "d")}}
out["calibration"] = {"hidden_parameter_lR_plus_0.06": [r for r in rows if r["cand"] == "PAR"],
                      "round5_ladder_n1_block": {"sigma": 0.005, "state_given": 0.127, "source": "round5/ladder/README.md table, row 1 | block (1 - plugPM 0.873)"}}
out["zero_point"] = {"check_zero": R("check_zero.json")["bitwise_equal_to_gworld"], "source": "check_zero.json",
                     "baseline_by_class_block": {c: R("baseline_by_class.json")["views"]["block"][c]["sigma_P0"] for c in ("all", "a", "b", "c", "d", "cd")},
                     "baseline_by_class_pop": {c: R("baseline_by_class.json")["views"]["pop"][c]["sigma_P0"] for c in ("all", "cd")}}
out["dose_response_XW_eta4"] = R("dose_XW.json")["rows"]
out["probe"] = {k: R("probe.json")[k] for k in ("background", "programs", "speed_one_thread")}
json.dump(out, open(os.path.join(HERE, "results", "summary.json"), "w"), indent=1)
f3 = lambda v, se=None: "n/a" if v is None else (f"{v:.3f}" if se is None else f"{v:.3f} ± {se:.3f}")
print("| candidate | eta | program | state-given screen | same-noise distance (max) | history-only share (LLR) | kept |")
print("|---|---|---|---|---|---|---|")
for r in rows:
    print(f"| {r['cand']} | {r['eta']:g} | {r['program']} | {f3(r['state_given_screen'], r['se'])} | {r['pair_rms_max']:.3f} | {f3(r['history_only_share_LLR'], r['history_only_share_LLR_se'])} | {f3(r['kept_fraction'])} |")
print(json.dumps(out["XW_eta4_horizons_1_to_16"], indent=1)[:3000])
print(json.dumps(out["forecast_block_view_eta4"], indent=1))
