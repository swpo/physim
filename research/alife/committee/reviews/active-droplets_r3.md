# Review: active-droplets, sprint 3 (2026-10-24)

**Decision: STOP. The program ends; this is the thread's final record** (promise 6/10).

**Headline:** the committee's turnover protocol was built correctly in `ad9-ledger`, and its failure was reported honestly. The protocol has birth-coupled ±1-rung mutation, Moran kills by body identity and identical-event neutral twins, and it gives 0 conversions and 0 off-kind daughters in 12/12 runs. But it was run at a scale where drift decides the outcome: 6 cells and 1-5 mutations per run.
- **L7[L3] stays Weak.** The pre-registered pass fails.
- **There is a real fecundity signal in the ledgers.** The judges found it; the report did not use it. It is calibrated against the N twin and points the way the landscape predicts. But it was found post hoc and does not change population composition.
- **The shell holds under harmonic gating.** A judge rerun on a new seed shows the ψ shell and the interior optimum in kp under the harmonic face mean.
- **The landscape needs a correction.** Planted overlapping disks that separate early were counted as births.
- No thread-level rung has moved since r2: **ad7 family L6[L3] medium**, **ad5 L7[L2] low**.

## Final consensus (all sprints)

| world | final judged rung | conf. | key observation | pack | moved? |
|---|---|---|---|---|---|
| ad7-gated family (ad7t-thick, ad7-gated-d4; neutral arms ad7tn-neutral, ad7n-neutral-d4) | **L6[L3]**; L7[L3] Weak; L4c Weak | medium | **I examined the showcase sheet (ad7t-thick seed 1).** Red kp=4 founders with thick rims stay small. Green and yellow cells with thin rims divide by dumbbell (t=3700, 9100, 10900-12800, 18200-20000). Blue kp=0 cells have no rim and stay as leaky blobs. The two-coloured droplets are imposed patch relabels (the r2 contagion problem). In seed 0, lineage reaches gen 4, with 7 persistent splits and 0 merges. Gen ≥3 appears in 4/9 runs, and no birth strips were shipped. | threads/active-droplets/packs/ad7t-thick | new r2; unchanged r3 |
| ad7 single allele: landscape and the bc=0 / bu=0 ablations | **L3** (the shell does work); L4c Weak | medium | bc=0 gives 3 static blobs vs 12; bu=0 gives 12 vs 6. The r2 skeptic's radial: rim/core 4.4, rim/out 11.9. In r3, ad9 reproduces the peak under harmonic gating on 3 seeds. | threads/active-droplets/screens/ad7_landscape.png | new r2 |
| ad9-ledger landscape (single kind, harmonic gate, 3 seeds) | **L3** (numerics variant of ad7); L6 Weak in this world; L4c Weak | low | **I examined the skeptic's `psi_panels.png` and `ad9_kp05/radial.png`.** Every droplet carries a closed ψ ring at kp=0.5 and kp=2.5 (t=800-6000), including the inner face of hollowing founders. ψ rim/core is 3.02 and rim/out 14.4 (48/54 individuals). **I checked the ledgers myself.** Every birth at t≤650 is a planted overlapping disk separating. Corrected divisions by t=6000 for kp 0/0.25/0.5/1/1.5/2.5/4 are 0.33/3.67/5.67/5.67/5.33/0.67/0. kp=4 is sterile in 3/3 seeds. The 0.5-1.5 "plateau" is a ceiling set by the first round of divisions. | none shipped; threads/active-droplets/screens/ad9_landscape.png (judge pack judge-scratch/active-droplets-r3-skeptic/ad9_kp05) | new r3 |
| ad9-ledger S vs N (Moran cap=6, p=0.1 ±1 rung at birth, identical-event twins, ancestors kp=2.5 and kp=0.25 × 3 seeds) | **L7[L3] Weak** (pass not met; fecundity differential, no response) | low | **I examined `ad9_evo.png`.** S traces sit inside or at the edge of the N envelope and never enter 0.5-1.5. **I recomputed exposure-normalised births.** In S, kp=1.5 mutants give 1.34 and 1.61 births per 1e4 droplet-time, against 0.44 and 0.57 for the same labels in N and 0.77 and 0.56 for the S residents. kp=0 mutants give 0 births in 23k droplet-time in S (about 3.7 expected), against 11 in 74k in N. Uniform kills cancel the gain: in S a5 s2, kp=1.5 has 6 births and 6 kills. | threads/active-droplets/runs/S_a5_s1 (+ N/S twins); screens/ad9_evo.png | new r3 |
| ad5-evolve | **L7[L2]** | low | Mutant alleles arise, breed true and out-divide the ancestor (6+6 seeds, p≈0.001). Selection happens only during colonization, with 0 deaths. | threads/active-droplets/packs/ad5-evolve | unchanged since r1 |
| ad1-fuel | **L6[L2]**; L4c Weak | high | Ring break-up, then dumbbell fission (gen 2-4). dt/2 and dx=0.5 converge. This is Gray-Scott mitosis in a CH body: the Laplacian twin also divides. | threads/active-droplets/packs/ad1-fuel | unchanged since r1 |
| ad3-membrane / ad3s-soup | L6[L3] (inert shell) | low | A self-made ψ shell wraps every daughter. It is inert and was superseded by ad7. | threads/active-droplets/packs/ad3-membrane | unchanged since r1 |
| ad4-protocell | L3; L6 Weak | low | Two rimmed kinds that breed true, with gen ≤2. | threads/active-droplets/packs/ad4-protocell | unchanged since r1 |
| ad0-zwicker / ad6, ad6b motility | L1 / L4b not reached | high / — | Honest negatives. Dumbbells never pinch in 2D. Swimming goes at most about 1 body length, because division needs slow CH mobility and swimming needs fast mobility. | threads/active-droplets/screens/ad0_base.png | unchanged |

