# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 231s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.03_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8154, 0.5469], min area 6 px

## Measurements
- components: final 22, mean 10.8, max 23; occupancy final 0.08
- tracks: 46; persistent (alive >= 50% of run): 1; longest 51 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.65 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 24, 22], H1 [1, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.398/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.1, nucleations 4
- channel total drift (end/start - 1): [-0.4915, -0.2832, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 75: holes 0, rim-vs-core 0.68, rim-vs-outside 0.36, heterogeneity 0.22; core [0.941, 0.778, 0.506, 0.482] rim [0.747, 0.534, 0.9, 0.027]
  - track 14 at frame 76: holes 0, rim-vs-core 0.88, rim-vs-outside 0.36, heterogeneity 0.26; core [0.978, 0.768, 0.428, 0.595] rim [0.764, 0.453, 0.971, 0.014]
  - track 20 at frame 81: holes 0, rim-vs-core 0.76, rim-vs-outside 0.35, heterogeneity 0.22; core [0.947, 0.806, 0.464, 0.584] rim [0.757, 0.534, 0.864, 0.031]
  - track 32 at frame 89: holes 0, rim-vs-core 0.84, rim-vs-outside 0.41, heterogeneity 0.24; core [0.979, 0.933, 0.35, 0.612] rim [0.778, 0.595, 0.818, 0.034]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 4.31 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.694)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 6.3 (aggregate of 77 individuals; 4/77 membrane-like individually; rim level 0.578)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.39 (aggregate of 77 individuals; 37/77 membrane-like individually; rim level 0.652)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.382, rim/outside 1.64 (aggregate of 77 individuals; 9/77 membrane-like individually; rim level 0.173)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=375, R_eq 4.37): none; #14 (t=380, R_eq 4.41): none; #20 (t=405, R_eq 4.22): none; #32 (t=445, R_eq 3.29): ['surfactant s']

## Warnings
- radial: 2 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
