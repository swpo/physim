# Evidence pack: active-nematic-marangoni-spread (seed 501)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1029s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/twin/seed501 --seeds 501 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0254, 0.5485], min area 6 px

## Measurements
- components: final 8, mean 10.4, max 17; occupancy final 0.03
- tracks: 86; persistent (alive >= 50% of run): 3; longest 258 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 8], H1 [1, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.311/time; max body lengths 11.0
- replication (lineage window K = 20 frames = time 100, default): splits 32, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 4, merges 13, merge/split ratio 0.406, nucleations 9
- channel total drift (end/start - 1): [-0.9065, -0.8119, None, 3.7771, None, -0.2938]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 151: holes 0, rim-vs-core 0.56, rim-vs-outside 0.33, heterogeneity 0.11; core [0.975, 0.753, 0.03, 0.426, 0.0, 1.0] rim [0.799, 0.495, 0.073, 0.889, 0.001, 1.0]
  - track 12 at frame 148: holes 0, rim-vs-core 0.55, rim-vs-outside 0.29, heterogeneity 0.09; core [0.978, 0.623, 0.024, 0.398, 0.0, 1.0] rim [0.816, 0.419, 0.059, 0.878, 0.001, 1.0]
  - track 57 at frame 289: holes 0, rim-vs-core 0.63, rim-vs-outside 0.44, heterogeneity 0.11; core [0.987, 0.983, 0.469, 0.008, 0.011, 1.0] rim [0.802, 0.692, 0.998, 0.021, 0.012, 1.0]
  - track 72 at frame 353: holes 0, rim-vs-core 0.68, rim-vs-outside 0.36, heterogeneity 0.11; core [0.973, 0.899, 0.0, 0.432, 0.021, 1.0] rim [0.791, 0.5, 0.001, 0.949, 0.052, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 65 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.84, rim/outside 2.92 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.766)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 8.64 (aggregate of 65 individuals; 8/65 membrane-like individually; rim level 0.577)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 2.79 (aggregate of 65 individuals; 14/65 membrane-like individually; rim level 0.117)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.3 (aggregate of 65 individuals; 34/65 membrane-like individually; rim level 0.512)
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 2.32 (aggregate of 65 individuals; 14/65 membrane-like individually; rim level 0.142)
  - radial chemostat target phi_b(x,t): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.962)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=755, R_eq 4.26): none; #12 (t=740, R_eq 3.91): ['s0 (mar 20)']; #57 (t=1445, R_eq 3.34): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #72 (t=1765, R_eq 3.14): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 65 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
