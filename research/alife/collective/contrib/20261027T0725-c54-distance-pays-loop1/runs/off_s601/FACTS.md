# Evidence pack: active-nematic-marangoni-distance-pays (seed 601)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 925s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/off/seed601 --seeds 601 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-0.9967, 0.5331], min area 6 px

## Measurements
- components: final 3, mean 5.2, max 19; occupancy final 0.01
- tracks: 40; persistent (alive >= 50% of run): 0; longest 170 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 3], H1 [2, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.0562/time; max body lengths 4.1
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 12
- channel total drift (end/start - 1): [-0.5932, -0.9193, None, -0.15, None, -0.0896]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 118: holes 0, rim-vs-core 0.46, rim-vs-outside 0.41, heterogeneity 0.08; core [0.998, 0.993, 0.0, 0.507, 0.033, 1.0] rim [0.867, 0.823, 0.0, 0.915, 0.055, 1.0]
  - track 12 at frame 101: holes 0, rim-vs-core 0.53, rim-vs-outside 0.45, heterogeneity 0.08; core [1.0, 1.0, 0.002, 0.407, 0.039, 1.0] rim [0.892, 0.84, 0.004, 0.903, 0.069, 1.0]
  - track 15 at frame 94: holes 0, rim-vs-core 0.50, rim-vs-outside 0.48, heterogeneity 0.08; core [0.999, 1.0, 0.0, 0.387, 0.058, 1.0] rim [0.89, 0.902, 0.001, 0.859, 0.106, 1.0]
  - track 38 at frame 380: holes 0, rim-vs-core 0.50, rim-vs-outside 0.42, heterogeneity 0.08; core [1.0, 1.0, 0.005, 0.497, 0.047, 0.833] rim [0.884, 0.886, 0.013, 0.966, 0.08, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 3.07 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.914)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 7.64 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.878)
  - radial s0 (mar 20): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 2.29 (aggregate of 27 individuals; 4/27 membrane-like individually; rim level 0.261)
  - radial s1 (mar 40): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.29, rim/outside 3.2 (aggregate of 27 individuals; 20/27 membrane-like individually; rim level 0.619)  MEMBRANE-LIKE
  - radial s2 (mar 60): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.88, rim/outside 2.18 (aggregate of 27 individuals; 20/27 membrane-like individually; rim level 0.21)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 1.02 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.911)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s1 (mar 40), s2 (mar 60)
- membrane-like channels per top track at mid-life: #21 (t=590, R_eq 3.48): ['s1 (mar 40)']; #12 (t=505, R_eq 2.93): ['s1 (mar 40)', 's2 (mar 60)']; #15 (t=470, R_eq 3.29): ['s1 (mar 40)', 's2 (mar 60)']; #38 (t=1900, R_eq 3.24): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
