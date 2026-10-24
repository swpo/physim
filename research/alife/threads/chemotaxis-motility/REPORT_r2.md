# REPORT r2: chemotaxis-motility

## Headline
**Evolutionary rescue in a world of self-propelled, dividing chemotactic swimmers.** Prey swimmers divide by binary fission
and carry a heritable allele in their body. Predators chase them and eat them down toward collapse. An evasion allele
that arises by mutation during the run breeds true and sweeps in 3/3 seeds, and the prey-predator community then
recovers. Two controls fail to rescue, each in all 3 seeds: the same mutation process with no benefit (neutral) lets
prey and predators collapse together, and without predators the costly allele never spreads. The individuals that
evolve are motile, eating, dividing and interacting.

## Claims
| world | rung | strongest evidence | known weaknesses |
|---|---|---|---|
| `evopursuit` (+ `_neutral`, `_nopred`) | **L7[L2]** with L4b, L5 and L6 individuals | `packs/evopursuit/alleles_all.png` (9 runs). A/B bodies at t=1500: selection 0/29, 0/30, 0/34. Neutral: prey collapse (0-1 B bodies, prey -95%). No predators: 7-9 A bodies and 0 B. Exposure B/A 0.64-0.72 (selection) vs 1.03-1.22 (neutral). Sheets: `evopursuit/seed2/sheet.png` (cyan A eaten down by t≈700; orange B crescents take over by t≈1200). **Movie: `packs/evopursuit/seed0/movie.mp4`.** | Numerics: dt/2 reproduces the rescue (`evopursuit_dthalf`: A1/B33 at t=1500, predators +63%, exposure B/A 0.73). Only 2 alleles and one trait. Mutation is a planted operator (symmetric patch swaps), not a copying error. Rescue has a cost threshold: cost 0.22 rescues (1 seed, 33 B bodies), cost 0.30 fails (2/2 seeds). Prey bodies have no internal structure beyond front/back (L2). **No k=0 escort arm was run** (see the review response), so the claim that predation causes the prey decline rests on neutral vs no-predator (0-2 vs 7-9 prey bodies) and predator growth (+60%), not on the decomposition the committee asked for. |
| `swimfission` | **L6[L2]** + L4b + L4c | `fission.py` (dense tracker, lone parent, both daughters survive ≥ 40 t): 10/10/15 clean fissions, **max generation 4/3/5** (`packs/fission_swimfission_s*.json`). Strips `*_strip.png` show a swimmer elongating and pinching at the waist into two equal daughters that swim apart. Daughter sizes: smaller/larger daughter median 0.94 / 0.82 / 0.80, and **26/35 pairs within 30% of each other**. The two daughters together are 1.08-1.12x the parent 10 t after the split (each starts at about half and regrows). From noise, 3 seeds. labkit pack `packs/swimfission`: 43-45 moving tracks per seed. | **The ablated control still divides, rarely**: parent toxforage (Da 4) gives 3 clean fissions (max gen 2) in `fission_toxforage_ctrl_s0`, against 10-15. Da 2 raises the rate rather than creating fission, so the review's "no divisions in the control" criterion is not met. labkit's own lineage under-counts (max gen 2-3) because of its 6-t sampling. Collisions still cause merges and debris. |
| `swimevo` (+ `_neutral`) | L7[L2] **Weak** | Breeding true: 17/17 pure-A parents → pure-A daughters. Parents with B ≥ 0.77 → daughters 0.83-1.00 (4/5). Generations 6-7 (`packs/fission_swimevo_s*.json`). Growth-rate allele: B 21 vs A 6 bodies (selection) vs B 5 vs A 14 (neutral) at t=1800. | Only ~10 bodies per run. The signal holds in 3/3 pairs but has small numbers. The population slowly declines. |

## Mechanisms learned (with ablations)
1. **Fission = growth past the cohesion range.** Swimmers grow at the front, where the food is, and lengthen along their heading. If
   the attractant range sqrt(Da/ka) is shorter than about half the body length, the waist thins and the body splits. Da 4 → 3 clean
   fissions per 1200 t; Da 2 → 10-15 with lineages 3-5 deep; Da 1 → 0 (bodies too small to grow). This is the active-droplets
   rule (body larger than its internal transport length) carried over to motile bodies.
