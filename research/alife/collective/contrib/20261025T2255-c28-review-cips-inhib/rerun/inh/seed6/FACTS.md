# Evidence pack: cips-inhib (seed 6)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 100s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out /tmp/claude-0/c28ci/inh --seeds 5 6 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0014, 0.99], min area 6 px

## Measurements
- components: final 30, mean 30.2, max 44; occupancy final 0.13
- tracks: 56; persistent (alive >= 50% of run): 33; longest 540 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 30], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 10, merge/split ratio n/a, nucleations 46
- channel total drift (end/start - 1): [-0.0, -0.582, 0.401, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 333: holes 0, rim-vs-core 0.37, rim-vs-outside 0.40, heterogeneity 0.10; core [0.949, 0.883, 0.223, 0.803] rim [0.698, 0.686, 0.365, 0.675]
  - track 1 at frame 338: holes 0, rim-vs-core 0.34, rim-vs-outside 0.39, heterogeneity 0.09; core [0.937, 0.84, 0.234, 0.816] rim [0.696, 0.668, 0.351, 0.711]
  - track 2 at frame 338: holes 0, rim-vs-core 0.28, rim-vs-outside 0.46, heterogeneity 0.09; core [0.963, 0.895, 0.192, 0.845] rim [0.792, 0.741, 0.309, 0.736]
  - track 3 at frame 338: holes 0, rim-vs-core 0.32, rim-vs-outside 0.38, heterogeneity 0.09; core [0.943, 0.852, 0.21, 0.847] rim [0.72, 0.683, 0.327, 0.741]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 204 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 25.3 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.905)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 4.4 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.815)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.48, rim/outside 0.715 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.51)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 2.11 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.818)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3330, R_eq 4.44): none; #1 (t=3380, R_eq 4.07): none; #2 (t=3380, R_eq 4.3): none; #3 (t=3380, R_eq 4.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
