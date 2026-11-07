"""make_summary -- collect every number the report claims -> results/summary.json (each with its source)."""
import json
import os

import numpy as np

RES = "/home/user/evalwork/vecworld/program/track2/actuation/results"
L = lambda f: json.load(open(os.path.join(RES, f)))
chk, via, pe, dp = L("check_wind.json"), L("viability.json"), L("probe_effects.json"), L("dp_check.json")
HS = pe["horizons"]
r4 = lambda x: None if x is None else (round(x, 4) if isinstance(x, float) else [None if v is None else round(v, 4) for v in x])
src = lambda f: os.path.join(RES, f)

out = {"what": "Track 2 actuation probe: wind channel vs matter kick on the gliders world (A_gliders, VW-1 port)",
       "code": {"level_variant": "/home/user/evalwork/vecworld/program/track2/actuation/wind.py",
                "programs": "/home/user/evalwork/vecworld/program/track2/actuation/programs.py",
                "scripts": ["check_wind.py", "viability.py", "probe.py", "dp_check.py", "analyze.py", "make_summary.py"]},
       "channel": {"grid": "8 x 8 blocks of 16 px, 2 components (128 coefficients)",
                   "embedding": "piecewise-constant block field, periodic Gaussian blur std 8 px (FFT), DC gain 1",
                   "law": "field added to the Flow-Lenia flow of both channels in all 20 substeps of a tick, before the port's clip and reintegration",
                   "noise": "a~ = u + sigma_w eta, eta ~ N(0, I_128) once per tick (Noise.stream(7))",
                   "cost": "0.5 ||u||^2 / sigma_w^2 nats per tick",
                   "background_field_sd_per_sigma_w": chk["basis"]["background_field_sd_per_sigma_w"],
                   "random_walk_px_per_tick_per_sigma_w": r4(chk["basis"]["random_walk_px_per_tick_per_sigma_w"]),
                   "group2x2_field_at_body_range": [r4(chk["basis"]["group2x2_field_at_inner_block_centre"]),
                                                    r4(chk["basis"]["group2x2_field_at_group_centre"])],
                   "source": src("check_wind.json")},
       "checks": {"port_equivalence_sigma0": {**chk["port_equivalence"], "source": src("check_wind.json")},
                  "shift_structure": {**chk["shift_structure"], "source": src("check_wind.json")},
                  "kl_channel_monte_carlo": {**chk["kl_channel_mc"], "source": src("check_wind.json")},
                  "data_processing_level1": {**dp, "source": src("dp_check.json")}},
       "cpu_seconds": {"check_wind": round(chk["seconds"], 1), "viability_sim": round(sum(via["sim_seconds"]), 1),
                       "dp_check": round(dp["seconds"], 1)},
       "viability": {"design": f"{via['members']} members per sigma_w, init + {via['burn_in_ticks']} burn-in + "
                               f"{via['ticks_after_burn_in']} ticks, shared keys across sigma_w; native band = 2.5-97.5% of "
                               "3-trajectory means of the 36 noise-free closure trajectories",
                     "member_ticks": via["member_ticks"], "native_band": via["native_band_from_closure_runs"],
                     "per_sigma": {s: {k: (r4(v) if isinstance(v, float) else v) for k, v in r.items() if k != "per_member"}
                                   for s, r in via["per_sigma"].items()},
                     "source": src("viability.json")}}
# probe
probe_s = []
for f in sorted(os.listdir(os.path.join(RES, "probe"))):
    probe_s.append(float(np.load(os.path.join(RES, "probe", f))["seconds"]))
