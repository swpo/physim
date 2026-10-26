# Evidence pack: active-nematic-cargo-kappa0 (seed 51)

- world: `../../variants/active-nematic-cargo-kappa0.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 474s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo/variants/active-nematic-cargo-kappa0.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo/controls/kappa0_seed51 --seeds 51 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.826, 0.6194], min area 6 px

## Measurements
- components: final 29, mean 20.9, max 32; occupancy final 0.07
- tracks: 125; persistent (alive >= 50% of run): 4; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.52 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 29], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.0834/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 100, default): splits 50, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 18, merge/split ratio 0.36, nucleations 7
- channel total drift (end/start - 1): [-0.5063, -0.3856, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 128: holes 0, rim-vs-core 0.55, rim-vs-outside 0.35, heterogeneity 0.13; core [0.96, 0.921, 0.287, 0.942] rim [0.754, 0.612, 0.686, 0.897]
  - track 44 at frame 138: holes 0, rim-vs-core 0.48, rim-vs-outside 0.34, heterogeneity 0.13; core [0.932, 0.807, 0.316, 0.919] rim [0.727, 0.535, 0.651, 0.88]
  - track 34 at frame 118: holes 0, rim-vs-core 0.54, rim-vs-outside 0.35, heterogeneity 0.13; core [0.959, 0.911, 0.268, 0.86] rim [0.752, 0.612, 0.662, 0.818]
  - track 81 at frame 160: holes 0, rim-vs-core 0.46, rim-vs-outside 0.34, heterogeneity 0.12; core [0.94, 0.88, 0.289, 0.933] rim [0.747, 0.595, 0.591, 0.888]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 142 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 4.74 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.755)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.749, rim/outside 8.04 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.638)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.81, rim/outside 2.97 (aggregate of 142 individuals; 121/142 membrane-like individually; rim level 0.557)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 1.28 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.831)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #30 (t=640, R_eq 2.93): ['surfactant s']; #44 (t=690, R_eq 2.88): ['surfactant s']; #34 (t=590, R_eq 2.82): ['surfactant s']; #81 (t=800, R_eq 3.09): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 142 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
