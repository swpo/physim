# Evidence pack: ad3-membrane (seed 5)

- world: `../../../../../../threads/active-droplets/worlds/ad3-membrane/world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 147s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3-membrane/world.py --out collective/contrib/20261025T2312-c23-review-ad3/rerun/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0504, 1.2296], min area 6 px

## Measurements
- components: final 18, mean 9.5, max 18; occupancy final 0.12
- tracks: 34; persistent (alive >= 50% of run): 8; longest 133 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.58 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00136/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 16, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1751, -0.6316, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 134: holes 0, rim-vs-core 0.46, rim-vs-outside 0.55, heterogeneity 0.15; core [0.973, 0.019, 0.167] rim [0.756, 0.076, 0.573]
  - track 11 at frame 134: holes 0, rim-vs-core 0.33, rim-vs-outside 0.60, heterogeneity 0.15; core [0.977, 0.03, 0.151] rim [0.828, 0.056, 0.442]
  - track 12 at frame 134: holes 0, rim-vs-core 0.47, rim-vs-outside 0.53, heterogeneity 0.15; core [0.972, 0.021, 0.157] rim [0.76, 0.076, 0.576]
  - track 22 at frame 176: holes 0, rim-vs-core 0.60, rim-vs-outside 0.34, heterogeneity 0.15; core [0.948, 0.037, 0.223] rim [0.656, 0.089, 0.748]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 63 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 34.8 (aggregate of 63 individuals; 2/63 membrane-like individually; rim level 0.83)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.63, rim/outside 0.658 (aggregate of 63 individuals; 0/63 membrane-like individually; rim level 0.154)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.1, rim/outside 9.78 (aggregate of 63 individuals; 58/63 membrane-like individually; rim level 0.605)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #10 (t=13400, R_eq 6.7): ['psi (amphiphile)']; #11 (t=13400, R_eq 6.36): ['psi (amphiphile)']; #12 (t=13400, R_eq 6.41): ['psi (amphiphile)']; #22 (t=17600, R_eq 5.97): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 63 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
