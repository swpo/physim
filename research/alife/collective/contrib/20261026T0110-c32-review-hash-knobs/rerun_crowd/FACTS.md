# Evidence pack: hash-chemistry-v2 (seed 8)

- world: `../world.py`, family `hash-chemistry`
- parent: None; mutation: reproduction of Sayama 2019 Hash Chemistry (positive control for O)
- run: 201 frames x 20 steps x dt 1.0 = time 4000; grid [128, 128]; wall 10s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0110-c32-review-hash-knobs/world.py --out collective/contrib/20261026T0110-c32-review-hash-knobs/rerun_crowd --seeds 8 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 5.0], min area 6 px

## Measurements
- components: final 1, mean 0.5, max 3; occupancy final 0.00
- tracks: 91; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [86, 18, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 400, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 91
- channel total drift (end/start - 1): [-0.2605, 94.2857, -0.5926]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1 components >= 12 px at frames [200]):
  - radial density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 5.72 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 1)
  - radial top_type: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 5.3 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 1)
  - radial other_types: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.505, rim/outside 7.78 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.5)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #90 (t=4000, R_eq 2.11): none; #0 (t=100, R_eq 1.49): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
