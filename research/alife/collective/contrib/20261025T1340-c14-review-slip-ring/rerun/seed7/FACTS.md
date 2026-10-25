# Evidence pack: pcell-yeff-cap-slip (seed 7)

- world: `../../../../collective/contrib/20261025T1152-c06-pcell-slip-ring-negative/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 1810s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1152-c06-pcell-slip-ring-negative/world.py --out scratch/c14/rev_slip/seed7 --seeds 7 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0006, 1.5127], min area 6 px

## Measurements
- components: final 1, mean 4.2, max 31; occupancy final 0.16
- tracks: 278; persistent (alive >= 50% of run): 1; longest 126 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.08 (1 = constant size)
- enclosures: components with a hole mean 0.91, final 1; holes at thresholds 0.2/0.35/0.5 final [59, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 1, 1], H1 [6, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 10000, default): splits 48, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 42, merge/split ratio 0.875, nucleations 152
- channel total drift (end/start - 1): [-0.8131, -0.2801, 0.7833, -0.5056, -0.0182]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 10: holes 0, rim-vs-core 0.58, rim-vs-outside 1.11, heterogeneity 0.21; core [0.22, 0.807, 0.806, 0.595, 0.851] rim [0.447, 0.304, 0.635, 0.658, 0.805]
  - track 21 at frame 8: holes 0, rim-vs-core 0.60, rim-vs-outside 1.07, heterogeneity 0.22; core [0.222, 0.79, 0.803, 0.581, 0.848] rim [0.438, 0.266, 0.66, 0.701, 0.788]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.65, rim/outside 1.4 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.247)
  - radial K particles: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.1, rim/outside 0.938 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.422)
  - radial L link: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 0.976 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.414)
  - radial membrane (wall): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 2.63 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.253)
  - radial mean yield / 2: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.23, rim/outside 0.945 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.824)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #225 (t=43500, R_eq 29): none; #264 (t=88000, R_eq 28.53, ring): none; #53 (t=5000, R_eq 7.25): ['membrane (wall)']; #21 (t=4000, R_eq 6.96): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 6 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
