# Review: lenia-multichannel, sprint 3 (2026-10-24)

**Decision: STOP. The program ends; this is the thread's final record** (promise 4/10).

**Headline:** the committee's branch-point assay was run cleanly and reported straight.
- **Coverage law confirmed.** From identical states, whole-body flips are lost in 1/12 arm-runs and partial flips in 9/12.
- **Real differential growth.** A 15%-yield allele outgrows its neutral twin in 10/10 informative pairs. Under S it has fewer deaths per division than the resident (0.30-0.43 vs 0.63-0.78), while the N arm is matched.
- **Kinds do not breed true.** Only 47% of allele-1 divisions give two pure daughters. Living cells change kind 7-15 times per S run against 1 mutation event, and the variation was imposed.

**mca-MIRd: L6[L2], L7 Weak** (moved up from Not tested). r-two56 still forms shelled cells from noise on a build-from-food metabolism (**rf-two56-mu0.01: L3**, new), but L4c[L3] was never tested. No thread-level rung has moved since r1.

## Final consensus (all sprints)

| world | final judged rung | conf. | key observation | pack | moved? |
|---|---|---|---|---|---|
| mcf-MIRd | **L6[L2]+L4c**; L5, L3 Weak | high | Planted MIRd+ with build-from-food: 6 persistent splits, gen 3 (seeds 0, 2). Norefill is extinct in 3/3, against 11-16 survivors with refill. The replication itself is Chan's. | threads/lenia-multichannel/packs/mcf-MIRd | unchanged since r1 |
| mcfd-MIRd | **L6[L2]+L4c+L5**; L3 Weak | medium | Adds decay 0.03, which gives boom-bust with fission after troughs (dense rerun: 4→17 cells). Decay 0/0.01/0.03 gives dormant/static/boom-bust. Not a regular cycle; dt/2 went extinct in 1/2 seeds. Showcase frames (t=240/720/1320; 15/12/9 cells): core, cap and dotted halo on dark, eaten food. | threads/lenia-multichannel/packs/mcfd-MIRd; movies/showcase.mp4 | unchanged since r1 |
| mca-MIRd (whole-body branch test) | **L6[L2]; L7 Weak** | medium (L6) | 12 identical-state S/N pairs from 2 neutral runs. S>N in 10/10 informative pairs; the 2 smallest starts (0.012, 0.014) were lost in both arms. S ends at 0.40-0.72 with 8-22 pure allele-1 cells, N at 0-0.56 with 0-8. Ledger: net conversions 1-3 against net allele-1 births 36-55. Fails the bar: 47% pure divisions, gross conversions ≫ mutations, imposed variation, isolated founders only, ledger not merge-aware, labkit gen ≤1. | threads/lenia-multichannel/packs/mca-MIRd-branch | L7 Not tested (r2) → Weak (r3) |
| mca-MIRd old operator (A0 + 4 px) | coverage law Supported (mechanism); partial-flip L7 Contradicted | medium | On the same 6 states, partial flips (0.50-0.79 coverage) are lost in 9/12 arm-runs against 1/12 for whole-body flips; whole ≥ old in 11/12. All 6 states come from one run. | none; threads/lenia-multichannel/screens/branch_test.png | new in r3 |
| mcg-MIRd (+ neutral) | **L6[L2]**; L7 Weak (two-sided yield: Contradicted) | medium | Continuous trait, which blends at contacts. Two-sided yield freezes 3/3 into a lattice, with no Jensen control. | threads/lenia-multichannel/packs/mcg-MIRd | unchanged since r2 |
| mcf-fastcell | **L4b[L3]+L4c** | medium | Planted Chan shelled gliders (A0 shell r 14-22, empty inside) travel 8-15 BL and carve food wakes. Norefill leaves 0/0/1 survivors. | threads/lenia-multichannel/packs/mcf-fastcell | unchanged since r1 |
| r-two56 | **L3**; L4a Contradicted | high | 2/420 random rules. Cog cells form from noise in 6 seeds and survive dt/2 and R=15/20. Static, with no turnover. | threads/lenia-multichannel/packs/r-two56 | unchanged since r1 |
| rf-two56-mu0.01 | **L3**; L2 Supported; L4c Not tested | medium | Cells form from noise in 4/4 seeds (3 researcher seeds plus skeptic seed 11). Skeptic radial: A0 ≈1 to ρ 0.55; A1 ≈0 at ρ 0.25-0.55 and ≈0.9 at ρ 0.75-1.0 (rim/out 78). Survivors are static in shallow food wells (F ≈0.7 at the centre vs 0.9 at 2.5 R). Decay 0.03 leaves ≤1 cell. | none; threads/lenia-multichannel/screens/rf-two56_food_decay.png (judge pack judge-scratch/lenia-multichannel-r3-skeptic/rf-two56-mu0.01) | new in r3 |
| r-two-s1-60 | L4b[L2] | medium | Known single-channel C-glider class; the second channel is dead. | threads/lenia-multichannel/packs/r-two-s1-60 | unchanged since r1 |
| eco-MIRd-Rplus | L6[L2]; L5 Weak | low | Two replicators coexist; the exclusion term is imposed. | threads/lenia-multichannel/packs/eco-MIRd-Rplus | unchanged since r1 (paused) |

