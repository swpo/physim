"""Checker edits to results/summary.json (run once, after check.py). Adds checker notes and new checker.* claims;
changes no existing value except where listed in meta.checker.edits. Re-running summarize.py + final_summary.py would
overwrite these edits."""
import json

OUT = "/home/user/evalwork/vecworld/program/track1/learned_phi2"
S = json.load(open(f"{OUT}/results/summary.json"))
K = json.load(open(f"{OUT}/check/check_numbers.json"))
A, B, C, D, E = K["A_recompute"], K["B_inspect"], K["C_end_to_end"], K["D_global_whitening"], K["E_conserved_projected"]
CK = f"{OUT}/check/check_numbers.json"
edits = []
byid = {c["id"]: c for c in S["claims"]}


def note(cid, text):
    byid[cid]["checker_note"] = text
    edits.append(f"{cid}: added checker_note")


def add(cid, statement, value, source, se=None):
    S["claims"].append({"id": cid, "statement": statement, "value": value, "se": se, "source": source})
    edits.append(f"{cid}: new claim")


# 1. tautological local-ridge claim
c = byid["local_predictor_gain_tau8"]
c["statement"] = ("c_GL(8) - c_G(8) per grid latent. GL = G + lridge, so this is >= 0 BY CONSTRUCTION and n_negative = 0 "
                  "says nothing about locality; see checker.local_ridge_alone_vs_G_tau8 for the local ridge alone")
edits.append("local_predictor_gain_tau8: statement reworded (non-negative by construction)")
add("checker.local_ridge_alone_vs_G_tau8", "c_L(8) - c_G(8): the fixed local ridge ALONE against the global family G, "
    "per grid latent (recomputed from results/cert/*__cert[AB].npz)", A["local_ridge_alone_vs_G_tau8"], CK)

# 2. alignment wording
note("alignment.LL_closG4_c3", "0.999 is the alignment to Pmom9 (zeroth + first moments of ALL three channels, a 9-dim "
     "subspace whose complement is the 3 quadrupole directions; a random 3-dim window expects 0.75, rand_s3_0 gives 0.68). "
     "Alignment to the total-mass moments Pmm3 is 0.82, so 'block mass plus its first spatial moments (alignment 0.999)' "
     "overstates it: the window has no quadrupole part and mixes the moments of all channels")
note("alignment.LL_closG4_c1", "P3 = 0.999 means a spatially uniform 2 x 2 window; its channel mix is not pool1's total mass "
     "(P1 = 0.84)")

# 3. Prop. 6 split: checked against the conserved direction (it survives)
for nm in ("pool3", "tent1", "LH_closG4_c1", "pool1"):
    if f"prop6.{nm}" in byid:
        note(f"prop6.{nm}", "checker: projecting out the exactly conserved total-mass direction changes gammaY, inherit and "
             f"gapX_r2 by < 1 nat (checker.prop6_projected.{nm}), so the split is not an artefact of that direction; it "
             "does move I_capt(1) by about 14 nats for pool1 and tent1. gammaY is a ridge (linear, finite-data) lower bound")
    add(f"checker.prop6_projected.{nm}", "Gaussian log-det measures and c_G with the total-mass direction (sum over cells of "
        "c0 + c1; the uniform cell direction for LH) projected out; nats per horizon 1..16, mean of the two halves", E[nm], CK)
add("checker.I1_projected", "I_capt(1) in nats with the conserved direction projected out (Gaussian proxy for E1's I_1 "
    "matching condition): tent1, LH_closG4_c1, pool1, pool3",
    {nm: E[nm]["logdet_projected"]["I_capt"][0] for nm in ("tent1", "LH_closG4_c1", "pool1", "pool3")}, CK)

# 4. claims the report makes that summary.json lacked
add("checker.pool3_channel_correlation", "correlation of the pooled channels (c0, c1, m2) of pool3 over all frames and cells "
    "(pooled) and the range over the 16 cells; the report says 0.88-0.95 without a saved source",
    {"pooled": B["pool3_channel_corr_pooled"], "per_cell_range": B["pool3_channel_corr_per_cell_range"]}, CK)
add("checker.lpca_minus_closure_tau_all", "c(lpca c) - c(LL_closG4 c), paired bootstrap over 36 trajectories (1000), "
    "family G; the report says local PCA 'lands within 0.03 of closure'",
    {k: A["diff"][k] for k in ("lpca1-LL_closG4_c1", "lpca2-LL_closG4_c2", "lpca3-LL_closG4_c3")}, CK)
add("checker.closure_minus_recon_LL_c1", "c(LL_closG4_c1) - c(LL_recon_c1), family G (the report's +0.048 +- 0.007)",
    A["diff"]["LL_closG4_c1-LL_recon_c1"], CK)
add("checker.rmlp_best_anywhere", "where the residual MLP was the best predictor in family G+rmlp (12 Phi2 incl. level 1)",
    {"L1": "tau 16 only: c 0.011 -> 0.017", "all other 11 Phi2": "never"}, f"{OUT}/results/cert/*_rmlp.json")
add("checker.GL_closG4_c1_window", "spatial spread of the GL c=1 encoder outputs before whitening: effective number of "
    "level-1 blocks per output (2x2 box = 4, tent = 8.7) and share of power inside the best 4x4 window",
    {k: v for k, v in B.items() if k.startswith("GL_")}, CK)

