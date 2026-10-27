# Evidence pack: fed-vortices (seed 54)

- world: `../../20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 342s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out collective/contrib/20261027T1040-c54-review-fed-vortex/noadv --seeds 54 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2098], min area 6 px

## Measurements
- components: final 52, mean 51.6, max 52; occupancy final 0.16
- tracks: 84; persistent (alive >= 50% of run): 52; longest 1001 frames; alive start-to-end: 17
- size of persistent tracks: max/min area ratio 4.15 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 52, 52], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0043/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 60, default): splits 23, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4537, 0.021, -189.7928, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 504: holes 0, rim-vs-core 0.63, rim-vs-outside 0.49, heterogeneity 0.20; core [0.83, 0.129, 0.067, 0.774] rim [0.503, 0.296, 0.23, 0.294]
  - track 3 at frame 504: holes 0, rim-vs-core 0.42, rim-vs-outside 0.62, heterogeneity 0.20; core [0.791, 0.147, 0.906, 0.713] rim [0.575, 0.255, 0.793, 0.394]
  - track 4 at frame 504: holes 0, rim-vs-core 0.76, rim-vs-outside 0.29, heterogeneity 0.20; core [0.796, 0.138, 0.082, 0.712] rim [0.393, 0.354, 0.287, 0.138]
  - track 80 at frame 529: holes 0, rim-vs-core 0.77, rim-vs-outside 0.30, heterogeneity 0.20; core [0.8, 0.135, 0.08, 0.716] rim [0.393, 0.354, 0.287, 0.137]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 312 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.714, rim/outside 39.5 (aggregate of 312 individuals; 0/312 membrane-like individually; rim level 0.695)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 25, rim/outside 0.787 (aggregate of 312 individuals; 0/312 membrane-like individually; rim level 0.527)
  - radial vorticity (signed): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.99 (aggregate of 312 individuals; 0/312 membrane-like individually; rim level 0.488)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.589, rim/outside 56.4 (aggregate of 312 individuals; 0/312 membrane-like individually; rim level 0.554)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1512, R_eq 3.78): none; #3 (t=1512, R_eq 3.87): none; #4 (t=1512, R_eq 3.95): none; #80 (t=1587, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
