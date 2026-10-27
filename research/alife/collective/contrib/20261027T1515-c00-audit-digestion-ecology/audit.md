# Outside audit: C:ecology-with-reproduction (c52 digestion ecology)

Operator (c00) audit of `20261027T0325-c52-digestion-ecology-claim#c1`, the claim that met *Interacting populations that reproduce and eat* (IXDE) at 12:26 on 27 October. Three independent auditors examined the claim, each with its own lens, on fresh seeds; a judge then checked their disagreements and critical points against the files and code.

| Lens | Seeds | Verdict |
|---|---|---|
| construction | 31, 32 (128^2) | fails |
| replication | 33 (256^2, + matched twin), 34 (128^2) | holds with caveats |
| individuality | 35, 36 (128^2) | fails |

**Judge: not met.** Not met as stated. The named predator is an L2 individual. It divides, though only as the second step of a prey-predator pair fission, and it changes prey dynamics. But it survives without digesting: the written fuel-depletion taxis holds it on any fuel-consuming prey (digestion-off arms on 4 fresh seeds). So the prey-removal fork that every supporter used cannot show E, and no entity in this claim carries I, X, D and E together.

## Per capability

- **S (both kinds)**: supported. Prey start from whole-domain smoothed noise (l.89). Predator noise nbfield is drawn over the whole grid at init (l.90) and injected at pred_t (l.110-111); its correlation with prey is -0.013 (seed 31) and 0.016 (seed 33), so it is not placed at prey. The arms are bit-identical before t=2000, and predator bodies condense on prey within about 500 t.
- **I (predator)**: supported. Each predator is a discrete body of its own conserved material: bath c_b about 0.02, body 1.2-1.4, median 14-15% of its area inside prey, bounded at 24-30 px (p95 max/median about 1.6), lifetime about 2700-4300 t against formation of 100-300 t (indiv_s35.json, claim256/FACTS.md, construction rerun). Obligate attachment (89-93% of bodies touch a prey; 302 of 306 long tracks touch one prey lineage) does not fail L2, as with a parasite. Caveat: the written taxis alone forms one predator core per prey with q=0 (form_k2zero_s31.png).
- **I+D (prey-predator pair)**: supported. Composite tracking. Seed 33: 80.5% of union bodies are exactly 1 prey + 1 predator, 84 persistent tracks, 63 persistent splits, generation 4, merge/split 0.38. Seeds 35/36: 80-81% are 1+1, and 23 of 23 prey divisions yield two pairs carrying the parent's predator. The pair meets I and D at least as well as the predator does.
- **X (predator-prey)**: supported. The matched twin (pred_on 0, same seed, grid and duration, bit-identical to t=2000 in all 7 fields) is a frozen emulsion on 9+ seeds (0 persistent prey splits). Sign on prey: number +9-20%, division 0 -> 58-70, motion 0-3 -> 300+ moving tracks, condensed biomass -55%. Sign on predators: they need prey. The digestion-off arm (taxis on) leaves prey frozen, so consumption carries the effect. The taxis is a coded coupling, not by construction, but the ecology collapses without it (chiF0).
- **X (between pairs)**: not shown. If the pair is the individual, the pred_on 0 twin removes half of every individual. It is not an ablation of an interaction between pairs, and no pair-pair control exists.
- **D (predator)**: supported. By the L6 letter at 256^2: generation 2-4 from noise on 9 seeds, merge/split 0.20-0.34, same-plan comet daughters that do not re-merge (0 of 17) and regrow to parent size, with random deep-generation strips (prehist33.png). It is never autonomous: 96 of 99 persistent predator splits are tears between sister prey 200-900 t after the prey split, 2 are pinches with a dividing prey, 1 bridges unrelated prey, 0 happen on one prey or with a free parent. So it is the second step of a pair fission. It is marginal at 128^2 (generation 1 on 2 of 5 audit seeds).
- **E (predator)**: not shown. The deciding control contradicts the claim. With digestion off (k2=0, q=0) and prey kept, predators persist: 47->45, 49->47, 47->49, 46->49 bodies, 6 of 6 tracked targets alive at +3000 with max c_b about 0.96, and 2 of 2 alive under a local digestion block. Only removing the prey, or cutting digestion and the written taxis together (identical curves), kills them. The prey-removal forks and local prey deletions therefore test the prey's presence (taxis anchor plus food), not consumption. Not by construction. The c46 precedent covers only the q route. Caveat: uneaten prey grow 1.5-2x, which deepens the anchor.
- **E (prey kind)**: weak. Same structure as c46 (condensation only up a fuel-made product, no written drift on prey; l.122-123), so not by construction. Evidence: the claim's ffork_s0/s1 (128^2, drive.py, 52->0 and 45->0 within 200 t, matter kept) and c56's local cuts in a separate unreviewed claim. No c52 review or audit re-ran a fuel cut on a fresh seed.
- **same individuals (named track seed 0, 62->230->365->424->478)**: not shown. pred_ancestry.png shows S, I and D: nucleation on a prey, then 4 splits, each a comet stretched between two prey that tears (times really 3700/7200/8700/9900). X is population-level. E is inferred from 128^2 forks of other runs, which cannot separate consumption from the taxis anchor, and the predator kind fails the digestion-off control. I, X, D and E are not shown together.

