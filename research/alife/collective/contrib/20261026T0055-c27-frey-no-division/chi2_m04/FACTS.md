# Evidence pack: frey-condensates (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 292s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27r/world.py --out collective/contrib/wip-c27r/chi2_m04 --seeds 0 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0052, 1.0028], min area 6 px

## Measurements
- components: final 7, mean 12.2, max 73; occupancy final 0.28
- tracks: 261; persistent (alive >= 50% of run): 1; longest 52 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 1.15/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 40, default): splits 63, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 70, merge/split ratio 1.11, nucleations 79
- channel total drift (end/start - 1): [-0.0, -0.7589]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 235 at frame 75: holes 0, rim-vs-core 0.16, rim-vs-outside 0.55, heterogeneity 0.10; core [0.979, 0.109] rim [0.827, 0.141]
  - track 240 at frame 78: holes 0, rim-vs-core 0.17, rim-vs-outside 0.63, heterogeneity 0.10; core [0.983, 0.064] rim [0.82, 0.098]
  - track 179 at frame 35: holes 0, rim-vs-core 0.25, rim-vs-outside 0.28, heterogeneity 0.09; core [0.926, 0.155] rim [0.679, 0.176]
  - track 251 at frame 85: holes 0, rim-vs-core 0.11, rim-vs-outside 0.73, heterogeneity 0.10; core [0.979, 0.047] rim [0.87, 0.077]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 3.84 (aggregate of 50 individuals; 3/50 membrane-like individually; rim level 0.641)
  - radial substrate s: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.7, rim/outside 0.899 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.155)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #235 (t=150, R_eq 9.18): none; #240 (t=156, R_eq 12.45): none; #179 (t=70, R_eq 4.15): none; #251 (t=170, R_eq 21.34, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 50 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
