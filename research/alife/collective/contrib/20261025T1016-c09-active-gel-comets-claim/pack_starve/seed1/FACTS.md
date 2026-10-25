# Evidence pack: active-gel-fed-comets (seed 1)

- world: `../../world_starve.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 42s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/claim/world_starve.py --out /tmp/claude-0/c09/ag/claim/pack_starve --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0, 8.3475], min area 6 px

## Measurements
- components: final 0, mean 8.6, max 58; occupancy final 0.00
- tracks: 113; persistent (alive >= 50% of run): 2; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.716/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 20, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 43, merge/split ratio 6.14, nucleations 55
- channel total drift (end/start - 1): [-0.9999, -0.7718, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 107 at frame 77: holes 0, rim-vs-core 0.20, rim-vs-outside 0.17, heterogeneity 0.05; core [0.559, 0.516, 0.387] rim [0.358, 0.49, 0.403]
  - track 109 at frame 82: holes 0, rim-vs-core 0.24, rim-vs-outside 0.21, heterogeneity 0.06; core [0.638, 0.596, 0.361] rim [0.398, 0.573, 0.379]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [34, 67, 101]):
  - radial generator a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.677, rim/outside 14.7 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.644)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 1.31 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.748)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.55, rim/outside 0.868 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.34)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #99 (t=72, R_eq 1.78): none; #102 (t=74, R_eq 1.78): none; #107 (t=77, R_eq 1.95): none; #109 (t=82, R_eq 2.11): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
