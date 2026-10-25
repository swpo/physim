# Evidence pack: fch-metabolic-micelles (seed 0)

- world: `../../wt1.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 922s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wt1.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/mt1/seed0 --seeds 0 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0791, 2.9896], min area 6 px

## Measurements
- components: final 1, mean 22.2, max 106; occupancy final 0.91
- tracks: 421; persistent (alive >= 50% of run): 1; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.17 (1 = constant size)
- enclosures: components with a hole mean 0.70, final 1; holes at thresholds 0.2/0.35/0.5 final [83, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [92, 77, 70], H1 [67, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.126/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 320, default): splits 135, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 81, merge/split ratio 0.6, nucleations 24
- channel total drift (end/start - 1): [3.0674, 9.2861, None, -0.8214]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 35: holes 0, rim-vs-core 0.61, rim-vs-outside 0.19, heterogeneity 0.20; core [0.619, 0.582, 0.121, 0.104] rim [0.179, 0.163, 0.176, 0.157]
  - track 100 at frame 39: holes 0, rim-vs-core 0.57, rim-vs-outside 0.15, heterogeneity 0.18; core [0.602, 0.455, 0.159, 0.097] rim [0.161, 0.09, 0.18, 0.135]
  - track 101 at frame 39: holes 0, rim-vs-core 0.71, rim-vs-outside 0.15, heterogeneity 0.21; core [0.621, 0.559, 0.144, 0.089] rim [0.17, 0.018, 0.184, 0.144]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.52, rim/outside 1.9 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.467)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.431, rim/outside 1.59 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.232)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 6.8, rim/outside 2.6 (aggregate of 128 individuals; 119/128 membrane-like individually; rim level 0.311)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 1 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.24)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #420 (t=1680, R_eq 67.74): none; #49 (t=560, R_eq 5.05): ['shell q']; #100 (t=624, R_eq 5.11): ['shell q']; #101 (t=624, R_eq 5.11): ['shell q']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 5 of 128 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
