# Evidence pack: phoretic-colloids (seed 4)

- world: `../../../20261026T0254-c33-phoretic-janus-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py --out collective/contrib/20261026T0317-c30-review-phoretic-janus/rerun --seeds 4 5 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6597], min area 6 px

## Measurements
- components: final 14, mean 22.4, max 39; occupancy final 0.07
- tracks: 269; persistent (alive >= 50% of run): 12; longest 367 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 17, 11], H1 [0, 0, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.379/time; max body lengths 8.4
- replication (lineage window K = 20 frames = time 10, default): splits 8, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 36, merge/split ratio 4.5, nucleations 217
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 218: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.15; core [0.783, 0.507, 0.522] rim [0.495, 0.404, 0.428]
  - track 41 at frame 218: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.13; core [0.895, 0.197, 0.549] rim [0.615, 0.196, 0.451]
  - track 26 at frame 202: holes 0, rim-vs-core 0.32, rim-vs-outside 0.33, heterogeneity 0.16; core [0.805, 0.417, 0.587] rim [0.507, 0.412, 0.475]
  - track 260 at frame 390: holes 0, rim-vs-core 0.24, rim-vs-outside 0.31, heterogeneity 0.16; core [0.802, 0.298, 0.47] rim [0.581, 0.228, 0.414]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 13.6 (aggregate of 115 individuals; 5/115 membrane-like individually; rim level 0.647)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 13.6 (aggregate of 115 individuals; 24/115 membrane-like individually; rim level 0.422)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 2.51 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.532)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=109, R_eq 3.57): none; #41 (t=109, R_eq 3.61): ['B density']; #26 (t=101, R_eq 4.07): none; #260 (t=195, R_eq 3.19): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
