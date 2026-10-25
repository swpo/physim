# Evidence pack: rdtrail (seed 9)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0755-c07-kstrail-rd-twin/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 120 steps x dt 0.025 (--dt; world META dt 0.05) = time 600; grid [192, 192]; wall 41s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world.py --out /tmp/claude-0/c11rev7/twin_kh05_dt2 --seeds 9 --dt 0.025 --spf 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9904], min area 6 px

## Measurements
- components: final 25, mean 17.2, max 27; occupancy final 0.48
- tracks: 79; persistent (alive >= 50% of run): 14; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.84 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [2, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.28/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 60, default): splits 33, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.182, nucleations 0
- channel total drift (end/start - 1): [11.812, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 123: holes 0, rim-vs-core 0.42, rim-vs-outside 0.35, heterogeneity 0.14; core [0.8, 0.591, 0.836] rim [0.487, 0.449, 0.591]
  - track 32 at frame 133: holes 0, rim-vs-core 0.50, rim-vs-outside 0.55, heterogeneity 0.18; core [0.915, 0.834, 0.881] rim [0.594, 0.618, 0.569]
  - track 39 at frame 139: holes 0, rim-vs-core 0.40, rim-vs-outside 0.37, heterogeneity 0.13; core [0.802, 0.623, 0.882] rim [0.504, 0.48, 0.652]
  - track 59 at frame 171: holes 0, rim-vs-core 0.34, rim-vs-outside 0.24, heterogeneity 0.11; core [0.719, 0.549, 0.844] rim [0.448, 0.451, 0.656]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 3.58 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.768)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 1.97 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.664)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.758, rim/outside 3.35 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.703)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=369, R_eq 10.49): none; #32 (t=399, R_eq 15.13): none; #39 (t=417, R_eq 10.33): none; #59 (t=513, R_eq 7.9): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
