# Evidence pack: active-nematic-marangoni (seed 70)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 392s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/gm05/seed70 --seeds 70 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8326, 0.5547], min area 6 px

## Measurements
- components: final 34, mean 22.5, max 34; occupancy final 0.09
- tracks: 97; persistent (alive >= 50% of run): 16; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.77 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 34, 29], H1 [0, 0, 0]
- motion: 53 long-lived tracks moved >= 1 body length; max speed 0.302/time; max body lengths 9.4
- replication (lineage window K = 20 frames = time 100, default): splits 39, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.308, nucleations 7
- channel total drift (end/start - 1): [-0.4979, -0.444, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 113: holes 0, rim-vs-core 0.49, rim-vs-outside 0.34, heterogeneity 0.13; core [0.908, 0.799, 0.534, 0.0] rim [0.731, 0.551, 0.924, 0.0]
  - track 22 at frame 126: holes 0, rim-vs-core 0.53, rim-vs-outside 0.34, heterogeneity 0.14; core [0.94, 0.78, 0.44, 0.0] rim [0.743, 0.5, 0.84, 0.0]
  - track 29 at frame 129: holes 0, rim-vs-core 0.54, rim-vs-outside 0.42, heterogeneity 0.14; core [0.923, 0.921, 0.507, 0.0] rim [0.731, 0.645, 0.925, 0.0]
  - track 79 at frame 185: holes 0, rim-vs-core 0.61, rim-vs-outside 0.40, heterogeneity 0.14; core [0.979, 0.921, 0.285, 0.0] rim [0.781, 0.574, 0.745, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 156 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4.56 (aggregate of 156 individuals; 0/156 membrane-like individually; rim level 0.728)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 8.92 (aggregate of 156 individuals; 5/156 membrane-like individually; rim level 0.567)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 3.29 (aggregate of 156 individuals; 77/156 membrane-like individually; rim level 0.61)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 156 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=565, R_eq 4.75): none; #22 (t=630, R_eq 3.91): none; #29 (t=645, R_eq 4.58): none; #79 (t=925, R_eq 3.09): ['surfactant s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
