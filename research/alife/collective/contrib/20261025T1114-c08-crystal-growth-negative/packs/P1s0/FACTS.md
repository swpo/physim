# Evidence pack: nrch (seed 0)

- world: `../../w/nrch.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 720s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/w/nrch.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/nr/P1s0 --seeds 0 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9408, 0.94], min area 6 px

## Measurements
- components: final 14, mean 15.6, max 32; occupancy final 0.22
- tracks: 141; persistent (alive >= 50% of run): 14; longest 227 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.91 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.278/time; max body lengths 57.0
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 27, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 21, merge/split ratio 0.778, nucleations 66
- channel total drift (end/start - 1): [0.0314, 1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 36 at frame 127: holes 0, rim-vs-core 0.24, rim-vs-outside 0.42, heterogeneity 0.20; core [0.944, 0.373] rim [0.703, 0.382]
  - track 60 at frame 129: holes 0, rim-vs-core 0.27, rim-vs-outside 0.36, heterogeneity 0.20; core [0.929, 0.376] rim [0.666, 0.406]
  - track 62 at frame 129: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.19; core [0.92, 0.327] rim [0.67, 0.379]
  - track 107 at frame 143: holes 0, rim-vs-core 0.22, rim-vs-outside 0.49, heterogeneity 0.20; core [0.956, 0.308] rim [0.763, 0.417]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 8.29 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.785)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.941 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.534)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #36 (t=3175, R_eq 14.12): none; #60 (t=3225, R_eq 13.73): none; #62 (t=3225, R_eq 10.84): none; #107 (t=3575, R_eq 14.04): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
