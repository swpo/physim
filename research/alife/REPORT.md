# ALife agent lab: final report

For the PhySim project lead, 24 October 2026. Paths are relative to `research/alife/`.
Rungs and confidences are the committee's final consensus (`committee/LEADERBOARD.md`,
`committee/reviews/*_r3.md`). They are not the researchers' own claims, and where the two
differ this report follows the committee. The rung notation is defined in `RUBRIC.md`.
`L6[L3]` means reproduction of individuals that have a material boundary layer.

**The run.** There were 7 independent researcher agents, each with its own thread, plus a
central committee of 3 lens judges and a director. The lab ran 3 sprints in about 8 hours
of wall-clock time, from 14:03 to 21:45 UTC. It produced about 130 world directories, 58
leaderboard rows and 21 committee reviews, at a cost of about 605 USD API-equivalent.

---

## 1. Summary

1. **Dividing cells with a real membrane can form from noise.** In autopoiesis
   `phase_membrane`, an Allen-Cahn phase wall is held up by links that the cell's own
   catalyst makes. Mobility is gated by phi^2, and the links adsorb at the wall into a
   ring 2.1-2.5x the core. Both daughters inherit the ring, to generation 3. Consensus
   **L6[L3], medium**. In active-droplets `ad7`, fuel-fed Cahn-Hilliard droplets make their
   own amphiphile shell, which gates fuel and catalyst. That gives membrane output an
   interior fitness optimum, and each side of the trade-off disappears under its own
   ablation. Consensus **L6[L3], medium**, with planted founders. These two worlds are the
   lab's best organized reproducers.
2. **No thread got far on heredity with selection.** Only two L7 rows exist, and both are
   low confidence:
   - autopoiesis `membrane_evo`, **L7[L3] low**, recorded as *disturbance-mediated*: the
     sweep runs mostly through fragments that the imposed death disk cuts off;
   - active-droplets `ad5-evolve`, **L7[L2] low**: selection happens only during
     colonization, against a sterile ancestor.

   The other five threads ended with L7 Weak, Contradicted or Not tested. The same four
   causes recur:
   - heritable labels leak between field bodies that touch (contagion);
   - cells have no death of their own;
   - mutation operators do not match the shape and size of the bodies;
   - tests were underpowered, with 6-40 bodies and 1-5 mutations per run.
3. **The strongest behavioural result is ecological.** In chemotaxis `evopursuit`,
   self-propelled prey form spontaneously and predators ride in the rear of prey crescents.
   An evasion allele that arises by mutation flips the sign of the predator's net effect on
   prey: it is lethal to allele-A prey (0.15-0.36x prey alone) and a net benefit to allele-B
   prey (2.4-3.5x). This holds in 18 matched fixed-allele arms. Consensus **L5[L2]+L4b,
   high**, with L6 and L7 Weak.
4. **Beyond diffusion, we found one transferable operator but proved little against
   diffusion.**
   - Three threads independently arrived at the same containment operator: mobility gated
     at a boundary the body makes itself, div(D e^{-beta m} grad c). It does the work in
     its own ablations.
   - Only one matched control that replaces the non-diffusive operator with linear
     diffusion ever failed where the world succeeded: the ad7 "R arm", on 1 seed. It was
     scored 2 provisional.
   - Several apparent non-diffusive wins turned out to be Gray-Scott chemistry in disguise:
     `ad1-fuel`, `mcfd-MIRd` and `xcell-div`.
   - Sharp boundaries were cheap to get and were not the bottleneck. The hard parts were
     containing heritable state and getting turnover.
5. **Question 1 (the judge): a rubric-driven judge works, but only if it re-runs worlds
   and demands matched controls.** The ladder plus modifiers plus promise held up across
   seven very different families. The judges downgraded more than two dozen researcher
   claims and upgraded about 7. Among other things, they caught:
   - a channel-index bug;
   - a timestep artifact behind one thread's entire reproduction mode;
   - three sign flips under matched controls;
   - label conversions (contagion or leakage) undermining selection claims in five
     threads.

   Rubric v2 (16 rule changes) was written from those counterexamples. Review was the
   expensive part: 64% of total spend.
6. **Question 2 (agent mutation): it is more expressive, but the hit rate is low and the
   gains came early.**
   - Every rung above L3 came from structural edits that a parameter-mutation EA cannot
     make: new fields, conservation laws, operator swaps, gates and cross-thread forks.
   - Random rule screens inside one family gave shelled cells in 2/420 rules and 0 cell
     replicators in 150.
   - Most gains came in sprints 1-2. In sprint 3 only autopoiesis raised its ceiling, and
     lenia and flow-lenia never moved up after sprint 1. Most later edits targeted heredity
     and failed.
   - Agents often overclaimed and skipped the controls they were asked to run.
7. **Question 3 (teams): the organization was good for breadth and for catching errors,
   but review was the bottleneck.**
   - Ideas really did move between threads. The gate, identical-event twins and confined
     alleles each went to 2-4 other threads, and forks produced the best rungs in
     active-droplets and autopoiesis.
   - But the sprint-1 reviews arrived 60-105 minutes into sprint 2, after that sprint's
     work was already finished in three threads.
   - The committee was CPU-bound.
   - Three sprints of about 1.5 hours each were too short to reach L7.
8. **Numerical artifacts can look like life.**
   - In particle-life, spore reproduction was overshoot by the explicit integrator, and
     every rung above L2 in that thread had rested on it for two sprints.
   - Halving dt is not a convergence test under reintegration tracking or with a clipped
     integrator.
   - ad7's 2-px shell has its width set by the grid.

   An automated search needs numerics gates built in.

---

## 2. What we found, by rung

**Best worlds per thread** (consensus rung and confidence; "noise" = forms from random initial conditions):

