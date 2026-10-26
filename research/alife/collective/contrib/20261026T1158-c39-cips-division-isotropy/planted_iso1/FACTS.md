# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world_iso.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 81 frames x 1000 steps x dt 0.1 = time 8000; grid [192, 192]; wall 626s; status ok
- command: `python -m labkit.run collective/contrib/c39-cips-iso-wip/world_iso.py --out collective/contrib/c39-cips-iso-wip/planted_iso1 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0186, 0.9814], min area 6 px

## Measurements
- components: final 16, mean 11.6, max 16; occupancy final 0.08
- tracks: 24; persistent (alive >= 50% of run): 13; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00321/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.0185, -0.599, 0.6426]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 41: holes 0, rim-vs-core 0.34, rim-vs-outside 0.68, heterogeneity 0.12; core [0.987, 0.942, 0.046] rim [0.811, 0.711, 0.23]
  - track 8 at frame 53: holes 0, rim-vs-core 0.36, rim-vs-outside 0.70, heterogeneity 0.12; core [0.992, 0.958, 0.066] rim [0.807, 0.714, 0.25]
  - track 10 at frame 56: holes 0, rim-vs-core 0.34, rim-vs-outside 0.69, heterogeneity 0.11; core [0.99, 0.953, 0.05] rim [0.826, 0.722, 0.233]
  - track 11 at frame 56: holes 0, rim-vs-core 0.35, rim-vs-outside 0.69, heterogeneity 0.12; core [0.988, 0.946, 0.047] rim [0.813, 0.713, 0.232]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial e: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 53.2 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.953)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 16.3 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.895)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 36.4, rim/outside 0.659 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.506)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=4100, R_eq 8.43): none; #8 (t=5300, R_eq 7.65): none; #10 (t=5600, R_eq 8.04): none; #11 (t=5600, R_eq 8.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
