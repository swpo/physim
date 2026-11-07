# Check of learned_phi2 (core 2, about 3 CPU-minutes)

**Verdict.** Code and numbers reproduce; the headline holds in weaker form; several secondary claims are wrong. No REPORT.md exists.

## What I did
- **Code read.** It matches the description.
- **End-to-end re-run.** Retraining LH_closG4_c1 gives bit-identical weights. Re-certifying it and tent1 matches the saved errors to 4e-7.
- **Recomputation.** My code reproduces every quoted ceiling and difference from the npz, to 0.001.
- **Isolation.** `vw` and `port` are untouched (their last edits predate this folder), so no vw tests. No figures exist.
- **New tests:**
  1. global whitening of the 16-number latents;
  2. the Prop. 6 split and I₁ with the conserved mass direction removed;
  3. the local ridge alone.
- **Files.** `check/` (scripts, `check_numbers.json`).

## Headline
- **Reported.** LH − pool1 = +0.275 ± 0.017 at τ=8; LH ties the tent (+0.001 ± 0.002).
- **Basis confound.** The per-coordinate ceiling rewards correlated coordinates, and overlapping windows are correlated. Whitened, the gains shrink:
  - tent − pool1: +0.146 ± 0.014;
  - LH − pool1: +0.135 ± 0.016;
  - tent − 4×4 box: +0.043 ± 0.017 (was +0.174).
- **E1 conditions.** The gain still exceeds 0.1, at matched content (R² 0.325 vs 0.318) and I₁ no lower (45.7 vs 42.2 nats, conserved direction removed).
- **Scope.** This is E1's level-2 analogue. The learned map only ties a designed window, so the reading is "designed Φ, audited by learning". "Best tapered Φ2" holds only among q=16 maps with at most a 4×4 support.

## Corrections (listed in summary.json meta.checker)
1. **pool3 channel correlation** is 0.93–0.99, not 0.88–0.95. "Only because" overstates it.
2. **"Local PCA within 0.03 of closure"** holds only at c=3 (−0.028). At c=1 the gap is −0.045 ± 0.006; at c=2, −0.049 ± 0.013.
3. **"The local ridge never loses"** is true by construction (GL ⊇ G).
   - Alone, it beats G on 54 of 59 latents (median +0.049).
   - It loses on all five overlapping-window latents, including tent1 and LH (−0.003 to −0.026).
4. **"Mass plus first moments (0.999)."** The 0.999 is alignment to all-channel moments (no quadrupole); to the mass moments it is 0.82.
5. **"No halo finds the 2×2 box."** The window is uniform in space, but its channel mix is about c0 + 0.7c1 − 0.24m2 (P1 alignment 0.84). It is not pool1.
6. **"GL trails LH by 0.14."** This is mostly basis: against a whitened LH the gap is −0.027 ± 0.012.
   - "GL's smooth neighbouring window" has no source. Its outputs spread over about 38 of 64 blocks, with span alignment 0.38 to the tent.
   - The GM validation-loss comparison is confounded by whitening, weight decay and step count.
7. **"Bottleneck least closed"** is false. The nonlinear autoencoders are lower: c(8) 0.010 and 0.073, against 0.19–0.24.
8. **Residual MLP.** It never helped a Φ2, but it was best for level 1 at τ=16 (+0.006).
9. **"P0's tapered window."** P0 tapered within a block and flattened to the box as τ* grew. Here the taper appears only across overlapping cells and persists at τ*=16.
10. **Wording.**
    - "Same encoder" should read "same ceiling".
    - "Not valid stacks" should read "less closed than level 1".
    - "Closure encoders" should read "local closure encoders" (GM and GL c=3 fall below level 1 at τ≤4).

## Confirmed
- **Prop. 6.** Removing the conserved direction moves γ_Y and the gap by less than 1 nat. "Mostly inherited" stands; γ_Y is a linear lower bound.
- **Level 2 more closed than level 1.** This holds but is partly a dimension effect: with the local ridge, pool3 − L1 at τ=8 falls from +0.300 to +0.162.

**Warning.** Re-running `final_summary.py` drops these edits.
