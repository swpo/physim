# Evidence pack: apfc (seed 1)

- world: `../../world.py`, family `active-pfc`
- parent: new class (Menzel & Loewen 2013 active phase-field crystal); mutation: none (benchmark model)
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 57s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/f76d4b70-94d3-54e6-8e9a-d0072da2d452/scratchpad/apfc/world.py --out /tmp/claude-0/-home-user-physim/f76d4b70-94d3-54e6-8e9a-d0072da2d452/scratchpad/apfc/pack --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.5906], min area 6 px

## Measurements
- components: final 6, mean 5.2, max 8; occupancy final 0.15
- tracks: 83; persistent (alive >= 50% of run): 1; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.92 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 7, 6], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.299/time; max body lengths 16.1
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 26, merge/split ratio 1, nucleations 5
- channel total drift (end/start - 1): [-0.689, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 57: holes 0, rim-vs-core 0.62, rim-vs-outside 0.16, heterogeneity 0.28; core [0.741, 0.414, 0.665] rim [0.435, 0.049, 0.273]
  - track 4 at frame 49: holes 0, rim-vs-core 0.60, rim-vs-outside 0.16, heterogeneity 0.28; core [0.728, 0.425, 0.665] rim [0.441, 0.045, 0.299]
  - track 13 at frame 74: holes 0, rim-vs-core 0.60, rim-vs-outside 0.16, heterogeneity 0.28; core [0.739, 0.423, 0.663] rim [0.444, 0.05, 0.303]
  - track 42 at frame 163: holes 0, rim-vs-core 0.58, rim-vs-outside 0.18, heterogeneity 0.28; core [0.747, 0.415, 0.647] rim [0.441, 0.05, 0.32]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial crystal amplitude (smoothed (phi - mean)^2): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.726, rim/outside 9.51 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.613)
  - radial density phi: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.479, rim/outside 1.31 (aggregate of 29 individuals; 6/29 membrane-like individually; rim level 0.241)
  - radial |P|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 8.65 (aggregate of 29 individuals; 2/29 membrane-like individually; rim level 0.493)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=285, R_eq 5.61): none; #4 (t=245, R_eq 5.47): none; #13 (t=370, R_eq 5.5): none; #42 (t=815, R_eq 5.61): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 29 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
