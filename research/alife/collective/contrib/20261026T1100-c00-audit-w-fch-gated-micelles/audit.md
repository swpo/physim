# Outside audit of W in c03's gated FCH micelles: the cargo is held without the wall

Operator-run outside audit of containment (W), filed as a c00 review under PROTOCOL.md (Review: the wall-off rule; Audit).
An independent auditor ran the claimed world and its arms with labkit on fresh seeds; a second agent then checked the variants,
the measurement and the conclusion, trying to refute it. Both reached the same decision.

## Auditor

W for fch-gated-micelles#c1 holds by construction: with the wall taken away, the cargo is still held at 2x or more.

**Runs.** Seven labkit runs at the claim's settings (100 frames x 200 steps, 128x128, dt 0.02), about 27 CPU-minutes, one at a time. Seeds 51 and 52 were used by no claim or review. Unchanged re-runs used the claim's own world.py path. Every arm's bodies are bit-identical to the unchanged run (max|du| = 0, same lineage), because u does not depend on c or q.

**Unchanged world.** It reproduces the claim on both seeds:
- S, I and B hold: white noise at t=0, a q ring with rim/core 10.7-11.5 on 238/241 and 258/259 individuals.
- D holds: 18 and 19 persistent splits, generation 3 and 4, 0 merges.
- Cargo in/out is 23.8x and 24.9x median, with 99.8-100% of body-frames at 2x or more.
- All 36/36 and 38/38 daughters are at 2x or more five frames after the split, at a median of about 8x rather than the claimed ~10x. The necks leak cargo and daughters are born cargo-poor.

**Wall-off arm (chi_q = 0).** q keeps its source, decay and transport, and the gate (beta = 8) is kept. The ring disappears and q fills the medium, yet the cargo stays at 3.41x and 3.51x median, with 99.8% and 99.5% of body-frames at 2x or more and 36/36 and 37/38 daughters at 2x or more. The claim's own definition gives 3.4x and 98-99%. This holds under near and far measuring bands: 2.5x with 75-78% of body-frames at 2x or more, and 4.7x with 100%.

