# Evidence pack: active-nematic-marangoni (seed 70)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 351s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/kr006/seed70 --seeds 70 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8803, 0.6215], min area 6 px

## Measurements
- components: final 27, mean 30.1, max 52; occupancy final 0.11
- tracks: 325; persistent (alive >= 50% of run): 3; longest 162 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 27, 24], H1 [1, 0, 0]
- motion: 75 long-lived tracks moved >= 1 body length; max speed 0.254/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 100, default): splits 89, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 92, merge/split ratio 1.03, nucleations 49
- channel total drift (end/start - 1): [-0.4967, -0.3315, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 72 at frame 108: holes 0, rim-vs-core 0.59, rim-vs-outside 0.36, heterogeneity 0.14; core [0.952, 0.859, 0.328, 0.0] rim [0.765, 0.502, 0.76, 0.0]
  - track 37 at frame 94: holes 0, rim-vs-core 0.53, rim-vs-outside 0.32, heterogeneity 0.14; core [0.952, 0.628, 0.321, 0.0] rim [0.753, 0.397, 0.759, 0.0]
  - track 35 at frame 69: holes 0, rim-vs-core 0.60, rim-vs-outside 0.34, heterogeneity 0.15; core [0.945, 0.846, 0.348, 0.0] rim [0.745, 0.489, 0.78, 0.0]
  - track 254 at frame 182: holes 0, rim-vs-core 0.50, rim-vs-outside 0.34, heterogeneity 0.14; core [0.953, 0.603, 0.326, 0.0] rim [0.767, 0.394, 0.745, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 182 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 3.68 (aggregate of 182 individuals; 7/182 membrane-like individually; rim level 0.662)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 6.22 (aggregate of 182 individuals; 28/182 membrane-like individually; rim level 0.445)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 2.81 (aggregate of 182 individuals; 70/182 membrane-like individually; rim level 0.544)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 182 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #72 (t=540, R_eq 3.24): ['surfactant s']; #37 (t=470, R_eq 4.11): none; #35 (t=345, R_eq 3.78): ['surfactant s']; #254 (t=910, R_eq 4.3): none

## Warnings
- radial: 21 of 182 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
