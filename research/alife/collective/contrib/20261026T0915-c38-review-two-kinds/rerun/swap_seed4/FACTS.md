# Evidence pack: active-nematic-marangoni-two-kinds (seed 4)

- world: `../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 664s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/20261026T0915-c38-review-two-kinds/rerun/swap_seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8378, 0.6843], min area 6 px

## Measurements
- components: final 31, mean 24.8, max 33; occupancy final 0.09
- tracks: 99; persistent (alive >= 50% of run): 15; longest 190 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.259/time; max body lengths 6.8
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.316, nucleations 11
- channel total drift (end/start - 1): [-0.5085, -0.3585, 7.7912, 10.2231]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 106: holes 0, rim-vs-core 0.61, rim-vs-outside 0.31, heterogeneity 0.15; core [0.927, 0.627, 0.017, 0.46] rim [0.728, 0.38, 0.043, 0.979]
  - track 21 at frame 118: holes 0, rim-vs-core 0.58, rim-vs-outside 0.33, heterogeneity 0.14; core [0.94, 0.834, 0.345, 0.021] rim [0.722, 0.552, 0.804, 0.057]
  - track 23 at frame 119: holes 0, rim-vs-core 0.67, rim-vs-outside 0.35, heterogeneity 0.18; core [0.964, 0.829, 0.296, 0.027] rim [0.736, 0.537, 0.852, 0.091]
  - track 53 at frame 146: holes 0, rim-vs-core 0.60, rim-vs-outside 0.38, heterogeneity 0.15; core [0.952, 0.846, 0.021, 0.288] rim [0.762, 0.529, 0.069, 0.754]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 165 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 5.14 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.737)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.738, rim/outside 9.64 (aggregate of 165 individuals; 1/165 membrane-like individually; rim level 0.584)
  - radial surfactant A: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 3.1 (aggregate of 165 individuals; 122/165 membrane-like individually; rim level 0.303)  MEMBRANE-LIKE
  - radial surfactant B: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 3.3 (aggregate of 165 individuals; 107/165 membrane-like individually; rim level 0.338)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant A
- membrane-like channels per top track at mid-life: #3 (t=530, R_eq 4.37): none; #21 (t=590, R_eq 4.07): ['surfactant A', 'surfactant B']; #23 (t=595, R_eq 3.87): ['surfactant A', 'surfactant B']; #53 (t=730, R_eq 3.24): ['surfactant A', 'surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
