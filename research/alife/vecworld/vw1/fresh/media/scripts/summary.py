"""Collect every number the page will state from the media key's result files -> results/summary.json."""
import json
import os

R = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
M = "/home/user/evalwork/vecworld/vw1/fresh/media/media"
S = "/home/user/evalwork/vecworld/vw1/fresh/media/scripts"
L = lambda f: json.load(open(f"{R}/{f}"))
ho, hc, hb = L("hero_objects_s0.json"), L("hero_coarse_s0.json"), L("hero_both_s0.json")
rh, ef, bl, cl, lg = L("render_hero.json"), L("events_fig.json"), L("blind.json"), L("compare_l0.json"), L("legibility.json")
H, SE, sz = lg["headline"], lg["bootstrap_se_over_trajectories"], lg["sizes"]
src_leg = {"source": f"{R}/legibility.json", "data": f"{R}/stats_both_J24_T300.npz",
           "scripts": [f"{S}/stats_run.py", f"{S}/stats_analyze.py"],
           "sizes": f"{sz['trajectories']} trajectories x {sz['ticks_per_trajectory']} ticks (+50 burn-in), 'both' world, "
                    f"designer.ensemble seed ({sz['designer_ensemble_seed']},), world_seed 0, no input",
           "se_method": f"bootstrap over trajectories, {lg['n_boot']} resamples"}


def v(key, old=None, unit=""):
    d = {"value": H[key], "se": SE.get(key), "unit": unit, **src_leg}
    if old is not None:
        d["old_page_vw0"] = old
    return d


