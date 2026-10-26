# Evidence pack: ringswim-dl2 (seed 11)

- world: `../../20261025T2312-c27-ringswim-repair-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 291s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2312-c27-ringswim-repair-claim/world.py --out /home/user/physim/research/alife/collective/contrib/20261026T0035-c25-review-ringrepair/pack --seeds 11 --damage 200:0.4:half --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5377], min area 6 px

## Measurements
- components: final 31, mean 35.0, max 104; occupancy final 0.18
- tracks: 979; persistent (alive >= 50% of run): 0; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 25.08, final 21; holes at thresholds 0.2/0.35/0.5 final [9, 23, 25]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 33, 29], H1 [31, 28, 20]
- motion: 87 long-lived tracks moved >= 1 body length; max speed 0.0627/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 1000, default): splits 309, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 3, merges 230, merge/split ratio 0.744, nucleations 0
- channel total drift (end/start - 1): [-0.3268, -0.8152, -0.3092, -0.4479]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 387 at frame 74: holes 1, rim-vs-core 0.22, rim-vs-outside 0.82, heterogeneity 0.20; core [0.067, 0.702, 0.444, 0.547] rim [0.18, 0.545, 0.517, 0.63]
  - track 500 at frame 104: holes 1, rim-vs-core 0.16, rim-vs-outside 0.79, heterogeneity 0.20; core [0.097, 0.67, 0.517, 0.686] rim [0.19, 0.556, 0.529, 0.621]
  - track 238 at frame 39: holes 1, rim-vs-core 0.33, rim-vs-outside 0.82, heterogeneity 0.20; core [0.106, 0.744, 0.579, 0.593] rim [0.262, 0.453, 0.521, 0.612]
  - track 843 at frame 180: holes 1, rim-vs-core 0.20, rim-vs-outside 0.80, heterogeneity 0.20; core [0.123, 0.746, 0.619, 0.637] rim [0.193, 0.574, 0.543, 0.602]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 199 components >= 12 px at frames [34, 67, 101, 133, 166, 200]; 1 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.95, rim/outside 0.757 (aggregate of 199 individuals; 0/199 membrane-like individually; rim level 0.493)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 7.16 (aggregate of 199 individuals; 24/199 membrane-like individually; rim level 0.614)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 5.22 (aggregate of 199 individuals; 147/199 membrane-like individually; rim level 0.511)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.08, rim/outside 5.74 (aggregate of 199 individuals; 151/199 membrane-like individually; rim level 0.547)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #387 (t=3700, R_eq 11.71, ring): ['membrane (wall)']; #500 (t=5200, R_eq 10.82, ring): ['L link', 'membrane (wall)']; #238 (t=1950, R_eq 9.47, ring): ['L link', 'membrane (wall)']; #843 (t=9000, R_eq 11.42, ring): ['K catalyst', 'L link', 'membrane (wall)']
- damage `half` (requested 0.40 of the area) at frame 200 (t=10000): target = main-run track #843; the individual is 1 component(s): outer component 232 px + 6 px it encloses (6 px of low-matter holes) = 238 px = 0.52x the median individual, aspect 1.06 (rule mature-compact: track age 41 frames vs K=20; 31 individuals from 31 components at that frame; open-ring individuals, not eligible: 1); mask 143 px (95 inside the individual)
- damage MEASURED: the target lost 41.3% of its matter (inside the individual: its components and what they enclose; 95 of 238 px lost > half their matter); net matter lost outside it = 2.42% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 48 of the 143 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[10000.0]: target [0.546] (matter [0.556]; pieces [1]); comparator [1.0] (matter [1.0]; pieces [1]). Follow-up: pre-cut field at frame 200, then recorded frames 200..200 segmented with the TARGETING range [0.0, 1.537671] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 122 of 199 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
