# Evidence pack: active-nematic-marangoni-spread (seed 500)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 753s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/C/seed500 --seeds 500 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0, 0.5524], min area 6 px

## Measurements
- components: final 1, mean 10.2, max 18; occupancy final 0.00
- tracks: 120; persistent (alive >= 50% of run): 1; longest 225 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.42 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [2, 0, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.389/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 100, default): splits 48, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 5, merges 16, merge/split ratio 0.333, nucleations 8
- channel total drift (end/start - 1): [-0.8339, -0.9688, None, -0.9059, None, -0.2133]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 249: holes 0, rim-vs-core 0.57, rim-vs-outside 0.31, heterogeneity 0.11; core [0.963, 0.673, 0.056, 0.51, 0.002, 1.0] rim [0.783, 0.411, 0.135, 0.978, 0.005, 1.0]
  - track 83 at frame 306: holes 0, rim-vs-core 0.54, rim-vs-outside 0.36, heterogeneity 0.10; core [0.965, 0.796, 0.0, 0.465, 0.005, 1.0] rim [0.795, 0.549, 0.001, 0.911, 0.011, 1.0]
  - track 12 at frame 84: holes 0, rim-vs-core 0.44, rim-vs-outside 0.34, heterogeneity 0.11; core [0.976, 0.716, 0.665, 0.024, 0.005, 1.0] rim [0.789, 0.511, 1.0, 0.064, 0.013, 1.0]
  - track 92 at frame 323: holes 0, rim-vs-core 0.61, rim-vs-outside 0.31, heterogeneity 0.11; core [0.976, 0.662, 0.0, 0.421, 0.034, 1.0] rim [0.797, 0.428, 0.0, 0.948, 0.092, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 2.93 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.741)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 8.67 (aggregate of 61 individuals; 4/61 membrane-like individually; rim level 0.597)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 2.35 (aggregate of 61 individuals; 11/61 membrane-like individually; rim level 0.0641)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.23 (aggregate of 61 individuals; 26/61 membrane-like individually; rim level 0.565)
  - radial s2 (mar 60): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 1.55 (aggregate of 61 individuals; 3/61 membrane-like individually; rim level 0.0478)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=1245, R_eq 4.51): none; #83 (t=1530, R_eq 4.85): none; #12 (t=420, R_eq 4.26): none; #92 (t=1615, R_eq 4.33): ['order |Q|', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 61 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
