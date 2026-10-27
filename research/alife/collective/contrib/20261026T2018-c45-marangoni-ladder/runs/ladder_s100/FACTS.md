# Evidence pack: active-nematic-marangoni-ladder (seed 100)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 849s; status ok
- command: `python -m labkit.run /tmp/claude-0/ld/world.py --out /tmp/claude-0/ld/runs/ladder/seed100 --seeds 100 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8302, 0.6191], min area 6 px

## Measurements
- components: final 17, mean 20.6, max 27; occupancy final 0.07
- tracks: 296; persistent (alive >= 50% of run): 0; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 19, 16], H1 [0, 0, 0]
- motion: 135 long-lived tracks moved >= 1 body length; max speed 0.395/time; max body lengths 11.5
- replication (lineage window K = 20 frames = time 100, default): splits 125, persistent splits 49 (0 more failed only because the siblings re-merged within K), max generation 7, merges 29, merge/split ratio 0.232, nucleations 14
- channel total drift (end/start - 1): [-0.5173, -0.5723, 2.0982, 5.4432, 3.3195]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 95 at frame 229: holes 0, rim-vs-core 0.63, rim-vs-outside 0.40, heterogeneity 0.13; core [0.954, 0.92, 0.355, 0.033, 0.011] rim [0.744, 0.597, 0.847, 0.096, 0.031]
  - track 56 at frame 145: holes 0, rim-vs-core 0.70, rim-vs-outside 0.44, heterogeneity 0.14; core [0.974, 0.945, 0.368, 0.008, 0.006] rim [0.76, 0.665, 0.976, 0.02, 0.02]
  - track 122 at frame 239: holes 0, rim-vs-core 0.77, rim-vs-outside 0.41, heterogeneity 0.15; core [0.987, 0.948, 0.277, 0.03, 0.014] rim [0.783, 0.646, 0.95, 0.098, 0.04]
  - track 273 at frame 390: holes 0, rim-vs-core 0.55, rim-vs-outside 0.32, heterogeneity 0.11; core [0.935, 0.87, 0.002, 0.455, 0.014] rim [0.755, 0.563, 0.003, 0.87, 0.031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 4.13 (aggregate of 129 individuals; 3/129 membrane-like individually; rim level 0.681)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 7.58 (aggregate of 129 individuals; 12/129 membrane-like individually; rim level 0.511)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 2.86 (aggregate of 129 individuals; 38/129 membrane-like individually; rim level 0.208)
  - radial s1 (mar 40): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 2.74 (aggregate of 129 individuals; 23/129 membrane-like individually; rim level 0.182)
  - radial s2 (mar 60): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 2.92 (aggregate of 129 individuals; 41/129 membrane-like individually; rim level 0.267)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #95 (t=1145, R_eq 3.39): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #56 (t=725, R_eq 4.75): none; #122 (t=1195, R_eq 4.22): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #273 (t=1950, R_eq 3.39): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
