# Evidence pack: fed-wave-matter (seed 1)

- world: `../../world.py`, family `schrodinger-poisson`
- parent: None; mutation: -
- run: 201 frames x 50 steps x dt 0.2 = time 2000; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/sp/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/sp/packC --seeds 0 1 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 4.5585], min area 6 px

## Measurements
- components: final 6, mean 6.4, max 20; occupancy final 0.03
- tracks: 731; persistent (alive >= 50% of run): 0; longest 17 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 4.9
- replication (lineage window K = 20 frames = time 200, default): splits 176, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 191, merge/split ratio 1.08, nucleations 204
- channel total drift (end/start - 1): [-0.9523, -0.0255, None, 1.0373]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 662 at frame 183: holes 0, rim-vs-core 0.13, rim-vs-outside 0.25, heterogeneity 0.12; core [0.295, 0.564, 0.434, 0.772] rim [0.194, 0.587, 0.431, 0.688]
  - track 378 at frame 84: holes 0, rim-vs-core 0.09, rim-vs-outside 0.17, heterogeneity 0.07; core [0.216, 0.543, 0.586, 0.126] rim [0.169, 0.549, 0.583, 0.206]
  - track 496 at frame 119: holes 0, rim-vs-core 0.17, rim-vs-outside 0.07, heterogeneity 0.12; core [0.327, 0.52, 0.367, 0.528] rim [0.167, 0.557, 0.356, 0.467]
  - track 505 at frame 121: holes 0, rim-vs-core 0.29, rim-vs-outside 0.11, heterogeneity 0.16; core [0.421, 0.516, 0.455, 0.519] rim [0.166, 0.574, 0.427, 0.4]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 33 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial density |psi|^2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.618, rim/outside 4.57 (aggregate of 33 individuals; 2/33 membrane-like individually; rim level 0.235)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.895 (aggregate of 33 individuals; 0/33 membrane-like individually; rim level 0.569)
  - radial potential -V: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 1.18 (aggregate of 33 individuals; 0/33 membrane-like individually; rim level 0.664)
  - radial phase cos: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 1.02 (aggregate of 33 individuals; 0/33 membrane-like individually; rim level 0.485)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #662 (t=1830, R_eq 8.2): none; #378 (t=840, R_eq 2.65): none; #496 (t=1190, R_eq 4.62): none; #505 (t=1210, R_eq 5.86): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 33 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
