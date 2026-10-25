# Evidence pack: neural-field-dep (seed 3)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/half50 --seeds 2 3 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.5:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 34, mean 39.9, max 77; occupancy final 0.09
- tracks: 720; persistent (alive >= 50% of run): 2; longest 419 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.20 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 34], H1 [0, 0, 0]
- motion: 189 long-lived tracks moved >= 1 body length; max speed 0.601/time; max body lengths 33.7
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 281, persistent splits 43 (0 more failed only because the siblings re-merged within K), max generation 6, merges 87, merge/split ratio 0.31, nucleations 7
- channel total drift (end/start - 1): [-1.0, None, -0.6045, -0.174]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 356 at frame 376: holes 0, rim-vs-core 0.27, rim-vs-outside 0.82, heterogeneity 0.16; core [0.891, 0.537, 1.0, 0.202] rim [0.662, 0.451, 0.895, 0.251]
  - track 431 at frame 447: holes 0, rim-vs-core 0.29, rim-vs-outside 0.90, heterogeneity 0.16; core [0.906, 0.6, 1.0, 0.339] rim [0.674, 0.493, 0.92, 0.44]
  - track 551 at frame 529: holes 0, rim-vs-core 0.27, rim-vs-outside 0.84, heterogeneity 0.17; core [0.933, 0.565, 1.0, 0.34] rim [0.696, 0.48, 0.91, 0.342]
  - track 628 at frame 606: holes 0, rim-vs-core 0.24, rim-vs-outside 0.87, heterogeneity 0.17; core [0.926, 0.555, 1.0, 0.485] rim [0.706, 0.508, 0.922, 0.531]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 212 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 2 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 2.89 (aggregate of 212 individuals; 0/212 membrane-like individually; rim level 0.701)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 1.88 (aggregate of 212 individuals; 4/212 membrane-like individually; rim level 0.541)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 25.5 (aggregate of 212 individuals; 1/212 membrane-like individually; rim level 0.811)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.49, rim/outside 0.883 (aggregate of 212 individuals; 15/212 membrane-like individually; rim level 0.414)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #356 (t=376, R_eq 3.09): none; #431 (t=447, R_eq 3.43): none; #551 (t=529, R_eq 3.29, DAMAGED): none; #628 (t=606, R_eq 4.11): none
- damage `half` (requested 0.50 of the area) at frame 500 (t=500): target = main-run track #551; the individual is one component of 28 px = 0.76x the median individual, aspect 1.32 (rule mature-compact: track age 95 frames vs K=50; 31 individuals from 31 components at that frame; open-ring individuals, not eligible: 2); mask 23 px (14 inside the individual)
- damage MEASURED: the target lost 50.4% of its matter (inside the individual: its components and what they enclose; 14 of 28 px lost > half their matter); net matter lost outside it = 1.67% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 9 of the 23 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [0.5, 1.25, 1.071, 1.071, None, None] (matter [0.496, 1.255, 1.052, 1.09, None, None]; pieces [1, 1, 1, 1, 0, 0]; merged with another individual at t=[654.0]; last seen t=653); comparator [1.0, 1.406, None, None, None, None] (matter [1.0, 1.401, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; merged with another individual at t=[557.0]; last seen t=556). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 212 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
