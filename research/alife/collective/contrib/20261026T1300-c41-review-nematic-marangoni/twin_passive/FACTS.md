# Evidence pack: active-nematic-marangoni (seed 31)

- world: `../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 488s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T1300-c41-review-nematic-marangoni/twin_passive --seeds 31 --frames 200 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.8285, 0.9417], min area 6 px

## Measurements
- components: final 7, mean 6.5, max 7; occupancy final 0.06
- tracks: 7; persistent (alive >= 50% of run): 7; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 7
- channel total drift (end/start - 1): [-0.4988, -0.2393, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 106: holes 0, rim-vs-core 0.60, rim-vs-outside 0.60, heterogeneity 0.25; core [0.968, 0.941, 0.059, 0.321] rim [0.715, 0.593, 0.404, 0.078]
  - track 1 at frame 106: holes 0, rim-vs-core 0.76, rim-vs-outside 0.58, heterogeneity 0.26; core [0.966, 0.933, 0.056, 0.369] rim [0.692, 0.564, 0.554, 0.024]
  - track 2 at frame 106: holes 0, rim-vs-core 0.79, rim-vs-outside 0.57, heterogeneity 0.27; core [0.964, 0.93, 0.058, 0.371] rim [0.689, 0.56, 0.6, 0.022]
  - track 3 at frame 106: holes 0, rim-vs-core 0.84, rim-vs-outside 0.57, heterogeneity 0.27; core [0.964, 0.929, 0.061, 0.375] rim [0.682, 0.553, 0.65, 0.014]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 41 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 35.3 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.911)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 60.2 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.831)
  - radial surfactant s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 11.2, rim/outside 20.3 (aggregate of 41 individuals; 41/41 membrane-like individually; rim level 0.739)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.96, rim/outside 44.7 (aggregate of 41 individuals; 34/41 membrane-like individually; rim level 0.561)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s, cargo c
- membrane-like channels per top track at mid-life: #0 (t=530, R_eq 6.48): ['surfactant s', 'cargo c']; #1 (t=530, R_eq 6.28): ['surfactant s', 'cargo c']; #2 (t=530, R_eq 6.21): ['surfactant s', 'cargo c']; #3 (t=530, R_eq 6.26): ['surfactant s', 'cargo c']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
