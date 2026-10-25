# Evidence pack: ringswim-waste (seed 7)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 606s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out /tmp/claude-0/c07/big/s7 --seeds 7 --size 256 256 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5542], min area 6 px

## Measurements
- components: final 35, mean 37.3, max 81; occupancy final 0.21
- tracks: 1958; persistent (alive >= 50% of run): 0; longest 32 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 25.69, final 26; holes at thresholds 0.2/0.35/0.5 final [5, 29, 32]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 35, 35], H1 [36, 34, 19]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.0571/time; max body lengths 5.0
- replication (lineage window K = 20 frames = time 2000, default): splits 660, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 567, merge/split ratio 0.859, nucleations 10
- channel total drift (end/start - 1): [-0.3275, -0.8052, -0.2862, -0.4027]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 624 at frame 62: holes 0, rim-vs-core 0.68, rim-vs-outside 0.96, heterogeneity 0.26; core [0.115, 0.891, 0.689, 0.387] rim [0.393, 0.414, 0.59, 0.761]
  - track 1266 at frame 131: holes 1, rim-vs-core 0.22, rim-vs-outside 0.79, heterogeneity 0.20; core [0.106, 0.759, 0.585, 0.55] rim [0.182, 0.571, 0.538, 0.606]
  - track 117 at frame 15: holes 1, rim-vs-core 0.29, rim-vs-outside 0.72, heterogeneity 0.21; core [0.131, 0.743, 0.666, 0.638] rim [0.224, 0.519, 0.511, 0.575]
  - track 112 at frame 15: holes 1, rim-vs-core 0.15, rim-vs-outside 0.79, heterogeneity 0.19; core [0.08, 0.651, 0.491, 0.638] rim [0.161, 0.524, 0.489, 0.628]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 213 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 9.63, rim/outside 0.777 (aggregate of 213 individuals; 0/213 membrane-like individually; rim level 0.532)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 9.03 (aggregate of 213 individuals; 11/213 membrane-like individually; rim level 0.629)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 6.68 (aggregate of 213 individuals; 133/213 membrane-like individually; rim level 0.547)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.91, rim/outside 7.3 (aggregate of 213 individuals; 139/213 membrane-like individually; rim level 0.56)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #624 (t=6200, R_eq 7.82): ['L link', 'membrane (wall)']; #1266 (t=13100, R_eq 10.62, ring): ['L link', 'membrane (wall)']; #117 (t=1500, R_eq 9.34, ring): ['L link', 'membrane (wall)']; #112 (t=1500, R_eq 11.48): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 110 of 213 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
