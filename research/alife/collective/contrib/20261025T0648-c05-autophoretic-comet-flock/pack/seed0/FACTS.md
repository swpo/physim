# Evidence pack: phase-slipflock (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_swimdiv; mutation: label-free local phoretic slip (Gaussian-averaged grad S, MUSCL advection) , no link ring (chi=0), from noise
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 69s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0648-c05-autophoretic-comet-flock/world.py --out collective/contrib/20261025T0648-c05-autophoretic-comet-flock/pack --seeds 0 1 --no-movie --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.7053], min area 6 px

## Measurements
- components: final 19, mean 19.1, max 28; occupancy final 0.10
- tracks: 79; persistent (alive >= 50% of run): 19; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.03 (1 = constant size)
- enclosures: components with a hole mean 0.51, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.0876/time; max body lengths 47.6
- replication (lineage window K = 20 frames = time 1000, default): splits 22, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.091, nucleations 0
- channel total drift (end/start - 1): [-0.2484, -0.8812, -0.2221, -0.6858]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 81: holes 0, rim-vs-core 0.50, rim-vs-outside 0.47, heterogeneity 0.18; core [0.25, 0.603, 0.624, 0.809] rim [0.406, 0.271, 0.38, 0.568]
  - track 25 at frame 81: holes 0, rim-vs-core 0.49, rim-vs-outside 0.50, heterogeneity 0.21; core [0.219, 0.641, 0.627, 0.753] rim [0.4, 0.296, 0.375, 0.601]
  - track 32 at frame 81: holes 0, rim-vs-core 0.41, rim-vs-outside 0.62, heterogeneity 0.21; core [0.224, 0.657, 0.647, 0.701] rim [0.355, 0.353, 0.408, 0.684]
  - track 77 at frame 116: holes 0, rim-vs-core 0.59, rim-vs-outside 0.40, heterogeneity 0.22; core [0.23, 0.608, 0.603, 0.743] rim [0.445, 0.217, 0.293, 0.512]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 116 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.81, rim/outside 0.819 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.578)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 22.3 (aggregate of 116 individuals; 0/116 membrane-like individually; rim level 0.626)
  - radial L link: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 9.83 (aggregate of 116 individuals; 1/116 membrane-like individually; rim level 0.616)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 34.2 (aggregate of 116 individuals; 22/116 membrane-like individually; rim level 0.775)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=4050, R_eq 4.33): none; #25 (t=4050, R_eq 5.05): none; #32 (t=4050, R_eq 5.2): none; #77 (t=5800, R_eq 5.47): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
