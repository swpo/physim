# Evidence pack: rdtrail (seed 9)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0755-c07-kstrail-rd-twin/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 20s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world.py --out /tmp/claude-0/c11rev7/twin_kh05 --seeds 9 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9928], min area 6 px

## Measurements
- components: final 21, mean 10.4, max 21; occupancy final 0.32
- tracks: 57; persistent (alive >= 50% of run): 2; longest 123 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.84 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 21, 21], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.14/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 60, default): splits 24, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.125, nucleations 0
- channel total drift (end/start - 1): [7.6715, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 139: holes 0, rim-vs-core 0.56, rim-vs-outside 0.43, heterogeneity 0.18; core [0.889, 0.696, 0.806] rim [0.526, 0.468, 0.439]
  - track 25 at frame 143: holes 0, rim-vs-core 0.51, rim-vs-outside 0.32, heterogeneity 0.17; core [0.845, 0.576, 0.698] rim [0.488, 0.395, 0.383]
  - track 24 at frame 126: holes 0, rim-vs-core 0.40, rim-vs-outside 0.34, heterogeneity 0.16; core [0.819, 0.638, 0.79] rim [0.495, 0.493, 0.607]
  - track 38 at frame 171: holes 0, rim-vs-core 0.52, rim-vs-outside 0.47, heterogeneity 0.17; core [0.883, 0.727, 0.866] rim [0.536, 0.52, 0.545]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 7.88 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.714)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 3.06 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.618)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 5.61 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.71)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=417, R_eq 15.25): none; #25 (t=429, R_eq 12.84): none; #24 (t=378, R_eq 11.77): none; #38 (t=513, R_eq 14.54): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
