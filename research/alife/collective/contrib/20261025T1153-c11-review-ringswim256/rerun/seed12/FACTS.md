# Evidence pack: ringswim-waste-256 (seed 12)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 493s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c07-ringswim-256/world.py --out /tmp/claude-0/c11rev19/rerun --seeds 12 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5553], min area 6 px

## Measurements
- components: final 25, mean 38.7, max 76; occupancy final 0.20
- tracks: 1935; persistent (alive >= 50% of run): 0; longest 35 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 26.67, final 21; holes at thresholds 0.2/0.35/0.5 final [4, 30, 36]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 31, 25], H1 [39, 35, 14]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.0557/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 2000, default): splits 650, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 559, merge/split ratio 0.86, nucleations 13
- channel total drift (end/start - 1): [-0.3246, -0.8138, -0.3015, -0.4537]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1627 at frame 180: holes 1, rim-vs-core 0.38, rim-vs-outside 0.71, heterogeneity 0.25; core [0.15, 0.82, 0.728, 0.565] rim [0.277, 0.524, 0.523, 0.547]
  - track 1423 at frame 153: holes 0, rim-vs-core 0.53, rim-vs-outside 1.03, heterogeneity 0.21; core [0.054, 0.731, 0.452, 0.38] rim [0.266, 0.496, 0.606, 0.771]
  - track 671 at frame 71: holes 1, rim-vs-core 0.34, rim-vs-outside 0.79, heterogeneity 0.22; core [0.12, 0.778, 0.651, 0.588] rim [0.25, 0.492, 0.513, 0.593]
  - track 138 at frame 17: holes 1, rim-vs-core 0.29, rim-vs-outside 0.62, heterogeneity 0.21; core [0.114, 0.671, 0.564, 0.712] rim [0.207, 0.477, 0.458, 0.549]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 209 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.09, rim/outside 0.794 (aggregate of 209 individuals; 0/209 membrane-like individually; rim level 0.528)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 7.81 (aggregate of 209 individuals; 9/209 membrane-like individually; rim level 0.635)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 6.23 (aggregate of 209 individuals; 140/209 membrane-like individually; rim level 0.555)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.06, rim/outside 6.64 (aggregate of 209 individuals; 143/209 membrane-like individually; rim level 0.585)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #1627 (t=18000, R_eq 9.47, ring): ['L link', 'membrane (wall)']; #1423 (t=15300, R_eq 10.17): none; #671 (t=7100, R_eq 8.5, ring): ['L link', 'membrane (wall)']; #138 (t=1700, R_eq 9.61, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 102 of 209 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
