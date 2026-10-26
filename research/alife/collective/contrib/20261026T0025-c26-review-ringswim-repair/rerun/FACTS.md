# Evidence pack: ringswim-dl2 (seed 11)

- world: `../../../20261025T2312-c27-ringswim-repair-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 281 frames x 50 steps x dt 1.0 = time 14000; grid [256, 256]; wall 296s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2312-c27-ringswim-repair-claim/world.py --out collective/contrib/_c26work/rev/rerun --seeds 11 --frames 280 --damage 200:0.4:half --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5368], min area 6 px

## Measurements
- components: final 37, mean 33.1, max 103; occupancy final 0.20
- tracks: 1285; persistent (alive >= 50% of run): 0; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 24.53, final 22; holes at thresholds 0.2/0.35/0.5 final [8, 27, 30]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 38, 36], H1 [38, 32, 18]
- motion: 107 long-lived tracks moved >= 1 body length; max speed 0.0627/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 1000, default): splits 419, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 4, merges 317, merge/split ratio 0.757, nucleations 0
- channel total drift (end/start - 1): [-0.3539, -0.8033, -0.2499, -0.3754]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 385 at frame 75: holes 1, rim-vs-core 0.25, rim-vs-outside 0.86, heterogeneity 0.21; core [0.067, 0.708, 0.444, 0.537] rim [0.197, 0.537, 0.53, 0.637]
  - track 498 at frame 104: holes 1, rim-vs-core 0.16, rim-vs-outside 0.79, heterogeneity 0.20; core [0.097, 0.671, 0.517, 0.686] rim [0.189, 0.557, 0.528, 0.621]
  - track 236 at frame 40: holes 1, rim-vs-core 0.32, rim-vs-outside 0.76, heterogeneity 0.21; core [0.118, 0.763, 0.612, 0.615] rim [0.244, 0.482, 0.511, 0.589]
  - track 1161 at frame 266: holes 1, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.23; core [0.092, 0.745, 0.547, 0.584] rim [0.195, 0.595, 0.555, 0.583]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 172 components >= 12 px at frames [47, 94, 141, 186, 233, 280]; 28 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 12.5, rim/outside 0.762 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.527)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 9.36 (aggregate of 172 individuals; 7/172 membrane-like individually; rim level 0.647)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.61, rim/outside 6.57 (aggregate of 172 individuals; 127/172 membrane-like individually; rim level 0.544)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.27, rim/outside 7.27 (aggregate of 172 individuals; 129/172 membrane-like individually; rim level 0.549)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #385 (t=3750, R_eq 11.67): none; #498 (t=5200, R_eq 10.82, ring): ['L link', 'membrane (wall)']; #236 (t=2000, R_eq 9.56, ring): ['L link', 'membrane (wall)']; #1161 (t=13300, R_eq 13.07): none
- damage `half` (requested 0.40 of the area) at frame 200 (t=10000): target = main-run track #841; the individual is 1 component(s): outer component 232 px + 6 px it encloses (6 px of low-matter holes) = 238 px = 0.52x the median individual, aspect 1.06 (rule mature-compact: track age 41 frames vs K=20; 31 individuals from 31 components at that frame; open-ring individuals, not eligible: 1); mask 143 px (95 inside the individual)
- damage MEASURED: the target lost 41.3% of its matter (inside the individual: its components and what they enclose; 95 of 238 px lost > half their matter); net matter lost outside it = 2.42% of its matter; share of all matter that disappeared that was under labkit's mask 1
- (half mode: the mask is the cut side of the individual DILATED by ~R_eq/4, so it also erases a layer just outside the threshold contour: 48 of the 143 mask px are outside the individual; that loss is the 'outside' figure above)
- after damage, area of the individual's largest piece (with what it encloses, so a cut inside an intact membrane leaves it at 1) / its area just before the cut, and matter in all its pieces / matter just before the cut, at t=[10000.0, 10800.0, 11600.0, 12400.0, 13200.0, 14000.0]: target [0.546, 2.958, None, None, None, None] (matter [0.556, 2.452, None, None, None, None]; pieces [1, 1, 0, 0, 0, 0]; merged with another individual at t=[11050.0]; last seen t=11000); comparator [1.0, None, None, None, None, None] (matter [1.0, None, None, None, None, None]; pieces [1, 0, 0, 0, 0, 0]; merged with another individual at t=[10050.0]; last seen t=10000). Follow-up: pre-cut field at frame 200, then recorded frames 200..280 segmented with the TARGETING range [0.0, 1.537671] (threshold 0.35), so the individual followed is the one that was cut; followed through its own splits, re-merges of its own pieces and nucleations within 1 R_eq of its pixels where it was last seen (<= 4 frames earlier); None = not seen (below threshold, or merged with another individual) (damage.png: crops at the last known position)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 115 of 172 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, damage.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