out["cpu_seconds"]["probe"] = round(sum(probe_s), 1)
out["cpu_seconds"]["total"] = round(sum(out["cpu_seconds"].values()), 1)
conds = {}
for c, row in pe["conditions"].items():
    d = {"budget": row["budget_mean"], "budget_unit": "L1 sum|a| over program" if c.startswith("KA") else "nats",
         "n_states": row["n_states"], "target_lateral_px_mean": r4(row["target_lateral_px_mean"]),
         "target_lateral_px_se": r4(row["target_lateral_px_se"]), "target_lost_share": r4(row["target_lost_share"])}
    if "kick_matter_moved_mean" in row:
        d["kick_matter_moved_mean"] = r4(row["kick_matter_moved_mean"])
    for v in ("coarse", "objects"):
        x = row[v]
        d[v] = {"ratio_to_Vbest_mean": r4(x["ratio_mean"]), "se": r4(x["ratio_se"]), "median": r4(x["ratio_median"]),
                "share_states_ge_0.1": r4(x["share_states_ge_0.1"]), "per_budget_unit": [float(f"{y:.3g}") for y in x["ratio_per_budget_unit"]],
                "paired_crn_ratio_mean": r4(x["paired_ratio_mean"]), "n64_mean_over_se": r4(x["n64_mean_over_se"])}
        if "ratio_vs_wind_world_Vbest_approx" in x:
            d[v]["ratio_to_wind_world_Vbest_approx"] = r4(x["ratio_vs_wind_world_Vbest_approx"])
    conds[c] = d
out["probe"] = {"design": "40 saved states x R = 3 shared noise keys; per state 11 conditions (+2 on states 0-9); "
                          "programs 4 ticks, open loop, aimed at one isolated moving body chosen at t = 0; records t = 0..16",
                "sigma_w": pe["sigma_w"], "horizons": HS, "V_best": pe["V_best"], "conditions": conds,
                "oracle_variance": pe["oracle_variance"],
                "scaling_check_same_push_quarter_background": pe.get("scaling_check_same_push_quarter_background"),
                "loglog_fits": pe["loglog_fits"], "budget_scan_vs_wind_world_Vbest": pe["budget_scan_vs_wind_world_Vbest"],
                "shift_per_nat_over_wind_dV": pe["shift_per_nat_over_wind_dV"],
                "source": src("probe_effects.json"), "raw": os.path.join(RES, "probe")}
# accounting
drift = [float(np.load(os.path.join(RES, "probe", f))["mass_drift"]) for f in sorted(os.listdir(os.path.join(RES, "probe")))]
nmem = [len(np.load(os.path.join(RES, "probe", f))["ci"]) for f in sorted(os.listdir(os.path.join(RES, "probe")))]
out["member_ticks"] = {"probe": int(sum(nmem) * 16), "viability": via["member_ticks"], "dp_check": dp["R"] * 3 * 4,
                       "check_wind": 3 + 8 + 3}
