# Evidence pack: ch-tumor (seed 0)

- world: `../../world.py`, family `ch-tumor`
- parent: None; mutation: Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 87s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0320-c32-ch-tumor-sighting/world.py --out collective/contrib/20261026T0320-c32-ch-tumor-sighting/screen/b --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0304, 1.0065], min area 6 px

## Measurements
- components: final 31, mean 37.5, max 225; occupancy final 0.11
- tracks: 328; persistent (alive >= 50% of run): 31; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.50 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 31], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00732/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 100, default): splits 92, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5115, -0.7331]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 106: holes 0, rim-vs-core 0.39, rim-vs-outside 0.27, heterogeneity 0.11; core [0.9, 0.149] rim [0.506, 0.157]
  - track 52 at frame 106: holes 0, rim-vs-core 0.36, rim-vs-outside 0.47, heterogeneity 0.11; core [0.966, 0.146] rim [0.61, 0.157]
  - track 59 at frame 106: holes 0, rim-vs-core 0.25, rim-vs-outside 0.58, heterogeneity 0.11; core [0.966, 0.145] rim [0.719, 0.155]
  - track 104 at frame 106: holes 0, rim-vs-core 0.36, rim-vs-outside 0.46, heterogeneity 0.11; core [0.962, 0.142] rim [0.601, 0.155]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 188 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (tissue): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 28.9 (aggregate of 188 individuals; 0/188 membrane-like individually; rim level 0.872)
  - radial sigma (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.945 (aggregate of 188 individuals; 0/188 membrane-like individually; rim level 0.17)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #50 (t=530, R_eq 5.67): none; #52 (t=530, R_eq 6.51): none; #59 (t=530, R_eq 7.14): none; #104 (t=530, R_eq 7.16): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
