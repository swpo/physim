# Evidence pack: membrane-evo-up (seed 22)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 101s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev/up --seeds 21 22 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.726], min area 6 px

## Measurements
- components: final 12, mean 10.6, max 18; occupancy final 0.28
- tracks: 112; persistent (alive >= 50% of run): 2; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.23 (1 = constant size)
- enclosures: components with a hole mean 9.29, final 9; holes at thresholds 0.2/0.35/0.5 final [7, 9, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 12], H1 [12, 12, 8]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00213/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 5000, default): splits 44, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 4, merges 4, merge/split ratio 0.091, nucleations 0
- channel total drift (end/start - 1): [-0.9016, None, 0.4931, -0.2124]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 99: holes 1, rim-vs-core 0.31, rim-vs-outside 0.75, heterogeneity 0.21; core [0.826, 0.0, 0.665, 0.536] rim [0.536, 0.0, 0.572, 0.61]
  - track 59 at frame 110: holes 1, rim-vs-core 0.22, rim-vs-outside 0.74, heterogeneity 0.20; core [0.732, 0.0, 0.621, 0.653] rim [0.528, 0.0, 0.545, 0.622]
  - track 66 at frame 108: holes 1, rim-vs-core 0.37, rim-vs-outside 0.69, heterogeneity 0.21; core [0.826, 0.0, 0.649, 0.547] rim [0.481, 0.0, 0.553, 0.63]
  - track 86 at frame 134: holes 1, rim-vs-core 0.35, rim-vs-outside 0.75, heterogeneity 0.20; core [0.85, 0.0, 0.626, 0.459] rim [0.543, 0.0, 0.579, 0.62]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 10.1 (aggregate of 67 individuals; 7/67 membrane-like individually; rim level 0.531)
  - radial K2: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 1.32 (aggregate of 67 individuals; 1/67 membrane-like individually; rim level 0.0761)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 4 (aggregate of 67 individuals; 50/67 membrane-like individually; rim level 0.479)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.37, rim/outside 2.91 (aggregate of 67 individuals; 57/67 membrane-like individually; rim level 0.459)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #35 (t=24750, R_eq 10.08, ring): ['K1', 'L link', 'membrane (wall)']; #59 (t=27500, R_eq 11.11, ring): ['L link', 'membrane (wall)']; #66 (t=27000, R_eq 8.85, ring): ['L link', 'membrane (wall)']; #86 (t=33500, R_eq 10.67, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 57 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