| Thread (family) | World | Rung (confidence) | What it does | Origin | Pack |
|---|---|---|---|---|---|
| autopoiesis (continuous autopoiesis) | `phase_membrane` | L6[L3] (medium) | Allen-Cahn wall tilted by the cell's own link product, a(L-theta). phi^2-gated mobility. Links adsorb at the wall into a ring that sets cell size (~2x) and division rate (~3x). Cells divide by central starvation. | noise | `threads/autopoiesis/packs/phase_membrane` |
| | `membrane_evo` (up / twin / down) | L7[L3] (low, disturbance-mediated) | Two kinds that differ only in link yield, with a sealed catalyst channel and identical-event twins (10 seeds x 3 arms). High yield sweeps (0.85-0.97 biomass share in 8/10 seeds); low yield is purged. | noise | `threads/autopoiesis/packs/membrane_evo_up` |
| | `phase_protocell_noise` | L6[L2] (high) | The wall loop without adsorption. 42-46 cells, gen 3-4, converged at dt/2 and 2x resolution. | noise | `threads/autopoiesis/packs/phase_protocell_noise` |
| active-droplets (Cahn-Hilliard + reactions) | `ad7-gated` family | L6[L3] (medium) | A self-made amphiphile shell psi gates fuel (weakly) and catalyst (strongly). Shell output has an interior optimum (seed 0: 4/7/12/11/10/9/6 droplets at kp 0-4). | planted | `threads/active-droplets/packs/ad7t-thick` |
| | `ad5-evolve` | L7[L2] (low) | Confined catalyst alleles mutate during the run, breed true, and out-divide a sterile ancestor (p≈0.001). Colonization only, 0 deaths. | planted | `threads/active-droplets/packs/ad5-evolve` |
| | `ad1-fuel` | L6[L2] (high) | Core starvation splits droplets into ring fragments and dumbbells, gen 2-4. Converged in dt and dx. It is Gray-Scott mitosis in a CH body. | planted | `threads/active-droplets/packs/ad1-fuel` |
| chemotaxis-motility (Keller-Segel, advection) | `evopursuit` | L5[L2]+L4b (high); L6, L7 Weak | Toxic-trail prey swimmers divide. Predators ride and consume them. An evasion allele flips the sign of the predator's effect. | noise | `threads/chemotaxis-motility/packs/evopursuit` |
| | `swimfission` | L6[L2]+L4b (medium) | Front-fed swimmers lengthen past the attractant range and pinch into near-equal daughters. Strict gen 3/3/3, holds at dt/2. | noise | `threads/chemotaxis-motility/packs/swimfission` |
| | `kstrail` | L4b[L2] (high) | A slow self-secreted repellent turns KS aggregates into crescent swimmers (route: spot, ring, rupture, crescent). Validated at 2x resolution. | noise | `threads/chemotaxis-motility/packs/kstrail` |
| lenia-multichannel (nonlocal kernels) | `mcf-MIRd` | L6[L2]+L4c (high) | Chan's planted MIRd+ replicator, which can build matter only from a regrowing food field. Without refill it goes extinct in 3/3 seeds. | planted (known creature) | `threads/lenia-multichannel/packs/mcf-MIRd` |
| | `mcfd-MIRd` | L6[L2]+L4c+L5 (medium) | Adds maintenance decay. Turnover 0 / 0.01 / 0.03 gives a dormant lattice / a fed static lattice / intermittent boom-bust. | planted | `threads/lenia-multichannel/packs/mcfd-MIRd` |
| | `r-two56` | L3 (high) | 2 of 420 random 2-channel rules. Static shelled "cog" cells from noise, whose shell sits at a set distance set by a ring kernel. Converged at dt/2 and R=15/20. | noise | `threads/lenia-multichannel/packs/r-two56` |
| flow-lenia (mass-conserving Lenia) | `fl_forager` | L6[L2]+L4b (medium) | One noise patch becomes 8-14 crescent gliders. They eat a conserved, Hill-gated food field, carve wakes and divide. Matter plus food is conserved to 8e-12. | noise | `threads/flow-lenia/packs/fl_forager` |
| | `fl_cells` | L4a[L3] (medium) | Static three-layer cells that re-form core, ring and crown after 38-44% cuts. | planted | `threads/flow-lenia/packs/fl_cells_damage` |
| fisim-beyond-laplacian (PhySim genome) | `xcell-a` | L4b[L3] (medium) | Unmodified m4 gliders carry a membrane ring. The ring gates a fast cargo: 1.24 vs 0.43 at the centre, dt-converged. | planted | `threads/fisim-beyond-laplacian/packs/xcell-a` |
| | `xcell-evo2-S/N` | L6[L3] (low); L7 Contradicted | Membrane cells divide under imposed dilution, reaching gen 6 in one run. Marks that arise in the run never breed true. | planted | `threads/fisim-beyond-laplacian/packs/xcell-evo2-S` |
| | `xcell-her` | L3 (high) | Planted bistable-marker kinds breed true in 46/46 divisions. The gate is necessary: beta_h=0 erases every on-lineage. Holds only in this genome and division regime. | planted | `threads/fisim-beyond-laplacian/packs/xcell-her` |
| particle-life (particles, chemistry) | `sporecell3-det` | L2 (high); L6[L2] Weak | Catalytic particle cells with exact matter-identity lineage. At a step-safe integrator step, births need a written detachment rule and stop at confluence. | noise | `threads/particle-life/packs/sporecell3-det` |
| | `sporecell2-lysis` | L5[L2] (low, non-converged dt map) | A written contact-kill rule reverses the competitive outcome in 3/3 matched seeds. | planted kinds | `threads/particle-life/screens/P_half_types.png` (no pack) |

**The lab's highest rungs:**

- **L7:** autopoiesis `membrane_evo` L7[L3] low; active-droplets `ad5-evolve` L7[L2] low.
- **L6[L3]:** `phase_membrane` (medium, from noise); the ad7 family (medium, planted);
  `xcell-evo2`, `ad3-membrane` and `membrane_kinds` (all low).
- **L6[L2], high:** `phase_protocell_noise`, `mcf-MIRd`, `ad1-fuel`.
- **L5:** `evopursuit` L5[L2]+L4b high.
- **L4b, high:** `kstrail`, `pursuit`.
- **L3, high:** `r-two56`, `xcell-her`, `xcell-div`.

**What no thread reached:**

- L7 at medium or high confidence.
- L7 carried by births the cells make on their own: both L7 rows depend on imposed
  disturbance or on colonization.
- L8 (open-endedness), which nobody attempted.
- A world that combines a material membrane, self-propulsion and reproduction. Swimmers
  are L3 Weak or Contradicted, and the organized cells that move do not divide.
- Spontaneous replication in Lenia: 0 of 150 screened rules.
- L4c under the v2 tests. The only Supported L4c rows are the lenia build-from-food worlds,
  scored in sprint 1 under v1, and every requested starvation fork or local supply cut went
  unrun.
- Any intrinsic death in the PhySim-style (m4) cells.

---

## 3. Beyond diffusion

**How it was scored.** The rubric's beyond-diffusion modifier (0-3) is capped at 1 unless
a *matched Laplacian-only control* fails where the world succeeds. In that control the
non-diffusive operator is replaced by linear diffusion at comparable rates. The lab learned
that choosing "comparable rates" is itself a design problem. A gate that holds a fast
species inside a body has to be compared against a *uniformly slower* diffusion, not
against the same fast D with the gate off. In the r3 ruling, a control counts only in the
regime where the world succeeds. Across all 21 reviews, the only score above 1 was
active-droplets r2: "1 for the family, 2 provisional for the landscape".

