# Evidence pack: ch-tumor (seed 0)

- world: `../../world.py`, family `ch-tumor`
- parent: None; mutation: Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 88s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0320-c32-ch-tumor-sighting/world.py --out collective/contrib/20261026T0320-c32-ch-tumor-sighting/screen/d --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0192, 1.0278], min area 6 px

## Measurements
- components: final 81, mean 99.4, max 209; occupancy final 0.31
- tracks: 392; persistent (alive >= 50% of run): 91; longest 185 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [81, 81, 81], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 100, default): splits 94, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 50, merge/split ratio 0.532, nucleations 32
- channel total drift (end/start - 1): [1.9771, -0.7438]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 109: holes 0, rim-vs-core 0.25, rim-vs-outside 0.58, heterogeneity 0.11; core [0.966, 0.128] rim [0.718, 0.131]
  - track 26 at frame 109: holes 0, rim-vs-core 0.36, rim-vs-outside 0.46, heterogeneity 0.11; core [0.962, 0.126] rim [0.601, 0.132]
  - track 33 at frame 109: holes 0, rim-vs-core 0.39, rim-vs-outside 0.27, heterogeneity 0.10; core [0.885, 0.132] rim [0.497, 0.135]
  - track 38 at frame 109: holes 0, rim-vs-core 0.36, rim-vs-outside 0.47, heterogeneity 0.11; core [0.962, 0.129] rim [0.605, 0.133]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 631 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (tissue): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 11.8 (aggregate of 631 individuals; 0/631 membrane-like individually; rim level 0.849)
  - radial sigma (nutrient): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.987 (aggregate of 631 individuals; 0/631 membrane-like individually; rim level 0.141)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=545, R_eq 6.65): none; #26 (t=545, R_eq 6.82): none; #33 (t=545, R_eq 5.26): none; #38 (t=545, R_eq 6.31): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
