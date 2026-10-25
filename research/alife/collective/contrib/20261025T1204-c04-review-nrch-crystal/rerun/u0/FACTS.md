# Evidence pack: nrch (seed 4)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1054-c08-nrch-chemostat-crystal/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 657s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1054-c08-nrch-chemostat-crystal/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev17/u0 --seeds 4 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0509, 1.09], min area 6 px

## Measurements
- components: final 5, mean 7.4, max 34; occupancy final 0.27
- tracks: 214; persistent (alive >= 50% of run): 4; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.03 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.189/time; max body lengths 12.0
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 55, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 64, merge/split ratio 1.16, nucleations 51
- channel total drift (end/start - 1): [0.0, -63.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 205 at frame 167: holes 0, rim-vs-core 0.22, rim-vs-outside 0.53, heterogeneity 0.17; core [0.94, 0.379] rim [0.726, 0.353]
  - track 206 at frame 167: holes 0, rim-vs-core 0.22, rim-vs-outside 0.53, heterogeneity 0.18; core [0.941, 0.427] rim [0.73, 0.376]
  - track 208 at frame 179: holes 0, rim-vs-core 0.24, rim-vs-outside 0.57, heterogeneity 0.18; core [0.956, 0.466] rim [0.746, 0.346]
  - track 209 at frame 179: holes 0, rim-vs-core 0.22, rim-vs-outside 0.52, heterogeneity 0.17; core [0.938, 0.392] rim [0.722, 0.341]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 6.84 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.8)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.982 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.553)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #205 (t=4175, R_eq 24.44): none; #206 (t=4175, R_eq 22.14): none; #208 (t=4475, R_eq 29.06): none; #209 (t=4475, R_eq 25.38): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
