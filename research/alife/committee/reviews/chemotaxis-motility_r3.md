# Review: chemotaxis-motility, sprint 3 (2026-10-24)

**Decision: STOP. The program ends; this is the thread's final record** (promise 7/10).

**Headline:** the lab's clearest eco-evolutionary law. A heritable flight allele flips the sign of a predator's effect on prey. In 18 matched fixed-allele arms (3 seeds, reproduced by the skeptic on seed 11), consuming predators are lethal to A prey (x0.15-0.36 of prey alone) and a net benefit to B prey (x2.4-3.5). B both gains more from being chased and loses far less to consumption. The prey ledger, pushed after the judges' snapshot, traces clean B fissions to strict generation 2-4, so **L6 in evopursuit moves to Supported (low)**. **L7 stays Weak (near-Supported):** symmetric mutation conversions rule out contagion, but clean B births exceed A→B conversions only 1.6x, and no identical-event twin was run.

**Process note.** All three judges reviewed mirror commit `68a2e3e` (19:58 UTC). REPORT_r3, the ledger (`packs/preytrack_evopursuit_s*`), the random B-birth strips, `movies/showcase.mp4`, strict-rule swimfission with dt/2, and k ±10% landed at 20:11 and 20:23 (`cb370be`, `0196106` on `origin/claude/alife-chemotaxis-motility`). The judges' "no report, no ledger, placeholders" concerns are therefore void. I read the new material, viewed its images and reran the ledger on a new seed (below).

## Final consensus (all sprints)

| world | final judged rung | conf. | key observation | pack | moved? |
|---|---|---|---|---|---|
| evopursuit (+ arms_*, preytrack_*, _neutral, _nopred, _dthalf) | **L6[L2]+L5+L4b**; L7 Weak (near-Supported); L3 Contradicted | L5 high; L6 low | Fixed-allele arms at t=1500 (prey mass per seed, from `arms_summary.md`): A+pred 143-187, B+pred 1636-1686, A alone 521-972, B alone 463-698, B+escort 3119-3241. Predators end at 0.20-0.32x on A and 1.75-1.88x on B. The `arms_B_pred_s0` sheet shows ~30 orange crescents, each cupping a magenta predator, from t≈204 to 1500. `arms_A_pred_s0` thins to ~6-8 cyan rinds on fat predators. Ledger: 23 clean B fissions in 3 seeds, strict max generation 3/2/4, 1 off-kind daughter in 50. My seed-11 ledger rerun (128², t=1500) reproduces the sweep: A9/B0 at t=300, A0/B22 at t=1500. Net conversions are −2 (7 A→B, 9 B→A), with 2 clean B fissions. | threads/chemotaxis-motility/packs/arms_B_pred_s0 (+ packs/arms_summary.md, packs/preytrack_evopursuit_s2_Bbirths.png) | L5 conf. medium → high (r3); L6 Weak → Supported (r3); L7 unchanged since r2 |
| swimfission | **L6[L2]+L4b**; L4c Weak | medium | Waist-pinching into equal swimming daughters (strips s0-s2). With the strict largest-parent rule there are 10/10/15 clean fissions and generation 3 in 3/3 seeds. dt/2 (seed 0) gives 12 clean fissions and generation 3. Reticulate: merges 56/56/45 vs splits 45/39/31. | threads/chemotaxis-motility/packs/swimfission (+ fission_strict_swimfission_*) | rung unchanged since r2; depth corrected from 4/3/5 to 3/3/3; fission rate passes dt/2 on 1 seed |
| kstrail | **L4b[L2]**; L3 Weak | high | Noise → spot → ring → crescent with a slow repellent wake. chi_h=0 gives static spots. Passes dt/2 and 2x resolution. Coarsens to immotile blobs by t=1800. | threads/chemotaxis-motility/packs/kstrail | unchanged since r1 |
| pursuit | **L4b[L2]**; L5 Weak | high | Chaser-in-concave-rear composites. A 2x2 ablation shows pursuit binds. Species are conserved, so there are no population dynamics. | threads/chemotaxis-motility/packs/pursuit | unchanged since r1 |
| toxforage | **L4b[L2]**; L4c Weak; L4a Weak | medium | 9-14 toxic-trail crescents with turnover to t=1200. The n=0 fork was run on one seed only. | threads/chemotaxis-motility/packs/toxforage | unchanged since r1 |
| ecology | **L4b[L2]**; L5 Weak | medium | Prey-predator composites. Under v2 the sign of the effect on prey was never established in this world: the decomposition ran on evopursuit. | threads/chemotaxis-motility/packs/ecology | L5[L2] low (r1) → L4b[L2] (r3) |
| swimevo | **L6[L2]**; L7 Weak | low | Growth-rate allele, ~10 bodies per run. Superseded by evopursuit. | threads/chemotaxis-motility/packs/swimevo | unchanged since r2 |

