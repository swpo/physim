# Evidence pack: active-nematic-marangoni-spread (seed 510)

- world: `../../../collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 880s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py --out /home/user/physim/research/alife/c56work/sp/E --seeds 510 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0069, 0.5645], min area 6 px

## Measurements
- components: final 13, mean 13.7, max 24; occupancy final 0.04
- tracks: 150; persistent (alive >= 50% of run): 0; longest 171 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 12], H1 [0, 0, 0]
- motion: 75 long-lived tracks moved >= 1 body length; max speed 0.457/time; max body lengths 11.6
- replication (lineage window K = 20 frames = time 100, default): splits 58, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 5, merges 24, merge/split ratio 0.414, nucleations 11
- channel total drift (end/start - 1): [-0.8034, -0.7186, None, 4.2156, None, -0.216]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 66 at frame 202: holes 0, rim-vs-core 0.60, rim-vs-outside 0.34, heterogeneity 0.12; core [0.967, 0.646, 0.023, 0.435, 0.005, 1.0] rim [0.773, 0.393, 0.059, 0.941, 0.013, 1.0]
  - track 32 at frame 121: holes 0, rim-vs-core 0.59, rim-vs-outside 0.33, heterogeneity 0.11; core [0.968, 0.736, 0.008, 0.502, 0.007, 1.0] rim [0.784, 0.419, 0.02, 0.963, 0.017, 1.0]
  - track 87 at frame 266: holes 0, rim-vs-core 0.49, rim-vs-outside 0.34, heterogeneity 0.13; core [0.944, 0.627, 0.007, 0.241, 0.454, 1.0] rim [0.775, 0.418, 0.015, 0.473, 0.795, 1.0]
  - track 133 at frame 373: holes 0, rim-vs-core 0.59, rim-vs-outside 0.34, heterogeneity 0.10; core [0.964, 0.785, 0.011, 0.431, 0.01, 1.0] rim [0.771, 0.454, 0.026, 0.879, 0.021, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 2.96 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.748)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.777, rim/outside 8.46 (aggregate of 85 individuals; 5/85 membrane-like individually; rim level 0.57)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.76, rim/outside 3.09 (aggregate of 85 individuals; 29/85 membrane-like individually; rim level 0.169)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 3.26 (aggregate of 85 individuals; 47/85 membrane-like individually; rim level 0.432)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 2.75 (aggregate of 85 individuals; 31/85 membrane-like individually; rim level 0.158)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.03 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.989)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20)
- membrane-like channels per top track at mid-life: #66 (t=1010, R_eq 4.37): ['s0 (mar 20)', 's1 (mar 40)']; #32 (t=605, R_eq 3.91): ['s1 (mar 40)']; #87 (t=1330, R_eq 4.51): none; #133 (t=1865, R_eq 4.03): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
