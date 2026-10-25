# Evidence pack: nematic-fuelcell (seed 3)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 368s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev12/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev12/base --seeds 3 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8598, 0.6408], min area 6 px

## Measurements
- components: final 26, mean 11.9, max 26; occupancy final 0.09
- tracks: 60; persistent (alive >= 50% of run): 7; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 26, 25], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.056/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.16, nucleations 6
- channel total drift (end/start - 1): [-0.5034, -0.1688, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 94: holes 0, rim-vs-core 0.41, rim-vs-outside 0.72, heterogeneity 0.15; core [0.946, 0.767, 0.413, 0.843] rim [0.81, 0.572, 0.731, 0.729]
  - track 4 at frame 94: holes 0, rim-vs-core 0.35, rim-vs-outside 0.70, heterogeneity 0.14; core [0.928, 0.74, 0.458, 0.861] rim [0.81, 0.627, 0.716, 0.698]
  - track 11 at frame 141: holes 0, rim-vs-core 0.53, rim-vs-outside 0.42, heterogeneity 0.16; core [0.943, 0.87, 0.455, 0.781] rim [0.736, 0.596, 0.826, 0.625]
  - track 20 at frame 170: holes 0, rim-vs-core 0.56, rim-vs-outside 0.42, heterogeneity 0.16; core [0.946, 0.93, 0.42, 0.757] rim [0.729, 0.63, 0.809, 0.608]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 3.69 (aggregate of 80 individuals; 8/80 membrane-like individually; rim level 0.595)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 5.96 (aggregate of 80 individuals; 9/80 membrane-like individually; rim level 0.517)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 2.09 (aggregate of 80 individuals; 43/80 membrane-like individually; rim level 0.547)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 2.41 (aggregate of 80 individuals; 8/80 membrane-like individually; rim level 0.503)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=470, R_eq 7.9, ring): ['phi (droplet)', 'shell s', 'fuel f']; #4 (t=470, R_eq 6.72): none; #11 (t=705, R_eq 4.41): none; #20 (t=850, R_eq 3.91): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