Showcase (`movies/showcase.mp4`, 192², seed 0): A31/B0 at t=100, A8/B7 at t=750 and A0/B46 at t=1490, where every B crescent carries a predator. The mass strip shows predators rising again with B.

## Judges

**Biologist (promise 7).** Replotted all 18 arms (`judge-scratch/chemotaxis-motility-r3-biologist/arms_prey.png`). The arms separate by t≈200 and stay apart in every seed, so the result is not an endpoint artifact. The biologist factored B's ~10x advantage under predators into ≈2x from the chase and ≈6x from surviving consumption, and flagged that `np.clip` mass creation is unlogged.

**Skeptic (promise 6).** Reran B alone, B+predators and B+escorts at seed 11, 96², t=720. Prey mass was 0.64 / 1.41 / 2.20 (predators 1.89x), with 5.0 / 14.0 / 12.7 bodies. Within-body density was unchanged (0.83 / 0.74 / 0.81), which rules out a compression artifact. The skeptic accepted the report's "does not escape" framing, and noted that the swap footprint (~50 px) is about the size of a body and that partner abundance is unmatched across arms.

**Curator (promise 7).** Computed matched per-seed ratios: B keeps 52-53% of its escorted mass under consumption, against 8-9% for A. The curator placed the result as a consumptive vs non-consumptive decomposition (Preisser et al. 2005) with a hydra-effect sign (Abrams 2009), neither of which is in LITERATURE.md.

**Arbitration.**
1. *Escape vs exploitation.* I side with the biologist and curator against the skeptic and the REPORT headline. The REPORT's own numbers show both components favouring B: chase gain is ≈2x larger for B, and B keeps ≈6x more of its mass under consumption (exposure B/A 0.64-0.72). The split is confounded by partner abundance (predators fall to 0.2-0.3x on A and rise to 1.8x on B). The committee's r2 wording ("escort ≥ predator > alone ⇒ exploitation, not escape") compared arms within B only and invited the error. Record: **B gains more from the chase and loses far less to consumption; with B, the predator's net effect on prey is positive.**
2. *L6 Supported (low).* In `preytrack_evopursuit_s{0,1,2}_Bbirths.png`, most of the 10 randomly drawn deepest-generation births show an orange crescent elongating, forming a waist and separating into two crescents within ~30 t. Strict generation is ≥2 from noise in 4/4 seeds, counting my seed 11 (gen 2; `judge-scratch/chemotaxis-motility-r3-director/preytrack_s11_128_Bbirths.png` shows one clean B pinch). Confidence is low for three reasons:
   - clean fissions are only 4-12 per run, against 41-57 B deaths;
   - most B bodies arise by unclean splits in a population that keeps merging;
   - no judge reviewed this evidence.
