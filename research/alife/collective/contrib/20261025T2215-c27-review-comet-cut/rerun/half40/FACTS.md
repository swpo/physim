# Evidence pack: neural-field-dep (seed 25)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27b/world.py --out collective/contrib/wip-c27b/rerun/half40 --seeds 25 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 39, mean 40.5, max 74; occupancy final 0.10
- tracks: 743; persistent (alive >= 50% of run): 0; longest 315 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [0, 0, 0]
- motion: 183 long-lived tracks moved >= 1 body length; max speed 0.595/time; max body lengths 21.8
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 281, persistent splits 37 (0 more failed only because the siblings re-merged within K), max generation 5, merges 105, merge/split ratio 0.374, nucleations 7
- channel total drift (end/start - 1): [1.0, None, -0.4903, -0.1945]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 360 at frame 324: holes 0, rim-vs-core 0.23, rim-vs-outside 0.88, heterogeneity 0.17; core [0.885, 0.464, 1.0, 0.348] rim [0.679, 0.458, 0.906, 0.377]
  - track 427 at frame 412: holes 0, rim-vs-core 0.27, rim-vs-outside 0.88, heterogeneity 0.17; core [0.928, 0.463, 1.0, 0.335] rim [0.684, 0.426, 0.903, 0.378]
  - track 239 at frame 188: holes 0, rim-vs-core 0.26, rim-vs-outside 0.84, heterogeneity 0.17; core [0.918, 0.537, 1.0, 0.253] rim [0.703, 0.442, 0.922, 0.34]
  - track 663 at frame 641: holes 0, rim-vs-core 0.28, rim-vs-outside 0.83, heterogeneity 0.18; core [0.888, 0.609, 1.0, 0.288] rim [0.696, 0.501, 0.862, 0.4]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 227 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 3 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 3.06 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.72)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 2.01 (aggregate of 227 individuals; 4/227 membrane-like individually; rim level 0.553)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 35.9 (aggregate of 227 individuals; 1/227 membrane-like individually; rim level 0.835)
  - radial synaptic resource r: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.56, rim/outside 0.878 (aggregate of 227 individuals; 16/227 membrane-like individually; rim level 0.414)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #360 (t=324, R_eq 4.62): none; #427 (t=412, R_eq 3.83): none; #239 (t=188, R_eq 3.43): none; #663 (t=641, R_eq 3.39): none
- damage `half` (requested 0.40 of the area) at frame 500 (t=500): target = main-run track #480; the individual is one component of 24 px = 0.69x the median individual, aspect 1.23 (rule mature-compact: track age 157 frames vs K=50; 35 individuals from 35 components at that frame; open-ring individuals, not eligible: 1); mask 18 px (10 inside the individual)
- damage MEASURED: the target lost 42.8% of its matter (inside the individual: its components and what they enclose; 10 of 24 px lost > half their matter); net matter lost outside it = 4.7% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 8 of the 18 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [0.542, 1.458, 2.083, 1.458, 2.125, 1.5] (matter [0.545, 1.489, 2.168, 2.759, 2.865, 3.05]; pieces [1, 1, 1, 2, 2, 2]); comparator [1.0, 3.042, None, None, None, None] (matter [1.0, 3.112, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; merged with another individual at t=[560.0]; last seen t=559). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 227 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
