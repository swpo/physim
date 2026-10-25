# Evidence pack: particle-lenia-turnover (seed 4)

- world: `../../world.py`, family `particle-lenia`
- parent: collective/contrib/20261025T1300-c13-particle-lenia-vesicles/world.py; mutation: particle turnover: random feed of new particles plus decay of every particle (c13)
- run: 151 frames x 100 steps x dt 0.1 = time 1500; grid [128, 128]; wall 854s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1500-c13-plenia-turnover-division/world.py --out collective/contrib/20261025T1500-c13-plenia-turnover-division/pack --seeds 3 4 --spf 100 --frames 150 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.9415], min area 6 px

## Measurements
- components: final 62, mean 61.5, max 95; occupancy final 0.22
- tracks: 618; persistent (alive >= 50% of run): 22; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.00 (1 = constant size)
- enclosures: components with a hole mean 20.21, final 25; holes at thresholds 0.2/0.35/0.5 final [8, 25, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [67, 62, 30], H1 [54, 4, 0]
- motion: 161 long-lived tracks moved >= 1 body length; max speed 0.219/time; max body lengths 23.5
- replication (lineage window K = 20 frames = time 200, default): splits 105, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 118, merge/split ratio 1.12, nucleations 203
- channel total drift (end/start - 1): [-0.0349, -0.0349, 2.5858]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 106 at frame 76: holes 0, rim-vs-core 0.27, rim-vs-outside 0.47, heterogeneity 0.23; core [0.714, 0.148, 0.465] rim [0.547, 0.362, 0.456]
  - track 68 at frame 74: holes 1, rim-vs-core 0.26, rim-vs-outside 0.46, heterogeneity 0.20; core [0.783, 0.139, 0.663] rim [0.564, 0.205, 0.531]
  - track 159 at frame 82: holes 0, rim-vs-core 0.35, rim-vs-outside 0.16, heterogeneity 0.14; core [0.663, 0.363, 0.355] rim [0.438, 0.444, 0.103]
  - track 179 at frame 83: holes 0, rim-vs-core 0.53, rim-vs-outside 0.41, heterogeneity 0.20; core [0.794, 0.22, 0.801] rim [0.495, 0.371, 0.394]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 367 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial particle density: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 6.14 (aggregate of 367 individuals; 219/367 membrane-like individually; rim level 0.687)  MEMBRANE-LIKE
  - radial U field: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 5.95, rim/outside 0.778 (aggregate of 367 individuals; 0/367 membrane-like individually; rim level 0.516)
  - radial G(U): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.88, rim/outside 22.4 (aggregate of 367 individuals; 262/367 membrane-like individually; rim level 0.666)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): particle density, G(U)
- membrane-like channels per top track at mid-life: #106 (t=760, R_eq 5.11): ['particle density', 'G(U)']; #68 (t=740, R_eq 4.51, ring): ['particle density', 'G(U)']; #159 (t=820, R_eq 4.3): none; #179 (t=830, R_eq 4.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 134 of 367 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
