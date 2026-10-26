# Evidence pack: xcell-evo2-S (seed 11)

- world: `../world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm S of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Selection arm: an h-on cell adds W[c,h]=0.15 cargo production (cargo activates the body, so on-cells grow and refill space faster).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 792s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27i/world.py --out collective/contrib/wip-c27i/rerun_s11 --seeds 11 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8711], min area 6 px

## Measurements
- components: final 9, mean 10.4, max 13; occupancy final 0.10
- tracks: 36; persistent (alive >= 50% of run): 7; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.02 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.231/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 200, default): splits 13, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4031, None, 26.6453, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.51, heterogeneity 0.16; core [0.944, 0.597, 0.092, 0.848] rim [0.608, 0.929, 0.049, 0.543]
  - track 15 at frame 126: holes 0, rim-vs-core 0.78, rim-vs-outside 0.68, heterogeneity 0.24; core [0.937, 0.583, 0.969, 0.913] rim [0.574, 0.932, 0.476, 0.586]
  - track 19 at frame 129: holes 0, rim-vs-core 0.75, rim-vs-outside 0.66, heterogeneity 0.23; core [0.933, 0.57, 0.963, 0.894] rim [0.578, 0.921, 0.492, 0.587]
  - track 20 at frame 136: holes 0, rim-vs-core 0.58, rim-vs-outside 0.50, heterogeneity 0.16; core [0.931, 0.607, 0.09, 0.808] rim [0.563, 0.936, 0.046, 0.515]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u (body): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 84.7 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.87)
  - radial m (CH membrane): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.64, rim/outside 10.2 (aggregate of 59 individuals; 58/59 membrane-like individually; rim level 0.944)  MEMBRANE-LIKE
  - radial h (marker): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 34.4 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.335)
  - radial q (waste): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 31.4 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.782)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): m (CH membrane)
- membrane-like channels per top track at mid-life: #4 (t=1010, R_eq 7.57): ['m (CH membrane)']; #15 (t=1260, R_eq 7.78): ['m (CH membrane)']; #19 (t=1290, R_eq 7.69): ['m (CH membrane)']; #20 (t=1360, R_eq 7.63): ['m (CH membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
