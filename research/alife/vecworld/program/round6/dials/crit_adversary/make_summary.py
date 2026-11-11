"""make_summary -- the numbers of CRITIQUE.md section 1 from results/adv_s<seed>.json (adv_fit.py), in one file.

    python -B make_summary.py        -> results/summary.json

PILOT values, state-given check at tiny size (sublevel_second/gvh.py's own items); never to be reused as an exam.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
out = {"PILOT_NEVER_REUSE_AS_EXAM": True,
       "what": "share of the public-to-oracle gap closed on sublevel_second/gvh.py's check (chosen carrier: lam 1, cat 1, rho 0.02, "
               "DX 0.5, a0 0.03; 64 px; 16 Lab episodes), by horizon; source files results/adv_s<seed>.json",
       "horizons": [4, 8, 16, 32], "rows": [], "cpu_s": {}}
for s in (5, 6, 7, 8):
    d = json.load(open(os.path.join(HERE, "results", f"adv_s{s}.json")))
    out["cpu_s"][f"seed{s}_adv_sim"] = d["cpu_s_sim_gvh_part_bank_total"][2]
    for k in ("G2", "A_in_n16", "A_act_n4", "A_act_n8", "A_act_n16", "H", "ceiling_true_mean"):
        if k not in d["share_of_pub_to_O_gap"]:
            continue
        out["rows"].append({"seed": s, "policy": k, "closed_by_horizon": [round(v, 3) for v in d["closed_by_horizon"][k]],
                            "closed_h_le_16": round(d["closed_h_le_16"][k], 3), "closed_h_8_16_32": round(d["closed_h_8_16_32"][k], 3),
                            "pooled": round(d["share_of_pub_to_O_gap"][k]["value"], 3), "pooled_se_members": round(d["share_of_pub_to_O_gap"][k]["se_members"], 3),
                            "fit": d["recipes"].get(k, {}).get("fit_g0_g1_tau_blur")})
    out[f"seed{s}"] = {"gap_share_by_horizon": [round(v, 3) for v in d["gap_pub_to_O"]["share_by_horizon"]],
                       "largest_member_share_of_gap": round(max(d["gap_pub_to_O"]["share_by_test_member"].values()), 3),
                       "n_test_members": len(d["test_members"]), "heaviest_member_focus_mass": d["heaviest_member_focus_mass"],
                       "paired_differences_value_se": d["paired_differences_value_se"],
                       "designer_file_max_abs_diff_L": d.get("designer_file", {}).get("max_abs_diff_L_pub_pub0_O_G2"),
                       "role": {5: "development seed of the adversary's recipes", 6: "recipes frozen before this seed ran; the designer's H re-run",
                                7: "the designer's runs only (bank=0)", 8: "the designer's runs only (bank=0)"}[s]}
out["cpu_s"]["adv_act_seed5_seed6"] = "224.1 and 202.3 (printed by adv_act.py; logs were scratch)"
out["cpu_s"]["total_about"] = round(sum(v for v in out["cpu_s"].values() if isinstance(v, float)) + 224.1 + 202.3)
json.dump(out, open(os.path.join(HERE, "results", "summary.json"), "w"), indent=1)
for r in out["rows"]:
    print(r["seed"], f"{r['policy']:18s}", r["closed_by_horizon"], "h<=16", r["closed_h_le_16"], "exam h", r["closed_h_8_16_32"], "pooled", r["pooled"], "+-", r["pooled_se_members"], r["fit"] or "")
for s in (5, 6, 7, 8):
    print(s, out[f"seed{s}"]["gap_share_by_horizon"], out[f"seed{s}"]["largest_member_share_of_gap"], out[f"seed{s}"]["designer_file_max_abs_diff_L"])
print("cpu", out["cpu_s"])
