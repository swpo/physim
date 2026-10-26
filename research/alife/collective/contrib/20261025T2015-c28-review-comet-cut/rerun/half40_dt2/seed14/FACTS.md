# Evidence pack: neural-field-dep (seed 14)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 20 steps x dt 0.1 = time 1400; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/half40_dt2 --seeds 11 12 13 14 --spf 20 --frames 700 --lineage-k 50 --damage 500:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 44, mean 38.3, max 70; occupancy final 0.11
- tracks: 656; persistent (alive >= 50% of run): 1; longest 433 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 44, 44], H1 [0, 0, 0]
- motion: 183 long-lived tracks moved >= 1 body length; max speed 0.316/time; max body lengths 36.8
- replication (lineage window K = 50 frames = time 100, --lineage-k): splits 263, persistent splits 43 (0 more failed only because the siblings re-merged within K), max generation 7, merges 72, merge/split ratio 0.274, nucleations 6
- channel total drift (end/start - 1): [-1.0, None, -0.5501, -0.1921]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 299 at frame 329: holes 0, rim-vs-core 0.19, rim-vs-outside 0.90, heterogeneity 0.14; core [0.871, 0.484, 1.0, 0.317] rim [0.695, 0.465, 0.946, 0.357]
  - track 161 at frame 176: holes 0, rim-vs-core 0.24, rim-vs-outside 0.87, heterogeneity 0.15; core [0.917, 0.702, 1.0, 0.294] rim [0.733, 0.579, 0.959, 0.381]
  - track 374 at frame 376: holes 0, rim-vs-core 0.20, rim-vs-outside 0.89, heterogeneity 0.15; core [0.93, 0.455, 1.0, 0.401] rim [0.736, 0.432, 0.952, 0.41]
  - track 610 at frame 671: holes 0, rim-vs-core 0.24, rim-vs-outside 0.89, heterogeneity 0.15; core [0.884, 0.554, 1.0, 0.195] rim [0.678, 0.482, 0.936, 0.26]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 219 components >= 12 px at frames [118, 235, 353, 465, 582, 700]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 2.94 (aggregate of 219 individuals; 0/219 membrane-like individually; rim level 0.71)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 1.91 (aggregate of 219 individuals; 9/219 membrane-like individually; rim level 0.541)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 29.4 (aggregate of 219 individuals; 1/219 membrane-like individually; rim level 0.831)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.869 (aggregate of 219 individuals; 5/219 membrane-like individually; rim level 0.405)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #299 (t=658, R_eq 4.33): none; #161 (t=352, R_eq 3.14): none; #374 (t=752, R_eq 5.23): none; #610 (t=1342, R_eq 2.99): none
- damage `half` (requested 0.40 of the area) at frame 500 (t=1000): target = main-run track #374; the individual is one component of 17 px = 0.53x the median individual, aspect 1.14 (rule mature-compact: track age 252 frames vs K=50; 32 individuals from 32 components at that frame; open-ring individuals, not eligible: 1); mask 15 px (7 inside the individual)
- damage MEASURED: the target lost 42.1% of its matter (inside the individual: its components and what they enclose; 7 of 17 px lost > half their matter); net matter lost outside it = 4.88% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 8 of the 15 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[1000.0, 1080.0, 1160.0, 1240.0, 1320.0, 1400.0]: target [0.471, None, None, None, None, None] (matter [0.502, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=1004); comparator [1.0, 1.444, None, None, None, None] (matter [1.0, 1.433, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; last seen t=1136). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 219 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