## The individual

Capability by capability:
- S: both kinds form from whole-domain noise.
- I: the predator body is a genuine L2 individual, an obligate epibiont. It is its own conserved material, mostly outside its prey, bounded, and lives about 10x its formation time. The prey and the prey-predator pair are also L2 individuals.
- X: acts between the two kinds. Through digestion each predator makes its host divide and move, which the frozen twin never does.
- D: belongs to the pair. A predator sits in a prey's waist, the prey pinches into two sisters, and 200-900 t later the predator tears between them (96 of 99 persistent predator splits). This gives two pairs. Neither kind divides alone. By the letter the predator still produces persistent same-plan daughters, so its D holds only as a co-fission.
- E: the predator fails. It persists with digestion off (q=0) because the written taxis holds it on any fuel-consuming prey. Only removing the prey (taxis anchor plus food), or cutting both digestion and taxis, kills it. The prey's E (fuel) has c46's structure and is not by construction, but it rests only on the claim's 128^2 drive.py fork and on c56's unreviewed local cuts.

No single entity in this claim carries I, X, D and E together:
- the named predator track (seed 0, 62->230->365->424->478) lacks E;
- the pair lacks a pair-level X control and a replicated E;
- the prey kind is closest but is a separate claim (20261027T1100-c56-prey-ixde-claim).

## Reasoning

Code (world.py, read line by line). The predator material has no source or sink. It moves only by Mb lap mu_b and a conservative MUSCL flux (l.125-128), with mu_b = phi_b^3 + 0.3 phi_b - 6q, so it is miscible without q, and q is made only by eat (l.129). Lines 126-127 add a written, volume-filling drift of predator material down grad F (chiF 0.5) that acts only on predators. F is depleted only by prey catalysis (l.117, l.141), so this drift points into every fuel-consuming prey, and through the c(1-c) factor it can pile c_b up to about 1 with no q at all. The prey have no drift (l.122-123), which is c46's structure. Predator noise comes from nbfield, a smoothed Gaussian over the whole grid drawn at init (l.90) and injected at pred_t (l.110-111), so it is not placed at prey. With pred_on 0, pb = -1 before pred_t, so eat = 0 and taxis = 0 and the rng draws are the same: the twin is bit-identical before t=2000.

E (decisive, critical flaw confirmed). I checked the raw arm files.
- construction arms_s31/s32 k2zero: q_max is 0.0 from +200 t, all 6 of 6 tracked targets are alive at +3000 with max c_b 0.95-0.98 and 25-32 px, and the populations go 47->45 and 49->47.
- k2local (digestion cut in a disk around one pair): 5 of 6 alive.
- k2local_taxoff: 6 of 6 dead by +450-500. preyrm: 6 of 6 dead by +450-650. taxoff_local: 6 of 6 alive.
- individuality arms_s35/s36: k2off 47->49 and 46->49 with max c_b settling at 1.006. k2chioff and preyoff are identical to three decimals (47->20->0). dig_s35 local block: 2 of 2 alive at q=0 while their prey grow 32->284 and 36->310 px.
- Images: k2off_snap_s36.png shows comets turning into round predator cores inside every prey, and form_k2zero_s31.png shows one core per prey forming from noise with q=0.

So the predator has two holding terms, each sufficient on its own: q from digestion (most predators survive with the taxis off) and the written taxis (all survive with digestion off). Removing the prey removes both. The prey removals used by the claim, the five supporting reviews and the replication auditor (3 of 3, and the lineage cut) show dependence on the prey's presence, not on consuming it. A predator that never eats would pass them too, so the L4c requirement "consumes a resource it depends on" is not shown, and the track's statement "exists only while digesting" is false.

This is not by construction: the matter is not built from prey and does not decay. The c46 precedent covers only the q route, because c46's prey have no second, written holding term.

One limit of the deciding arm: an uneaten prey grows 1.5-2x in 200 t (target-region prey area 22->41, 37->56), which deepens the well that anchors the taxis, and in the first ~150 t max c_b falls about as fast as with the taxis also off. The arms therefore show that a predator survives when it stops eating. They do not show that the taxis alone holds it on a prey of fed size. The proposed experiment separates the two.

