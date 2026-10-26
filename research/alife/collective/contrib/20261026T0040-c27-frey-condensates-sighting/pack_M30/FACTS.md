# Evidence pack: frey-condensates (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 288s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27p/world.py --out collective/contrib/wip-c27p/pack_M30 --seeds 0 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [0.01, 1.0007], min area 6 px

## Measurements
- components: final 7, mean 14.3, max 104; occupancy final 0.33
- tracks: 254; persistent (alive >= 50% of run): 6; longest 93 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.61 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.712/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 40, default): splits 36, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 89, merge/split ratio 2.47, nucleations 104
- channel total drift (end/start - 1): [0.0, -0.7493]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 193 at frame 54: holes 0, rim-vs-core 0.19, rim-vs-outside 0.62, heterogeneity 0.10; core [0.986, 0.023] rim [0.803, 0.075]
  - track 225 at frame 58: holes 0, rim-vs-core 0.18, rim-vs-outside 0.62, heterogeneity 0.09; core [0.984, 0.029] rim [0.812, 0.088]
  - track 214 at frame 52: holes 0, rim-vs-core 0.19, rim-vs-outside 0.62, heterogeneity 0.10; core [0.987, 0.034] rim [0.802, 0.093]
  - track 184 at frame 37: holes 0, rim-vs-core 0.24, rim-vs-outside 0.50, heterogeneity 0.10; core [0.98, 0.042] rim [0.744, 0.097]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 4.78 (aggregate of 64 individuals; 3/64 membrane-like individually; rim level 0.796)
  - radial substrate s: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 3.84, rim/outside 0.852 (aggregate of 64 individuals; 1/64 membrane-like individually; rim level 0.186)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #193 (t=108, R_eq 11.38): none; #225 (t=116, R_eq 12.3): none; #214 (t=104, R_eq 10.09): none; #184 (t=74, R_eq 9.56): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
