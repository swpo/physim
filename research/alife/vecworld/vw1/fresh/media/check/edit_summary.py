"""Checker edits to results/summary.json (backup of the original in check/summary.orig.json).
Every edit is listed in summary['checker']['edits']."""
import json
import os
import shutil

R = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
C = "/home/user/evalwork/vecworld/vw1/fresh/media/check"
if not os.path.exists(f"{C}/summary.orig.json"):
    shutil.copy(f"{R}/summary.json", f"{C}/summary.orig.json")
s = json.load(open(f"{C}/summary.orig.json"))
L, edits = s["legibility"], []

# 1. event-slot share: the old 0.16 is a 3-tick sample; VW-0 over all ticks (same definition) is 0.1148
k = "frac_present_slot_ticks_with_tracker_event_at_t_plus_1"
L[k]["old_page_vw0"] = 0.1148
L[k]["old_page_vw0_counts"] = "6517 of 56766 slot-ticks (VW-0 integrate/data/A_gliders base_*.npz, all ticks, checker recomputation)"
L[k]["note"] = ("Fresh VW-1 (0.1147) equals VW-0 (0.1148) over all ticks. The page's '16% of the data' is the checker's "
                "VW-0 sample at ticks 60, 140, 220 only (88 of 560 = 0.157), not the overall share.")
edits.append(f"legibility.{k}.old_page_vw0: 0.16 -> 0.1148 (VW-0 all-tick value, same definition); note added")
k2 = k + "_at_ticks_60_140_220"
L[k2]["counts"] = "66 of 551 slot-ticks"
L[k2]["old_page_vw0_counts"] = "88 of 560"
L[k2]["note"] = "difference 3.7 points: z = 1.8 binomial, about 1.3 SE with the bootstrap SE on both sides; not significant"
edits.append(f"legibility.{k2}: counts 66/551 vs 88/560 and significance note added")

# 2. objects per tick: the median step 8 -> 7 is quantisation
L["objects_per_tick_mean"]["old_page_vw0"] = 7.654
L["objects_per_tick_mean"]["old_page_vw0_se"] = 0.088
L["objects_per_tick_median"]["note"] = ("median 8 -> 7 is a quantisation effect: mean 7.44 +- 0.11 (fresh) vs 7.65 +- 0.09 "
                                        "(VW-0, checker recomputation from base_*.npz), about 1.4 SE apart; 49% vs 55% of ticks "
                                        "have >= 8 objects. Page wording: 'seven or eight bodies (mean 7.4)', not 'median 7 vs 8'.")
edits.append("legibility.objects_per_tick_mean.old_page_vw0 = 7.654 +- 0.088 added; objects_per_tick_median.note added")

# 3. path label
L["track_path_body_lengths_median_tracks_ge_50_ticks"]["page_label"] = (
    "median over the 16% of tracks living >= 50 ticks (over all tracks: 2.2 body lengths; 21% of tracks censored by the window)")
edits.append("legibility.track_path_body_lengths_median_tracks_ge_50_ticks.page_label added (old page said 'Tracks travel a median of 7.6')")

# 4. rubric wording
old = L["rubric_verdict"]
L["rubric_verdict"] = old.replace("median 7 bodies", "7-8 bodies, mean 7.4").replace(
    "mass fixed to 2e-14", "mass conserved to 2e-14 relative")
edits.append("legibility.rubric_verdict: 'median 7 bodies' -> '7-8 bodies, mean 7.4'; 'mass fixed to 2e-14' -> 'mass conserved to 2e-14 relative'")

# 5. fusion example: slot 0 is not a single glider
fe = s["hero_episode"]["fusion_example"]
fe.update({"absorbed_mass": 277.0, "survivor_mass_before": 423.0, "fission_piece_mass": 137.0, "survivor_mass_after_fission": 563.0,
           "note": ("slot 0 (mass 277, about 1.9 median glider masses; itself formed by a fusion at tick 83) merges with slot 8 "
                    "(423) into a 700-mass curved worm; at tick 96 a 137-mass piece (about one glider) buds off as slot 1 and "
                    "slot 8 keeps 563; at tick 97 slot 8 absorbs slot 3 and sheds two more pieces (171, 105). "
                    "Do not caption it 'a glider fuses with body 8 ... splits again'.")})
edits.append("hero_episode.fusion_example: masses and caption note added (slot 0 is a 277-mass merged body, not a glider; "
             "tick 96 is a one-glider bud-off, not a split of the worm)")

# 6. cross-view sharing is not new
x = s["same_hidden_episode_across_views"]
x["status"] = ("not a new leak: the checker's VW-0 finding (companion worlds with one world seed share the input permutation) "
               "persists in VW-1. VW-1's key change separates different world seeds only (checker control: world_seed 1 "
               "gives a different level 0 and in_map). It matters only if one agent is given two views with one world seed.")
x["checker_reproduction"] = "check/rerun.json: coarse world re-run in a new process, level 0 identical to the saved objects episode for 61 ticks"
edits.append("same_hidden_episode_across_views.status added: persisting VW-0 leak, not new")

# 7. media notes
s["media"]["objects"]["checker_note"] = ("glyphs sit on the bodies in the poster and frames 5/150/295; one slot can cover two "
                                         "touching crescents (tick 150 slots 2 and 4); glyphs at the bottom edge spill over the "
                                         "strip's label row (cosmetic)")
s["media"]["coarse"]["checker_note"] = "bright blocks match the matter in the poster and frames 5/150/295"
edits.append("media.objects/coarse.checker_note added")

# 8. provenance wording
s["about_provenance_checked"] = ("No VW-0 simulator step runs. lenia_world.py is imported by the tracker inside phi.phi_objects "
                                 "(geometry and screen settings of its Level0 only) and by analyze.py (constants); render_l1 "
                                 "imports level0/render.py (colour map only), not level0/flowlenia.py.")
edits.append("about_provenance_checked added (report said lenia_world is imported only through the tracker)")

s["checker"] = {"edits": edits, "report": f"{R}/check.md",
                "independent_recomputation": f"{C}/recompute.json (all headline values equal to 1e-12)",
                "rerun": f"{C}/rerun.json (objects hero 60 ticks, coarse 60 ticks, ensemble(2, seed=(7,)) 30 ticks: bit for bit)",
                "cpu_s": 140}
json.dump(s, open(f"{R}/summary.json", "w"), indent=1)
print("\n".join(edits))
