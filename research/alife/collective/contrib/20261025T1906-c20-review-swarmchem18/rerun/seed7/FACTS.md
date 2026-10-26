# Evidence pack: swarmchem-23 (seed 7)

- world: `../world.py`, family `swarm-chemistry`
- parent: new class (Sayama 2009 Swarm Chemistry); mutation: none; recipe from a random screen
- run: 151 frames x 20 steps x dt 1.0 = time 3000; grid [128, 128]; wall 902s; status ok
- command: `python -m labkit.run /tmp/c20sw/world.py --out /tmp/c20sw/pack --seeds 7 --frames 150 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.1994], min area 6 px

## Measurements
- components: final 15, mean 12.9, max 46; occupancy final 0.15
- tracks: 1655; persistent (alive >= 50% of run): 0; longest 5 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.43, final 1; holes at thresholds 0.2/0.35/0.5 final [5, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 12, 4], H1 [12, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 400, default): splits 350, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 292, merge/split ratio 0.834, nucleations 612
- channel total drift (end/start - 1): [0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 197 at frame 16: holes 0, rim-vs-core 0.11, rim-vs-outside 0.17, heterogeneity 0.11; core [0.568, 0.085, 0.159] rim [0.497, 0.172, 0.156]
  - track 313 at frame 29: holes 0, rim-vs-core 0.26, rim-vs-outside 0.19, heterogeneity 0.10; core [0.735, 0.091, 0.014] rim [0.492, 0.18, 0.033]
  - track 524 at frame 48: holes 0, rim-vs-core 0.22, rim-vs-outside 0.42, heterogeneity 0.14; core [0.811, 0.022, 0.092] rim [0.605, 0.087, 0.152]
  - track 131 at frame 10: holes 0, rim-vs-core 0.21, rim-vs-outside 0.20, heterogeneity 0.10; core [0.694, 0.064, 0.024] rim [0.505, 0.14, 0.073]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 73 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial species 0 density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 3.05 (aggregate of 73 individuals; 5/73 membrane-like individually; rim level 0.518)
  - radial species 1 density: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 2.96, rim/outside 0.966 (aggregate of 73 individuals; 11/73 membrane-like individually; rim level 0.267)
  - radial species 2 density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.04 (aggregate of 73 individuals; 11/73 membrane-like individually; rim level 0.219)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #197 (t=320, R_eq 3.7): none; #313 (t=580, R_eq 4.48): ['species 2 density']; #524 (t=960, R_eq 9.46, ring): ['species 0 density', 'species 1 density']; #131 (t=200, R_eq 3.48): none

## Warnings
- radial: 12 of 73 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
