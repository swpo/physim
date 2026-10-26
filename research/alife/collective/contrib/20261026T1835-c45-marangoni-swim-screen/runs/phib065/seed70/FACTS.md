# Evidence pack: active-nematic-marangoni (seed 70)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 360s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/phib065/seed70 --seeds 70 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.7855, 0.486], min area 6 px

## Measurements
- components: final 8, mean 2.8, max 8; occupancy final 0.02
- tracks: 18; persistent (alive >= 50% of run): 0; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [1, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.398/time; max body lengths 7.2
- replication (lineage window K = 20 frames = time 100, default): splits 8, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.125, nucleations 1
- channel total drift (end/start - 1): [-0.6227, -0.8362, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 148: holes 0, rim-vs-core 0.42, rim-vs-outside 0.45, heterogeneity 0.12; core [1.0, 0.961, 0.6, 0.0] rim [0.914, 0.765, 0.967, 0.0]
  - track 4 at frame 118: holes 0, rim-vs-core 0.45, rim-vs-outside 0.53, heterogeneity 0.09; core [1.0, 1.0, 0.544, 0.0] rim [0.926, 0.94, 0.983, 0.0]
  - track 9 at frame 166: holes 0, rim-vs-core 0.50, rim-vs-outside 0.50, heterogeneity 0.11; core [1.0, 0.998, 0.469, 0.0] rim [0.936, 0.916, 0.962, 0.0]
  - track 12 at frame 187: holes 0, rim-vs-core 0.58, rim-vs-outside 0.53, heterogeneity 0.12; core [1.0, 1.0, 0.367, 0.0] rim [0.956, 0.917, 0.943, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 21 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 4.83 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.822)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 7.36 (aggregate of 21 individuals; 1/21 membrane-like individually; rim level 0.819)
  - radial surfactant s: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.34, rim/outside 3.29 (aggregate of 21 individuals; 10/21 membrane-like individually; rim level 0.752)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 21 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=740, R_eq 4.26): none; #4 (t=590, R_eq 3.99): none; #9 (t=830, R_eq 3.83): none; #12 (t=935, R_eq 3.14): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
