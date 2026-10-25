# Evidence pack: neural-field-dep (seed 11)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 20 steps x dt 0.1 = time 1400; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/half40_dt2 --seeds 11 12 13 14 --spf 20 --frames 700 --lineage-k 50 --damage 500:0.4:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 30, mean 41.3, max 72; occupancy final 0.09
- tracks: 716; persistent (alive >= 50% of run): 0; longest 295 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 204 long-lived tracks moved >= 1 body length; max speed 0.305/time; max body lengths 24.3
- replication (lineage window K = 50 frames = time 100, --lineage-k): splits 275, persistent splits 49 (0 more failed only because the siblings re-merged within K), max generation 5, merges 103, merge/split ratio 0.375, nucleations 2
- channel total drift (end/start - 1): [-1.0, None, -0.5941, -0.173]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 330 at frame 288: holes 0, rim-vs-core 0.26, rim-vs-outside 0.91, heterogeneity 0.16; core [0.945, 0.542, 1.0, 0.361] rim [0.697, 0.473, 0.951, 0.353]
  - track 384 at frame 376: holes 0, rim-vs-core 0.28, rim-vs-outside 0.84, heterogeneity 0.17; core [0.907, 0.504, 1.0, 0.287] rim [0.666, 0.411, 0.901, 0.35]
  - track 302 at frame 212: holes 0, rim-vs-core 0.27, rim-vs-outside 0.78, heterogeneity 0.17; core [0.886, 0.563, 1.0, 0.24] rim [0.676, 0.49, 0.869, 0.312]
  - track 649 at frame 647: holes 0, rim-vs-core 0.24, rim-vs-outside 0.91, heterogeneity 0.15; core [0.885, 0.597, 1.0, 0.399] rim [0.679, 0.516, 0.917, 0.419]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 233 components >= 12 px at frames [118, 235, 353, 465, 582, 700]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 3.13 (aggregate of 233 individuals; 0/233 membrane-like individually; rim level 0.725)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 1.99 (aggregate of 233 individuals; 10/233 membrane-like individually; rim level 0.55)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 35.4 (aggregate of 233 individuals; 0/233 membrane-like individually; rim level 0.85)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.52, rim/outside 0.902 (aggregate of 233 individuals; 8/233 membrane-like individually; rim level 0.418)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #330 (t=576, R_eq 3.09): none; #384 (t=752, R_eq 2.76): none; #302 (t=424, R_eq 2.88): none; #649 (t=1294, R_eq 4.15): none
- damage `half` (requested 0.40 of the area) at frame 500 (t=1000): target = main-run track #538; the individual is one component of 33 px = 1.00x the median individual, aspect 1.24 (rule mature-compact: track age 58 frames vs K=50; 43 individuals from 43 components at that frame; open-ring individuals, not eligible: 1); mask 23 px (13 inside the individual)
- damage MEASURED: the target lost 39.1% of its matter (inside the individual: its components and what they enclose; 13 of 33 px lost > half their matter); net matter lost outside it = 2.42% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 10 of the 23 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[1000.0, 1080.0, 1160.0, 1240.0, 1320.0, 1400.0]: target [0.606, None, None, None, None, None] (matter [0.609, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[1044.0]; last seen t=1042); comparator [1.0, 0.5, 1.156, 2.0, 2.469, 0.844] (matter [1.0, 0.493, 1.182, 2.914, 3.476, 0.855]; pieces [1, 1, 1, 2, 2, 1]; merged with another individual at t=[1392.0, 1398.0]). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 233 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
