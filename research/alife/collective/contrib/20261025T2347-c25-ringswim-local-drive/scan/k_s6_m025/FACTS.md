# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 81s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2347-c25-ringswim-local-drive/scan/k_s6_m025 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5388], min area 6 px

## Measurements
- components: final 11, mean 10.2, max 29; occupancy final 0.26
- tracks: 176; persistent (alive >= 50% of run): 0; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 3.55, final 6; holes at thresholds 0.2/0.35/0.5 final [0, 6, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [11, 7, 1]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0177/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 1000, default): splits 66, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 7, merge/split ratio 0.106, nucleations 0
- channel total drift (end/start - 1): [-0.3324, -0.7887, -0.2114, -0.3131]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 103 at frame 121: holes 1, rim-vs-core 0.21, rim-vs-outside 0.83, heterogeneity 0.20; core [0.083, 0.769, 0.554, 0.575] rim [0.185, 0.591, 0.565, 0.607]
  - track 130 at frame 165: holes 0, rim-vs-core 0.65, rim-vs-outside 0.44, heterogeneity 0.18; core [0.253, 0.765, 0.904, 0.873] rim [0.372, 0.38, 0.624, 0.449]
  - track 118 at frame 145: holes 0, rim-vs-core 0.32, rim-vs-outside 1.04, heterogeneity 0.22; core [0.107, 0.87, 0.656, 0.558] rim [0.251, 0.6, 0.624, 0.648]
  - track 158 at frame 190: holes 1, rim-vs-core 0.26, rim-vs-outside 0.90, heterogeneity 0.21; core [0.08, 0.786, 0.54, 0.534] rim [0.207, 0.581, 0.58, 0.622]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 10.9, rim/outside 0.826 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.556)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 7.19 (aggregate of 60 individuals; 5/60 membrane-like individually; rim level 0.695)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.58, rim/outside 5.57 (aggregate of 60 individuals; 43/60 membrane-like individually; rim level 0.633)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 6.17 (aggregate of 60 individuals; 38/60 membrane-like individually; rim level 0.653)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #103 (t=6050, R_eq 11.95, ring): ['K catalyst', 'L link', 'membrane (wall)']; #130 (t=8250, R_eq 4.72): none; #118 (t=7250, R_eq 8.57): ['L link', 'membrane (wall)']; #158 (t=9500, R_eq 11.45, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 60 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