out = {
    "about": "Media key: hero videos, legibility statistics and blind structure recovery, all from fresh VW-1 runs "
             "(aworld.MapWorld on the JAX Flow-Lenia port; VW-0 analysis/drawing helpers used read-only on VW-1 outputs).",
    "hero_episode": {
        "api": "World.reset(0) then World.step(None) x 300 (agent API); level 0 and level 1 from designer.state() of the same episode",
        "seed": 0, "world_seed": 0, "ticks": 300, "steps_per_tick": 20,
        "objects_present_median_min_max": [ho["objects_present"]["median"], ho["objects_present"]["min"], ho["objects_present"]["max"]],
        "tracker_events": ho["tracker_events_over_episode"],
        "obs_bitwise_equal_to_quantised_permuted_designer_level": {"objects": ho["obs_equal_quantised_permuted_designer_level_bitwise"],
                                                                   "coarse": hc["obs_equal_quantised_permuted_designer_level_bitwise"],
                                                                   "both": hb["obs_equal_quantised_permuted_designer_level_bitwise"]},
        "cpu_s": {"objects": ho["cpu_s"], "coarse": hc["cpu_s"], "both": hb["cpu_s"]},
        "card_keys": sorted(ho["card"].keys()), "card_has_no_world_or_coarse_graining_name": not any(
            s in json.dumps(ho["card"]) for s in ("A_gliders", "objects", "coarse", "Phi", "slot")),
        "fusion_example": {k: ef["chosen"][k] for k in ("t_fusion", "t_fission", "slot", "absorbed", "worm_mass")},
        "source": [f"{R}/hero_objects_s0.json", f"{R}/hero_coarse_s0.json", f"{R}/hero_both_s0.json", f"{S}/hero_run.py"]},
    "same_hidden_episode_across_views": {
        "level0_identical_all_300_ticks": {k: cl[k]["level0_identical_all_ticks"] for k in ("objects_vs_coarse", "objects_vs_both", "coarse_vs_both")},
        "input_map_identical": {k: cl[k]["in_map_identical"] for k in ("objects_vs_coarse", "objects_vs_both", "coarse_vs_both")},
        "note": "same world_seed and reset seed => same hidden trajectory and same hidden input permutation in every view",
        "source": f"{R}/compare_l0.json"},
    "media": {k: {"file": rh[k]["file"], "bytes": rh[k]["bytes"], "frames": rh[k]["frames"], "crf": rh[k]["crf"],
                  "poster": rh[k]["poster"], "poster_tick": rh[k]["poster_tick"], "codec": "H.264 yuv420p 896x590 15 fps"}
              for k in ("objects", "coarse")},
    "legibility": {
        "objects_per_tick_median": v("objects_median", 8.0),
        "objects_per_tick_mean": v("objects_mean"),
        "objects_per_tick_p10_p90": {"value": [lg["objects_stats_vw0_estimator"]["objects_per_tick"]["p10"],
                                               lg["objects_stats_vw0_estimator"]["objects_per_tick"]["p90"]], "old_page_vw0": [6, 9], **src_leg},
        "body_length_px": v("body_length_px", 12.70, "px (2.4 x median radius of gyration)"),
        "speed_px_per_tick_median": v("speed_px_per_tick_median", 1.611, "px per tick (continuing slots)"),
        "ticks_to_cross_body_length": v("ticks_to_cross_body_length", 7.88, "ticks"),
        "track_path_body_lengths_median_tracks_ge_50_ticks": v("path_body_lengths_median_tracks_ge_50", 7.55, "body lengths"),
        "frac_tracks_ge_50_ticks": v("frac_tracks_ge_50", 0.160),
        "frac_long_tracks_path_ge_3_body_lengths": v("frac_tracks_ge_50_with_path_ge_3", 0.976),
        "track_path_body_lengths_median_all_tracks": {"value": H["path_body_lengths_median_all_tracks"], **src_leg},
        "track_life_median_ticks": v("track_life_median_ticks", 20.0, "ticks"),
        "fusions_per_100_ticks": v("fusions_per_100_ticks", 23.2, "per 100 ticks per trajectory (all objects)"),
        "fissions_per_100_ticks": v("fissions_per_100_ticks", 22.8, "per 100 ticks per trajectory (all objects)"),
        "fusion_to_fission_ratio": {"value": lg["fusion_to_fission_ratio"], **src_leg},
        "births_deaths_total": [lg["events_total"]["births"], lg["events_total"]["deaths"]],
        "encounters_per_100_ticks": v("encounters_per_100_ticks", 18.3),
        "encounters_fused_within_5_ticks": v("encounters_fused_within_5_ticks", 0.649),
        "frac_present_slot_ticks_with_tracker_event_at_t_plus_1": v("frac_slot_ticks_event_at_t+1", 0.16),
        "frac_present_slot_ticks_with_tracker_event_at_t_plus_1_at_ticks_60_140_220": v("frac_slot_ticks_event_at_t+1_at_ticks_60_140_220", 0.157),
        "frac_tracks_censored_by_300_tick_window": {"value": H["frac_tracks_censored_by_window"], **src_leg},
        "glider_mass_median": v("mass_median", 146.3),
        "trajectories_with_fusion_and_fission": {"value": lg["trajectories_with_fusion_and_fission"], "of": sz["trajectories"], **src_leg},
        "mass_max_rel_drift_per_channel_over_300_ticks": {"value": lg["mass"]["max_rel_drift_per_channel_over_run"],
                                                          "old_page_vw0": 1.9e-14, "how": "Ensemble.invariants every tick", **src_leg},
        "sim_cpu_s": sz["sim_cpu_s"],
        "rubric_verdict": ("I Supported (median 7 bodies, no births or deaths, bodies persist through identity churn); "
                           "M Supported (98% of tracks living >= 50 ticks travel >= 3 body lengths, median 7.8; known Flow-Lenia "
                           "gliders, novelty 0); X Weak (fusion 22.5 and fission 22.3 per 100 ticks, 63% of encounters fuse "
                           "within 5 ticks, no matched ablation, merges = splits); D absent (fission without growth: mass fixed "
                           "to 2e-14, so splitting is fragmentation); S not met (planted noise patches)")},
    "anonymisation": {
        "objects": {**bl["objects"], "old_page_vw0": {"presence_coords_found": 12, "coords_assigned_to_correct_slot_frac": 1.0,
                                                      "position_pairs": "24 of 24"}},
        "coarse": {**bl["coarse"], "old_page_vw0": {"best_partner_in_same_block_frac": 1.0}},
        "both": bl["both"],
        "episode": "one fresh agent episode per view: World.reset(0), World.step(None) x 300 (301 observations)",
        "rules": bl["rules"], "source": f"{R}/blind.json", "script": f"{S}/blind.py"},
}
json.dump(out, open(f"{R}/summary.json", "w"), indent=1)
print(json.dumps(out["legibility"]["ticks_to_cross_body_length"], indent=1)[:400])
