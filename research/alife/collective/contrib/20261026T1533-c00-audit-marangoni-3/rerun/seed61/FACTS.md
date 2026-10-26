# Evidence pack: active-nematic-marangoni (seed 61)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 561s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/minority/scout/seed61 --seeds 61 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8404, 0.5795], min area 6 px

## Measurements
- components: final 33, mean 24.7, max 33; occupancy final 0.09
- tracks: 81; persistent (alive >= 50% of run): 23; longest 184 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 33], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.314/time; max body lengths 10.7
- replication (lineage window K = 20 frames = time 100, default): splits 32, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 4, merges 7, merge/split ratio 0.219, nucleations 9
- channel total drift (end/start - 1): [-0.504, -0.3924, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 109: holes 0, rim-vs-core 0.67, rim-vs-outside 0.33, heterogeneity 0.22; core [0.938, 0.768, 0.407, 0.365] rim [0.727, 0.467, 0.835, 0.009]
  - track 30 at frame 124: holes 0, rim-vs-core 0.74, rim-vs-outside 0.29, heterogeneity 0.23; core [0.953, 0.469, 0.401, 0.462] rim [0.758, 0.27, 0.924, 0.012]
  - track 34 at frame 126: holes 0, rim-vs-core 0.74, rim-vs-outside 0.31, heterogeneity 0.24; core [0.954, 0.618, 0.384, 0.466] rim [0.755, 0.381, 0.875, 0.009]
  - track 76 at frame 178: holes 0, rim-vs-core 0.63, rim-vs-outside 0.30, heterogeneity 0.21; core [0.93, 0.599, 0.433, 0.359] rim [0.744, 0.393, 0.88, 0.015]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 166 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 4.82 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.725)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 9.83 (aggregate of 166 individuals; 10/166 membrane-like individually; rim level 0.567)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 3.34 (aggregate of 166 individuals; 89/166 membrane-like individually; rim level 0.597)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.442, rim/outside 2.35 (aggregate of 166 individuals; 13/166 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=545, R_eq 3.95): ['surfactant s']; #30 (t=620, R_eq 3.83): ['surfactant s']; #34 (t=630, R_eq 4.18): none; #76 (t=890, R_eq 4.41): ['order |Q|', 'cargo c']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 166 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
