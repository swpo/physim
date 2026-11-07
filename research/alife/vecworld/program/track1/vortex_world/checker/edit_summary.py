"""Checker edits to results/summary.json (each edit listed in checker.edits)."""
import json, os
import numpy as np

VWD = "/home/user/evalwork/vecworld/program/track1/vortex_world"
P = os.path.join(VWD, "results/summary.json")
CK = os.path.join(VWD, "checker")
S = json.load(open(P))
edits = []

# E1 wrong count in a note
old = S["repro"]["per_step_max_rel_diff"]["note"]
S["repro"]["per_step_max_rel_diff"]["note"] = (
    "one JAX step on numpy's state vs numpy's next state, max |diff|/max|field|, 100 step pairs (every 250th native step, "
    "0..24750), which include the labelling step 15000 and the mutation steps 17500, 20000, 22500; 128^2")
edits.append({"path": "repro.per_step_max_rel_diff.note", "old": old, "new": S["repro"]["per_step_max_rel_diff"]["note"],
              "why": "repro.json has 100 per-step pairs; the special steps are among them, not extra"})

# E2 seeds per arm (n_seeds = 4 is wrong for sel0)
S["pilot_64"]["design"]["value"]["seeds_per_arm"] = {"sel": 4, "neu": 4, "sel0": 2}
S["pilot_64"]["design"]["note"] = "n_seeds is the default; sel0 ran 2 seeds (pilot_H64.json seeds_per_arm)"
edits.append({"path": "pilot_64.design", "old": "n_seeds 4 only", "new": "added seeds_per_arm {sel 4, neu 4, sel0 2}",
              "why": "sel0 (noise off) has 2 seeds"})

# E3 'overflow' holds overflow counts AND peaks
for blk in ("pilot_64", "pilot_128"):
    S[blk]["timing"]["note"] = ("'overflow' rows are (raw_overflow_ticks, kept_overflow_ticks, raw_peak, kept_peak) per member "
                                "(vw/objects.py OVERFLOW): no overflow; peaks below max_raw/max_kept")
edits.append({"path": "pilot_64.timing.note, pilot_128.timing.note", "old": "(none)",
              "new": "overflow = (raw_overflow_ticks, kept_overflow_ticks, raw_peak, kept_peak); zero overflow",
              "why": "the last two numbers are peaks, not overflows"})

# E4 bootstrap wording + leave-out groups
old = S["pilot_64"]["closure_ceiling"]["note"]
S["pilot_64"]["closure_ceiling"]["note"] = (old + "; leave-out groups are (arm, seed), so 8 groups when pooled; "
                                            "bootstrap_c_w2_p16_p84 = 16th and 84th percentiles over 200 seed resamples (not full ranges); "
                                            "c is a lower bound (linear predictor) and is in units of 5-time-unit ticks")
edits.append({"path": "pilot_64.closure_ceiling.note", "old": old, "new": S["pilot_64"]["closure_ceiling"]["note"],
              "why": "report calls the 16-84% interval a 'range'"})

rc = json.load(open(os.path.join(CK, "recompute.json")))
s128 = np.load(os.path.join(CK, "seed128_s1.npz"))
sb1, sb0 = s128["sel"][:, 1].astype(np.float64), s128["neu"][:, 1].astype(np.float64)
k = np.ones(9) / 9

def first_major(sb):
    i = np.flatnonzero(np.convolve(sb, k, "valid") > 0.5)
    return float((i[0] + 4) * 5) if i.size else None

seed1 = {"T_ticks": int(len(sb1) - 1), "t_end": float((len(sb1) - 1) * 5),
         "sel_s_b_t500_1500": round(sb1[100:300].mean(), 3), "neu_s_b_t500_1500": round(sb0[100:300].mean(), 3),
         "sel_N_t500_1500": round(float(s128["sel"][100:300, 0].mean()), 2), "neu_N_t500_1500": round(float(s128["neu"][100:300, 0].mean()), 2),
         "sel_s_b_last50_ticks": round(sb1[-50:].mean(), 3), "neu_s_b_last50_ticks": round(sb0[-50:].mean(), 3),
         "first_t_majority_b": {"sel": first_major(sb1), "neu": first_major(sb0)}}

