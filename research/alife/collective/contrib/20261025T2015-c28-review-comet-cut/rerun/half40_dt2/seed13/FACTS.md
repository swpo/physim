# Evidence pack: neural-field-dep (seed 13)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 20 steps x dt 0.1 = time 1400; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/half40_dt2 --seeds 11 12 13 14 --spf 20 --frames 700 --lineage-k 50 --damage 500:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 43, mean 41.4, max 77; occupancy final 0.09
- tracks: 761; persistent (alive >= 50% of run): 0; longest 254 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 43], H1 [0, 0, 0]
- motion: 200 long-lived tracks moved >= 1 body length; max speed 0.298/time; max body lengths 20.0
- replication (lineage window K = 50 frames = time 100, --lineage-k): splits 298, persistent splits 35 (0 more failed only because the siblings re-merged within K), max generation 6, merges 97, merge/split ratio 0.326, nucleations 4
- channel total drift (end/start - 1): [-1.0, None, -0.5829, -0.1824]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 452 at frame 424: holes 0, rim-vs-core 0.31, rim-vs-outside 0.79, heterogeneity 0.19; core [0.886, 0.589, 1.0, 0.378] rim [0.654, 0.509, 0.829, 0.463]
  - track 238 at frame 165: holes 0, rim-vs-core 0.27, rim-vs-outside 0.89, heterogeneity 0.17; core [0.941, 0.518, 1.0, 0.33] rim [0.692, 0.448, 0.923, 0.339]
  - track 391 at frame 324: holes 0, rim-vs-core 0.23, rim-vs-outside 0.89, heterogeneity 0.15; core [0.889, 0.532, 1.0, 0.233] rim [0.683, 0.474, 0.928, 0.266]
  - track 607 at frame 588: holes 0, rim-vs-core 0.25, rim-vs-outside 0.85, heterogeneity 0.16; core [0.908, 0.593, 1.0, 0.358] rim [0.695, 0.508, 0.93, 0.417]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 227 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 12 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 3.04 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.719)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 2.05 (aggregate of 227 individuals; 7/227 membrane-like individually; rim level 0.557)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 31.4 (aggregate of 227 individuals; 1/227 membrane-like individually; rim level 0.831)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.53, rim/outside 0.871 (aggregate of 227 individuals; 13/227 membrane-like individually; rim level 0.416)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #452 (t=848, R_eq 3.74): none; #238 (t=330, R_eq 3.19): none; #391 (t=648, R_eq 3.61): none; #607 (t=1176, R_eq 3.57): none
- damage `half` (requested 0.40 of the area) at frame 500 (t=1000): target = main-run track #530; the individual is one component of 28 px = 0.82x the median individual, aspect 1.43 (rule mature-compact: track age 91 frames vs K=50; 38 individuals from 38 components at that frame; open-ring individuals, not eligible: 0); mask 20 px (11 inside the individual)
- damage MEASURED: the target lost 39.3% of its matter (inside the individual: its components and what they enclose; 11 of 28 px lost > half their matter); net matter lost outside it = 4.3% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 9 of the 20 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[1000.0, 1080.0, 1160.0, 1240.0, 1320.0, 1400.0]: target [0.607, 2.607, 4.607, None, None, None] (matter [0.607, 2.435, 5.05, None, None, None]; pieces [1, 1, 2, 0, 0, 0]; merged with another individual at t=[1172.0, 1236.0]; last seen t=1234); comparator [1.0, 0.871, None, None, None, None] (matter [1.0, 0.916, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; last seen t=1132). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 227 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
