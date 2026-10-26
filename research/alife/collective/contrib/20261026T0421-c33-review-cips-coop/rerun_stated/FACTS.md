# Evidence pack: cips-turnover (seed 4)

- world: `../../20261026T0301-c35-cips-coop-rods-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 241 frames x 500 steps x dt 0.1 = time 12000; grid [256, 256]; wall 1333s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0301-c35-cips-coop-rods-negative/world.py --out collective/contrib/wip-c33-cips/rerun_stated --seeds 4 --frames 240 --spf 500 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0097, 0.9813], min area 6 px

## Measurements
- components: final 18, mean 11.6, max 18; occupancy final 0.11
- tracks: 18; persistent (alive >= 50% of run): 18; longest 175 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 27.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 18
- channel total drift (end/start - 1): [-0.0005, -0.5696, 0.6137]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 153: holes 0, rim-vs-core 0.30, rim-vs-outside 0.74, heterogeneity 0.12; core [0.982, 0.932, 0.045] rim [0.808, 0.748, 0.2]
  - track 1 at frame 153: holes 0, rim-vs-core 0.25, rim-vs-outside 0.73, heterogeneity 0.10; core [0.955, 0.857, 0.016] rim [0.819, 0.73, 0.185]
  - track 2 at frame 155: holes 0, rim-vs-core 0.30, rim-vs-outside 0.73, heterogeneity 0.11; core [0.98, 0.918, 0.032] rim [0.808, 0.737, 0.199]
  - track 3 at frame 159: holes 0, rim-vs-core 0.30, rim-vs-outside 0.74, heterogeneity 0.12; core [0.981, 0.921, 0.035] rim [0.803, 0.736, 0.199]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [81, 121, 159, 200, 240]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 27 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.8)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 12.9 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.794)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.4, rim/outside 0.662 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.515)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=7650, R_eq 12.19): none; #1 (t=7650, R_eq 13.23): none; #2 (t=7750, R_eq 12.19): none; #3 (t=7950, R_eq 12.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
