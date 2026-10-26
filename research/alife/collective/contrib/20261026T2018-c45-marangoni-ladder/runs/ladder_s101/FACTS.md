# Evidence pack: active-nematic-marangoni-ladder (seed 101)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 857s; status ok
- command: `python -m labkit.run /tmp/claude-0/ld/world.py --out /tmp/claude-0/ld/runs/ladder/seed101 --seeds 101 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8279, 0.5901], min area 6 px

## Measurements
- components: final 20, mean 19.9, max 29; occupancy final 0.07
- tracks: 262; persistent (alive >= 50% of run): 0; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 21, 20], H1 [0, 0, 0]
- motion: 131 long-lived tracks moved >= 1 body length; max speed 0.395/time; max body lengths 8.2
- replication (lineage window K = 20 frames = time 100, default): splits 116, persistent splits 60 (0 more failed only because the siblings re-merged within K), max generation 9, merges 20, merge/split ratio 0.172, nucleations 8
- channel total drift (end/start - 1): [-0.4916, -0.5663, -0.918, 7.6273, 3.6732]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 109 at frame 262: holes 0, rim-vs-core 0.24, rim-vs-outside 0.53, heterogeneity 0.13; core [0.936, 0.75, 0.528, 0.042, 0.007] rim [0.839, 0.612, 0.698, 0.064, 0.009]
  - track 147 at frame 303: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.10; core [0.911, 0.46, 0.002, 0.557, 0.006] rim [0.754, 0.347, 0.004, 0.908, 0.011]
  - track 99 at frame 242: holes 0, rim-vs-core 0.69, rim-vs-outside 0.50, heterogeneity 0.15; core [0.986, 0.985, 0.384, 0.02, 0.022] rim [0.772, 0.756, 1.0, 0.08, 0.053]
  - track 203 at frame 346: holes 0, rim-vs-core 0.58, rim-vs-outside 0.42, heterogeneity 0.12; core [0.961, 0.94, 0.339, 0.02, 0.007] rim [0.764, 0.676, 0.813, 0.055, 0.017]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 4.29 (aggregate of 135 individuals; 3/135 membrane-like individually; rim level 0.685)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 8.23 (aggregate of 135 individuals; 10/135 membrane-like individually; rim level 0.533)
  - radial s0 (mar 20): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 2.6 (aggregate of 135 individuals; 26/135 membrane-like individually; rim level 0.109)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.04 (aggregate of 135 individuals; 50/135 membrane-like individually; rim level 0.447)
  - radial s2 (mar 60): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 2.67 (aggregate of 135 individuals; 15/135 membrane-like individually; rim level 0.0953)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #109 (t=1310, R_eq 4.11): ['s0 (mar 20)', 's1 (mar 40)']; #147 (t=1515, R_eq 4.95): ['order |Q|']; #99 (t=1210, R_eq 4.51): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #203 (t=1730, R_eq 3.74): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 135 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
