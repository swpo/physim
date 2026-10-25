# Evidence pack: pcell-yeff-cap-slip (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1152-c06-pcell-slip-ring-negative/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 1288s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1152-c06-pcell-slip-ring-negative/world.py --out /tmp/claude-0/c11rev30/rerun --seeds 3 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0049, 1.441], min area 6 px

## Measurements
- components: final 2, mean 2.7, max 20; occupancy final 0.17
- tracks: 250; persistent (alive >= 50% of run): 0; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.93, final 1; holes at thresholds 0.2/0.35/0.5 final [66, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 1, 1], H1 [6, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 10000, default): splits 13, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 10, merge/split ratio 0.769, nucleations 185
- channel total drift (end/start - 1): [-0.8135, -0.2703, 0.8016, -0.5812, -0.0031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.717, rim/outside 1.42 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.235)
  - radial K particles: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.58, rim/outside 1.03 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.529)
  - radial L link: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.993 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.451)
  - radial membrane (wall): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.752, rim/outside 2.5 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.212)
  - radial mean yield / 2: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.7, rim/outside 0.949 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.803)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #113 (t=53000, R_eq 29.68, ring): none; #79 (t=18500, R_eq 29.61, ring): none; #212 (t=89000, R_eq 29.82, ring): none; #194 (t=80000, R_eq 29.91, ring): ['S', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 8 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
