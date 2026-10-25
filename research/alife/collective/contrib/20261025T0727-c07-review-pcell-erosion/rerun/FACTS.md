# Evidence pack: pcell-ytrait (seed 5)

- world: `../world_ytrait.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [128, 128]; wall 93s; status ok
- command: `python -m labkit.run collective/contrib/_c07rev2/world_ytrait.py --out collective/contrib/_c07rev2/rerun --seeds 5 --spf 150 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8381], min area 6 px

## Measurements
- components: final 9, mean 20.3, max 25; occupancy final 0.04
- tracks: 61; persistent (alive >= 50% of run): 24; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 38.83 (1 = constant size)
- enclosures: components with a hole mean 2.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 9], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.000565/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 3000, default): splits 18, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.167, nucleations 0
- channel total drift (end/start - 1): [-0.0782, -0.9482, -0.8429, -0.8877]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 104: holes 0, rim-vs-core 0.68, rim-vs-outside 0.54, heterogeneity 0.20; core [0.239, 0.708, 0.873, 0.825] rim [0.438, 0.216, 0.52, 0.593]
  - track 34 at frame 103: holes 0, rim-vs-core 0.59, rim-vs-outside 0.57, heterogeneity 0.20; core [0.202, 0.669, 0.817, 0.777] rim [0.405, 0.186, 0.56, 0.674]
  - track 49 at frame 109: holes 0, rim-vs-core 0.59, rim-vs-outside 0.57, heterogeneity 0.20; core [0.2, 0.682, 0.817, 0.783] rim [0.419, 0.217, 0.55, 0.656]
  - track 59 at frame 119: holes 0, rim-vs-core 0.62, rim-vs-outside 0.55, heterogeneity 0.21; core [0.198, 0.652, 0.785, 0.742] rim [0.432, 0.17, 0.502, 0.634]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 5.4, rim/outside 0.8 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.603)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.633, rim/outside 51.1 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.533)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 71.9 (aggregate of 119 individuals; 59/119 membrane-like individually; rim level 0.882)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.37, rim/outside 62.4 (aggregate of 119 individuals; 100/119 membrane-like individually; rim level 0.922)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #38 (t=15600, R_eq 4.82): ['membrane (wall)']; #34 (t=15450, R_eq 5.14): ['membrane (wall)']; #49 (t=16350, R_eq 5.08): ['L link', 'membrane (wall)']; #59 (t=17850, R_eq 5.64): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