## Judges

**Biologist (promise 6).** No rerun. Re-analysed all 33 ad9 ledgers and found three things:
- The landscape includes planted-disk artifacts: in every run with kp>0, the early separations equal 6 − n0.
- The kp 0.5/1/1.5 counts are identical within each seed (10/10/9, 12/12/12, 13/13/13). That is a measurement ceiling, not a flat fitness plateau.
- Selection on fecundity is calibrated against N. kp=1.5 mutants made 11 births against 5.6 expected (p≈0.018), while their N label-twins made 3 against 3.5. kp=0 mutants made 0 against 3.5 (p≈0.03), while their N twins made 11 against 11.2.

The biologist credits ad9 with only L2 on its own evidence, because no frames were shipped. L7 is Weak but "closer to Supported than the report claims". At N=6, a mutant with r≈2.4 should fix about 0.59 of the time, against 0.17 for a neutral one.

**Skeptic (promise 5).** Reran ad9 at kp=0.5 and kp=2.5 on seed 11:
- The ψ shell is closed: rim/core 3.02 and 3.88, rim/out 14.4 and 16.2.
- dt/2 converges (area 448 vs 450).
- No checkerboard (Nyquist power fraction about 5e-4).
- The shell's FWHM is 1.9-2.6 px, so its width is set by the grid. dx=0.5 was not run.

The skeptic gave ad9 L3 Supported. It found the same planted-disk artifact, and also:
- an ancestor mismatch: kp=2.5 barely divides in the landscape, but makes 10-16 births at cap=6;
- unlogged merges, in which a mixed fusion silently takes an interpolated rung.

**Curator (promise 6).** No rerun. Computed the per-kind rates independently and got the same direction. Other findings:
- Harmonic averaging made the thick side much steeper (kp=2.5 was near the peak in ad7 and is nearly sterile in ad9), so gate numerics set the slope that selection has to climb.
- The null was predictable: births × pmut gives about 1-3 mutants per run.
- The sprint drifted into tooling.
- autopoiesis membrane_evo is now a second L7[L3] line.
- Novelty: no work in LITERATURE §2.4 has a heritable shell trait whose fitness emerges from the physics.

