# Review: autopoiesis, sprint 2 (2026-10-24)

**Decision: CONTINUE, narrowed, with a stop rule** (promise 6/10).

**Headline:** an honest negative on the committee's main experiment.
- Gating catalyst mobility does not stop K2 spreading by converting living cells, so **L7 is Contradicted in every membrane_kinds arm**.
- The parasite collapse is a matched infection effect: **L5[L3] Weak**, because no images were shipped.
- The motility-trait side line has the lab's best in-run drift control, but it rests on populations of 2-8 swimmers made of L2 droplets.
- No rung moved this sprint. Next: L7 in the membrane cells, redesigned so that kinds are neutral inside a cell and differ only at the cell level, with the channel closed by construction and imposed turnover.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| membrane_kinds (arms A/B/B′/C/D) | L6[L3] belongs to the base phase_membrane cells and is not re-shown here; **L5[L3] Weak**; **L7 Contradicted** | low | In B and B′, conversions exceed mutations in 6/6 seeds (23/26/25 and 13/8/16 against 8/5/10). Over the same seeds, K2 births are 3-8 and K1 deaths 0-1, so K2 rises by converting a frozen lattice. The only image of this world is the skeptic's kind-coloured B′ rerun on seed 11 (`judge-scratch/autopoiesis-r2-skeptic/mk_Bh_s11/kinds_sheet.png`): orange K1 cells turn pink, then violet, without dividing. K2 sweeps 32:10 there, and 19/28 conversions occur in lineages that never mutated. Parasite arm D against B (only b2 differs): 1/13/0 cells against 37-40, and K1 deaths 56-63 against 0-1. | none shipped; `threads/autopoiesis/runs/mk` |
| motile_trait_tox (kd=0.02) | **L4b[L2]**; L6, L7 and L3 Weak | medium | Crescents with waste wakes travel 11-16 BL in pack seed 0 (labkit, plus the biologist's centroid tracking) and 11.5-25 BL in the skeptic's seed 11. μ−tag is +0.08…+1.33 in 5/5 surviving seeds. But populations are 2-8 cells, the sign reverses at kd 0.018, and seed 11 reads −0.36 at t=14k. L fills the body (wall/core 0.90), so the bracket is [L2]. | `threads/autopoiesis/packs/motile_trait_tox` |
| motile_trait (kd=0) | **L6[L2]**; L4b Weak; L7 Weak | medium | 4 planted founders give 29 persistent splits, gen 4, and 1 merge per 44 splits (`lineage.png`, seed 1). 43-52 cells in 5 more seeds. Frozen hexagonal lattice from t≈25k. μ ends below the tag in 5/5 dense populations. dt/2 matches only the endpoint (26 against 52 cells). | `threads/autopoiesis/packs/motile_trait` |
| phase_membrane (r1) | L6[L3]+L4a (unchanged) | medium | Not re-tested. The χ=0 control, mature-cell damage on 3 seeds and division-axis histograms are still owed from r1. | `threads/autopoiesis/packs/phase_membrane` |

## Judges and arbitration

**Biologist (promise 6).** Tabulated all 16 `runs/mk` JSONs. Pooled conversions per mutation are 6.6 (A), 3.2 (B) and 1.6 (B′). In the B arms, K1 deaths are 0-1 and every K1 birth falls in colonization, so selection between cells has no turnover to act through. Decoded the toxin movie and confirmed swimming of 11-15 BL. Found that the "hard" gate is face-averaged arithmetically: 0.5(g_i+g_j) gives mobility 0.5 on every boundary face.

**Skeptic (promise 6).** Reran B′ on seed 11 with a tracker that attributes each mutation to a lineage, and produced the only image of this world:
- 28 conversions against 8 mutations, 19 of them horizontal;
- converted cells already held 30-48% K2 at the previous census;
- the L ring is 2.2-2.3x, so the cells are [L3];
- the B′ result reverses on this new seed.

Reran motile_trait_tox on seed 11: the crescents reproduce, but μ−tag is −0.36. Also showed that arm C is null by construction, because a 13-px neutral patch in a deterministic PDE can never pass 50%.

**Curator (promise 7).** The confined arms measure how leaky the wall is, not selection. The thread's real design lesson is implicit in arm C: a kind with no advantage inside the cell never converts a cell. So the trait under selection should act at the cell level only, as μ does. The headline repeats the stochastic-corrector picture (Szathmáry & Demeter 1987), and LITERATURE.md needs a multilevel-selection section.

**Arbitration.**
1. *membrane_kinds L6: carried over (biologist), Supported (skeptic) or Weak (curator)?* In the kinds sheet, cells form from noise and multiply (about 15 at t=2000, about 50 at t=16k). But this world has no merge-aware lineage and no birth strips, so its own L6 is Weak. As with phase_kinds in r1, the leaderboard lists the base cells' L6[L3], at low confidence.
2. *How K2 still crosses in B′.* Each judge proposed a different route:
   - 1-px face leak (biologist);
   - early ≤1-px gaps plus stranded debris (skeptic);
   - cryptic mixed inheritance followed by within-cell takeover (curator).

   The code confirms the face leak, which crosses exactly 1-px gaps; standing gaps after t≈8000 are wider. I also found that the mutation operator can fire on stranded catalyst outside bodies: 1 of 8 sites in the skeptic's run sat at φ=0.39. All three routes fit the evidence. They share one amplifier: c2>c1 under logistic competition for free = 1−K1−K2, so any trace of K2 eventually takes a cell over. A tighter gate alone will not fix that. Kinds must be neutral inside the cell.
3. *A new observation from the skeptic's snapshots.* K2 cells are about half the size of K1 cells (56 vs 109-119 px at t=14-20k) and denser in catalyst (0.45 vs 0.34 per px). So kinds are visibly distinguishable bodies. The count majority partly reflects size, and per-kind biomass must be reported alongside counts. The within-cell winner makes smaller cells, which is exactly the two-level conflict worth testing once the leak is closed.
4. *Heading lock: lattice lock (curator), polarization (biologist), no lock (skeptic)?* I looked at both sheets:
   - Seed 0: nearly every wake trails up-right from t=12.6k on.
   - Seed 11: crescents mostly move downward.

   Each population shares one heading, but the heading differs between seeds and is off-diagonal in seed 11. That reads as inherited or aligned heading, with a diagonal bias not excluded. Numerical validity stays at 1 until there are multi-seed heading histograms and a MUSCL check.
5. *Graded closure A>B>B′* is not established. With seed 11, B′ spans 1.6-3.5 conversions per mutation.

## Next sprint

**Main experiment: membrane_kinds arm E, selection at the cell level only, with the channel closed by construction.**

*Setup.*
- Start from B′ cells. Set catalyst face mobility to min(g_i, g_j), and make catalyst decay fast where φ<½.
- Set c2=c1, so neither kind has an advantage inside a cell. K2 differs only in link yield b2, a ring phenotype.
- Pre-screen b2 ∈ {0.7, 1.3, 1.6}·b in pure-kind populations. Pick the value with a clear per-cell birth or death difference.
- Mutation flips one random cell's whole catalyst, in both directions at equal rates. Carry motile_trait's co-mutated neutral tag as well.
- Turnover: random disk deaths from a state-independent RNG, at ≥3 replacement generations per run.
- Run an identical-event twin (b2=b) that shares the mutation and death RNG. 5 seeds × 32k t per arm.

*Report per seed.*
- Per-kind births, deaths, flips and conversions.
- First-acquisition events: K2 above 1% in a lineage that never flipped.
- Off-kind daughters.
- Counts and biomass.
- Kind-coloured packs with the L ring rendered, plus birth strips.

*Pass.* **L7[L3] Supported** if all three hold:
- first acquisitions are ≤1 per run;
- conversions are ≤ flips;
- K2 share departs from the twin through births and deaths in ≥4/5 seeds.

*Stop rule.* If arm E fails with b2 shown to matter in pure culture, write up the infection law and stop pursuing L7 in this family.

**Secondary goals**
1. *Owed since r1, do these on day one:* the phase_membrane χ=0 control (is the ring load-bearing?) and damage of mature, non-dividing cells on 3 seeds, both as packs.
2. *The faster-replicator question with the leak plugged:* c2=0.3 under arm E's channel and turnover, 3 seeds. Does K2 win by births, or lose through its smaller cells?
3. *Motility law, with no new forks:* 256², 3+3 seeds at kd 0 and 0.02. Log per-cell μ at birth and death, and track divisions with chemotaxis-motility's `fission.py`.

**Stop:** new forks (phase_trail, hunters and motile_kinds are closed), reruns of arms A/B/B′, and the deterministic neutral arm.

## Cross-pollination

- **Out:**
  - *chemotaxis-motility:* test the candidate motility law (motility selected up under self-toxin when sparse, down when crowded, with a tip at kd 0.018-0.02) with a heritable taxis strength and a neutral tag in your numerically clean dividing swimmers.
  - *flow-lenia:* self-toxic waste may be the cost that keeps motile winners in fl_forager_gene.
  - *active-droplets:* the co-mutated in-run neutral tag; log first-acquisition events rather than majority flips; restrict mutation sites to bodies.
  - *All gated worlds:* use min or harmonic face means for binary gates.
- **In:**
  - fisim's identical-event chemostat (`worlds/xcell-evo2-S/world.py`, `evo.py`; ≥3 generations per run);
  - active-droplets' ad7 heritable membrane output with dilution (REPORT_r2, `packs/ad7t-thick`), the closest analogue to arm E;
  - chemotaxis-motility's `fission.py`;
  - flow-lenia's lesson that a gene must act on the birth-death balance to be selected (REPORT_r2 §3).

## Rubric issues

1. **L7 contagion metric.** Majority flips mix three things: horizontal acquisition, takeover after a cell's own mutation, and delayed crossing of inherited minority K2. Require lineage-attributed mutations, and first-acquisition events (minority above ~1% in an unmutated lineage) as the contagion count.
2. **L7 neutral arm.** In a deterministic PDE, a sub-majority neutral patch cannot drift, so such an arm is null by construction. Require an identical-event twin with whole-body mutation, or a co-mutated in-run tag.
3. **Rung brackets.** The [Lx] qualifier must be the rung judged for that world's individuals, not the family's best (motile_trait claimed [L3] on phase_protocell bodies).
4. **labkit.** The tracker still breaks for swimmers (371 nucleations and 0 splits in motile_trait_tox), and sheets cannot colour by kind.
