# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv2.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 202s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv2.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/v2c --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9827], min area 6 px

## Measurements
- components: final 0, mean 6.3, max 20; occupancy final 0.00
- tracks: 67; persistent (alive >= 50% of run): 0; longest 95 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 1.36/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 50, default): splits 26, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 11, merge/split ratio 0.423, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, None, -0.479]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 125: holes 0, rim-vs-core 0.45, rim-vs-outside 0.42, heterogeneity 0.09; core [0.918, 0.17, 0.045, 0.0] rim [0.48, 0.269, 0.024, 0.01]
  - track 36 at frame 117: holes 0, rim-vs-core 0.45, rim-vs-outside 0.42, heterogeneity 0.09; core [0.913, 0.178, 0.044, 0.0] rim [0.478, 0.272, 0.023, 0.008]
  - track 37 at frame 117: holes 0, rim-vs-core 0.45, rim-vs-outside 0.42, heterogeneity 0.09; core [0.917, 0.17, 0.043, 0.001] rim [0.48, 0.267, 0.022, 0.016]
  - track 63 at frame 115: holes 0, rim-vs-core 0.34, rim-vs-outside 0.45, heterogeneity 0.08; core [0.879, 0.195, 0.029, 0.006] rim [0.544, 0.267, 0.018, 0.018]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [40, 81, 121, 159]):
  - radial u (cell): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 3.58 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.706)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.37, rim/outside 3.48 (aggregate of 40 individuals; 38/40 membrane-like individually; rim level 0.334)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 1.85 (aggregate of 40 individuals; 2/40 membrane-like individually; rim level 0.048)
  - radial n (nutrient): peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 1.04 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.113)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #43 (t=312.5, R_eq 23.04): ['|P| (actin polarization)']; #36 (t=292.5, R_eq 22.76): ['|P| (actin polarization)']; #37 (t=292.5, R_eq 22.84): ['|P| (actin polarization)']; #63 (t=287.5, R_eq 19.27): ['|P| (actin polarization)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 40 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
