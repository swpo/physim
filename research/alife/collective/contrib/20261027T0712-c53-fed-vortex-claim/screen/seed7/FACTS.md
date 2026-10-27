# Evidence pack: fed-vortices (seed 7)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 46s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/screen --seeds 3 4 5 6 7 8 9 10 --frames 150 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2087], min area 6 px

## Measurements
- components: final 36, mean 38.3, max 44; occupancy final 0.14
- tracks: 97; persistent (alive >= 50% of run): 32; longest 151 frames; alive start-to-end: 15
- size of persistent tracks: max/min area ratio 5.61 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 36], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.266/time; max body lengths 12.2
- replication (lineage window K = 20 frames = time 60, default): splits 23, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.391, nucleations 0
- channel total drift (end/start - 1): [-0.5317, 0.1234, -78.9855, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.45, rim-vs-outside 0.45, heterogeneity 0.17; core [0.749, 0.126, 0.895, 0.572] rim [0.499, 0.243, 0.762, 0.242]
  - track 3 at frame 76: holes 0, rim-vs-core 0.74, rim-vs-outside 0.34, heterogeneity 0.19; core [0.834, 0.138, 0.061, 0.765] rim [0.447, 0.297, 0.257, 0.18]
  - track 5 at frame 76: holes 0, rim-vs-core 0.78, rim-vs-outside 0.32, heterogeneity 0.21; core [0.822, 0.158, 0.927, 0.754] rim [0.41, 0.327, 0.715, 0.15]
  - track 82 at frame 111: holes 0, rim-vs-core 0.71, rim-vs-outside 0.29, heterogeneity 0.19; core [0.797, 0.108, 0.074, 0.643] rim [0.404, 0.315, 0.28, 0.134]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 230 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.723, rim/outside 16.6 (aggregate of 230 individuals; 0/230 membrane-like individually; rim level 0.665)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 10.7, rim/outside 0.788 (aggregate of 230 individuals; 0/230 membrane-like individually; rim level 0.488)
  - radial vorticity (signed): peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.989 (aggregate of 230 individuals; 0/230 membrane-like individually; rim level 0.488)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.62, rim/outside 29 (aggregate of 230 individuals; 1/230 membrane-like individually; rim level 0.502)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=228, R_eq 4.92): none; #3 (t=228, R_eq 3.48): none; #5 (t=228, R_eq 3.57): none; #82 (t=333, R_eq 4.44): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
