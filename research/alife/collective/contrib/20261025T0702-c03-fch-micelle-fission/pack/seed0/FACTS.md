# Evidence pack: fch-micelle-fission (seed 0)

- world: `../../world_mic.py`, family `fch-bilayer`
- parent: None; mutation: new class: functionalized Cahn-Hilliard (Promislow/Gavish) with an asymmetric double well, O(1) functionalization
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/world_mic.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/mic_pack --seeds 0 1 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1151, 2.9849], min area 6 px

## Measurements
- components: final 52, mean 39.3, max 52; occupancy final 0.26
- tracks: 82; persistent (alive >= 50% of run): 33; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 52, 52], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 80, default): splits 27, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 23
- channel total drift (end/start - 1): [0.6628]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 50: holes 0, rim-vs-core 0.17, rim-vs-outside 0.33, heterogeneity 0.29; core [0.556] rim [0.388]
  - track 5 at frame 51: holes 0, rim-vs-core 0.37, rim-vs-outside 0.21, heterogeneity 0.29; core [0.639] rim [0.265]
  - track 7 at frame 51: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.29; core [0.615] rim [0.163]
  - track 60 at frame 87: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.29; core [0.609] rim [0.157]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 255 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (shifted, u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.51, rim/outside 11 (aggregate of 255 individuals; 0/255 membrane-like individually; rim level 0.484)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=200, R_eq 5.01): none; #5 (t=204, R_eq 5.05): none; #7 (t=204, R_eq 5.01): none; #60 (t=348, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
