# Evidence pack: phase-trait (seed 6)

- world: `../../../../../../threads/autopoiesis/worlds/phase_trait/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: continuous heritable catalyst trait c (growth rate) with link-output trade-off b(c) and +-delta point mutations
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 59s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_trait/world.py --out collective/contrib/20261025T2314-c23-review-phasetrait/rerun/seed6 --seeds 6 --frames 160 --spf 300 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.502], min area 6 px

## Measurements
- components: final 40, mean 30.4, max 40; occupancy final 0.40
- tracks: 85; persistent (alive >= 50% of run): 28; longest 143 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.06 (1 = constant size)
- enclosures: components with a hole mean 6.28, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 4, 34]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [42, 40, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 6000, default): splits 39, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.026, nucleations 0
- channel total drift (end/start - 1): [-0.5319, 13.6389, 34.5621, 10.8508, 9.203]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 90: holes 1, rim-vs-core 0.30, rim-vs-outside 1.06, heterogeneity 0.17; core [0.145, 0.686, 0.626, 0.912, 0.615] rim [0.249, 0.45, 0.594, 0.766, 0.608]
  - track 28 at frame 93: holes 1, rim-vs-core 0.30, rim-vs-outside 1.05, heterogeneity 0.17; core [0.143, 0.691, 0.64, 0.9, 0.636] rim [0.243, 0.459, 0.603, 0.756, 0.591]
  - track 34 at frame 94: holes 0, rim-vs-core 0.51, rim-vs-outside 1.39, heterogeneity 0.17; core [0.068, 0.959, 0.925, 0.883, 0.628] rim [0.26, 0.508, 0.911, 0.754, 0.691]
  - track 57 at frame 108: holes 0, rim-vs-core 0.30, rim-vs-outside 1.38, heterogeneity 0.18; core [0.08, 0.891, 0.863, 0.871, 0.627] rim [0.193, 0.625, 0.831, 0.78, 0.635]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 201 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 10, rim/outside 1 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.458)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 7.54 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.718)
  - radial trait c (0..0.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 5.67 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.721)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 5.69 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.843)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.85, rim/outside 5.36 (aggregate of 201 individuals; 176/201 membrane-like individually; rim level 0.829)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #20 (t=27000, R_eq 7.33, ring): ['membrane (wall)']; #28 (t=27900, R_eq 7.53, ring): ['membrane (wall)']; #34 (t=28200, R_eq 6.56): ['membrane (wall)']; #57 (t=32400, R_eq 7.05): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 201 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
