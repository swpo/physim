# Evidence pack: active-nematic-marangoni-distance-pays (seed 602)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 898s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/dep07/seed602 --seeds 602 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0036, 0.5449], min area 6 px

## Measurements
- components: final 4, mean 7.4, max 14; occupancy final 0.01
- tracks: 54; persistent (alive >= 50% of run): 0; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [1, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.533/time; max body lengths 9.9
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 7, merges 2, merge/split ratio 0.08, nucleations 2
- channel total drift (end/start - 1): [-0.9165, -0.9221, None, 0.3223, None, -0.3267]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 198: holes 0, rim-vs-core 0.70, rim-vs-outside 0.38, heterogeneity 0.12; core [0.989, 0.934, 0.001, 0.459, 0.059, 1.0] rim [0.815, 0.509, 0.003, 0.981, 0.153, 1.0]
  - track 32 at frame 208: holes 0, rim-vs-core 0.51, rim-vs-outside 0.45, heterogeneity 0.08; core [0.996, 0.987, 0.007, 0.337, 0.014, 1.0] rim [0.843, 0.786, 0.019, 0.776, 0.04, 1.0]
  - track 35 at frame 232: holes 0, rim-vs-core 0.62, rim-vs-outside 0.46, heterogeneity 0.09; core [0.989, 0.987, 0.403, 0.009, 0.002, 1.0] rim [0.853, 0.852, 0.992, 0.029, 0.006, 1.0]
  - track 49 at frame 366: holes 0, rim-vs-core 0.53, rim-vs-outside 0.44, heterogeneity 0.10; core [0.993, 0.994, 0.549, 0.003, 0.002, 0.833] rim [0.847, 0.758, 1.0, 0.011, 0.003, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 3.23 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.825)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 9.66 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.698)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 2.96 (aggregate of 44 individuals; 13/44 membrane-like individually; rim level 0.187)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 3.57 (aggregate of 44 individuals; 26/44 membrane-like individually; rim level 0.556)  MEMBRANE-LIKE
  - radial s2 (mar 60): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 1.86 (aggregate of 44 individuals; 14/44 membrane-like individually; rim level 0.0808)
  - radial chemostat target phi_b(x,t): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.04 (aggregate of 44 individuals; 1/44 membrane-like individually; rim level 0.946)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s1 (mar 40)
- membrane-like channels per top track at mid-life: #22 (t=990, R_eq 3.04): ['s1 (mar 40)', 's2 (mar 60)']; #32 (t=1040, R_eq 3.66): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #35 (t=1160, R_eq 3.57): ['s0 (mar 20)', 's1 (mar 40)']; #49 (t=1830, R_eq 3.04): ['s0 (mar 20)', 's1 (mar 40)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
