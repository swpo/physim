# Evidence pack: active-nematic-marangoni (seed 3)

- world: `../../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [128, 128]; wall 199s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/rods_converge/behav/dt0.05_n128 --seeds 3 4 --frames 120 --spf 100 --dt 0.05 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8303, 0.56], min area 6 px

## Measurements
- components: final 30, mean 16.5, max 30; occupancy final 0.09
- tracks: 75; persistent (alive >= 50% of run): 6; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.81 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.363/time; max body lengths 8.1
- replication (lineage window K = 20 frames = time 100, default): splits 31, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.226, nucleations 6
- channel total drift (end/start - 1): [-0.503, -0.3976, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 82: holes 0, rim-vs-core 0.77, rim-vs-outside 0.35, heterogeneity 0.24; core [0.949, 0.712, 0.438, 0.47] rim [0.722, 0.419, 0.929, 0.013]
  - track 23 at frame 85: holes 0, rim-vs-core 0.73, rim-vs-outside 0.35, heterogeneity 0.23; core [0.952, 0.785, 0.445, 0.56] rim [0.77, 0.515, 0.867, 0.066]
  - track 25 at frame 85: holes 0, rim-vs-core 0.71, rim-vs-outside 0.37, heterogeneity 0.22; core [0.931, 0.808, 0.444, 0.465] rim [0.727, 0.527, 0.86, 0.013]
  - track 38 at frame 93: holes 0, rim-vs-core 0.59, rim-vs-outside 0.36, heterogeneity 0.21; core [0.919, 0.721, 0.463, 0.525] rim [0.779, 0.489, 0.768, 0.1]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 113 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 4.44 (aggregate of 113 individuals; 0/113 membrane-like individually; rim level 0.696)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 8.63 (aggregate of 113 individuals; 4/113 membrane-like individually; rim level 0.548)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.35 (aggregate of 113 individuals; 51/113 membrane-like individually; rim level 0.609)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.428, rim/outside 2.01 (aggregate of 113 individuals; 17/113 membrane-like individually; rim level 0.14)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=410, R_eq 4.41): none; #23 (t=425, R_eq 3.83): none; #25 (t=425, R_eq 4.22): none; #38 (t=465, R_eq 4.58): ['order |Q|', 'cargo c']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 113 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
