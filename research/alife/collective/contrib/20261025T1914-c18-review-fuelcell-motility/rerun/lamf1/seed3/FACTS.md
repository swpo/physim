# Evidence pack: nematic-fuelcell (seed 3)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 355s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev12/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev12/lamf1 --seeds 3 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8539, 0.6818], min area 6 px

## Measurements
- components: final 25, mean 12.6, max 26; occupancy final 0.09
- tracks: 49; persistent (alive >= 50% of run): 8; longest 140 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 26, 25], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0479/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 5, merges 2, merge/split ratio 0.1, nucleations 6
- channel total drift (end/start - 1): [-0.5034, -0.0941, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 139: holes 0, rim-vs-core 0.45, rim-vs-outside 0.39, heterogeneity 0.14; core [0.919, 0.712, 0.518, 0.77] rim [0.734, 0.531, 0.846, 0.613]
  - track 9 at frame 139: holes 0, rim-vs-core 0.61, rim-vs-outside 0.45, heterogeneity 0.16; core [0.968, 0.964, 0.371, 0.69] rim [0.732, 0.656, 0.823, 0.569]
  - track 42 at frame 183: holes 0, rim-vs-core 0.40, rim-vs-outside 0.51, heterogeneity 0.16; core [0.944, 0.916, 0.421, 0.696] rim [0.783, 0.714, 0.71, 0.591]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 3.98 (aggregate of 89 individuals; 8/89 membrane-like individually; rim level 0.638)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.84, rim/outside 6.07 (aggregate of 89 individuals; 8/89 membrane-like individually; rim level 0.547)
  - radial shell s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 2.18 (aggregate of 89 individuals; 42/89 membrane-like individually; rim level 0.574)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 2.5 (aggregate of 89 individuals; 8/89 membrane-like individually; rim level 0.548)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=430, R_eq 6.21, ring): none; #8 (t=695, R_eq 4.82): none; #9 (t=695, R_eq 3.66): ['shell s']; #42 (t=915, R_eq 3.83): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
