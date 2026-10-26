# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out tr45 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 46.5, max 69; occupancy final 0.10
- tracks: 640; persistent (alive >= 50% of run): 4; longest 115 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 148 long-lived tracks moved >= 1 body length; max speed 0.611/time; max body lengths 27.0
- replication (lineage window K = 20 frames = time 60, default): splits 242, persistent splits 36 (0 more failed only because the siblings re-merged within K), max generation 5, merges 93, merge/split ratio 0.384, nucleations 6
- channel total drift (end/start - 1): [1.0, None, -0.5087, -0.1807]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 233 at frame 76: holes 0, rim-vs-core 0.27, rim-vs-outside 0.86, heterogeneity 0.17; core [0.941, 0.57, 1.0, 0.337] rim [0.708, 0.472, 0.933, 0.409]
  - track 446 at frame 145: holes 0, rim-vs-core 0.25, rim-vs-outside 0.93, heterogeneity 0.15; core [0.945, 0.526, 1.0, 0.323] rim [0.714, 0.458, 0.966, 0.389]
  - track 355 at frame 109: holes 0, rim-vs-core 0.28, rim-vs-outside 0.85, heterogeneity 0.15; core [0.908, 0.616, 1.0, 0.16] rim [0.691, 0.489, 0.919, 0.263]
  - track 554 at frame 171: holes 0, rim-vs-core 0.29, rim-vs-outside 0.91, heterogeneity 0.16; core [0.892, 0.512, 1.0, 0.235] rim [0.654, 0.407, 0.927, 0.33]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 261 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 2.98 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.709)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 1.91 (aggregate of 261 individuals; 7/261 membrane-like individually; rim level 0.541)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.843, rim/outside 28.5 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.815)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.875 (aggregate of 261 individuals; 11/261 membrane-like individually; rim level 0.397)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #233 (t=228, R_eq 2.99): none; #446 (t=435, R_eq 3.04): none; #355 (t=327, R_eq 2.82): none; #554 (t=513, R_eq 3.66): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 261 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
