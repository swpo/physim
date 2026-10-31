# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../../../scripts/noisy_world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 30s; status ok
- command: `nsweep behav pm level 0.1`
- segmentation: matter > 0.35 of robust range [0.0, 1.5528], min area 6 px

## Measurements
- components: final 14, mean 6.9, max 17; occupancy final 0.24
- tracks: 161; persistent (alive >= 50% of run): 0; longest 51 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 4.10, final 9; holes at thresholds 0.2/0.35/0.5 final [0, 10, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 14, 14], H1 [13, 11, 3]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00955/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 51, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 16, merge/split ratio 0.314, nucleations 20
- channel total drift (end/start - 1): [-0.3909, -0.7669, -0.1196, -0.2607]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 113 at frame 136: holes 0, rim-vs-core 0.47, rim-vs-outside 0.88, heterogeneity 0.20; core [0.073, 0.821, 0.497, 0.551] rim [0.266, 0.427, 0.517, 0.723]
  - track 116 at frame 136: holes 1, rim-vs-core 0.28, rim-vs-outside 0.74, heterogeneity 0.22; core [0.121, 0.808, 0.691, 0.608] rim [0.179, 0.599, 0.525, 0.557]
  - track 106 at frame 126: holes 0, rim-vs-core 0.35, rim-vs-outside 0.99, heterogeneity 0.22; core [0.11, 0.925, 0.704, 0.6] rim [0.207, 0.618, 0.566, 0.64]
  - track 115 at frame 132: holes 0, rim-vs-core 0.88, rim-vs-outside 0.53, heterogeneity 0.24; core [0.215, 0.891, 0.87, 0.77] rim [0.407, 0.241, 0.374, 0.523]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 11.4, rim/outside 0.802 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.478)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 8.62 (aggregate of 44 individuals; 1/44 membrane-like individually; rim level 0.735)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 6.64 (aggregate of 44 individuals; 32/44 membrane-like individually; rim level 0.583)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.95, rim/outside 4.86 (aggregate of 44 individuals; 32/44 membrane-like individually; rim level 0.605)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #113 (t=6800, R_eq 8.78): ['L link', 'membrane (wall)']; #116 (t=6800, R_eq 9.8, ring): ['L link', 'membrane (wall)']; #106 (t=6300, R_eq 7.44): ['L link', 'membrane (wall)']; #115 (t=6600, R_eq 5.47): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
