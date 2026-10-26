# Evidence pack: hash-chemistry (seed 32)

- world: `../../../20261026T0009-c30-hash-chemistry-o-calibration/world.py`, family `hash-chemistry`
- parent: None; mutation: reproduction of Sayama 2019 Hash Chemistry (positive control for O)
- run: 101 frames x 20 steps x dt 1.0 = time 2000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0009-c30-hash-chemistry-o-calibration/world.py --out collective/contrib/_c26work/rev2/rerun32 --seeds 32 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 6.0], min area 6 px

## Measurements
- components: final 2, mean 2.2, max 6; occupancy final 0.00
- tracks: 208; persistent (alive >= 50% of run): 0; longest 3 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 4, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 400, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 208
- channel total drift (end/start - 1): [303.7, 2096.0, 104.5556]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 3 components >= 12 px at frames [83, 100]):
  - radial density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 2.47 (aggregate of 3 individuals; 2/3 membrane-like individually; rim level 0.458)
  - radial top_type: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 2.76 (aggregate of 3 individuals; 2/3 membrane-like individually; rim level 0.481)
  - radial other_types: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.78, rim/outside 3.71 (aggregate of 3 individuals; 3/3 membrane-like individually; rim level 0.5)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): other_types (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #124 (t=1340, R_eq 1.38): none; #203 (t=2000, R_eq 2.26): ['density', 'top_type', 'other_types']; #0 (t=40, R_eq 2.03): none; #20 (t=360, R_eq 1.6): ['other_types']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 2 of 3 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