S["checker"] = {
    "source": "checker/ (rerun.py, recompute.py, edit_summary.py and their outputs); independent check, core 3",
    "edits": edits,
    "rerun_64_seed0": {"value": {"ticks": 200, "arms": ["sel", "neu"], "max_abs_diff_L2_vs_saved": 0.0, "cpu_s": 52.1},
                       "source": "checker/rerun.py repro64 200 (stdout), checker/repro64_s0.npz",
                       "note": "pilot.py's worlds, designer member 0, R = 0: level-2 identical to results/pilot_H64.npz rows to t = 1000"},
    "independent_128_seed1": {"value": seed1, "source": "checker/rerun.py seed128 300 1 -> checker/seed128_s1.npz, checker/seed128.log",
                              "note": "designer ensemble(1, seed=1), same twin design as pilot_H128 (seed 0); a second seed"},
    "recomputed": {"value": {k_: rc[k_] for k_ in ("64_sel", "64_neu", "64_sel0", "128_sel", "128_neu", "64_paired_mid",
                                                  "64_paired_late", "64_paired_late_N", "closure_pooled",
                                                  "closure_pooled_twins_held_out_together")},
                   "source": "checker/recompute.py -> checker/recompute.json (from results/pilot_H64.npz, pilot_H128.npz)",
                   "note": "matches analysis_H64/H128.json to the printed digits; L2 equals kinds(L1) to 3e-8"},
    "report_corrections": [
        {"claim": "64^2 count N late 8.4 vs 7.1", "correct": "8.25 vs 7.10", "source": "pilot_64.selection count_mean_late"},
        {"claim": "noise off at 64^2 (2 seeds) the shares are 0.62 and 0.56",
         "correct": "2-seed means: 0.62 in t 500-1500 and 0.56 in t 1500-2500 (per seed 0.71, 0.53 and 0.51, 0.62)",
         "source": "pilot_64.selection.sel0"},
        {"claim": "Level 2 stays closed at c >= 0.6 out to 32 ticks (160 t)",
         "correct": "true for s_b only (0.63 at 160 t); N is 0.59 at 40 t and 0.43 at 160 t", "source": "pilot_64.closure_ceiling.pooled"},
        {"claim": "Bootstrap ranges at 160 t: s_b 0.57-0.77, N 0.32-0.56", "correct": "16th-84th percentiles, not ranges",
         "source": "analyse.py boot()"},
        {"claim": "No program moved s_b by more than 0.07, which is within 2 SE",
         "correct": "max |ds_b| 0.074 (cut15 at 80 t, 1.5 SE); 1 of 15 program x horizon cells exceeds 2 SE (cut15 at 20 t: +0.024 +- 0.011, 2.2 SE), as expected by chance",
         "source": "input_probe_64 effects"},
        {"claim": "Same-sign stir 0.05 x 2 ticks: -0.35 +- 0.18", "correct": "at 10 t (h = 2 ticks); -0.25 +- 0.19 at 5 t, ~0 from 20 t on",
         "source": "input_probe_64 effects.feed05"},
        {"claim": "A 100-nat input moves the level-2 count by about one predictive SD",
         "correct": "1.19 sqrt(Ve) at 10 t only (+0.88 +- 0.35, 2.5 SE; 6 starts from one seed's trajectory); 0.62 at 20 t (1.7 SE), 0.35 at 40 t (0.9 SE); s_b unmoved",
         "source": "input_probe_64 effects.cut05"},
        {"claim": "eps shows at level 2 only during the rise (t <~ 2000)",
         "correct": "64^2 only; at 128^2 the port's seed 0 is still separated at t 1500-2200 (0.75 vs 0.27) and the source has 0.86-0.93 vs 0.38-0.60 at t 2000-4500 (3/3 seeds)",
         "source": "pilot_128.selection; physim c53 selection claim heredity_summary.txt"},
        {"claim": "the 128^2 result rests on one seed",
         "correct": "an independent seed (checker, designer seed 1, to t 1500) repeats the rise: s_b 0.40 vs 0.16 in t 500-1500, kind-b majority at t 1090, neutral never; the late window (t 1500-2200) is still one seed",
         "source": "checker.independent_128_seed1"},
        {"claim": "100 nats move N by about one predictive SD; gliders' open-loop programs moved the error by 1-2% at most",
         "correct": "in the same units (squared mean shift / predictive variance) vortex cut05 at 10 t gives 1.41 against gliders' <= 0.007 (body kick) and <= 0.022 (32-cell push) at level 1; unmatched: level-2 count vs level 1, best of 3 programs and 5 horizons, 6 starts from one trajectory, linear Ve vs best-of V_best",
         "source": "input_probe_64 effects.cut05['2'].N.in_sqrt_Ve = 1.186; CRITIQUE.md section 1a"},
        {"claim": "E4 passes provisionally", "correct": "not established: the closure and input comparisons with gliders are unmatched (level 2 of 2 numbers vs level 1, linear vs best-of predictors, no I1, horizons in designer-chosen ticks), the invariant premise is false, and input visibility is a transient N effect partly made by the tracker",
         "source": "checker review"},
        {"claim": "the selection signal at 64^2 appears during the rise",
         "correct": "paired sel-neu s_b in t 500-1500: +0.18 mean, 4/4 seeds positive, t = 3.08, p = 0.054 two-sided (sign test 1/16 one-sided); the neutral twin also reaches a kind-b majority in 4/4 seeds (t 470-955)",
         "source": "checker/recompute.json 64_paired_mid, 64_neu first_t_majority"},
    ],
    "checker_cpu_s": {"value": {"rerun_64_seed0_200ticks": 52.1, "test_vortex": 13.3, "seed128_s1_300ticks": 339.0, "recompute_plots_misc_est": 30, "total_min": 7.2}, "source": "checker/seed128.log and rerun stdout (user time)"},
}
txt = json.dumps(S, indent=1, default=float)          # serialise fully before touching the file
tmp = P + ".tmp"
open(tmp, "w").write(txt)
os.replace(tmp, P)
print(json.dumps(S["checker"]["independent_128_seed1"], indent=1))
