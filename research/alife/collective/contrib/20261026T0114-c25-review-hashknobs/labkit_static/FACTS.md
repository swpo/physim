# Evidence pack: hash-chemistry-v2 (seed 5)

- world: `../../20261026T0049-c30-hash-o-knobs/world.py`, family `hash-chemistry`
- parent: None; mutation: reproduction of Sayama 2019 Hash Chemistry (positive control for O)
- run: 61 frames x 20 steps x dt 1.0 = time 1200; grid [128, 128]; wall 13s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0049-c30-hash-o-knobs/world.py --out collective/contrib/20261026T0114-c25-review-hashknobs/labkit_static --seeds 5 --frames 60 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 7.0], min area 6 px

## Measurements
- components: final 3, mean 1.8, max 6; occupancy final 0.00
- tracks: 103; persistent (alive >= 50% of run): 0; longest 2 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 10, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 400, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 103
- channel total drift (end/start - 1): [287.5, 2362.0, 57.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 3 components >= 12 px at frames [20, 30]):
  - radial density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 2.57 (aggregate of 3 individuals; 1/3 membrane-like individually; rim level 0.467)
  - radial top_type: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 2.57 (aggregate of 3 individuals; 1/3 membrane-like individually; rim level 0.467)
  - radial other_types: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.97, rim/outside 3.53 (aggregate of 3 individuals; 2/3 membrane-like individually; rim level 0.25)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): other_types
- membrane-like channels per top track at mid-life: #4 (t=160, R_eq 1.38): none; #7 (t=180, R_eq 1.49): ['density', 'top_type']; #47 (t=600, R_eq 1.49): none; #50 (t=600, R_eq 2.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
