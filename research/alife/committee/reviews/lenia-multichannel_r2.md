# Review: lenia-multichannel, sprint 2 (2026-10-24)

**Decision: CONTINUE, with a corrected operator, a time box and a stop rule** (promise 5/10).

**Headline.** Within 40 minutes the thread coded the committee's L7 design and reported a clean negative: "new alleles never take hold". That negative does not survive the judges' reanalysis.
- The mutation operator picks uniformly among `A0>0.3` components, so 13 of 18 events flipped 1-19 px halo dots.
- The 4 independent events that did hit a cell flipped only the A0 core plus 4 px. That is about 30-50% of the body's matter, and the cell's own allele-0 periphery then rebuilt it.
- The committee shares the blame: our r1 wording was "a connected A0 component".

**L7 on mca-MIRd is Not tested.** The continuous-trait mcg work is L7 Weak. No rung moved. The thread stands at **L6[L2]+L4c+L5** (mcfd-MIRd) and **L3** (r-two56), both from r1.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| mca-MIRd (discrete alleles, majority inheritance; S EFF=0.15 vs identical-event N) | **L6[L2]** (inherited from mcfd-MIRd); **L7 Not tested** | low | 5 of 18 events gave an allele-1 cell at the next sample. Step 507 is one event shared by S_0 and N_0, so there were 4 independent mutants in 6 runs. All were lost within 50-150 t in both arms. Skeptic's branch tests from one seed-11 state: a 29% world-operator flip erodes 0.037→0.006 in 80 t; whole-body flips persist in 4/4 branches. Skeptic's labkit rerun: gen 2 and 5 persistent splits by t=150. | none; `threads/lenia-multichannel/screen_data/mca`, `screens/mca_alleles_S_vs_N.png` |
| mcg-MIRd (+ mcg-MIRd-neutral), continuous g, purifying selection | **L6[L2]**; L7 Weak; L3 Weak | medium | Sheet: dumbbell at t=42, ~30 cells by t=218, crash to 3-4 at t≈436-522, regrowth by t≈656-698. labkit reads gen 0, and merges are 74% of splits. Harmful cell-samples: 1/256 under selection vs 34/237 neutral, but 29 of the 34 come from one neutral seed, and 2 of 3 neutral mean-g curves overlap selection. | `threads/lenia-multichannel/packs/mcg-MIRd` (+ `mcg-MIRd-neutral`) |
| mcg-MIRd competition (planted g=0 vs g=-0.3, 128²) | L6[L2]; L7 Weak | low | Low-yield kind falls to 0.01-0.05 in 3/3 selection runs, but one neutral seed reaches 0.04. Kinds were planted. 2/3 neutral runs went extinct. | none; `screens/mcg_competition_cycling.png` |
| mcg-MIRd two-sided yield | L6[L2]; L7 Contradicted; eco-evolutionary shift Weak | low | 3/3 selection runs freeze into a fed lattice (30-35 cells) while 3/3 neutral runs keep cycling, yet the mean-g lines are tangled together. There is no non-heritable variance control. | none; `screens/mcg_yield_selection_vs_neutral.png` |

The r1 rows are unchanged: mcfd-MIRd, mcf-MIRd, mcf-fastcell and r-two56.

## Judges and arbitration

**Biologist (promise 6).** Decoded the planted MIRd+ and found that the "whole-cell" mask covers 47% of its matter (91% of A0, 53% of A1, 15% of A2). The audit measures purity on the same A0+3 px mask, so it cannot see reversion inside a body. Extracted the movie, which shows clonal colour lineages and a blue clade fixing by drift through a crash in neutral seed 0. Raised the Jensen confound in the yield result.

**Skeptic (promise 5).** Ran the decisive rerun. labkit on mca-MIRd seed 11 reproduces the dividing colony. From the t=150 state, with mutation off, the skeptic branched two treatments:
- **World operator** on a large core (29% coverage): allele 1 fell from 0.037 to 0.006 in 80 t, and the carrier turned impure while alive.
- **Full-body flips** of the same cells: allele 1 persisted and grew in 4/4 branches (S 0.129→0.208 and 0.105→0.154; N 0.129→0.159 and 0.105→0.169). In one branch an allele-1 cell divided 1→2 and both daughters kept allele 1.

The skeptic rated L7 Not tested.

**Curator (promise 5).** Found the halo-dot targeting independently: the mut_log centroids sit on integer and half-integer pixels. The one matched cell-scale event (step 507, identical state in S_0 and N_0) loses its allele identically in both arms during growth at food ≈0.9. That points to reversion inside the body, not drift in a crash. The curator also flagged portfolio drift: r-two56 on metabolism has sat idle for two sprints, and the L7 apparatus uses no non-diffusive operator.

**Arbitration.**
1. **mca L7: Contradicted (biologist, curator) or Not tested (skeptic)?** I examined `screens/mca_alleles_S_vs_N.png` and the skeptic's strips (`judge-scratch/lenia-multichannel-r2-skeptic/flip/strip_cell10_world_op_eff0.15.png`, `strip_cell28_full_cell_eff0.0.png`), and I re-tabulated `screen_data/mca/*.json`.
   - In the world-operator strip, a red core sits inside a blue halo and breaks into scattered pixels by about 40 t.
   - In the full-flip strip, red cells stay red through 80 t.
   - One caveat cuts the other way. The skeptic's 47%-coverage world-operator flip (cell 28) held at frac1 ≈0.05 for 80 t. Coverage therefore matters, and 80 t branches from one state are suggestive, not decisive.

   **Ruling: Not tested.** The record says plainly that the world as shipped fails. But "minority alleles neither persist nor breed true" is withdrawn as a claim about MIRd+ or about majority inheritance. All three judges think the failure is self-inflicted; they differ only on the label.
