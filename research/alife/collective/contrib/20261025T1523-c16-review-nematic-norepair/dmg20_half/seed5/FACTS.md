# Evidence pack: active-nematic-droplets (seed 5)

- world: `../../../20261025T1250-c11-active-nematic-no-repair/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 459s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1250-c11-active-nematic-no-repair/world.py --out collective/contrib/20261025T1523-c16-review-nematic-norepair/dmg20_half/seed5 --seeds 5 --damage 150:0.2:half --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8256, 0.6359], min area 6 px

## Measurements
- components: final 32, mean 21.4, max 32; occupancy final 0.07
- tracks: 105; persistent (alive >= 50% of run): 12; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 33, 29], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.0754/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 100, default): splits 43, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 9, merge/split ratio 0.209, nucleations 10
- channel total drift (end/start - 1): [-0.5101, -0.3824, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 118: holes 0, rim-vs-core 0.51, rim-vs-outside 0.34, heterogeneity 0.18; core [0.933, 0.866, 0.448] rim [0.714, 0.564, 0.798]
  - track 40 at frame 136: holes 0, rim-vs-core 0.48, rim-vs-outside 0.37, heterogeneity 0.17; core [0.945, 0.89, 0.399] rim [0.746, 0.609, 0.73]
  - track 41 at frame 136: holes 0, rim-vs-core 0.50, rim-vs-outside 0.39, heterogeneity 0.18; core [0.95, 0.906, 0.416] rim [0.752, 0.638, 0.792]
  - track 89 at frame 187: holes 0, rim-vs-core 0.56, rim-vs-outside 0.40, heterogeneity 0.18; core [0.962, 0.963, 0.396] rim [0.736, 0.658, 0.803]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 148 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 4.77 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.763)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.765, rim/outside 8.29 (aggregate of 148 individuals; 1/148 membrane-like individually; rim level 0.638)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 2.12 (aggregate of 148 individuals; 108/148 membrane-like individually; rim level 0.651)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #18 (t=590, R_eq 3.14): ['surfactant s']; #40 (t=680, R_eq 3.14): ['surfactant s']; #41 (t=680, R_eq 3.34): ['surfactant s']; #89 (t=935, R_eq 3.43): ['surfactant s']
- damage `half` (requested 0.20 of the area) at frame 150 (t=750): target = main-run track #69; the individual is one component of 23 px = 0.61x the median individual, aspect 1.39 (rule mature-compact: track age 22 frames vs K=20; 24 individuals from 24 components at that frame; open-ring individuals, not eligible: 1); mask 12 px (5 inside the individual)
- damage MEASURED: the target lost 81.6% of its matter (inside the individual: its components and what they enclose; 5 of 23 px lost > half their matter); net matter lost outside it = 82.7% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 7 of the 12 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[750.0, 800.0, 850.0, 900.0, 950.0, 1000.0]: target [0.739, None, None, None, None, None] (matter [0.848, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; last seen t=765); comparator [1.0, 0.885, 1.192, 1.231, 1.231, 1.115] (matter [1.0, 0.773, 1.194, 1.204, 1.154, 1.15]; pieces [1, 1, 1, 1, 1, 1]). Follow-up: pre-cut field at frame 150, then recorded frames 150..200 segmented with the TARGETING range [-0.825064, 0.633961] (threshold 0.5655), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 148 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
