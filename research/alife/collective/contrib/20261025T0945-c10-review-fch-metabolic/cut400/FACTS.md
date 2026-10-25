# Evidence pack: fch-metabolic-micelles (seed 23)

- world: `../world_ctl.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 622s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0945-c10-review-fch-metabolic/world_ctl.py --out collective/contrib/20261025T0945-c10-review-fch-metabolic/cut400 --seeds 23 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.17 of robust range [0.0106, 2.9069], min area 6 px

## Measurements
- components: final 0, mean 21.8, max 38; occupancy final 0.00
- tracks: 59; persistent (alive >= 50% of run): 14; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 160, default): splits 18, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 19
- channel total drift (end/start - 1): [-0.9641, -0.9969, None, -0.957]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 59: holes 0, rim-vs-core 0.86, rim-vs-outside 0.31, heterogeneity 0.27; core [0.665, 0.728, 0.387, 0.024] rim [0.207, 0.004, 0.477, 0.04]
  - track 11 at frame 59: holes 0, rim-vs-core 0.71, rim-vs-outside 0.38, heterogeneity 0.25; core [0.68, 0.607, 0.389, 0.025] rim [0.222, 0.091, 0.558, 0.038]
  - track 12 at frame 50: holes 0, rim-vs-core 0.76, rim-vs-outside 0.29, heterogeneity 0.26; core [0.696, 0.712, 0.295, 0.202] rim [0.218, 0.129, 0.402, 0.263]
  - track 39 at frame 81: holes 0, rim-vs-core 0.64, rim-vs-outside 0.59, heterogeneity 0.16; core [0.681, 0.163, 0.321, 0.004] rim [0.279, 0.09, 0.815, 0.005]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 114 components >= 12 px at frames [25, 50, 76, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.529, rim/outside 8.96 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.497)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.522, rim/outside 10.5 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.277)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.9, rim/outside 6.31 (aggregate of 114 individuals; 114/114 membrane-like individually; rim level 0.764)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.95 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.249)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=472, R_eq 4.85): ['shell q']; #11 (t=472, R_eq 4.75): ['shell q']; #12 (t=400, R_eq 5.01): ['shell q']; #39 (t=648, R_eq 3.39): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
