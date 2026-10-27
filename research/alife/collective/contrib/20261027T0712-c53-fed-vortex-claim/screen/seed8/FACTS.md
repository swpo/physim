# Evidence pack: fed-vortices (seed 8)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 47s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/screen --seeds 3 4 5 6 7 8 9 10 --frames 150 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2072], min area 6 px

## Measurements
- components: final 32, mean 33.3, max 37; occupancy final 0.14
- tracks: 79; persistent (alive >= 50% of run): 32; longest 151 frames; alive start-to-end: 16
- size of persistent tracks: max/min area ratio 4.94 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 32], H1 [0, 0, 0]
- motion: 37 long-lived tracks moved >= 1 body length; max speed 0.222/time; max body lengths 9.3
- replication (lineage window K = 20 frames = time 60, default): splits 17, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 8, merge/split ratio 0.471, nucleations 0
- channel total drift (end/start - 1): [-0.5526, 0.161, -810.2631, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 76: holes 0, rim-vs-core 0.79, rim-vs-outside 0.30, heterogeneity 0.21; core [0.822, 0.126, 0.058, 0.724] rim [0.391, 0.326, 0.276, 0.127]
  - track 4 at frame 76: holes 0, rim-vs-core 0.79, rim-vs-outside 0.35, heterogeneity 0.20; core [0.853, 0.135, 0.045, 0.798] rim [0.444, 0.319, 0.248, 0.182]
  - track 5 at frame 76: holes 0, rim-vs-core 0.69, rim-vs-outside 0.30, heterogeneity 0.18; core [0.792, 0.159, 0.912, 0.694] rim [0.428, 0.318, 0.718, 0.161]
  - track 73 at frame 130: holes 0, rim-vs-core 0.78, rim-vs-outside 0.28, heterogeneity 0.20; core [0.809, 0.121, 0.06, 0.654] rim [0.371, 0.373, 0.287, 0.111]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 197 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.742, rim/outside 16.2 (aggregate of 197 individuals; 0/197 membrane-like individually; rim level 0.674)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.3, rim/outside 0.78 (aggregate of 197 individuals; 0/197 membrane-like individually; rim level 0.483)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 1 (aggregate of 197 individuals; 0/197 membrane-like individually; rim level 0.487)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.659, rim/outside 28.2 (aggregate of 197 individuals; 3/197 membrane-like individually; rim level 0.508)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=228, R_eq 4.15): none; #4 (t=228, R_eq 3.74): none; #5 (t=228, R_eq 4.07): none; #73 (t=390, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
