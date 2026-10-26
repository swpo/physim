# Evidence pack: ad3-membrane (seed 3)

- world: `../../world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 146s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0501-c32-review-ad3/world.py --out collective/contrib/20261026T0501-c32-review-ad3/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0503, 1.2277], min area 6 px

## Measurements
- components: final 16, mean 10.3, max 16; occupancy final 0.12
- tracks: 30; persistent (alive >= 50% of run): 8; longest 134 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.37 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00226/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1718, -0.6257, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 134: holes 0, rim-vs-core 0.40, rim-vs-outside 0.57, heterogeneity 0.15; core [0.98, 0.015, 0.164] rim [0.79, 0.069, 0.512]
  - track 13 at frame 134: holes 0, rim-vs-core 0.46, rim-vs-outside 0.55, heterogeneity 0.15; core [0.979, 0.019, 0.165] rim [0.765, 0.074, 0.572]
  - track 14 at frame 134: holes 0, rim-vs-core 0.48, rim-vs-outside 0.54, heterogeneity 0.15; core [0.979, 0.02, 0.164] rim [0.753, 0.076, 0.582]
  - track 22 at frame 166: holes 0, rim-vs-core 0.62, rim-vs-outside 0.35, heterogeneity 0.15; core [0.944, 0.039, 0.223] rim [0.64, 0.088, 0.759]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 26.6 (aggregate of 74 individuals; 2/74 membrane-like individually; rim level 0.907)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.24, rim/outside 0.682 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.154)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.74, rim/outside 10.8 (aggregate of 74 individuals; 68/74 membrane-like individually; rim level 0.743)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #12 (t=13400, R_eq 6.31): ['psi (amphiphile)']; #13 (t=13400, R_eq 6.31): ['psi (amphiphile)']; #14 (t=13400, R_eq 6.33): ['psi (amphiphile)']; #22 (t=16600, R_eq 5.75): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
