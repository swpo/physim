# Evidence pack: phase-membrane (seed 9)

- world: `../../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/pmbd/pm/seed9 --seeds 9 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5427], min area 6 px

## Measurements
- components: final 20, mean 15.7, max 25; occupancy final 0.36
- tracks: 159; persistent (alive >= 50% of run): 3; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.98 (1 = constant size)
- enclosures: components with a hole mean 9.99, final 14; holes at thresholds 0.2/0.35/0.5 final [3, 14, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 20], H1 [19, 19, 11]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00543/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 63, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 9, merge/split ratio 0.143, nucleations 0
- channel total drift (end/start - 1): [-0.5367, -0.6316, 0.1855, 0.0512]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 42: holes 1, rim-vs-core 0.38, rim-vs-outside 0.81, heterogeneity 0.23; core [0.123, 0.912, 0.68, 0.528] rim [0.242, 0.59, 0.535, 0.588]
  - track 65 at frame 52: holes 1, rim-vs-core 0.15, rim-vs-outside 0.80, heterogeneity 0.17; core [0.09, 0.688, 0.511, 0.734] rim [0.147, 0.596, 0.495, 0.627]
  - track 63 at frame 52: holes 1, rim-vs-core 0.30, rim-vs-outside 0.79, heterogeneity 0.20; core [0.106, 0.797, 0.591, 0.636] rim [0.213, 0.54, 0.501, 0.592]
  - track 128 at frame 143: holes 1, rim-vs-core 0.16, rim-vs-outside 0.85, heterogeneity 0.18; core [0.096, 0.772, 0.546, 0.64] rim [0.165, 0.625, 0.529, 0.622]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 12.2, rim/outside 0.868 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.466)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 4.8 (aggregate of 96 individuals; 1/96 membrane-like individually; rim level 0.724)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.74, rim/outside 3.86 (aggregate of 96 individuals; 84/96 membrane-like individually; rim level 0.564)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.76, rim/outside 3.73 (aggregate of 96 individuals; 80/96 membrane-like individually; rim level 0.642)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #28 (t=2100, R_eq 8.78, ring): ['L link', 'membrane (wall)']; #65 (t=2600, R_eq 12.17, ring): ['L link', 'membrane (wall)']; #63 (t=2600, R_eq 8.9, ring): ['L link', 'membrane (wall)']; #128 (t=7150, R_eq 10.03, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 64 of 96 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
