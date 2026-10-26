# Evidence pack: active-nematic-marangoni (seed 9)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 671s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev9/k0_s9 --seeds 9 --frames 200 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8395, 0.5757], min area 6 px

## Measurements
- components: final 29, mean 23.0, max 31; occupancy final 0.09
- tracks: 112; persistent (alive >= 50% of run): 15; longest 153 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 29], H1 [0, 0, 0]
- motion: 59 long-lived tracks moved >= 1 body length; max speed 0.28/time; max body lengths 7.7
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 3, merges 19, merge/split ratio 0.463, nucleations 11
- channel total drift (end/start - 1): [-0.498, -0.4161, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 106: holes 0, rim-vs-core 0.53, rim-vs-outside 0.33, heterogeneity 0.15; core [0.944, 0.698, 0.384, 0.8] rim [0.74, 0.447, 0.805, 0.756]
  - track 47 at frame 141: holes 0, rim-vs-core 0.57, rim-vs-outside 0.33, heterogeneity 0.15; core [0.936, 0.705, 0.424, 0.902] rim [0.73, 0.429, 0.871, 0.861]
  - track 11 at frame 87: holes 0, rim-vs-core 0.49, rim-vs-outside 0.38, heterogeneity 0.14; core [0.927, 0.848, 0.448, 0.768] rim [0.765, 0.578, 0.828, 0.743]
  - track 70 at frame 163: holes 0, rim-vs-core 0.54, rim-vs-outside 0.41, heterogeneity 0.14; core [0.929, 0.82, 0.475, 0.993] rim [0.746, 0.564, 0.915, 0.982]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 152 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 4.59 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.71)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 8.85 (aggregate of 152 individuals; 10/152 membrane-like individually; rim level 0.542)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.25 (aggregate of 152 individuals; 72/152 membrane-like individually; rim level 0.591)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 1.26 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.77)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=530, R_eq 4.33): none; #47 (t=705, R_eq 4.22): none; #11 (t=435, R_eq 4.75): none; #70 (t=815, R_eq 4.51): none

## Warnings
- radial: 5 of 152 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
