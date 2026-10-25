# Evidence pack: fch-turnover-test (seed 0)

- world: `../../wturn_a2.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 121 frames x 400 steps x dt 0.02 = time 960; grid [128, 128]; wall 426s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wturn_a2.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/turn_a2/seed0 --seeds 0 --frames 120 --spf 400 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0712, 2.9819], min area 6 px

## Measurements
- components: final 47, mean 34.5, max 47; occupancy final 0.23
- tracks: 73; persistent (alive >= 50% of run): 35; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 13.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 47, 47], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 22, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.4913, 1.2152, None, -0.6099]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 61: holes 0, rim-vs-core 0.33, rim-vs-outside 0.46, heterogeneity 0.25; core [0.567, 0.586, 0.258, 0.077] rim [0.397, 0.304, 0.242, 0.109]
  - track 7 at frame 61: holes 0, rim-vs-core 0.79, rim-vs-outside 0.21, heterogeneity 0.25; core [0.623, 0.646, 0.236, 0.056] rim [0.176, 0.001, 0.294, 0.138]
  - track 11 at frame 61: holes 0, rim-vs-core 0.71, rim-vs-outside 0.20, heterogeneity 0.23; core [0.621, 0.581, 0.254, 0.062] rim [0.17, 0.039, 0.286, 0.136]
  - track 55 at frame 99: holes 0, rim-vs-core 0.55, rim-vs-outside 0.32, heterogeneity 0.22; core [0.636, 0.279, 0.359, 0.109] rim [0.182, 0.003, 0.496, 0.157]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 220 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.517, rim/outside 10.4 (aggregate of 220 individuals; 0/220 membrane-like individually; rim level 0.489)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.375, rim/outside 13.5 (aggregate of 220 individuals; 0/220 membrane-like individually; rim level 0.226)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.5, rim/outside 5.32 (aggregate of 220 individuals; 220/220 membrane-like individually; rim level 0.7)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.01, rim/outside 0.889 (aggregate of 220 individuals; 0/220 membrane-like individually; rim level 0.251)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=488, R_eq 4.98): ['shell q']; #7 (t=488, R_eq 4.98): ['shell q']; #11 (t=488, R_eq 4.98): ['shell q']; #55 (t=792, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
