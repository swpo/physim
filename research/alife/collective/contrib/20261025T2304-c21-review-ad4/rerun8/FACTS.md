# Evidence pack: ad4-protocell (seed 8)

- world: `../../../../threads/active-droplets/worlds/ad4-protocell/world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 220s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad4-protocell/world.py --out collective/contrib/20261025T2304-c21-review-ad4/rerun8 --seeds 8 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0637, 1.4263], min area 6 px

## Measurements
- components: final 11, mean 10.0, max 11; occupancy final 0.12
- tracks: 16; persistent (alive >= 50% of run): 11; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 2.62 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00109/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1037, -0.604, 3.4336, 0.2711, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 0.70, heterogeneity 0.13; core [0.974, 0.091, 0.0, 0.953, 0.139] rim [0.717, 0.161, 0.0, 0.617, 0.566]
  - track 3 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 0.71, heterogeneity 0.14; core [0.973, 0.091, 0.0, 0.951, 0.14] rim [0.706, 0.162, 0.0, 0.606, 0.576]
  - track 4 at frame 101: holes 0, rim-vs-core 0.63, rim-vs-outside 0.70, heterogeneity 0.14; core [0.97, 0.078, 0.0, 0.958, 0.159] rim [0.706, 0.163, 0.0, 0.614, 0.611]
  - track 12 at frame 123: holes 0, rim-vs-core 0.60, rim-vs-outside 0.70, heterogeneity 0.13; core [0.963, 0.027, 0.95, 0.0, 0.156] rim [0.72, 0.105, 0.619, 0.0, 0.588]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 63 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 59.5 (aggregate of 63 individuals; 0/63 membrane-like individually; rim level 0.922)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.33, rim/outside 0.709 (aggregate of 63 individuals; 0/63 membrane-like individually; rim level 0.216)
  - radial a (catalyst A): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 47.6 (aggregate of 63 individuals; 0/63 membrane-like individually; rim level 0.629)
  - radial b (catalyst B): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 26.1 (aggregate of 63 individuals; 0/63 membrane-like individually; rim level 0.26)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.91, rim/outside 19.1 (aggregate of 63 individuals; 61/63 membrane-like individually; rim level 0.76)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #0 (t=10100, R_eq 6.7): ['psi (amphiphile)']; #3 (t=10100, R_eq 6.75): ['psi (amphiphile)']; #4 (t=10100, R_eq 7.55): ['psi (amphiphile)']; #12 (t=12300, R_eq 7.48): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
