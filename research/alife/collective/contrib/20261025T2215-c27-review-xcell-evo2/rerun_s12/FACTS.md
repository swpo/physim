# Evidence pack: xcell-evo2-S (seed 12)

- world: `../world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm S of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Selection arm: an h-on cell adds W[c,h]=0.15 cargo production (cargo activates the body, so on-cells grow and refill space faster).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 784s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27i/world.py --out collective/contrib/wip-c27i/rerun_s12 --seeds 12 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8716], min area 6 px

## Measurements
- components: final 11, mean 11.1, max 13; occupancy final 0.12
- tracks: 28; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 12.52 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.164/time; max body lengths 17.1
- replication (lineage window K = 20 frames = time 200, default): splits 9, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.3, None, 25.6213, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.51, heterogeneity 0.15; core [0.935, 0.653, 0.089, 0.849] rim [0.588, 0.936, 0.048, 0.557]
  - track 3 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.65, heterogeneity 0.16; core [0.929, 0.575, 0.093, 0.904] rim [0.694, 0.841, 0.061, 0.64]
  - track 6 at frame 101: holes 0, rim-vs-core 0.77, rim-vs-outside 0.71, heterogeneity 0.22; core [0.934, 0.584, 0.991, 0.916] rim [0.574, 0.934, 0.509, 0.59]
  - track 22 at frame 158: holes 0, rim-vs-core 0.60, rim-vs-outside 0.88, heterogeneity 0.23; core [0.941, 0.571, 0.986, 0.917] rim [0.661, 0.86, 0.619, 0.665]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u (body): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 88.9 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.879)
  - radial m (CH membrane): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.64, rim/outside 10.3 (aggregate of 69 individuals; 68/69 membrane-like individually; rim level 0.958)  MEMBRANE-LIKE
  - radial h (marker): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 40.1 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.391)
  - radial q (waste): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 33.4 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.778)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): m (CH membrane)
- membrane-like channels per top track at mid-life: #2 (t=1010, R_eq 7.11): ['m (CH membrane)']; #3 (t=1010, R_eq 7.61): ['m (CH membrane)']; #6 (t=1010, R_eq 7.74): ['m (CH membrane)']; #22 (t=1580, R_eq 7.69): ['m (CH membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
