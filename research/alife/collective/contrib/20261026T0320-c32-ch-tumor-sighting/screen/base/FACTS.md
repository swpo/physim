# Evidence pack: ch-tumor (seed 0)

- world: `../../world.py`, family `ch-tumor`
- parent: None; mutation: Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [192, 192]; wall 44s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0320-c32-ch-tumor-sighting/world.py --out collective/contrib/20261026T0320-c32-ch-tumor-sighting/screen/base --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0728, 0.4955], min area 6 px

## Measurements
- components: final 0, mean 1.8, max 179; occupancy final 0.00
- tracks: 180; persistent (alive >= 50% of run): 0; longest 4 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 100, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.7334, -0.8]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 4: holes 0, rim-vs-core 0.04, rim-vs-outside 0.13, heterogeneity 0.04; core [0.463, 0.019] rim [0.418, 0.019]
  - track 2 at frame 4: holes 0, rim-vs-core 0.03, rim-vs-outside 0.05, heterogeneity 0.01; core [0.392, 0.02] rim [0.36, 0.021]
  - track 3 at frame 4: holes 0, rim-vs-core 0.07, rim-vs-outside 0.08, heterogeneity 0.02; core [0.45, 0.019] rim [0.382, 0.02]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
