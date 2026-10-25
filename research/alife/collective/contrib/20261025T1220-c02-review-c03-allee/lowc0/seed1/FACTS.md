# Evidence pack: fch-allee-micelles (seed 1)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1050-c03-allee-no-turnover/world_lowc0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 1703s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1050-c03-allee-no-turnover/world_lowc0.py --out collective/contrib/20261025T1220-c02-review-c03-allee/lowc0/seed1 --seeds 1 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.23 of robust range [0.0, 2.1787], min area 6 px

## Measurements
- components: final 0, mean 3.1, max 24; occupancy final 0.00
- tracks: 31; persistent (alive >= 50% of run): 0; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 320, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [-1.0, -1.0, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 15: holes 0, rim-vs-core 0.34, rim-vs-outside 0.48, heterogeneity 0.10; core [1.0, 0.159, 0.82, 0.562] rim [0.717, 0.122, 1.0, 0.562]
  - track 8 at frame 15: holes 0, rim-vs-core 0.35, rim-vs-outside 0.48, heterogeneity 0.11; core [1.0, 0.146, 0.774, 0.562] rim [0.737, 0.119, 1.0, 0.562]
  - track 1 at frame 11: holes 0, rim-vs-core 0.40, rim-vs-outside 0.47, heterogeneity 0.13; core [1.0, 0.305, 0.731, 0.182] rim [0.717, 0.224, 1.0, 0.226]
  - track 6 at frame 11: holes 0, rim-vs-core 0.45, rim-vs-outside 0.49, heterogeneity 0.13; core [1.0, 0.27, 0.655, 0.25] rim [0.722, 0.217, 1.0, 0.286]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2 components >= 12 px at frames [25]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 17 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 1)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 1.15 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.0266)
  - radial shell q: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.75, rim/outside 2.29 (aggregate of 2 individuals; 2/2 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.947 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.875)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #3 (t=240, R_eq 3.19): ['shell q']; #8 (t=240, R_eq 3.14): ['shell q']; #1 (t=176, R_eq 3.52): ['shell q']; #6 (t=176, R_eq 3.52): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
