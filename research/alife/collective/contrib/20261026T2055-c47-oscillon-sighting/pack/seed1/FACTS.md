# Evidence pack: param-oscillon (seed 1)

- world: `../../world.py`, family `parametric-oscillon`
- parent: None; mutation: new class: damped wave field with detuned parametric pumping drawn from a consumed, regrowing energy field
- run: 151 frames x 1000 steps x dt 0.02 = time 3000; grid [128, 128]; wall 601s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2055-c47-oscillon-sighting/world.py --out collective/contrib/20261026T2055-c47-oscillon-sighting/pack --seeds 0 1 --frames 150 --lineage-k 5 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0042, 1.6722], min area 6 px

## Measurements
- components: final 56, mean 72.6, max 155; occupancy final 0.13
- tracks: 416; persistent (alive >= 50% of run): 62; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.41 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [61, 60, 56], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.0305/time; max body lengths 2.4
- replication (lineage window K = 5 frames = time 100, --lineage-k): splits 52, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 132, merge/split ratio 2.54, nucleations 0
- channel total drift (end/start - 1): [-0.6998, -0.2375]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 64 at frame 77: holes 0, rim-vs-core 0.38, rim-vs-outside 0.18, heterogeneity 0.13; core [0.786, 0.296] rim [0.415, 0.371]
  - track 162 at frame 77: holes 0, rim-vs-core 0.24, rim-vs-outside 0.30, heterogeneity 0.13; core [0.77, 0.258] rim [0.535, 0.3]
  - track 166 at frame 77: holes 0, rim-vs-core 0.38, rim-vs-outside 0.16, heterogeneity 0.13; core [0.767, 0.317] rim [0.398, 0.395]
  - track 173 at frame 77: holes 0, rim-vs-core 0.37, rim-vs-outside 0.17, heterogeneity 0.13; core [0.769, 0.324] rim [0.404, 0.403]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 411 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial A: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 11.2 (aggregate of 411 individuals; 2/411 membrane-like individually; rim level 0.623)
  - radial E: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.895 (aggregate of 411 individuals; 0/411 membrane-like individually; rim level 0.407)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #64 (t=1540, R_eq 3.34): none; #162 (t=1540, R_eq 3.29): none; #166 (t=1540, R_eq 3.39): none; #173 (t=1540, R_eq 3.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
