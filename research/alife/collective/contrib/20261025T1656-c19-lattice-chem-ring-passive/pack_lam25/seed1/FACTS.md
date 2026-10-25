# Evidence pack: lattice-chem (seed 1)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 283s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py --out (c19 run of research/alife/collective/contrib/20261025T1518-c19-lattice-chem-sighting/world.py) --seeds 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 28.0], min area 6 px

## Measurements
- components: final 57, mean 71.3, max 146; occupancy final 0.16
- tracks: 866; persistent (alive >= 50% of run): 52; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [78, 59, 56], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 1000, default): splits 202, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 302, merge/split ratio 1.5, nucleations 170
- channel total drift (end/start - 1): [2.4926, None, -0.5949, 1.2263]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 101: holes 0, rim-vs-core 0.18, rim-vs-outside 0.39, heterogeneity 0.17; core [0.712, 0.111, 0.035, 0.479] rim [0.586, 0.222, 0.084, 0.508]
  - track 24 at frame 103: holes 0, rim-vs-core 0.21, rim-vs-outside 0.45, heterogeneity 0.14; core [0.72, 0.081, 0.017, 0.556] rim [0.574, 0.111, 0.077, 0.427]
  - track 25 at frame 103: holes 0, rim-vs-core 0.37, rim-vs-outside 0.45, heterogeneity 0.19; core [0.849, 0.06, 0.021, 0.487] rim [0.561, 0.252, 0.073, 0.363]
  - track 69 at frame 103: holes 0, rim-vs-core 0.14, rim-vs-outside 0.45, heterogeneity 0.16; core [0.698, 0.083, 0.053, 0.463] rim [0.628, 0.185, 0.109, 0.452]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 397 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 9.69 (aggregate of 397 individuals; 16/397 membrane-like individually; rim level 0.551)
  - radial M (membrane): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 3.11, rim/outside 4.43 (aggregate of 397 individuals; 360/397 membrane-like individually; rim level 0.346)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 3.19, rim/outside 0.674 (aggregate of 397 individuals; 0/397 membrane-like individually; rim level 0.213)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #8 (t=5050, R_eq 2.93): ['M (membrane)']; #24 (t=5150, R_eq 2.76): ['M (membrane)']; #25 (t=5150, R_eq 2.99): ['M (membrane)']; #69 (t=5150, R_eq 2.93): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 397 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
