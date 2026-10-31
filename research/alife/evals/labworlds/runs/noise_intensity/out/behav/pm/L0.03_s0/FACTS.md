# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../../../scripts/noisy_world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 30s; status ok
- command: `nsweep behav pm level 0.03`
- segmentation: matter > 0.35 of robust range [0.0, 1.5448], min area 6 px

## Measurements
- components: final 16, mean 15.6, max 31; occupancy final 0.33
- tracks: 172; persistent (alive >= 50% of run): 1; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.43 (1 = constant size)
- enclosures: components with a hole mean 9.45, final 11; holes at thresholds 0.2/0.35/0.5 final [2, 11, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 16], H1 [14, 12, 7]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0118/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 1000, default): splits 61, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 12, merge/split ratio 0.197, nucleations 11
- channel total drift (end/start - 1): [-0.5211, -0.6649, 0.1159, -0.1009]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 118 at frame 118: holes 1, rim-vs-core 0.19, rim-vs-outside 0.81, heterogeneity 0.18; core [0.082, 0.704, 0.466, 0.712] rim [0.164, 0.58, 0.494, 0.603]
  - track 56 at frame 40: holes 1, rim-vs-core 0.22, rim-vs-outside 0.84, heterogeneity 0.20; core [0.099, 0.823, 0.578, 0.576] rim [0.167, 0.622, 0.519, 0.603]
  - track 35 at frame 36: holes 1, rim-vs-core 0.26, rim-vs-outside 0.92, heterogeneity 0.21; core [0.078, 0.814, 0.508, 0.487] rim [0.194, 0.614, 0.541, 0.612]
  - track 146 at frame 134: holes 1, rim-vs-core 0.28, rim-vs-outside 0.82, heterogeneity 0.20; core [0.108, 0.8, 0.597, 0.615] rim [0.197, 0.561, 0.497, 0.588]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10.7, rim/outside 0.858 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.485)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 5.78 (aggregate of 96 individuals; 1/96 membrane-like individually; rim level 0.732)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.68, rim/outside 4.76 (aggregate of 96 individuals; 76/96 membrane-like individually; rim level 0.599)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.35, rim/outside 4.44 (aggregate of 96 individuals; 78/96 membrane-like individually; rim level 0.654)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #118 (t=5900, R_eq 11.07, ring): ['L link', 'membrane (wall)']; #56 (t=2000, R_eq 10.17, ring): ['L link', 'membrane (wall)']; #35 (t=1800, R_eq 10.98): none; #146 (t=6700, R_eq 8.9, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 47 of 96 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
