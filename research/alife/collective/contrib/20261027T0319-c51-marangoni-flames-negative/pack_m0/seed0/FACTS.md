# Evidence pack: marangoni-flames (seed 0)

- world: `../../../world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 18s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/mg/world.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/mg/packs/m0 --seeds 0 1 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7534], min area 6 px

## Measurements
- components: final 11, mean 6.2, max 49; occupancy final 0.01
- tracks: 121; persistent (alive >= 50% of run): 0; longest 300 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0408/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 20, default): splits 34, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.176, nucleations 6
- channel total drift (end/start - 1): [-0.9541, -0.1165, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 109 at frame 454: holes 0, rim-vs-core 0.23, rim-vs-outside 0.62, heterogeneity 0.06; core [0.942, 0.058, 0.0, 1.0] rim [0.746, 0.132, 0.0, 0.917]
  - track 104 at frame 176: holes 0, rim-vs-core 0.12, rim-vs-outside 0.55, heterogeneity 0.04; core [0.823, 0.036, 0.0, 0.889] rim [0.757, 0.118, 0.0, 0.94]
  - track 102 at frame 156: holes 0, rim-vs-core 0.12, rim-vs-outside 0.58, heterogeneity 0.05; core [0.81, 0.034, 0.0, 0.868] rim [0.758, 0.114, 0.0, 0.934]
  - track 111 at frame 519: holes 0, rim-vs-core 0.22, rim-vs-outside 0.67, heterogeneity 0.05; core [0.987, 0.065, 0.0, 1.0] rim [0.783, 0.131, 0.0, 0.957]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 39 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 17.5 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.863)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 5.73, rim/outside 0.645 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.25)
  - radial |u|: flat profile (no radial structure; level 0; aggregate of 39 individuals)
  - radial burn r: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 44.9 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.961)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #109 (t=454, R_eq 2.59): none; #104 (t=176, R_eq 3.04): none; #102 (t=156, R_eq 3.14): none; #111 (t=519, R_eq 2.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