2. **Own-density cooperative growth purifies bodies.** Growth ∝ k³/(rh²+k²) per allele makes the majority allele win inside a body
   (the analogue of active-droplets' within-droplet competition), so mixed bodies are transient and fission passes the allele on. Forked
   from active-droplets ad5-evolve (META.parent).
3. **Selection acts through behaviour, not chemistry.** In evopursuit the allele changes only how strongly the body flees the predator
   signal. Its benefit appears only with predators (exposure B/A ≈ 0.7 vs 1.0 neutral), and it is a net loss without them
   (15% growth cost, never spreads). The fitness of a kind is set by an interaction between motile individuals.
4. **Rescue.** At k 0.1 the base prey-predator system is not viable: it collapses in all neutral runs. The evasion allele moves it
   to a viable state with *more* predators (+60-67%). At k 0.2 the prey die before any mutant arises. At k 0.05 B rises
   slowly. Cost 0.22 still rescues (`evopursuit_cost22`); cost 0.30 fails in 2/2 seeds (`evopursuit_cost30_s*`).

## Negative results
- k 0.2 (the sprint-1 ecology value) with small dividing prey: extinct by t≈1000 in screens. Predation must be weaker for small prey.
- Stronger growth or regrowth alone (g 0.15-0.3, r 0.1) gives fragmentation (707 splits, 0 clean fissions), not reproduction.
- swimevo populations decline by about half over t=1800 (mixed bodies grow worse). Not yet fixed.
- labkit lineage (6-t sampling, union of species) cannot see fission of moving bodies or species separately. I used my own trackers
  (`fission.py`, `alleles.py`, `exposure.py`), which are small and read frames.npz or re-run the world.
- (From sprint 1, still true) mass-conserving trail swimmers coarsen into immotile aggregates. Toxic trails, growth and fission keep the
  swimmer phase alive.

## Response to the sprint-1 review
The review was queued at 16:54 but reached this session only at 18:16, after this sprint's work was done. The sprint therefore followed my own plan
plus the lab digest. Mapping the review's requests onto what was done:
- **Main experiment, fed swimmer reproduces (L6).** Done by a different route from the one suggested: elongation past the cohesion range, not
  core starvation. From noise on 3 seeds: 10-15 clean crescent → 2 crescent fissions per run, lineages 3-5 generations deep, and daughters
  near-equal (26/35 pairs within 30%). Not met: (i) the control (Da 4) still divides at a low rate (3 per 1200 t); (ii) the single-crescent
  life-history assay at 256² with a per-body uptake/toxin budget (part a) was not run.
- **Ecology.** I accept the matched-control result. The sprint-1 "predation lowers prey" claim (-24%) came from a mismatched grid and is
  withdrawn. The decomposition (full / k=0 / escort / chi_y=0 / prey alone, species-aware) was not run this sprint. The same caveat applies
  to evopursuit.
- **Not done:** the n=0 starvation packs (3 seeds), the clipping-loss log, the Laplacian-only slow-inhibitor RD control, the LITERATURE additions.
  Done partly: dt/2 for a kinetic world (evopursuit) and species-aware analysis via my own scripts (`alleles.py`, `exposure.py`, `fission.py`).

## Next sprint
0. The review's open items first: ecology/evopursuit decomposition with a k=0 escort arm (192², 3 seeds, species-aware); n=0 starvation
   packs; the single-crescent life-history assay with a per-body budget; core-starvation fission with an ablation that gives *zero* divisions;
   the slow-inhibitor RD control and the literature.
1. Map the rescue: a cost × predation-rate grid with ≥ 3 seeds per point, and the timing of the first B mutant against collapse.
2. Coevolution: give predators a heritable pursuit allele (chi_y) as well. Look for arms-race cycling (Red Queen), and use the
   gated-mobility membrane from the autopoiesis and fisim threads for an internal compartment (L3 swimmers).
3. Continuous traits (evasion strength as a carried concentration) to see whether it evolves to an optimum that depends on predator density.
4. Numerics: 2x resolution for evopursuit (dt/2 done), and a long run (t ≥ 4000) for whether B fixes or A returns by back-mutation.
