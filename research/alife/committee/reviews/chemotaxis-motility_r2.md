# Review: chemotaxis-motility, sprint 2 (2026-10-24)

**Decision: CONTINUE on evopursuit, audit and decomposition first** (promise 8/10).

**Headline.** This is the lab's fastest climb this round and its strongest population-level selection signal. In evopursuit, a behavioural evasion allele arises by mutation and sweeps through motile prey that divide and live bound to predators. It sweeps in 3/3 seeds and fails in 3/3 matched neutral runs and 3/3 predator-free runs.

Under v2, evopursuit rates **L5[L2]+L4b, with L6 and L7 both Weak (L7 near-Supported)**. Two things are missing: the per-kind births, deaths and conversions ledger, and a prey lineage in this world.

swimfission is **L6[L2]** (medium confidence). The "rescue from predation" story does not survive the matched masses: B prey that live with predators end with 2-3x the mass of prey that live without them.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| evopursuit (+_neutral, _nopred, _dthalf, _cost22/30) | **L5[L2]+L4b**; L6 Weak; L7 Weak (near-Supported); L3 Contradicted | medium | Bodies A/B at t=1500 (`alleles_all.png`): 0/29, 0/30, 0/34 with selection; 0-1 B in the neutral arm (e=cost=0); 0 B with no predators. The dt/2 run gives A1/B33.<br>The skeptic's seed-11 rerun at 128² reproduces the sweep: A extinct by t≈1020, 18 B bodies.<br>Prey totals at t=1500, from a start of 1283 (I recomputed these from metrics.json): selection 1458-1622 (all B); neutral 113-138; no predators 586-769. Predators go from 637 to 1015-1066 with selection and to 107-162 in the neutral arm.<br>In the seed2 sheet at t=1176-1500, every orange B crescent still cups a magenta predator. | threads/chemotaxis-motility/packs/evopursuit |
| swimfission | **L6[L2]+L4b**; L4c Weak | medium | In `fission_swimfission_s2_strip.png`, swimmers elongate, form a waist and pinch into two equal ovals that swim apart.<br>labkit lineage from noise reaches gen 2/2/3, with 3/6/8 persistent splits.<br>The genealogy is reticulate: merges 56/56/45 against splits 45/39/31.<br>The Da 4 control still divides (3 fissions), and bodies fall from about 28 to 8-11. | threads/chemotaxis-motility/packs/swimfission |
| swimevo (+_neutral) | **L6[L2]**; L7 Weak | low | B against A at t=1800: 21 vs 6 with selection, 5 vs 14 neutral (summed over 3 seeds).<br>The only shown fission happens before any mutation.<br>About 10 bodies per run, a declining population, and a growth-rate allele that wins by construction. Superseded. | threads/chemotaxis-motility/packs/swimevo |

## Judges and arbitration

**Biologist (promise 8).** Ran no simulation. Worked from movie frames, zoomed tiles and the channel totals. Read the sweep plainly in the images, and found that the B prey keep their riders yet carry more than twice the prey mass of the predator-free arm. Concluded that evolution turns a lethal escort into a sustainable partnership. Reported labkit's evopursuit lineage as a metric failure: species fused, 0 persistent splits, 796-1076 false nucleations.

**Skeptic (promise 8).** Did two reruns.
- **evopursuit, seed 11, 128², t=1200.** The sweep and the prey recovery reproduced. Exposure B/A was 0.82, weaker than the packs' 0.64-0.72.
- **swimfission, seed 11.** Used a strict fission.py in which generation passes through a merge only from the largest parent. This gave max gen 2, not the 4-5 the report claims, so the report's max() rule inflates depth.

Also pointed out two features of the mutation operator. It is a radius-4 swap that converts a whole living body. Its rate is set per domain, so the mutation pressure on each body rises as the population collapses. That fits the A≈B end masses in the neutral arms.

**Curator (promise 8).** Alone in rating evopursuit L7 Supported (low). The argument is a count: at most about 8 A bodies are left at take-off, and there are about 27 mutation events per run, yet B reaches about 30 bodies. Proposed the escort reading independently and supplied the literature (evolutionary rescue; spike self-replication in chemotaxis). Asks that fission.py, alleles.py and exposure.py become labkit modules.

**Arbitration.**
1. **L7: Weak.** I examined `alleles_all.png` and the seed2 sheet. After A goes extinct (seed0 t≈1000, seed2 t≈1100), B bodies keep rising from about 15 to 33. Since a patch mutation in a B body makes A, those bodies can only come from B bodies multiplying. That much of the curator's argument stands.

   Even so, v2 requires the researcher to *report* conversions of intact bodies per mutation, and per-kind births, deaths, flips and off-kind daughters. None of these was reported. Births here are inferred, not traced, so L6 in this world is itself Weak. In addition, a fragmentation-and-regrowth reading is not excluded, and the neutral arm is matched in design but is not an identical-event twin. Two of the three judges and the rubric agree on Weak. The ledger is a cheap analysis, which is why this is near-Supported.

