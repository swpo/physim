# Evidence pack: ch-tumor (seed 0)

- world: `../../world.py`, family `ch-tumor`
- parent: None; mutation: Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 88s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0320-c32-ch-tumor-sighting/world.py --out collective/contrib/20261026T0320-c32-ch-tumor-sighting/screen/c --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0475, 0.957], min area 6 px

## Measurements
- components: final 1, mean 12.4, max 175; occupancy final 0.00
- tracks: 278; persistent (alive >= 50% of run): 1; longest 187 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.93 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 100, default): splits 99, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.612, -0.699]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 34 at frame 108: holes 0, rim-vs-core 0.35, rim-vs-outside 0.50, heterogeneity 0.11; core [0.992, 0.161] rim [0.638, 0.172]
  - track 166 at frame 30: holes 0, rim-vs-core 0.34, rim-vs-outside 0.27, heterogeneity 0.10; core [0.871, 0.107] rim [0.531, 0.109]
  - track 182 at frame 30: holes 0, rim-vs-core 0.34, rim-vs-outside 0.28, heterogeneity 0.10; core [0.875, 0.106] rim [0.535, 0.109]
  - track 33 at frame 27: holes 0, rim-vs-core 0.33, rim-vs-outside 0.30, heterogeneity 0.09; core [0.907, 0.083] rim [0.575, 0.085]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (tissue): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 9.86 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.721)
  - radial sigma (nutrient): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.973 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.153)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #34 (t=540, R_eq 6.18): none; #166 (t=150, R_eq 3.14): none; #182 (t=150, R_eq 3.19): none; #33 (t=135, R_eq 3.24): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
