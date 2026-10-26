# Outside audit: crawler-layer-repair (C:motile-repair)

Run by the operator outside the collective: a construction auditor read world.py and ran a beta=0 arm, an algebraic-contour wall arm, kappa=0 and source-split arms on one shared trajectory; a replication auditor re-ran the unchanged world on unused seeds 41 and 43, uncut and cut, plus a dt/2 cut run and a kappa=0/beta=0 ablation; a judge checked their disagreements.

**Judge: met_with_caveats.** C:motile-repair (IBRM) is met with caveats: I, M and R are c22's wave-pinning crawler unchanged, and B counts only under the L3 quasi-equilibrium clause, as a passive adsorbate bolted onto that crawler. W does not hold; I rate it Weak.

## Per capability

- **I**: supported. One planted body, 101/101 frames in every pack (u41, u43, c41, c43, pack_cut/seed0); one body before and after the cut; area ratio 1.20 uncut. It persists as a planted template (Orbium/Particle-Lenia level).
- **B**: supported. Counts under the RUBRIC L3 quasi-equilibrium clause and the collective's ruling: 97% of s production is at phi>0.5 and 99.97% in the body; pack_nosrc removes the layer; the ring is complete in u41_snap.png and through the cut (c41_vs_twin.png). The construction objections (beta=0 kills the ring, s is 97% f(phi), no feedback, an algebraic contour does the same) are real but belong to the mechanism and beyond-diffusion modifiers, not the gate.
- **W**: weak. With the wall, in/out stays >=2 all run and the ablation removes the rear-side contrast (3.8 vs 1.1). But in the claim's window kappa=0 still meets the 2x all-round threshold in most frames, the 1.5x leg is the claimant's single-seed t=0-8 run, and an algebraic contour gives identical containment (6.75 vs 6.83), so the wall is an imposed exclusion potential on a contour-equivalent layer.
- **R (front re-nucleation)**: supported. Mature cell, branched twins, >=2 seeds, erased matter removed from the cell. Non-polar disk at t~9-10.6, new front at t~10.6-11, crawls on at 0.35 vs the twin's 0.42 (c41/c43, cut_s5, c32, c33, c34). 7 of 9 seeds repaired; seeds 4 and 6 died; labkit seed 2 used competition between the two remnant lobes.
- **R (layer re-coat, shape rounding)**: by_construction. The adsorption drift coats any phi interface: an intact twin with s erased in the sector re-coats to the twin's level in about 2 time units (cut_s5_table.txt ARM columns). Rounding is Allen-Cahn curvature flow. The reviews left by_construction empty.
- **M**: supported. 5.1 body lengths at 0.42 with no imposed field (u41, u43); the linear-kinetics twin does not move. This is c22's wave-pinning motility, and speed is +8% at dt/2 (dth41c).
- **IBRM together**: supported. The single labkit track 0 in c41, c43 and pack_cut/seed0 crawls with its ring, is cut, re-nucleates and crawls on with its ring, in 101/101 frames. The combination is additive: no capability acts on another.
- **S**: not_shown. Not claimed; a planted disk with a planted 75% polarity front.

## Caveats

