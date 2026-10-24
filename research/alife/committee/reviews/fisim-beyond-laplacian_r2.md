# Review: fisim-beyond-laplacian, sprint 2 (2026-10-24)

**Decision: CONTINUE, narrowed, with a stop rule** (promise 5/10). **Headline:** an honest and well-corrected negative sprint. The S/N selection run found no selection, and the reason is harder than the report says. Kick-arisen markers bred true in **0 of 3** on-divisions (2 independent kicks), the cells never die on their own, and the gate still has no resolved Laplacian control. xcell-evo2 takes over the family's L6[L3] (low) from the retracted xcell-turn. Next: one decisive heredity assay of arisen markers, gated vs resolved ungated arms, in the fast-division regime. L7 is retried only if that passes.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| xcell-evo2-S / -N | **L6[L3]**; L7 Contradicted; arisen-marker heredity 0/3 | low | S0 reaches gen 6 (11 persistent splits, 0 merges) and N1 gen 4. The other 4 runs reach gen 2. The biologist's crops of the S0 chain show rod, then dumbbell, then two equal ringed daughters at t=450/510/570/960. on→on+on is 0 in 6 runs, and the 3 on-divisions (S0, S1, N1) were all on→on+off. Final on-cells: S 1/0/2 vs N 1/1/0. Every death is an imposed disk erasure. | threads/fisim-beyond-laplacian/packs/xcell-evo2-S, …/xcell-evo2-N |
| xcell-her | **L3**; planted-kind heredity Supported; L6 Weak; L7 Contradicted | high | Unchanged r1 packs. Arm L (ungated, Dh=0.02) loses all planted markers by t≈100. The skeptic reproduced this on seed 11 at 64², but the ungated h fronts are ≈1 px wide, so it is not yet a matched control. | threads/fisim-beyond-laplacian/packs/xcell-her |
| xcell-a | **L4b[L3]**; L4a Weak | medium | Unchanged: an m4 glider carrying a passive gated compartment. | threads/fisim-beyond-laplacian/packs/xcell-a |
| xcell-turn | L3 (**retracted**; L6 withdrawn) | low | Its gen 5/6/4 is colonization by 2 surviving founders, which were poisoned at planting and carry a cargo-gated waste index bug. It is superseded by xcell-evo2. | threads/fisim-beyond-laplacian/packs/xcell-turn |

## Judges and arbitration

**Biologist (promise 5).** Ran no simulation. Replayed the state-independent kick/kill RNG and built a merge-aware lineage from the movie frames: raw gen 6/4/2 (S) and 3/4/2 (N), 0 merges, and 38/55 splits with no dilution disk touching the parent. Called L6[L3] Supported. Key insight: division is limited by space, not by kc. Free-space daughters re-divide every 50-70 t, crowded cells wait 1200+ t, and the chemostat runs at ≈0.7 generations per run. A bite census gives L4a Weak (incidental, no twin).

**Skeptic (promise 5).** Reran evo2-S on seed 11 (T=400). This reproduced the slow turnover and the kick mechanism: a compact h core inside the ring, held to t=400 (`hcrop_on.png`). Also reran arm L on a new seed. Found that the ungated Dh=0.02 fronts are ≈1 px wide, so lattice pinning cannot be excluded. Found that the neutral arm is not exactly ancestor-matched: an identity g on the h deviation gives S off-cells ≈+0.025 cargo drive. No dt/2 test has been run with disk erasure. Called L6 Weak.

**Curator (promise 4).** Confirmed from source that S and N share `krng = rng(10000+seed)`, so they are identical-event twins. Credit to the design. Found that s_L.py ran only the L rows at Dh=0.02, with no image. Raised drift from the brief: turnover and mutation now come from world-level Python, outside the x-genome. Also noted that wch=0.15 was assumed and never measured, and that frames.npz was not shipped, so the kinds calls cannot be audited.

