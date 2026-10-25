# Evidence pack: ringswim-waste (seed 4)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 41s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/wtilt/a3/seed4 --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5818], min area 6 px

## Measurements
- components: final 13, mean 13.2, max 23; occupancy final 0.24
- tracks: 267; persistent (alive >= 50% of run): 0; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 4.03, final 4; holes at thresholds 0.2/0.35/0.5 final [1, 4, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 14, 13], H1 [9, 8, 1]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0143/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 1000, default): splits 114, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.061, nucleations 0
- channel total drift (end/start - 1): [-0.379, -0.7889, -0.1427, -0.3556]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 171 at frame 160: holes 0, rim-vs-core 0.69, rim-vs-outside 0.44, heterogeneity 0.19; core [0.254, 0.721, 0.863, 0.865] rim [0.381, 0.321, 0.55, 0.416]
  - track 205 at frame 165: holes 1, rim-vs-core 0.30, rim-vs-outside 0.75, heterogeneity 0.20; core [0.112, 0.769, 0.644, 0.621] rim [0.218, 0.525, 0.509, 0.603]
  - track 96 at frame 74: holes 0, rim-vs-core 0.82, rim-vs-outside 0.72, heterogeneity 0.23; core [0.368, 0.948, 0.999, 0.801] rim [0.543, 0.323, 0.516, 0.662]
  - track 238 at frame 185: holes 0, rim-vs-core 0.43, rim-vs-outside 0.84, heterogeneity 0.21; core [0.085, 0.745, 0.542, 0.574] rim [0.316, 0.409, 0.533, 0.702]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 6.58, rim/outside 0.825 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.536)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 9.57 (aggregate of 85 individuals; 8/85 membrane-like individually; rim level 0.719)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 7.46 (aggregate of 85 individuals; 53/85 membrane-like individually; rim level 0.698)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.94, rim/outside 7.68 (aggregate of 85 individuals; 63/85 membrane-like individually; rim level 0.714)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #171 (t=8000, R_eq 4.75): none; #205 (t=8250, R_eq 8.85, ring): ['L link', 'membrane (wall)']; #96 (t=3700, R_eq 3.66): ['membrane (wall)']; #238 (t=9250, R_eq 8.61): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 29 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
