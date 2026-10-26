# Evidence pack: active-nematic-marangoni-res15 (seed 51)

- world: `../../variants/active-nematic-marangoni-res15.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [192, 192]; wall 563s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni/variants/active-nematic-marangoni-res15.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni/controls/res15_seed51 --seeds 51 --size 192 192 --frames 100 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8353, 0.6423], min area 6 px

## Measurements
- components: final 29, mean 16.0, max 29; occupancy final 0.09
- tracks: 63; persistent (alive >= 50% of run): 10; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 26], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.528/time; max body lengths 7.1
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.115, nucleations 8
- channel total drift (end/start - 1): [-0.494, -0.2786, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 64: holes 0, rim-vs-core 0.98, rim-vs-outside 0.52, heterogeneity 0.26; core [0.983, 0.894, 0.298, 0.875] rim [0.787, 0.576, 0.784, 0.11]
  - track 8 at frame 61: holes 0, rim-vs-core 0.78, rim-vs-outside 0.53, heterogeneity 0.24; core [0.965, 0.906, 0.277, 0.636] rim [0.789, 0.621, 0.719, 0.09]
  - track 13 at frame 60: holes 0, rim-vs-core 0.75, rim-vs-outside 0.45, heterogeneity 0.21; core [0.939, 0.883, 0.331, 0.619] rim [0.76, 0.616, 0.693, 0.044]
  - track 18 at frame 71: holes 0, rim-vs-core 0.97, rim-vs-outside 0.52, heterogeneity 0.26; core [0.99, 0.971, 0.246, 0.763] rim [0.781, 0.644, 0.764, 0.044]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 113 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 5.04 (aggregate of 113 individuals; 0/113 membrane-like individually; rim level 0.728)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.738, rim/outside 9.94 (aggregate of 113 individuals; 5/113 membrane-like individually; rim level 0.576)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 3.5 (aggregate of 113 individuals; 69/113 membrane-like individually; rim level 0.549)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.385, rim/outside 4.49 (aggregate of 113 individuals; 13/113 membrane-like individually; rim level 0.175)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=320, R_eq 6.26): ['surfactant s']; #8 (t=305, R_eq 7.11): ['cargo c']; #13 (t=300, R_eq 6.86): none; #18 (t=355, R_eq 6.41): ['surfactant s']

## Warnings
- radial: 2 of 113 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
