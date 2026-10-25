# Evidence pack: neural-field-dep (seed 14)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/half40 --seeds 11 12 13 14 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 43.6, max 71; occupancy final 0.10
- tracks: 724; persistent (alive >= 50% of run): 1; longest 363 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.36 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 40, 40], H1 [0, 0, 0]
- motion: 211 long-lived tracks moved >= 1 body length; max speed 0.615/time; max body lengths 32.8
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 288, persistent splits 59 (0 more failed only because the siblings re-merged within K), max generation 7, merges 87, merge/split ratio 0.302, nucleations 5
- channel total drift (end/start - 1): [-1.0, None, -0.5638, -0.1875]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 460 at frame 512: holes 0, rim-vs-core 0.27, rim-vs-outside 0.88, heterogeneity 0.17; core [0.958, 0.495, 1.0, 0.418] rim [0.713, 0.407, 0.948, 0.489]
  - track 494 at frame 541: holes 0, rim-vs-core 0.27, rim-vs-outside 0.85, heterogeneity 0.16; core [0.878, 0.477, 1.0, 0.202] rim [0.668, 0.409, 0.901, 0.317]
  - track 507 at frame 553: holes 0, rim-vs-core 0.33, rim-vs-outside 0.78, heterogeneity 0.18; core [0.925, 0.58, 1.0, 0.301] rim [0.678, 0.432, 0.874, 0.41]
  - track 619 at frame 594: holes 0, rim-vs-core 0.28, rim-vs-outside 0.84, heterogeneity 0.18; core [0.923, 0.614, 1.0, 0.435] rim [0.685, 0.538, 0.891, 0.498]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 242 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 2 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 3 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.709)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 2.06 (aggregate of 242 individuals; 6/242 membrane-like individually; rim level 0.569)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 35.2 (aggregate of 242 individuals; 1/242 membrane-like individually; rim level 0.82)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.51, rim/outside 0.864 (aggregate of 242 individuals; 10/242 membrane-like individually; rim level 0.409)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #460 (t=512, R_eq 3.57): ['synaptic resource r']; #494 (t=541, R_eq 3.66): none; #507 (t=553, R_eq 3.24): none; #619 (t=594, R_eq 3.57): none
- damage `half` (requested 0.40 of the area) at frame 500 (t=500): target = main-run track #519; the individual is one component of 26 px = 0.81x the median individual, aspect 1.19 (rule mature-compact: track age 76 frames vs K=50; 42 individuals from 42 components at that frame; open-ring individuals, not eligible: 1); mask 19 px (11 inside the individual)
- damage MEASURED: the target lost 42.6% of its matter (inside the individual: its components and what they enclose; 11 of 26 px lost > half their matter); net matter lost outside it = 4.31% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 8 of the 19 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [0.577, 1.615, 1.538, 1.615, None, None] (matter [0.574, 1.622, 1.567, 1.639, None, None]; pieces [1, 1, 1, 1, 0, 0]; merged with another individual at t=[659.0]; last seen t=658); comparator [1.0, 1.708, 1.542, 1.542, 1.875, 1.333] (matter [1.0, 1.713, 1.52, 1.558, 1.851, 1.35]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 242 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
