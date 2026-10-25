# Evidence pack: neural-field-dep (seed 0)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/half --seeds 0 1 --spf 50 --damage 100:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 42, mean 38.0, max 69; occupancy final 0.11
- tracks: 584; persistent (alive >= 50% of run): 3; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.91 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 42], H1 [0, 0, 0]
- motion: 127 long-lived tracks moved >= 1 body length; max speed 0.587/time; max body lengths 42.7
- replication (lineage window K = 20 frames = time 100, default): splits 232, persistent splits 35 (0 more failed only because the siblings re-merged within K), max generation 7, merges 51, merge/split ratio 0.22, nucleations 9
- channel total drift (end/start - 1): [-1.0, None, -0.5314, -0.2071]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 440 at frame 148: holes 0, rim-vs-core 0.31, rim-vs-outside 0.85, heterogeneity 0.19; core [0.937, 0.609, 1.0, 0.433] rim [0.687, 0.481, 0.918, 0.532]
  - track 449 at frame 150: holes 0, rim-vs-core 0.26, rim-vs-outside 0.82, heterogeneity 0.16; core [0.907, 0.535, 1.0, 0.205] rim [0.693, 0.46, 0.943, 0.327]
  - track 450 at frame 150: holes 0, rim-vs-core 0.25, rim-vs-outside 0.84, heterogeneity 0.17; core [0.901, 0.525, 1.0, 0.288] rim [0.681, 0.459, 0.915, 0.348]
  - track 558 at frame 185: holes 0, rim-vs-core 0.26, rim-vs-outside 0.90, heterogeneity 0.16; core [0.931, 0.545, 1.0, 0.294] rim [0.689, 0.479, 0.951, 0.352]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 214 components >= 12 px at frames [34, 67, 100, 133, 166, 200]; 2 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 2.97 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.706)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 1.92 (aggregate of 214 individuals; 6/214 membrane-like individually; rim level 0.532)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 26.3 (aggregate of 214 individuals; 3/214 membrane-like individually; rim level 0.799)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.875 (aggregate of 214 individuals; 9/214 membrane-like individually; rim level 0.407)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #440 (t=740, R_eq 3.19): none; #449 (t=750, R_eq 3.19): ['adaptation a']; #450 (t=750, R_eq 3.57): none; #558 (t=925, R_eq 3.19): none
- damage `half` (requested 0.40 of the area) at frame 100 (t=500): target = main-run track #400; the individual is one component of 33 px = 0.92x the median individual, aspect 1.57 (rule mature-compact: track age 29 frames vs K=20; 28 individuals from 28 components at that frame; open-ring individuals, not eligible: 1); mask 22 px (13 inside the individual)
- damage MEASURED: the target lost 38.6% of its matter (inside the individual: its components and what they enclose; 13 of 33 px lost > half their matter); net matter lost outside it = 2.23% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 9 of the 22 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]: target [0.606, 1.636, None, None, None, None] (matter [0.614, 1.659, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; last seen t=680); comparator [1.0, 1.865, 2.135, 2.432, 1.324, 2.135] (matter [1.0, 3.522, 7.208, 8.294, 4.754, 6.138]; pieces [1, 2, 7, 7, 5, 5]; re-nucleated pieces picked up at t=[790.0]). Follow-up: pre-cut field at frame 100, then recorded frames 100..200 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 214 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- damage target is elongated (aspect 1.57 > 1.5; rule mature-compact): it may be elongating or pinching (dividing) rather than a compact individual; check damage.png or damage at another frame

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