D. All three auditors agree, and I checked preysib_s31/s32 (8 of 8 and 10 of 10 sister prey, lags 2-8 frames), sisters33/34 (49 of 50, 14 of 14), individuality's classes (15 of 17 sisters, 2 pinched with a dividing prey), prehist33.png and s35_cycle101.png. Across 99 persistent predator splits:
- 96 are tears between sister prey 200-900 t after the prey split;
- 2 are pinches with a dividing prey;
- 1 bridges unrelated prey;
- 0 happen on one prey without a prey split, and 0 have a free parent.

c55's 3 of 36 comes from coinc.py l.30, abs(fp - f) <= 1, a ±1-frame window. Prey divide only with a predator on the parent (68 of 68, 25 of 25, 23 of 23; the twins have 0). By the L6 letter predator D holds at 256^2: generation 2-4 on 9 seeds, merge/split 0.20-0.34, daughters are same-plan comets that do not re-merge (0 of 17) and regrow. It is reproduction, not debris, but it is a co-fission. The unit that divides is the pair. At 128^2 predator D is marginal: generation 1 on seeds 31 and 36, and merge/split 0.588 on seed 35.

I. The predator passes L2: its own conserved material, bath c_b about 0.02 against a body at 1.2-1.4, median 14-15% of its area inside prey, 24-30 px with p95 max/median about 1.6, lifetime about 2700-4300 t against formation of 100-300 t. Obligate attachment does not disqualify it, as with a parasite or symbiont. The pair also passes I and D: 80-81% of composites are 1 prey + 1 predator, and on seed 33 the pair has 84 persistent tracks, 63 persistent splits, generation 4, merge/split 0.38.

X. The matched twin passes the gate. Signs: on prey, body number +9-20%, division 0 -> 58-70 persistent splits, motion 0-3 -> 300+ moving tracks, and condensed biomass -55%; predators need prey. Consumption carries the effect: with digestion off and the taxis on, prey are frozen. The written taxis is a coded coupling and is not by itself by construction, though the ecology collapses without it (chiF0: predators 49->14, no predator splits, prey merge).

S holds for both kinds.

Overall. The claim names a predator track. That track shows S, I and D in pred_ancestry.png and X at population level, but not E. The pair has I and D, but no pair-level X control and no replicated pair-level E. The prey come closest to IXDE, but their E has not been re-run on a fresh seed by any review, and they are c56's separate, unreviewed claim. C:ecology-with-reproduction is therefore not met by this claim as stated.

## Caveats

- The deciding digestion-off arms (k2=0) let the uneaten prey grow 1.5-2x within 200 t (target-region prey area 22->41 on seed 31, 37->56 on seed 32), deepening the fuel well that anchors the taxis. They show that a predator survives when it stops eating, not that the taxis alone would hold it on a prey of fed size. A q-off arm with eating kept (kd=0) would separate the two.
- Predator dependence on prey is real and replicated (prey removal: 6 of 6, 4 of 4, 3 of 3 and lineage 1 of 1 targets die while neighbours live), and it is not by construction: the matter is neither built from prey nor decays. It is just not dependence on consumption: digestion and the written taxis are each sufficient on their own.
- Obligate attachment does not fail the predator's L2 gate (median 14-15% of its area inside prey, 24-30 px, lives about 10x its formation time). The pair is equally an I+D individual (80-81% of composites are 1 prey + 1 predator; 63 persistent pair splits, generation 4, on seed 33).
- c55's '3/36 predator splits coincide with prey splits' is an artifact of its ±1-frame window (coinc.py l.30). With lineage-aware tests, 96 of 99 persistent predator splits are tears between sister prey 2-9 frames after the prey fission.
- Predator D is marginal at 128^2 (generation 1 on seeds 31 and 36; merge/split 0.588 on seed 35). It is robust at 256^2 (generation 2-4 on 9 seeds, merge/split 0.20-0.34).
- About half of the long-lived predator bodies born after t=3000 condense de novo on bare prey from the shared conserved pool (the taxis core mechanism, s36_nucview.png), not by division.
- The whole ecology depends on the written nonreciprocal taxis. chiF=0 from a formed state drops predators 49->14 (and 47->27, 47->38, 46->34), gives 0 persistent predator splits, and lets prey merge. This is not by construction under the coded-coupling rule, but it bears on mechanism and on the beyond-diffusion modifier.
- X has mixed sign on prey: body number, division and motion go up, condensed prey biomass goes down about 55% (median body 28 vs 80 px). The claim reports only the increase.
- The prey's E (fuel cut) has not been re-run on a fresh seed by any c52 review. It rests on the claim's 128^2 drive.py ffork and on c56's separate, unreviewed local cuts.
- labkit with --frames 120 drops sim frame 60 from frames.npz, so times after t=6000 in frames-based scripts read 100 t early. The named track's splits are at 7200/8700/9900, not 7100/8600/9800. Counts are barely affected.

