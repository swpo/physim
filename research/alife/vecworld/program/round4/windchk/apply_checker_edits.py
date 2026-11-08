"""apply_checker_edits -- the independent checker's edits to round4/wind/results/summary.json (run once).

usage: python -B apply_checker_edits.py
Every edit replaces an exact substring of an interpretation field (asserted present once) and is listed in the
'checker' block it adds. Numbers in the new text come from recompute_check.json (this folder), which
recompute_check.py derives from round4/wind/results/items/*.npz, or from the cited blocks of the summary.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.join(HERE, "..", "wind", "results", "summary.json")
S = json.load(open(SUM))
assert "checker" not in S, "edits already applied"
I = S["interpretation"]

EDITS = [
    ("a_coarse_free_runs",
     "both match the wind-free headline (vw1/fresh 0.991, 0.966, 0.848, 0.495, 0.134, 0.078)",
     "M matches the wind-free headline (vw1/fresh 0.991, 0.966, 0.848, 0.495, 0.134, 0.078) at every horizon; F matches "
     "it except at h = 16, where it is higher (0.175 +- 0.012 vs 0.134 +- 0.011; separate studies, GPU vs CPU)"),
    ("a_coarse_free_runs", "SE <= 0.004 [closure.M_coarse.MW]", "SE <= 0.0042 [closure.M_coarse.MW]"),
    ("b_objects_settled",
     "so wind_recert's 'up to 0.09' is excluded and was small-sample noise (16 trajectories)",
     "so a loss of the size wind_recert left open (up to about 0.09) is excluded at full size; wind_recert's objects "
     "gaps (-0.053, -0.076, -0.054 at h = 2, 4, 8; track2/wind_recert summary closure.objects.F_minus_M) differ from the "
     "pooled estimate here by 1.2, 1.8 and 1.7 combined SE: consistent with sampling noise in its 16-trajectory sample, "
     "not shown to be noise (its layout, 16 x 236 ticks, and its predictor set also differ)"),
    ("b_objects_settled",
     "[closure.M_objects.MW, closure.M2_objects.MW]",
     "[closure.M_objects.MW, closure.M2_objects.MW]; pooled over the two pairs (checker): 0.015, 0.022, 0.034, 0.036, "
     "0.045, 0.042 V_best, SE 0.006-0.011, z 1.7 at h = 1 (not significant) and 3.2-5.6 at h = 2-32; pair 1 alone has "
     "z 3.5-5.4 at h = 1-8 and 2.1-2.5 at h = 16-32"),
    ("b_objects_settled",
     "and the best level-1 errors on the common scale are higher in F than in M by 0.04-0.09 V_best (each within 1.1 SE) "
     "[F_vs_M.objects.common_scale], so the ceiling (a ratio) does not move",
     "and in pair 1 the best level-1 errors on the common scale are higher in F than in M by 0.04-0.09 V_best (each "
     "within 1.1 SE) [F_vs_M.objects.common_scale]; pooled over both pairs that unpaired difference is -0.044 to +0.032 "
     "(SE 0.017-0.044, common-scale units) [combine.json objects_pooled_pairs.dV_best], so a rise of F's best error is "
     "not resolved beyond pair 1; the ceiling (a ratio) does not move"),
    ("c_learning_curves",
     "going from 1/2 to all fit trajectories cuts V_best by 26-36% at h = 1-8 in both F and M (not saturated); objects "
     "2-6% (close to saturation)",
     "going from 1/2 to all fit trajectories cuts V_best by 26-36% at h = 1-8 in both F and M (not saturated; but at "
     "h = 8 the curve is non-monotone, V_best at 1/2 being 27% above V_best at 1/4 in F and 26% in M, and at h = 16 "
     "V_best rises from 1/2 to all, so the reading is firm at h = 1-4 only); objects 2-6% at h = 1-16, which the "
     "study's own rule still calls not saturated (learning_curve.saturated false at h = 1-16), though the drop is small"),
    ("d_program_mix",
     "the true effect of a program on the level-1 law (CRN no-input twins) is",
     "the true effect of a program on the level-1 law (CRN no-input twins; the loss of a predictor that assumes no "
     "input: the best input-blind predictor targets the program-mixture mean and loses at most this on average, so it "
     "is an upper bound on what ignoring the inputs costs and the recovered shares below are lower bounds, as "
     "wind_recert's checker noted) is"),
    ("e_exam_z",
     "exam z for 'actions matter' with a learned level-1 predictor (best input-blind vs best input-aware, one truth per "
     "item, R = 1):",
     "exam z for 'actions matter' with a learned level-1 predictor (best input-blind vs best input-aware, one truth per "
     "item, R = 1; projected for an exam of n items from the variance components of the 324 items with the observed "
     "mean effect taken as true, not observed test statistics; observed on all 324 items with 6 truths the ES z is "
     "7.0, 3.2, 1.2 at h = 1, 2, 4 (objects), and choosing the best-by-ES predictors on half the trajectories and "
     "scoring the other half gives the same projected z64, 3.0, 1.4, 0.4, so selection does not inflate it; checker):"),
    ("e_exam_z",
     "The ideal (simulator-level) contrast is large: coarse ES z = 7.6-8.4 at 64 items (h = 1-8), objects 2.2-5.9 "
     "[P.*.energy.ideal]",
     "The ideal (simulator-level) contrast is large: coarse ES z = 7.6-8.4 at 64 items (h = 1-8), objects 2.2-5.9 "
     "[P.*.energy.ideal]; its blind ensemble is the no-input twins, not the program-mixture forecast, so these z are "
     "upper bounds for a simulator-level input-blind vs input-aware contrast"),
]
LIST_EDITS = [
    ("decides", 0,
     "objects pooled over 72 + 72 trajectories within 1.2 SE, loss < 0.04 at 95%); the objects-view question left open "
     "by wind_recert is closed: no loss",
     "objects pooled over 72 + 72 trajectories within 1.2 SE, loss < 0.04 at 95%, a bound read after the fact since no "
     "margin was declared); the objects-view question left open by wind_recert is closed: no loss larger than 0.04"),
    ("decides", 1,
     "the oracle cost of the wind is now measured precisely: coarse 0.01-0.04 V_best, objects 0.03-0.04 V_best per horizon",
     "the oracle cost of the wind is now measured: coarse 0.01-0.04 V_best per horizon (SE <= 0.0042); objects "
     "0.015-0.045 V_best pooled over the two pairs (pair 1 0.028-0.043, pair 2 0.001-0.052; pooled SE 0.006-0.011, "
     "h = 1 not significant)"),
    ("failed_or_weak", 2,
     "CRN pairs (MW, twins) therefore decorrelate after about 5 ticks;",
     "CRN pairs (MW, twins) therefore decorrelate after about 5 ticks (extrapolated from the 3-tick check at about "
     "x2,000 per tick; on the CPU the checker's rerun of check4.py without burn-in gives the CRN null and lax.map vs "
     "WindWorld exactly 0, round4/windchk/check4_cpu.json);"),
    ("next_steps", 2,
     "72-144 trajectories cost about 0.5-1 GPU-hour ($2-4) with this code",
     "72-144 trajectories cost about 0.5-1 GPU-hour ($2-4) with this code (checker: likely low at 144 trajectories; one "
     "H100-hour is $4.29 and the two coarse analyses alone took 1,302 and 1,367 s at 36 trajectories and grow with the "
     "data, so plan on 1-2 GPU-hours, about $5-9)"),
]

log = []
for field, old, new in EDITS:
    assert I[field].count(old) == 1, (field, old)
    I[field] = I[field].replace(old, new)
    log.append({"field": f"interpretation.{field}", "old": old, "new": new})
for field, k, old, new in LIST_EDITS:
    assert I[field][k].count(old) == 1, (field, k, old)
    I[field][k] = I[field][k].replace(old, new)
    log.append({"field": f"interpretation.{field}[{k}]", "old": old, "new": new})

S["checker"] = {
    "who": "independent checker of round-4 study wind (worktree wt-windchk), 8 Nov 2026; no GPU job run",
    "verdict": "the code does what the report says and every headline number recomputes from the saved per-item outputs; "
               "the job record matches the report; the certificate conclusions follow. Wording was overstated in places "
               "(wind_recert's gap 'was noise', the objects oracle cost 'precisely 0.03-0.04', objects learning curve "
               "'close to saturation', the projected exam z read as test results, the ideal contrast and 'true effect' "
               "not flagged as upper bounds, F 'matches' the fresh headline at h = 16); edits below",
    "job_records": {
        "r4-wind-001": "rejected at 00:33:06Z (H100 offer at $4.29/h needs $11.80 for max_hours 2.5 + 0.25 h, cap $10); "
                       "billed $0 (origin/gpu-jobs:jobs/r4-wind-001/status.json)",
        "r4-wind-002": "done, exit_code 0, H100_80GB (lambdalabs us-south-2, $4.29/h, not spot), pod created 00:36:24Z, "
                       "terminated 01:07:06Z (0.512 h); run 00:41:36Z-01:07:27Z (0.431 h); billed $1.8562 (0.433 "
                       "H100-hours), conservative $2.2138, cap $12; ref c39d9bd77; 45 files collected, not truncated "
                       "(origin/gpu-jobs:jobs/r4-wind-002/status.json). check4 exited 1 (non-fatal, by design of job.sh) "
                       "because the GPU is not deterministic (crn_null_L1_maxabs 1.2e-7, lax.map vs WindWorld 6.1e-13 "
                       "at tick 1); the vmap-vs-WindWorld bound < 1e-6 held (2.9e-7 at tick 3)",
        "copies": "all 35 files in results/ (JSON, logs, items/*.npz) and results/status.json are byte-identical to "
                  "origin/gpu-jobs:jobs/r4-wind-002/out/ and status.json",
    },
    "recomputed": {
        "script": "research/alife/vecworld/program/round4/windchk/recompute_check.py (own code, numpy only, 2,000 "
                  "trajectory-bootstrap resamples, other seeds) -> recompute_check.json; about 2 CPU-minutes",
        "ceilings": "F/M coarse, F/M/F2/M2 objects from items err/orac: max |diff| to the JSON 8e-9 at every horizon; "
                    "bootstrap SEs agree within resampling noise (e.g. F coarse h = 4 0.0037 vs 0.0033)",
        "F_minus_M": "coarse d identical, |z| <= 1.93 (JSON 1.90); objects pooled d identical, SE 0.014-0.020, "
                     "one-sided 95% loss bound 0.014, 0.025, 0.008, 0.032, 0.036, 0.032 (JSON 0.014, 0.024, 0.009, "
                     "0.033, 0.038, 0.033): <= 0.04 either way",
        "MW": "coarse 0.0436, 0.0248, 0.0124, 0.0101, 0.0165, 0.0342 V_best identical; objects pair 1 0.028-0.043 "
              "(z 2.2-5.4), pair 2 0.001-0.052 (z 0.06-3.9), pooled 0.0147, 0.0224, 0.0335, 0.0363, 0.0453, 0.0422 "
              "(SE 0.0088, 0.0069, 0.0068, 0.0065, 0.0112, 0.0107); the two pairs agree (|z| <= 1.6)",
        "learning_curve": "rel_drop_half_to_all identical in all four blocks; rel_drop_quarter_to_half coarse h = 8 "
                          "-0.265 (F), -0.259 (M): non-monotone",
        "P": "true effect (programs) coarse 0.197, 0.218, 0.204, 0.092, 0.080, objects 0.079, 0.079, 0.095, 0.058, "
             "0.104 identical; recovered shares identical (patchnet+u -0.166 to -0.705; ridge_p2+u2 coarse 0.118, "
             "0.134, 0.177, 0.077; slotnet+u 0.440, 0.178, 0.057); ridge_p2+u2 / patchnet error ratio 1.240, 1.263, "
             "1.265, 1.250 at h = 1-8; ES z (best blind -> best aware) objects 3.00 / 4.25 at 64 / 128 items, "
             "aimed+regional 3.96 / 5.61 at 32 / 64, h = 2: 1.34 / 1.90 and 1.41 / 1.99; ideal ES z64 coarse 7.57, "
             "8.10, 8.40, 7.61, 6.03, objects 5.92-2.21: all identical",
        "selection_check_P": "best-by-ES predictors chosen on half the trajectories, z64 on the other half (200 splits): "
                             "3.02, 1.39, 0.41 at h = 1, 2, 4 vs in-sample 3.00, 1.34, 0.52",
    },
    "cpu_rerun": "check4.py without --burn on this container's CPU (jax CPU, x64, 22 s; "
                 "research/alife/vecworld/program/round4/windchk/check4_cpu.json): lax.map vs WindWorld 0 at every tick, "
                 "CRN null 0, vmap vs WindWorld 5.7e-14 at tick 1 and 8.8e-12 at tick 3 (check ok): the "
                 "non-determinism is a GPU property",
    "design_notes": [
        "F and M share keys but are burned in at their own sigma_w, so they are effectively independent draws; the "
        "paired bootstrap is still valid, and MW is the properly paired measure of the wind's cost",
        "no declaration was written before the run (unlike wind_recert); the 'certificate holds' criterion (|z| < 2, "
        "one-sided bound < 0.04) is applied after the fact; with every |z| <= 1.9 there is no multiple-comparison issue "
        "for the null result, the question is only the size of the excluded loss",
        "per-item CRN effects stay unbiased under GPU decorrelation (the estimator subtracts the within-item variance "
        "of the 3 twin pairs); the unpaired effect assumes independent replicates and is biased low when twins share "
        "keys, which is why the CRN version is the headline",
        "process: 0e37cb9f0..11f0953d0 differs only by the round4/wind files and requests/r4-wind-001.json, so the "
        "restore of the rollout_kit and round4/sbi files is exact; no commit since 0e37cb9f0 touches vw1/ (vw, port), "
        "integrate/, track2/actuation or track2/wind_recert",
        "secrets: none; the world is the public gliders parameters (WindWorld defaults); the 'theta' keys in "
        "results/sim_P.json are blind-program wind directions (wr.build_program), not hidden parameters",
    ],
    "edits": log,
    "report_wording_not_in_summary": [
        "'the learned level-1 predictors pick up none of the inputs' effect in the block view': true of the nets and of "
        "the best predictor; the linear ridge_p2+u2 recovers 12-18% at h <= 4 relative to its own, 24-26% weaker base",
        "'MW measures 0.03-0.04 V_best, z about 3-5' (objects): pair 1 only; its z is 2.1-5.4; pair 2 gives "
        "0.001-0.052; pooled 0.015-0.045, z 1.7-5.6",
        "'the up to 0.09 object-view loss in wind_recert was noise': consistent with noise (gaps 1.2-1.8 combined SE "
        "from the full-size estimate), not shown to be noise",
        "'Exam z ... 3.0 at 64 items and 4.2 at 128': projected z for an exam of that size, not observed",
        "'A simulator-level predictor would see the inputs clearly: z 7.6-8.4': at h = 1-8 and against the no-input "
        "twins, an upper bound",
        "GPU-hours: 0.433 billed H100-hours (billed $1.8562 / $4.29), 0.512 pod-hours",
    ],
    "note_on_regeneration": "round4/wind/interpretation.json and README.md keep the pre-check wording; rerunning "
                            "make_summary4.py drops this block and the edits (reapply with "
                            "round4/windchk/apply_checker_edits.py)",
}
json.dump(S, open(SUM, "w"), indent=1)
print("applied", len(log), "edits to", SUM)
