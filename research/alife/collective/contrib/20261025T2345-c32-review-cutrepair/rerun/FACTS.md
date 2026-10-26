# Evidence pack: ringswim-dl2 (seed 7)

- world: `../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 261 frames x 50 steps x dt 1.0 = time 13000; grid [256, 256]; wall 244s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2345-c32-review-cutrepair/world.py --out collective/contrib/20261025T2345-c32-review-cutrepair/rerun --seeds 7 --frames 260 --damage 200:0.4:half --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5408], min area 6 px

## Measurements
- components: final 30, mean 37.5, max 118; occupancy final 0.20
- tracks: 1276; persistent (alive >= 50% of run): 0; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 26.38, final 25; holes at thresholds 0.2/0.35/0.5 final [8, 27, 32]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 31, 30], H1 [35, 33, 25]
- motion: 95 long-lived tracks moved >= 1 body length; max speed 0.0589/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 1000, default): splits 409, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 322, merge/split ratio 0.787, nucleations 0
- channel total drift (end/start - 1): [-0.3305, -0.8077, -0.2989, -0.428]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 543 at frame 118: holes 1, rim-vs-core 0.21, rim-vs-outside 0.70, heterogeneity 0.18; core [0.104, 0.597, 0.509, 0.801] rim [0.157, 0.507, 0.468, 0.627]
  - track 287 at frame 55: holes 1, rim-vs-core 0.19, rim-vs-outside 0.81, heterogeneity 0.20; core [0.115, 0.722, 0.593, 0.642] rim [0.196, 0.56, 0.54, 0.608]
  - track 952 at frame 214: holes 0, rim-vs-core 0.80, rim-vs-outside 0.55, heterogeneity 0.23; core [0.213, 0.843, 0.801, 0.736] rim [0.424, 0.209, 0.401, 0.548]
  - track 843 at frame 188: holes 0, rim-vs-core 0.29, rim-vs-outside 0.85, heterogeneity 0.16; core [0.059, 0.57, 0.35, 0.631] rim [0.223, 0.449, 0.539, 0.722]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 201 components >= 12 px at frames [44, 87, 131, 175, 216, 260]; 7 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 11.7, rim/outside 0.762 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.518)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 9.32 (aggregate of 201 individuals; 18/201 membrane-like individually; rim level 0.648)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 6.58 (aggregate of 201 individuals; 150/201 membrane-like individually; rim level 0.551)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.39, rim/outside 7.44 (aggregate of 201 individuals; 161/201 membrane-like individually; rim level 0.583)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #543 (t=5900, R_eq 11.93, ring): ['K catalyst', 'L link', 'membrane (wall)']; #287 (t=2750, R_eq 10.88, ring): ['L link', 'membrane (wall)']; #952 (t=10700, R_eq 5.78): ['L link', 'membrane (wall)']; #843 (t=9400, R_eq 10.54): ['L link', 'membrane (wall)']
- damage `half` (requested 0.40 of the area) at frame 200 (t=10000): target = main-run track #939; the individual is 1 component(s): outer component 348 px + 97 px it encloses (97 px of low-matter holes) = 445 px = 0.97x the median individual, aspect 1.15 (rule mature-compact: track age 20 frames vs K=20; 34 individuals from 34 components at that frame; open-ring individuals, not eligible: 1); mask 282 px (178 inside the individual)
- damage MEASURED: the target lost 41.8% of its matter (inside the individual: its components and what they enclose; 178 of 445 px lost > half their matter); net matter lost outside it = 2.53% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 104 of the 282 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[10000.0, 10600.0, 11200.0, 11800.0, 12400.0, 13000.0]: target [0.434, 1.191, 1.299, 0.447, None, None] (matter [0.502, 1.152, 1.385, 0.531, None, None]; pieces [1, 1, 1, 1, 0, 0]; merged with another individual at t=[12050.0]; last seen t=12000); comparator [1.0, None, None, None, None, None] (matter [1.0, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[10300.0]; last seen t=10250). Follow-up: pre-cut field at frame 200, then recorded frames 200..260 segmented with the TARGETING range [0.0, 1.540414] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 125 of 201 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
