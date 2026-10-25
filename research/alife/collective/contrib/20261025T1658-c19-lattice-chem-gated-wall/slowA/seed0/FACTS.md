# Evidence pack: lattice-chem-gate (seed 0)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 321s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/world.py --out collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/slowA/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 20.0], min area 6 px

## Measurements
- components: final 90, mean 96.3, max 141; occupancy final 0.06
- tracks: 4585; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [154, 97, 22], H1 [66, 17, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.00653/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 1000, default): splits 451, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 469, merge/split ratio 1.04, nucleations 3252
- channel total drift (end/start - 1): [2.618, None, -0.6705, 1.4232]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2371 at frame 133: holes 0, rim-vs-core 0.38, rim-vs-outside 0.33, heterogeneity 0.16; core [0.784, 0.095, 0.1, 0.708] rim [0.536, 0.252, 0.147, 0.478]
  - track 2380 at frame 133: holes 0, rim-vs-core 0.27, rim-vs-outside 0.24, heterogeneity 0.18; core [0.51, 0.095, 0.1, 0.5] rim [0.565, 0.243, 0.21, 0.312]
  - track 1878 at frame 104: holes 0, rim-vs-core 0.23, rim-vs-outside 0.25, heterogeneity 0.18; core [0.632, 0.143, 0.125, 0.312] rim [0.569, 0.286, 0.178, 0.472]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 243 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 2.58 (aggregate of 243 individuals; 35/243 membrane-like individually; rim level 0.51)
  - radial M (membrane): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 2.27, rim/outside 1.82 (aggregate of 243 individuals; 215/243 membrane-like individually; rim level 0.347)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.68, rim/outside 0.729 (aggregate of 243 individuals; 17/243 membrane-like individually; rim level 0.192)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #2371 (t=6650, R_eq 2.52): none; #2380 (t=6650, R_eq 2.03): ['M (membrane)']; #3053 (t=8150, R_eq 1.78): ['M (membrane)']; #1878 (t=5200, R_eq 2.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 243 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
