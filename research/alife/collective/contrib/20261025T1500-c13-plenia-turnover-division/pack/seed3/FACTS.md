# Evidence pack: particle-lenia-turnover (seed 3)

- world: `../../world.py`, family `particle-lenia`
- parent: collective/contrib/20261025T1300-c13-particle-lenia-vesicles/world.py; mutation: particle turnover: random feed of new particles plus decay of every particle (c13)
- run: 151 frames x 100 steps x dt 0.1 = time 1500; grid [128, 128]; wall 988s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1500-c13-plenia-turnover-division/world.py --out collective/contrib/20261025T1500-c13-plenia-turnover-division/pack --seeds 3 4 --spf 100 --frames 150 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.9377], min area 6 px

## Measurements
- components: final 63, mean 62.1, max 90; occupancy final 0.23
- tracks: 713; persistent (alive >= 50% of run): 21; longest 145 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.50 (1 = constant size)
- enclosures: components with a hole mean 21.89, final 29; holes at thresholds 0.2/0.35/0.5 final [10, 29, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [69, 61, 28], H1 [51, 5, 0]
- motion: 156 long-lived tracks moved >= 1 body length; max speed 0.249/time; max body lengths 14.6
- replication (lineage window K = 20 frames = time 200, default): splits 122, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 155, merge/split ratio 1.27, nucleations 243
- channel total drift (end/start - 1): [-0.0177, -0.0177, 1.7748]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 124 at frame 76: holes 0, rim-vs-core 0.46, rim-vs-outside 0.44, heterogeneity 0.20; core [0.75, 0.2, 0.777] rim [0.528, 0.376, 0.409]
  - track 165 at frame 82: holes 1, rim-vs-core 0.28, rim-vs-outside 0.45, heterogeneity 0.19; core [0.702, 0.241, 0.67] rim [0.546, 0.281, 0.44]
  - track 333 at frame 95: holes 1, rim-vs-core 0.25, rim-vs-outside 0.42, heterogeneity 0.19; core [0.659, 0.218, 0.747] rim [0.525, 0.272, 0.547]
  - track 301 at frame 53: holes 1, rim-vs-core 0.35, rim-vs-outside 0.41, heterogeneity 0.21; core [0.748, 0.202, 0.718] rim [0.521, 0.274, 0.457]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 368 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial particle density: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 5.39 (aggregate of 368 individuals; 213/368 membrane-like individually; rim level 0.651)  MEMBRANE-LIKE
  - radial U field: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 6.02, rim/outside 0.805 (aggregate of 368 individuals; 0/368 membrane-like individually; rim level 0.52)
  - radial G(U): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.76, rim/outside 20.5 (aggregate of 368 individuals; 231/368 membrane-like individually; rim level 0.691)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): particle density, G(U)
- membrane-like channels per top track at mid-life: #124 (t=760, R_eq 4.41): none; #165 (t=820, R_eq 4.07, ring): ['particle density', 'G(U)']; #333 (t=950, R_eq 3.95, ring): ['particle density', 'G(U)']; #301 (t=530, R_eq 4.18): ['particle density', 'G(U)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 157 of 368 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