## Judges

**Biologist (promise 5; L6[L2], L7 Weak).** The seed-0 sheet shows clonal spread as discrete dividing bodies, not a smear, and chimeras at contact fronts. The biologist found that the S arm raises the population (27.5 vs 18.1 cells) and that allele 0 falls at only 7/10 points. The founder sits in a food trough at an expanding front, so allele surfing is a candidate, and it explains the N=0.56 outlier. The opaque allele overlay hides whether allele-1 daughters keep the core/cap/halo body plan.

**Skeptic (promise 4; L7 Weak).** Ran two reruns.
- **rf-two56** on a new seed: the cells form, and the radial confirms the A1 annulus.
- **Matched S/N pair from a contact founder** (1-px gap, coverage 1.0, start 0.052): the allele was lost in both arms within about 75 t.

Raised three further points:
- Gross conversions (0→1: 4/7/8 per S run) against 1 mutation is contagion.
- Inheritance and phenotype use a σ=3 px neighbourhood majority that is not scaled with R.
- The 12 points are pseudo-replicates from 2 runs.

**Curator (promise 4; L7 Weak).** Extracted per-kind deaths from the ledger, which shows that the advantage runs through births and deaths. Flagged that 1.15× yield at decay 0.03 puts the effective decay/Y at ≈0.026, on the static side of the thread's own threshold. Also flagged that r-two56 was under-delivered for the third sprint, and that the coded per-body retry went unreported.

**Arbitration.**
1. *Contagion or births?* I re-tabulated `screen_data/ledger/*.json`.
   - Under S, conversions run both ways (0→1: 4/7/8; 1→0: 3/4/7), so the net is +1/+3/+1. Net allele-1 births (divisions − deaths) are +36/+43/+55, against +7/+11/+6 under N.
   - **Ruling:** the sweep is not carried by conversion (curator). But 7-15 kind changes of living cells per run against 1 mutation breaks "kinds change only at mutation or birth" (skeptic). Together with 47% pure daughters, L7 stays Weak.
   - Absolute division counts are inflated by fission-fusion flicker: allele 0 logs 133 divisions and 83 deaths in about 18 cells. Within-arm ratios are still comparable.
2. *Selection or range expansion?* I examined `packs/mca-MIRd-branch/seed0/sheet.png` and `screens/branch_test.png`.
   - The pale colony grows from the single bottom-left cell at t=0 as separate round bodies.
   - By t=350-500 it sets into a near-hexagonal lattice, and only a few orange-capped allele-0 cells keep moving.
   - **Ruling:** the differential growth is real, but the assay measures establishment of isolated founders at a front. One contact founder failed in both arms. The result does not generalize beyond isolated founders.
