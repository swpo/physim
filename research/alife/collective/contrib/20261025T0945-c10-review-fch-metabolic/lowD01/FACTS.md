# Evidence pack: fch-metabolic-micelles (seed 23)

- world: `../world_ctl.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 76 frames x 400 steps x dt 0.02 = time 600; grid [128, 128]; wall 317s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0945-c10-review-fch-metabolic/world_ctl.py --out collective/contrib/20261025T0945-c10-review-fch-metabolic/lowD01 --seeds 23 --frames 75 --spf 400 --no-movie`
- segmentation: matter > 0.18 of robust range [0.0176, 2.7234], min area 6 px

## Measurements
- components: final 0, mean 13.6, max 24; occupancy final 0.00
- tracks: 31; persistent (alive >= 50% of run): 14; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 160, default): splits 4, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 19
- channel total drift (end/start - 1): [-0.9406, -0.993, None, -0.0007]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 30: holes 0, rim-vs-core 0.50, rim-vs-outside 0.55, heterogeneity 0.16; core [0.714, 0.311, 0.537, 0.468] rim [0.29, 0.272, 0.807, 0.488]
  - track 13 at frame 30: holes 0, rim-vs-core 0.54, rim-vs-outside 0.56, heterogeneity 0.16; core [0.749, 0.287, 0.491, 0.488] rim [0.303, 0.249, 0.797, 0.507]
  - track 27 at frame 31: holes 0, rim-vs-core 0.57, rim-vs-outside 0.61, heterogeneity 0.15; core [0.741, 0.245, 0.453, 0.576] rim [0.313, 0.215, 0.834, 0.588]
  - track 5 at frame 24: holes 0, rim-vs-core 0.56, rim-vs-outside 0.55, heterogeneity 0.17; core [0.806, 0.437, 0.359, 0.276] rim [0.401, 0.38, 0.742, 0.304]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [12, 25, 38, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.561, rim/outside 16.6 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.549)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.762, rim/outside 1.69 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.466)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 10.7, rim/outside 7.93 (aggregate of 64 individuals; 64/64 membrane-like individually; rim level 0.949)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.917 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.388)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #11 (t=240, R_eq 3.29): ['shell q']; #13 (t=240, R_eq 3.29): ['shell q']; #27 (t=248, R_eq 3.19): ['shell q']; #5 (t=192, R_eq 3.48): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
