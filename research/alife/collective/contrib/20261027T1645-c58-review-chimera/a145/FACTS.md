# Evidence pack: chimera-field (seed 5)

- world: `../../20261027T1049-c55-chimera-field-negative/world.py`, family `nonlocal-oscillators`
- parent: None; mutation: -
- run: 121 frames x 50 steps x dt 0.1 = time 600; grid [128, 128]; wall 13s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1049-c55-chimera-field-negative/world.py --out collective/contrib/20261027T1645-c58-review-chimera/a145 --seeds 5 --frames 120 --spf 50 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9878], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.98
- tracks: 1; persistent (alive >= 50% of run): 1; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.12 (1 = constant size)
- enclosures: components with a hole mean 0.90, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 4, 2], H1 [5, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.584/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 1
- channel total drift (end/start - 1): [None, -8.5736, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 4, rim-vs-core 0.17, rim-vs-outside 0.56, heterogeneity 0.20; core [0.65, 0.463, 0.0, 0.466] rim [0.5, 0.479, 0.0, 0.383]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial incoherence 1-|Z|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.542)
  - radial cos phase: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.703)
  - radial fuel Y: flat profile (no radial structure; level 0; aggregate of 6 individuals)
  - radial local frequency: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.397)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=305, R_eq 71.25): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 6 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
