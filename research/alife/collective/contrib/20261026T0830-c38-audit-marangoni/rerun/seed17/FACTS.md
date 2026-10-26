# Evidence pack: active-nematic-marangoni (seed 17)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 665s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0830-c38-audit-marangoni/rerun/seed17 --seeds 17 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8429, 0.5748], min area 6 px

## Measurements
- components: final 28, mean 24.1, max 32; occupancy final 0.09
- tracks: 108; persistent (alive >= 50% of run): 18; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 29, 27], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.314/time; max body lengths 9.4
- replication (lineage window K = 20 frames = time 100, default): splits 39, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 3, merges 19, merge/split ratio 0.487, nucleations 11
- channel total drift (end/start - 1): [-0.5019, -0.45, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 114: holes 0, rim-vs-core 0.72, rim-vs-outside 0.33, heterogeneity 0.23; core [0.939, 0.684, 0.439, 0.438] rim [0.724, 0.424, 0.908, 0.01]
  - track 18 at frame 114: holes 0, rim-vs-core 0.71, rim-vs-outside 0.42, heterogeneity 0.24; core [0.964, 0.717, 0.354, 0.523] rim [0.793, 0.486, 0.827, 0.08]
  - track 26 at frame 123: holes 0, rim-vs-core 0.52, rim-vs-outside 0.39, heterogeneity 0.22; core [0.935, 0.671, 0.403, 0.399] rim [0.778, 0.488, 0.742, 0.091]
  - track 77 at frame 176: holes 0, rim-vs-core 0.67, rim-vs-outside 0.33, heterogeneity 0.20; core [0.945, 0.702, 0.374, 0.405] rim [0.753, 0.453, 0.811, 0.012]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 160 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.49 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.703)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 8.78 (aggregate of 160 individuals; 12/160 membrane-like individually; rim level 0.538)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.13 (aggregate of 160 individuals; 65/160 membrane-like individually; rim level 0.583)
  - radial cargo c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.493, rim/outside 2.12 (aggregate of 160 individuals; 20/160 membrane-like individually; rim level 0.129)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=570, R_eq 4.15): none; #18 (t=570, R_eq 4.18): ['surfactant s']; #26 (t=615, R_eq 3.99): none; #77 (t=880, R_eq 3.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 160 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
