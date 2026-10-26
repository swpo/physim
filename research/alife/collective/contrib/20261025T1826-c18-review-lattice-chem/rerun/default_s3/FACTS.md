# Evidence pack: lattice-chem (seed 3)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 412s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev7/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev7/default --seeds 3 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 27.0], min area 6 px

## Measurements
- components: final 57, mean 67.6, max 143; occupancy final 0.16
- tracks: 510; persistent (alive >= 50% of run): 52; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [78, 60, 57], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000311/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 83, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 186, merge/split ratio 2.24, nucleations 164
- channel total drift (end/start - 1): [2.4368, None, -0.5943, 1.2585]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 101: holes 0, rim-vs-core 0.16, rim-vs-outside 0.39, heterogeneity 0.17; core [0.661, 0.119, 0.036, 0.484] rim [0.599, 0.222, 0.075, 0.389]
  - track 56 at frame 101: holes 0, rim-vs-core 0.17, rim-vs-outside 0.54, heterogeneity 0.16; core [0.719, 0.065, 0.067, 0.528] rim [0.623, 0.16, 0.083, 0.426]
  - track 59 at frame 101: holes 0, rim-vs-core 0.34, rim-vs-outside 0.34, heterogeneity 0.16; core [0.698, 0.125, 0.044, 0.674] rim [0.531, 0.215, 0.087, 0.4]
  - track 69 at frame 101: holes 0, rim-vs-core 0.17, rim-vs-outside 0.40, heterogeneity 0.16; core [0.67, 0.085, 0.069, 0.47] rim [0.527, 0.175, 0.086, 0.452]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 381 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 10.8 (aggregate of 381 individuals; 7/381 membrane-like individually; rim level 0.544)
  - radial M (membrane): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 3.45, rim/outside 5.36 (aggregate of 381 individuals; 359/381 membrane-like individually; rim level 0.357)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 3.83, rim/outside 0.695 (aggregate of 381 individuals; 1/381 membrane-like individually; rim level 0.255)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #16 (t=10100, R_eq 3.09): ['M (membrane)']; #56 (t=10100, R_eq 3.09): ['M (membrane)']; #59 (t=10100, R_eq 3.14): ['M (membrane)']; #69 (t=10100, R_eq 2.93): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 381 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
