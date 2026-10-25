# Evidence pack: membrane-evo-up (seed 42)

- world: `../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 96s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev7/lk42 --seeds 42 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7138], min area 6 px

## Measurements
- components: final 5, mean 9.2, max 23; occupancy final 0.25
- tracks: 223; persistent (alive >= 50% of run): 0; longest 50 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.09, final 4; holes at thresholds 0.2/0.35/0.5 final [3, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 5, 5], H1 [8, 5, 4]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00211/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 5000, default): splits 76, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 42, merge/split ratio 0.553, nucleations 3
- channel total drift (end/start - 1): [-0.9877, None, 0.6678, -0.0866]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 92 at frame 101: holes 1, rim-vs-core 0.32, rim-vs-outside 0.65, heterogeneity 0.22; core [0.471, 0.392, 0.737, 0.593] rim [0.269, 0.223, 0.553, 0.594]
  - track 51 at frame 73: holes 1, rim-vs-core 0.41, rim-vs-outside 0.70, heterogeneity 0.21; core [0.863, 0.0, 0.677, 0.575] rim [0.484, 0.0, 0.544, 0.628]
  - track 49 at frame 69: holes 1, rim-vs-core 0.47, rim-vs-outside 0.77, heterogeneity 0.22; core [0.873, 0.0, 0.622, 0.528] rim [0.431, 0.0, 0.54, 0.666]
  - track 42 at frame 61: holes 0, rim-vs-core 0.72, rim-vs-outside 0.90, heterogeneity 0.23; core [0.943, 0.0, 0.668, 0.51] rim [0.289, 0.0, 0.597, 0.804]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 10.5 (aggregate of 55 individuals; 2/55 membrane-like individually; rim level 0.349)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.88 (aggregate of 55 individuals; 2/55 membrane-like individually; rim level 0.281)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 2.78 (aggregate of 55 individuals; 27/55 membrane-like individually; rim level 0.512)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.28, rim/outside 1.92 (aggregate of 55 individuals; 34/55 membrane-like individually; rim level 0.421)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #92 (t=25250, R_eq 8.83, ring): ['L link', 'membrane (wall)']; #51 (t=18250, R_eq 8.63, ring): ['L link', 'membrane (wall)']; #49 (t=17250, R_eq 7.51, ring): ['L link', 'membrane (wall)']; #42 (t=15250, R_eq 6.08): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 42 of 55 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
