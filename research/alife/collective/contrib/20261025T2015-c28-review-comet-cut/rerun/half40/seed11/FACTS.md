# Evidence pack: neural-field-dep (seed 11)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/half40 --seeds 11 12 13 14 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 31, mean 38.9, max 71; occupancy final 0.09
- tracks: 694; persistent (alive >= 50% of run): 1; longest 439 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 172 long-lived tracks moved >= 1 body length; max speed 0.603/time; max body lengths 27.2
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 265, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 10, merges 94, merge/split ratio 0.355, nucleations 3
- channel total drift (end/start - 1): [-1.0, None, -0.6074, -0.174]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 378 at frame 412: holes 0, rim-vs-core 0.26, rim-vs-outside 0.88, heterogeneity 0.19; core [0.919, 0.499, 1.0, 0.496] rim [0.68, 0.474, 0.894, 0.516]
  - track 131 at frame 182: holes 0, rim-vs-core 0.22, rim-vs-outside 0.91, heterogeneity 0.15; core [0.9, 0.539, 1.0, 0.418] rim [0.691, 0.501, 0.946, 0.463]
  - track 478 at frame 482: holes 0, rim-vs-core 0.26, rim-vs-outside 0.88, heterogeneity 0.17; core [0.917, 0.617, 1.0, 0.406] rim [0.69, 0.537, 0.92, 0.461]
  - track 587 at frame 559: holes 0, rim-vs-core 0.28, rim-vs-outside 0.85, heterogeneity 0.16; core [0.891, 0.546, 1.0, 0.141] rim [0.66, 0.475, 0.906, 0.252]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 213 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 5 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 2.92 (aggregate of 213 individuals; 0/213 membrane-like individually; rim level 0.701)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 1.96 (aggregate of 213 individuals; 5/213 membrane-like individually; rim level 0.549)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 28 (aggregate of 213 individuals; 1/213 membrane-like individually; rim level 0.803)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.49, rim/outside 0.862 (aggregate of 213 individuals; 4/213 membrane-like individually; rim level 0.404)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #378 (t=412, R_eq 5.29): none; #131 (t=182, R_eq 4.11): none; #478 (t=482, R_eq 3.99): none; #587 (t=559, R_eq 2.99): none
- damage `half` (requested 0.40 of the area) at frame 500 (t=500): target = main-run track #548; the individual is one component of 16 px = 0.50x the median individual, aspect 1.23 (rule mature-compact: track age 52 frames vs K=50; 31 individuals from 31 components at that frame; open-ring individuals, not eligible: 2); mask 13 px (7 inside the individual)
- damage MEASURED: the target lost 43.9% of its matter (inside the individual: its components and what they enclose; 7 of 16 px lost > half their matter); net matter lost outside it = 3.54% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 6 of the 13 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [0.562, None, None, None, None, None] (matter [0.561, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[503.0]; last seen t=502); comparator [1.0, None, None, None, None, None] (matter [1.0, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[503.0]; last seen t=502). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 213 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
