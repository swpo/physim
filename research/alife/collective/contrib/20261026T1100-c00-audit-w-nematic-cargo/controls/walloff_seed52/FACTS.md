# Evidence pack: active-nematic-cargo-walloff (seed 52)

- world: `../../variants/active-nematic-cargo-walloff.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 484s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo/variants/active-nematic-cargo-walloff.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo/controls/walloff_seed52 --seeds 52 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8275, 0.6335], min area 6 px

## Measurements
- components: final 34, mean 25.2, max 37; occupancy final 0.07
- tracks: 114; persistent (alive >= 50% of run): 12; longest 162 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 34, 34], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.128/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 100, default): splits 45, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 4, merges 14, merge/split ratio 0.311, nucleations 10
- channel total drift (end/start - 1): [-0.5041, -0.3278, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 108: holes 0, rim-vs-core 0.40, rim-vs-outside 0.41, heterogeneity 0.10; core [0.94, 0.906, 0.875, 0.103] rim [0.718, 0.598, 0.74, 0.137]
  - track 23 at frame 113: holes 0, rim-vs-core 0.34, rim-vs-outside 0.37, heterogeneity 0.09; core [0.918, 0.791, 0.942, 0.096] rim [0.729, 0.535, 0.814, 0.117]
  - track 34 at frame 133: holes 0, rim-vs-core 0.36, rim-vs-outside 0.37, heterogeneity 0.10; core [0.92, 0.844, 0.907, 0.107] rim [0.721, 0.564, 0.787, 0.134]
  - track 84 at frame 171: holes 0, rim-vs-core 0.35, rim-vs-outside 0.39, heterogeneity 0.10; core [0.939, 0.87, 0.83, 0.113] rim [0.741, 0.6, 0.721, 0.147]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 166 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.86 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.764)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 8.42 (aggregate of 166 individuals; 1/166 membrane-like individually; rim level 0.648)
  - radial surfactant s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 2.15 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.792)
  - radial cargo c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.4, rim/outside 0.676 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.255)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=540, R_eq 3.29): none; #23 (t=565, R_eq 3.52): none; #34 (t=665, R_eq 3.19): none; #84 (t=855, R_eq 2.88): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 166 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
