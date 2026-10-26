# Evidence pack: hash-chemistry (seed 0)

- world: `../../world.py`, family `hash-chemistry`
- parent: None; mutation: reproduction of Sayama 2019 Hash Chemistry (positive control for O)
- run: 101 frames x 20 steps x dt 1.0 = time 2000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run collective/contrib/WIP-c30-hash/world.py --out collective/contrib/WIP-c30-hash/pack --seeds 0 1 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 6.0], min area 6 px

## Measurements
- components: final 5, mean 1.8, max 7; occupancy final 0.00
- tracks: 170; persistent (alive >= 50% of run): 0; longest 5 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 3, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 400, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 170
- channel total drift (end/start - 1): [333.0, 1988.0, 149.1111]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 3 components >= 12 px at frames [67, 100]):
  - radial density: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.49, rim/outside 6.87 (aggregate of 3 individuals; 2/3 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial top_type: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.37, rim/outside 8.4 (aggregate of 3 individuals; 2/3 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial other_types: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.88, rim/outside 9.76 (aggregate of 3 individuals; 2/3 membrane-like individually; rim level 1)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): density, top_type, other_types
- membrane-like channels per top track at mid-life: #88 (t=1320, R_eq 1.38): none; #31 (t=680, R_eq 1.87): none; #46 (t=880, R_eq 1.38): ['other_types']; #50 (t=920, R_eq 1.38): ['other_types']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 3 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 2 of 3 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
