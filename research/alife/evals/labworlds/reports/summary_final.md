# PhySim ALife collective: project summary at the 28 Oct pause

Paths are relative to `/home/user/physim/research/alife`. Contribution ids live under `collective/contrib/<id>/`. Figures come from the last import: librarian commit e8818f1c6 at 2026-10-28T10:25:54Z (`collective/STATE.md`, `ledger.json`, `progress.json`). Nothing was re-run. Three fact-checks compared the draft with the repository, the librarian worktree and its git history (`/home/user/librarian`), `/home/user/librarian.log` and the cited contributions. Where they disagreed, I opened the source myself. That included running build.py's own tally read-only in memory.

## 1. What was built and what came out of it

Phase 1 (24 Oct, 14:03–21:45Z) ran 7 research threads judged by a Program Committee (`CHARTER.md`, `RUBRIC.md`, `REPORT.md`). It left 83 seed entries the committee had judged. Phase 2 (Oct 25–28) replaced the threads and the committee with a shared ledger. Sixty-four remote agent sessions (c01–c64, about 5.5 h each) and the operator, c00, published 2389 contributions using 921.4 CPU hours. A librarian (`collective/build.py`, `sync.sh`) decided each claim from independent re-runs and scored the results. By the pause, 8 of 11 grand challenges were met, each with at least one audited holder:

- cells that swim and divide from noise, with and without a beyond-diffusion test;
- swimmers whose self-made wall holds a cargo;
- containment that daughters inherit through division;
- heredity with selection driven by intrinsic deaths;
- reproduction that a diffusion-only twin cannot match;
- dividing cells that live on a consumed, regrowing fuel;
- crawlers that repair their polarity.

Reach rose from 38 to 122 capability sets. Much of the value is in the corrections. Audits left 9 established claims disputed, though STATE.md shows only 6. After the launch the operator changed the rules or the librarian 24 times (23 not counting a history replay), most often in response to a concrete failure. Three challenges remain open: ecology with metabolism, open-ended novelty, and a spreading swimmer minority. Reach has been 122 since 15:13Z Oct 26, apart from 12:26–15:19Z Oct 27, when it stood at 130 while c52's ecology briefly met IXDE.

**Capability letters** (`collective/SCORE.md`):

| Letter | Capability |
|---|---|
| I | discrete, persistent individuals |
| B | an organized individual: a material boundary layer or differentiated parts |
| W | containment: a species with its own transport held inside (or kept out) at 2x or more across the wall for most of the body's life, lost when the wall is ablated, and surviving a 1.5x grid |
| R | repair |
| M | self-propulsion |
| E | metabolism: the body consumes a resource it depends on |
| X | interaction that changes population dynamics |
| D | reproduction |
| H | heredity with selection |
| O | open-ended novelty |
| S | forms spontaneously from a start that is unstructured over the whole domain (a localized seed counts as planted) |
| (BD) | beyond diffusion: a matched Laplacian-only twin fails where the world succeeds |

A reviewer whose review counts can mark a capability "by construction" when the code imposes it. Examples are curvature-flow repair, metabolism from an open feed or build-from-food, and cargo that is still held after the wall-off control removes the wall. One mark keeps the capability out of the score. The work is credited in K instead, and a later audit that names its deciding control can lift the mark.

## 2. How the collective works

**Why it replaced the threads.** `collective/RETRO_lab1.md` lists nine lessons. Its headline: one broadcast, the 16:36 digest, produced 15 of the lab's 22 cross-thread forks, and there was no second aggregation. Among the other lessons:

- Only 13 of 89 cross-thread suggestions (15%) were acted on, and all 13 arrived inside the target thread's own review.
- Review latency was the bottleneck.
- Tool pointers were reused 0 of 9 times.
- The digest spread an L7 claim and a generation count that were later withdrawn.

**Agents.** Each agent ran a loop: sync, take a `QUEUE.md` assignment, announce an intent, work 45–90 min, publish one contribution, push. Sessions had a 6 h lease (6 h 10 min in build.py). Agents could not edit generated files or published contributions, and contributions about the collective's own process were forbidden.

**Librarian.** Every 180 s it imported all agent branches and rebuilt STATE.md, QUEUE.md, ledger.json and progress.json. It pushed when something changed, and otherwise every 30 minutes.

**How claims are decided.**
- A review counts only if its own directory holds a labkit re-run on a seed the claim did not use. It then counts whatever it found, so a failed re-run is evidence against the claim. A Supported review whose reported seeds mostly fail is not counted. Only each reviewer's latest review counts.
- A capability is held when:
  - at least 2 reviewers support it. The bar is 3 when the claim has 4 or more capabilities besides S, or a capability nobody has established; S needs one more;
  - for W, R, E, X and H, a supporter points to a gate-control file;
  - supporters outnumber dissenters. A Contradicted review counts twice. A capability that a Weak or Contradicted review lists as observed does not count against;
  - with 3 or more capabilities besides S, supporters confirm they appear on the same tracked individuals;
  - the claim's packs cover at least 2 seeds.
- Reviews by the claim's author are ignored, and reviewers on the claim's code lineage count as one opinion. Reviewers may mark a capability as by construction. Audits can reject supporting reviews (`support_rejected`) or marks (`bc_rejected`).

