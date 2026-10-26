# Evidence pack: active-nematic-rodsource (seed 7)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0300-c34-swimdivide/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 545s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0300-c34-swimdivide/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev/z10_s7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8077, 0.5533], min area 6 px

## Measurements
- components: final 32, mean 21.1, max 33; occupancy final 0.05
- tracks: 101; persistent (alive >= 50% of run): 12; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 32, 31], H1 [0, 0, 0]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.0738/time; max body lengths 6.1
- replication (lineage window K = 20 frames = time 100, default): splits 43, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 4, merges 8, merge/split ratio 0.186, nucleations 7
- channel total drift (end/start - 1): [-0.4954, -0.564, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 133: holes 0, rim-vs-core 0.45, rim-vs-outside 0.35, heterogeneity 0.16; core [0.946, 0.886, 0.44] rim [0.76, 0.611, 0.745]
  - track 30 at frame 134: holes 0, rim-vs-core 0.48, rim-vs-outside 0.34, heterogeneity 0.16; core [0.949, 0.916, 0.423] rim [0.742, 0.61, 0.732]
  - track 27 at frame 131: holes 0, rim-vs-core 0.43, rim-vs-outside 0.31, heterogeneity 0.15; core [0.919, 0.799, 0.518] rim [0.724, 0.522, 0.781]
  - track 79 at frame 180: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.15; core [0.952, 0.891, 0.459] rim [0.759, 0.605, 0.734]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 4.23 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.787)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 7.06 (aggregate of 146 individuals; 2/146 membrane-like individually; rim level 0.657)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 2.78 (aggregate of 146 individuals; 110/146 membrane-like individually; rim level 0.645)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #25 (t=665, R_eq 3.19): ['surfactant s']; #30 (t=670, R_eq 2.99): ['surfactant s']; #27 (t=655, R_eq 3.43): ['surfactant s']; #79 (t=900, R_eq 3.34): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 146 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