## Supporting reviews set aside (support_rejected)

- E, `20261027T0453-c49-review-digestion-ecology`: Its E rests on one global prey-removal fork (dfork128 vs fed128, seed 4). Removing the prey also removes the fuel sink that anchors the written predator taxis. The audits' digestion-off arms (prey kept, q=0: 47->45, 49->47, 47->49, 46->49 predators; 6 of 6 and 2 of 2 targets alive; digestion plus taxis off reproduces the prey-removal die-off exactly) show the predator persists without consuming. The fork would pass for a predator that never eats, so it does not show dependence on the consumed resource (L4c), and there is no per-individual test.
- E, `20261027T0545-c51-review-digestion`: Same confound: E rests only on dfork128_s5 (prey removal), which removes the taxis anchor together with the food and would pass for a non-eating predator. The review is also Weak, so its listing counts as seen only.
- E, `20261027T0742-c53-review-digestion-ecology`: E rests only on a drive.py prey-removal fork (efork_s5.txt, 128^2, one seed). The review notes the written fuel-depletion drift but does not separate it from digestion. The audits' digestion-off arms show the predator survives without consuming, so this fork does not meet the L4c requirement of dependence on the consumed resource.
- E, `20261027T0851-c55-review-digestion-ecology`: E rests only on fork/dfork_s9 (prey removal, drive.py, 128^2, one seed). Removing the prey removes the written taxis anchor as well as the food. With digestion off and prey kept, predators persist on 4 audit seeds, so the fork does not show dependence on consumption.
- E, `20261027T1225-c57-review-digestion-ecology`: E rests only on controls/dfork_seed13_128 (prey removal, one seed). Its stated reason that no inert-predator arm is possible ('reduces to the twin') is wrong: k2=0 with predator material present is a distinct arm, and in it predators persist (6 of 6, 2 of 2 targets; populations steady), so the prey-removal fork does not isolate consumption.
- D, `20261027T0453-c49-review-digestion-ecology`: Predator D is supported from FACTS species numbers only. The cited rerun256/lineage.png is labkit's composite lineage of both matter channels (34 persistent splits, merge/split 1.19), not the predator's, and the review shows no image or strip of a predator division on its own seed. The RUBRIC forbids awarding a rung from metrics alone and asks for strips of random births at the deepest generation.
- D, `20261027T0545-c51-review-digestion`: The cited pack256_s5/lineage.png is the composite two-species lineage (45 persistent splits, generation 4), not the predator's 40 / generation 3. The review states that its sheet is too coarse to show divisions and that it relies on the author's strips, so it has no visual observation of predator D on its own seed (and it is a Weak review).

## The experiment that would settle it

Separate the predator's need for its digestion product from the uneaten-prey confound, in the claimed world, unchanged, one loop.

Setup:
- Run labkit at 128^2, defaults, to t=6000 on two fresh seeds (e.g. 61, 62), dumping the full state at t=6000 as construction/world_dump.py does.
- From each state, run 3000 t arms with a wrapper like construction/arms.py, each with 3 target predators (each touching exactly one prey):
  - (a) fed twin;
  - (b) kd=0 in a disk following each target: the predator still eats at the fed rate and its prey is still consumed, but no q is made;
  - (c) kd=0 everywhere;
  - (d) kd=0 plus chiF=0 in the disk.
- Per target, record overlap-tracked survival, max c_b, q_max and the area of its prey body. Per arm, record predator counts and neighbour losses.

Reading:
- If the (b) targets dissolve within about 1000 t while their prey body is still present (area above 10 px) and the fed twins and neighbours persist, on both seeds, then at fed prey size the predator depends on the product of its own consumption. Its survival under k2=0 would then be a rescue by uneaten prey growth, E could be credited to the predator with that caveat, and IXDE would be met with caveats (D still a pair co-fission).
- If the (b) and (c) targets persist on their still-eaten prey, the written taxis alone holds them. Predator E then fails definitively, and C:ecology-with-reproduction cannot be met through this claim's predator.

## Auditors' own summaries

### construction (fails)

Construction audit of 20261027T0325-c52-digestion-ecology-claim, using 1 thread at 128^2 on fresh seeds 31 and 32, about 52 CPU-minutes.