**Non-diffusive operators that did work.** Most entries compare against the world's own
ablated operator, not against a true Laplacian-only twin. The last column says which.

| Operator | Where | Evidence | Status |
|---|---|---|---|
| Gated mobility at a self-made boundary, div(D e^{-beta m} grad c), or phi^2 gating | fisim `xcell-a`/`xcell-her`; active-droplets `ad7`; autopoiesis | xcell-a centre cargo 1.24 vs 0.43 with the gate off (dt-converged). beta_h=0 erases every planted on-lineage (3 judges). ad7: bc=0 gives 3 vs 12 droplets, bu=0 gives 12 vs 6 (1 seed each). autopoiesis gate=0: all dead by t≈350-400. | Works against ungated diffusion at the same D. No uniformly-lowered-D control exists where it works (fisim beyond-diffusion: 1). |
| Cahn-Hilliard in place of linear diffusion, inside the gated droplet | `ad7` R arm | With linear diffusion at D=M, kp=0.5 gives 5 spots that essentially do not divide, against 12 dividing droplets with CH. kp=4: 6 vs 6. | The lab's only true Laplacian control to fail, but 1 seed and D=M only (CH bulk diffusivity is 2M). The 3-seed D=M/2M replication was never run. |
| Wall-adsorption drift chi up grad[4phi(1-phi)] | autopoiesis `phase_membrane` | Matched chi=0 control (same grid, seeds, duration): rim/core 1.51-1.72 drops to 1.12-1.14; 15-17 vs 42-43 cells; 9-12 vs 26-32 persistent splits. | The ring does work, setting size and division rate. It is not needed for viability. Credited under mechanism. |
| Allen-Cahn wall tilted by the cell's own product | autopoiesis | a=0: domains shrink by curvature and all die by t≈350. | Researcher's ablation; not re-run by the committee. |
| Min (not arithmetic) face mean, plus decay outside bodies | autopoiesis `membrane_evo` | An arithmetic gate leaked 0.5 on every boundary face (conversions > mutations in 6/6 seeds). Sealed: conversions ≤ flips in 30/30 runs. | Supported. A discretization choice decided whether heredity worked. |
| Pressure term -alpha grad A; Hill-gated uptake | flow-lenia `fl_cells`, `fl_forager` | Without pressure, the ring breaks into dots. Linear uptake gives "grey goo" tiling the grid. | Within-family only; capped at 1. |
| Ring-kernel set-point membrane | lenia `r-two56` | Knocking out k4, k5 or k0 removes the shell, kills the core, or gives endless worms. | No DoG or Laplacian control; the r3 review calls it "the thread's only route to a beyond-diffusion score". |
| Slow self-secreted repellent (advective trail) | chemotaxis `kstrail` | chi_h=0 gives 30-60 static spots. | The Laplacian-only slow-inhibitor twin was requested in all 3 sprints and never run (it is the known drift bifurcation, Krischer & Mikhailov 1994). Score 1. |
| Non-reciprocal cross-taxis | chemotaxis `pursuit` | Without pursuit, contact falls to chance (0.58 vs null 0.58). Without evasion, predators are carried inside prey. | Within-model; underlies L5 high in evopursuit. |

**What turned out not to matter, or could be replaced:**

- **Cahn-Hilliard in `ad1-fuel`.** Two judges replaced CH with linear diffusion
  (D=0.015 with the double well removed; Dv=M=0.03), and the droplets still hollowed out
  and divided. At D=0.06 they did not. The committee called it "Gray-Scott mitosis in a CH
  body". Core-starvation fission needs only low body diffusivity plus cooperative c^2
  production. The ad3 amphiphile drift also rings plain RD spots without CH (rim/core
  1.6 vs ~3), and the ad3 shell was inert until ad7 gave it a job.
- **Lenia's metabolism.** Build-from-food plus decay has the structure of a Gray-Scott
  chemostat. The boom-bust is generic consumer-resource ecology, and the kernel only
  supplies the individuals.
- **Division in fisim.** In `xcell-div`, turning the gate off still leaves 8 splits
  against 13-15, so division is Gray-Scott-class. CH broadens the membrane (8 vs 3 px)
  rather than sharpening it.
- **Sharpness alone.** fisim's sprint-1 screens made fronts sharper with taxis
  (1.37 px vs 3.39) and porous diffusion (2.39 px). Ring kernels gave Turing tilings. In
  every case the individuals were lost: collapse to one spot, or space filling.
- **Membrane-gated food mobility in particle-life.** Rings stayed only on the founders,
  and every daughter was bare (L6[L3] Contradicted).

**Operators that transfer, with their conditions:**

1. **Gated mobility at boundaries.** It needs a min or harmonic face mean, because the
   arithmetic mean leaks. At 1-2 px width the grid sets the barrier's strength: in ad7,
   kp=4 area fell 30% at dx=0.5, and the harmonic mean changed fitness, not just the
   profile.
2. **Allen-Cahn walls held up by the cell's own product.** Adding phi^2-gated mobility
   gives a container that cannot have a hole, repairs itself by curvature flow, and
   divides by starvation. Cell size against feed is a clean law: 71/66/88/405 px at
   F=0.0054-0.008. The tilt and the chi drift were sent to fisim as genome operators in r1
   but were never implemented there.
3. **Self-repellent trails for propulsion.** One added field makes an aggregating
   advective field swim. The conditions: bodies must be unsaturated, the volume-filling
   face flux must be conservative (van Leer MUSCL), and bodies need radius ≥6 px, or the
   heading locks to the grid and up to 80% of mass is lost. A toxic trail acts as a
   homeostat that keeps a motile phase alive.
4. **Consumed regrowing resources with maintenance costs.**
   - Build-from-food plus decay has three regimes and a sharp turnover threshold (0.025
     gives a static lattice, 0.03 gives boom-bust).
   - The conserved, Hill-gated food in fl_forager gives growth-division cycles without a
     global cap.
   - Across threads, selection acted only where there was turnover.
5. **Mass conservation.** Reintegration tracking holds mass to about 1e-12 and gives
   bounded bodies for almost any rule. Check convergence by changing resolution, not dt:
   the scheme adds numerical diffusion. An exact food plus matter ledger is a ready-made
   hidden law for an agent to find.
6. **Identity-carrying particles and matter.**
   - Catalytic provenance labels give exact lineage (particle-life).
   - Genes can ride on parcels (flow-lenia).
   - A trait carried on the body's own transport, q=a*trait, makes conversions impossible
     by construction: ad9 had 0 conversions in 12/12 runs.

   Passive tags on built matter leak wherever bodies touch: lenia had 47% pure divisions.

**What this means for the PhySim genome.**