**Arbitration.**
1. *evo2 L6, Supported vs Weak.* I looked at S0 `lineage.png` and `judge-scratch/fisim-beyond-laplacian-r2-biologist/S0_chain.png`. The 450→510→570 and 960 births are genuine fissions with complete rings around both daughters, which answers the skeptic's "unverified short tracks". **L6[L3] Supported, at low confidence.** Reasons for low: only 2/6 runs reach gen ≥ 3 by labkit (4/6 by the judge tracker), bodies are planted, deaths are imposed, division is Gray-Scott-class, and the birth strips came from a judge, not the researcher.
2. *Arisen heredity.* All three judges independently found the three on→on+off splits in kinds.json, which the report's headline omits. In `S1_kick115.png` the t≈120 kick lands on one pole, and the cell pinches at t≈170-180 with h pooled in the neck. Gated heredity is shown for planted, cell-filling domains, **not** for arisen ones. Raising the division rate alone will make this worse.
3. *Arm L.* In `judge-scratch/fisim-beyond-laplacian-r2-skeptic/larm_check.png`, ungated h domains are blocky and are left behind as the bodies drift, while gated h stays round and moves with each body. That could be real gate function or grid pinning. Beyond-diffusion stays ≤ 1 for the whole family until resolved arms (Dh 0.05/0.1, and Dh 0.02 at dx=0.25) fail where the gate succeeds.
4. *xcell-turn.* The researcher's retraction stands. Its leaderboard row is replaced (L3, retracted).

## Next sprint

**Main experiment: heredity of kick-arisen markers, gated vs resolved Laplacian arms, in the fast-division regime.**

*Setup.*
- Genome: xcell-evo2-N.
- Get divisions every ~50-100 t by freeing space: about 10x dilution (KILL_RATE≈1.0) or fewer founders. Use kc 0.35-0.5 only if that fails.
- At t≈100, kick (σ 1.5, amplitude 2.5) a random interior point of half the cells. Log each kick's offset from the cell centroid and the time to that cell's next pinch.

*Arms.* All arms use the same grid, IC, seeds and event RNG, with 3 seeds each and T≈600:
- gated: β_h=5, Dh=0.3;
- ungated: Dh 0.05 and 0.1 at dx=0.5;
- ungated: Dh 0.02 at dx=0.25.

*Readouts.*
- Classify every on-division from raw per-daughter h.
- Count conversions of intact cells.
- Ship h crops of every on-division on a fixed absolute h scale, plus frames.npz.

*Pass.*
- ≥ 20 on-divisions per arm.
- Gated on+on ≥ 80%.
- Every resolved ungated arm is clearly worse, in images.

*Stop rule.* Allow one fix if gated arisen marks still split: a cell-filling kick, faster h spread inside the ring, or within-cell purification. If they still split after that, or if a resolved ungated arm matches the gate, stop chasing L7 in this family. Return to the brief instead: an independent, self-made membrane field carrying the gate.

**Secondary goals**
1. *Only if the assay passes:* run the S/N twins at fast dilution (3 seeds per arm, T=2000).
   - Use a thresholded g, so that off-cells are exactly neutral.
   - Measure s directly as per-kind inter-division time and area.
   - Pre-register the readouts: on→on+on vs on+off by kick-to-pinch time; per-kind births and deaths per 200 t; on-fraction S vs N.
   - Pass: one arisen lineage with ≥ 3 consecutive on+on divisions, and S above N's spread in 3/3 seeds.
2. *Intrinsic death inside the genome.* Screen one conserved cost that is split at division (the researcher's CH-type waste idea) as a replacement for the world-level disk erasure.
3. *Record.* Correct the r2 headline on arisen heredity. Ship birth strips for any L6 claim.

## Cross-pollination

- **Out.**
  - *autopoiesis:* the membrane_kinds r2 horizontal transfer through φ tails is the problem the perm gate solves. In xcell-her, on and off cells sit interleaved in a touching lattice with 0 switches.
  - *active-droplets:* shared-RNG identical-event S/N twins, plus chemostat dilution, to get selection past colonization. Dilution must run near the free-space division rate.
  - *lenia-multichannel, particle-life:* a lab lesson. Dissipative-soliton cells do not die, and a concentration-type waste cannot age them. Intrinsic death needs an extensive cost that is split at division.
- **In.**
  - From chemotaxis-motility: within-body purification (REPORT_r2 Mechanism 2) and `fission.py`.
  - From active-droplets: cross-inhibition (REPORT_r1 Mechanism 4).
  - From autopoiesis: `kindtrack.py`.

## Rubric issues

1. **labkit colour scales.** Per-pack percentile colour scales saturate bistable marker channels, so kinds cannot be read from the S1/S2/N1/N2 sheets. Use fixed or cross-arm-shared scales for kind channels.
2. **labkit rim_vs_outside.** It misreads band membranes, because its outside annulus sits on the m peak. The evo2 packs also lack radial.png.
3. **L7: arisen vs planted kinds.** Require off-kind-daughter counts for *arisen* kinds separately from planted ones. A planted-kind result must not stand in for heredity of variation.
4. **L7: power.** A selection test whose arisen lineages get < ~3 divisions each should be reported as "underpowered", not as a measured null. World-level events outside the genome (kicks, erasure) must be declared in META.