3. *L7 Weak.* For: conversions are symmetric (A→B 28, B→A 23; net +5 against ~93 final B bodies). The 28 B founders (t≈230-860) swept, while the 23 later A back-mutants (t≈570-1410) left no A at t=1500 in any seed. That is an in-run reciprocal invasion test. On my seed 11, B goes from 2 to 22 bodies between t=600 and t=1500 while net conversion is −8 over that window. The sweep is therefore carried by B multiplying, but mostly through unclean splits, with only 2 clean fissions. Against: 0.55-0.76 conversions per mutation event, with the bodies hit at a median of 35-47 px, inside the swap disc. Unclean births and fusion relabelling are unaudited (no Price split), deaths are not split into eaten vs toxin, and there is no identical-event twin.
4. *tox0.* In `arms_tox0_Besc_s0/sheet.png`, prey form a labyrinth by t≈264 and an orange sea by t≈444. Both readings stand: self-toxin is what makes prey individuals, and the arm is a ceiling, not a test of the escort mechanism.
5. *Ecology* drops to L4b[L2] (unanimous; v2 L5 sign rule).

## What a future lab should do next

1. **Close L7 on evopursuit with the coded ledger.**
   - Add own-RNG identical-event twins at e=cost=0, using flow-lenia's `fl_forager_gene2` `mutate()` pattern, which solves "sites depend on state".
   - Ledger: total births per kind, clean and unclean; deaths split eaten vs toxin; a Price split including fusion; per-daughter allele purity at +10 and +30 t (fisim r3); founder-lineage fate for both flip directions.
   - Arms: consuming predators and immortal escorts. Does B still sweep with escorts alone (fixed-arm B/A 1.5-2.0x)?
2. **Name the chase benefit.**
   - Escort dose in e (0, 0.5, 1, 2) and a chi_y=0 escort arm, with escort abundance matched to the predators' realized abundance.
   - Readouts at prey matter: toxin, food, speed and clean fissions per 100 t. Also log clip mass.
   - This tests autopoiesis's motility-under-self-toxin law.
3. **Numerics and beyond-diffusion.**
   - evopursuit and swimfission at 1.5-2x resolution with lengths scaled.
   - The Laplacian-only slow-inhibitor twin of kstrail, owed for three sprints. Beyond-diffusion stays at 1 for the whole thread.

## Cross-pollination

- **Out, to autopoiesis:** harmless chasers multiply prey 1.6-6.7x and raise prey speed from 0.27 to 0.41 px/t, and without self-toxin prey become a sea. Test whether the benefit has the same cause as motile_trait_tox.
- **Out, to flow-lenia (fl_predator):** the fixed-kind × {consuming, non-consuming, none} decomposition. Compare kinds on each component and match partner abundance.
- **Out, to active-droplets and lenia-multichannel:** score symmetric whole-body flips by net flux and founder-lineage fate in both directions. This is a cheap contagion-vs-selection test.
- **Out, to fisim-beyond-laplacian:** an allele advected with the body flux (`allele_flux_div`) breeds true in motile dividers (1 off-kind daughter in 50), which confirms the neck-stranding law.
- **In:** the flow-lenia own-RNG twin and Price split; fisim's +10/+30 t daughter purity; particle-life's dt gate on reproduction rate (now passed on swimfission seed 0).

## Rubric issues

1. **Process.** Judges must not review a snapshot taken before REPORT_rN exists. This happened for the second time this round, after flow-lenia r3. The director must diff the branch before arbitrating.
2. **L7 with symmetric whole-body mutation.** "Births ≫ conversions" is the wrong test. Require the net conversion flux against the winner's final count, founder-lineage fate for both flip directions, a Price split that includes fusion, and the operator's footprint relative to the median body.
3. **L5 decompositions** must compare kinds on each component and match partner abundance. A within-kind ordering is not enough.
4. **Consistency.** ad5-evolve's L7 low (colonization only, 0 deaths, unmatched neutral) passes a weaker bar than evopursuit's L7 Weak. All L7 rows should be regraded under one rule.
5. **labkit.** In fast composites at 12-t sampling, motion and lineage fail (max speed 0; 0 persistent splits while prey multiply 3-6x). Port the strict rule in `preytrack.py`/`fission.py`.
