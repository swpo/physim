# Evidence pack: fed-vortices-noise (seed 4)

- world: `../../../../scripts/noisy_world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 78s; status ok
- command: `nsweep behav fv level 0.03`
- segmentation: matter > 0.28 of robust range [0.0002, 0.2157], min area 6 px

## Measurements
- components: final 32, mean 34.0, max 40; occupancy final 0.14
- tracks: 140; persistent (alive >= 50% of run): 28; longest 151 frames; alive start-to-end: 7
- size of persistent tracks: max/min area ratio 18.62 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 32, 31], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.24/time; max body lengths 12.0
- replication (lineage window K = 20 frames = time 60, default): splits 40, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 22, merge/split ratio 0.55, nucleations 1
- channel total drift (end/start - 1): [-0.4529, 0.1645, -48.6292, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 76: holes 0, rim-vs-core 0.59, rim-vs-outside 0.25, heterogeneity 0.16; core [0.726, 0.147, 0.877, 0.536] rim [0.389, 0.324, 0.694, 0.12]
  - track 14 at frame 76: holes 0, rim-vs-core 0.83, rim-vs-outside 0.34, heterogeneity 0.22; core [0.856, 0.132, 0.041, 0.795] rim [0.416, 0.335, 0.252, 0.16]
  - track 20 at frame 76: holes 0, rim-vs-core 0.57, rim-vs-outside 0.27, heterogeneity 0.16; core [0.709, 0.158, 0.868, 0.517] rim [0.386, 0.359, 0.692, 0.129]
  - track 118 at frame 120: holes 0, rim-vs-core 0.66, rim-vs-outside 0.31, heterogeneity 0.18; core [0.789, 0.109, 0.91, 0.615] rim [0.412, 0.303, 0.707, 0.145]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 204 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.729, rim/outside 9.44 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.643)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.69, rim/outside 0.793 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.484)
  - radial vorticity (signed): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 1.06 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.515)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.633, rim/outside 24.4 (aggregate of 204 individuals; 2/204 membrane-like individually; rim level 0.467)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=228, R_eq 4.65): none; #14 (t=228, R_eq 3.83): none; #20 (t=228, R_eq 5.38): none; #118 (t=360, R_eq 4.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
