# Evidence pack: apfc (seed 6)

- world: `../../world.py`, family `active-pfc`
- parent: new class (Menzel & Loewen 2013 active phase-field crystal); mutation: none (benchmark model)
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1225-c13-review-apfc-births/world.py --out collective/contrib/20261025T1225-c13-review-apfc-births/rerun --seeds 5 6 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.6004], min area 6 px

## Measurements
- components: final 9, mean 10.0, max 14; occupancy final 0.19
- tracks: 216; persistent (alive >= 50% of run): 0; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 9], H1 [0, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.303/time; max body lengths 9.5
- replication (lineage window K = 20 frames = time 100, default): splits 70, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 69, merge/split ratio 0.986, nucleations 4
- channel total drift (end/start - 1): [-0.6187, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 61: holes 0, rim-vs-core 0.56, rim-vs-outside 0.17, heterogeneity 0.26; core [0.706, 0.414, 0.661] rim [0.438, 0.063, 0.316]
  - track 163 at frame 163: holes 0, rim-vs-core 0.58, rim-vs-outside 0.16, heterogeneity 0.26; core [0.707, 0.415, 0.667] rim [0.441, 0.062, 0.3]
  - track 94 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.16, heterogeneity 0.26; core [0.689, 0.414, 0.649] rim [0.438, 0.058, 0.338]
  - track 130 at frame 131: holes 0, rim-vs-core 0.56, rim-vs-outside 0.16, heterogeneity 0.26; core [0.711, 0.426, 0.663] rim [0.449, 0.061, 0.322]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial crystal amplitude (smoothed (phi - mean)^2): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.753, rim/outside 6.23 (aggregate of 61 individuals; 1/61 membrane-like individually; rim level 0.623)
  - radial density phi: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.436, rim/outside 1.37 (aggregate of 61 individuals; 15/61 membrane-like individually; rim level 0.249)
  - radial |P|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 7.01 (aggregate of 61 individuals; 4/61 membrane-like individually; rim level 0.53)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #29 (t=305, R_eq 5.32): none; #163 (t=815, R_eq 5.32): none; #94 (t=505, R_eq 5.23): none; #130 (t=655, R_eq 5.26): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 61 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
