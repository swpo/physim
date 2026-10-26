# Evidence pack: fch-gated-micelles-walloff (seed 51)

- world: `../../variants/walloff.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 207s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/fch-gated-micelles/variants/walloff.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/fch-gated-micelles/controls/walloff_seed51 --seeds 51 --frames 100 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1118, 2.9853], min area 6 px

## Measurements
- components: final 52, mean 39.7, max 52; occupancy final 0.26
- tracks: 84; persistent (alive >= 50% of run): 39; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 52, 52], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 27, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.6611, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 50: holes 0, rim-vs-core 0.45, rim-vs-outside 0.11, heterogeneity 0.13; core [0.615, 0.259, 0.513] rim [0.172, 0.17, 0.475]
  - track 7 at frame 51: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.12; core [0.61, 0.224, 0.488] rim [0.164, 0.146, 0.45]
  - track 10 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.10, heterogeneity 0.13; core [0.604, 0.255, 0.504] rim [0.159, 0.17, 0.466]
  - track 66 at frame 90: holes 0, rim-vs-core 0.21, rim-vs-outside 0.34, heterogeneity 0.18; core [0.567, 0.396, 0.787] rim [0.382, 0.307, 0.769]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 259 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.51, rim/outside 10.5 (aggregate of 259 individuals; 1/259 membrane-like individually; rim level 0.481)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.595, rim/outside 2.32 (aggregate of 259 individuals; 0/259 membrane-like individually; rim level 0.322)
  - radial shell q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 1.11 (aggregate of 259 individuals; 0/259 membrane-like individually; rim level 0.615)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=200, R_eq 4.92): none; #7 (t=204, R_eq 4.95): none; #10 (t=204, R_eq 4.98): none; #66 (t=360, R_eq 5.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
