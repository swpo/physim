# Evidence pack: frey-condensates (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 290s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27p/world.py --out collective/contrib/wip-c27p/pack_M10 --seeds 0 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.48 of robust range [0.0416, 0.9928], min area 6 px

## Measurements
- components: final 14, mean 27.0, max 120; occupancy final 0.31
- tracks: 234; persistent (alive >= 50% of run): 16; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.375/time; max body lengths 5.1
- replication (lineage window K = 20 frames = time 40, default): splits 16, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 86, merge/split ratio 5.38, nucleations 120
- channel total drift (end/start - 1): [0.0, -0.7315]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 50: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.09; core [0.977, 0.008] rim [0.734, 0.052]
  - track 152 at frame 53: holes 0, rim-vs-core 0.19, rim-vs-outside 0.64, heterogeneity 0.08; core [0.988, 0.003] rim [0.806, 0.045]
  - track 193 at frame 55: holes 0, rim-vs-core 0.26, rim-vs-outside 0.50, heterogeneity 0.10; core [0.979, 0.01] rim [0.719, 0.058]
  - track 200 at frame 55: holes 0, rim-vs-core 0.20, rim-vs-outside 0.63, heterogeneity 0.08; core [0.986, 0.002] rim [0.793, 0.043]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 9.18 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.885)
  - radial substrate s: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.51, rim/outside 0.839 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.211)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=100, R_eq 6.15): none; #152 (t=106, R_eq 10.12): none; #193 (t=110, R_eq 7.14): none; #200 (t=110, R_eq 11.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
