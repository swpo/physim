# Evidence pack: ch-tumor (seed 0)

- world: `../../world.py`, family `ch-tumor`
- parent: None; mutation: Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 87s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0320-c32-ch-tumor-sighting/world.py --out collective/contrib/20261026T0320-c32-ch-tumor-sighting/screen/h --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0464, 1.385], min area 6 px

## Measurements
- components: final 200, mean 111.4, max 240; occupancy final 0.28
- tracks: 385; persistent (alive >= 50% of run): 53; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [212, 204, 196], H1 [9, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 84, merge/split ratio 5.6, nucleations 271
- channel total drift (end/start - 1): [0.1582, -0.8694]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 148: holes 0, rim-vs-core 0.14, rim-vs-outside 0.17, heterogeneity 0.04; core [0.558, 0.078] rim [0.421, 0.081]
  - track 2 at frame 148: holes 0, rim-vs-core 0.13, rim-vs-outside 0.21, heterogeneity 0.04; core [0.565, 0.076] rim [0.44, 0.079]
  - track 4 at frame 148: holes 0, rim-vs-core 0.12, rim-vs-outside 0.18, heterogeneity 0.04; core [0.562, 0.079] rim [0.44, 0.082]
  - track 333 at frame 166: holes 0, rim-vs-core 0.11, rim-vs-outside 0.30, heterogeneity 0.04; core [0.57, 0.073] rim [0.462, 0.077]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 752 components >= 12 px at frames [101, 133, 166, 200]):
  - radial phi (tissue): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 6.97 (aggregate of 752 individuals; 1/752 membrane-like individually; rim level 0.485)
  - radial sigma (nutrient): peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 0.961 (aggregate of 752 individuals; 0/752 membrane-like individually; rim level 0.0847)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=740, R_eq 3.04): none; #2 (t=740, R_eq 3.52): none; #4 (t=740, R_eq 2.71): none; #333 (t=830, R_eq 7, ring): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 752 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
