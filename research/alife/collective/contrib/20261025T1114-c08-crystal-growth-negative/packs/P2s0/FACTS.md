# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 710s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/P2s0 --seeds 0 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.938, 0.953], min area 6 px

## Measurements
- components: final 18, mean 19.1, max 37; occupancy final 0.25
- tracks: 214; persistent (alive >= 50% of run): 18; longest 216 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.271/time; max body lengths 62.4
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 54, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 43, merge/split ratio 0.796, nucleations 68
- channel total drift (end/start - 1): [0.1348, 513.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 139 at frame 133: holes 0, rim-vs-core 0.17, rim-vs-outside 0.47, heterogeneity 0.20; core [0.916, 0.331] rim [0.78, 0.437]
  - track 148 at frame 135: holes 0, rim-vs-core 0.27, rim-vs-outside 0.37, heterogeneity 0.20; core [0.926, 0.397] rim [0.659, 0.421]
  - track 160 at frame 137: holes 0, rim-vs-core 0.18, rim-vs-outside 0.43, heterogeneity 0.20; core [0.92, 0.381] rim [0.738, 0.413]
  - track 164 at frame 137: holes 0, rim-vs-core 0.27, rim-vs-outside 0.37, heterogeneity 0.20; core [0.926, 0.382] rim [0.66, 0.413]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 8.59 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.801)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.958 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.561)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #139 (t=3325, R_eq 12.88): none; #148 (t=3375, R_eq 12.9): none; #160 (t=3425, R_eq 12.69): none; #164 (t=3425, R_eq 12.49): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
