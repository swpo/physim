# Evidence pack: neural-field-dep (seed 12)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 20 steps x dt 0.1 = time 1400; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/half40_dt2 --seeds 11 12 13 14 --spf 20 --frames 700 --lineage-k 50 --damage 500:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 41.8, max 75; occupancy final 0.10
- tracks: 742; persistent (alive >= 50% of run): 1; longest 356 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 206 long-lived tracks moved >= 1 body length; max speed 0.31/time; max body lengths 34.1
- replication (lineage window K = 50 frames = time 100, --lineage-k): splits 293, persistent splits 42 (0 more failed only because the siblings re-merged within K), max generation 5, merges 88, merge/split ratio 0.3, nucleations 1
- channel total drift (end/start - 1): [-1.0, None, -0.5797, -0.1886]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 410 at frame 376: holes 0, rim-vs-core 0.25, rim-vs-outside 0.91, heterogeneity 0.16; core [0.947, 0.619, 1.0, 0.486] rim [0.722, 0.538, 0.955, 0.545]
  - track 500 at frame 471: holes 0, rim-vs-core 0.26, rim-vs-outside 0.91, heterogeneity 0.17; core [0.917, 0.591, 1.0, 0.401] rim [0.684, 0.525, 0.928, 0.455]
  - track 372 at frame 312: holes 0, rim-vs-core 0.31, rim-vs-outside 0.86, heterogeneity 0.19; core [0.916, 0.542, 1.0, 0.295] rim [0.655, 0.46, 0.88, 0.371]
  - track 670 at frame 641: holes 0, rim-vs-core 0.24, rim-vs-outside 0.90, heterogeneity 0.16; core [0.912, 0.506, 1.0, 0.466] rim [0.69, 0.478, 0.934, 0.51]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 229 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 6 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 3.04 (aggregate of 229 individuals; 0/229 membrane-like individually; rim level 0.715)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 2 (aggregate of 229 individuals; 11/229 membrane-like individually; rim level 0.563)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 33.7 (aggregate of 229 individuals; 0/229 membrane-like individually; rim level 0.839)
  - radial synaptic resource r: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.89 (aggregate of 229 individuals; 13/229 membrane-like individually; rim level 0.418)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #410 (t=752, R_eq 3.52): none; #500 (t=942, R_eq 3.52): none; #372 (t=624, R_eq 3.24): ['synaptic resource r']; #670 (t=1282, R_eq 4.62): none
- damage `half` (requested 0.40 of the area) at frame 500 (t=1000): target = main-run track #586; the individual is one component of 22 px = 0.68x the median individual, aspect 1.09 (rule mature-compact: track age 61 frames vs K=50; 38 individuals from 38 components at that frame; open-ring individuals, not eligible: 0); mask 18 px (9 inside the individual)
- damage MEASURED: the target lost 40.6% of its matter (inside the individual: its components and what they enclose; 9 of 22 px lost > half their matter); net matter lost outside it = 4.33% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 9 of the 18 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[1000.0, 1080.0, 1160.0, 1240.0, 1320.0, 1400.0]: target [0.591, 2.273, 4.0, 3.182, 2.545, 3.682] (matter [0.594, 3.716, 4.78, 6.375, 4.201, 7.019]; pieces [1, 2, 2, 3, 2, 3]; merged with another individual at t=[1222.0]); comparator [1.0, 1.091, 1.182, None, None, None] (matter [1.0, 1.141, 1.239, None, None, None]; pieces [1, 1, 1, 0, 0, 0]; merged with another individual at t=[1234.0]; last seen t=1232). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 229 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
