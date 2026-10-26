# Evidence pack: ch-tumor (seed 0)

- world: `../../world.py`, family `ch-tumor`
- parent: None; mutation: Cahn-Hilliard tissue with nutrient-limited proliferation and apoptosis (new class)
- run: 3 frames x 100 steps x dt 0.05 = time 10; grid [192, 192]; wall 1s; status non-finite fields at frame 3
- command: `python -m labkit.run collective/contrib/20261026T0320-c32-ch-tumor-sighting/world.py --out collective/contrib/20261026T0320-c32-ch-tumor-sighting/screen/f --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.2062, 1.7509], min area 6 px

## Measurements
- components: final 1, mean 0.7, max 1; occupancy final 1.00
- tracks: 1; persistent (alive >= 50% of run): 1; longest 2 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.00 (1 = constant size)
- enclosures: components with a hole mean 0.33, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 4, 1], H1 [11, 4, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 1
- channel total drift (end/start - 1): [4.8124, -0.5113]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1 components >= 12 px at frames [2]):
  - radial phi (tissue): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.997)
  - radial sigma (nutrient): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside n/a (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0.0056)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=10, R_eq 108.32): none

## Warnings
- RUN FAILED: non-finite fields at frame 3 (only 3 frames analysed)
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- fewer than 30 recorded frames: tracking statistics are weak
- lineage window K=20 frames is more than half the run: late splits cannot count as persistent
- radial: for 1 of 1 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
