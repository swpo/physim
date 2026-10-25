# Evidence pack: membrane-evo (seed 21)

- world: `../../twin_nodeath.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 101s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/evo/twin_nodeath.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/evo/twin_nodeath/seed21 --seeds 21 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6859], min area 6 px

## Measurements
- components: final 6, mean 5.5, max 16; occupancy final 0.24
- tracks: 24; persistent (alive >= 50% of run): 6; longest 135 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.10 (1 = constant size)
- enclosures: components with a hole mean 5.32, final 6; holes at thresholds 0.2/0.35/0.5 final [6, 6, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [6, 6, 6]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00771/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 5000, default): splits 4, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.7154, None, 0.1929, -0.2758]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 93: holes 1, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.20; core [0.885, 0.0, 0.715, 0.502] rim [0.546, 0.0, 0.612, 0.615]
  - track 19 at frame 93: holes 1, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.20; core [0.884, 0.0, 0.74, 0.546] rim [0.547, 0.0, 0.613, 0.617]
  - track 20 at frame 94: holes 1, rim-vs-core 0.28, rim-vs-outside 0.73, heterogeneity 0.21; core [0.779, 0.0, 0.724, 0.673] rim [0.535, 0.0, 0.602, 0.61]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 3.22 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.365)
  - radial K2: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.61 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.0912)
  - radial L link: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 2.27 (aggregate of 34 individuals; 2/34 membrane-like individually; rim level 0.351)
  - radial membrane (wall): peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 4.35, rim/outside 1.41 (aggregate of 34 individuals; 22/34 membrane-like individually; rim level 0.247)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=23250, R_eq 13.87, ring): ['membrane (wall)']; #19 (t=23250, R_eq 13.95, ring): ['membrane (wall)']; #20 (t=23500, R_eq 13.53, ring): ['membrane (wall)']; #21 (t=23500, R_eq 15.71, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 32 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
