"""Apply the independent checker's edits to round4/bias/results/summary.json (claims wording + a "checker" block).

usage: python3 apply_checker_edits.py      (idempotent: refuses to run twice)
Numbers come from results/recheck.json (recheck.py) and results/pairboot.json (pairboot.py), both computed from
origin/gpu-jobs:jobs/r4-bias-003/out with own code, and from the job status files on origin/gpu-jobs.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "bias", "results", "summary.json")
S = json.load(open(P))
assert "checker" not in S, "checker edits already applied"
RC = json.load(open(os.path.join(HERE, "results", "recheck.json")))
PB = json.load(open(os.path.join(HERE, "results", "pairboot.json")))
K, H = RC["configs"], RC["hand"]
SRC_RC = "round4/biaschk/results/recheck.json"
SRC_PB = "round4/biaschk/results/pairboot.json"
r = lambda v, n=3: round(float(v), n)

EDITS = [
    (0,
     "closure and the local-law objective rediscover block mass on their own: the learned c = 1 latent and block mass predict each other with cross-validated R^2 >= 0.93 both ways, identically across seeds (seed R^2 >= 0.997).",
     "closure and the local-law objective learn a block-mass-like variable on their own: the learned c = 1 latent and block mass predict each other with cross-validated R^2 >= 0.93 both ways (0.93 / 0.94 N0 closure, 0.97 L0 closure and N0 local law, 0.995 L0 local law), identically across seeds (seed R^2 >= 0.997). Checker: at the weakest arm the agreement metric (global ridge over the 64 block values) does not single out block mass: N0 closure agrees with the designed tent at least as well (R^2 0.96 / 0.95), and block mass and the tent themselves agree at 0.94 / 0.92; N0 closure also holds less predictable content than block mass (I_avail at horizon 1 214 vs 275 nats, participation ratio 44.5 vs 54.1), so it reads as a noisy block mass rather than block mass itself; the identification is clean for L0 local law (0.995 with mass vs 0.95 / 0.93 with the tent)."),
    (1,
     "Reconstruction with the nonlinear local encoder does not: at h = 0 it learns",
     "Reconstruction with the nonlinear local encoder does not at c = 1 and small halos: at h = 0 it learns"),
    (1,
     "(first principal component of block content).",
     "(first principal component of block content). Checker: the failure is specific to c = 1 with halo 0-4 px (R^2(mass | Z) 0.24 / 0.45, seed R^2 0.08 / 0.36); with halo 8 / 16 px it is 0.79 / 0.83 (seed R^2 0.63 / 0.87), and at c = 4 the nonlinear autoencoders contain mass (R^2(mass | Z) 0.97-0.98) and are seed-stable (seed R^2 0.88-0.93)."),
    (2,
     "it agrees best with the designed tent at h = 4-8 (R^2 0.93-0.97 both ways),",
     "it agrees with the designed tent at R^2 0.93-0.97 both ways at halo 4-8 px, but so does the halo-0 latent (0.96 / 0.95) and block mass itself (0.94 / 0.92), so agreement does not single the tent out, and in content the halo latents are not the tent (halo 8 px: I_avail 193 vs 282 nats, participation ratio 22 vs 31, horizon-16 ceiling 0.38 vs 0.33; checker),"),
    (3,
     "Higher learned closure ceilings are bought by smoothing.",
     "Higher learned closure ceilings come with smoothing and with lost predictable content; the smoothing itself need not cost content: the designed tent (a smoothed block mass, also a hand design) has more I_avail / I_capt than block mass (282 / 179 nats) and a higher horizon-16 ceiling (0.33 vs 0.14), while the learned N4 / N8 closure latents have about the tent's effective dimension or less (participation ratio 30 / 22 vs 31) and 77 / 88 nats less I_avail (checker). Comparison at c = 1 and 2 only: there is no hand design at c = 4 (learned c = 4 maxima 479 I_avail, N4_recon_c4, and 225 I_capt, N8_local_c4)."),
    (4,
     "is at least as good a bias as the global closure head at every receptive field:",
     "is a better bias than the global closure head at every receptive field for horizons up to 4 (checker; not at horizon 8 for block-only encoders, see below):"),
    (4,
     "higher captured predictive information at h = 1 and equal or higher ceilings, and closer to block mass.",
     "higher captured predictive information at h = 1 (I_capt N 146 / 160 / 155 / 128 vs 121 / 115 / 111 / 92 nats, L 148 / 163 / 163 / 131 vs 124 / 121 / 112 / 89 at halo 0 / 4 / 8 / 16), higher ceilings at horizons <= 4 at every receptive field (paired trajectory bootstrap z >= 7.8), and closer to block mass. Checker: not equal or higher ceilings everywhere: for the block-only encoders the global closure head is more closed at horizon 8 (N0 -0.016, z -6.0; L0 -0.022, z -9.1), and at horizon 16 the N8 / L8 differences are within noise (z -0.7 / -1.1)."),
    (5,
     "Locality is what lets closure find mass:",
     "Locality is what lets closure find mass in this grid (checker: the U arm also differs in optimisation, 2,000 instead of 3,000 steps, weight decay 0.3, batch 256, and a global 64 x 64 whitening, so locality is not isolated; the same U encoder lands on block mass under reconstruction, R^2 0.97):"),
    (6,
     "partly mass, less closed than block mass beyond h = 2.",
     "partly mass (R^2(mass | Z) 0.74 at halo 0, 0.56 at halo 16 px), less closed than block mass at horizons 1, 2, 4 and 16 (N0_pib: -0.046 / -0.086 / -0.084 / -0.023, paired z <= -3.3) but slightly more closed at horizon 8 (0.394 vs 0.375, z 3.3; checker); N16_pib is less closed at every horizon."),
    (9,
     "nonlinear reconstruction is not (seed R^2 0.08-0.87).",
     "nonlinear reconstruction at c = 1 is not (seed R^2 0.08-0.87). Checker: at c = 2 / 4 the largest closure/local seed difference is 0.032 (N8_clos_c2, horizon 8); nonlinear reconstruction seed R^2 is 0.40-0.60 at c = 2 and 0.88-0.93 at c = 4; seed R^2 comes from latents that stayed on the pod and could not be recomputed."),
    (10,
     "pod hours 0.396 + 0.447 + 1.951 = 2.79.",
     "pod hours 0.396 + 0.447 + 1.951 = 2.79 (LEDGER column, request to termination; billed GPU-hours = billed / rate = 0.344 + 0.342 + 1.825 = 2.51; r4-bias-001 ran on an A100 80GB PCIe, datacrunch, $2.3489/h, r4-bias-002/003 on an H100 80GB PCIe, lambdalabs, $3.29/h; checker)."),
]

NEWVALS = {
    0: {"N0_clos_c1.R2_tent_from_Z": (K["N0_clos_c1"]["agreement"]["tent"]["R2_H_from_Z"], f"{SRC_RC}:configs.N0_clos_c1.agreement.tent.R2_H_from_Z"),
        "N0_clos_c1.R2_Z_from_tent": (K["N0_clos_c1"]["agreement"]["tent"]["R2_Z_from_H"], f"{SRC_RC}:configs.N0_clos_c1.agreement.tent.R2_Z_from_H"),
        "hand_mass.R2_tent_from_mass": (H["mass"]["agreement"]["tent"]["R2_H_from_Z"], f"{SRC_RC}:hand.mass.agreement.tent.R2_H_from_Z"),
        "hand_mass.R2_mass_from_tent": (H["mass"]["agreement"]["tent"]["R2_Z_from_H"], f"{SRC_RC}:hand.mass.agreement.tent.R2_Z_from_H"),
        "L0_local_c1.R2_tent_from_Z": (K["L0_local_c1"]["agreement"]["tent"]["R2_H_from_Z"], f"{SRC_RC}:configs.L0_local_c1.agreement.tent.R2_H_from_Z"),
        "L0_local_c1.R2_Z_from_tent": (K["L0_local_c1"]["agreement"]["tent"]["R2_Z_from_H"], f"{SRC_RC}:configs.L0_local_c1.agreement.tent.R2_Z_from_H"),
        "N0_clos_c1.I_avail_h1": (K["N0_clos_c1"]["I_avail"][0], f"{SRC_RC}:configs.N0_clos_c1.I_avail[0]"),
        "hand_mass.I_avail_h1": (H["mass"]["I_avail"][0], f"{SRC_RC}:hand.mass.I_avail[0]"),
        "N0_clos_c1.participation_ratio": (K["N0_clos_c1"]["participation_ratio"], f"{SRC_RC}:configs.N0_clos_c1.participation_ratio"),
        "hand_mass.participation_ratio": (H["mass"]["participation_ratio"], f"{SRC_RC}:hand.mass.participation_ratio")},
    1: {f"{c}.{k}": (K[c]["agreement"]["mass"]["R2_H_from_Z"] if k == "R2_mass_from_Z" else None, f"{SRC_RC}:configs.{c}.agreement.mass.R2_H_from_Z")
        for c in ("N4_recon_c1", "N8_recon_c1", "N16_recon_c1", "N0_recon_c4", "N4_recon_c4", "N8_recon_c4", "N16_recon_c4") for k in ("R2_mass_from_Z",)},
    2: {"hand_tent.I_avail_h1": (H["tent"]["I_avail"][0], f"{SRC_RC}:hand.tent.I_avail[0]"),
        "hand_tent.participation_ratio": (H["tent"]["participation_ratio"], f"{SRC_RC}:hand.tent.participation_ratio"),
        "hand_tent.ceiling_G_h16": (H["tent"]["ceiling_G"][4], f"{SRC_RC}:hand.tent.ceiling_G[4]"),
        "N8_clos_c1.I_avail_h1": (K["N8_clos_c1"]["I_avail"][0], f"{SRC_RC}:configs.N8_clos_c1.I_avail[0]")},
    3: {"hand_tent.I_avail_h1": (H["tent"]["I_avail"][0], f"{SRC_RC}:hand.tent.I_avail[0]"),
        "hand_tent.I_capt_h1": (H["tent"]["I_capt"][0], f"{SRC_RC}:hand.tent.I_capt[0]"),
        "N4_clos_c1.I_avail_h1": (K["N4_clos_c1"]["I_avail"][0], f"{SRC_RC}:configs.N4_clos_c1.I_avail[0]"),
        "N4_clos_c1.participation_ratio": (K["N4_clos_c1"]["participation_ratio"], f"{SRC_RC}:configs.N4_clos_c1.participation_ratio"),
        "N4_recon_c4.I_avail_h1": (K["N4_recon_c4"]["I_avail"][0], f"{SRC_RC}:configs.N4_recon_c4.I_avail[0]"),
        "N8_local_c4.I_capt_h1": (K["N8_local_c4"]["I_capt"][0], f"{SRC_RC}:configs.N8_local_c4.I_capt[0]")},
    4: {f"{e}{h}_local_minus_clos_c1": (PB[f"{e}{h}_local_c1 - {e}{h}_clos_c1"], f"{SRC_PB}:{e}{h}_local_c1 - {e}{h}_clos_c1")
        for e in "NL" for h in (0, 4, 8, 16)},
    6: {"N0_pib_minus_hand_mass": (PB["N0_pib_c1 - hand_mass"], f"{SRC_PB}:N0_pib_c1 - hand_mass")},
    9: {"N8_clos_c2.ceiling_G_seed_diff": (K["N8_clos_c2"]["ceiling_G_seed_diff"], f"{SRC_RC}:configs.N8_clos_c2.ceiling_G_seed_diff")},
}

edits_log = []
for i, old, new in EDITS:
    c = S["claims"][i]
    assert c["claim"].count(old) == 1, (i, old)
    c["claim"] = c["claim"].replace(old, new)
    edits_log.append({"claim": i, "old": old, "new": new})
for i, vals in NEWVALS.items():
    c = S["claims"][i]
    for k, (v, src) in vals.items():
        c["values"]["checker." + k] = (round(float(v), 4) if isinstance(v, (int, float)) else v)
        c["sources"]["checker." + k] = src

S["checker"] = {
    "who": "independent checker of round-4 study bias (worktree wt-biaschk), 8 Nov 2026; no GPU job run; about 2 CPU-minutes (nice 10)",
    "verdict": ("The code does what the report says; every ceiling recomputes from the saved per-item errors (max deviation "
                f"{RC['max_abs_dev_vs_combined_json']['ceiling_G']}) and every quoted I_avail / I_capt, agreement R^2 and participation "
                "ratio re-averages exactly from the per-half certification files; all 102 claim values match combined.json; job "
                "records match; no secret committed. Main direction holds: local closure / local-law encoders learn a mass-like "
                "variable, nonlinear c = 1 reconstruction does not, halos smooth, nothing learned beats the hand designs in "
                "predictable content, no bias finds objects. Wording overstated in places (edits below): 'rediscovers block mass' "
                "at R^2 0.93 is not distinguishable from the tent under this metric and carries 61 nats less content than block "
                "mass; the 8-px halo latent does not 'match the tent' in content; 'equal or higher ceilings' for the local law "
                "fails at horizon 8 for block-only encoders (paired z -6 / -9); the predictive bottleneck is more closed than block "
                "mass at horizon 8; 'smoothing costs content' is contradicted by the hand tent; reconstruction instability and the "
                "0.014 seed bound hold at c = 1 only; the U arm confounds locality with optimisation settings."),
    "job_records": {
        "r4-bias-001": "cancelled, exit_code null, A100_80GB PCIe (datacrunch FIN-01, $2.3489/h, not spot), pod ready 01:45:18Z, terminated 02:05:47Z; billed $0.8082, conservative $0.9307, cap $15 (origin/gpu-jobs:jobs/r4-bias-001/status.json)",
        "r4-bias-002": "cancelled, exit_code null, H100_80GB PCIe (lambdalabs us-west-3, $3.29/h), ready 02:18:21Z, terminated 02:38:41Z; billed $1.1261, conservative $1.4703, cap $15; progress shows CUDA_ERROR_OUT_OF_MEMORY loading 'jit_concatenate' at N4_clos_c1 (02:33:17) (status.json tails)",
        "r4-bias-003": "done, exit_code 0 (logs/exit.rc 0), NVIDIA H100 PCIe 81559 MiB (logs/sysinfo.txt), lambdalabs us-west-3 $3.29/h, ready 02:57:21Z, terminated 04:46:41Z; billed $6.0058, conservative $6.4202, cap $16; ref 25b044a54; 990 files collected, not truncated; sim backend gpu x64 jax 0.12.0.1, 708 / 739 member-ticks/s base (A / B); 80 configs, none skipped, no train or cert errors",
        "total": "billed $7.9401 (0.8082 + 1.1261 + 6.0058); billed GPU-hours 2.51; LEDGER pod hours 2.79 (from request); within the study's $25 cap",
        "copies": "results/combined.json, table.txt, sim_A.json, sim_B.json, progress.txt, train_done.json, status.json and train/*.json (80) are byte-identical to origin/gpu-jobs:jobs/r4-bias-003/; results/windows holds 104 of the 204 window files, all identical; the study code (b4, bsim, bnets, btrain, bcert, bcombine, bwin, job.sh), vw1 and learned_phi2 are unchanged between the job ref 25b044a54 and 53729c104 (only binterp.py and bsummary.py, local, were added/changed)",
    },
    "code_review": [
        "Cross-fitting is honest: each Phi is fitted (and early-stopped on the fit half's last 8 trajectories) on one designer seed and encoded with the fit half's standardisation and whitening on the other half's 32 certification trajectories; branch replicates are never used in fitting; hand designs are not fitted.",
        "Certification uses learned_phi2's fixed family unchanged (lphi.certify / combine with NJ = 32): ceiling = (V_mean - V_best) / (V_mean - V_oracle), pooled over 2 x 128 test states (64 trajectories x 4 test ticks, 5 fresh-noise branches); bootstrap SE over trajectories. Ceilings of different widths average over different numbers of coordinates.",
        "Whitening is per channel for the N and L encoders (local, so for c = 1 it is only a scale) and global (64c x 64c) for U; the closure loss is in whitened units, which favours smooth (more predictable) latents, consistent with the halo result.",
        "Agreement R^2 is a cross-validated global ridge from all 64c latent values to all 64 hand values (4 trajectory folds). It is invariant to local smoothing up to noise, which is why block mass and the tent agree at 0.92-0.94 and why it cannot separate 'block mass' from 'smoothed block mass' near that level.",
        "The rand8 baselines (untrained random 32-px linear windows) give R^2(mass | Z) 0.18 (c = 1), so mass agreement is not an artefact of any linear local window.",
        "No exam secret: vw.World(aworld specs['both'], world_seed = 0) with public parameters; designer seeds 9701 / 9702 only randomise initial states.",
    ],
    "recomputed": {
        "script": "round4/biaschk/recheck.py (own code, numpy only) on origin/gpu-jobs:jobs/r4-bias-003/out; output results/recheck.json",
        "ceilings": f"G and GL ceilings of all 166 Phi (80 configs x 2 seeds + 6 hand) recomputed from items/*.npz: max |difference| to combined.json {RC['max_abs_dev_vs_combined_json']['ceiling_G']} (float32 copies)",
        "re-averaged_only": "I_avail, I_capt, agreement R^2 and participation ratio re-averaged from cert/*.json: exact. The log-dets and R^2 themselves need the latents, which stayed on the pod, as do the seed R^2 values: not independently recomputable.",
        "claim_values": "all 102 combined.json-sourced claim values match (|diff| <= 5e-4, rounding); the seed-difference bound 0.0137 (U_clos_c1) recomputes over the 20 c = 1 closure/local configs",
        "maxima": "best learned c = 1: I_avail and I_capt L4_local_c1 265.7 / 163.2; c = 2: I_avail U_local_c2 404.5, I_capt N4_local_c2 227.2; best R^2(objmass | Z) N0_recon_c4 0.6848 vs hand mass 0.6877, chan 0.697, view 0.702",
        "windows": "cosine of the learned raw-unit window to the block-mass window, mean of 4 replicas: L0_clos 0.756, L0_local 0.937 (report 0.75 / 0.94)",
        "paired_bootstrap": "round4/biaschk/pairboot.py: local minus closure ceilings and N0_pib / N0_clos minus block mass, 400 resamples of the 64 trajectories, both configs on the same items; output results/pairboot.json",
    },
    "edits": edits_log,
    "report_wording_not_in_summary": [
        "'recovers local mass conservation': the study measures agreement with block mass, not a conservation law of the latent; read 'recovers a block-mass-like variable'.",
        "'With an 8-px halo it matches the designed tent window (R^2 0.93 / 0.97)': the halo-0 and halo-4 latents agree with the tent as well (0.96 / 0.95, 0.97 / 0.97), and the halo-8 latent has 88 nats less I_avail than the tent.",
        "'the local law is at least as good at every receptive field ... with equal or higher ceilings': not at horizon 8 for N0 / L0 (see claim 4).",
        "'Reconstruction bias gives an unstable, poorly closed variable when the encoder is nonlinear': at c = 1 and small halos only.",
        "'Stability: closure and local-law ceilings differ by at most 0.014 between seeds': at c = 1; up to 0.032 at c = 2 / 4.",
        "'Pod-hours 2.79' is the ledger column from request to termination; billed GPU-hours are 2.51. 'The two issues from r4-bias-001': the OOM first appeared in r4-bias-002 (r4-bias-001 was cancelled for slow vmapped convolution gradients).",
        "'Memory stayed flat at 7.2 GB in use, 18.8 GB peak': 7.2-7.8 GB in use, 18.8-18.9 GB peak over the configs (progress.txt).",
    ],
    "secrets": "none: public world parameters, no exam seeds or keys; results/status.json and progress.txt carry no IP (redacted '<ip>') or credentials.",
}
json.dump(S, open(P, "w"), indent=1)
print("applied", len(edits_log), "edits;", sum(len(v) for v in NEWVALS.values()), "checker values")