**Other arms (seed 51).**
- Gating by the domain-mean q (a uniform, lowered D): 2.59x, 76% of body-frames at 2x or more (96% by the claim's definition; 49-98% depending on band).
- Gating by q blurred over 4 px, so no ring: 4.57x, 100%.
- beta = 0: 1.12x, 2%.

**Why.** The cargo source kp(u - u_m)_+ (world.py line 123) is restricted to the bodies by the code. q is also made only in bodies, builds up, and slows the cargo everywhere. So any slow transport around a body-restricted source holds the cargo at 2x or more. The gate coupling is necessary, but the self-made ring only raises the contrast from about 3.5x to about 24x; it is not what meets the 2x criterion.

**The claim and the reviews.** The claim's own pack_chiq0 (2.4-6.7x) and the chi_q = 0 runs in c01 (7.1x) and c06 (2.6-6.3x) already showed this. All 8 reviews still supported W without marking it by construction.

Everything is in /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/fch-gated-micelles/, with the full table in w_table.txt. Nothing under the repository was modified.

### W decision

The wall-off arm still holds the cargo, so the self-made wall is not what holds it at 2x. In the arm, chi_q = 0 removes q's adsorption drift. q keeps its source, decay and Dq, so its total is the same as in the unchanged world. beta and the gate are kept, and the bodies are bit-identical (max|du| = 0 in every frame; same 27/26 splits and 18/19 persistent splits). The ring is gone (q rim/core 0.93) and q fills the medium. Even so, the cargo is held at a median in/out of 3.41x (seed 51) and 3.51x (seed 52), with 99.8% and 99.5% of body-frames at 2x or more. Every tracked body is at 2x or more for most of its life (75/75 and 72/72), and 36/36 and 37/38 daughters are at 2x or more five frames after the split. The claim's own cargo definition, applied to all frames, gives 3.37x / 97.7% and 3.39x / 99.1%. This survives a change of measuring band: a near band gives 2.5x with 75-78% of body-frames at 2x or more, a far band 4.6-4.8x with 100%. Two further arms show where the holding comes from. With the gate driven by the domain mean of q (a spatially uniform, lowered cargo D, bodies identical), the cargo is still at 2.59x with 76% of body-frames at 2x or more (84% after t = 120; 96% under the claim's definition). With the gate driven by q blurred over 4 px (no ring), it is 4.57x with 100%. The cargo source kp(u - u_m)_+ (world.py line 123, used on line 127) is restricted to the bodies by the code. q is also made only in bodies and builds up over the run (kdq = 0.002). Its domain mean slows the cargo everywhere, roughly exp(-8 x 0.37), about 0.05 of Dc. A body-restricted source plus slow transport holds the cargo at 2x or more without any ring. The ring raises the contrast about 7x (23.8-24.9x against 3.4-3.5x), which is real, but it is not needed to meet the 2x criterion. Removing the gate entirely (beta = 0) gives 1.12x, so the coupling is necessary, but the localized wall is not.

### Cargo terms written against the body field

Yes for the source. The cargo source is prod = kp * max(u - u_m, 0) (world.py line 123, used on line 127): cargo is made only where the amphiphile body field u > -0.6, i.e. inside micelles. The cargo flux, gate_div(c, q, Dc, beta, dx) (lines 81-89, called on line 127), depends only on q: chi = 0, so the u-coupled c_div is not used. The cargo decay, kd * c, is uniform. On its own, at Dc = 1, the body-restricted source does not hold the cargo (beta = 0: 1.12x, 2% of body-frames at 2x or more). But it is what turns any slowing of the cargo into containment: a uniform lowered D gives 2.6x, the wall-off arm 3.4-3.5x. q is also written against u. Its source, (kq/kp) * prod (line 128), is restricted to the bodies, and its adsorption potential Vq = -chi_q exp(-((u - u_w)/sig_w)^2) (line 125) places the ring. With chi_q = 0, q is still enriched in the bodies (q in/out 0.46/0.37), so the gate still follows the body through q's u-restricted source.

### Flaws and caveats

- The claim's own chi_q = 0 arm (pack_chiq0, contrast.txt: 2.4-6.7x, 83-100% of bodies at 2x or more) is the wall-off control, and it already shows the cargo held at 2x or more without the wall. The claim calls this 'cuts it' and files it under B. By the protocol's wall-off rule this makes W by construction. My wall-off runs on fresh seeds 51 and 52 reproduce it: 3.41x and 3.51x, with 99.8% and 99.5% of body-frames at 2x or more.
- The claim's controls_run for W points at beta = 0 and at res15. The protocol says removing a mobility gate (beta = 0) speeds the cargo everywhere and does not decide W alone.
- All 8 collective reviews (c01, c06, c07, c05, c09, c10, c11, and the c13 audit) support W, and none lists it in by_construction. c01 (shell_controls.txt: chi_q = 0 on seed 3, 7.1x at t=400, weakest body 2.5x) and c06 (chi_q = 0 on seed 9, 2.6-6.3x) ran the wall-off arm themselves, saw at least 2x, and still supported W. c07, c09, c10, c11 and c13 found W not beyond diffusion (uniformly lowered D holds the cargo) but did not mark it by construction.
- The cargo source is restricted to the bodies by the code (world.py line 123), and the shell q is too (line 128). q decays slowly (kdq = 0.002), builds up in the medium, and lowers the cargo's diffusivity everywhere, to about exp(-8 x 0.37) or roughly 0.05 of Dc. A gate with no spatial structure (the domain mean of q) still holds the cargo at 2.6x with 76% of body-frames at 2x or more; a ring-free blurred gate holds it at 4.6x with 100%.
- Fission leaks cargo at the neck: daughters measured five frames after the split are at a median of 7.9-8.5x (minimum 2.1x), below the claim's '~10x or more'. In the wall-off arm, daughters at +5 frames sit at about 2.4-2.7x and depend on the measuring band (3/36 and 17/38 at 2x or more with a near band), so inheritance there is marginal.
- The cargo and the shell are passive (osm = 0), so the containment does no work for the body. Division and all lineage counts are identical in every arm (bit-identical u).

## Checker

Agrees: True. W decision: by_construction.

- (minor) The audit says the result 'survives a change of measuring band', but that only holds while the outside sample stays at least about 1.5 px from the contour. I measured independently on the saved fields (body = raw (u+1.6) > 0.5, periodic labels). With inside = the whole body and outside = the 0.5-2.5 px ring just outside the contour, the wall-off arm drops to 1.76x with 38% of body-frames at 2x or more (seed 51) and 1.81x / 37% (seed 52). With a 0.5-1.5 px ring it is 1.66x / 32%. The unchanged world on the same measure is 11.4x / 96%. The signed-distance profiles explain why: in the unchanged world the cargo drops sharply at the q ring (c about 2.4 at -2 px, 0.52 at -1 px, 0.17 at +1 px). In the wall-off arm it falls off smoothly with no step (0.95, 0.64, 0.47, 0.39). The decision therefore assumes that 'held across the boundary' compares the body with its surroundings a few px out. That is how the claim itself measured W (whole body against the medium beyond a 3-px dilation), so applying the same measure to the wall-off arm is the consistent choice, and it gives 3.37x / 97.7% and 3.39x / 99.1%. Under a measure that hugs the contour, the decision would flip to 'wall holds'. The audit should say this rather than call the result band-robust.
- (minor) The default band in measure_w.py skips about 2.5 px on both sides of the contour (inside: distance >= 2.5 px; outside: 2.5-5.5 px). That inflates the ratio more for a smooth halo, as in the wall-off arm, than for a step profile, as in the unchanged world, so it leans mildly toward 'held' in the wall-off arm. The audit offsets this by also reporting the near band (2.47x / 75-78%, which I reproduced as 2.47x / 76%) and the claim's own definition. It is a disclosure issue, not an error.
- (minor) The wall-off contrast is not stationary. q decays over 1/kdq = 500 time units, longer than the 400-unit run, so the domain-mean q climbs from 0.05 to 0.65 and the cargo's mobility keeps falling (to exp(-8 x 0.65), about 0.006 Dc in the late medium). As a result the wall-off ratio rises from about 2.3-2.6x (frames 10-45) to 8.5x at t=400. The arm still passes in the early frames on the default band (share 0.98-1.00 per frame). A longer or steady-state run would only strengthen the by-construction reading, but the audit should note that part of the holding comes from this run-length-dependent build-up of q.
- (minor) The cargo_terms field answers 'Yes for the source'. That could be read as triggering the protocol's second by-construction clause (a term in the body field that would hold the cargo inside a filled body). But the body-restricted source alone does not hold the cargo: at beta=0 it gives 1.12x, or 1.33x against the far medium in my check. The decision rests only on the wall-off arm, which the audit's text does say, so this is a matter of wording.

I agree with the audit: W is by construction.

(1) Variants. I diffed each variant against the claim's world.py, which is clean in git.
- walloff.py changes only chi_q from 3 to 0. That sets Vq to 0, so v_div becomes plain diffusion with Dq. q keeps its source (kq/kp)*prod, its decay kdq and its Dq, and the cargo stays gated by q through beta = 8.
- homgate.py changes only line 127, gating the cargo by np.full_like(q, q.mean()): a uniform, lowered D.
- smoothgate.py changes only line 127, gating by q Gaussian-blurred in Fourier space. The blur width is 4*dx in physical units, which is 4 px.
- betaoff.py changes only beta to 0.
- Every variant also changes META name, and nothing else.
No shadow species is needed: osm = 0, so neither q nor c acts back on u.

(2) Measurement. measure_w.py builds bodies with labkit's own segmentation. For each body, inside is the pixels at distance >= 2.5 px from the contour, and outside is a 2.5-5.5 px band, split between bodies by nearest body (Voronoi). The frames are raw float16 fields, not normalized. I rebuilt the measure independently from the saved frames.npz (raw-threshold bodies, periodic labels). It reproduces the audit's numbers:

| arm | audit | mine |
|---|---|---|
| unchanged, seed 51 | 23.8x | 23.1x |
| wall-off, seed 51 | 3.41x | 3.26x (98%) |
| wall-off, seed 52 | 3.51x | 3.38x (99%) |
| homgate | 2.59x | 2.48x (72%) |
| beta = 0 | 1.12x | 1.12x |
| near band, wall-off seed 51 | 2.47x / 74.8% | 2.47x / 76% |

claim_def.py matches the claim's cargo_contrast.py. The only caveat is the band sensitivity listed under problems.

(3) Re-runs. Both re-runs are labkit runs: metrics.json gives world 'fch-gated-micelles', path = the claim's world.py, seeds 51 and 52, and FACTS.md shows the labkit.run command. No other run of this world in the collective used seed 51 or 52 (seeds used: 0, 1, 2, 3, 5, 7, 9, 17, 19). I confirmed that the bodies are bit-identical across arms: max|du| = 0 for wall-off on both seeds and for homgate and betaoff on seed 51. The q field is also identical in homgate and betaoff.

(4) Rule. Applied with the claim's own W measure, the wall-off arm still holds the cargo at 2x or more for almost all body-frames: 3.37x / 97.7% and 3.39x / 99.1% under the claim's definition, and 99.8% / 99.5% on the audit's default band. That is by construction under PROTOCOL.md. The claim's own pack_chiq0 run (2.4-6.7x) and the earlier reviews' chi_q = 0 runs (c01: 7.1x, weakest body 2.5x; c06 on seed 9) agree. The ring is real and raises the contrast about 7x, but it is not needed to clear 2x on a body-versus-surroundings measure. The decision would flip only under a contour-hugging measure (whole body against a 0.5-2.5 px ring), where the wall-off arm gives 1.8x / 37-38% and the unchanged world 11.4x / 96%.

My scripts are /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/wcheck_fchgm/indep.py, /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/wcheck_fchgm/matrix.py and /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/wcheck_fchgm/helpers.py. Nothing under research/alife was modified, and no new simulations were run.
