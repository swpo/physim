# Evidence pack: chimera-field (seed 5)

- world: `../../20261027T1049-c55-chimera-field-negative/world.py`, family `nonlocal-oscillators`
- parent: None; mutation: -
- run: 121 frames x 50 steps x dt 0.1 = time 600; grid [128, 128]; wall 10s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1049-c55-chimera-field-negative/world.py --out collective/contrib/20261027T1645-c58-review-chimera/a11 --seeds 5 --frames 120 --spf 50 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.9062], min area 6 px

## Measurements
- components: final 0, mean 0.5, max 5; occupancy final 0.00
- tracks: 27; persistent (alive >= 50% of run): 0; longest 6 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 9, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 0.667, nucleations 2
- channel total drift (end/start - 1): [None, 0.9995, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 7: holes 0, rim-vs-core 0.34, rim-vs-outside 0.23, heterogeneity 0.19; core [0.731, 0.423, 0.0, 0.501] rim [0.444, 0.515, 0.0, 0.337]
  - track 26 at frame 24: holes 0, rim-vs-core 0.49, rim-vs-outside 0.31, heterogeneity 0.20; core [0.777, 0.48, 0.0, 0.635] rim [0.454, 0.208, 0.0, 0.384]
  - track 6 at frame 8: holes 0, rim-vs-core 0.25, rim-vs-outside 0.28, heterogeneity 0.18; core [0.619, 0.549, 0.0, 0.489] rim [0.474, 0.4, 0.0, 0.36]
  - track 18 at frame 18: holes 0, rim-vs-core 0.41, rim-vs-outside 0.24, heterogeneity 0.19; core [0.76, 0.552, 0.0, 0.581] rim [0.458, 0.414, 0.0, 0.337]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 5 components >= 12 px at frames [20]):
  - radial incoherence 1-|Z|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 2.19 (aggregate of 5 individuals; 0/5 membrane-like individually; rim level 0.471)
  - radial cos phase: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.23 (aggregate of 5 individuals; 0/5 membrane-like individually; rim level 0.56)
  - radial fuel Y: flat profile (no radial structure; level 0; aggregate of 5 individuals)
  - radial local frequency: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.671, rim/outside 1.99 (aggregate of 5 individuals; 0/5 membrane-like individually; rim level 0.351)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=35, R_eq 14.27): none; #26 (t=120, R_eq 20.37): none; #6 (t=40, R_eq 24.25, ring): none; #18 (t=90, R_eq 15.1): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