3. *Self-dormancy.* The selected allele drives its carriers into the fed-static lattice. This is the second instance, after the r2 two-sided yield runs (3/3). We record it as a candidate eco-evolutionary law at Weak: there is no Jensen control and the windows are 500 t.
4. *B5 (per-body confinement).* `NOTEBOOK.md` B5 ends at "Ledger rerun on the same 3 points × S/N" and has no output. `worlds/mca-MIRd-body/world.py` exists. The stop rule's decisive retry is therefore **unreported**, and the L7 line ends at Weak, not at a clean negative.
5. *rf-two56 L3.* labkit's band test fails (A1 rim/core 1.24) because of a central A1 dot. The skeptic's `radial.png` shows a clean annulus with A1 ≈0 between the dot and the shell. L3 stands on that profile plus the r1 kernel ablations, at medium confidence: one unlabelled screen, and no resolution check on the fed variant. The radial F profile shows that survivors keep a shallow well, so they do eat, but dependence on food was never tested.

## What a future lab should do next

1. **rf-two56 food-limited fork (curator's design).**
   - Set decay to 0.015-0.02 and limit the food (ρ 0.005, D 0.5), so that formed cogs sit in wells with F < 0.8.
   - At t=300, branch three arms: a fed twin, a local supply cut around one isolated cog, and global refill off.
   - Pass: the cut cell dies or loses its shell while its twin and neighbours persist, on ≥2/3 seeds. That would be a spontaneous L4c[L3] in a kernel world.
   - Add a matched Laplacian/DoG control for the set-point membrane. This is the thread's only route to a beyond-diffusion score.
2. **Finish B5 (`worlds/mca-MIRd-body`).**
   - Run per-body inheritance and phenotype from the 12 branch states plus ≥6 contact founders.
   - Use a merge-aware ledger: daughters must stay separate for ≥50 t and reach ≥50% of parent mass. Report gross and net conversions per mutation.
   - Render a two-panel sheet for each arm (raw channels | allele outline).
   - Pass: ≥90% pure divisions, conversions ≤ mutations, and S>N in ≥10/12. Then run mutation arising in the run, with autopoiesis membrane_evo's identical-event twin, ≥5 seeds per arm and one dt/2 arm. Otherwise stop L7 on MIRd+.
3. **Self-dormancy law.**
   - Run fixed-allele cultures across μ/Y 0.02-0.035, together with a Jensen control and crowding-dependent decay.
   - Question to settle: does selection on yield drive the population across its own turnover threshold?

## Cross-pollination

- **Out:**
  - *flow-lenia, active-droplets, particle-life.* The paired identical-state branch assay is a cheap, high-power selection test. Use per-kind deaths/divisions as the readout, report establishment against founder size, and include contact founders.
  - *autopoiesis, flow-lenia, particle-life.* Check self-dormancy: does the selected kind lower turnover?
  - *all L7 threads.* Report gross and net conversions.
- **In (record):**
  - autopoiesis: the sealed channel, identical-event twin and evotrack;
  - chemotaxis-motility r3: the fixed-allele decomposition, which separates carrying capacity from replacement;
  - fisim r3: coverage at the pinch, not only at mutation.

## Rubric issues

1. **L7 conversions.** Report gross conversions in both directions and the net, per mutation event. A sweep is contagion when the net conversions carry a material share of the kind's gain. Gross conversions above the number of mutations still fail "breeds true".
2. **L7 founders.** In branch assays, founders must be random or include contact cells. Isolation-selected founders sit on expanding fronts (surfing), so they cap confidence at low.
3. **Kind overlays.** Must not hide the body plan: use an outline or a side panel, and ship both arms.
4. **labkit.**
   - The radial band test fails a clean annulus that has a central dot (rf-two56 A1 1.24) and passes a one-sided cap (MIRd+ A1 2.03). Use bands at the profile trough and add an anisotropy check.
   - Lineage still reads gen 0-1 on dividing colonies.
5. **Report hygiene.** A committee-assigned retry must have an outcome or a "not run" line in the report.
