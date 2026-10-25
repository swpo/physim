# Evidence pack: fch-allee-micelles (seed 1)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1050-c03-allee-no-turnover/world_wb1.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 1733s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1050-c03-allee-no-turnover/world_wb1.py --out collective/contrib/20261025T1220-c02-review-c03-allee/wb1/seed1 --seeds 1 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1226, 2.9625], min area 6 px

## Measurements
- components: final 39, mean 38.3, max 39; occupancy final 0.19
- tracks: 62; persistent (alive >= 50% of run): 39; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.28 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 320, default): splits 21, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.048, nucleations 18
- channel total drift (end/start - 1): [0.2767, -0.6251, None, -0.7534]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 76: holes 0, rim-vs-core 0.57, rim-vs-outside 0.31, heterogeneity 0.24; core [0.604, 0.347, 0.389, 0.04] rim [0.158, 0.0, 0.487, 0.082]
  - track 6 at frame 76: holes 0, rim-vs-core 0.64, rim-vs-outside 0.31, heterogeneity 0.26; core [0.614, 0.444, 0.384, 0.042] rim [0.162, 0.0, 0.492, 0.096]
  - track 8 at frame 76: holes 0, rim-vs-core 0.67, rim-vs-outside 0.28, heterogeneity 0.27; core [0.602, 0.49, 0.388, 0.047] rim [0.153, 0.0, 0.451, 0.107]
  - track 59 at frame 79: holes 0, rim-vs-core 0.63, rim-vs-outside 0.29, heterogeneity 0.25; core [0.61, 0.421, 0.382, 0.045] rim [0.157, 0.0, 0.46, 0.094]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 234 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.495, rim/outside 22.4 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.468)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.114, rim/outside 8.73 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.087)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 14.2, rim/outside 6.39 (aggregate of 234 individuals; 234/234 membrane-like individually; rim level 0.853)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 10.2, rim/outside 0.855 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.139)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #1 (t=1216, R_eq 4.98): ['shell q']; #6 (t=1216, R_eq 4.95): ['shell q']; #8 (t=1216, R_eq 5.01): ['shell q']; #59 (t=1264, R_eq 4.98): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
