# Evidence pack: phoretic-colloids (seed 5)

- world: `../../../20261026T0529-c33-phoretic-swimdivide-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 190s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0529-c33-phoretic-swimdivide-claim/world.py --out collective/contrib/c39-rev-phor-wip/rerun/seed5 --seeds 5 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5546], min area 6 px

## Measurements
- components: final 13, mean 17.1, max 32; occupancy final 0.05
- tracks: 635; persistent (alive >= 50% of run): 0; longest 741 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 16, 11], H1 [0, 0, 0]
- motion: 112 long-lived tracks moved >= 1 body length; max speed 0.541/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 10, default): splits 78, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 7, merges 98, merge/split ratio 1.26, nucleations 380
- channel total drift (end/start - 1): [0.43, 0.01, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 166 at frame 645: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.21; core [0.89, 0.165, 0.758] rim [0.529, 0.185, 0.575]
  - track 339 at frame 1183: holes 0, rim-vs-core 0.22, rim-vs-outside 0.27, heterogeneity 0.12; core [0.77, 0.285, 0.378] rim [0.568, 0.209, 0.336]
  - track 15 at frame 323: holes 0, rim-vs-core 0.28, rim-vs-outside 0.39, heterogeneity 0.13; core [0.891, 0.093, 0.575] rim [0.633, 0.071, 0.467]
  - track 630 at frame 1587: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.26; core [0.782, 0.343, 0.861] rim [0.483, 0.262, 0.649]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 91 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 15.5 (aggregate of 91 individuals; 5/91 membrane-like individually; rim level 0.597)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 13.8 (aggregate of 91 individuals; 28/91 membrane-like individually; rim level 0.339)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 2.73 (aggregate of 91 individuals; 0/91 membrane-like individually; rim level 0.562)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #166 (t=322.5, R_eq 4.75): ['B density']; #339 (t=591.5, R_eq 2.33): none; #15 (t=161.5, R_eq 3.74): ['B density']; #630 (t=793.5, R_eq 5.67): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