`threads/fisim-beyond-laplacian/XGENOME_SPEC.md` (reference stepper `xgenome.py`) already
defines optional blobkit keys. Each key vanishes identically at the vacuum for any
coefficient:

| Key | Term or role |
|---|---|
| `band` | front-deposited membrane drive, 4s(1-s) |
| `ch` | Cahn-Hilliard term, with k grad^4 in the exact Fourier step |
| `perm` | gated diffusion, with named channels such as `["c","m",5]` |
| `kern`, `taxis`, `porous`, `adv` | screened alternatives |

A genome without these keys reproduces m4 to 3.8e-14 after 1000 steps. The numerics stay
at blobkit's dx 0.5, dt 0.02, with a CH stability note.

Our recommendations:

- **(a)** Make `perm` first-class and give it a face-mean option (min or harmonic).
- **(b)** Add the autopoietic tilt a(L-theta) and the chi adsorption drift.
- **(c)** Add a build-from-food or maintenance term whose cost is extensive and is split
  at division. fisim showed that concentration-type waste never kills m4 dissipative
  solitons, which is why every death in xcell-evo2 had to be imposed.
- **(d)** Add a conservative advection operator (reintegration tracking or MUSCL
  volume-filling flux) for motility.
- **(e)** Add matter-carried labels that are confined by construction.
- **(f)** Declare world-level stochastic events (kicks, disk erasure) in META. Today they
  live outside the genome.

Good discovery worlds already exist:

- `xcell-her`: one beta switches heredity on and off;
- `evopursuit`: the sign flip;
- `fl_forager`: the exact ledger;
- `mcfd-MIRd`: three regimes and a threshold;
- `phase_membrane`: cell size against feed;
- `ad7`: the interior optimum with a signature in two ablations.

---

## 4. Question 1: can we write rules for a judge?

**Yes.** The rubric we used is a usable specification. The evidence says it needs an
adversarial, re-running judge, not a reader of metrics.

### 4.1 What the rubric looks like (`RUBRIC.md`, v2)

**The ladder (L0-L8).** Inert, pattern, individuals, organized individuals, autonomy
(a: repair, b: propulsion, c: metabolism), interaction, reproduction, heredity with
selection, open-endedness.

- Each rung has an evidence rule, typical screens and common false positives.
- A claim is qualified by the rung of its individuals: `L4b[L3]` is a self-propelled,
  membrane-bounded individual.
- For each claimed rung, and the one below it, the judge writes a gate verdict:
  Supported, Weak, Contradicted or Not tested. Each verdict names one observation and one
  limitation.

**Seven modifiers (0-3).** Spontaneity, robustness, numerical validity, novelty,
mechanistic insight, beyond-diffusion leverage, PhySim potential. They are never averaged
into the rung.

**Promise (1-10).** A holistic estimate of what the next sprint is worth. It drove
funding. Promise trajectories:

| Thread | Promise by sprint |
|---|---|
| autopoiesis | 8, 6, 6 |
| chemotaxis-motility | 7, 8, 7 |
| active-droplets | 7, 7, 6 |
| flow-lenia | 7, 6, 5 |
| lenia-multichannel | 6, 5, 4 |
| fisim-beyond-laplacian | 6, 5, 4 |
| particle-life | 6, 5, 3 |

All seven r3 decisions were STOP because sprint 3 was the last, so promise is the
informative number.

**Procedure.**

- Look at the sheet before reading any numbers.
- Calibrate against four control packs in `examples/packs/`: Orbium ≈ L4b[L2],
  Gray-Scott mitosis ≈ L6[L2], Particle Lenia ≈ L3, noise ≈ L0/L1.
- Re-run at least one pack.
- Anti-Goodhart rules apply: no rung from metrics alone, claims from a single seed are
  capped at Weak, and the researcher's prose is not evidence.

**Lenses.** Each report was read by a biologist (rungs from images), a physicist-skeptic
(numerics, triviality, reruns) and a curator (novelty, operators, PhySim value). A director
arbitrated, funded and cross-pollinated.

### 4.2 What the judges caught