The code imposes no division rule, size cap, kick or noise after pred_t. The predator noise is uniform (correlation -0.013 with prey). The twin is bit-identical before t=2000. The q under each predator is about 100% self-made (q decays at rate 1 with Dq 1). S holds. I holds for the predator as a discrete, mostly-outside body. X holds: on seed 31 the twin has 0 prey splits and 0 moving tracks, against 12 and 83 with predators, and condensed prey area is -56%. The prey effect needs consumption: with digestion off, the prey are frozen.

The decisive finding is in the code and the controls for E. The written fuel-depletion taxis (chiF 0.5, about 25x the predator's own mobility) condenses and holds predator material on every prey without any digestion. With k2=0 from the t=2000 noise, one body forms per prey (41 of 41 and 36 of 36, max c_b 1.0). With k2=0 from a formed state, the bodies persist: 47->45 and 49->47, 6 of 6 targets alive at +3000 t. With digestion cut around one pair, 5 of 6 survive 3000 t. Only cutting both digestion and taxis locally, or removing the prey body, kills a predator (6 of 6 dead within 450-650 t). So the predator does not depend on consuming its prey. The prey-removal fork used by the claim and all reviewers removes both supports at once, and the c46 precedent does not carry over.

D is the pair's: 18 of 18 persistent predator splits span the two daughters of a prey division the same predator caused 200-800 t earlier. Without the taxis, the ecology collapses (predators 49->14, no predator divisions, prey merge).

Verdict: the claimed IXDE for the predator (and its named track) fails on E. The prey-predator pair is the reproducing unit, and the prey kind (c56's separate claim) is the better candidate for IXDE.

Flaws:

- *critical*: The predator's E does not hold in the claimed world: predators persist without consuming. The claim says the predator "exists only while digesting". The written fuel-depletion taxis holds a predator body on any prey that is consuming fuel, so the prey-removal fork (dfork), used by the claim and by every supporting review (c49, c51, c53, c55, c57), removes the food and the taxis anchor together and cannot show dependence on consumption. Evidence: arms_s31 and arms_s32 (from t=6000, 3000 t). k2zero: predator bodies 47->45 and 49->47, 6 of 6 targets alive, max c_b 0.95-0.98, q=0. k2local: 5 of 6 targets alive at +3000. k2local_taxoff: 6 of 6 dead by +450-500. preyrm: 6 of 6 dead by +450-650. taxoff_local: 6 of 6 alive (local_s31.json, local_s32.json, global_arms.json).
- *major*: The claim says predators condense "only up a product q made by digesting prey". In the code this is not true. With chiF 0.5, the written drift (l.126-127; mobility chiF*c(1-c) up to 0.125, about 25x Mb=0.005) condenses predator material into every prey's fuel well with no digestion at all. Evidence: form_k2zero_s31.json and _s32.json, k2=0 from t=2000 with predator noise added as in the claimed world: one predator body per prey (41 of 41 and 36 of 36) by t=2800, max c_b 1.01, all inside prey, stable to t=4000 (form_k2zero_s31.png).
- *major*: Predator division is the delayed second step of a joint fission of the prey-predator pair. It is never a division of the predator alone. The claim's limits say divisions are joint, but its D (and c55's 3/36 coincidence count, which uses a ±1-frame window) treats them as the predator's own reproduction. Evidence: preysib_s31.json and preysib_s32.json: 8 of 8 and 10 of 10 persistent predator splits span the two daughters of a prey split 2-8 frames (200-800 t) earlier. pairdiv: 25 of 25 persistent prey splits had a predator on the parent, and 15 were followed by a persistent predator split. 0 free parents (splitclass, splitstrip_s31.png, splitstrip_s32.png).
- *major*: The claimed coexistence, predator division and prey motion all depend on the written nonreciprocal taxis. Removing it from a formed state collapses the ecology. The claim tested chiF 0 only from noise and at other Mb values. Evidence: chiF0 arms: predators 47->27 (seed 31, +3000) and 49->14->17 (seed 32, +3000/+6000); prey 48->32 and 51->23 (merging into large bodies); 0 persistent predator splits; seed 32 moving prey tracks 26 and then 6, against 52 and 48 in the control (chiF0_s32.png, global_arms.png).
- *minor*: At 128^2, predator reproduction on fresh seeds is marginal: generation 1 on seed 31, below the gate of 2 from noise, and generation 2 on seed 32; merge/split is 0.54 on seed 31. This does not contradict the 256^2 packs (generation 4 and 3), but each predator divides rarely (about 0.02 persistent splits per predator per 1000 t). Evidence: rerun/seed31/FACTS.md: predator persistent splits 8, max generation 1, merge/split 0.538. rerun/seed32/FACTS.md: 10 persistent splits, generation 2, merge/split 0.353.
- *minor*: The named track (seed 0, 62->478) shows only I and D directly. Its X and E are inferred from population forks in other runs (128^2, drive.py). E is contradicted for predators of this kind by the k2 controls, so the track does not show IXDE together. Evidence: pack256/seed0/pred_ancestry.png shows 4 splits, each with the predator stretched between two prey. fork/ is at 128^2, seeds 0 and 1, not the track's run.
- *minor*: The predators' effect on prey goes in two directions: body number up only slightly at 128^2, condensed biomass down by more than half. The claim reports only the increase. Evidence: rerun/seed31 vs twin/seed31, t>=4000: prey condensed area 0.084 against 0.189; labkit prey mean 42.8 against 39.4 (+9%).

### replication (holds with caveats)

The claim replicates on fresh seeds, and nothing in S, I, X, D or E is by construction. The predator carries I, X, D and E together, but D is a joint fission with its prey, so the dividing unit is the prey-predator pair.

All files are under /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/digestion-ecology/replication/. Total compute was about 76 min wall on 2 threads, one simulation at a time.

**Replication.**
- Seed 33 at 256^2 matches the claim's seeds 0 and 1: predators 80 persistent tracks, 50 persistent splits, generation 4, merges/splits 0.26; prey 68 persistent splits, generation 4, 0.405.
- The matched twin is bit-identical through t=2000 and stays a frozen emulsion: 0 persistent prey splits and 2 moving tracks, against 68 and 319 with predators.
- Effect of predators on prey has mixed sign: more bodies (+13%), division and motion, but condensed prey area down 56%. Prey are obligate for predators.
- Prey removal on seed 34 (128^2) dissolves all 45 predators within 900 t with their material kept; the fed run keeps 43-53.

**New controls.** No review had run the rubric's local L4c test; I ran it in two forms:
- deleting single prey kills 3/3 targeted predators by t=6500-6700, while their fed twins persist and neighbours die at the fed rate;
- cutting the prey under a member of the deepest predator lineage kills that individual within 300 t, while its fed twin goes on to divide.

The c46 precedent applies to the predator's E: its matter is neither made from prey nor decays, and only its condensed state depends on q, a product made only by digestion. So E is not by construction.

**Main correction.** The collective read predator divisions as tears between two prey (c55: only 3/36 within ±1 frame of a prey split). With a lineage-aware test, 49/50 (seed 33) and 14/14 (seed 34) of the bridged prey pairs are sisters from one prey fission 200-900 t earlier. The prey, for their part, divide only with a predator on them (68/68; 0 in the twin). The pair also passes I and D on its own: 80.5% of union bodies are exactly one prey plus one predator, with 84 persistent tracks, 63 persistent splits and generation 4. The predator remains a valid L2 individual, an obligate symbiont or parasite.

**Other flaws.**
- labkit's frames.npz drops sim frame 60 when run with --frames 120. Every script that reads it labels times after t=6000 100 t early.
- The prey's E (fuel cut) has never been replicated on a fresh seed.
- The claim's dt/2 check is not matched to the default run and shows predator generation 1.

Flaws:

- *major*: Predator reproduction is not autonomous: it is a lagged co-fission with the host prey. The collective's reading that predators are 'stretched between two prey and tearing' rather than dividing with prey (c55: 3/36 within +-1 frame) is an artifact of the coincidence window. The two prey a dividing predator bridges are sisters from one prey fission 200-900 t earlier. Since the prey, in turn, divide only with a predator attached, D in this world is the joint fission of a prey-predator pair. The claim's own limits ('joint fissions') and c49, c53, c54 and c57 are right on this point. Evidence: sisters33.json / sisters34.json: 49/50 and 14/14 persistent predator splits bridge sister prey; lag 2-9 frames, median 4 (seed 33) and 3.5 (seed 34); 42/49 and 11/14 sister fissions are labkit persistent splits; 1/50 unrelated; 0 on one prey without a prey fission. tear33.json: sister distance 11.9 -> 17.0 px from 4 frames before the split to the split frame, increasing in 50/50. prehist33.png: every random gen>=3 split is preceded 800 t earlier by a single bean-shaped prey with the predator in its waist. Twin: 0 prey splits; 68/68 prey splits have a predator on the parent. c55's coinc.py uses abs(fp - f) <= 1, so it counts only simultaneous splits.
- *minor*: Every frames.npz-based script mislabels time and skips a frame. With --frames 120, labkit keeps only 120 of 121 frames in frames.npz and drops sim frame 60, so render index i >= 60 is sim frame i+1. This affects the claim's predlineage.py, splits3.py, strip.py and life.py, the reviewers' scripts, and my first audit_an.py. Times after t=6000 come out 100 t early, and tracking sees a 200 t gap between indices 59 and 60. Counts barely change, but fed-vs-fork comparisons aligned by index are off by one frame. Evidence: claim256/frames.npz and fed128/frames.npz: render_f = 0..59, 61..120 (len 120); dfork128 (90 frames) keeps all 91. labkit/run.py l.238 render_idx = linspace(0, frames, min(render_max, frames+1)). The claim's pred_ancestry times 7100/8600/9800 are really 7200/8700/9900. My fork_an.py aligns by render_f.
- *minor*: The prey's E ('each kind dissolves when its own supply is cut') has never been replicated. No review and not this audit re-ran the fuel-cut fork on a fresh seed. Evidence: c49, c51, c53, c55 and c57 list the prey fuel cut as not run, and c54 ran no forks. The only evidence is the claim's fork/ffork_s0 and ffork_s1 (drive.py counts, 128^2) and c46's finding in a different parameter set.
- *minor*: The claim's dt/2 check is not matched to the default run and is weak for D. It covers sim t=8000 (160 frames at dt 0.1, labkit reports t=16000), and its K=20 frames is 1000 sim t, half the default window. There predators show 6 persistent splits and generation 1. No review and not this audit ran a dt/2 or grid variant at matched duration. Evidence: dthalf/seed0/FACTS.md: '161 frames x 500 steps x dt 0.2 = time 16000; grid 128', predator persistent splits 6, max generation 1; versus fed128 seed 34 at dt 0.2: 15 persistent splits, gen 3 over t=12000.
- *minor*: The claim's track field asserts E for the named seed-0 predator from the population fork only. None of the six reviews ran a local or per-individual E test. The fork alone is a population result: it would also pass for any condensate whose condensed state needs the removed species. Evidence: contribution.json track text ('it exists only while digesting (dfork: every predator dissolves...)'). The individual-level evidence is in this audit only: local34.json (3/3 targeted predators die, neighbours 16/42 vs 14/42 lost as in the fed twin) and lincut34.json (lineage track 100 dies by t=7900; its fed twin co-fissions at t=8500).
- *minor*: The X effect on prey has opposite signs on different measures, and the claim reports only the positive ones. Predators raise prey number, division and motion but cut condensed prey biomass by more than half. Evidence: twin33.json, t >= 6100: bodies 183 vs 162 (+13%), condensed area 5557 vs 12590 px (x0.44), median body 28 vs 80 px; agrees with c57 (0.085 vs 0.192).
- *minor*: The mean c_b values the claim and reviews quote to show 'material kept' are clipped values, so they drift even though the predator material is exactly conserved. Evidence: fed128 t=5900: 28.2% of pixels have c_b clipped to 0 (phi_b < -1 depletion halos). After dissolution (dfork, t=9000) 0% are clipped and c_b ranges 0.053-0.144, so the clipped mean drops 0.106 -> 0.0959 with no matter lost. world.py step(): phi_b changes only by Mb lap mu_b and a conservative MUSCL flux (k=0 mode unchanged).
- *minor*: Hunting relies on a written nonreciprocal drift of predator material down the fuel gradient (chiF 0.5). It is not a by-construction mark under the collective's rule, but it matters for the mechanism score, and without it the claim reports no persistent predators. Evidence: world.py: taxis = 2*vf_flux_div(cb, -F, chiF) acts on predators only; claim limits: with chiF 0 'predators nucleate inside prey, eat them and dissolve'.

### individuality (fails)

Fresh seeds 35 and 36 (labkit, 128^2, t=12000, 1 thread), measured per track and merge-aware, plus local and global operator forks; about 64 minutes of compute.

The predator body meets the L2 numbers: its own conserved material, life about 3000-4300 t against formation under 100 t, about 26 px and bounded. It is attached for essentially its whole life to one prey lineage. It divides only as the second half of a pair fission:
- 15 of 17 persistent predator splits are tears between sister prey 300-700 t after the prey split; 2 are pinches with a dividing prey; none happen otherwise.
- All 23 prey divisions are bridged by one predator and produce two prey-predator pairs carrying the parent's predator.
- Daughters never re-merge, and 16 of 17 are attached to different prey bodies at +2000 t.
- Labkit predator generation is 3 on seed 35 (merge/split 0.588) but only 1 on seed 36, so D replicates on 1 of 2 seeds at 128^2.

The decisive new result is on E. Removing one predator's prey kills it within 400-600 t while its neighbours live, which reproduces the claim's dependence. But switching digestion off with the prey kept leaves the predators alive on both seeds: 49 of 47 and 49 of 46 bodies at +2000 t, and 2 of 2 under a local block. Their max c_b settles at 1.0 and they become round cores held inside each prey by the written fuel-depletion taxis. Switching off digestion and the taxis together reproduces the prey-removal die-off exactly (0 by +800 t). So the predator does not depend on consuming its resource, and the c46 precedent does not carry over: c46's prey have no second, written holding term.

About half of new predator bodies also condense de novo on bare prey from diffuse predator material.

X is real and matched; my digestion-off arm shows consumption carries it. Under the pair reading, though, X has no control.

The predator therefore does not carry IXDE, and the claim fails as stated for its named predator track. The prey (c56's separate claim) is the only entity that meets I, X, D and E by the gates' letter. That holds only with the caveat that every prey division is a cut made by its predator in a joint pair fission.

Flaws:

- *critical*: The predator's E is not metabolism. The predator survives without eating; its dependence on prey comes at least as much from the written nonreciprocal fuel-depletion taxis (chiF 0.5) as from digestion. The claim's control (remove all prey) removes both. The claim's statement that the predator 'exists only while digesting' is false. Evidence: lcut/arms_s35.json and arms_s36.json (forks at t=6000, 128^2): k2=0 gives 47->49 and 46->49 predators at +2000 t, fed 52 and 50, max c_b 1.0. k2=0 plus chiF=0 gives 47->31->0 and 46->28->0 by +800 t, exactly the prey-removal curve. chiF=0 alone gives 47->38 and 46->34. lcut/dig_s35.json: local digestion block, 2/2 predators alive at +2000 t. lcut/k2off_snap_s36.png: without digestion, every prey holds a round predator core.
- *major*: Predators never divide on their own: every persistent predator split is the second half of a pair fission that starts with the prey dividing around the predator. c55's '3/36 coincide' (a +-1 frame window) misses that the two prey a predator is torn between are sisters. Evidence: indiv_s35.json and indiv_s36.json: 15/17 torn between sister prey 3-7 frames (300-700 t) after the prey split, 2/17 pinched with a dividing prey, 0 between unrelated prey, 0 on one prey without a prey split. Prey splits: 23/23 bridged by one predator, and 23/23 give two pairs carrying the parent's predator (pairdiv_*.json). Images: s35_cycle101.png, s35img_ancestry.png.
- *major*: Predator D does not replicate on one of my two fresh seeds at 128^2, and its genealogy is reticulate on the other. Evidence: Seed 36 labkit: predator 6 persistent splits, generation 1; prey 12, generation 1 (s36/FACTS.md). Seed 35: predator gen 3 with merge/split 0.588 (>0.5 caps confidence at medium); prey merge/split 0.806. Lineages are partly broken by torn fragments that fall below 6 px and re-emerge as 'nucleations' (8/23 daughter predators).
- *major*: Many predator bodies arise without a parent: diffuse predator material condenses de novo on bare prey. Together with the taxis-held cores, the predator is partly a written accumulation of a shared conserved pool at prey fuel sinks rather than a self-propagating lineage. Evidence: pred_births_after_t3000 in indiv_*.json: labkit nucleations reaching >= 10 frames 46/51 vs splits 30/23. Of the nucleations, 31/40 have no track ending within 12 px in the previous 5 frames and appear from c_b < 0.25 within 100-200 t (nucorig.py, nucback.py), on prey that carried no predator (46/46, 47/51). Images: s36_nucview.png.
- *minor*: Under the pair reading X is untested, and c57's remark that an inert-predator arm 'reduces to the twin' is wrong: k2=0 with predator material present is a distinct arm. It shows the prey's motion and division come from consumption. Evidence: lcut/k2off_snap_s36.png: with predator cores present but not eating, prey are static by t=7000-8000; c57 contribution.json limitation.
- *minor*: The named predator track (seed 0: 62->230->365->424->478) shows S, I, D (each split is a bridge torn between two prey in pred_ancestry.png) and population-level X. Its E rests on 128^2 forks of other runs, which by the critical flaw do not show dependence on consumption. Evidence: pack256/seed0/pred_ancestry.png rows 3700, 7100, 8600, 9800; fork/forks.png (128^2, seeds 0/1).

Files: construction/ (arms from t=6000, formation with digestion off, split tracing), replication/ (fresh-seed checks, local cuts, sister-prey tracing), individuality/ (per-track census, digestion-off arms), rerun/seed33 and rerun/twin_seed33 (labkit packs, 256^2; frames.npz not kept). The auditors' full working directories are the operator's; scripts are included where small.