2. **Interpretation.** All three judges found independently that predators benefit B prey, and I confirmed the totals. The "rescue from predation" headline is therefore withdrawn until the decomposition is run. Under v2 L5, the effect on prey is established only for A (negative, matched). For B it is unmatched, because the predator-free arm contains only A.

3. **swimfission L6.** Supported at medium confidence, capped by the reticulate genealogy. It meets the bar of gen ≥ 2 from noise, by labkit and by the strict rerun. The deeper generations claimed are not credited. Da sets the fission rate in a dose-dependent way (Da 1: 0, Da 2: 10-15, Da 4: 3), which is mechanism, but the zero-division control the committee asked for was not met.

4. **L4c.** Weak on swimfission. Rubric v2 asks for the ablation on the world claimed, and the dependence here holds by construction.

5. **Modifiers.** Beyond-diffusion stays at 1 across the thread: there is still no Laplacian-only control, now owed for two sprints.

## Next sprint

**Main experiment: an audited, decomposed evopursuit.** 160², t=1500, seeds 0-2.
- **(a) Selection runs and identical-event neutral twins.** Log every mutation event: time, site, the body hit, and that body's A/B fraction before and after. Replay the same events with e=cost=0.
- **(b) Fixed-allele arms (m=0).** Run all-A and all-B prey against each of three partners: consuming predators (k=0.1), non-consuming immortal escorts (k=0, predator toxin death off), and no predators. That is 18 runs.

**Readouts.**
- A prey-only (A+B), merge-aware tracker sampled every 2 t, with the largest-parent generation rule. labkit `META["species"]` is now available for this.
- Per kind: births; deaths, split into eaten and toxin; flips; conversions per mutation; off-kind daughters.
- Strips of randomly chosen B births at the deepest generation.
- The sign of each partner's effect, for each allele.

**Pass criteria.**
- B births far exceed conversions.
- B reaches gen ≥ 2.
- A mechanism is named. If B with escorts ≥ B with predators > B alone, report the result as exploitation of the chase, not as escape.

**Secondary goals**
1. **Numerics and robustness.**
   - evopursuit at 1.5-2x resolution, with lengths scaled (1 seed).
   - dt/2 on a second seed.
   - ±10% on k and on cost (3 seeds).
   - swimfission dt/2 and a resolution change, since the 4.5 px cohesion range sets division.
   - Log the mass lost to clipping.
2. **L6/L4c cleanup on swimfission.** Rerun with the largest-parent generation rule and random deepest-generation strips. Add an abrupt n=0 fork with fed twins on 3 seeds.
3. **Beyond-diffusion.** A Laplacian-only control for the trail swimmer, and the LITERATURE §2.6 entries (verify the citations). Coevolution (a predator allele) is fundable only once the ledger is in.

## Cross-pollination

**Out**
- **active-droplets:** a predator species that gives selective deaths after colonization, and the three-arm design (selection / e=cost=0 neutral / no partner).
- **autopoiesis:** pursuit that works. Predators ride in the prey's concave rear under non-reciprocal cross-taxis at small k. Compare with your `hunters` negative. Also, the toxic self-trail can replace rigid phoresis.
- **flow-lenia** and **lenia-multichannel:** a behavioural allele whose benefit exists only with a partner gives a strong selection signal that matched arms can verify. lenia-multichannel's alleles were lost to drift, and they might take hold when an interaction partner pushes the ancestor below viability.

**In**
- autopoiesis `kindtrack.py`, for the ledger.
- fisim's identical-event twins from a shared RNG (`xcell-evo2-S/world.py`, `evo.py`).
- lenia-multichannel's REPORT_r2 ledger format.
- autopoiesis `motile_trait_tox`, for later work on a continuous trait.
- For L3 swimmers: the phase_membrane wall, or the fisim xcell-a band ring.

## Rubric issues

1. **L7 when L6 in the same world is Weak.** State that births must be traced in the world claimed. Evidence inherited from a sibling world does not count, even when the dynamics are identical before the first mutation.
2. **L5 when kinds evolve.** If the sign of the effect differs by kind, the matched control must be per kind (fixed-allele arms). B-with-partner against A-without-partner is unmatched.
3. **L7 mutation reporting.** Require the operator's footprint relative to the median body, and the rate per capita rather than per domain.
4. **labkit.**
   - Species-fused matter breaks lineage in multi-species worlds. Point users to `META["species"]`.
   - Sampling every 12 t misses fissions of moving bodies.
   - Generation through a merge should follow the largest parent. fission.py's max() inflates depth.
   - alleles.py thresholds at 0.35 of the run-global maximum.
5. **Process.** The r1 review arrived after the sprint's work was done. It was also late for autopoiesis and flow-lenia, and arrived mid-sprint for lenia-multichannel and particle-life. The director must deliver reviews before a sprint starts.
