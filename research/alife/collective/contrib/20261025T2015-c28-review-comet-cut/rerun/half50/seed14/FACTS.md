# Evidence pack: neural-field-dep (seed 14)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/half50 --seeds 11 12 13 14 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.5:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 32, mean 42.8, max 71; occupancy final 0.09
- tracks: 693; persistent (alive >= 50% of run): 1; longest 374 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.95 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 32, 32], H1 [0, 0, 0]
- motion: 203 long-lived tracks moved >= 1 body length; max speed 0.615/time; max body lengths 33.9
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 275, persistent splits 56 (0 more failed only because the siblings re-merged within K), max generation 7, merges 82, merge/split ratio 0.298, nucleations 5
- channel total drift (end/start - 1): [-1.0, None, -0.6259, -0.1713]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 460 at frame 518: holes 0, rim-vs-core 0.29, rim-vs-outside 0.87, heterogeneity 0.17; core [0.912, 0.54, 1.0, 0.38] rim [0.669, 0.42, 0.908, 0.444]
  - track 494 at frame 541: holes 0, rim-vs-core 0.27, rim-vs-outside 0.85, heterogeneity 0.16; core [0.878, 0.476, 1.0, 0.2] rim [0.667, 0.409, 0.901, 0.316]
  - track 299 at frame 241: holes 0, rim-vs-core 0.24, rim-vs-outside 0.81, heterogeneity 0.15; core [0.923, 0.605, 1.0, 0.304] rim [0.711, 0.534, 0.944, 0.368]
  - track 619 at frame 594: holes 0, rim-vs-core 0.25, rim-vs-outside 0.80, heterogeneity 0.19; core [0.873, 0.533, 1.0, 0.378] rim [0.664, 0.483, 0.876, 0.41]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 235 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 2 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 3.05 (aggregate of 235 individuals; 0/235 membrane-like individually; rim level 0.714)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 2.06 (aggregate of 235 individuals; 5/235 membrane-like individually; rim level 0.567)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 37.6 (aggregate of 235 individuals; 0/235 membrane-like individually; rim level 0.82)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.865 (aggregate of 235 individuals; 12/235 membrane-like individually; rim level 0.412)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #460 (t=518, R_eq 4.07): none; #494 (t=541, R_eq 3.66): none; #299 (t=241, R_eq 2.52): none; #619 (t=594, R_eq 3.87): none
- damage `half` (requested 0.50 of the area) at frame 500 (t=500): target = main-run track #519; the individual is one component of 26 px = 0.81x the median individual, aspect 1.19 (rule mature-compact: track age 76 frames vs K=50; 42 individuals from 42 components at that frame; open-ring individuals, not eligible: 1); mask 22 px (13 inside the individual)
- damage MEASURED: the target lost 50.6% of its matter (inside the individual: its components and what they enclose; 13 of 26 px lost > half their matter); net matter lost outside it = 4.31% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 9 of the 22 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [0.462, 1.577, 1.577, 1.692, None, None] (matter [0.47, 1.595, 1.594, 1.681, None, None]; pieces [1, 1, 1, 1, 0, 0]; merged with another individual at t=[660.0]; last seen t=659); comparator [1.0, 1.708, 1.542, 1.542, 1.667, 1.833] (matter [1.0, 1.713, 1.52, 1.554, 1.693, 1.865]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 235 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
