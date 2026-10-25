# Evidence pack: active-nematic-droplets (seed 41)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1141-c11-active-nematic-ringed/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 200 steps x dt 0.025 (--dt; world META dt 0.05) = time 1000; grid [128, 128]; wall 904s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T1141-c11-active-nematic-ringed/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/nematic-ringed/replication/dthalf --seeds 41 --spf 200 --dt 0.025 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8268, 0.6162], min area 6 px

## Measurements
- components: final 31, mean 19.8, max 33; occupancy final 0.06
- tracks: 93; persistent (alive >= 50% of run): 6; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.0746/time; max body lengths 5.3
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.15, nucleations 7
- channel total drift (end/start - 1): [-0.5024, -0.4195, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 119: holes 0, rim-vs-core 0.18, rim-vs-outside 0.53, heterogeneity 0.18; core [0.92, 0.847, 0.568] rim [0.829, 0.727, 0.671]
  - track 20 at frame 126: holes 0, rim-vs-core 0.52, rim-vs-outside 0.35, heterogeneity 0.17; core [0.941, 0.89, 0.435] rim [0.715, 0.577, 0.784]
  - track 21 at frame 128: holes 0, rim-vs-core 0.46, rim-vs-outside 0.35, heterogeneity 0.16; core [0.934, 0.875, 0.448] rim [0.742, 0.606, 0.765]
  - track 70 at frame 180: holes 0, rim-vs-core 0.57, rim-vs-outside 0.36, heterogeneity 0.18; core [0.965, 0.952, 0.398] rim [0.745, 0.628, 0.81]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 4.78 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.757)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 8.24 (aggregate of 133 individuals; 1/133 membrane-like individually; rim level 0.644)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 2.15 (aggregate of 133 individuals; 96/133 membrane-like individually; rim level 0.647)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #18 (t=595, R_eq 2.99): ['surfactant s']; #20 (t=630, R_eq 3.04): ['surfactant s']; #21 (t=640, R_eq 3.34): ['surfactant s']; #70 (t=900, R_eq 3.09): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
