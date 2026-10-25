# Evidence pack: neural-field-dep (seed 12)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/core50 --seeds 11 12 13 14 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.5:core --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 38, mean 42.9, max 75; occupancy final 0.09
- tracks: 775; persistent (alive >= 50% of run): 0; longest 272 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 38], H1 [0, 0, 0]
- motion: 219 long-lived tracks moved >= 1 body length; max speed 0.596/time; max body lengths 20.9
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 309, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 7, merges 91, merge/split ratio 0.294, nucleations 1
- channel total drift (end/start - 1): [-1.0, None, -0.6273, -0.1882]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 489 at frame 459: holes 0, rim-vs-core 0.33, rim-vs-outside 0.88, heterogeneity 0.17; core [0.907, 0.715, 1.0, 0.186] rim [0.748, 0.488, 0.925, 0.342]
  - track 538 at frame 524: holes 0, rim-vs-core 0.30, rim-vs-outside 0.88, heterogeneity 0.17; core [0.931, 0.675, 1.0, 0.449] rim [0.695, 0.533, 0.924, 0.554]
  - track 579 at frame 547: holes 0, rim-vs-core 0.31, rim-vs-outside 0.86, heterogeneity 0.17; core [0.915, 0.624, 1.0, 0.348] rim [0.679, 0.489, 0.901, 0.467]
  - track 713 at frame 659: holes 0, rim-vs-core 0.24, rim-vs-outside 0.88, heterogeneity 0.17; core [0.911, 0.575, 1.0, 0.291] rim [0.705, 0.492, 0.927, 0.364]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 238 components >= 12 px at frames [118, 235, 353, 465, 582, 700]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 3.03 (aggregate of 238 individuals; 0/238 membrane-like individually; rim level 0.716)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 1.92 (aggregate of 238 individuals; 7/238 membrane-like individually; rim level 0.542)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 32.8 (aggregate of 238 individuals; 2/238 membrane-like individually; rim level 0.844)
  - radial synaptic resource r: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.878 (aggregate of 238 individuals; 8/238 membrane-like individually; rim level 0.404)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #489 (t=459, R_eq 3.19): none; #538 (t=524, R_eq 2.99): none; #579 (t=547, R_eq 3.04): none; #713 (t=659, R_eq 3.83): none
- damage `core` (requested 0.50 of the area) at frame 500 (t=500): target = main-run track #583; the individual is one component of 22 px = 0.67x the median individual, aspect 1.38 (rule mature-compact: track age 67 frames vs K=50; 42 individuals from 42 components at that frame; open-ring individuals, not eligible: 0); mask 12 px (12 inside the individual)
- damage MEASURED: the target lost 57.6% of its matter (inside the individual: its components and what they enclose; 12 of 22 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [None, None, None, None, None, None] (matter [None, None, None, None, None, None]; pieces [0, 0, 0, 0, 0, 0]; not seen after the cut); comparator [1.0, 1.381, None, None, None, None] (matter [1.0, 1.398, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; merged with another individual at t=[542.0]; last seen t=541). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 238 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
