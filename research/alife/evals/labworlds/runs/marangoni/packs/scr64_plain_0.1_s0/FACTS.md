# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [64, 64]; wall 53s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/scr64_plain_0.1_s0 --seeds 0 --frames 100 --size 64 64 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8435, 0.5857], min area 6 px

## Measurements
- components: final 7, mean 7.4, max 11; occupancy final 0.07
- tracks: 51; persistent (alive >= 50% of run): 2; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 5], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.427/time; max body lengths 8.1
- replication (lineage window K = 20 frames = time 100, default): splits 11, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 12, merge/split ratio 1.09, nucleations 17
- channel total drift (end/start - 1): [-0.4841, 0.1649, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 46: holes 0, rim-vs-core 0.73, rim-vs-outside 0.39, heterogeneity 0.23; core [0.962, 0.94, 0.314, 0.266] rim [0.74, 0.512, 0.8, 0.023]
  - track 27 at frame 68: holes 0, rim-vs-core 0.30, rim-vs-outside 0.48, heterogeneity 0.22; core [0.944, 0.603, 0.41, 0.267] rim [0.831, 0.537, 0.659, 0.167]
  - track 14 at frame 48: holes 0, rim-vs-core 0.56, rim-vs-outside 0.30, heterogeneity 0.20; core [0.908, 0.792, 0.408, 0.279] rim [0.741, 0.504, 0.774, 0.024]
  - track 39 at frame 75: holes 0, rim-vs-core 0.31, rim-vs-outside 0.36, heterogeneity 0.19; core [0.868, 0.643, 0.569, 0.253] rim [0.778, 0.461, 0.759, 0.115]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 3.41 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.695)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.728, rim/outside 2.54 (aggregate of 49 individuals; 5/49 membrane-like individually; rim level 0.431)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 2.42 (aggregate of 49 individuals; 25/49 membrane-like individually; rim level 0.605)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.615, rim/outside 0.804 (aggregate of 49 individuals; 12/49 membrane-like individually; rim level 0.144)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=230, R_eq 3.95): ['surfactant s']; #27 (t=340, R_eq 4.33): none; #14 (t=240, R_eq 3.91): none; #39 (t=375, R_eq 3.52): ['cargo c']

## Warnings
- radial: 1 of 49 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
