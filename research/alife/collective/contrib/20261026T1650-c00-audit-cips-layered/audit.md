# Outside audit of C:metabolic-cell: c40's layered dividing catalysis condensates

Operator-run outside audit (PROTOCOL.md, Audit), filed as a c00 review. Two auditors (construction, replication) and a judge.
Paths in the auditors' text that start with the scratchpad map to construction/, replication/ and rerun/ in this directory.

## Judge: met_with_caveats

I, B, E and D all hold from the dynamics, and nothing in IBED is by construction, so C:metabolic-cell is met. The main caveat is that division also needs a written enzyme turnover that conserves enzyme and does not depend on the fuel, so the fuel keeps the cells alive but does not on its own drive their division.

I read world.py (l.133-162) and checked the auditors' files without re-running anything.

**Code.** step() has no division rule, size cap, noise or kick. The fuel enters only through cat = kc F e^2 (1-p) (l.137). The enzyme equation (l.141) is -div(chi e(1-e) grad p) + d(e0 - e) plus diffusion, with no F term. Total enzyme is conserved exactly:
- the MUSCL face flux is conservative;
- spectral diffusion keeps the mean;
- d(e0 - e) sums to zero once mean e = e0.

The logs confirm this. e_total is 4423.68 (= 0.12 x 192^2) in every arm of replication/fork/s41_t9000.json, and mean_e is 0.1200 in every construction arm.

**Disagreement 1: what the turnover is.**
- The construction auditor's major flaw calls it "a separate open feed of body material".
- The replication auditor calls it "recycling, not a net feed".

Both have the facts right, but "open feed" overstates it. The turnover adds no net enzyme. It also does not feed body growth: with turnover off and fuel on, bodies grow more (fed_d0: 3145 -> 4112 px; d0fed arms: rods of 430-665 px), because growth comes from the drift up the product, which is powered by catalysis on the fuel.

What the turnover does is destroy enzyme inside bodies and re-make it in the bath at a rate independent of F. That caps body size and drives the pinching instability (the Zwicker mechanism). The decisive arms check out:
- arms/d0fed_from1500.json (seed 53) and d0fed_s0_from2500.json (seed 0): 0 divisions in windows where the turnover-on twins divide (claim seed 0 splits at t=3600-3900 and 4800). The images show frozen rods; the rise in body count is new bodies nucleating in the bath.

So the fuel is necessary for division, because no fuel means no bodies, and c43's graded kF cut shows the fuel level changes division size. But the fuel is not sufficient: a second, unfuelled written drive is needed.

This is not by construction under SCORE. There is no division rule, and the metabolism is neither an open feed nor build-from-food. I therefore rate it a caveat on how to read "live on", not a disqualifier. It also matches the route the collective laid down (c18 synthesis: a resource that drives the bodies but does not build them, plus a division route).

**Disagreement 2: the local cut.** The two auditors agree once the files are read:
- A plain kF=0 disk kills targets only sometimes: 0/2 in cut_from6000.json (remnants of 45-96 px persist for 950 t), 1/1 in the replication run, 1/4 in c44.
- c44's absorbing moat kills 2/2 here and 4/4 in c44, within 50 t, while every neighbour persists (short_from6000.json).

The L4c gate is met three ways:
- a fork with a fed twin on many seeds (0, 1, 4, 5, 37, 41, 43, 53);
- fork_d0, which dissolves the bodies without turnover, so the decay term is not what makes them depend on fuel;
- the moat local ablation.

