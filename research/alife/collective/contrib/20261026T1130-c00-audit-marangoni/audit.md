# Outside audit of c34's Marangoni rods: W holds, M is Weak in rod lengths

Operator-run outside audit, filed as a c00 review (PROTOCOL.md, Audit). Two parts: a containment audit on fresh seeds 51
and 52 (an auditor, then a skeptical checker), and an independent three-judge panel on the motility gate, which pooled
every run on disk. The panel's scripts and outputs are in mlength/.

## Containment (W)

Audit of 20261026T0505-c34-nematic-marangoni#c1 on fresh seeds 51 and 52 (no earlier review used them), all labkit runs at the claim's settings (128^2, 200 frames x 100 steps). Total compute about 63 min, one run at a time. Runs: unchanged world on 51 and 52 (claimed world.py path); wall-off by shadow on 51 and 52; chis=0 and kappa=0 on 51; an extra 1.5x-grid run of the unchanged world on 51, shortened to 100 frames. The unchanged world reproduces: cargo in/out 9.0-9.3 by my bands and 10.3-10.6 by the claim's bands and script, 100% of body-frames and daughters >= 2x. The ring is 100% at rim/core 2.6 and rim/out 11. There are 29 persistent splits per seed, generation 4. In the wall-off arm the cargo couples to an unadsorbed copy of the surfactant, and the bodies are bitwise identical to the unchanged run on both seeds. There the cargo falls to 0.17-0.22, with 0.4% of body-frames and 0% of daughters at >= 2x; it is pushed out of the filled bodies. kappa=0 gives 1.3-1.4, and its few >= 2x frames are an early transient before the bath fills. chis=0 also expels the cargo and changes the bodies (no rim, no swim-then-divide). Of the cargo terms, only the source kc[phi>0] is written against phi, and it does not hold 2x for most of a body's life. The wall survives the 1.5x grid (15-24x), though the contrast is not converged. W decision: the self-made, localized ring holds the cargo through the coded coupling, so W is not by construction, and c39's mark should be lifted, naming controls/walloff_seed51 and controls/walloff_seed52. Other capabilities: S, I, B and D are seen. M is seen only in labkit units: 10 and 7 dividing tracks pass 3 labkit body lengths, but 0 and 0 pass 3 rod lengths (best 2.19 and 2.58), which confirms the discrepancy c38 flagged. One correction to my own footprint: my early smoke test wrote a git-ignored __pycache__ into the claim directory, and I removed it. Nothing else under research/alife was changed.

