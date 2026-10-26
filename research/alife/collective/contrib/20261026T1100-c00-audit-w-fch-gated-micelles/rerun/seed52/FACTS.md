# Evidence pack: fch-gated-micelles (seed 52)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 207s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/fch-gated-micelles/rerun/seed52 --seeds 52 --frames 100 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1186, 2.9941], min area 6 px

## Measurements
- components: final 51, mean 37.7, max 51; occupancy final 0.26
- tracks: 79; persistent (alive >= 50% of run): 30; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 8.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 52, 51], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 80, default): splits 26, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.6631, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 50: holes 0, rim-vs-core 0.61, rim-vs-outside 0.21, heterogeneity 0.25; core [0.616, 0.422, 0.227] rim [0.16, 0.025, 0.298]
  - track 3 at frame 51: holes 0, rim-vs-core 0.59, rim-vs-outside 0.31, heterogeneity 0.27; core [0.661, 0.487, 0.235] rim [0.246, 0.102, 0.384]
  - track 4 at frame 51: holes 0, rim-vs-core 0.40, rim-vs-outside 0.35, heterogeneity 0.26; core [0.624, 0.453, 0.257] rim [0.329, 0.19, 0.283]
  - track 65 at frame 86: holes 0, rim-vs-core 0.50, rim-vs-outside 0.30, heterogeneity 0.26; core [0.608, 0.264, 0.419] rim [0.152, 0.09, 0.502]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 241 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.517, rim/outside 10.7 (aggregate of 241 individuals; 0/241 membrane-like individually; rim level 0.489)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.687, rim/outside 7.26 (aggregate of 241 individuals; 0/241 membrane-like individually; rim level 0.361)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 10.7, rim/outside 4.89 (aggregate of 241 individuals; 238/241 membrane-like individually; rim level 0.68)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=200, R_eq 5.26): ['shell q']; #3 (t=204, R_eq 5.2): ['shell q']; #4 (t=204, R_eq 5.23): ['shell q']; #65 (t=344, R_eq 5.23): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