**Score.**
- P: distinct capability subsets reached by established claims.
- P_BD: the same count over diffusion-tested claims, only for subsets containing a capability the twin lost.
- Q: breadth, the number of dynamical classes reaching each diffusion-tested subset, capped at 3 and summed.
- K: established mechanism findings and laws.
- C: corrections, meaning contradicted claims plus established negative findings.

**Challenges and audits.** Grand challenges (`collective/seed/challenges.json`) head the open tasks. An agent reaches the open tasks only after its campaign, a due synthesis, an audit (at most 2 running), a due literature check, a review, and its exploration focus. Since 4ae9625c9, every established Phase-2 claim that meets a challenge, holds 4 or more capabilities besides S, or is diffusion-tested gets one audit. Lab-1 seed claims are never audited. An audit uses two lenses: reading the code line by line plus one deciding control, and replication on unused seeds. The operator c00 also audited from outside the collective: 10 of the 27 audits are its own, and build.py treats every c00 review as an audit.

**How the rules changed.** From the v2 launch (a03d4cb72, Oct 25 05:46Z) to f438d2635 (Oct 27 18:11Z), the operator made 24 more rule and librarian commits (23 without the history replay 447c6f810), and SCORE_VERSION went from 2 to 8. Most answered a concrete failure. Some added features: literature checks (5f80011fc), assignment release (e5d2651b2), successor challenges after a success (8f626abf7), and rule announcements (5d3472d60).

- **Oct 25 morning: mechanics.**
  - Re-runs became mandatory and gate controls had to be files.
  - Single-seed claims hold only S and I.
  - d601b77ef fixed a lineage discount that had "collapsed all supporting reviews of a claim into one".
- **Oct 25 13:32Z (97cb38ce6): failed re-runs count against a claim.** Dropping them had been "biasing the ledger toward establishment".
- **Oct 25 15:00Z (172279226):** a claim names its grand challenge through its `C:` task.
- **Oct 25 16:58–17:21Z: prompted by c00's audit `20261025T1715-c00-audit-nematic-ringed`, imported at 17:19Z.** 563065c74 (16:58Z) cites the audit's findings before it was published.
  - labkit's `--dt` only relabels time, so a dt/2 test must change the world's own time step.
  - A passive boundary layer must be made by the body.
  - Audits were added (4ae9625c9) because reviews "rarely read the code".
- **Oct 26: per-capability rules.**
  - Beyond-diffusion credit. db3b5c3ac counted a capability only when most twin reviewers named it. Three minutes later a70023430 restored the union of the capabilities each reviewer names, with a bare `true` covering only what that reviewer supported.
  - W needs a wall-off arm (54838cf09). The same commit made by-construction marks count only from counted reviews and let audits lift them. dd8ab200b added the coupling-off arm.
  - M is measured along the axis of travel, audits can reject supporting reviews through `support_rejected`, and lineage counts only authors of code-bearing ancestors (958979b6c).
  - QUEUE announces rule changes (5d3472d60).
  - Capabilities shown by only a minority of bodies (B, W, R, M or E) may be held, with no fixed thresholds (225b47876, 27e2fe141).
- **Oct 27 18:11Z (f438d2635): RUBRIC L4c "consumption, not presence".** It also added an optional supply-threshold control. No rule file changed after this.

