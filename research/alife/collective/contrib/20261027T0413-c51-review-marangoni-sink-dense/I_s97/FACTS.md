# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 97)

- world: `../../20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 453s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out collective/contrib/20261027T0413-c51-review-marangoni-sink-dense/I_s97 --seeds 97 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.009, 0.5413], min area 6 px

## Measurements
- components: final 8, mean 7.6, max 14; occupancy final 0.02
- tracks: 71; persistent (alive >= 50% of run): 0; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.46/time; max body lengths 8.2
- replication (lineage window K = 20 frames = time 100, default): splits 28, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 7, merges 3, merge/split ratio 0.107, nucleations 12
- channel total drift (end/start - 1): [-0.8546, -0.8497, None, -0.076]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 126: holes 0, rim-vs-core 0.56, rim-vs-outside 0.45, heterogeneity 0.13; core [0.991, 0.964, 0.313, 1.0] rim [0.844, 0.722, 0.798, 1.0]
  - track 38 at frame 148: holes 0, rim-vs-core 0.56, rim-vs-outside 0.30, heterogeneity 0.12; core [0.992, 0.661, 0.324, 1.0] rim [0.835, 0.42, 0.801, 1.0]
  - track 44 at frame 161: holes 0, rim-vs-core 0.62, rim-vs-outside 0.33, heterogeneity 0.15; core [0.983, 0.884, 0.445, 1.0] rim [0.814, 0.552, 0.937, 1.0]
  - track 65 at frame 293: holes 0, rim-vs-core 0.52, rim-vs-outside 0.42, heterogeneity 0.13; core [0.984, 0.958, 0.434, 1.0] rim [0.825, 0.726, 0.874, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 2.86 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.771)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 8.13 (aggregate of 45 individuals; 1/45 membrane-like individually; rim level 0.629)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.29 (aggregate of 45 individuals; 24/45 membrane-like individually; rim level 0.646)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=630, R_eq 3.34): ['surfactant s']; #38 (t=740, R_eq 2.39): ['surfactant s']; #44 (t=805, R_eq 3.95): ['surfactant s']; #65 (t=1465, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