# 5. end-to-end re-run and the basis check
add("checker.end_to_end_rerun", "LH_closG4_c1 retrained from scratch on both halves (seed 0, 5000 steps) and re-certified; "
    "tent1 re-certified; max relative deviation of per-item errors from the saved npz", C, CK)
D["GL_vs_whitened"] = {k: v for k, v in K["X_extra"].items() if k.startswith("GL_closG4_c1-")}
add("checker.global_whitening", "c_G after whitening the 16-number latent globally (fit on the other half; rank-reduced for "
    "box4_1), i.e. the span compared in a decorrelated basis as GL_closG4_c1 is; paired differences with bootstrap SE", D, CK)
note("diff.GL_closG4_c1-LH_closG4_c1.G", "confounded: GL's latent is certified in a globally whitened basis, LH's in a "
     "spatially correlated one; compare checker.global_whitening (LH whitened) before reading this as locality")
for cid in ("diff.tent1-pool1.G", "diff.LH_closG4_c1-pool1.G", "diff.tent1-box4_1.G"):
    note(cid, "the per-coordinate ceiling rewards correlated coordinates, and overlapping windows are more correlated than "
         "disjoint boxes; in a globally whitened basis the tau = 8 difference is smaller (checker.global_whitening: "
         "tent1 - pool1 +0.146 +- 0.014, LH - pool1 +0.135 +- 0.016, tent1 - box4_1 +0.043 +- 0.017)")
add("checker.local_ridge_alone_loses_tau8", "grid latents where the local ridge alone is below family G at tau = 8",
    K["X_extra"]["local_ridge_alone_loses_tau8"], CK)
add("checker.GL_span_alignment", "span alignment (weight space, standardised level-1 coordinates) of GL_closG4_c1's 16 "
    "outputs to the tent1, pool1 and LH spans (tent1 vs pool1 for scale)", K["X_extra"]["span_alignment_GL"], CK)
note("closure_val_loss_c3", "not comparable across rows: GM and GL whiten all 48 numbers jointly, LL and LM only the 3 "
     "channels per cell (cells may stay correlated), and GM also has weight decay 1.0 and 2000 steps against LL's 5000")

REPORT_FIX = [
    "'pool3 channels 0.88-0.95 correlated' -> 0.93-0.99 (c0-c1 0.94, c0-m2 0.97, c1-m2 0.99); 'only because' -> the ceiling is basis dependent",
    "'local PCA lands within 0.03 of closure' -> only at c = 3 (-0.028 +- 0.003); c = 1: -0.045 +- 0.006, c = 2: -0.049 +- 0.013",
    "'the fixed local ridge never loses to the global family (0 to +0.18)' -> tautological (GL contains G); the local ridge alone beats G on 54 of 59 latents (median +0.049) and loses on the 5 overlapping-window latents (-0.003 to -0.026)",
    "'closure picks the block mass plus its first spatial moments (alignment 0.999)' -> 0.999 is to the moments of all three channels (no quadrupole); to the mass moments it is 0.82",
    "'with no halo it finds the 2 x 2 box' -> a spatially uniform 2 x 2 window, channel mix about c0 + 0.7 c1 - 0.24 m2 (P1 alignment 0.84), not pool1",
    "'the prediction bottleneck gives the least closed learned levels' -> false: the nonlinear local autoencoders are lower (c(8) 0.010 / 0.073 vs 0.19-0.24)",
    "'the residual MLP never improved on the linear family' -> never for a Phi2; it was best for level 1 at tau 16 (0.011 -> 0.017)",
    "'GL trails LH by 0.14' / 'unconstrained encoders lose' -> mostly a basis artefact: against globally whitened LH, GL is -0.027 +- 0.012 at tau 8; 'GL picks a smooth window spanning neighbouring cells' has no source (outputs spread over ~38 of 64 blocks, span alignment to tent 0.38)",
    "'beats the box by +0.275 ... clears E1's bar' -> +0.275 in the per-coordinate basis; +0.146 +- 0.014 (tent) / +0.135 +- 0.016 (LH) in a whitened basis, still above 0.1; I_1 not lower (45.3 / 45.7 vs 42.2 nats, conserved direction removed); this is the level-2 analogue of E1 and the learned Phi2 only ties a designed window",
    "'This is P0's tapered window' -> different phenomenon: P0 tapered within a disjoint block and flattened to the block sum as tau* grew; here no-halo encoders find a uniform box at every tau* and the taper appears only across overlapping cells",
    "'gives the same encoder' (local vs global head) -> the same ceiling (|dc| <= 0.012)",
    "'do not make valid stacks' -> Prop. 6 holds for any Phi2; they give a level less closed than level 1. GM / GL closure c = 3 are also below level 1 at tau <= 4, so 'pooling and closure encoders' -> 'pooling and local closure encoders'",
]
S["meta"]["checker"] = {
    "who": "independent checker, core 2", "files": [CK, f"{OUT}/check/check.py", f"{OUT}/check/apply_edits.py",
                                                    f"{OUT}/results/check.md"],
    "cpu_s": round(K["cpu_seconds_total"] + K["cpu_seconds_total_extra"] + 70, 0),
    "edits": edits, "report_corrections": REPORT_FIX,
    "warning": "re-running summarize.py and final_summary.py regenerates summary.json and drops these edits"}
json.dump(S, open(f"{OUT}/results/summary.json", "w"), indent=1)
print(len(edits), "edits")