**Where code and documents disagree** (checked in build.py, sync.sh and the git log):
- QUEUE's rule notice (5d3472d60, 13:41Z Oct 26) reads only PROTOCOL, SCORE and RUBRIC. All build.py-only changes (5401c4439, 5e632c8b2, e78eab676, d601b77ef, e3b057c8a, f6fad9123) came before it, when nothing was announced. build.py has not changed since then.
- Several behaviours exist only in code:
  - the 3-review floor when a claim could add more than 8 new subsets;
  - thresholds that count capabilities besides S;
  - lineage reviewers collapsed to one opinion, where SCORE.md bars them;
  - the effect of the `necessary`/`law` flags on K, K's deduplication by (operator, capability, world), and Q's dependence on `class_confirmed` (the fields themselves appear in PROTOCOL's templates);
  - C counting a contradicted claim only if it was once supported;
  - a canary false-support check that `sync.sh` never turns on.
- RUBRIC.md still says v2, and `committee/RUBRIC_CHANGES.md` lacks the L4c change.

## 3. What it found

### The 8 met grand challenges

**reproduction-beyond-diffusion (IBD, BD).** First met at 07:55Z Oct 25 by lab-1 `phase_membrane` (`lab1-autopoiesis-phase-membrane#c1`, class phase-field).
- **World:** Allen-Cahn cells whose wall is held up by "link" molecules their own catalyst makes. Mobility is gated by φ², links drift onto the wall as a ring 2.1–2.5x the core, and cells divide by central starvation.
- **Deciding control:** c01's uniform-D twin (`20261025T0731-c01-phase-membrane-bd-twin`). At λ=0.1 the twin still divides (26 persistent splits), but its ring is 1.16, against 2.29–2.37 in the world. So the twin loses B, not D.
- **Caveats:**
  - The only beyond-diffusion vote is `20261025T0748-c01-review-phase-membrane-bd` (bd [B]), written by the agent who built the twin.
  - At λ=0.001 the twin keeps a 1.93 ring at 1x and fails only at 2x.
  - `threads/autopoiesis/FINAL.md`: the χ=0 control "forms and divides just as well", so the ring is not load-bearing.
  - STATE.md marks this holder "lab 1 committee"; it was never audited.
- **Other holders:** c15's fuel-cell rods held the challenge 15:18–20:42Z Oct 25, until audits. c34 nematic-cargo (zeta=0 twin: 0 splits) is the audited holder.

**autonomous-heredity (SIBDH, must name the challenge).** Holders: `20261025T1345-c14-pcell-mwall-claim#c1` and its b42 variant (class hybrid-particle-field).
- **World:** about 10⁴ identity-carrying Brownian catalyst particles inside the Allen-Cahn cells. Each particle carries a heritable link yield that mutates when it duplicates. A cell whose yield drifts low loses its phase and dissolves; nothing imposes the deaths.
- **Result (claim):** mean yield rises 1.00→1.16–1.18, while an inert marker ends at 0.95–1.02 (4 of 4 seeds). In the raw genealogy, deaths fall at the 1st–6th yield percentile, against the marker's 39th–54th.
- **Deciding control:** a neutral-trait twin. In `20261025T1940-c21-audit-b42`, on fresh seeds 10–11, the twin gives yield minus marker of −0.02/+0.07 with 0 splits and 0 deaths. The b42 world on the same seeds gives +0.17/+0.17. c00's audit of the base claim ran its twin on one seed only.
- **Caveats:**
  - `20261025T1715-c00-audit-pcell-mwall`: a remnant artefact (MINP=20) inflates death counts about 2x (c21: 1.3–2.8x), so the birth-rank statistics do not survive. About half the yield rise comes from faster growth of high-yield cells. Yield-biased deaths do survive remnant-aware recounts (c21: percentile 0.004–0.018 on 7/7 seeds).
  - In b42, D exists only because the trait evolves, and 78 of 82 mature deaths are founders that never divided (`20261025T2022-c21-b42-deaths-are-founders`), so this is one sweep.
  - The trait has no cost and an imposed cap at 1.2.
- **Timing:** the claim reached SIBDH at 14:29Z. STATE.md showed the challenge open at 14:59 and achieved at 15:02, after 172279226 (15:00Z) let a `C:` task name it.

**swim-divide (SIBMD).** Held since 06:21Z Oct 26 by `20261026T0227-c29-kernel-ring-screen#c1` (class phase-field).
- **History:** c11's ringed rods first met it at 12:49Z Oct 25 and lost it at 17:19Z to c00's audit.
- **World:** Allen-Cahn cells build a self-made link ring (rim/core 1.64 and 1.57). They move by a written chemotactic advection up the substrate gradient their own consumption creates, and they divide with no division rule (224 and 244 persistent splits).
- **Deciding controls:** with mu=0 (no drive) the best track is 1.9 body lengths. With chi=0 (no ring drift) the ring is 0.98 and there are 16 splits.
- **Audit `20261026T0618-c37-audit-kernelring`:** isolated cells in a fresh bath do not swim (0.83 body lengths or less), so the motion is crowd autochemotaxis.
- **Limits:** only 1–3 lineages per seed do all three things in one track, everything happens before the torus jams, and no beyond-diffusion twin was run.

**swim-divide-bd (SIBMD, BD).** Holder: `20261026T0505-c34-nematic-marangoni#c1` (class active-nematic).
- **World:** Cahn-Hilliard rods with nematic order and an extensile active stress, in a Brinkman-Stokes fluid. The rods make a surfactant that adsorbs as a ring. Marangoni stress from that surfactant along each rod's own interface propels it, and the active stress stretches rods into binary fission.
- **Deciding control:** the passive twin (zeta=0, mar=0) gives static round droplets with 0 splits and no motion. With the Marangoni stress alone (mar=40), droplets become filaments that fragment and freeze.
- **Beyond-diffusion vote:**
  - c39 and c41 gave bd_supported [M, D]. Only c41 re-ran the passive twin; c39 relied on the author's. c36 voted bd_supported false, so BD stands 2–1. B and W persist in the twin.
  - `20261026T1533-c00-audit-marangoni-3` set aside the M supports of c36, c39 and c41. build.py does not filter BD lists by `support_rejected`, so M's BD credit still rests on c39 and c41.
  - c36 notes that the propulsion is frictional, not a force-free swim.

**contained-swimmers (SIBWMD).** Same c34 claim. Each rod also makes a cargo that its own ring excludes through the chemical potential ln c + κs.
- **Result:** cargo in/out 10.4–10.8, with 100% of daughters at 2x or more.
- **W controls:** κ=0 gives 1.33 and 0% of daughters; c00's wall-off arm gives 0.17x.
- **M:** measured in rod lengths, M failed at first: 4 of 245 pooled dividing tracks reached 3 lengths (`20261026T1130-c00-audit-marangoni`). It passed later as a replicated minority, 5 of 61 dividing tracks on seeds 61–64 (`20261026T1533-c00-audit-marangoni-3`). mar=0 gives 0 swim-then-divide tracks.
- **History (STATE.md):**
  - first met, audited, at 09:49Z Oct 26;
  - open at 11:51Z after c00's first M audit;
  - shown but disputed 13:26–13:44Z and again from 14:12Z;
  - audited from 15:41Z, after c00's third audit and the minority rule (225b47876, 15:38Z).

**inherited-contents (IBWD).** Holders: `20261026T0405-c34-nematic-cargo#c1` (the same rods without the Marangoni back-action) and the c34 Marangoni rods.
- **Result:** cargo in/out 12–14, with 97–100% of daughters at 2x or more after fission.
- **Deciding control:** the wall-off arm (adsorption drift off, bodies identical) gives 0.24–0.25 on seeds from two auditors; κ=0 gives 1.36–1.48. The claim holds at 8.3–10.3 on a 1.5x grid and 15.0 at dt/2.
- **Limits:** the containment is leaky and kinetic (21–30% of cargo on the rods).
- **History:** c03's gated micelles first met this challenge at 09:18Z Oct 25 and lost it at 11:16Z Oct 26 (see §4). c03's fch-metabolic also held it 09:56–17:55Z Oct 25.

**metabolic-cell (IBED).** Holder: `20261026T1100-c40-cips-layered-divide-claim#c1` (class catalysis-induced phase separation, CIPS). Met 15:05Z Oct 26.
- **World:** enzyme condenses by drifting up the gradient of its own catalytic product. Catalysis burns a regrowing fuel and makes an amphiphile that forms an outer layer, and bodies pinch into layered daughters.
- **Controls:**
  - A global fork with regrowth off dissolves all 19 bodies within 100 t, while fed twins keep all 19. c00's audit (`20261026T1650-c00-audit-cips-layered`) notes that this fork "passes for any active condensate", because bath enzyme also burns the fuel.
  - The individual-level control is c44's absorbing fuel moat (`20261026T1525-c44-cips-moat-cut`): 12 of 12 targets die within 25–50 t while their neighbours keep their size. Plain local regrowth cuts kill only some targets (0/2, 1/1, 1/4).
- **c00's audit also found:** bodies use 47–71% of the fuel on 4–6% of the area.
- **Caveats:**
  - Division needs a written enzyme turnover. Charged to the fuel, it still gives 7 and 6 splits (`20261026T2102-c48-cips-fuel-powered-division`).
  - Births stop when the box fills, and the fed world has no deaths.
  - The layer is one-way coupled.
  - S is weak.

**motile-repair (IBRM).** Holder: `20261026T0243-c31-crawler-layer-repair-claim#c1` (class crawler-phase-field). Met 03:26Z Oct 26; this was the largest single P jump (+14).
- **World:** a planted wave-pinning crawler. A bistable polarity protein forms a front, protrusion there moves the cell, and the protein makes an edge layer.
- **Deciding control:** after a 40% front cut, the cell rounds, re-nucleates a front and crawls at 0.34–0.36, against its uncut twin's 0.42.
- **c00's audit (`20261026T0450-c00-audit-crawler-layer-repair`):**
  - Repair on 7 of 9 seeds; seed 2 took a two-lobe competition path, and seeds 4 and 6 die.
  - Only front re-nucleation counts as repair; the layer re-coating and the rounding are by construction.
  - I, M and R are c22's established crawler, reproduced bit for bit.
  - The challenge is "met only in the letter".
- **Beyond diffusion:** the ledger credits W, R and M. c30's slow-diffusion twin gave W; c00's linear-kinetics twin, which loses polarity, gave M and R.
- **Limits:** no cut cell regains its size (about 52%), and the claim has no S and no D. c00 judged W Weak, but the ledger holds W at 4 for, 1 against.

### Frontier and classes

**Largest established sets:**

| Set | Holder | Diffusion-tested |
|---|---|---|
| SIBWMD | c34 Marangoni rods | yes |
| IBWRM | c31 crawler | yes |
| SIBDH | c14 pcell-mwall | no |
| SIBED | c40 CIPS | no |
| SIMX | lab-1 evopursuit | no |
| SIXD | c36, c42, c52 active emulsions | no |

**Dynamical classes.**
- 20 classes have established capability claims.
- Only 7 claims in 4 classes are diffusion-tested: active-nematic, crawler-phase-field, phase-field, and fch-bilayer. Three of the seven are disputed by audit: c01 fch-uptake-cargo, c15 nematic-fuelcell and c31 crawler.
- Another 20 classes produced only negatives or findings.

## 4. What it corrected

**The most instructive overturned claims:**

- **Ringed nematic rods (`20261025T1141-c11-active-nematic-ringed`).**
  - c00 found that the bath makes 63–82% of the surfactant, and bath-made surfactant alone forms the ring (rim/core 2.18). B is by construction.
  - The same audit found that the `--dt` time-step controls had been mislabelled.
  - Six reviews came before the audit; four (c01, c03, c09, c12) supported the claim and two were Weak.
  - Rules: true dt/2; self-made layers; audits.
- **Nematic fuel-cell rods (c15).** The bath makes 73% and 78% of all surfactant (`20261025T2005-c21-audit-fuelcell`; c23: bodies make 24–29%). With a rod-only source the ring sits at 0.19, does not gate, and splits fall to 8 and 4. A ring-free slow-diffusion twin matches the world at 15/3/25 (`20261025T1517-c20-fuelring-is-slow-diffusion`).
- **FCH uptake cargo (c01; FCH = functionalized Cahn-Hilliard).** The claimed 141–169x containment refilled within 20 t after the solute was erased, heading toward a Boltzmann factor of about 820–900. It is an equilibrium partition. The audit calls the "no uniform-D twin" argument "true but empty" (`20261025T1850-c17-audit-uptake-cargo`).
- **Gated micelles (c03).** Under the existing wall-off rule (54838cf09), with the shell's adsorption removed, the cargo is still held at 3.41x and 3.51x (`20261026T1100-c00-audit-w-fch-gated-micelles`). W is by construction. The coupling-off arm (dd8ab200b) came from the parallel nematic-cargo W audit (`20261026T1100-c00-audit-w-nematic-cargo`), where a filled body expels the cargo under a repulsive coupling.
- **A mark lifted.** c39's audit (`20261026T0812-c39-audit-nematic-cargo`) ran the wall-off arm (0.25) but still marked W by construction, because the exclusion is a written term. Under 54838cf09, for W a written coupling term alone is never a reason for by construction; the wall-off arm decides. Wall-off arms (0.25, 0.24) showed that the ring does the holding.
- **Marangoni M.** sqrt(area) "counts about two lengths per rod length". Rules: measure M along the axis of travel; `support_rejected`; minority capabilities. The minority is not inherited: parent-offspring slope +0.22 [−0.61, +1.44] (`20261026T1530-c00-marangoni-minority-lineages`).
- **Digestion ecology (`20261027T0325-c52-digestion-ecology-claim`).**
  - With digestion off and prey kept, predators persist on 4 seeds (47→45, 49→47, 47→49, 46→49), anchored by a written fuel-depletion drift (chiF 0.5).
  - 96 of 99 predator splits are co-fission with sister prey.
  - Rule: L4c "consumption, not presence".
  - `20261026T1700-c43-cips-consumer` then failed the same test (consumers 31→39 with eating off). It is the only Phase-2 claim to be contradicted.
- **Reacting thermals (c49).** In c53's audit (`20261027T0534-c53-audit-thermals`), caps with burning and heat loss off rise at 0.48 px/t against 0.41 when fed. The motion is passive buoyant rise in imposed gravity, so M is by construction. E is by construction because heat is a written build-from-food term with decay.

**Laws.**
- The slow-diffusion containment law (`20261025T0901-c01-slowd-containment-law`): contrast−1 = 1.01 (Dc/0.1)^−0.93, a joint fit over four points. A 1/Dc fit to Dc=0.01 alone predicted 4.1 at the held-out Dc=0.03, and 4.0/4.1 was observed. The analogous prediction for a doubled decay rate fails off steady state (predicted 19.4, observed 12.9).
- Coexistence by arena size (`20261026T1511-c42-arena-heldout`): 0/4 up to 4/4 across 32–96², with pre-registered predictions met at 80² and 40².

**Mechanisms.**
- Local cuts decide metabolism; an absorbing moat kills 12 of 12 targets.
- Barriers beat uniform diffusion: the chemoton gate holds 69% of the catalyst, against 7–17% with any uniform diffusivity.
- CIPS division needs a window of enzyme turnover.
- Predators survive only on a mixed diet.

**Negatives.**
- 150 of the 258 findings are negative, and 104 established negatives make up most of C.
- New classes tried without success include Schrödinger-Poisson, nonlocal oscillators, polar active fluids and reactive Marangoni, plus about 15 others (BFF program soup, hash chemistry, particle-Lenia, Swift-Hohenberg among them).
- Inside productive classes: a third trophic level freezes the population; the CIPS catalysis trait is not selected; evoloop is not open-ended over 500k steps.
- Three negatives were themselves overturned:
  - c37's "never split" fell when c39 found 36 of 57 break-ups (c41 found 83).
  - c37's delay-map negative fell when c41 found that the spot drifts 8–10 body lengths and that the map used the stabilising sign (`20261026T1131-c41-review-sh-delay`).
  - c25's "divide or travel, not both" fell when c29 found 5 lineages that do both.

**Count discrepancies, resolved.**
- C = 30 contradicted claims (29 lab-1 plus c43) + 104 negatives = 134. STATE.md's heading "33 contradicted claims" also counts 3 contradicted findings, which C leaves out.
- build.py's audit logic gives 9 disputed claims. STATE.md prints only six (`n_disp[:6]`). The three missing are c31 crawler (W), c49 thermals (M, E) and c52 ecology (E).
- K = 34 from 35 eligible findings: `20261026T1415-c42-coexistence-arena-size` and `20261026T1511-c42-arena-heldout` share operator, capability and world, so they count once.

## 5. What remains open

**Ecology with reproduction (IXDE).** It was met only from 12:26Z to 15:20Z Oct 27, by c52 with its audit pending, until c00's audit disputed E. No established design holds D and an E that is not by construction on the same individuals.
- **c56's prey (`20261027T1100-c56-prey-ixde-claim`, provisional) is the nearest.**
  - Two Supported reviews find D and E on the same prey: `20261027T1633-c57-review-prey-ixde` and `20261027T2136-c60-review-prey-ixde`.
  - `20261028T0058-c62-review-prey-ixde` is Weak. The prey's E passes the L4c catalysis-off arm (6/6 dissolve), but all 72 prey splits have a predator within 6 px. Both supporters also note that prey divide only when predators are present.
  - QUEUE.md: "IEXD: 1 more supporting re-run(s)". The challenge is neither named nor beyond diffusion, so one more supporting review would show it met, with the audit pending.
- **c60 half-drift (chiF 0.25, `20261027T2013-c60-halftaxis-ecology`, provisional): E passes, D sits on the pair.**
  - Starved targets die: c60 reports 9/9 in 350–450 t; the reviews find 8 of 9 at 300–600 t.
  - Predators divide only after their own prey divides (c62: 76/76; c61: 77/77). All 98 prey splits have a predator within 6 px (c62), and twin prey never divide.
  - c00's audit of c52 found that treating the pair as the individual would need a pair-level X control that does not exist.
- **c46 hunting droplets (provisional; E 0 for, 2 against):** predators divide on their own, but D and E sit on different kinds, and both kinds' E is written into the rule (`20261028T0925-c64-synthesis`).
- **c62 Flow-Lenia (two provisional claims): D exists but is seed-dependent; E is by construction.**
  - In the from-noise claim `20261028T0344` (reviews by c63 and c64), predators reach generation 1 on seed 21 and 4 on seed 22. The planted claim `20261028T0303` reaches only generation 2 on seed 24.
  - The product gates the whole growth field (c63, and c64 twice).
  - Submitted c64 findings: the gate is all-or-nothing (`0601`); gate floors of 0.1–0.5 leave 16–26 starved predators alive, and minority gates leave 15–19 (`0921`); between bodies at least 50 t old, fusions outnumber clean splits 34:9 and 43:13 (`0718`).
- c64's synthesis: no design has "a body that runs its full rule without the resource and starves as an outcome of its dynamics". The last lead is submitted: a sampled-at-merge predator trait beats its neutral twin on 3/3 seeds (+0.24, +0.19, +0.06; `20261028T0953-c64-fl-sampled-trait-interim`).

**Open-ended novelty (IDHO).** O was never claimed or established. The base is c53's fed vortices (SIDH: the fitter kind reaches 0.86–0.93 of vortices, against 0.38–0.60 in its twin). The longest test is c61's T=30000 run of c58's three-component-trait vortices with the standard waste, on one fresh seed (`20261028T0326-c61-vortex-t30k-saturates`):
- The share of vortices on new trait ground is 0.00–0.02 after t=8000 (twin 0.00–0.01).
- First-time dominant kinds keep appearing (5, 5, 4, 3, 6, 3 per 5000 t), but all lie within |class| ≤ 3. By RUBRIC L8 that is cycling through a finite repertoire.
- Later wastes also stay bounded: c63's distribution-memory waste (`0700`, replicated `0833`), a never-decaying one (`1010`), and a dm/sw scan that stalls after 4–5.6 mutation steps (`0925`). c61's long-memory waste travels on 1 of 4 seeds only (`0344`, correcting `0105`).
- c58 itself notes that the kinds have equal fitness and that the frequency dependence is written in, so any O may be by construction.
- All 19 vortex-novelty findings are submitted and unreviewed. Only the 1-D precursor, `20261027T1230-c58-vortex-trait-climb`, is established.

**Minority swimmers spread (IMDH).** There has been no work since Oct 27 17:54Z, and none of the results below is established (loops 1 and 2 are provisional; paired4 is submitted).
- **c50's four-loop campaign (`20261027T0240-c50-marangoni-spread-paired4`):** c50 reports the trait rising over its twin on 4/4 seeds (+7.6, +7.2, +3.4, +0.4), but the swimmer share is higher on only 1 of 4.
  - c51's Weak fresh-seed review does not reproduce the rise for t≥1000 (36.2 vs 36.4).
  - Fresh-seed reviews of loops 1 and 2 are split: c57 (seed 520) reproduces the trait rise (50.0 vs 41.8), c56 does not (40.8 vs 42.9); so the rise replicates on 1 of 3 fresh-seed reviews.
- **c54's assay:** the response is plastic (the twin passes almost as often), and mar 60 loses in competition. The single-kind levelling result failed its own dt/2 check (4.36 vs 2.66 lengths per cycle).
- **c00's graded-motility finding:** speed is unimodal, so the minority is the tail of one graded state.
- **Untried:** graded supply, range expansion, and larger populations (192²).
- **Acceptance:** a claim must name the challenge and show a self-copied trait, a trait-blind mutation operator, single-kind ancestors, and two controls: an environment where moving cannot change survival, and an identical-event twin.

## 6. Numbers

| Component | Start (Oct 24 21:45Z) | Now (Oct 28 10:25Z) | Peak |
|---|---|---|---|
| P | 38 | 122 | 130 |
| P_BD | 0 | 74 | 74 |
| Q | 0 | 90 | 94 |
| K | 0 | 34 | 34 |
| C | 29 | 134 | 134 |
| P_prov (P including provisional claims) | 52 | 198 | 198 |
| P without the top claim | – | 110 | – |

**Contributions.** 2389 in total. By kind: intent 985, review 876, finding 258, sighting 77, question 71, claim 59, synthesis 42, literature 18, tool 3. Per day: 1196, 777, 337, 79. Audits are 27 reviews with an `A:` task (10 by c00).

**Sessions.** 65 authors: c00 (47 contributions) plus 64 workers. Workers were active 5.08–5.88 h (mean 5.54) and made 11–71 contributions each (median 33.5). Peak concurrency was 16 by the log and 12 by session spans. From Oct 27 it was mostly 2–4, with dips to 0–1.

**CPU.** 921.4 h (progress.json: 921.35): 386.05, 280.18, 185.40 and 69.72 by day.

**Pending reviews.**
- 83 claims need reviews, including 59 submitted findings: 58 were never reviewed, and 1 has only a review that does not count.
- QUEUE shows "review pressure 148.0". That is the 148 reviews still needed on Phase-2 claims (161 counting lab-1 seed claims), divided by max(1, active agents), which is 1 because 0 agents were active.
- The backlog low was 13, at 11:33Z Oct 26.

**Verdicts and statuses.**
- There are 877 review verdicts in 876 review contributions, because `20261025T0833-c05-review-ringswim` judges two claims. 79.9% are Supported, 19.3% Weak and 0.8% (7) Contradicted.
- Phase-2 claims: 52 established, 7 provisional, 1 contradicted. Only 28 of the 52 score every capability they claimed, and 21 carry by-construction marks.
- Lab-1: 82 ledger keys (48 established, 29 contradicted, 4 provisional, 1 submitted) from 83 seed entries. The missing entry is `lab1-particle-life-sporecell3`, a negative control with no capabilities, which `derive()` skips.

**Plateau.**
- P has been 122 since 15:13Z Oct 26, apart from 12:26–15:19Z Oct 27 at 130.
- P_BD has been 74 since 14:12Z Oct 26. Q has been 90 since then, apart from 94 at 03:28–05:36Z Oct 27.
- The last challenge still met was met at 15:05Z Oct 26. IXDE was met at 12:26Z Oct 27 and lost at 15:20Z.
- Since 15:13Z Oct 26 the collective added 609 contributions and 343.28 CPU h (37% of the total). In net terms only K (26→34, flat since 13:22Z Oct 27), C (114→134) and P_prov (190→198) rose.
- The final exploration share was 0%, against a 33% target.
- The 10:43Z pause is not recorded in the repo. c63 and c64 published leave intents at 10:16 and 10:23. The last import is e8818f1c6 at 10:25:54Z. Since then `sync.sh`, still running, has pushed timestamp-only rebuilds with 0 new contributions and unchanged scores (bff3a2e01 at 10:59:53Z, 188bf9643 at 11:32:32Z). The local checkout is still at e8818f1c6.

## 7. Lessons for the next phase

**What the scaffold does well.**
- Requiring re-runs, plus code-reading audits, finds capabilities that the code imposes. All 4 falls in P came from c00's audits, each with a concrete deciding control: a bath-versus-rod surfactant source split (c11), M re-measured in rod lengths (the Marangoni rods, twice), and a digestion-off arm (c52). Wall-off arms removed W from c03 without lowering P.
- Most rules were learned from counterexamples, and each is tied to a contribution.
- Negatives accumulate as credited knowledge.

**What it does badly.**
- **Inside review is lenient.** Only 0.8% of verdicts were Contradicted, and all 4 falls in P followed c00's outside audits. Four of the six reviews before the ringed-rods audit supported the claim.
- **The rules changed under running sessions.** M switched off and on twice in one afternoon. Before 5d3472d60 no rule change was announced, and the documents still trail the code.
- **Reach stalled while effort continued.** Exploration fell to 0%, and the score "does not see exploration until it pays off".
- **The backlog grew as agents left.** Claims needing review rose from 13 to 83, and the newest c63/c64 work is unreviewed.
- **The record is incomplete.** STATE.md shows only 6 of the 9 disputed claims, the canary check was never run so there is no measured false-support rate, and the lab-1 holder of reproduction-beyond-diffusion was never audited.
- **Many contributions are cheap coordination.** Intents are 41% of contributions but 0.0% of CPU. Reviews take 46.9% of CPU, findings 33.7% and claims 13.0%.

**Next steps the evidence supports.**
- Schedule outside audits early, including audits of lab-1 holders.
- Turn on the canaries.
- Announce every rule change, including those made only in code.
- Clear the review backlog before adding agents.
- Attack each open challenge at its named failing control:
  - IXDE: one more supporting review of c56's prey claim, then an audit that weighs c62's dissent; failing that, a maintenance cost on the body ("a cost the body pays to persist", `20261028T0921`) or a pair-level X control;
  - IDHO: a waste restored relative to mean fitness (Q `20261028T0912`). The no-decay half already failed (`1010`).
  - IMDH: the graded-supply assay.

## Corrections applied

- Phase 1 dates: "Oct 24–25" became 24 Oct, 14:03–21:45Z (`REPORT.md`; build.py `LAB_START`).
- Source note: three fact-checks plus source checks replace the "two disputed points"; the last import is named as e8818f1c6.
- Disputed claims: 9 established claims are disputed and STATE.md shows 6 (`n_disp[:6]`).
- Rule revisions: 24 commits after the a03d4cb72 launch (23 without the replay 447c6f810), with the inclusion rule stated; "each triggered by a failure" became "most", with the feature commits named.
- "Reach has not grown since 15:13Z" now notes P=130 at 12:26–15:19Z Oct 27.
- Capability table: B, W and S now use SCORE.md's full wording.
- "By construction" redefined per SCORE.md: one counted mark, credited in K, liftable by an audit.
- RETRO_lab1: "four problems" became nine lessons, with the 16:36-digest headline added and the withdrawn generation count included.
- Decision rules: thresholds count capabilities besides S; the unreliable-Supported, latest-review, Weak-listed and lineage rules added.
- Assignment order corrected: challenges come first only among open tasks.
- Audit exceptions added: lab-1 claims are never audited, at most 2 audits run at once, and every c00 review counts as an audit.
- Rule history: 172279226 added; 563065c74 shown as predating the audit's 17:19Z import; db3b5c3ac and a70023430 described correctly; 54838cf09's extra effects and the minority rule's scope (B, W, R, M, E) added.
- Code-versus-docs list: unannounced build.py changes all predate 5d3472d60; `necessary`/`law`/`class_confirmed` appear in PROTOCOL templates; lineage, thresholds, the C rule and the lease added; "none recorded in the files" removed.
- reproduction-BD: added the single BD vote by the twin's builder, the λ=0.001 twin, the χ=0 ring not being load-bearing, the unaudited lab-1 holder and c15's 15:18–20:42Z holding.
- Autonomous heredity: the +0.17/+0.17 is the b42 world in c21's audit, the twin had 0 splits and 0 deaths, and c00's twin ran on one seed.
- Autonomous heredity: c00's and c21's audit caveats added (death inflation, half the yield rise from growth, bias surviving recounts).
- "About 10⁴ particles per cell" became about 10⁴ in all.
- swim-divide-bd: c36's bd false vote (2–1), only c41 re-running the twin, and `support_rejected` not filtering BD credit added.
- contained-swimmers history: first met 09:49Z Oct 26, with the open and disputed intervals listed.
- inherited-contents: c34 Marangoni added as second holder; c03 fch-metabolic's 09:56–17:55Z holding added.
- metabolic-cell: the global fork is not discriminating; c44's moat (12/12) is the individual-level control; box-fill and one-way-coupling caveats added.
- motile-repair: seed 2 took the competition path and seeds 4 and 6 die; only re-nucleation counts; "met only in the letter"; BD credit is W, R and M (c30: W; c00: M, R).
- Diffusion-tested claims: 3 of the 7 are disputed (c01, c15, c31), not only fch-bilayer.
- Ringed rods: "six reviews passed" became six reviews before the audit, four Supported and two Weak.
- c15: 73%/78% is of all surfactant, not of the ring; c23's 24–29% and c21's rod-only-source control added.
- Gated micelles: the audit applied the existing wall-off rule; the coupling-off arm came from the nematic-cargo W audit.
- "A mark lifted": the rule applies to W only (54838cf09), and c39's own wall-off arm had already given 0.25.
- Reacting thermals: E is by construction from build-from-food heat; M from buoyant rise in imposed gravity (c53's audit).
- Slow-diffusion law: 4.1 came from a Dc=0.01-only fit; 19.4 vs 12.9 is the kd prediction, not the Dc law.
- Overturned negatives: two became three (c37's delay-map negative added); c41's 83 break-ups added.
- Report conflicts resolved: C composition, the 9 disputed claims, and K's deduplication of the two c42 findings.
- Ecology: "no design holds D and E on the same individuals" corrected to exclude by-construction E; c56's prey claim and c46's design added.
- c60: marked provisional; 9/9 is the author's figure (reviews find 8/9); "prey divide only where cut" became "predator within 6 px"; the pair-level X phrase attributed to c00's c52 audit.
- c62: generations attributed to the two claims and their seeds; the 50 t threshold on fusions, minority-gate counts and submitted status added.
- c64 quote corrected to "outcome of its dynamics"; the sampled-trait lead added as submitted.
- Open-ended: c61's run is c58's three-trait vortices with the standard waste on one seed; later bounded wastes added.
- Open-ended: the by-construction objection attributed to c58; the established 1-D precursor noted.
- Minority swimmers: c50 and c54 results marked submitted; c51's, c56's and c57's non-reproductions and c54's dt/2 failure added.
- Minority swimmers: acceptance criteria added.
- Plateau: 609 contributions and 343.28 h counted from 15:13Z; Q=94 window, P_prov rise and the "last challenge still met" wording fixed.
- Last build: librarian rebuilds at 10:59:53Z (bff3a2e01) and 11:32:32Z (188bf9643) with unchanged scores added; local checkout still at e8818f1c6.
- Explained gaps: 877 vs 876 verdicts (c05's two-claim review); 83 vs 82 lab-1 entries (sporecell3 has no capabilities).
- Pending reviews: 59 findings split into 58 never reviewed and 1 not counted; 148 excludes lab-1 seed claims (161 with them).
- Concurrency: "2–4 from Oct 27" now notes dips to 0–1.
- Lessons: all 4 P falls came from c00's audits, and the deciding controls are named correctly.
- Lessons: "coordination costs dominate" replaced with CPU shares (intents 0.0%).
- Next steps: the c56 review and audit step added; the IDHO step updated after the `1010` result.