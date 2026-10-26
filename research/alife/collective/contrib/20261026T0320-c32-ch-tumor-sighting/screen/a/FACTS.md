# Evidence pack: ch-tumor (seed 0)

- world: `../../world.py`, family `ch-tumor`
- parent: None; mutation: Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 87s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0320-c32-ch-tumor-sighting/world.py --out collective/contrib/20261026T0320-c32-ch-tumor-sighting/screen/a --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0222, 1.1387], min area 6 px

## Measurements
- components: final 100, mean 91.7, max 171; occupancy final 0.30
- tracks: 208; persistent (alive >= 50% of run): 101; longest 152 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [101, 101, 100], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 100, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 30, merge/split ratio 10, nucleations 172
- channel total drift (end/start - 1): [-0.0055, -0.745]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 124: holes 0, rim-vs-core 0.31, rim-vs-outside 0.25, heterogeneity 0.08; core [0.813, 0.145] rim [0.499, 0.148]
  - track 2 at frame 126: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.09; core [0.8, 0.147] rim [0.482, 0.15]
  - track 3 at frame 126: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.09; core [0.81, 0.145] rim [0.49, 0.148]
  - track 4 at frame 126: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.09; core [0.803, 0.146] rim [0.483, 0.149]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 612 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial phi (tissue): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 13.9 (aggregate of 612 individuals; 0/612 membrane-like individually; rim level 0.771)
  - radial sigma (nutrient): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.988 (aggregate of 612 individuals; 0/612 membrane-like individually; rim level 0.152)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=620, R_eq 5.5): none; #2 (t=630, R_eq 5.05): none; #3 (t=630, R_eq 5.35): none; #4 (t=630, R_eq 5.11): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