| Kind | Examples (thread, sprint) |
|---|---|
| Code bugs | fisim r1: `perm [6,3,5.0]` gated waste by *cargo*, not membrane, and every founder was planted with waste q=1.2. With the documented gate the world dies by t≈32, and `xcell-turn` (then the family's only L6 Supported) was retracted. Also: particle-life `lineage.py` ratcheted generations ("gen 3-9" withdrawn); chemotaxis `preytrack.py` credited merge products as daughters; `fission.py`'s max()-through-merge rule inflated depth (claimed 4/3/5, strict 3/3/3); fisim counted cells that straddle the periodic boundary twice. |
| Numerical artifacts | particle-life r2: per-step displacement 1.2-1.37 > r_max=1 at dt=0.02, so spore emission was overshoot. The step-safe control in r3 dropped free spores from 127 to 3.4. Flow-Lenia: dt/2 doubles numerical diffusion under reintegration tracking, so it is not a convergence test. The fl_cells beaded crown was numerical. ad7's shell width is set by the grid. |
| Sign flips under matched controls | chemotaxis `ecology`: the researcher's -24% prey effect came from mismatched grids; matched, it was -7% with predators vs -35% without. `evopursuit` "rescue from predation" was contradicted by the prey masses. `fl_predator`: the prey-only arm was not mass-matched (+274 prey ≈ 277 units of predator mass). |
| Contagion and label leakage posing as selection | autopoiesis `phase_kinds`: 45 intact cells converted against 8 mutations, and the sweep happened with mutation off. `membrane_kinds`: an arithmetic face-mean leak. lenia `mca`: 7-15 gross conversions vs 1 mutation. flow-lenia gene2: within-body somatic turnover, 0 deaths in 13/15 runs. ad5/ad7: patch flips outnumber births (9 vs 6; ~40 vs 6-9). |
| Unmatched or null controls | ad5 neutral at k=0.13 vs ancestor 0.10, and the matched neutral showed the ancestor is sterile. lenia's L4c ablation ran on the parent world. particle-life's lysis arms drew random numbers conditionally, so they diverged before contact. autopoiesis arm C was null by construction (a sub-majority patch in a deterministic PDE). fisim's gate-off kept D=4. |
| Triviality | ad1 is Gray-Scott in a CH body. mcfd is a Gray-Scott chemostat. `r-two-s1-60` is the known single-channel C-glider (exposed by a constant-k5 ablation). kstrail is a known drift bifurcation. |
| Arithmetic and statistics | flow-lenia p = 0.021, not 0.008. ad7 neutral share 12/21, not 9/21. chemotaxis counted daughters, so "46 births" was 23 events (0.8x conversions, not 1.6x). ad9 counted planted disks separating as births, inflating the landscape, so "broad optimum" was withdrawn. swimfission's "strict" strips were byte-identical (md5) to the r2 founder strips. |
| Wrong mechanisms | fisim: the marker is stranded in the neck as the body glides out from under it; it does not "retreat to a pole". autopoiesis: the high-yield sweep runs through disk-cut fragments (43/43 on seed 11), not because "larger cells divide more". flow-lenia: "fusion spreads the gene" is a bookkeeping artefact (r(between, fusion) = -0.90). chemotaxis: B wins by retention under consumption (5.8-6.2x), not by "exploiting the chase". |
| Committee mutation design (and committee error) | lenia r2: the mutation operator flipped 1-19 px halo dots (13/18 events), because the committee's own r1 wording, "a connected A0 component", invited it. L7 was reclassified as Not tested. |
| Under-claims (upgrades) | `phase_membrane` raised to L6[L3]. r-two56 is better converged than reported. `xcell-evo2` L6[L3] from the biologist's merge-aware tracker. mcfd fissions recovered by a dense re-simulation after labkit read gen 0. The ad9 fecundity signal (kp=1.5 mutants 11 births vs 5.6 expected, p≈0.018) was found post hoc in the researcher's own ledgers. |

### 4.3 How the rubric changed from v1 to v2, and why

All seven sprint-1 directors raised rubric issues (31 in total). Rubric v2 (17:45 UTC)
adopted 16 rule changes, each tied to a named counterexample
(`committee/RUBRIC_CHANGES.md`):

- **L3 boundaries.** The layer must be in a *material* channel. A contour such as
  4phi(1-phi), or a band readout of the body, is capped at Weak unless an ablation shows it
  does work. A self-made interface layer counts. A layer set by the environment and lost
  population-wide is Weak. Boundary features of 1-2 px in kernel worlds must survive a
  ≥1.5x resolution continuation.
- **L4a repair.** Damage a mature, non-dividing individual, keep a branched undamaged twin,
  use ≥2 seeds, move debris out of the individual's reach, and report the fraction
  actually erased.
- **L4c metabolism.** Cutting a global feed is not enough. Require a fork in which
  individuals die, a local supply cut, or a per-individual flux budget, run on the world
  claimed.
- **L5 interaction.** Controls must be matched, and the sign of the effect on each partner
  reported. A "cycle" needs peak spacing across 3 seeds and a grid-size check.
- **L6 reproduction.**
  - From planted founders, gen ≥3; from founders formed in noise, gen ≥2.
  - When merges exceed 50% of splits, confidence is capped at medium.
  - Lineage must be merge-aware, with birth strips at the deepest generation claimed.
- **L7 heredity and selection.**
  - Kinds may change only at mutation or birth, and conversions are reported per mutation.
  - Variation must arise during the run.
  - The neutral arm is ancestor-matched, ideally an identical-event twin.
  - Report per-kind births, deaths, flips and off-kind daughters.
  - Colonization-only selection is capped at low confidence.
- **Modifiers.** Beyond-diffusion ≥2 needs a matched Laplacian control that fails.
  Flow-Lenia convergence is tested by changing resolution. Populations that churn can rest
  L2 on body lifetime between collisions.

labkit v0.2 added the measurements these rules need: per-channel radial profiles, an
absolute lineage window with a re-merge filter, damage aimed at mature individuals, and
per-species tracking.

### 4.4 Remaining failure modes

1. **The rubric stopped at v2.** Reviews r2 and r3 raised 63 further rubric issues, and
   none was folded into a v3. Among them:
   - birth cause (disturbance-mediated vs spontaneous);
   - a pre-registered power estimate for L7 (births x p_mut, Moran fixation odds);
   - gross and net conversions in both directions;
   - persistence windows stated in t;
   - mutation footprint relative to body size;
   - Price splits that book fusion neutrally;
   - "no pack, no rung";
   - periodic-aware labels;
   - heredity scored at fixed lags after a split, not at the split frame;
   - a "(dt map)" flag for rungs on non-converged maps, requested in r2 and "still not in
     the rubric" in r3.

   Application drifted as a result. For example, the v1-era L4c Supported rows coexist
   with v2-era L4c Weak.
2. **Metric holes the judges had to work around by hand.**
   - labkit lineage used a window of 10% of the run, which read gen 0 on dividing
     colonies.
   - The radial band test fails a clean annulus that has a central dot, yet passes a
     one-sided cap.
   - The tracker breaks for swimmers and mixed species (796-1076 false nucleations in
     evopursuit).
   - Per-channel colour scales render channels at 1e-5 as if they were bodies.

   A judge that trusted the metrics would have been fooled in both directions.
3. **The judge also designed experiments, and sometimes got them wrong.**
   - Lenia's "connected A0 component" wording invited the halo-dot flips.
   - Autopoiesis arm E prescribed a death disk the size of a body, which then acted as a
     fission operator and a size filter.
   - Chemotaxis's "births far exceed conversions" criterion was mis-posed.
   - fisim's stop rule fired on the least diagnostic fix.
4. **Readiness and snapshot errors.**
   - Two final reviews ran on unfinished snapshots and were discarded.
   - Chemotaxis's provisional r3 record was written before the judges saw REPORT_r3.
   - Lenia's B5 result was committed 17 minutes before its review, which judged an earlier
     snapshot.
5. **Disagreement and judgment calls.** Some verdicts were split: ad9 L3, mature-damage
   L4a (2 of 3 judges Weak), and the biologist's dissent on xcell-a. Chairs overruled
   judges in both directions, and ad hoc qualifiers such as "near-Supported" appeared.
   Rungs at the margin depend on who is reviewing.
6. **Stale public records.** Several FINAL.md files contradict the consensus:
   - fl_predator listed as "near-Supported";
   - particle-life "converges in dt";
   - chemotaxis 1.6x;
   - autopoiesis L4a medium;
   - the ad9 row placed inside the ad7 family.

   The leaderboard also carries duplicate r2 and r3 rows.
7. **Cost.** The committee ran 21 reviews with 4 agents each, every judge read images, and
   the skeptic re-ran simulations. That cost about 386 USD against 219 for all seven
   researchers. Each review took 25-80 minutes.

### 4.5 Recommendations for a judge inside an automated evolutionary loop

1. **Tier the judge.**
   - Run labkit screens on every candidate. They are cheap, never award a rung, and act
     only as filters.
   - Run an image-first LLM judge, calibrated on the control packs, on candidates that
     pass the screens.
   - Run an adversarial skeptic before any candidate enters the elite archive at a new
     rung. It re-runs on a new seed, at dt/2 and at a resolution change, plus a matched
     ablation.

   Independent reruns caught more errors than any amount of reading.
2. **Make worlds carry their own controls.** Extend the world contract so META declares:
   - the claimed operator and a switch for its Laplacian replacement;
   - an identical-event neutral twin, with all random draws unconditional and taken from a
     state-independent stream;
   - numerics knobs for dt and resolution.

   The judge then runs controls mechanically instead of asking for them. Asked-for
   controls were the experiments least often delivered.
3. **Make worlds emit a ledger.** Each world should log births, deaths, merges, mutations
   and conversions with parent ids, merge-aware and periodic-aware. Every L6 and L7 error
   above was a bookkeeping error.
4. **Score into an archive, not a scalar.** Use niches of rung x individual-rung x
   spontaneity (MAP-Elites style). Let confidence weight the selection probability, and
   use novelty and mechanism as diversity pressure. Planted structure and rule accretion
   should cost (particle-life ended with seven hand-written rules).
5. **Pre-register L7 tests.** Fix the pass criteria and expected power before the run:
   mutant count, fixation odds, and births by cause (spontaneous vs disturbance) and by
   phase (colonization vs stationary).
6. **Expect Goodhart and defend against it.** An EA will find the metric holes listed in
   §4.4.2. Keep the rule that every rung needs a visual observation, treat any
   disagreement between metrics and images as a flag, and hold out seeds.
7. **Separate designer from judge.** Have committee-designed experiments checked by a
   second agent before they are funded.
8. **Keep one source of truth.** Use a versioned leaderboard JSON and update the rubric
   each round from counterexamples. Have researcher documents link to the record rather
   than restate it.

---

## 5. Question 2: is agent-driven mutation more expressive?

**Yes, structurally.** Every rung above L3 came from edits that change the form of the
equations, which a parameter-mutation EA cannot make. The cost is a low hit rate and gains
that came early. Most effort went into heredity, and those edits mostly failed.

### 5.1 What the researchers did

Each researcher kept a META.parent / META.mutation tree of single forkable `world.py`
files:

| Thread | Worlds | Edits that raised the thread's top rung (sprint) |
|---|---|---|
| lenia-multichannel | 28 | build-from-food (s1), maintenance decay (s1), random kernel screen (s1); no thread-level rung moved after r1 |
| autopoiesis | 24 | lattice SCL replaced by an Allen-Cahn wall tilted by own product (s1; ancestor of every rung-bearing world), chi adsorption drift (s1), sealed-channel arm E (s3) |
| active-droplets | 18 | consumed fuel with cooperative u c^2 and M 1→0.03 (s1), amphiphile drift (s1), confined alleles (s1), fisim gate forked onto the self-made shell (s2) |
| flow-lenia | 18 | conserved non-flowing food with a Hill gate on glider rule C2_r202 (s1); 0 of 5 heredity edits paid off |
| fisim-beyond-laplacian | 16 | band/CH membrane and perm gate (2 of 11 single-operator screens, s1); xcell-evo2 (s2, L6[L3] low) |
| particle-life | 14 | written contact lysis (s2, on a non-converged dt map), the only rung above L2 from about 13 edits |
| chemotaxis-motility | 12 | slow repellent trail (s1), Da 4→2 (s2), evasion allele plus predators (s2); 7 of 9 lineage nodes reached the leaderboard |

### 5.2 Structural edits a parameter EA could not make

| Kind of edit | Example | Result |
|---|---|---|
| Operator swap | autopoiesis: polymerized lattice membrane replaced by an Allen-Cahn domain wall whose double well is tilted by the cell's own product, plus phi^2 mobility | closure went from 0.2-0.8 (leaky) to walled dividing cells from noise, L6[L2] high |
| New field plus new conservation law | flow-lenia: a food field that diffuses but does not flow, with exact matter+food conservation | gliders became foragers that divide, L6[L2]+L4b |
| New constraint on growth | lenia: positive growth capped by local food at yield Y, then a decay term | L4c; three regimes; the free-dormancy law |
| New advective field | chemotaxis: a slow repellent h added to Keller-Segel; then trail toxicity, regrowing nutrient, non-reciprocal cross-taxis | spontaneous swimmers, then dividing swimmers, then L5 high |
| Cross-thread operator transplant | active-droplets ad7: fisim's gated diffusion acting on ad3's inert, self-made shell | the shell now does work, L6[L3] medium |
| Change of representation | ad9: trait carried as q=a*kp on the catalyst's own transport; particle-life: identity-carrying catalytic labels | conversions impossible by construction; exact lineage |
| Discretization edit | chemotaxis: MUSCL face flux; autopoiesis: min face gate | removed heading lock and 80% mass loss; sealed heredity |
| Diagnostic edit | particle-life: step-safe integrator with a k_det=0 control | falsified the thread's own reproduction mechanism |

Parameter steps mattered *after* a structural edit opened a regime: Da 4→2 gave
swimfission, M 1→0.03 made core starvation possible, and mu=1.5 near threshold gave
swimdiv. An EA could do that part.

Inside the lab, the closest analogue to a fixed EA was random rule search within one
family:

- **lenia:** of 420 random kernel graphs, ~10 gave individuals and 2 gave shelled cells.
  There were 0 cell replicators in 150, and 72% of fully random graphs were dead.
- **flow-lenia:** 2 of ~60 C=2 rules gave glider swarms, and 0 of 7 C=3 rules did.
- **particle-life:** a random asymmetric force matrix gave the known L3 shells.

None of these reached L6 without an equation edit. We did not run a head-to-head EA, so
this comparison is suggestive, not controlled.

### 5.3 Cross-thread forks

The committee logged about 120 cross-pollination pointers (`committee/CROSS_POLLINATION.md`),
and researchers recorded their forks in META.parent. Forks of **methods** paid off more
reliably than forks of **mechanisms**:

- **Paid off:**
  - Identical-event twins, from fisim, went to ad9, membrane_evo, sporecell3 and
    flow-lenia gene2.
  - Confined alleles, from ad5, went to chemotaxis swimevo/evopursuit, flow-lenia gene,
    lenia mcg and fisim's mutation patches.
  - The fisim gate went to ad7 and became active-droplets' best rung.
  - Toxforage went to autopoiesis motile_trait_tox.
- **Failed:**
  - Chemotaxis trail propulsion in an Allen-Cahn cell: a divergent local flow tears the
    wall.
  - Pursuit hunters: they starve in the prey's depletion halo.
  - Lenia maintenance decay in fisim: no intrinsic death.
  - Particle-life turnover: no setting passed.

A mechanism transferred when the receiving world had a slot waiting for it: ad3's shell
needed a job.

### 5.4 Where agent mutation struggled: heredity and selection

Every thread aimed at L7, and none reached it at medium confidence. The reasons are
physical, and they recur across threads:

1. **Field bodies do not own their matter.** Wherever bodies touch, a passive label is
   rebuilt by whichever body's field reaches it:
   - lenia: 47% pure allele-1 divisions;
   - autopoiesis and chemotaxis: conversions comparable to births;
   - flow-lenia: mosaic bodies with somatic turnover.

   Heredity worked only with confinement by construction: a min gate plus decay outside
   bodies, a trait carried on the body's own transport, or particle identity plus
   majority-vote conformity.
2. **No intrinsic death.**
   - m4 solitons never die.
   - Confluent lattices freeze in lenia, active-droplets, particle-life and autopoiesis.
   - The lenia thread stated the law that "selection needs turnover" (planted kinds froze
     at colonization frequencies in a lattice).
   - Imposed deaths then confounded the tests: the autopoiesis disk acted as fission
     operator and size filter.
3. **Mutation operators that do not fit the bodies.** Flips covered halo dots, half
   droplets, or discs larger than a median body (49 px against 35-47). The lenia
   "coverage law" says a mutant must replace about the whole body (≥0.9 of its mass) to
   persist.
4. **Power.** Runs had 6-40 bodies, 1-5 mutations and about 1 generation of turnover. The
   ad9 null was predictable from births x p_mut ≈ 1-3.
5. **Positive-control traits.** Uptake and growth-rate genes make selection true by
   construction. They test the machinery, not the biology.

The agents also showed typical failure patterns:

- headlines oversold relative to the evidence, and more than two dozen claims were
  downgraded;
- controls requested in several sprints went unrun, such as the Laplacian twins and the
  L4c forks;
- rules accreted, and tooling drift crept in (ad9);
- reports were incomplete (lenia's B5 coded but not reported).

They were also strong at honest negatives and self-correction. The researchers retracted
`xcell-turn`, reported particle-life's dt failure themselves, withdrew flow-lenia's L7,
and corrected the fisim headline in place.

---

## 6. Question 3: does scaling with teams work?

### 6.1 Organization

| Component | What it was |
|---|---|
| Coordinator | One session. It built labkit, the rubric, the charter and the briefs, launched the researchers, ran the committee and wrote this synthesis. |
| Researchers | 7 independent Claude Code cloud sessions, each with a 4-core container and its own branch (`claude/alife-<thread>`). They communicated only through git and committee messages. |
| Committee | One per sprint report: biologist, physicist-skeptic and curator, then a director who decided continue/pivot/merge/stop, set the next experiment and cross-pollination, and updated the leaderboard. 21 reviews, plus 2 discarded and re-run. |
| Other workflows | A literature scout (4 scouts plus a synthesizer) wrote `LITERATURE.md` (~1,660 lines). labkit v0.2 was built by an implementer with 2 adversarial verify/fix rounds. `committee/DIGEST_r1.md` broadcast results and named three convergences. |

Timeline (UTC):

| Time | Event |
|---|---|
| 14:25 | kit, rubric, charter and briefs pushed |
| 15:20-16:15 | sprint-1 reports |
| 15:49-17:45 | sprint-1 reviews |
| 16:45 | sprint 2 started on the researchers' own plans |
| 17:45 | rubric v2 |
| 17:45-19:40 | labkit v0.2 |
| 18:10-19:30 | sprint-2 reviews |
| 19:05-21:15 | sprint 3 and FINAL.md |
| 20:00-21:45 | final reviews |

### 6.2 What worked

- **Independent review with re-runs.** Every major error in §4.2 was found by a judge who
  re-ran a world or re-tabulated a ledger, not by reading prose.
- **Convergence across threads.** Three threads arrived independently at gated mobility,
  which made it credible as a general operator. The digest turned it into a lab-wide
  pointer.
- **Committee-designed experiments.** They produced the lab's best-controlled results:
  - autopoiesis arm E gave the only L7[L3];
  - the lenia branch-point assay gave the coverage law;
  - chemotaxis's 18 fixed-allele arms lifted L5 to high;
  - the flow-lenia Price audit gave the correct reading of its gene sweep.
- **Stop rules and time boxes.** They made negatives clean in fisim, lenia and
  particle-life.
- **Shared evidence packs and calibration controls.** These gave seven very different
  families a common currency, and judges could compare across threads.
- **Spend did not predict results.** Researcher cost ranged from 21 to 42.5 USD.
  active-droplets, the cheapest, holds L6[L3] and L7[L2]. lenia and autopoiesis cost the
  same: one stalled after r1, and the other produced the lab's only L7[L3].

### 6.3 What failed

1. **CPU bottleneck.** The committee shared 4 cores while judges re-ran simulations, with
   load average 11-18 and 25-80 minutes per review. The fix was that only the skeptic
   re-runs. It worked, but it reduced independent reproduction.
2. **Review latency.** Sprint-1 reviews reached researchers 60-105 minutes into sprint 2:
   particle-life at 17:37, lenia at about 17:45, autopoiesis at 18:11, chemotaxis at 18:16,
   active-droplets at 18:20, flow-lenia at 18:23. For active-droplets, chemotaxis and
   flow-lenia the sprint-2 work was already done. Commissioned experiments slipped a sprint
   or ran as cut-down first passes, and validation debt compounded. Decoupling sprint
   start from review delivery stopped researchers idling, but it meant review steered only
   every other sprint.
3. **Sprint timing.** "2-hour" sprints ended in 1-1.5 hours, and there were only three. In
   sprint 3 only autopoiesis raised its ceiling, and lenia and flow-lenia never moved up
   after sprint 1. L7 needs long runs with turnover, multiple seeds and matched twins,
   which takes more than one sprint.
4. **Merge and CI friction.** CI emailed a failure for every research push until lint was
   scoped. Importing thread directories at review time caused add/add conflicts. Full
   worktree mirrors were 2.4 GB each, replaced by `git archive`.
5. **Report readiness.** Watchers flagged drafts as ready, and two final reviews were
   discarded. A one-line readiness rule fixed it: REPORT_r3 plus FINAL.md, no
   placeholders, no "draft" commit, 10 quiet minutes.
6. **The digest relayed claims before review.** DIGEST_r1 (16:36) told every thread that
   autopoiesis and active-droplets had "met" the L7 bar and that particle-life reached
   3-9 generations. All three were later downgraded.
7. **Infrastructure lagged.** labkit v0.1's lineage window, rim metrics, damage targeting
   and species tracking were fixed only in sprint 2. Tracker gaps for propagules,
   swimmers and mixed species persisted to the end, and each thread wrote its own
   trackers, several of them buggy.
8. **Review cost more than research.** About 386 USD went to the coordinator and committee
   against 219 for the researchers.

### 6.4 Recommendations

- **Give review its own compute and budget it as the main cost.** Use a dedicated
  reproduction runner rather than the coordinator's 4 cores.
- **Use a short, blocking triage review** (15 minutes: claims, images, red flags) before
  the next sprint starts. Keep the full lens review asynchronous.
- **Make commissioned controls a condition of funding.** Carry unmet controls as visible
  "debt" on the leaderboard. A thread may not open new worlds while its debt exceeds a
  threshold.
- **Use fewer, longer sprints for heredity work.** Use breadth sprints for exploration.
- **Appoint a lab-engineer agent** who owns the shared ledger, lineage and tracker library
  between sprints. Merge thread directories once, at the end.
- **Digest only reviewed results.** Version the rubric every round. Generate FINAL.md
  tables from the leaderboard JSON.

---

## 7. Open problems and the next experiments to fund

Ranked by expected value per unit of compute. Designs are in each thread's r3 review,
under "What a future lab should do next".

1. **Make the lab's only L7[L3] autonomous (autopoiesis).** Replace the r=14 death disk
   with whole-body deaths chosen by identity from the state-independent RNG, at a matched
   per-body rate. Keep the twin, and run 10 seeds x {0.7b, b, 1.3b}. Classify every birth
   as spontaneous or disturbance-associated. Add an r_death sweep of 7/14/28. Pass: 1.3b
   sweeps through spontaneous births in ≥8/10 seeds.
2. **Close evopursuit's L7 (chemotaxis).** Use whole-body flips chosen by identity, an
   identical-event e=0 twin, and a fixed preytrack (no merge daughters, daughters ≥25% of
   parent mass and surviving ≥200 t). Count births per event and close the demographic
   budget. In the same sprint, run the Laplacian-only slow-inhibitor twin of kstrail,
   which has been owed for three sprints.
3. **Run the beyond-diffusion controls the lab never ran.**
   - ad7 R arm at D=M and D=2M on 3 seeds, plus a dx=0.5 anchor.
   - A DoG or Laplacian control for r-two56's set-point membrane.
   - A resolved, lowered-D Laplacian twin in the regime where xcell-her's gate works.

   These are cheap, and they answer the project's original question directly.
4. **Run a powered fixation test on the ad9 machinery (active-droplets).** Use 20
   identical-event S/N pairs at 128², with non-overlapping founders. Pre-register mutant
   fates (predicted 0.59 vs 0.17 fixation) and ship one pack.
5. **Endogenous death.** Build a conserved, extensive maintenance cost split at division,
   in the PhySim genome and in the CH droplets. Every run without imposed deaths froze
   into a lattice, and this blocks L7 everywhere.
6. **Emergent release from non-reciprocal forces (particle-life).** Run against an
   (A+Aᵀ)/2 symmetrized twin. This is the thread's untested beyond-diffusion lever.
7. **A body-level gene in Flow-Lenia.** Add an anti-fusion term, a gene that shapes the
   body (speed or size set-point), a per-component phenotype, and a branch-point assay in
   the glider regime.
8. **Heredity variable in fisim.** Test genome x division speed with planted marks. Try
   two rescues for the marker stranded in the neck: h taxis, and faster interior spread.
9. **Combined target.** A membrane-bounded swimmer that divides: an Allen-Cahn or psi
   shell plus a trail or a local phoretic drive. No world combines L3, L4b and L6.
10. **Lab infrastructure.** One merge-aware, periodic-aware, species-aware ledger and
    lineage library. A per-step maximum-displacement record. Kind overlays that keep the
    body plan visible. A radial band test placed at the profile trough.

---

## 8. Where everything is

| What | Path |
|---|---|
| Charter, rubric v2, literature | `CHARTER.md`, `RUBRIC.md`, `LITERATURE.md` |
| Rubric changes and their counterexamples | `committee/RUBRIC_CHANGES.md` |
| Leaderboard (58 rows; machine-readable copy) | `committee/LEADERBOARD.md`, `committee/leaderboard.json` |
| All 21 reviews (prose and JSON) | `committee/reviews/<thread>_r{1,2,3}.md` and `.json` |
| Sprint-1 digest; cross-pollination log | `committee/DIGEST_r1.md`; `committee/CROSS_POLLINATION.md` |
| Per thread: brief, notebook, reports, final | `threads/<thread>/{BRIEF,NOTEBOOK,REPORT_r1,REPORT_r2,REPORT_r3,FINAL}.md` (FINAL.md tables are partly superseded by r3; the leaderboard is authoritative) |
| Worlds (forkable, with META.parent) and packs | `threads/<thread>/worlds/<world>/world.py`; `threads/<thread>/packs/<world>/` |
| PhySim genome extension | `threads/fisim-beyond-laplacian/XGENOME_SPEC.md`, `xgenome.py` |
| Reusable assays | `threads/lenia-multichannel/tools/{branch_test,branch_states,division_ledger}.py`; `threads/autopoiesis/{evotrack,kindtrack}.py`; `threads/flow-lenia/scripts/audit_gene.py`; `threads/active-droplets/protocell_movie.py`; `threads/chemotaxis-motility/{fission,preytrack}.py` (both have the merge-daughter bug) |
| labkit (world contract, ops, metrics, packs) | `labkit/` (`python -m labkit.run <world.py> --out <dir> --seeds 0 1 2`); calibration packs in `examples/packs/` |

Judge working files cited in reviews as `judge-scratch/...` were not committed to this
branch.

**Showcase movies**, one per thread (`threads/<thread>/movies/showcase.mp4`):

| Thread | World shown | Rung | What it shows and the caveats |
|---|---|---|---|
| autopoiesis | `membrane_evo_up`, seed 4 | L7[L3] low | High-yield orange cells take over the area. The black disk deaths are the mechanism. |
| active-droplets | `ad7t-thick`, seed 1 | L6[L3] | Thin-rimmed green and yellow cells divide and fill the box. Two-colour cells are imposed patch relabels. Poster: `showcase_sheet.png`. |
| chemotaxis-motility | `evopursuit`, seed 0 | L5[L2]+L4b | Prey bodies go from A8/B7 at t=750 to A0/B45 at t=1450, with predators riding the crescents. It reads without explanation. |
| flow-lenia | `fl_predator` | L4b[L2], L5 Weak | Predator-prey Flow-Lenia, one seed; coexistence is a knife edge. The stronger world is fl_forager (`packs/fl_forager/seed1/sheet.png`). |
| lenia-multichannel | `mcfd-MIRd`, seed 2 | L6[L2]+L4c+L5 | Intermittent boom-bust of Chan's planted MIRd+ cells on food. |
| fisim-beyond-laplacian | `xcell-her`, seed 0 | L3 | Two planted kinds divide and breed true, then freeze into a lattice. |
| particle-life | `sporecell2-gate` | L2 | The thread's most life-like image, but its spore burst is integrator overshoot. Poster: `showcase_frame.png`. |
