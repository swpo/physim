# Evidence pack: cips-fuel (seed 5)

- world: `../../../20261026T0146-c25-cips-slowp-negative-fix/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 200 steps x dt 0.1 = time 6000; grid [128, 128]; wall 155s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0146-c25-cips-slowp-negative-fix/world.py --out collective/contrib/20261026T0221-c30-review-cips-slowp/rerun/st_dp02_dthalf --seeds 5 --size 128 128 --frames 300 --spf 200 --no-movie`
- segmentation: matter > 0.52 of robust range [0.0005, 0.9543], min area 6 px

## Measurements
- components: final 51, mean 65.8, max 107; occupancy final 0.13
- tracks: 202; persistent (alive >= 50% of run): 50; longest 287 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 53, 52], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00578/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 400, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 57, merge/split ratio n/a, nucleations 145
- channel total drift (end/start - 1): [0.0, -0.5395, 0.4486]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 159: holes 0, rim-vs-core 0.13, rim-vs-outside 0.37, heterogeneity 0.04; core [0.897, 0.912, 0.029] rim [0.793, 0.854, 0.076]
  - track 10 at frame 159: holes 0, rim-vs-core 0.18, rim-vs-outside 0.48, heterogeneity 0.06; core [0.963, 0.945, 0.01] rim [0.814, 0.859, 0.074]
  - track 15 at frame 159: holes 0, rim-vs-core 0.18, rim-vs-outside 0.43, heterogeneity 0.06; core [0.948, 0.916, 0.016] rim [0.8, 0.834, 0.082]
  - track 0 at frame 154: holes 0, rim-vs-core 0.19, rim-vs-outside 0.47, heterogeneity 0.06; core [0.954, 0.933, 0.013] rim [0.8, 0.847, 0.081]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 337 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 21.6 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.869)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 4.3 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.903)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.6, rim/outside 0.503 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.413)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=3180, R_eq 2.76): none; #10 (t=3180, R_eq 2.76): none; #15 (t=3180, R_eq 2.33): none; #0 (t=3080, R_eq 2.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 337 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