out["probe"]["mass_drift_max_abs"] = max(drift)
# headline numbers (all copied from the blocks above; source = probe_effects.json unless noted)
C = pe["conditions"]
ov = pe["oracle_variance"]
sc = pe["budget_scan_vs_wind_world_Vbest"]
pick = lambda c, v: [round(x, 4) for x in C[c][v]["ratio_mean"]]
out["headline"] = {
    "note": "ratio = unbiased squared shift of the state-conditioned level-1 mean per coordinate / closure V_best; "
            "horizons 1, 2, 4, 8, 16 ticks from program start; mean over 40 states; sigma_w = 0.2 unless noted",
    "WA2_coarse": pick("WA2", "coarse"), "WA12.5_coarse": pick("WA12.5", "coarse"), "WA50_coarse": pick("WA50", "coarse"),
    "WA12.5_objects": pick("WA12.5", "objects"), "WA50_objects": pick("WA50", "objects"),
    "WR12.5_coarse": pick("WR12.5", "coarse"), "WR50_coarse": pick("WR50", "coarse"), "WR50_objects": pick("WR50", "objects"),
    "KA4_coarse": pick("KA4", "coarse"), "KA16_coarse": pick("KA16", "coarse"), "KA64_coarse": pick("KA64", "coarse"),
    "KA16_objects": pick("KA16", "objects"), "KA64_objects": pick("KA64", "objects"),
    "WA_per_nat_coarse_C12.5": [float(f"{x:.3g}") for x in C["WA12.5"]["coarse"]["ratio_per_budget_unit"]],
    "WA_per_nat_objects_C50": [float(f"{x:.3g}") for x in C["WA50"]["objects"]["ratio_per_budget_unit"]],
    "WA_loglog_slopes_coarse": [round(pe["loglog_fits"][f"WA/coarse/h{h}"]["slope"], 3) for h in HS],
    "WA50_coarse_vs_wind_world_Vbest": [round(x, 4) for x in C["WA50"]["coarse"]["ratio_vs_wind_world_Vbest_approx"]],
    "WA50_objects_vs_wind_world_Vbest": [round(x, 4) for x in C["WA50"]["objects"]["ratio_vs_wind_world_Vbest_approx"]],
    "WA12.5_coarse_n64_mean_over_se": [round(x, 1) for x in C["WA12.5"]["coarse"]["n64_mean_over_se"]],
    "kick_equivalent_wind_nats_coarse_h1_h2_h4_h8": {k: [round(pe["loglog_fits"][f"WA/coarse/h{h}"][f"{k}_equivalent_wind_nats"], 2)
                                                        for h in (1, 2, 4, 8)] for k in ("KA16", "KA64")},
    "kick_matter_moved": {k: round(C[k]["kick_matter_moved_mean"], 2) for k in ("KA4", "KA16", "KA64")},
    "target_lateral_px": {k: [round(x, 2) for x in C[k]["target_lateral_px_mean"]] for k in ("WA2", "WA12.5", "WA50", "KA16", "KA64")},
    "same_push_quarter_background_ratio_coarse": [round(x, 3) for x in pe["scaling_check_same_push_quarter_background"]["coarse"]["ratio_q_over_main"]],
    "oracle_var_coarse_port": [round(x, 5) for x in ov["twin_0"]["coarse"]["mean"]],
    "oracle_var_coarse_wind0.2": [round(x, 5) for x in ov["twin_w"]["coarse"]["mean"]],
    "closure_V_oracle_coarse": [round(x, 5) for x in ov["wind_vs_port"]["coarse"]["closure_V_oracle"]],
    "dV_over_Vbest_coarse_sigma0.2": [round(x, 3) for x in ov["wind_vs_port"]["coarse"]["increase_over_V_best"]],
    "dV_over_Vbest_objects_sigma0.2": [round(x, 3) for x in ov["wind_vs_port"]["objects"]["increase_over_V_best"]],
    "dV_quarter_over_main_coarse": [round(x, 3) for x in ov["sigma2_scaling_check"]["coarse"]["ratio_quarter_over_main"]],
    "C_nats_for_0.1_wind_world_Vbest_WA": {s_: {k: round(v["C_nats"], 1) for k, v in row.items()
                                                 if v and k.startswith("WA/") and not k.endswith("h16")}
                                           for s_, row in sc.items()},
    "dV_over_Vbest_by_sigma_coarse": {s_: [round(sc[s_][f"WA/coarse/h{h}"]["dV_over_Vbest"], 3) for h in (1, 2, 4, 8)] for s_ in sc},
    "dp_check_kl_proxy_C2": {h: round(r["kl_proxy_1d_nats"], 3) for h, r in dp["rows"]["2.0"].items()},
    "dp_check_kl_proxy_C12.5": {h: round(r["kl_proxy_1d_nats"], 3) for h, r in dp["rows"]["12.5"].items()},
    "viability_out_of_band": {s_: [k for k, ok in r["in_native_band"].items() if not ok] for s_, r in via["per_sigma"].items()},
    "viability_speed_p90": {s_: round(r["speed_p90"], 3) for s_, r in via["per_sigma"].items()},
}
json.dump(out, open(os.path.join(RES, "summary.json"), "w"), indent=1)
print("cpu", out["cpu_seconds"])
