# Evidence pack: neural-field-dep (seed 1)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/comrep/half --seeds 0 1 --spf 50 --damage 100:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 34, mean 40.8, max 70; occupancy final 0.09
- tracks: 761; persistent (alive >= 50% of run): 0; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 35, 35], H1 [0, 0, 0]
- motion: 121 long-lived tracks moved >= 1 body length; max speed 0.584/time; max body lengths 40.7
- replication (lineage window K = 20 frames = time 100, default): splits 304, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 7, merges 79, merge/split ratio 0.26, nucleations 7
- channel total drift (end/start - 1): [1.0, None, -0.528, -0.1886]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 365 at frame 100: holes 0, rim-vs-core 0.30, rim-vs-outside 0.85, heterogeneity 0.18; core [0.932, 0.538, 1.0, 0.375] rim [0.671, 0.436, 0.889, 0.395]
  - track 566 at frame 156: holes 0, rim-vs-core 0.29, rim-vs-outside 0.89, heterogeneity 0.17; core [0.931, 0.552, 1.0, 0.348] rim [0.681, 0.441, 0.933, 0.396]
  - track 690 at frame 183: holes 0, rim-vs-core 0.28, rim-vs-outside 0.89, heterogeneity 0.16; core [0.892, 0.554, 1.0, 0.172] rim [0.647, 0.477, 0.9, 0.238]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 213 components >= 12 px at frames [34, 67, 100, 133, 166, 200]; 5 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 2.95 (aggregate of 213 individuals; 0/213 membrane-like individually; rim level 0.708)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 1.93 (aggregate of 213 individuals; 7/213 membrane-like individually; rim level 0.545)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 30.4 (aggregate of 213 individuals; 0/213 membrane-like individually; rim level 0.819)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.851 (aggregate of 213 individuals; 4/213 membrane-like individually; rim level 0.403)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #365 (t=500, R_eq 3.57): none; #536 (t=730, R_eq 6.18): none; #566 (t=780, R_eq 3.34): none; #690 (t=915, R_eq 2.88): none
- damage `half` (requested 0.40 of the area) at frame 100 (t=500): target = main-run track #423; the individual is one component of 30 px = 0.80x the median individual, aspect 1.37 (rule mature-compact: track age 33 frames vs K=20; 36 individuals from 36 components at that frame; open-ring individuals, not eligible: 0); mask 22 px (12 inside the individual)
- damage MEASURED: the target lost 41% of its matter (inside the individual: its components and what they enclose; 12 of 30 px lost > half their matter); net matter lost outside it = 1.3% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 10 of the 22 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]: target [0.567, 1.067, None, None, None, None] (matter [0.568, 1.11, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; merged with another individual at t=[640.0]; last seen t=635); comparator [1.0, 1.448, 4.379, 1.345, 1.172, 5.207] (matter [1.0, 3.876, 8.138, 2.157, 2.902, 15.089]; pieces [1, 3, 3, 2, 3, 7]; merged with another individual at t=[620.0, 710.0, 730.0, 740.0]). Follow-up: pre-cut field at frame 100, then recorded frames 100..200 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 213 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
