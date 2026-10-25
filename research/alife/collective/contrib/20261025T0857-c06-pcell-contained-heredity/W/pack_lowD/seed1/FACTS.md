# Evidence pack: pcell-multilevel-nogate-lowD (seed 1)

- world: `../../world_lowD.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 125 steps x dt 1.0 = time 20000; grid [128, 128]; wall 87s; status ok
- command: `python -m labkit.run collective/work/pcell/W/world_lowD.py --out collective/work/pcell/W/pack_lowD --seeds 0 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5588], min area 6 px

## Measurements
- components: final 4, mean 10.3, max 26; occupancy final 0.22
- tracks: 70; persistent (alive >= 50% of run): 7; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.73 (1 = constant size)
- enclosures: components with a hole mean 8.10, final 3; holes at thresholds 0.2/0.35/0.5 final [27, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 4, 4], H1 [13, 4, 2]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00552/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2500, default): splits 19, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.158, nucleations 2
- channel total drift (end/start - 1): [-0.7709, -0.4025, 0.8224, -0.2876, 0.0159]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 83: holes 1, rim-vs-core 0.12, rim-vs-outside 0.81, heterogeneity 0.19; core [0.232, 0.455, 0.545, 0.493, 0.758] rim [0.256, 0.434, 0.58, 0.599, 0.732]
  - track 34 at frame 67: holes 1, rim-vs-core 0.23, rim-vs-outside 0.83, heterogeneity 0.19; core [0.202, 0.664, 0.678, 0.583, 0.762] rim [0.27, 0.451, 0.62, 0.602, 0.735]
  - track 44 at frame 97: holes 0, rim-vs-core 0.28, rim-vs-outside 0.97, heterogeneity 0.18; core [0.214, 0.565, 0.634, 0.65, 0.836] rim [0.318, 0.308, 0.609, 0.695, 0.804]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 2.68, rim/outside 0.881 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.434)
  - radial K particles: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.991, rim/outside 3.49 (aggregate of 59 individuals; 3/59 membrane-like individually; rim level 0.511)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 2.48 (aggregate of 59 individuals; 28/59 membrane-like individually; rim level 0.537)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.1, rim/outside 2.4 (aggregate of 59 individuals; 48/59 membrane-like individually; rim level 0.464)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 2.87 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.752)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #38 (t=10375, R_eq 15.48, ring): ['membrane (wall)']; #34 (t=8375, R_eq 13.74, ring): ['membrane (wall)']; #44 (t=12125, R_eq 8.78): ['membrane (wall)']; #53 (t=13000, R_eq 19.35, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 47 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
