"""apply_checker_edits -- the independent checker's edits to round4/sbi/results/summary.json (run once).

usage: python -B apply_checker_edits.py
Each edit replaces an exact substring of a 'conclusions' entry (asserted present once) and is listed in the
'checker' block it adds. Numbers in the new text come from results/recheck_oes.json and results/recheck_ident.json
(this folder; recheck_oes.py and recheck_ident.py derive them from round4/sbi/results/job/, byte-identical to
origin/gpu-jobs:jobs/r4-sbi-002/out/), or from the cited blocks of the summary.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.join(HERE, "..", "sbi", "results", "summary.json")
S = json.load(open(SUM))
assert "checker" not in S, "edits already applied"
C = S["conclusions"]
RO = json.load(open(os.path.join(HERE, "results", "recheck_oes.json")))
RI = json.load(open(os.path.join(HERE, "results", "recheck_ident.json")))
assert RO["oes"]["net|true"] == 0.5645 and RI["per_budget"]["512"]["hpd_le_90"] == 6

EDITS = [
    (0, "contraction flattens beyond about 128 episodes (emulator misfit floor).",
     "contraction flattens beyond about 128 episodes: 128 -> 512 episodes shrinks the sd by only 0.84-0.97x "
     "(checker), because the emulator and CV-misfit covariance, which do not shrink with n, dominate the likelihood "
     "there (a floor by construction of the method; on average it is conservative at these truths: the Lab summaries' "
     "chi2 at the true theta under the data-only covariance is 49 at n = 512 against 94 expected from the misfit "
     "model)."),
    (0, "Marginal coverage is close to nominal on 8 truths (in90 0.875-1.0)",
     "Marginal coverage is close to nominal on 8 truths (in50 0.34-0.56, in90 0.875-1.0; 32 checks per budget, "
     "correlated within truths and nested across budgets)"),
    (0, "the joint 90% HPD covers 6/8 truths at n = 128 and 512 (slightly overconfident, n too small to decide).",
     "the joint 90% HPD covers 6/8 truths at n = 128 and 512; at n = 512 truth 4 (dm_00 near the box edge, "
     "u = -0.87) lies at HPD level 0.9997 (chi2 of its Lab summary at the true theta 21 under the full likelihood "
     "covariance, 4 expected), one clear miss, larger than the constant misfit term allows; 8 truths cannot measure the "
     "rate (checker). The offline check uses simulator episodes only, so it tests the inference machinery, not "
     "simulator-vs-Lab agreement."),
    (1, "even at 2 episodes. The same net on the real Lab data needs 512 episodes to come within 0.019 OES (z 5.8) and "
        "is far worse below (gap post - real 1.04 / 0.52 / 0.22 / 0.10 / 0.019 at 2 / 8 / 32 / 128 / 512 episodes).",
     "even at 2 episodes; for the ridge, 2 episodes leave 0.010 (item z 3.0, truth-cluster z 1.8, 6/8 truths) and 8 or "
     "more match. The same net on the real Lab data needs 512 episodes to come within 0.019 OES (z 5.8) and is far "
     "worse below (gap post - real 1.04 / 0.52 / 0.22 / 0.10 / 0.019 at 2 / 8 / 32 / 128 / 512 episodes; "
     "truth-cluster z 8.1 / 10.6 / 13.5 / 13.6 / 4.5, 8/8 truths each). The size of this gap is learner-specific "
     "(checker): the real@2 net trains on one episode (the other is its early-stopping hold-out); the ridge on real "
     "data reaches 0.387 at 8 and 0.458 at 32 episodes (equal to the net's real@128, 0.459) and comes within 0.006 "
     "(truth-cluster z 1.4) of its simulation-trained version at 128 episodes and level at 512 (-0.003). Simulation "
     "training beats real-data training at every budget for the net, and up to 32 episodes for the ridge. At 512 the "
     "net compares 1,024 simulated with 512 real episodes, so data source and amount are confounded."),
    (2, "identification adds 0.021 OES on top (net true - prior_pred, z 5.7; ridge 0.042, z 7.7); the box-centre "
        "plug-in loses 0.091 (net) against the truth.",
     "identification adds 0.021 OES on top (net true - prior_pred, item z 5.7, truth-cluster z 3.4, 8/8 truths; "
     "ridge 0.042, z 7.7, cluster z 5.9; amortised net 0.030, cluster z 5.2); the box-centre plug-in loses 0.091 "
     "(net; cluster z 3.3) against the truth. Box centre is worse than prior-predictive training for the net (0.070, "
     "cluster z 2.8) and the ridge (0.036, cluster z 2.3) but not for the amortised net (0.002, cluster z 1.6). The "
     "prior_mean and prior_pred nets are one trained net each, shared by all 8 truths, so no z here includes their "
     "training-seed variance (checker)."),
]
log = []
for i, old, new in EDITS:
    assert C[i].count(old) == 1, (i, old[:60])
    C[i] = C[i].replace(old, new)
    log.append({"conclusion": i, "old": old, "new": new})
C.append("Checker addition: the amortised theta-conditioned net (8,192 design episodes, 6,000 steps) beats the per-theta "
         "nets (1,024 episodes, 3,000 steps) by 0.007-0.012 OES (item z 2.2-4.2, truth-cluster z 1.3-2.9; at 32 "
         "episodes not significant); data and steps differ 8x and 2x, so this does not isolate amortisation. 46 of 50 "
         "simulation-trained nets (and the amortised net) had their best held-out loss at the last or second-to-last "
         "evaluation, so about 0.575 is not shown to be a ceiling for history-only predictors, and the remaining gap to "
         "the oracle mixes level-0 state uncertainty with predictor limits; the study shows only that the parameters "
         "account for about 0.02-0.04 of it (true - prior_pred: net 0.021, amortised 0.030, ridge 0.042). See checker.")
log.append({"conclusion": 3, "old": None, "new": "added (amortised net; not a ceiling)"})

S["checker"] = {
    "who": "independent checker of round-4 study sbi (worktree wt-sbichk), 8 Nov 2026; no GPU job run; about 5 "
           "CPU-minutes (nice 10)",
    "verdict": "the code does what the report says; every OES, gap, identification and calibration number recomputes "
               "from the saved outputs; job records match; no secret committed. The direction of every main conclusion "
               "holds with truth-clustered uncertainty. Wording overstated in places: 'beats real-data training at every "
               "budget' holds for the net, not for the ridge beyond 32 episodes; '2 episodes match the true parameters' "
               "holds for the net, not quite for the ridge; the size of post - real at small budgets is specific to a "
               "data-only net trained on 1-7 episodes; the 128 -> 512 contraction is 0.84-0.97x, not 0.8x; one truth "
               "is a clear coverage miss at 512; z values are item-level; 'remaining gap = state uncertainty' and "
               "'amortisation helps' are not isolated. Edits below",
    "job_records": {
        "r4-sbi-001": "infra_error at 00:35:23Z (datacrunch A100_80GB out of stock), billed $0 "
                      "(origin/gpu-jobs:jobs/r4-sbi-001/status.json)",
        "r4-sbi-002": "done, exit_code 0 (logs/exit.rc 0), A100-SXM4-40GB (lambdalabs asia-south-1, $1.99/h, not spot), "
                      "pod ready 00:42:20Z, terminated 02:31:58Z (1.83 h), script 1.80 h, billed $3.641, conservative "
                      "$3.811, cap $13; ref 0533b3a; 23 files collected, not truncated; backend gpu, cuda:0, jax 0.12.0.1 "
                      "(status.json, out/info.json, logs/sysinfo.txt)",
        "copies": "results/job/*.json, *.npz, progress.txt and results/status.json are byte-identical to "
                  "origin/gpu-jobs:jobs/r4-sbi-002/ (sha256 checked); run_sbi.py, sbi_lib.py, sbi_net.py, vw1/vw, "
                  "vw1/port and track2 are unchanged between the job ref 0533b3a and bd7525cbe",
    },
    "code_review": [
        "Truths: 16 box draws from the job's fresh secret through viab_joint.viability, first 8 of 14 viable; written to "
        "truths.json (PILOT_NEVER_REUSE_AS_EXAM); only the commitment of the 256-bit secret is stored.",
        "Lab (BatchLab under SEC.child('lab', i)) and exam (GExam under SEC.child('truth', i)) use separate secret "
        "children; simulator seeds (5500-based keys: 10+i true, 30/31 prior, 1000n+i post, 4402 design) do not "
        "collide; no exam trajectory enters any training set.",
        "prior_mean is the box centre (SL.CEN, u = 0); prior_pred draws theta from the viability-weighted box; each is "
        "one net (and one ridge) shared by all 8 truths.",
        "Nets keep their best held-out-episode parameters (val_frac 0.1, at least 1 episode): real@2 trains on 1 "
        "episode (94 examples), real@8 on 7; sim nets on 922 of 1,024 episodes; train_info.json best_step is 2,750 or "
        "3,000 of 3,000 for 46 of 50 simulation nets and 6,000 of 6,000 for the amortised net.",
        "Synthetic likelihood: covariance Sigma(u)/n + v(u) Sigma_mean + Bm; the last two do not shrink with n, so the "
        "contraction floor is built in. Offline calibration uses simulator episodes at held-out design points (flat "
        "box prior), so it checks the inference, not simulator-vs-Lab agreement.",
        "OES SEs are an iid bootstrap over the 512 pooled items (vw.scoring.skill_report); they ignore the 8-truth "
        "clustering and the per-truth training of each net.",
    ],
    "recomputed": {
        "scripts": "round4/sbichk/recheck_oes.py (own numpy code, not vw.scoring; 4,000 item and 4,000 two-stage "
                   "truth-cluster bootstrap draws) -> results/recheck_oes.json; round4/sbichk/recheck_ident.py "
                   "(projection, emulator and posteriors refit from design_features.npz and lab_features.npz) -> "
                   "results/recheck_ident.json; sbi/offline_calib.py re-run into scratch",
        "oes": "all 37 aggregates reproduce exactly (4 decimals); all 7 cells valid (denominator z 23-229); item-level "
               "SEs and z agree with prediction.json within bootstrap noise",
        "identification": "emulator CV chi2 3.868 (with misfit), projection R2 0.78/0.95/0.61/0.66, prior sd, "
                          "contraction ratios (to 3 decimals), in50/in90 and joint HPD counts 7,7,7,6,6 of 8 reproduce "
                          "from the float32 features",
        "offline_calibration": "re-run of offline_calib.py reproduces in50, in90 and hpd_le_90 at n = 1, 2, 4 exactly",
        "sd_shrink_128_to_512": RI["sd_shrink_128_to_512"],
        "lab_chi2_at_truth_full_cov_mean": {n: RI["per_budget"][n]["chi2_full_mean"] for n in RI["per_budget"]},
        "lab_chi2_at_truth_data_only_cov_mean": {n: RI["per_budget"][n]["chi2_dataonly_mean"] for n in RI["per_budget"]},
        "lab_chi2_data_only_expected_under_misfit_model_mean": {"2": 4.4, "8": 5.4, "32": 9.6, "128": 26.5,
                                                                "512": 94.1},
        "hpd_level_n512": RI["per_budget"]["512"]["hpd"],
    },
    "truth_clustered_gaps": {k: v for k, v in RO["gaps"].items()},
    "edits": log,
    "report_wording_not_in_summary": [
        "Headline 'beats one trained on the real Lab data at every budget': net only; ridge real >= post at 512 "
        "(-0.003) and post - real 0.006 (cluster z 1.4) at 128.",
        "'Two episodes of identification already match the true parameters': net only; ridge true - post@2 = 0.010 "
        "(cluster z 1.8, 6/8 truths).",
        "'four times the data shrinks the sd by only 0.8x': 0.84, 0.97, 0.88, 0.88 (lR, dm_00, ls_00, lh).",
        "'joint 90% region misses 2 of 8 ... mild overconfidence': at 512 one miss is far out (truth 4, HPD level "
        "0.9997); marginal in90 is 0.97-1.0, so the misses are joint, not marginal.",
        "'learning from data alone needs about 512 episodes': for this net; the ridge on 32 real episodes equals the "
        "net on 128.",
        "'Amortised net 0.574-0.575 at posterior draws': 0.5735-0.5752 (0.573-0.575 at 3 decimals); its edge over the "
        "per-theta nets is confounded with 8x data and 2x steps (cluster z 1.3-2.9).",
        "'remaining gap to the oracle is uncertainty about the state, not the parameters': only the second half is "
        "shown (parameters about 0.02-0.04); predictor limits are not separated from state uncertainty.",
        "'partly revises the round-3 finding': round 3's ridge gap (true - box centre 0.063, item z 1.3, 4 truths, "
        "4 x 60 training ticks) was underpowered; the new 0.079 (cluster z 4.3) has the same sign and size, so it "
        "resolves rather than reverses it.",
        "All z in the report are item-level; truth-cluster z are 1.2-4.6x smaller (truth_clustered_gaps); the "
        "direction of every main conclusion survives with cluster z >= 2.2 (smallest: ridge box centre vs prior "
        "predictive 2.3, 7/8 truths; ridge post - real at 2 episodes 2.9, 8/8 truths).",
    ],
    "secrets": "no secret in the study folder or the request: the only 64-hex strings are the secret commitment and "
               "bundle hashes; truths.json and summary.json carry pilot theta under PILOT_NEVER_REUSE_AS_EXAM",
}
json.dump(S, open(SUM, "w"), indent=1, default=float)
print(f"applied {len(log)} edits")
