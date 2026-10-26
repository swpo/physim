# Evidence pack: fch-gated-micelles-homgate (seed 51)

- world: `../../variants/homgate.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 229s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/fch-gated-micelles/variants/homgate.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/fch-gated-micelles/controls/homgate_seed51 --seeds 51 --frames 100 --no-movie`
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
  - track 2 at frame 50: holes 0, rim-vs-core 0.46, rim-vs-outside 0.24, heterogeneity 0.18; core [0.615, 0.274, 0.24] rim [0.172, 0.207, 0.343]
  - track 7 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.21, heterogeneity 0.18; core [0.61, 0.259, 0.234] rim [0.164, 0.188, 0.297]
  - track 10 at frame 51: holes 0, rim-vs-core 0.45, rim-vs-outside 0.21, heterogeneity 0.18; core [0.604, 0.284, 0.255] rim [0.159, 0.214, 0.304]
  - track 66 at frame 90: holes 0, rim-vs-core 0.21, rim-vs-outside 0.42, heterogeneity 0.28; core [0.567, 0.498, 0.383] rim [0.382, 0.391, 0.405]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 259 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.51, rim/outside 10.5 (aggregate of 259 individuals; 1/259 membrane-like individually; rim level 0.481)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.689, rim/outside 2.05 (aggregate of 259 individuals; 0/259 membrane-like individually; rim level 0.377)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.5, rim/outside 5.11 (aggregate of 259 individuals; 258/259 membrane-like individually; rim level 0.684)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=200, R_eq 4.92): ['shell q']; #7 (t=204, R_eq 4.95): ['shell q']; #10 (t=204, R_eq 4.98): ['shell q']; #66 (t=360, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
