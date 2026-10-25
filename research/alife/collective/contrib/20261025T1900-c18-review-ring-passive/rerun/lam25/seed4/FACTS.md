# Evidence pack: lattice-chem (seed 4)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 203s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev11/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev11/lam25 --seeds 4 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 28.0], min area 6 px

## Measurements
- components: final 68, mean 79.2, max 159; occupancy final 0.15
- tracks: 699; persistent (alive >= 50% of run): 64; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [80, 68, 68], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 1000, default): splits 141, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 245, merge/split ratio 1.74, nucleations 186
- channel total drift (end/start - 1): [2.5268, None, -0.6026, 1.2573]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.07, rim-vs-outside 0.56, heterogeneity 0.15; core [0.75, 0.111, 0.033, 0.519] rim [0.703, 0.118, 0.081, 0.514]
  - track 4 at frame 101: holes 0, rim-vs-core 0.15, rim-vs-outside 0.42, heterogeneity 0.16; core [0.673, 0.068, 0.046, 0.47] rim [0.633, 0.185, 0.087, 0.541]
  - track 9 at frame 101: holes 0, rim-vs-core 0.19, rim-vs-outside 0.39, heterogeneity 0.16; core [0.69, 0.127, 0.086, 0.603] rim [0.635, 0.13, 0.058, 0.426]
  - track 28 at frame 103: holes 0, rim-vs-core 0.13, rim-vs-outside 0.35, heterogeneity 0.16; core [0.692, 0.103, 0.046, 0.513] rim [0.586, 0.156, 0.073, 0.556]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 449 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 11.4 (aggregate of 449 individuals; 15/449 membrane-like individually; rim level 0.571)
  - radial M (membrane): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 3.9, rim/outside 4.87 (aggregate of 449 individuals; 425/449 membrane-like individually; rim level 0.366)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.92, rim/outside 0.647 (aggregate of 449 individuals; 0/449 membrane-like individually; rim level 0.226)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #2 (t=5050, R_eq 2.46): ['M (membrane)']; #4 (t=5050, R_eq 2.99): ['M (membrane)']; #9 (t=5050, R_eq 2.46): ['M (membrane)']; #28 (t=5150, R_eq 2.99): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 449 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