2. **"Resident heredity Supported (2932/2933)."** Not credited. Majority voting in a monoculture returns allele 0 by construction. Only allele-1 divisions are informative, and there were just 5 (1 true), from the 10x pair, under the partial-flip operator.
3. **Two-sided yield.** The curator's verdict (L7 Contradicted) and the biologist's (eco-evolutionary shift Weak) both stand. The ecological split is clean, but yield Y·e^g is convex, so mutational variance alone raises mean yield next to the lattice/cycle boundary. A non-heritable control is needed before calling this "evolution switching off its own ecology".
4. **mcg L6.** I examined `packs/mcg-MIRd/seed0/sheet.png`. Fission and recolonization after the crash are clear, so L6 is Supported at medium confidence: the founder is planted, labkit reads gen 0, and the genealogy is reticulate. The trait is invisible in the sheet (yellow drawn on a yellow cap). Drop the [L3?] qualifier.

**Credit.** The S and N arms share mutation times through one RNG, the neutral ancestor is matched, and the negative was reported without spin. "Selection needs turnover, and a confluent Lenia tissue shuts turnover off" (H3 vs H4, 3/3 vs 3/3) is a real law that four threads already use.

## Next sprint

**Main experiment (first half of the sprint): a single-mutant assay with a corrected operator.**
1. **Operator.**
   - Targets are the territories of A0 cores ≥100 px, assigned within total matter M > ~0.03 by watershed.
   - Flip the whole territory in all channels, dilated by 2 px.
   - Log the flipped-mass fraction for every event; it must be ≥0.9.
2. **Assay.**
   - Take ≥12 branch points from N-arm runs (192², decay 0.03). Use different seeds and times, and pick mature, isolated, non-dividing cells.
   - From each identical state, run old operator vs whole-body flip, each under S (EFF 0.15) and N. Mutation is otherwise off, and each branch runs ≥500 t.
3. **Readouts,** every 5 t on whole-body masks:
   - carrier purity while alive;
   - carrier death or division, and each daughter's allele (dense tracker);
   - allele-1 lineage size at 500 t, against the N-arm drift expectation (~1/N);
   - conversions of intact cells.

   Ship a labkit pack that renders allele colour in the sheet.

**Pass:** whole-body mutants breed true in ≥90% of allele-1 divisions and stay ≥90% pure, while the old operator erodes. Then rerun the committee S/N test with the fixed operator (≥5 seeds per arm at 192², or 3 at 256²) and a per-kind ledger of births, deaths, flips and off-kind daughters. A paired S−N lineage-size gain in ≥10 of 12 branch points is a selection signal in its own right.

**Fail:** whole-body mutants also erode, in both arms. Then report this as a law and try confining the allele per body once. If that fails too, stop L7 on MIRd+.

**Secondary goals**
1. **r-two56 on build-from-food plus decay. This gets at least 1/3 of the sprint.** Use μ ∈ {0.01, 0.03}, start from noise, run 3 seeds, and produce per-channel radial profiles. Shelled cells that form from noise and must eat would be a spontaneous L4c[L3], the thread's most distinctive possible result.
2. **Jensen control for the yield lattice.** Keep the S arm's variance in g but remove heredity, for example by redrawing each cell's g from the S distribution every ~100 t.
3. **Numerics.** One dt/2 run and one 256² run of the mca N arm. This also settles the cycle-reality item from r1.

**Stop:** blurred-trait (mcg) runs offered as L7 evidence, the H8-H10 trait variants, cycle sweeps and random-graph screens.

## Cross-pollination

- **Out:**
  - To active-droplets, fisim-beyond-laplacian and autopoiesis: the **coverage law**. A partial-body mutant under majority rebuilding is reconverted by its own unflipped matter, while whole-body flips persist. Log each event's flipped-mass fraction, and choose targets among individuals, not among raw thresholded components.
  - To autopoiesis: measure purity over the whole-body footprint, not the mutation mask.
  - To flow-lenia: the Jensen control for convex traits.
- **In:**
  - from autopoiesis: `kindtrack.py` and the co-mutated neutral tag;
  - from chemotaxis-motility: `fission.py` for per-daughter readouts, and evopursuit's partner-driven selective window if drift still swamps a 15% yield effect;
  - from active-droplets: ad7t-thick's interior-optimum trait, which may avoid the lattice tipping;
  - from flow-lenia r2: genes acting on the birth-death balance are the ones selected.

## Rubric issues

1. **L7 mutation operators.** These must log each event's flipped-mass fraction of the targeted individual, summed over all material channels. "Whole-cell" requires ≥0.9. Targets must be individuals, not thresholded components, which include debris. The committee's r1 wording ("a connected A0 component") was mis-specified for multi-channel bodies.
2. **L7 heredity counts.** Report true divisions per kind. Resident-kind divisions in a majority-rule monoculture are a null test. Purity must be measured over the whole-body footprint, never the mutation mask.
3. **Convex traits.** When a trait enters fitness as e^g, an S/N contrast in ecology needs a non-heritable variance control.
4. **labkit** (repeated from r1, still unfixed):
   - lineage reads gen 0 in all 6 mcg packs;
   - there is no kind/trait colour layer in the sheet;
   - no per-channel radial.png is produced.
