# Evidence pack: frey-condensates (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 302s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27p/world.py --out collective/contrib/wip-c27p/pack_M30_m04 --seeds 0 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [0.0103, 1.0], min area 6 px

## Measurements
- components: final 5, mean 14.8, max 83; occupancy final 0.27
- tracks: 159; persistent (alive >= 50% of run): 7; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.97 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.811/time; max body lengths 5.9
- replication (lineage window K = 20 frames = time 40, default): splits 14, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 47, merge/split ratio 3.36, nucleations 86
- channel total drift (end/start - 1): [-0.0, -0.7236]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 105 at frame 47: holes 0, rim-vs-core 0.17, rim-vs-outside 0.64, heterogeneity 0.10; core [0.984, 0.044] rim [0.821, 0.104]
  - track 104 at frame 45: holes 0, rim-vs-core 0.19, rim-vs-outside 0.61, heterogeneity 0.10; core [0.982, 0.015] rim [0.8, 0.082]
  - track 144 at frame 65: holes 0, rim-vs-core 0.20, rim-vs-outside 0.62, heterogeneity 0.11; core [0.987, 0.029] rim [0.795, 0.089]
  - track 146 at frame 66: holes 0, rim-vs-core 0.15, rim-vs-outside 0.70, heterogeneity 0.10; core [0.984, 0.023] rim [0.84, 0.072]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 7.49 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.824)
  - radial substrate s: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 3.5, rim/outside 0.845 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.199)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #105 (t=94, R_eq 10.26): none; #104 (t=90, R_eq 11.66): none; #144 (t=130, R_eq 10.14): none; #146 (t=132, R_eq 14.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 68 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
