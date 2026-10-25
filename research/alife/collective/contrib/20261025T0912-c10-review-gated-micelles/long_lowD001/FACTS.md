# Evidence pack: fch-gated-micelles (seed 17)

- world: `../world_ctl.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 301 frames x 200 steps x dt 0.02 = time 1200; grid [128, 128]; wall 627s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0912-c10-review-gated-micelles/world_ctl.py --out collective/contrib/20261025T0912-c10-review-gated-micelles/long_lowD001 --seeds 17 --frames 300 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1162, 2.9968], min area 6 px

## Measurements
- components: final 106, mean 66.7, max 108; occupancy final 0.56
- tracks: 239; persistent (alive >= 50% of run): 48; longest 300 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [110, 110, 110], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.0155/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 80, default): splits 98, persistent splits 69 (0 more failed only because the siblings re-merged within K), max generation 5, merges 16, merge/split ratio 0.163, nucleations 22
- channel total drift (end/start - 1): [1.9949, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 151: holes 0, rim-vs-core 0.52, rim-vs-outside 0.25, heterogeneity 0.24; core [0.615, 0.568, 0.214] rim [0.173, 0.334, 0.336]
  - track 9 at frame 151: holes 0, rim-vs-core 0.53, rim-vs-outside 0.27, heterogeneity 0.24; core [0.614, 0.633, 0.239] rim [0.172, 0.362, 0.367]
  - track 15 at frame 151: holes 0, rim-vs-core 0.55, rim-vs-outside 0.22, heterogeneity 0.24; core [0.608, 0.653, 0.246] rim [0.155, 0.339, 0.303]
  - track 90 at frame 212: holes 0, rim-vs-core 0.49, rim-vs-outside 0.28, heterogeneity 0.26; core [0.606, 0.495, 0.304] rim [0.162, 0.331, 0.421]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 443 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.509, rim/outside 3.42 (aggregate of 443 individuals; 3/443 membrane-like individually; rim level 0.476)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.65, rim/outside 1.59 (aggregate of 443 individuals; 0/443 membrane-like individually; rim level 0.518)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.6, rim/outside 3.05 (aggregate of 443 individuals; 438/443 membrane-like individually; rim level 0.715)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #3 (t=604, R_eq 4.98): ['shell q']; #9 (t=604, R_eq 4.95): ['shell q']; #15 (t=604, R_eq 5.2): ['shell q']; #90 (t=848, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
