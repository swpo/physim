# Evidence pack: phase-trait (seed 5)

- world: `../../../../../../threads/autopoiesis/worlds/phase_trait/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: continuous heritable catalyst trait c (growth rate) with link-output trade-off b(c) and +-delta point mutations
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 61s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_trait/world.py --out collective/contrib/20261025T2314-c23-review-phasetrait/rerun/seed5 --seeds 5 --frames 160 --spf 300 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5365], min area 6 px

## Measurements
- components: final 39, mean 33.9, max 42; occupancy final 0.40
- tracks: 89; persistent (alive >= 50% of run): 37; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.78 (1 = constant size)
- enclosures: components with a hole mean 6.57, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 11, 32]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [40, 39, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000341/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 6000, default): splits 42, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.53, 13.5198, 34.3032, 10.8397, 9.0729]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 87: holes 0, rim-vs-core 0.72, rim-vs-outside 1.17, heterogeneity 0.16; core [0.124, 0.938, 1.0, 0.959, 0.809] rim [0.297, 0.394, 1.0, 0.661, 0.495]
  - track 32 at frame 90: holes 0, rim-vs-core 0.43, rim-vs-outside 1.31, heterogeneity 0.17; core [0.069, 0.829, 0.746, 0.872, 0.498] rim [0.236, 0.532, 0.71, 0.81, 0.757]
  - track 34 at frame 90: holes 0, rim-vs-core 0.37, rim-vs-outside 1.15, heterogeneity 0.16; core [0.105, 0.64, 0.584, 0.826, 0.488] rim [0.255, 0.417, 0.537, 0.758, 0.722]
  - track 59 at frame 99: holes 0, rim-vs-core 0.50, rim-vs-outside 1.19, heterogeneity 0.19; core [0.088, 0.763, 0.676, 0.88, 0.485] rim [0.286, 0.425, 0.589, 0.763, 0.754]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 225 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 11.4, rim/outside 0.983 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.461)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 10 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.715)
  - radial trait c (0..0.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 7.32 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.694)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 7.38 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.875)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.99, rim/outside 6.87 (aggregate of 225 individuals; 209/225 membrane-like individually; rim level 0.866)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #17 (t=26100, R_eq 5.44): ['membrane (wall)']; #32 (t=27000, R_eq 6.77): ['membrane (wall)']; #34 (t=27000, R_eq 9.66): none; #59 (t=29700, R_eq 7.42): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 57 of 225 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