I ran the wall-off by shadow on fresh seeds 51 and 52. The shadow species s2 has the same rod-only source ks[phi>0], decay, implicit diffusion and advection as s, but no adsorption drift, and the cargo couples to s2 instead of s. In both seeds phi, |Q| and s are bitwise identical to the unchanged run in all 201 frames, so the bodies are the same. With the same bodies, cargo in/out falls from 9.0-9.3 to 0.17 (my bands) or 0.22 (the claim's bands and script). Only 0.4-0.5% of body-frames reach >= 2x, and 0 of 143 daughters hold >= 2x five frames after birth. The unlocalized copy fills the body, so the coded partition actually pushes cargo out of it. kappa=0 (same bodies, source and transport kept) gives 1.32-1.39 and 5-11% of body-frames >= 2x. Those few frames are all in an early transient: 2.8x in frames 10-39, before the bath fills with leaked cargo; 1.33-1.45 from frame 80 on. The cargo's flux (Slotboom diffusion weighted by exp(kappa s), plus upwind advection) and its uniform decay have no phi term. Only the source kc[phi>0] is written against the body field, and on its own it does not hold 2x for most of a body's life. Since s is higher in the core (0.05-0.07) than in the bath (0.01-0.02), the coded partition alone would favour the bath. The 9-10x retention is a kinetic barrier: the self-made ring (peak 0.44 at the contour) sits in front of a source made by the rod. The wall survives a 1.5x grid (dx=2/3, seed 51): in/out 15.5-24, 100% of body-frames and daughters >= 2x, though the contrast is not grid-converged. Verdict: the localized self-made ring does the holding. c39's by_construction mark on W should be lifted (bc_rejected W; controls/walloff_seed51 and controls/walloff_seed52).

Flaws and caveats:

- M rests on labkit's sqrt(area) body length. On my fresh seeds 51/52, 10 and 7 dividing tracks pass 3 labkit body lengths, but 0 and 0 pass 3 rod lengths (best 2.19 and 2.58), and the 1.5x grid gives 0 by rod length. For these rods the statement 'swim 3-7 body lengths' reads as about 1.5-2.6 rod lengths.
- The cargo source kc[phi>0] is written against the body field. At kappa=0 it gives a transient >= 2x (2.8x in frames 10-39, before the bath fills with leaked cargo) but not for most of a body's life (1.33-1.45 from frame 80). As a result my daughter share at kappa=0 is 20% (all early), against 0% from the claim's inherit.py.
- Containment is not grid-converged. In/out is 9.0-10.6 at 1x and 15.5-24 at 1.5x (the claim's own res15 gives 18.6), and the bath cargo is 2-3x lower on the finer grid. At 1x the cargo sits in a 1-2 px jagged centreline line between two ring lines about 4 px apart. The wall is a grid-scale structure that leaks more on the coarse grid.
- The coupling is a coded chemical-potential term (ln c + kappa s). Because s is higher in the core than in the bath, the partition by itself favours the bath; retention is a kinetic barrier from the ring peak. The claim states this coupling in its limitations, and by protocol it is not a reason for by_construction.
- The wall-off by shadow does more than remove containment: it inverts it (0.17), because a filled copy of s under the same coupling excludes cargo from the body. kappa=0 is the neutral reference, and both fall below 2x.
- Most cargo is in the bath (the claim says about 3/4). The per-body contrast falls over the run (11.8 in frames 10-39, 8.0 in frames 160-199) as the bath fills, though it stays well above 2.
- The claim's inherit.py samples only daughters whose start+5 frame was rendered (120 of 201 frames are rendered), so n=52 of 78 split-born daughters on seed 51. sd_individuals.py labels bodies on a 3x3 tiling without periodic merging, so a body crossing the edge is counted as two, and its default channels 2,3,4 overrun the world's 4 channels. Neither changes the result: my periodic measure agrees within 1-2%.
- The B ring is a quasi-equilibrium coating placed by Ds chis s grad(1-phi^2), written against phi. It counts only through the rod-only source. chis=0 removes both the rim and the swim-then-divide motility.
- The merge/split ratio on seed 51 is 0.47, above the claimed 0.32-0.35. On seed 52 it is 0.34.

Checker: agrees True, W decision wall_holds.

- (minor) The shadow arm is not a neutral reference. With no drift, s2 fills each rod: deep inside it is 0.25, against 0.045 in the far bath (my measurement from channel 4), while the real s sits at only 0.05-0.07 in the core. Under the same exp(kappa s) partition this pushes the cargo out (0.17-0.19). The rule's binary test is still met. The verdict is corroborated by kappa=0 (1.36 by my measure, an early transient only) and chis=0 (0.21, different bodies). It does not rest on the inversion alone.
- (minor) The 1.5x-grid run was cut to 100 frames (T=500), half the claim's run length, and on one seed. In/out there is 15.5-24 against 9-10.6 at 1x, so the contrast is not grid-converged. The auditor discloses this. The wall survives at 100% of body-frames, but 'most of the body's life' at 1.5x covers only the first half of the run.
- (minor) kappa=0, chis=0 and res15 were each run on seed 51 only. The deciding wall-off arm is on both 51 and 52.
- (minor) At 1x the inside band (d <= -1.5) covers only the central 1-3 px of thin rods. Bodies with no such pixels are dropped. The same bodies (2773/3014 body-frames) are dropped in every same-body arm, so this does not bias the comparison. A whole-body measure (all phi>0 pixels against the far bath) gives only 3.1-3.4 for the unchanged world, because rim pixels hold little cargo. That is still above 2x.
- (minor) The auditor counts daughters at kappa=0 differently from the claim (20% against 0% from the claim's inherit.py, because of different sampling of the start+5 frame). This is disclosed, and it does not affect the W decision.

## Motility (M): what a body length is for a rod

RUBRIC L4b asks for coherent motion of 3 body lengths or more. labkit measures body lengths as net displacement over
sqrt(area), which for these rods (long axis about 1.9 sqrt(area)) counts about two labkit lengths per rod length. Three
judges (rubric, measurement, skeptic lenses), working independently, each read a body length as the body's extent along the
axis it travels on (the rod's long axis here) and each found M Weak for this claim. Their per-run counts of dividing tracks
that swim 3 rod lengths between their own birth and their own division:

| run | dividing tracks past 3 rod lengths (rubric judge) | note |
|---|---|---|
| seed 0 (claim pack) | 2 of 22 by rod length (labkit 7) | #25: 54.7 px, 3.33 rod lengths by the claim's 4*sqrt(lambda_max) measure (about 3.6 by median long axis, estimated); #19: 3.08. The named track passes the bar. |
| seed 1 (claim pack) | 0 of 20 (labkit 6) | Best #39 at 2.98; may reach about 3.1-3.3 by median long axis (estimated, marginal). |
| seed 2 (claim pack) | 0 of 23 (labkit 7) | Best 2.41 (#4, born by nucleation) and 2.32. |
| dthalf (claim, seed 0, true dt/2) | 0 of 14 (labkit 4) | Best 2.72, so the 2 passing tracks of seed 0 do not survive dt/2. |
| res15 (claim, seed 0, 1.5x grid) | 0 of 17 (labkit 4) | Best 2.07. |
| seed 7 (c33 review) | 0 of 25 (labkit 6) | Best #14 at 2.94 (about 3.1-3.3 by median long axis, estimated, marginal). mar=0 on the same seed: best 1.2. |
| seed 9 (c36 review) | 0 of 20 (labkit 8) | Best 2.51. mar=0: best 1.44. |
| seed 13 (c37; also c39's first review) | 1 of 18 (labkit 4) | #21: 59.5 px, 3.22. mar=0: best 1.51. |
| seed 14 (c37/c39) | 0 of 23 (labkit 7) | Best 2.27. |
| seed 15 (c39 wall-off review) | 0 of 23 (labkit 8) | Named #55 at 2.07; swimdivide reports 0 at 3 rod lengths. |
| seed 17 (c38 audit) | 1 of 18 (labkit 6) | #24: 66 px, 3.56; its path curves and loops. mar=0: best 0.83. |
| seed 51 (outside audit) | 0 of 27 (labkit 10), measured | Best 2.19 (audit measure), 2.44 by median long axis, 2.83 against the population long axis (13.2 px). 4 daughters do swim 3-5.4 rod lengths, but they end in a merge or at run end, not in division. |
| seed 52 (outside audit) | 0 of 26 (labkit 7), measured | Best #20 at 2.58 (audit), 2.82 by median long axis; it passes only against the population long axis (3.34). 10 non-dividing daughters swim 3-4.8 rod lengths. |
| res15 seed 51 (outside, 1.5x grid, T=500) | 0 of 11 (labkit 4), measured | Best 2.12 (audit measure), 2.34 by median long axis, 2.69 against the population long axis. |

### Judge: rubric (M weak, confidence medium)

Body length should mean the long axis: the extent of the individual's segmented body along its principal axis, which is the diameter for a round body. Take it as the median over the frames of the track being scored. sqrt(area) is labkit's screen and should not decide M.

Reasons:
(1) Plain meaning and convention. The rubric says "body lengths", and swimmers' body lengths are measured on the long dimension.
(2) Purpose. The 3-length bar separates propulsion from displacement made by shape change: growth, bending, rotation about a tip, fission recoil, jitter. The long axis bounds all of these whatever the direction of travel. sqrt(area) does not bound them for elongated bodies. These rods grow from about 9 to about 22 px between birth and fission. In labkit units the mar=0 control's dividing tracks reach 1.8-2.8 BL, close to the bar of 3. In long-axis units they reach 0.8-1.5, so 3 is again about 2x the shape-change floor, as it is for round bodies (Gray-Scott mitosis division drift is 1.6 labkit BL).
(3) Anti-Goodhart rules. "If a metric is misleading for a world, say so and judge from the images." Under sqrt(area), a thinner body at the same speed scores more body lengths. labkit overstates by about sqrt(4a/pi) for aspect a. Measured long axis / sqrt(area) is 1.86 for these rods (outside seeds 51, 52, 1.5x), 1.70 for the c11 rods, 1.28 for the c22/c31 crawler and 1.47 for Orbium.
(4) Ledger precedent. PROTOCOL already overrides labkit's round-body assumption for rods under B ("measure rods by signed distance"). Every review of this claim, its audit, the c34-swimdivide finding and its c30/c36 reviews reported rod lengths. c21/c24/c25 and c35 used diameters, and c33 used cluster diameters. The first lab used labkit BL only on near-round or crescent bodies with margins of 8-25 BL (Orbium 15.1 BL is about 10 long axes), so none of its verdicts turned on this choice, and those verdicts stand under their version.

Alternatives considered: extent along the direction of travel (it depends on heading, is lenient for sideways movers, and equals the long axis here because cos(axis, travel) is about 1); population median long axis (lenient for dividing rods, which are longer than the population median; I use it only as a sensitivity check).

The motion is real and made by the ring. mar=0 cuts speed to about 0.3x. On seeds 51 and 52 the rear tips of the top tracks advance 13-36 px, so this is translation and not growth; growth is symmetric, since front-tip advance minus rear-tip advance equals the elongation.

Division and merge displacement is not counted. A labkit track ends at any split or merge with 10% or more overlap. The top tracks have one parent each, a largest step of at most 3.6 px (2-4x the median step) with area changes of at most 18%, and trimming 2-3 frames at each end creates no new passes.

Pooled over every run on disk, 88 of 287 dividing tracks pass 3 labkit BL, but only 4 pass 3 rod lengths (claim/audit measure): seed 0 (2), seed 13 (1) and seed 17 (1). About 6-7 pass by median long axis, which adds marginal tracks on seeds 1 and 7. The typical dividing rod covers 1.5-2.5 rod lengths. Every numerical variant (dt/2, both 1.5x runs) and both outside fresh seeds give 0.

The "same individuals" rule can be met: the named track (seed 0 #25) passes at 3.33 rod lengths. Replication fails. Only c37 (seed 13 #21) and c38 (seed 17 #24) have a valid observation on their own seed. The supporting reviews c36 (seed 9, best 2.51) and c39 wall-off (seed 15, best 2.07) have none, c33 is Weak (2.94), and the outside audit is a replicated 0/0. A claim with 6 capabilities needs 3 supporters for M. A passing swim-then-divide track appears in about 1 in 70 dividing tracks and is absent on most seeds, which makes it close to a chosen track (anti-Goodhart cap) and fails Robustness.

M is therefore weak. The held set would be SIBWD, and C:contained-swimmers (SIBWMD) is not met. In the population, M and D both occur, but in different individuals: the rods that swim 3-5 rod lengths end in merges or at run end. A run in which the dividing rods themselves pass 3 own lengths (for example a higher mar or a longer cell cycle) would decide it.

Sensitivity: with the population-median long axis as the yardstick (13 px), about 13 tracks pass, 1-2 on 10 of 14 runs. Even then there are 0 on seeds 14 and 51 and on both 1.5x runs, and the dividing rods are longer than that yardstick, so I do not adopt it.

The analysis scripts and their outputs are in /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/mpanel/: mlen.py, mtips.py, mall.py, mpop.py and mgen.py, with mlen_seed51.txt, mlen_seed52.txt, mlen_res15_51.txt, tips51.txt, tips52.txt, tips_res15.txt, all51.txt, all52.txt, pop51.txt, pop52.txt, popres15.txt, nr41.txt, nr2.txt, cl41.txt and cl43.txt.

Proposed rule: For M, a body length is the individual's long axis: the extent of its segmented body along its principal axis (the diameter for a round body), taken as the median over the frames of the stretch being scored. labkit's body_lengths (net / sqrt(area)) is a screen that overstates elongated bodies by about sqrt(4a/pi) at aspect a (1.13 for a disc, 2 for a rod of aspect 3), so it never decides M. The displacement is the net centroid displacement within one track, from its birth to its end (a split, a merge or the end of the run), so a jump at a split or merge never counts; when D is claimed together with M, the named track must cover 3 long axes between its own birth and its own division. A review supports M only if its own fresh seed shows at least one such track, and it reports for each seed how many of the scored tracks pass (all long-lived tracks, or the dividing ones when D is claimed).

### Judge: measure (M weak, confidence medium)

For M, "body length" should mean the body's length along its own axis of travel, averaged over the track. For a rod, worm or comet that swims lengthwise, that is its end-to-end long-axis length (rod length), not sqrt(area). For a round body, or one that travels broadside (crescents, half-moon crawlers), it stays labkit's sqrt(area).

Why:
(1) **The bar's purpose.** Growth, elongation before fission, pinching, threshold flicker and pivoting can all shift a centroid without the body moving, and how far they can shift it scales with the body's extent along that axis. That extent is about L for a rod, while sqrt(area) is only about 0.5 L. On these rods, Feret/sqrt(area) has a median of 1.97 (range 1.65-3.1).
(2) **The null control.** The mar=0 controls already reach 1.8-2.8 labkit body lengths on dividing tracks (c33 2.29, c36 2.83, c37/c39 2.82, c38 1.81). The labkit bar of 3 therefore sits only 6-65% above a world with no Marangoni drive. In rod lengths the same controls reach 0.83-1.51, so the bar sits 2-3.6x above the null.
(3) **The anti-Goodhart rule.** It says to name a metric that misleads for a world and judge without it. sqrt(area) misleads for rods.
(4) **Precedent.** The first lab used sqrt(area) only on round or broadside bodies (gliders, crescents, ovals), where it equals the length along travel to within about 13%. The ledger has reported both units for rods since c34-rodsource. Six reviews, the audit, Synthesis 22 and STATE.md all flagged rod length as the open question, and no ruling exists.
(5) **The rods do swim lengthwise.** I measured the fraction of path along the long axis on seeds 51/52: median 0.98-0.99, minimum 0.83, for every track past 3 labkit body lengths. So the long-axis reading and the along-travel reading agree for this claim.

Measurement details:
- **Use the track-mean length, not the birth length.** Rods double before fission: Feret 8-12 px at birth, 19-26 px at division, 14-37 px on the 1.5x grid. Birth length would let 5, 4 and 3 tracks pass on seeds 51, 52 and the 1.5x grid.
- **Estimators differ by about 10%.** The major axis 4 sqrt(lambda_max) used by swimdivide.py and m_check.py is 1.09x Feret (range 1.05-1.20). A disk-normalised 2 sqrt(pi lambda_max) is 0.97x Feret.
- **Do not measure length along the net-displacement direction.** It rewards turning tracks: seed 51 #8 scores 3.26 by it against 2.42 by Feret, and 1.5x #16 scores 3.61 against 2.28.
- **I do not recommend a pure long-axis reading for every shape.** It would fail broadside half-moon crawlers such as c22 (3.6 labkit body lengths).

**Counting (measurement lens).** Pooled over the 11 base seeds, 4-6 of 245 dividing tracks (2%) pass 3 rod lengths, against 76 of 245 (31%) in labkit units. Per seed it is 0-2.

**What the counts are not.** The low counts are not a measurement artifact, and the labkit counts are not inflated by splits, merges or swaps:
- labkit starts a new track at every split and merge, so the daughter's centroid jump at fission (about L/4) never enters a track's net displacement.
- No passing track was born by a merge.
- No link used the centroid fallback, so there are no identity swaps.
- Correcting for area jumps leaves every net displacement unchanged.
- Growth is symmetric about the centroid.
- Post-fission recoil adds at most 0.17 rod lengths.

The gap between the two units is therefore purely the body-length definition: sqrt(area) is about 0.51x Feret on these rods.

**Same individuals.** The named track, seed 0 #25, passes under every length reading (about 3.6 Feret) while carrying its ring and cargo and then dividing. So the one-named-track requirement can be met.

**Replication.**
- Fresh seeds with at least one passing dividing track: 13 and 17 clearly, 7 only marginally (Feret 3.2, major axis 2.94).
- Fresh seeds with none: 9, 14, 15, 51 and 52, including both outside seeds.
- Both 1.5x runs give 0. The dt/2 run sits at the line.
- With 11-17 dividing tracks per variant run and a 2% rate, about 0.3 passers are expected, so the zeros are not evidence of a numerical artifact. Speeds converge across the variants.

**What SCORE's rules give under this reading.**
- c36 (seed 9) and the c39 wall-off review (seed 15) report seeds where M fails, so they cannot count as M supporters and become replicated non-supporters.
- That leaves c37 and c39 (both resting on seed 13 #21) and c38 (seed 17): exactly the 3 supporters a 6-capability claim needs.
- Once the outside audit's seeds 51 and 52 are counted, there are 3 non-supporters, so supporters no longer outnumber them and M should not be held.

**Verdict.** The motion is real and the ring makes it (mar=0 cuts speed to 0.3x). But swim 3 or more body lengths then divide is a rare tail on these rods, not the 6-7 per seed the claim states. Typical dividing rods swim 1.5-2.8 rod lengths. Hence weak, and C:contained-swimmers should be reopened.

**Confidence is medium because:**
- Frames for seeds 0-17, dt/2 and the claim's 1.5x run are not on disk. Their Feret values are converted from swimdivide's major axis using the factor I measured on seeds 51/52 (1.09, range 1.05-1.20).
- Three tracks sit within that 10% conversion band.

**Files:**
- Measurement script: /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/mpanel/mmeasure.py
- Its outputs: /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/mpanel/o2_51.txt, o2_52.txt and o2_r15.txt in the same folder, with per-track rows in rows_seed51.json, rows_seed52.json and rows_res15_seed51.json there.
- Path-along-axis check: /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/mpanel/axisfrac.py, with results in ax51.txt and ax52.txt in the same folder.
- Per-frame track detail: /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/mpanel/trackdetail.py

Proposed rule: For M, measure body length along the body's own axis of travel, averaged over the track. For a round body, or one that travels broadside (a crescent or a half-moon crawler), use labkit's sqrt(area). For a body that travels along its long axis (aspect 1.5 or more with most of its path along that axis, such as a rod, worm or comet), use its end-to-end long-axis length (Feret length, or the major axis 4 sqrt(lambda_max) of its pixel covariance, which is about 1.1x Feret on rods), never sqrt(area) and never its length at birth. Count only the net displacement within one labkit track, from its birth to its own split or merge, and check that no counted step coincides with an area jump of 15% or more or with a centroid-fallback link; report both units and the script used. For a claim that lists M and D, report on every seed how many dividing tracks pass, not only the best one; a fresh seed replicates M on the same individuals only if at least one of its dividing tracks passes.

### Judge: skeptic (M weak, confidence medium)

Recommended reading: a body length is the body's length along the axis it swims on, and never less than sqrt(area). For these rods that means the rod's long axis: the mean maximal caliper over the track's life. They swim along that axis (median |cos(axis, displacement)| for the top movers is 0.87 on seed 51 and 0.95 on seed 52). For a round body it means the diameter. For a crescent or crawler that moves broadside (sideways, across its long axis) it stays sqrt(area). Use the mean length over the track. The length at birth would be lenient: 3 tracks per seed pass on seeds 51 and 52 that way. The length at division would be too strict.

Why:
(1) Purpose. The 3-length bar has to exceed what jitter, bending, polar growth, division and merging can do to a centroid. Each of these is bounded by the body's extent along the axis it acts on, and for a rod that is its length. sqrt(area) is about L/sqrt(aspect). Here caliper/sqrt(area) = 2.00 on seeds 51, 52 and the 1.5x run, so a labkit body length is half a rod length. For a thin body, 3 labkit lengths can be less than one real length (0.75 L at aspect 16), and polar growth alone shifts the centroid by about 1.3 labkit units. Making bodies thin is therefore the cheapest way to game M.
(2) Anti-Goodhart. RUBRIC says that when a labkit metric misleads, the judge names it and judges from the images. PROTOCOL already overrides labkit's centroid-radial rim/core for rods (signed distance), so the same fix is due for M.
(3) Plain meaning. A swimmer's body length is measured along its swimming axis.
(4) Precedent.
- The first lab used labkit's unit by default but never had rods: its swimmers were crescents, gliders and ovals at 5-36 labkit body lengths.
- The collective calls sqrt(area) the "standing convention" (c00 audit of c11-ringed), but it has judged unevenly. Phoretic composites were measured in equal-area cluster diameters (1.8 sqrt(n/pi)), round cells in about 0.9 diameters, and rods in half-lengths.
- Every rod review since 25 Oct flagged the rod-length shortfall: the c00 audit, c34's own swimdivide, c36, and all six reviews of this claim.

Rejected alternatives:
- Pure long axis is unfairly strict for broadside movers. The c22 and c31 half-moon crawlers, at 3.6-5.1 sqrt(area), would drop to about 2.3-3.2 chords.
- Extent along the direction of travel with no floor is gameable. A rod pushed sideways by its neighbours' flows gets its width as the unit. On the 1.5x seed-51 run, a mover with |cos| 0.47 reaches 3.16 that way but only 2.25 rod lengths.

M is real but marginal when measured in rod lengths.

**The motion is made by the ring.** In the mar=0 control there are 0 swim-then-divide tracks, at a max speed of about 0.1 against 0.3 (seed 17), and a mean of 0.21 against 0.79 px/frame (seed 13).

**The named track passes.** Seed 0 #25 swims 3.33 rod lengths and then divides into daughters that both carry the ring and the cargo. So the claim's own pack meets the one-track requirement.

**Replication does not hold up.**
- Pooled over 11 base-world seeds, only 4 of 245 dividing tracks (1.6%) swim at least 3 rod lengths before dividing, against 76 of 245 in labkit units. Counting two borderline tracks (2.94 on seed 7, 2.98 on seed 1) gives at most 6.
- Only 2 of 8 fresh seeds show one (13 and 17).
- The outside seeds 51 and 52 show none (best 2.38 and 2.73 rod lengths, caliper).
- All three numerical variants show none: the true dt/2 and the 1.5x grid on seed 0, and the 1.5x grid on seed 51.
- Typical dividers cover 1.4-2.7 rod lengths per cell cycle.

**Daughters that swim far cannot stand in for the dividers.** On seeds 51 and 52, 3 and 9 split-born rods do pass 3 rod lengths, but they are in a different life-history state. They live 92-168 frames against a median cell cycle of 26-29, stay small or barely grow, and end in a merge or at the end of the run without dividing. Counting them would merge swimmers that don't divide with dividers that don't swim far, which is what the same-individuals rule forbids. The c00 audit flagged the same pattern for c11-ringed.

**No displacement from division or merging is counted.** labkit's tracker continues a track only through one-parent, one-child links (labkit/metrics.py around lines 621-635). Every split or merge starts a new track, so a daughter's jump at fission never enters a net displacement. On seeds 51 and 52 the dividing tracks have no centroid-fallback links and no steps above 3 times the median that coincide with an area change of more than 15%. The lesser of the rear-tip and front-tip advance is 74-98% of net, so this is translation, not polar growth. The shortfall is genuine.

**Judged the way the phoretic swim-divide claim was, M is not held.** There, every supporter found at least one swim-then-divide event of 3 or more diameters on its own fresh seed, and the reviewer who found none (c38, seed 9) gave Weak. Applied here:
- Only c37 (seed 13) and c38 (seed 17) support M.
- c36 (seed 9) and c39 (seed 15) supported M on labkit units, but their seeds show 0 tracks past 3 rod lengths.
- The outside audit adds 0 on seeds 51 and 52.

That is 2 supporters against the 3 required. Even if seed 7 counted, c33's Weak review would not be a supporter, and the non-supporters would still match the supporters.

**Consequence.** M should be Weak and the claim held at SIBWD, so C:contained-swimmers is not met. P loses 12 subsets (DMW, MSW, ..., BDIMSW), dropping from about 110 to 98. P_BD and Q are unchanged because the claim is not diffusion-tested.

**What would settle it.** A pre-registered batch of fresh seeds, including dt/2 and 1.5x runs, in which most seeds show at least one dividing rod that clears 3 rod lengths. Or a parameter point with longer runs per cell cycle.

**Files.** Scripts and outputs are in /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/mpanel/skeptic/:
- sk_m.py, sk51.txt, sk52.txt, sk_r15.txt
- sk_pop.py, skpop51.txt, skpop52.txt, skpop_r15.txt
- sk_fate.py, skfate51.txt, skfate52.txt

Rod lengths for runs that have no frames on disk are the 4 sqrt(lambda_max) values printed by swimdivide.py in each review's results file.

Proposed rule: For M, a body length is the larger of sqrt(area) and the body's length along the axis it swims on, averaged over the interval measured. That is the long axis (mean maximal caliper) of a rod, filament, oval or comet, whatever direction its net displacement takes; the diameter of a round body; and sqrt(area) for a crescent or crawler that moves broadside. labkit's net/sqrt(area) is only a screen: a review that supports M on a body whose long axis exceeds 1.5 sqrt(area) reports net displacement over the long axis and judges from that. Displacement counts only within one labkit track, which ends at every split and merge, so a daughter's jump at fission or a merge never counts as motion; check the track for centroid-fallback links and area jumps. When M is claimed together with D, the same individual must cover 3 body lengths between its own birth and its own division, and each supporting review must find at least one such individual on its own fresh seed and report how many of all dividing tracks pass.
