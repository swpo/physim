# Evidence pack: fch-allee-micelles (seed 7)

- world: `../../../20261025T1050-c03-allee-no-turnover/world_lowc0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 76 frames x 800 steps x dt 0.02 = time 1200; grid [128, 128]; wall 472s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1050-c03-allee-no-turnover/world_lowc0.py --out collective/contrib/20261025T1240-c09-review-allee/lowc0/seed7 --seeds 7 --frames 75 --spf 800 --no-movie`
- segmentation: matter > 0.20 of robust range [0.0008, 2.5207], min area 6 px

## Measurements
- components: final 0, mean 6.4, max 24; occupancy final 0.00
- tracks: 27; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 320, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 22
- channel total drift (end/start - 1): [-0.9974, -1.0, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 14: holes 0, rim-vs-core 0.64, rim-vs-outside 0.62, heterogeneity 0.15; core [0.914, 0.135, 0.568, 0.53] rim [0.435, 0.1, 0.993, 0.559]
  - track 24 at frame 14: holes 0, rim-vs-core 0.55, rim-vs-outside 0.56, heterogeneity 0.16; core [0.876, 0.146, 0.646, 0.505] rim [0.404, 0.106, 0.927, 0.526]
  - track 26 at frame 14: holes 0, rim-vs-core 0.64, rim-vs-outside 0.61, heterogeneity 0.15; core [0.919, 0.143, 0.577, 0.526] rim [0.434, 0.102, 1.0, 0.526]
  - track 5 at frame 12: holes 0, rim-vs-core 0.62, rim-vs-outside 0.59, heterogeneity 0.16; core [0.915, 0.161, 0.498, 0.409] rim [0.437, 0.132, 0.894, 0.426]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [12, 25]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.725, rim/outside 17.4 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.722)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 1.24 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.139)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 6.65, rim/outside 5.12 (aggregate of 27 individuals; 27/27 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 0.989 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.528)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #6 (t=224, R_eq 3.19): ['shell q']; #24 (t=224, R_eq 3.29): ['shell q']; #26 (t=224, R_eq 3.19): ['shell q']; #5 (t=192, R_eq 3.48): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
