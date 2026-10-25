# Evidence pack: neural-field-dep (seed 12)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py`, family `neural-field`
- parent: None; mutation: (c24 copy with a damage hook) c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 701 frames x 10 steps x dt 0.1 = time 700; grid [128, 128]; wall 4s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2008-c24-comet-cut-regrowth/world.py --out /tmp/claude-0/c28rev/core30 --seeds 11 12 13 14 --spf 10 --frames 700 --lineage-k 50 --damage 500:0.3:core --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 37, mean 42.8, max 75; occupancy final 0.09
- tracks: 766; persistent (alive >= 50% of run): 0; longest 311 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 37, 37], H1 [0, 0, 0]
- motion: 224 long-lived tracks moved >= 1 body length; max speed 0.589/time; max body lengths 26.4
- replication (lineage window K = 50 frames = time 50, --lineage-k): splits 307, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 8, merges 87, merge/split ratio 0.283, nucleations 1
- channel total drift (end/start - 1): [-1.0, None, -0.6383, -0.1868]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 538 at frame 547: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.18; core [0.918, 0.518, 1.0, 0.399] rim [0.694, 0.436, 0.929, 0.441]
  - track 579 at frame 559: holes 0, rim-vs-core 0.26, rim-vs-outside 0.89, heterogeneity 0.15; core [0.91, 0.65, 1.0, 0.333] rim [0.693, 0.538, 0.939, 0.406]
  - track 489 at frame 459: holes 0, rim-vs-core 0.33, rim-vs-outside 0.88, heterogeneity 0.17; core [0.908, 0.715, 1.0, 0.186] rim [0.749, 0.488, 0.925, 0.342]
  - track 729 at frame 671: holes 0, rim-vs-core 0.28, rim-vs-outside 0.82, heterogeneity 0.18; core [0.882, 0.499, 1.0, 0.265] rim [0.664, 0.398, 0.878, 0.347]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 236 components >= 12 px at frames [118, 235, 353, 465, 582, 700]; 3 components of the damaged lineage after the cut left out):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 3.03 (aggregate of 236 individuals; 0/236 membrane-like individually; rim level 0.717)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 1.93 (aggregate of 236 individuals; 9/236 membrane-like individually; rim level 0.546)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 31.9 (aggregate of 236 individuals; 2/236 membrane-like individually; rim level 0.842)
  - radial synaptic resource r: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.886 (aggregate of 236 individuals; 10/236 membrane-like individually; rim level 0.407)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #538 (t=547, R_eq 2.59): none; #579 (t=559, R_eq 3.34): none; #489 (t=459, R_eq 3.19): none; #729 (t=671, R_eq 3.24): none
- damage `core` (requested 0.30 of the area) at frame 500 (t=500): target = main-run track #583; the individual is one component of 22 px = 0.67x the median individual, aspect 1.38 (rule mature-compact: track age 67 frames vs K=50; 42 individuals from 42 components at that frame; open-ring individuals, not eligible: 0); mask 7 px (7 inside the individual)
- damage MEASURED: the target lost 33.6% of its matter (inside the individual: its components and what they enclose; 7 of 22 px lost > half their matter); net matter lost outside it = 0% of its matter; share of all matter that disappeared that was under labkit's mask 1
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[500.0, 540.0, 580.0, 620.0, 660.0, 700.0]: target [0.364, None, None, None, None, None] (matter [0.349, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[506.0]; last seen t=505); comparator [1.0, 1.429, None, None, None, None] (matter [1.0, 1.459, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; merged with another individual at t=[543.0]; last seen t=542). Follow-up: pre-cut field at frame 500, then recorded frames 500..700 segmented with the TARGETING range [0.0, 1.0] (threshold 0.5), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 236 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
