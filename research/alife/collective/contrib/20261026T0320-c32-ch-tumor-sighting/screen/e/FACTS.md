# Evidence pack: ch-tumor (seed 0)

- world: `../../world.py`, family `ch-tumor`
- parent: None; mutation: Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 87s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0320-c32-ch-tumor-sighting/world.py --out collective/contrib/20261026T0320-c32-ch-tumor-sighting/screen/e --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.01, 1.3838], min area 6 px

## Measurements
- components: final 71, mean 51.9, max 77; occupancy final 0.32
- tracks: 295; persistent (alive >= 50% of run): 43; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.29 (1 = constant size)
- enclosures: components with a hole mean 0.47, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [77, 73, 71], H1 [2, 2, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 1.07/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 100, default): splits 69, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 60, merge/split ratio 0.87, nucleations 88
- channel total drift (end/start - 1): [0.1452, -0.8596]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 123: holes 1, rim-vs-core 0.09, rim-vs-outside 0.39, heterogeneity 0.04; core [0.589, 0.075] rim [0.501, 0.078]
  - track 114 at frame 131: holes 0, rim-vs-core 0.11, rim-vs-outside 0.38, heterogeneity 0.05; core [0.606, 0.069] rim [0.497, 0.077]
  - track 259 at frame 155: holes 0, rim-vs-core 0.14, rim-vs-outside 0.32, heterogeneity 0.05; core [0.606, 0.07] rim [0.467, 0.083]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 361 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial phi (tissue): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 5.39 (aggregate of 361 individuals; 13/361 membrane-like individually; rim level 0.471)
  - radial sigma (nutrient): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.952 (aggregate of 361 individuals; 0/361 membrane-like individually; rim level 0.0943)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=615, R_eq 11.71, ring): ['phi (tissue)']; #13 (t=620, R_eq 15.5, ring): ['phi (tissue)']; #114 (t=655, R_eq 11.03): none; #259 (t=775, R_eq 7.61): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 36 of 361 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
