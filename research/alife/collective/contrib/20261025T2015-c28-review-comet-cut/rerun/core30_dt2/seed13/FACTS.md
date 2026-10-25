# Evidence pack: neural-field-dep (seed 13)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 20 steps x dt 0.1 = time 1400; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/core30_dt2 --seeds 11 12 13 14 --spf 20 --frames 700 --lineage-k 50 --damage 500:0.3:core --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 45, mean 41.6, max 77; occupancy final 0.09
- tracks: 758; persistent (alive >= 50% of run): 0; longest 283 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 45, 45], H1 [0, 0, 0]
- motion: 209 long-lived tracks moved >= 1 body length; max speed 0.299/time; max body lengths 20.0
- replication (lineage window K = 50 frames = time 100, --lineage-k): splits 298, persistent splits 39 (0 more failed only because the siblings re-merged within K), max generation 6, merges 94, merge/split ratio 0.315, nucleations 4
- channel total drift (end/start - 1): [-1.0, None, -0.6054, -0.1877]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 452 at frame 441: holes 0, rim-vs-core 0.24, rim-vs-outside 0.84, heterogeneity 0.17; core [0.894, 0.549, 1.0, 0.427] rim [0.679, 0.508, 0.915, 0.475]
  - track 238 at frame 165: holes 0, rim-vs-core 0.27, rim-vs-outside 0.89, heterogeneity 0.17; core [0.941, 0.519, 1.0, 0.33] rim [0.693, 0.448, 0.923, 0.34]
  - track 391 at frame 324: holes 0, rim-vs-core 0.23, rim-vs-outside 0.89, heterogeneity 0.15; core [0.89, 0.533, 1.0, 0.234] rim [0.683, 0.475, 0.928, 0.267]
  - track 609 at frame 606: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.16; core [0.895, 0.552, 1.0, 0.44] rim [0.675, 0.488, 0.917, 0.472]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 231 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 10 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 3.08 (aggregate of 231 individuals; 0/231 membrane-like individually; rim level 0.724)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 2.05 (aggregate of 231 individuals; 7/231 membrane-like individually; rim level 0.567)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 33.3 (aggregate of 231 individuals; 1/231 membrane-like individually; rim level 0.841)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.53, rim/outside 0.875 (aggregate of 231 individuals; 11/231 membrane-like individually; rim level 0.412)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #452 (t=882, R_eq 4.15): none; #238 (t=330, R_eq 3.19): none; #391 (t=648, R_eq 3.61): none; #609 (t=1212, R_eq 4.48): none
- damage `core` (requested 0.30 of the area) at frame 500 (t=1000): target = main-run track #530; the individual is one component of 28 px = 0.82x the median individual, aspect 1.43 (rule mature-compact: track age 91 frames vs K=50; 38 individuals from 38 components at that frame; open-ring individuals, not eligible: 0); mask 10 px (10 inside the individual)
- damage MEASURED: the target lost 36.1% of its matter (inside the individual: its components and what they enclose; 10 of 28 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[1000.0, 1080.0, 1160.0, 1240.0, 1320.0, 1400.0]: target [0.357, 2.321, 1.75, 1.714, 2.143, 1.0] (matter [0.603, 2.301, 3.529, 2.841, 2.966, 2.9]; pieces [2, 1, 3, 2, 2, 3]; merged with another individual at t=[1166.0]); comparator [1.0, 0.903, None, None, None, None] (matter [1.0, 0.931, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; last seen t=1132). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 231 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
