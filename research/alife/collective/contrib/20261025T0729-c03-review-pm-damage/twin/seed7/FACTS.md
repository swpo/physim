# Evidence pack: phase-membrane (seed 7)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 11s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/twin/seed7 --seeds 7 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5409], min area 6 px

## Measurements
- components: final 13, mean 14.5, max 22; occupancy final 0.28
- tracks: 142; persistent (alive >= 50% of run): 2; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.50 (1 = constant size)
- enclosures: components with a hole mean 9.45, final 10; holes at thresholds 0.2/0.35/0.5 final [2, 11, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [14, 13, 10]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00686/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 59, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 4, merges 4, merge/split ratio 0.068, nucleations 0
- channel total drift (end/start - 1): [-0.4354, -0.7063, -0.0575, -0.13]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 91: holes 1, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.19; core [0.097, 0.769, 0.565, 0.65] rim [0.163, 0.614, 0.516, 0.61]
  - track 84 at frame 118: holes 1, rim-vs-core 0.17, rim-vs-outside 0.80, heterogeneity 0.18; core [0.093, 0.733, 0.506, 0.699] rim [0.158, 0.593, 0.498, 0.626]
  - track 88 at frame 114: holes 1, rim-vs-core 0.30, rim-vs-outside 0.77, heterogeneity 0.20; core [0.107, 0.793, 0.586, 0.627] rim [0.224, 0.533, 0.505, 0.588]
  - track 117 at frame 141: holes 1, rim-vs-core 0.23, rim-vs-outside 0.78, heterogeneity 0.20; core [0.107, 0.792, 0.597, 0.635] rim [0.188, 0.598, 0.518, 0.595]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 12.4, rim/outside 0.809 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.487)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 6.58 (aggregate of 86 individuals; 1/86 membrane-like individually; rim level 0.751)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 5.25 (aggregate of 86 individuals; 74/86 membrane-like individually; rim level 0.583)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.27, rim/outside 4.95 (aggregate of 86 individuals; 76/86 membrane-like individually; rim level 0.627)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #60 (t=4550, R_eq 10.22, ring): ['L link', 'membrane (wall)']; #84 (t=5900, R_eq 11.9, ring): ['L link', 'membrane (wall)']; #88 (t=5700, R_eq 9.1, ring): ['L link', 'membrane (wall)']; #117 (t=7050, R_eq 9.44, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 53 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
