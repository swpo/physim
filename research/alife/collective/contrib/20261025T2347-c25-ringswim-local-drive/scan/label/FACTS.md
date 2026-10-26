# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 77s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2347-c25-ringswim-local-drive/scan/label --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5385], min area 6 px

## Measurements
- components: final 8, mean 8.3, max 31; occupancy final 0.20
- tracks: 278; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.00, final 7; holes at thresholds 0.2/0.35/0.5 final [2, 7, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 8], H1 [9, 8, 7]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0557/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 1000, default): splits 89, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 69, merge/split ratio 0.775, nucleations 0
- channel total drift (end/start - 1): [-0.3386, -0.7991, -0.2686, -0.4609]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 34: holes 0, rim-vs-core 0.63, rim-vs-outside 0.94, heterogeneity 0.25; core [0.118, 0.879, 0.632, 0.463] rim [0.391, 0.382, 0.6, 0.741]
  - track 228 at frame 166: holes 1, rim-vs-core 0.18, rim-vs-outside 0.77, heterogeneity 0.22; core [0.087, 0.672, 0.5, 0.669] rim [0.197, 0.561, 0.531, 0.595]
  - track 89 at frame 45: holes 1, rim-vs-core 0.18, rim-vs-outside 0.79, heterogeneity 0.20; core [0.119, 0.7, 0.595, 0.677] rim [0.2, 0.574, 0.544, 0.599]
  - track 6 at frame 20: holes 0, rim-vs-core 0.43, rim-vs-outside 0.82, heterogeneity 0.20; core [0.23, 0.815, 0.854, 0.825] rim [0.393, 0.49, 0.68, 0.665]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 10.6, rim/outside 0.788 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.522)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 7.29 (aggregate of 49 individuals; 1/49 membrane-like individually; rim level 0.639)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 5.31 (aggregate of 49 individuals; 35/49 membrane-like individually; rim level 0.541)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.98, rim/outside 6.06 (aggregate of 49 individuals; 37/49 membrane-like individually; rim level 0.569)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #51 (t=1700, R_eq 8.08): ['L link', 'membrane (wall)']; #228 (t=8300, R_eq 11.95, ring): ['L link', 'membrane (wall)']; #89 (t=2250, R_eq 11.69, ring): ['K catalyst', 'L link', 'membrane (wall)']; #6 (t=1000, R_eq 4.92): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 49 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
