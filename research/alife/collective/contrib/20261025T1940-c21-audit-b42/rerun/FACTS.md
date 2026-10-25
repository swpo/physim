# Evidence pack: pcell-mwall-b42 (seed 10)

- world: `../../20261025T1430-c14-pcell-mwall-b42-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 513s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1430-c14-pcell-mwall-b42-claim/world.py --out collective/contrib/20261025T1940-c21-audit-b42/rerun --seeds 10 --threshold 0.35 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 1.6747], min area 6 px

## Measurements
- components: final 30, mean 31.0, max 40; occupancy final 0.38
- tracks: 63; persistent (alive >= 50% of run): 30; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.10 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 9, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 30], H1 [19, 11, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000386/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 10000, default): splits 10, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4617, -0.6927, 0.0662, 0.0353, -0.6513, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 1.10, rim-vs-outside 0.43, heterogeneity 0.26; core [0.309, 0.436, 0.785, 0.813, 0.786, 0.754] rim [0.505, 0.056, 0.275, 0.318, 0.183, 0.358]
  - track 6 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 0.94, heterogeneity 0.25; core [0.145, 0.576, 0.688, 0.631, 0.882, 0.463] rim [0.413, 0.117, 0.404, 0.532, 0.555, 0.465]
  - track 7 at frame 101: holes 0, rim-vs-core 1.16, rim-vs-outside 0.42, heterogeneity 0.27; core [0.345, 0.481, 0.849, 0.815, 0.733, 0.862] rim [0.522, 0.068, 0.259, 0.267, 0.244, 0.353]
  - track 55 at frame 168: holes 0, rim-vs-core 0.77, rim-vs-outside 1.20, heterogeneity 0.26; core [0.066, 0.595, 0.537, 0.319, 0.988, 0.226] rim [0.327, 0.166, 0.535, 0.687, 0.66, 0.538]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 185 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 6.42, rim/outside 0.935 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.602)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 12.9 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.396)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 15.2 (aggregate of 185 individuals; 105/185 membrane-like individually; rim level 0.809)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.46, rim/outside 13.5 (aggregate of 185 individuals; 159/185 membrane-like individually; rim level 0.839)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 14.4 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.845)
  - radial M wall material: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.84, rim/outside 14.2 (aggregate of 185 individuals; 163/185 membrane-like individually; rim level 0.737)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #5 (t=50500, R_eq 5.01): ['M wall material']; #6 (t=50500, R_eq 7.46): ['L link', 'membrane (wall)', 'M wall material']; #7 (t=50500, R_eq 4.3): none; #55 (t=84000, R_eq 11.04): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
