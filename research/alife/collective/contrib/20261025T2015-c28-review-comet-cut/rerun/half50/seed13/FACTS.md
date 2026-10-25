# Evidence pack: neural-field-dep (seed 13)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/half50 --seeds 11 12 13 14 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.5:half --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 39.3, max 75; occupancy final 0.10
- tracks: 692; persistent (alive >= 50% of run): 1; longest 442 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 177 long-lived tracks moved >= 1 body length; max speed 0.639/time; max body lengths 27.1
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 267, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 7, merges 90, merge/split ratio 0.337, nucleations 3
- channel total drift (end/start - 1): [-1.0, None, -0.5559, -0.176]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 167 at frame 259: holes 0, rim-vs-core 0.13, rim-vs-outside 1.02, heterogeneity 0.15; core [0.894, 0.434, 1.0, 0.349] rim [0.765, 0.445, 0.966, 0.352]
  - track 495 at frame 553: holes 0, rim-vs-core 0.25, rim-vs-outside 0.92, heterogeneity 0.16; core [0.936, 0.571, 1.0, 0.408] rim [0.703, 0.512, 0.943, 0.437]
  - track 498 at frame 559: holes 0, rim-vs-core 0.27, rim-vs-outside 0.87, heterogeneity 0.18; core [0.923, 0.516, 1.0, 0.339] rim [0.674, 0.47, 0.899, 0.361]
  - track 596 at frame 641: holes 0, rim-vs-core 0.22, rim-vs-outside 0.82, heterogeneity 0.17; core [0.919, 0.54, 1.0, 0.306] rim [0.72, 0.496, 0.926, 0.341]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 224 components >= 12 px at frames [118, 235, 353, 465, 582, 700]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 2.96 (aggregate of 224 individuals; 0/224 membrane-like individually; rim level 0.711)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 1.9 (aggregate of 224 individuals; 5/224 membrane-like individually; rim level 0.53)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 28.5 (aggregate of 224 individuals; 3/224 membrane-like individually; rim level 0.818)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.889 (aggregate of 224 individuals; 12/224 membrane-like individually; rim level 0.408)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #167 (t=259, R_eq 7.33): none; #495 (t=553, R_eq 3.74): none; #498 (t=559, R_eq 3.34): none; #596 (t=641, R_eq 3.29): none
- damage `half` (requested 0.50 of the area) at frame 500 (t=500): target = main-run track #494; the individual is one component of 22 px = 0.61x the median individual, aspect 1.26 (rule mature-compact: track age 97 frames vs K=50; 39 individuals from 39 components at that frame; open-ring individuals, not eligible: 0); mask 19 px (11 inside the individual)
- damage MEASURED: the target lost 49.5% of its matter (inside the individual: its components and what they enclose; 11 of 22 px lost > half their matter); net matter lost outside it = 3.96% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 8 of the 19 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [0.5, None, None, None, None, None] (matter [0.505, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=502); comparator [1.0, 0.929, 1.107, 1.25, 1.179, 0.929] (matter [1.0, 0.95, 1.122, 1.26, 1.167, 0.927]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 224 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