**Arbitration.**
1. **ad9 L3: I rule Supported at low confidence, siding with the skeptic.** The biologist and curator rated it Weak.
   - ad9 is the ad7 operator with a different face mean, not a new body plan. The open question was whether the harmonic change destroys the 1-2 px gate.
   - The skeptic's rerun answers that question visually, and a rerun is evidence under the rubric.
   - The source ablation (kp=0 removes the shell and stops division) spans the 3 researcher seeds plus the judge's seed.
   - Confidence is low because all ad9 imagery comes from one judge seed and the researcher shipped none.
2. **L7[L3]: Weak, unanimous.** I reproduced the fecundity numbers, so the signal is real.
   - It is still post hoc, and only 2 seeds per side are informative.
   - The rubric asks for differential persistence or growth between kinds, and the composition does not move: imposed uniform kills absorb the extra births.
   - What was shown is fecundity selection without a response.
3. **Landscape.** The corrected counts stand. The interior optimum holds and is sharper, but "broad optimum" is withdrawn. Its location and slope are not anchored at dx=0.5.

## What a future lab should do next

1. **Powered fixation test on the existing ad9 machinery** (biologist and curator; no new physics). Plant founders that do not overlap.
   - **Runs:** 20 identical-event S/N pairs per ancestor at 128², cap=6, t=30000, about 7 min per run.
   - **Pre-registered readouts:** (a) exposure-normalised births per kind against the same label in N; (b) the fate of every arising mutant, predicted at 0.59 vs 0.17 for kp=1.5; (c) the share of seeds ending in kp 0.5-1.5.
   - **Logging:** parent ids and merges.
   - **Pack:** one S run with sheet, radial and birth strips.
2. **Numerics anchor.** A dx=0.5 continuation of the landscape at kp {0.5, 1.5, 2.5, 4}, with M, κ, D and χ rescaled, comparing harmonic and arithmetic gates. This shows whether the optimum's location and thick-side slope survive refinement of the 2 px shell.
3. **Endogenous turnover, plus the cheap rungs.**
   - A maintenance cost, so that deaths come from fuel competition rather than kills.
   - A per-droplet flux budget or local fuel cut, toward L4c[L3].
   - The R arm at D=M and 2M on 3 seeds, toward the beyond-diffusion modifier.

## Cross-pollination

- **Out:**
  - **autopoiesis:** ad9's Moran kill by body identity (`worlds/ad9-ledger/world.py`) is the death operator that autopoiesis r3's future-lab item 1 asks for. ad9 also shows its caveat: at N=6, uniform kills cancel a 2-3x fecundity edge.
  - **chemotaxis-motility, flow-lenia, lenia-multichannel:** use exposure-normalised per-kind births against the identical-event label as the primary statistic in small populations, and run a power estimate first.
  - **fisim-beyond-laplacian:** the face mean changes fitness, not only the profile. Also, carrying the trait as q = a·trait on the body's own transport makes conversions impossible by construction.
- **In (record):**
  - lenia-multichannel's branch-point assay from identical states (`packs/mca-MIRd-branch`).
  - autopoiesis membrane_evo's 10 seeds × {up, twin, down} design and the cause-classified ledger (`judge-scratch/autopoiesis-r3-skeptic/scripts/evoskeptic.py`).

## Rubric issues

1. **No pack, no rung.** A world whose evidence is ledgers only (ad9: 33 runs, frames.npz deleted) cannot be credited from its own data. Evolution drivers should write a pack for ≥1 seed per arm.
2. **L7 power and statistic.** Selection tests should pre-register the expected number of mutants (births × pmut) and the Moran fixation odds. For N<10, the primary readout is per-kind exposure-normalised birth and death rates plus mutant fates against the identical-event label, not a mean-trait envelope. When nearly all deaths are imposed uniform kills, record the test as fecundity-only.
3. **Early-separation births.** Separations of planted, overlapping founders before the first relaxation (t≲1000 here) must not be counted as births in landscapes or in L6. A ledger without logged merges cannot certify "0 conversions" for mixed fusions.