- I, M and R are c22's established wave-pinning results reproduced bit for bit; s and c never feed back on phi or rho (world.py step l.290-321). The only new capability is B, a passive adsorbate.
- B counts only under the L3 quasi-equilibrium clause. The ring is made entirely by the drift written against grad 4phi(1-phi) (beta=0 gives rim/core 0.50-0.51), and s is 97% a function of phi. Mechanism and beyond-diffusion credit for B should be 0.
- R (front re-nucleation) repaired on 7 of 9 distinct seeds. Seeds 4 and 6 died, and labkit seed 2 took the competition path rather than the non-polar disk the claim describes. Size is not restored (52% of the twin's area).
- Layer re-coating and shape rounding after the cut are by construction. They should go in by_construction, which all three reviews left empty.
- The cut zeroes s and c in the sector out to r<L/2, medium included (world.py l.192, l.212-213), which inflates the cargo in/out reported after the cut (6.15 to 10.48 at the instant of the cut on seed 5).
- W is Weak: in the claim's own window the kappa=0 arm still gives an all-round in/out of about 2 (75-100% of frames on 4 of 5 checks); only the rear-side ratio and the held share separate the arms.
- W's 1.5x resolution leg is the claimant's only, one seed over t=0-8 (runs/r3res384.log). It is a series, not the single frame both auditors described, but it is unreplicated.
- An algebraic contour wall gives the same containment, so W belongs to the imposed exclusion potential, not to the self-made layer. The wall also leaks once production stops (6.0 to 2.56 in 4 time units).
- Planted single cell with a planted polarity front: no S, no D.

## Judge's reasoning

I checked the points of disagreement and every major flaw against world.py, the claim's files and the auditors' outputs. I re-ran nothing.

Code facts both auditors rely on, all confirmed:
- s and c never reach the phi or rho update (step() lines 290-321), and layer_step and cargo_step draw no random numbers. The body dynamics are therefore c22's world bit for bit. The construction auditor's labkit run on seed 4 matches c22's packs/front40_seed4 exactly: longest track 60 frames, area ratio 37.66, max speed 14.1.
- The cut mask extends to hypot < L/2 (line 192), and s and c are zeroed inside it (lines 212-213). The cut therefore also deletes cargo in the medium (12.5% on seed 5), which inflates the cargo in/out reported after the cut.
- world_src_body.py differs from world.py only in its SRC and kp defaults. The claim's kappa=0 arms are therefore valid for the SRC=rho world.

I (L2): Supported, for a planted cell. One body appears in 101/101 frames in every pack. The cut cell settles at 52% of its twin's area, a size set by its conserved protein. There is no population and no formation from noise.

B (the auditors disagree): Supported, under the RUBRIC L3 quasi-equilibrium clause and the collective's ruling.
- The species is self-made: 97% of kp*phi*rho production is at phi>0.5 and 99.97% inside the body. It is transported on its own and decays.
- The source ablation removes the layer (pack_nosrc).
- The ring is complete in images (u41_snap.png, arms_s5_t8.png) and persists through the cut (c41_vs_twin.png, t=8.2).
- Each of the construction auditor's grounds for Weak is real, but each is one the rubric assigns to the mechanism and beyond-diffusion modifiers rather than to the gate:
  - The ring needs the drift written against grad 4phi(1-phi): with beta=0, rim/core is 0.51.
  - 97% of the spatial variance of s is a function of phi.
  - s has no feedback on the body.
  - An algebraic contour does the same work.
- So B counts, but it is a passive layer whose location is imposed, and it should score 0 on mechanism and beyond-diffusion.

M (L4b): Supported. The cell travels 5.1 body lengths at 0.42 with no imposed field. This is c22's wave-pinning motility; the linear-kinetics twin does not move. Speed rises 8% at dt/2.

R (L4a): Supported for front re-nucleation, the only repair the collective's ruling credits.
- Mature cell, branched twins, at least 2 seeds; the erased matter leaves the cell (C is reduced).
- On seeds 41 and 43 the cut cell is non-polar at t≈9-10.6, grows a new front at t≈10.6-10.8, and crawls on at 0.35 against its twin's 0.42.
- Across the claim, the reviews and the audits it repaired on 7 of 9 distinct seeds. It died on seed 6 (c32) and seed 4 (construction labkit run, the same as c22).
- labkit seed 2 takes c22's two-lobe competition path rather than a non-polar disk (c22 classify.txt: 0 non-polar frames; pack_cut/seed2/sheet.png, t=8.6). The claim's description of seed 2 is partly wrong.
- Layer re-coating of the cut edge and shape rounding are by construction. On an intact twin, erasing s in the cut sector re-coats it to the twin's level within about 2 time units. No review listed these under by_construction.

IBRM together: shown on one track. labkit track 0 is the only track, present in 101/101 frames in pack_cut/seed0, c41 and c43.

W: Weak, because the gate is met only in the letter.
- In favour:
  - With the wall, in/out is at least 2 for the whole run (100% of frames to t=20 on seed 41).
  - Ablating the wall removes the rear-side contrast on every seed: 3.5-3.8 falls to 1.0-1.3.
  - In arms_s5_t8.png, with kappa=0 the cargo cloud spills across the rear boundary, peaking outside the body.
  - Over a full life the kappa=0 in/out drops below 2 after t≈6.5 (seed 5 continuation: 1.65 at t=16). On claim seed 2 it is at least 2 in only 48% of frames.
  - The lowered-D Laplacian twin fails: rear 0.99.
- Against:
  - In the window the claim and the three reviews used to support W, the matched ablation still meets the 2x all-round threshold in 75-100% of frames on 4 of 5 seed checks. That comes from production inside the body and the front moving into clean medium. No review noticed it.
  - The 1.5x resolution leg is the claimant's alone. Both auditors call it a single frame; in fact runs/r3res384.log is a t=0-8 series that tracks the base run within 3% (6.62 vs 6.46 at t=8). But it covers one seed and half the body's life, and no one has replicated it.
  - The wall leaks. With production off from t=4, in/out falls from 6.0 to 2.56 in 4 time units. That is still slower than the claim's kappa=0 production-off run (koff1_k0.log: 2.01 to 0.82 in 2 units), so the wall does slow the loss, but the containment is a balance of production and leak.
  - An algebraic contour 0.42*4phi(1-phi) with kappa=10 holds the cargo equally well: 6.75 vs 6.83 at t=1-8, and 3.71 vs 4.48 at t=16, so equivalent rather than identical. The containment is a property of the exclusion potential written onto the contour, not of the self-made layer.

Overall: I, B, R and M are all on the same individual, so the challenge is met by the rules, with caveats.
- The new contribution over c22's established IRM is a passive, by-construction-located adsorbate.
- Repair is not universal: about 2 of 9 cut cells die.
- The by-construction parts of R are not separated in the claim or the reviews.
- W stays Weak until a full-life matched gate is run at two resolutions.

## Settling experiment for W

A full-life, matched W gate at two resolutions, run with one passive-arm driver per trajectory. Because s and c never feed back, all arms can share one phi/rho trajectory, as the construction auditor's arms.py does.

Setup:
- Two fresh seeds (e.g. 51 and 53), N=256 and N=384, t=0-20.
- On each trajectory, carry these arms:
  - kappa=10 (as claimed);
  - kappa=0;
  - the algebraic contour s := 0.42*4phi(1-phi) with kappa=10;
  - production-off forks at t=8 (kc_off_t=8) for both kappa=10 and kappa=0;
  - a 40% front cut at t=8 whose erase mask is limited to the body (phi>0.01 in the sector, no medium erasure), with its uncut twin.
- Record per frame:
  - all-round in/out by signed distance;
  - rear-side in/out;
  - held fraction;
  - after production stops, the half-life of the excess (in/out - 1).

Pre-declared rule:
- W holds if, at both resolutions and on both seeds:
  - (a) kappa=10 gives in/out >=2 in more than half of the t=1-20 frames;
  - (b) kappa=0 is below 2 in more than half of the same frames and its rear ratio stays below 1.5;
  - (c) the retention half-time with the wall is at least 3x that of kappa=0;
  - (d) the cut cell under body-only erasure keeps in/out >=2 after t=9.
- If the contour arm matches kappa=10 within 15%, record W as a property of the imposed exclusion potential: mechanism 0 for the layer, and no credit for a self-made wall.

Cost: about 4 trajectories of 10-25 minutes each, roughly 1-1.5 hours, which fits one agent loop.

## Auditor: construction (holds_with_caveats)

Construction audit of c31's crawler-layer-repair claim (IBRM+W). The body dynamics (phi, rho, per-body pool) are c22's wave-pinning crawler unchanged. s and c never feed back, and my labkit cut run on fresh seed 4 matches c22's front40_seed4 exactly (dies at t~12, area ratio 37.66). So I, M and R are c22's established, emergent results: on fresh seed 5 the cut cell floods into a non-polar disk, re-nucleates at t~11 and crawls on. That includes c22's failures, which the claim leaves out: death on seed 4 and the two-lobe competition path on labkit seed 2. The layer s is self-made (97.1% of production at phi>0.5, 99.97% inside the body), but the drift written against grad 4phi(1-phi) creates the whole ring: with the same source and beta=0, rim/core is 0.51 against 3.64. s is 97% a function of phi, the ring stays uniform despite a ~10x front/rear source asymmetry, and erasing s on an intact cell recoats it within ~2 time units, so layer repair is automatic. Read literally, the L3 quasi-equilibrium clause would count B; I rate it Weak. W does work: in/out 6.8 to 4.5 against 2.2 to 1.65 with kappa=0, rear 3.8 against 1.1, and a lowered-D Laplacian-only twin fails. But production geometry alone gives about 2x for the first ~6 time units. An algebraic contour wall gives the same containment (6.75, rear 3.59, held 0.71), and the cut's erasure of medium cargo inflates the post-cut in/out (6.15 to 10.48 at the instant of the cut). Overall the challenge is met only in the letter: a motile, repairing crawler (c22) carrying a by-construction adsorbate layer and its contour-equivalent cargo wall. I left the claim directory unmodified. Compute was about 37 minutes, one job at a time.

Flaws:

- **major**: The layer is the equilibrium of an operator written against the body field. The cell supplies only the material, and the layer is a passive tracer. Evidence: beta=0 arm, same kp*phi*rho source: signed-distance rim/core 0.51 vs 3.64 and cover 0.00 vs 0.72 (runs/arms_s5_table.txt). s is 97% explained by a function of phi (runs/extra_s5.txt). The ring is uniform to +-10% despite a ~10x front/rear source asymmetry. Neither s nor c is read by the phi/rho update (world.py step l.290-321).
- **major**: The 'self-made wall' does no containment work that an algebraic contour of the body field does not do equally well, so W is a property of an exclusion potential placed on the contour. Evidence: Contour arm, s := 0.42*4phi(1-phi) with kappa=10: in/out 6.75 vs 6.83, rear 3.59 vs 3.80, held 0.71 vs 0.71 at t=1-8; 3.71 vs 4.48 at t=16 (runs/arms_s5_table.txt, runs/arms_s5_cont.log, figs/arms_s5_t8.png).
- **major**: R, M and I are c22's established result reproduced exactly. The added species do not touch the body, and c22's failure modes (death on seed 4, competition path on seed 2) are omitted from the claim. Evidence: My labkit cut run on seed 4 dies at t~12, with area ratio 37.66, 60 frames, max speed 14.1 and 2.2 body lengths, the same as c22 packs/front40_seed4 (rerun_cut/FACTS.md). The c31 pack_cut seed0 and seed2 FACTS equal c22's front40_seed0 and seed2 (2.53/4.1 and 2.28/3.9). The claim names seeds 0, 2 and 3 as re-nucleating, but labkit seed 2 shows the dumbbell competition path (pack_cut/seed2/sheet.png t=8.6).
- **major**: The cut erases s and cargo in the whole box sector out to r=L/2, medium included, which inflates the post-cut cargo in/out the claim reports as 'cargo held'. Evidence: world.py l.192 (mask: hypot<L/2) and l.212-213. On seed 5 the cut erases 12.5% of the medium cargo, and in/out jumps from the twin's 6.15 to 10.48 at the instant of the cut, while the new edge is still uncoated (cover 0.52) (runs/cut_s5.log). The claim's cuttable cut-arm values of 9.0 and 10.0 against the twin's 6.3 and 5.2 are partly this artifact.
- **minor**: Production geometry alone (cargo made only inside, kc*phi, and a front moving onto clean ground) gives in/out of about 2 for the first ~6 time units, so the W ablation contrast hugs the 2x line instead of collapsing; only the rear-side measure separates cleanly. Evidence: kappa=0: 2.19 median and 79% of frames >=2 over t=1-8, falling below 2 after t~6.5 and reaching 1.65 at t=16, rear ~1.0 (runs/arms_s5_table.txt, runs/arms_s5_cont.log). The claim's wtable.txt gives 80%, 100% and 48% of frames >=2 for kappa=0.
- **minor**: labkit's radial membrane screen does not discriminate in this world: the polarity crescent and the cargo pile are also flagged MEMBRANE-LIKE, so only the signed-distance numbers support B. Evidence: pack/seed0/FACTS.md: rho rim/core 2.21, s 2.06, c 2.88, all MEMBRANE-LIKE. My beta=0 arm scores 0.83 labkit-style, which shows the radial s score itself comes from the drift.
- **minor**: Layer repair after damage is automatic by construction: the drift coats any interface whatever the cell does. It should be scored under mechanism, not counted as the organized individual repairing itself. Evidence: On the intact twin body, erasing s and c in the cut sector recovers sector coverage 0 -> 0.47 (t=8.5) -> 0.64 (t=9.5) -> 0.70 (t=10.5), the twin's level, with no cut (runs/cut_s5_table.txt, figs/cut_s5.png bottom row).
- **minor**: Re-nucleation is kicked by additive noise on rho that is then clipped at 0 (world.py l.312-313, l.320). The rectification also sets the rear low-state level that feeds the layer source. Evidence: Rear rho is 0.084 inside the body at t=8 on seed 5, where the deterministic low state is 0 (pickle check of runs/arms_s5_state.pkl). This is inherited from c22's eta=2.

## Auditor: replication (holds_with_caveats)

I re-ran the claim's world.py unchanged through labkit on new seeds 41 and 43, both uncut and with the claim's in-world 40% front cut at t=8. Each uncut run is the cut run's twin, identical to t=8.0. I also ran a matched kappa=0/beta=0 ablation on seed 41 and a dt/2 cut run on seed 41 that also stopped cargo production at t=4. Total compute was about 65 minutes.

Replication holds for I, B, R and M on the same individual: labkit track 0 is present in 101/101 frames. The s ring scores rim/core 1.95-2.06 in labkit and 3.5-3.7 by signed distance, with rim/out 19-20 (labkit) and 38-46 (signed distance), and it is complete around the body. The cell crawls 5.1 body lengths at 0.42. After the cut it is non-polar at t=9.0-10.6, has a new front at t=10.6-10.8, and crawls at 0.35-0.36 against its twin's 0.42, keeping the layer (rim/core about 4) and the cargo (in/out 7-9). At dt/2 the layer (-3%) and the re-nucleation timing are unchanged, but crawl speed is 8% higher.

B: 97-100% of s is made by the cell, so B counts under the RUBRIC L3 quasi-equilibrium clause. The matched beta=0 twin shows the ring is made entirely by the adsorption drift written against grad 4phi(1-phi) (rim/core 0.50). s and c never feed back on the cell, so the layer and the cargo are passive passengers on c22's established IRM crawler.

W is weak. The matched kappa=0 arm still gives in/out 2.19, at or above 2 in 75% of frames, so production geometry alone supplies the 2x; only the rear-side contrast (1.14 vs 3.82) and the held share separate the arms. With production stopped, the wall leaks: in/out falls from 6.0 to 2.6 and held from 0.66 to 0.33 within 4 time units.

R: the emergent part is c22's front re-nucleation, which repaired on 2/2 of my seeds (7 of 8 seeds across claim and reviews). The layer re-coating and shape rounding are by construction, and size is not restored (52% of the twin's area).

