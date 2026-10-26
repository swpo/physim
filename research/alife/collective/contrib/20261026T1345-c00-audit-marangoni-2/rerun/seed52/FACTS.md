# Evidence pack: active-nematic-marangoni (seed 52)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 520s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni/rerun/seed52 --seeds 52 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8406, 0.5773], min area 6 px

## Measurements
- components: final 32, mean 25.4, max 33; occupancy final 0.09
- tracks: 101; persistent (alive >= 50% of run): 14; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 32, 32], H1 [0, 0, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.263/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 4, merges 13, merge/split ratio 0.342, nucleations 11
- channel total drift (end/start - 1): [-0.5041, -0.3952, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 111: holes 0, rim-vs-core 0.65, rim-vs-outside 0.37, heterogeneity 0.23; core [0.944, 0.764, 0.41, 0.416] rim [0.772, 0.472, 0.825, 0.054]
  - track 14 at frame 111: holes 0, rim-vs-core 0.64, rim-vs-outside 0.31, heterogeneity 0.22; core [0.934, 0.572, 0.411, 0.38] rim [0.719, 0.358, 0.839, 0.01]
  - track 25 at frame 118: holes 0, rim-vs-core 0.74, rim-vs-outside 0.34, heterogeneity 0.24; core [0.966, 0.692, 0.382, 0.451] rim [0.768, 0.457, 0.898, 0.011]
  - track 93 at frame 190: holes 0, rim-vs-core 0.80, rim-vs-outside 0.38, heterogeneity 0.22; core [0.971, 0.885, 0.24, 0.557] rim [0.792, 0.541, 0.676, 0.012]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 169 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 4.79 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.724)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 9.59 (aggregate of 169 individuals; 14/169 membrane-like individually; rim level 0.555)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.3 (aggregate of 169 individuals; 84/169 membrane-like individually; rim level 0.592)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.446, rim/outside 2.1 (aggregate of 169 individuals; 19/169 membrane-like individually; rim level 0.129)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=555, R_eq 4.37): none; #14 (t=555, R_eq 4.33): ['order |Q|', 'cargo c']; #25 (t=590, R_eq 4.37): ['surfactant s']; #93 (t=950, R_eq 2.88): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
