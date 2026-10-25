# Evidence pack: ringswim-waste-256 (seed 0)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 60 steps x dt 1.0 = time 12000; grid [128, 128]; wall 69s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py --out /tmp/claude-0/c28sd/dL01 --seeds 0 --size 128 128 --spf 60 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5046], min area 6 px

## Measurements
- components: final 3, mean 3.4, max 14; occupancy final 0.27
- tracks: 24; persistent (alive >= 50% of run): 3; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 52.00 (1 = constant size)
- enclosures: components with a hole mean 2.60, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [3, 3, 3]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00673/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 1200, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.7502, -0.5598, 0.4024, -0.2156]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 19 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 0.374 (aggregate of 19 individuals; 2/19 membrane-like individually; rim level 0.0773)
  - radial K catalyst: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 1.29 (aggregate of 19 individuals; 4/19 membrane-like individually; rim level 0.443)
  - radial L link: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 1.02 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 0.321)
  - radial membrane (wall): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 6.38, rim/outside 0.564 (aggregate of 19 individuals; 1/19 membrane-like individually; rim level 0.171)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=6060, R_eq 20.88, ring): none; #12 (t=6060, R_eq 22.53, ring): none; #17 (t=6060, R_eq 22.1, ring): none; #19 (t=1620, R_eq 16.96, ring): ['K catalyst']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 19 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