I agree with c32, c33 and c34 on every replicated number. I disagree on W, where none noted that kappa=0 still meets the 2x threshold, and on by_construction, which all three left empty.

Flaws:

- **major**: W gate not met as written. The SCORE gate requires that ablating the wall operator removes the contrast, but production geometry alone already gives about 2x across the boundary. All three reviews (c32, c33, c34) read kappa=0 in/out of 1.8-2.2 as 'loses the contrast' without noting that it still meets the 2x threshold. Evidence: runs/abl41 vs runs/u41 (seed 41, identical cell trajectory): kappa=0 in/out median 2.19, >=2 in 75% of frames t=1-8; kappa=10 gives 6.85. Claim wtable.txt: the kappa=0 arm is >=2 in 0.80/1.00/0.48 of frames. Only the rear ratio (1.14 vs 3.82) and the held share (0.42 vs 0.70) separate the arms. A matched kappa=0 production-off arm on the claimed SRC=rho world is missing; koff1*.log used world_src_body.py.
- **major**: The wall leaks. Once cargo production stops, the containment decays within a few time units. The 'held' state is a production/leak balance rather than retention. Evidence: runs/dth41c (kc_off_t=4, dt/2): in/out 6.04 (t=4.4) -> 3.60 (6.4) -> 2.56 (8.0); held 0.66 -> 0.46 -> 0.33. Total cargo follows decay alone (0.93 -> 0.78), so the cargo is leaving the body. figs/dth41c_vs_c41.png shows the rear pile emptying.
- **major**: The layer's location is imposed. The s ring exists only because of the adsorption drift written against grad 4phi(1-phi); the cell contributes only the source. It counts under the L3 quasi-equilibrium clause because the cell makes about 100% of s. s and c do not feed back on the cell, so B and W are passive passengers bolted onto c22's established IRM crawler. The IBRM combination for C:motile-repair required no interaction between the capabilities. Evidence: beta=0 matched twin (runs/abl41): s rim/core 0.50 by signed distance and 0.83 labkit, not membrane-like, against 3.58 with beta=4 (stats/abl41.json, figs/abl41_vs_u41.png). world.py layer_step: flux v=Ds*beta*grad(w), w=4phi(1-phi). Production in phi>0.5: 97.0%. The phi update has no s or c term.
- **minor**: The repair content new to this claim is by construction. Layer re-coating of the cut edge and shape rounding are automatic. The emergent repair is c22's front re-nucleation, size is not restored, and the reviews listed nothing in by_construction. Evidence: figs/c41_vs_twin.png t=8.2: complete ring around the kidney-shaped remnant one frame after the cut. Area 1.36 vs twin 2.62 at t=14-20 (stats/c41.json).
- **minor**: Crawl speed is not converged in dt. The claim's dt/2 check covered one t=8 frame of layer and cargo only. Evidence: runs/dth41c vs runs/u41/c41: t=2-8 speed 0.453 vs 0.419 (+8%). After re-nucleation (t=11.0-11.2) 0.44-0.53 vs 0.39-0.46. Layer rim/core 3.52 vs 3.58 and re-nucleation at t=10.8 in both, so B and R timing are converged.
- **minor**: The labkit radial screen marks the polarity crescent and the rear cargo pile as membrane-like. It is not discriminating for front/rear-asymmetric fields; B must rest on signed distance plus images. Evidence: u41/u43 FACTS.md: rho (polarity) rim/core 2.14/2.42 MEMBRANE-LIKE; c rim/core 2.80/2.87 MEMBRANE-LIKE, although c sits inside the rear rim (figs/u41_snap.png).
- **minor**: The cargo contrast falls over the run in the uncut twin. The front cut also misses most of the cargo, so 'keeping the cargo through the cut' is partly geometric. Evidence: u41 in/out 6.85 (t=1-8) -> 2.86 (t=14-20), u43 6.88 -> 3.92 (periodic L=5 box re-crossing). Cut erases only 9% of the in-body cargo (scripts/cutfrac.py) because it piles at the rear.
- **minor**: The per-body protein pool is a non-local rule. rho_cyt is an instantaneous integral over each connected component of phi>0.01, labelled every step (plabel/update_cyt). For one body it equals Camley's global well-mixed cytosol and imposes no motion or repair, but M (wave-pinning) and R (post-cut pool level) both depend on it. Evidence: world.py update_cyt: Nk from ndimage.sum over olab labels; ck=(Nk-Bk)/Ak. Single body in all runs (ncomp 1, labkit components max 1).
- **minor**: Repair is not universal across seeds. Evidence: c32 seed 6: the cut cell died (area 1.6 -> 0). c22 labkit: 3 of 5 seeds re-nucleated. My seeds 41 and 43 (base dt) and 41 at dt/2 all repaired.