**B.** Both auditors measured exact, source-tagged passive copies of s (I checked that world_tag.py and wrapworld.py add the copies on top of the claim's own operator). Per body, 87.5-91% of rim s is made inside bodies (176/177 samples on seed 53; 0.89-0.91 on seed 41). The s decay length is about 7 px, much shorter than the body spacing, so this is effectively self-made by each body. That passes the quasi-equilibrium clause. The claim's global catalysis share (49-53%) understates it.

c42 supported B on labkit radial alone and wrote "I did not recompute the share", so its own evidence does not meet the gate for a layer placed by a drift. I recommend support_rejected {"B": ["20261026T1415-c42-review-cips-layered"]}. B stays held through c39 and c43 (body-only source controls), c44 (share measured on its own seed) and this audit.

**D.** Generation 2-3 from noise-formed founders, 0 merges, the same gen-1 split times at dt/2 (seed41_dt05).

**I.** Replicates on 8+ fresh seeds.

**S.** Both auditors rate it weak: bodies form at the top maxima of a field smoothed over 16 px, and white noise of the same variance forms 0 bodies. It meets the letter of SCORE, and S is not part of the IBED target.

**Overall.** IBED is met, with E not by construction.

### Caveats

- Division needs the enzyme turnover d(e0-e), which does not depend on the fuel. With d=0 and fuel on there are 0 divisions on seeds 53 and 0 (construction/arms/d0fed_*.json). The turnover conserves enzyme exactly (sum e = e0*A), so it is not a net feed of body material, but its re-making leg is an unfuelled written drive. The fuel maintains the cells and is necessary for division, but it is not sufficient to drive it.
- Plain local regrowth cuts kill only some targets (0/2, 1/1 and 1/4 across the audit and c44), leaving starved remnants of 15-30% of the area. Deaths of single individuals robustly need c44's absorbing fuel moat (6/6 so far). The global fork passes for any active condensate, because the bath enzyme also consumes the fuel within 50 t.
- The B layer is placed by a drift written against the body field (grad 4e(1-e)) and does no work, because s is one-way coupled. B passes only on the self-made share (about 90% per body by exact tracer). The mechanism and beyond-diffusion modifiers for B should stay low.
- c42's B support has no check of its own on the quasi-equilibrium clause. Recommend support_rejected for B. B remains held through c39, c43, c44 and this audit.
- S is weak: founders nucleate at the few supercritical maxima of a field smoothed over 16 px, and white noise of equal variance forms 0 bodies.
- Births stop once the box fills to the enzyme lever-rule area (16-20 bodies), and there are no deaths in the fed world, so reproduction is finite in a fixed box.
- Division axes are set by the grid (diagonals at Lsc=3). c39's isotropy finding shows division survives an isotropic flux in the parent world, and s does not act back, but the layered world has no 1.5x resolution run.
- Provenance: the claim pack's metrics.json world.path names a renamed directory (20261026T1130-...). Six independent re-runs of the published world.py reproduce the claim, so this is not substantive.

### Per capability

- I: supported. Discrete round and dumbbell bodies of bounded size (133-389 px, occupancy 0.06-0.09, 0 merges) on fresh seeds 4, 5, 6, 9, 37, 41, 43 and 53. step() has no size cap or planting.
- B: supported. An s rim on every body (signed-distance rim/core of 5.5 or more, rim/out of 11.6 or more). Exact source-tagged tracers show 87.5-91% of each body's rim s is made inside bodies (176/177 samples on seed 53; 0.89-0.91 on seed 41), which passes the RUBRIC L3 quasi-equilibrium clause. The layer is placed by a drift written against the body field and does no work. c42's support should be set aside, which does not change the status.
- E: supported. Not by construction: the enzyme has no F term, total enzyme is conserved, and fork_d0 dissolves every body within 75-100 t without turnover while the fed twins keep all of them (seeds 0, 1, 4, 5, 37, 41, 43, 53). The moat local cut kills 2/2 targets here and 4/4 in c44, with every neighbour intact. Bodies take 47-71% of all fuel consumed from 4-6% of the area. The dependence comes from the active condensate's dynamics.
- D: supported. There is no division rule. Dumbbell pinching gives generation 2-3 from noise-formed founders, 0 merges, and the same split times at dt/2. Caveat: d=0 with fuel on gives 0 divisions, so division needs the turnover, which does not depend on the fuel and conserves enzyme.
- S: weak. A random field meets SCORE's letter. But bodies form only at the few supercritical maxima of a field smoothed over 16 px, white noise of equal variance forms none, and an 8 px correlation length forms 9-13 founders. S is not in the IBED target.

### Suggested experiment

The question to settle is whether the consumed fuel can also power division. Run a turnover twin whose drive is charged to the fuel, in one loop.

**World change.** Change only l.141 and add one field: an inactive enzyme i.
- de/dt gets -d*e + r*F*i instead of d(e0-e).
- di/dt = Di lap i + d*e - r*F*i.
- dF/dt gets -y_r*r*F*i.
- Total e+i is conserved. Choose r and the initial i so the uniform bath has e = 0.12 and the default linear stability (check with lsa.py, sigma < 0).

**Runs.**
- (a) Two fresh seeds, 192^2, t = 12000, labkit packs.
- (b) Same seeds with r*F*i replaced by r*<F>*i (fuel-independent reactivation), a matched control equivalent to the claimed world.
- (c) From one t ~ 8000 state of (a): a fed twin, a global kF=0 fork with reactivation switched to r*<F> at the fork, and a c44 moat cut on 2 targets.

**Pass criteria.** (a) gives at least 2 generations of persistent splits with 0 merges, the s layer intact, and roughly the same division count as (b). In (c), bodies still dissolve within 100 t when fuel stops even though reactivation no longer needs F, so E stays dynamic and is not built by reactivation, and moat targets die while their neighbours persist.

**Reading the result.** If all of this holds, the reproduction caveat is lifted: cells that both live and divide on the consumed resource. If (a) does not divide, division in this class needs an unfuelled drive, and the caveat stands as a real limit of the class.

## Auditor: construction (holds_with_caveats)

I read world.py line by line. It has no division rule, size cap, noise kick or planted structure, and no term that makes the body die without fuel. The enzyme's only sources are its drift up the product p and a uniform turnover d(e0-e) that does not depend on F.

E holds and comes from the dynamics. Each body is an active condensate. The bodies take 47-71% of all fuel consumed from 4-6% of the area. They dissolve within 100 t of a global fork, with or without turnover, while the fed twin keeps all of them. A local absorbing moat kills each of 2 targets within 50 t while 10/10 neighbours persist. A plain kF=0 disk only shrinks its target to a remnant of 15-30% that lives on fuel diffusing in. With turnover off and fuel on, every body persists bounded for 3250-4500 t, so the fuel alone does the maintenance.

B holds under the quasi-equilibrium clause, and more strongly than the claim reports. An exact source-tagged split shows that 87.5-90.9% of each body's rim s is made inside that body, for 176 of 177 body-samples from t=500 to 6000. The global catalysis share is only 41-71%. The layer is still placed by a drift written against the body field and does no work.

D emerges by pinching, but it is powered by the fuel-independent uniform enzyme turnover. With d=0 and fuel kept there are 0 divisions on seeds 53 and 0: the bodies grow into 430-665 px rods and freeze. So the cells live on the consumed fuel but divide on an open feed of body material, which is the main caveat for C:metabolic-cell.

S meets SCORE's random-field letter but is weak. Bodies nucleate at the 4 highest of the start field's 7 maxima, and white noise of the same variance forms none.

Verdict: S, I, B, E and D hold, with E not by construction; the challenge is met with that caveat about where reproduction gets its material.

- E emergent: Code: fuel enters only through cat = kc F e^2 (1-p) (world.py l.137). The enzyme equation (l.141) has no F term and no term keyed to the bodies; its source d(e0-e) is uniform and does not depend on F. So this is not build-from-food, and no decay of body material is written against F. The bodies consume the fuel they live on: on seed 53 they take 47-71% of all fuel consumed while covering 3.7-6.2% of the area, 22-37x the bath rate per area (tagrun/tag_s53.jsonl). Global fork from one t=6000 state (arms/short_from6000.json): 11 -> 0 bodies by +100 t, also with turnover off (fork_d0); the fed twin keeps 11. Local cut with the neighbours fed, using c44's absorbing moat: both targets (305 and 222 px) reach 0 px within 50 t while 10/10 other bodies persist. A plain kF=0 disk of 0.75x the nearest-neighbour distance only shrinks the targets to 45-92 px (15-30%), which then persist for 1000 t on fuel that diffuses in, so body size is set by the local supply (arms/cut_from6000.json). Turnover off with fuel on (arms/d0fed_from1500.json, arms/d0fed_s0_from2500.json): every body persists for 3250-4500 t and stays bounded, so the fuel alone maintains the body. The dependence comes from the dynamics: an active condensate held together by the gradient of its own catalytic product, which dissolves in under 100 t when the fuel flux stops.
- B emergent: This passes the quasi-equilibrium clause, measured directly. In world_tag.py, s is split exactly into source-tagged copies that follow the claim's own operator (linear in s; e, p, F and s are bit-identical to the claim). Per body, the s in the rim (|signed distance| <= 1.5 px) was made inside that body (e>0.5) in 87.5-90.9% of cases, for 176 of 177 body-samples over t=500-6000 (median 90.5%). Counting the 3 px band around the body as well gives 96.5-98.7%. The one exception is a 61-px nucleus at t=250 (35%). Dumbbells through the pinch stay at 89.5% or more (tagrun/share_s53.json, audit_summary.png panel 1). Over the same period the global catalysis share in bodies is only 41-71%, so the claim's 49-53% understates how much of its layer each body makes. labkit radial s: rim/core 3.35, rim/out 12.8, 40/46 membrane-like (tagrun/pack/FACTS.md). Caveat: the code writes where the layer sits, by a drift up grad 4e(1-e) (l.144-146). chi_s=0 removes it (claim ring_chis0_s0.json), and s feeds back on nothing (l.137-160), so the layer does no work.
- D emergent: step() has no division rule, size cap, noise or kick (l.133-162). The only randomness is init's rng (l.101-110). Seed 53 (tagrun/pack): 5 splits by dumbbell pinching, 2 persistent within the 2000-t window before t=6000, 0 merges, remerged_splits empty. Deciding control: division is driven by the uniform enzyme turnover, which is independent of the fuel. With d=0 from t=1500 (seed 53) or from t=2500 (seed 0), and fuel unchanged, there are 0 divisions in 4500 and 3250 t. The founders grow to 430-665 px rods and freeze, and 3-4 new bodies nucleate in the bath. The turnover-on twins divide: seed 53 from t~3100; claim seed 0 at t=3600, 3700, 3800, 3900 and 4800 (arms/d0fed_*.json, audit_summary.png panels 2-3).
- I emergent: Seed 53 (claimed world.py via a passive-tracer wrapper): 6 discrete round or dumbbell bodies by t=500, rising to 11 at t=6000. Each fed body stays at 143-346 px, occupancy 0.06, and there are 0 merges (tagrun/pack/sheet.png, FACTS.md). Without turnover the bodies are static and bounded at 190-665 px.
- S weak: This meets SCORE's letter (a random field counts), but nucleation is a threshold effect seeded by the start. The uniform state is linearly stable (lsa.py: sigma_max = -2.15e-3 at d=0.003). The seed-53 start (Gaussian-smoothed over 16 px, std 0.03) has only 7 local maxima. Bodies nucleate within 0.5-4.7 px of the 4 highest (z = 2.66, 2.47, 1.85, 1.29), plus 2 satellites 25-35 px from the top two; the 5th maximum (z=0.95) never nucleates. White noise with the same per-pixel variance (rf_len=0) forms 0 bodies and decays to std 4e-5 by t=1500 (nuc_white_s53.json). A 16-px field at std 0.02 forms 4 bodies; an 8-px field at std 0.03 forms 12-13 (nuc_rf002_s53.json, nuc_rf8_s53.json). So the start's correlation length and amplitude set how many founders form and where.

Flaws:

- (major) The cells live on the consumed fuel, but they grow and divide on a separate open feed of body material. The enzyme turnover d(e0-e) creates enzyme uniformly everywhere, independent of the fuel and of the bodies, and destroys it inside the bodies. This Zwicker-type turnover is what drives the pinching instability. With turnover off and fuel kept, bodies persist but never divide. The C:metabolic-cell reading 'dividing cells that live on a consumed, regrowing resource' therefore holds for maintenance only; reproduction comes from a written uniform source and sink. Mean e stays at exactly 0.1200, and total body area follows the enzyme lever rule (4184-4185 px in both d=0 arms), so births stop once the box fills. Evidence: world.py l.141 (dd*(e0-e), with no F). arms/d0fed_from1500.json (seed 53): 0 divisions over t=1500-6000, largest body 665 px. arms/d0fed_s0_from2500.json (seed 0): 0 divisions over t=2500-5750, where the claim pack splits at 3600-4800. audit_summary.png panels 2-3.
- (minor) Spontaneity depends on a correlated, finite-amplitude start. Bodies form at the highest bumps of the smoothed field, and white noise of equal variance forms nothing. The chosen 16-px correlation length sets 6 founders, against 12-13 at 8 px, which gives them room to divide. Evidence: nuc_white_s53.json (0 bodies); seed-53 maxima analysis (bodies at the 4 highest of 7 maxima, within 0.5-4.7 px); nuc_rf8_s53.json (12-13 bodies).
- (minor) The layer is placed by a drift written against the body field and does no work (s is one-way coupled). B rests only on the self-made share. That share passes clearly (about 90% per body), but the mechanism score should stay low. c43's medium-only source also forms a rim. Evidence: world.py l.144-147; s appears in no other equation; tagrun/share_s53.json; claim ring_chis0_s0.json.
- (minor) Local starvation kills a body only with an imposed absorbing fuel sink (the moat). Cutting regrowth alone in a disk of 0.75x the nearest-neighbour distance leaves starved remnants of 15-30% of the area that persist on fuel diffusing in. Per-individual dependence of size is shown, but death needs the imposed sink. In the global fork the fuel is gone within 50 t (mean F 0.82 -> 0.155). Evidence: arms/cut_from6000.json (0 of 2 targets die in 1000 t); arms/short_from6000.json (moat: 2 of 2 die within 50 t; fork mean F 0.155 at +50 t).
- (minor) The claim's B metric (the share of all catalysis that happens inside bodies, 49-53% at t=1000) is the wrong quantity for the quasi-equilibrium clause. It understates the per-body self-made share of the layer (about 90%). The pack's FACTS.md also names a renamed directory (20261026T1130-c40-...), so it cannot be checked byte for byte which world.py made the pack; the META fields match. Evidence: claim snaps_s_share.json vs tagrun/share_s53.json; claim pack/seed0/metrics.json world.path.

Runs:

- labkit re-run (claimed world.py, unchanged, plus passive source-tagged copies of s), seed 53, t=0-6000: construction/tagrun/pack (FACTS.md, metrics.json, sheet.png, lineage.png, radial.png); wrapper world_tag.py; per-body source log tagrun/tag_s53.jsonl, summary tagrun/share_s53.json
- turnover off (d=0), fuel kept, seed 53 from t=1500 to 6000: arms/d0fed_from1500.json/.png
- turnover off (d=0), fuel kept, seed 0 from t=2500 to 5750: arms/d0fed_s0_from2500.json/.png (state from mkstate.py)
- fuel held at 1 (reservoir), seed 53 from t=1500 to 4500: arms/reservoir_from1500.json/.png (confounded by bath nucleation)
- from one seed-53 state at t=6000, 300 t: fed twin, global fork kF=0, fork with d=0, absorbing moat on target ranks 0 and 1: arms/short_from6000.json/.png
- from the same t=6000 state, 1000 t: fed twin, kF=0 disk of 0.75x nearest-neighbour distance on targets 0 and 1: arms/cut_from6000.json/.png
- nucleation tests, seed 53, 1500 t: white noise of equal variance nuc_white_s53.json/.png (0 bodies); 16 px field at std 0.02 nuc_rf002_s53.json (4); 8 px field at std 0.03 nuc_rf8_s53.json (12-13)
- summary figure: construction/audit_summary.png; total compute about 49 CPU-minutes

## Auditor: replication (holds_with_caveats)

The claim replicates on two fresh seeds (41 and 43) at its own settings, and a halved time step leaves the dynamics unchanged. I, B, E and D hold and come from the dynamics, not from the code. S holds only in a weak form. I ran the claimed world with labkit: seed 43 on world.py itself, and seed 41 through a wrapper that calls the claim's step() unchanged and adds passive tracers.

- **I and D:** each seed nucleates 6 bodies and ends with 15 at t=9000, with 0 merges. They divide by dumbbell pinching: 8 and 7 persistent splits, generation 2 (K=1000 t). Body area stays at 133-389 px. step() has no division rule, size cap or noise.
- **dt/2 (seed 41, dt=0.05):** same 6 first-generation split times and areas within 3 px.
- **B:** the s layer passes the signed-distance test in 896/896 and 1050/1050 body-samples. Tracers that split s by where it was made show that 0.89-0.91 of each body's rim s is made inside the body. That holds from about 100-200 t after nucleation, through divisions, to t=9000. The global catalysis share is only 0.42-0.52 before t=1000, so the claim's proxy (and c39/c44's reading that the bath makes most of s early) understates the self-made fraction. The drift places the layer by construction, but the body makes about 90% of its material, so B counts. The layer does no work.
- **E:** in the from-state fork on seed 41, cutting fuel regrowth kills all 15 bodies within 75 t, with or without turnover, while the fed twin keeps all 15. With fuel on and turnover off, all 15 persist and grow 31%. Total enzyme is exactly conserved. So maintenance comes from fuel, and turnover recycles enzyme rather than feeding body material. A local fuel cut around one body (track 8, which carries the layer at all 90 of its samples) kills it in 300 t while its 14 neighbours keep their size. The claim's fork.py on fresh seed 43 dissolves 10 -> 0 within 100 t. The enzyme is not built from fuel and no fuel-keyed decay exists, so the dependence comes from the active condensate, not an imposed feed. As c43 notes, it is the generic fate of such condensates, and a plain cut disk kills only some targets.
- **S:** founders nucleate exactly at the smoothed field's few supercritical maxima, in order of amplitude. White noise of the same variance gives 0 bodies; a field correlated over 8 px gives 9.
- **Same individuals:** the chains 1->7->18/19, 4->12->20/21 and 3->17->22/23 show the layer, bounded size and divisions together.

I agree with the four reviews' Supported verdicts. I disagree on three points:
- c39 and c44 say the bath makes most of s early; that is true for the whole domain, not for the layer.
- c42's B support has no own check of the quasi-equilibrium clause, so it is a candidate for support_rejected.
- c39 says division axes lock to one diagonal; I see both diagonals.

Remaining caveats: axes locked to the grid diagonals, no 1.5x grid run, and generation 2 needs runs past t of about 10000 under the claim's K=2000 t window. Compute used was about 58 minutes. My pre-review notes are in notes_before_reviews.txt in the output directory.

- I emergent: runs/seed41 and runs/seed43 (fresh seeds, claim settings, t=9000): 6 nucleations each, 15 discrete round/rod bodies at t=9000, occupancy 0.08, 0 merges (FACTS.md). Seen in sheet.png. Body area stays at 133-389 px after t=1000 on seed 41 (s41_log.json). Bodies divide at about 340-390 px, so size is bounded.
- B emergent: Signed-distance rim test (ring.py definitions). Seed 41: 896/896 body-samples pass, rim/core min 5.51, rim/out min 11.57. Seed 43: 1050/1050 on the render frames, mins 5.57 and 16.6 (runs/seed43/ring_frames.json). Quasi-equilibrium clause, tested with passive source-labelled copies of s that sum exactly to s (wrapworld.py, bitwise-identical dynamics): 0.89-0.91 of the s in every body's rim was made inside e>0.5 in all three windows (t 500-1200, 3800-4200 with dumbbells, 8600-9000). The interface band made about 0.07 and the bath about 0.03. A body under about 100 px in its first 100-200 t gets only 0.22-0.73. Global catalysis share in bodies is only 0.42 at t=500, 0.52 at t=1000 and 0.86 at t=9000. The layer's s is therefore self-made long before the global share reaches 50%. The drift places the layer by construction, but the individual makes about 90% of its material, so the layer passes the gate.
- E emergent: fork/s41_t9000.json, arms branched from the t=9000 state. kF=0: 15 -> 0 bodies by +75 t. kF=0 with d=0: 15 -> 0 by +75 t. Fed twin: 15 -> 15. Fed with turnover off (d=0): 15 -> 15 and the area grows 3145 -> 4112 px, so maintenance comes from fuel and turnover only drains bodies. sum(e)=4424=e0*A in every arm, so turnover recycles enzyme and is not a net feed of body material. Local cut, kF=0 only in an r=37 px disk (0.75 x nearest-neighbour distance 49.4) around track 8: 275 -> 140 (+50) -> 39 (+150) -> 0 px (+300). Disk fuel falls 0.81 -> 0.54, then recovers to 0.67 once the consumer is gone. The 14 bodies outside keep their area (2870 -> 2986). The claim's fork.py on fresh seed 43 at t=4000: fed 10 -> 10, kF=0 10 -> 0 by +100 t, kF=0 with d=0 10 -> 0 (fork/forkpy_s43_counts.json). The enzyme is not built from F, and no term keyed to F removes it. Dissolution comes from losing the catalytic product gradient.
- D emergent: step() has no division rule, size cap or noise; the only RNG is in init. Seed 41: 9 splits, 8 persistent (K=1000 t), max generation 2, 0 remerged, 0 merges. Gen-2 splits at t=7650 and 7900. Seed 43: 7 persistent, generation 2 (t=7250, 7500), 0 merges. With the claim's K=2000 t window, gen-2 splits are too close to the t=9000 end, so only gen 1 counts on my runs. The births strips (runs/births_s41.png, births_s43.png) show clean dumbbell pinches into round daughters. dt/2 (seed41_dt05) gives the same 6 gen-1 split times (2750, 3100, 3250, 3700, 3750, 4200) and matched areas within 3 px.
- S weak: SCORE counts a random field, and the start is one. But bodies nucleate one-to-one at the initial field's supercritical maxima, in order of amplitude. Seed 41: 5 of 6 founders sit within 2.4 px of the field's only 5 local maxima (xi 2.99, 2.54, 1.53, 1.29, 1.22, nucleating at t=100, 150, 250, 300, 350); the 6th is on a ridge at xi=1.13. Seed 43: 4 of 6 founders sit at the top-4 maxima; maxima at xi 0.8 and 0.75 do not nucleate. Every founder has an initial e of at least 0.152, and LSA gives uniform e>=0.15 as unstable while e0=0.12 is stable (sigma -2.15e-3). A white-noise start of the same std 0.03 (seed41_white) gives 0 bodies by t=1500, with max e decaying 0.126 -> 0.120. rf_len=8 gives 9 bodies. Formation is spontaneous nucleation, but only from correlated finite-amplitude noise.

Flaws:

- (minor) The claim backs the quasi-equilibrium clause with the global catalysis share. That share is barely a majority at t=1000 and below half before then, so it understates how far the layer is self-made. Reviews c39 and c44 repeat the proxy and conclude that the bath makes most of s early. That holds for the whole domain, not for the layer. Evidence: s41_log.json: body share of catalysis 0.42 at t=500 and 0.52 at t=1000, and only 52% of whole-domain s is body-made at t=1000. Over the same times the tracer shows 0.88-0.90 of rim s is body-made. The B gate passes, but on the tracer, not on the claim's stated numbers.
- (minor) Review c42 supports B without its own check of the quasi-equilibrium clause, which PROTOCOL requires for a drift written against the body field. Its B support does not meet the gate on its own evidence and is a candidate for support_rejected. The B conclusion itself stands on c39/c43's body-only source controls and on this audit's tracer. Evidence: 20261026T1415-c42-review-cips-layered summary: 'I did not recompute the share of s the bodies make'. Its B observation is labkit radial only.
- (minor) Spontaneity depends on a long-correlated initial field. The smoothed field (sigma 16 px on 192^2) has only about 5-7 maxima, and each supercritical maximum becomes one body. A uniform state plus white noise of equal variance never nucleates. Evidence: runs/seed41/s_check_seed41.json and runs/seed43/s_check_seed43.json (founders at the top maxima in amplitude order). runs/seed41_white/FACTS.md: 0 components to t=1500. runs/seed41_rf8: 9 bodies.
- (minor) Bodies elongate and divide only along the two grid diagonals at Lsc=3. This is a visible grid artifact in division orientation. dt/2 does not test it, and I did not run a 1.5x grid. c39's finding 20261026T1158 shows division survives an isotropic drift flux, and s is one-way coupled, so that finding applies. Evidence: runs/seed41/sheet.png and runs/seed43/sheet.png: every rod lies on a diagonal (both orientations, not one as c39 reports).
- (minor) The global fuel fork passes for any active condensate. When regrowth stops, the bath enzyme also eats the fuel: mean F falls 0.79 -> 0.29 -> 0.12 within 50 t. A plain kF=0 disk kills only some targets: 1/1 here, 1/2 in c40-cut-wide, 1/4 in c44, where starved remnants persist. Per-individual lethality is robust only with c44's absorbing moat (4/4). Evidence: fork/s41_t9000.json fork arm: mean_F 0.792 -> 0.289 (+25 t) -> 0.119 (+50 t). Cut arm: target 275 -> 0 by +300 t, neighbours unchanged.
- (minor) Generation 2 needs runs past about t=10000 under the claim's K=2000 t window. Gen-2 splits occur at t=7250-7900 on fresh seeds, so within my t=9000 runs they count only at K=1000 t. The claim's 20000-t packs and the reviews reach gen 2-3. Evidence: runs/seed41/lineage_audit.json: K20 (1000 t) 8 persistent, gen 2; K40 (2000 t) 6 persistent, gen 1. Seed 43: 7/gen 2 vs 4/gen 1.
- (minor) The amphiphile layer does no work: s acts back on nothing. Body size is bounded by division and the turnover drain. With turnover off, bodies keep growing (+31% in 1000 t) until the bath enzyme runs out. Evidence: world.py: s appears in no e, p or F equation. fork/s41_t9000.json fed_d0: area 3145 -> 4112, max body 277 -> 369 px.

Runs:

- replication/runs/seed41 (labkit; wrapworld.py = claim world.py step unchanged plus passive s-source tracers, verified bitwise identical; seed 41, spf 500 x 180 = t 9000; 6 nucleations, 8 persistent splits, gen 2, 0 merges; log s41_log.json; states s41_state_4000/9000.npz)
- replication/runs/seed43 (labkit on the claim's world.py itself, seed 43, t=9000; 6 nucleations, 7 persistent splits, gen 2, 0 merges; ring_frames.json 1050/1050 pass)
- replication/runs/seed41_dt05 (numerical variant: the world's own dt halved, WORLD_P dt=0.05, seed 41 to t=5500; identical nucleations and gen-1 split times; 445/445 layer samples pass)
- replication/fork/forkpy_s43 (the claim's fork.py unchanged, seed 43, t_fork=4000, 300 t after: fed 10->10, kF=0 10->0, kF=0+d=0 10->0)
- replication/fork/s41_t9000 (fork_state.py from the seed-41 t=9000 state: fed, kF=0, kF=0+d=0, fed+d=0, local kF=0 disk r=37 around track 8)
- replication/runs/seed41_white (rf_len=0 white noise, same std 0.03, t=1500: 0 bodies)
- replication/runs/seed41_rf8 (rf_len=8, same std, t=1500: 9 bodies)
- replication/lsa_out.txt (claim lsa.py: d=0.003 sigma -2.15e-3 at e0=0.12; uniform e>=0.15 unstable)

