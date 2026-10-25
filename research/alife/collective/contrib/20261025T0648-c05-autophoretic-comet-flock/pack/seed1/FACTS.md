# Evidence pack: phase-slipflock (seed 1)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_swimdiv; mutation: label-free local phoretic slip (Gaussian-averaged grad S, MUSCL advection) , no link ring (chi=0), from noise
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0648-c05-autophoretic-comet-flock/world.py --out collective/contrib/20261025T0648-c05-autophoretic-comet-flock/pack --seeds 0 1 --no-movie --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.7157], min area 6 px

## Measurements
- components: final 18, mean 18.4, max 29; occupancy final 0.10
- tracks: 82; persistent (alive >= 50% of run): 18; longest 161 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 3.82 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.0813/time; max body lengths 67.1
- replication (lineage window K = 20 frames = time 1000, default): splits 20, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 0.25, nucleations 0
- channel total drift (end/start - 1): [-0.2449, -0.8837, -0.2327, -0.6231]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 81: holes 0, rim-vs-core 0.56, rim-vs-outside 0.41, heterogeneity 0.23; core [0.141, 0.599, 0.589, 0.739] rim [0.379, 0.231, 0.3, 0.547]
  - track 14 at frame 81: holes 0, rim-vs-core 0.42, rim-vs-outside 0.52, heterogeneity 0.21; core [0.145, 0.593, 0.587, 0.735] rim [0.369, 0.314, 0.393, 0.628]
  - track 24 at frame 81: holes 0, rim-vs-core 0.54, rim-vs-outside 0.42, heterogeneity 0.22; core [0.144, 0.599, 0.588, 0.758] rim [0.371, 0.247, 0.317, 0.561]
  - track 28 at frame 81: holes 0, rim-vs-core 0.53, rim-vs-outside 0.45, heterogeneity 0.22; core [0.143, 0.597, 0.587, 0.751] rim [0.379, 0.248, 0.319, 0.569]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 109 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17.8, rim/outside 0.804 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.557)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 24.3 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.634)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 9.87 (aggregate of 109 individuals; 1/109 membrane-like individually; rim level 0.641)
  - radial membrane (wall): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 55.8 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.787)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=4050, R_eq 5.53): none; #14 (t=4050, R_eq 5.17): none; #24 (t=4050, R_eq 5.17): none; #28 (t=4050, R_eq 5.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
