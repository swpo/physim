# Evidence pack: fch-allee-micelles (seed 0)

- world: `../../wa_h1_k0.1.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 948s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/wa_h1_k0.1.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/al_wa_h1_k0.1/seed0 --seeds 0 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.23 of robust range [0.0, 2.1835], min area 6 px

## Measurements
- components: final 0, mean 3.3, max 25; occupancy final 0.00
- tracks: 29; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 320, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 24
- channel total drift (end/start - 1): [-1.0, -1.0, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 14: holes 0, rim-vs-core 0.41, rim-vs-outside 0.51, heterogeneity 0.12; core [0.999, 0.165, 0.747, 0.529] rim [0.676, 0.136, 1.0, 0.529]
  - track 17 at frame 14: holes 0, rim-vs-core 0.34, rim-vs-outside 0.49, heterogeneity 0.10; core [1.0, 0.176, 0.793, 0.529] rim [0.737, 0.138, 1.0, 0.529]
  - track 26 at frame 14: holes 0, rim-vs-core 0.35, rim-vs-outside 0.48, heterogeneity 0.11; core [1.0, 0.184, 0.774, 0.478] rim [0.738, 0.142, 1.0, 0.529]
  - track 2 at frame 11: holes 0, rim-vs-core 0.30, rim-vs-outside 0.56, heterogeneity 0.13; core [1.0, 0.25, 0.682, 0.299] rim [0.792, 0.225, 0.895, 0.325]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 3 components >= 12 px at frames [25]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 17.6 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 1)
  - radial catalyst c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 1.14 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.0264)
  - radial shell q: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.69, rim/outside 2.37 (aggregate of 3 individuals; 3/3 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.882)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=224, R_eq 3.29): ['shell q']; #17 (t=224, R_eq 3.19): ['shell q']; #26 (t=224, R_eq 3.19): ['shell q']; #2 (t=176, R_eq 3.52): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
