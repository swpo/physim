# Evidence pack: pcell-yeff-cap (seed 7)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1108-c06-pcell-efficiency-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 438s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1108-c06-pcell-efficiency-claim/world.py --out /tmp/claude-0/c11rev26/rerun --seeds 7 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5523], min area 6 px

## Measurements
- components: final 11, mean 17.3, max 25; occupancy final 0.34
- tracks: 67; persistent (alive >= 50% of run): 13; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.00 (1 = constant size)
- enclosures: components with a hole mean 6.83, final 6; holes at thresholds 0.2/0.35/0.5 final [29, 7, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 11, 11], H1 [12, 6, 5]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.000626/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 10000, default): splits 14, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.143, nucleations 12
- channel total drift (end/start - 1): [-0.7129, -0.414, 0.7364, -0.0145, -0.2087]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 106: holes 0, rim-vs-core 0.67, rim-vs-outside 1.11, heterogeneity 0.23; core [0.218, 0.746, 0.761, 0.561, 0.879] rim [0.391, 0.186, 0.659, 0.779, 0.674]
  - track 53 at frame 131: holes 1, rim-vs-core 0.29, rim-vs-outside 0.81, heterogeneity 0.22; core [0.186, 0.586, 0.618, 0.381, 0.994] rim [0.247, 0.39, 0.598, 0.552, 0.882]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 101 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 3.07, rim/outside 0.948 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.495)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.712, rim/outside 5.71 (aggregate of 101 individuals; 2/101 membrane-like individually; rim level 0.518)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 4.79 (aggregate of 101 individuals; 60/101 membrane-like individually; rim level 0.757)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.53, rim/outside 4.12 (aggregate of 101 individuals; 78/101 membrane-like individually; rim level 0.704)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 4.58 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.877)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #22 (t=50500, R_eq 18.12, ring): none; #25 (t=50500, R_eq 20.03, ring): none; #35 (t=53000, R_eq 6.08): ['L link', 'membrane (wall)']; #53 (t=65500, R_eq 17.46, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 101 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
