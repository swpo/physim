# Evidence pack: active-gel-fed-comets (seed 0)

- world: `../../world_starve.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 42s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/claim/world_starve.py --out /tmp/claude-0/c09/ag/claim/pack_starve --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0, 8.2627], min area 6 px

## Measurements
- components: final 0, mean 7.9, max 49; occupancy final 0.00
- tracks: 102; persistent (alive >= 50% of run): 2; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.55/time; max body lengths 6.1
- replication (lineage window K = 20 frames = time 20, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 38, merge/split ratio 5.43, nucleations 45
- channel total drift (end/start - 1): [-0.9999, -0.772, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 89 at frame 74: holes 0, rim-vs-core 0.25, rim-vs-outside 0.23, heterogeneity 0.07; core [0.684, 0.655, 0.338] rim [0.438, 0.616, 0.357]
  - track 99 at frame 92: holes 0, rim-vs-core 0.30, rim-vs-outside 0.23, heterogeneity 0.07; core [0.712, 0.567, 0.363] rim [0.418, 0.515, 0.388]
  - track 100 at frame 97: holes 0, rim-vs-core 0.39, rim-vs-outside 0.20, heterogeneity 0.09; core [0.717, 0.646, 0.349] rim [0.33, 0.576, 0.383]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [34, 67, 101]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.666, rim/outside 15.9 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.634)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 1.29 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.738)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.55, rim/outside 0.868 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.337)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #88 (t=74, R_eq 1.6): none; #89 (t=74, R_eq 2.03): none; #99 (t=92, R_eq 2.11): none; #100 (t=97, R_eq 2.59): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
