# Evidence pack: lattice-chem-gate (seed 1)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 323s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/world.py --out collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/slowA/seed1 --seeds 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 20.0], min area 6 px

## Measurements
- components: final 94, mean 96.9, max 138; occupancy final 0.08
- tracks: 4692; persistent (alive >= 50% of run): 0; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [157, 85, 15], H1 [57, 11, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.0106/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 1000, default): splits 493, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 508, merge/split ratio 1.03, nucleations 3241
- channel total drift (end/start - 1): [2.7423, None, -0.6763, 1.4327]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 952 at frame 74: holes 0, rim-vs-core 0.14, rim-vs-outside 0.27, heterogeneity 0.19; core [0.588, 0.286, 0.1, 0.518] rim [0.595, 0.328, 0.124, 0.382]
  - track 46 at frame 30: holes 0, rim-vs-core 0.19, rim-vs-outside 0.30, heterogeneity 0.18; core [0.597, 0.102, 0.143, 0.357] rim [0.502, 0.242, 0.085, 0.413]
  - track 2289 at frame 114: holes 0, rim-vs-core 0.34, rim-vs-outside 0.34, heterogeneity 0.17; core [0.706, 0.071, 0.1, 0.469] rim [0.488, 0.2, 0.12, 0.237]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 260 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 2.56 (aggregate of 260 individuals; 38/260 membrane-like individually; rim level 0.514)
  - radial M (membrane): peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 2.32, rim/outside 1.75 (aggregate of 260 individuals; 216/260 membrane-like individually; rim level 0.339)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.9, rim/outside 0.722 (aggregate of 260 individuals; 21/260 membrane-like individually; rim level 0.188)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #952 (t=3700, R_eq 2.76): ['M (membrane)']; #46 (t=1500, R_eq 2.52): ['A (autocatalyst)', 'M (membrane)']; #81 (t=1500, R_eq 1.87): none; #2289 (t=5700, R_eq 2.11): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 260 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
