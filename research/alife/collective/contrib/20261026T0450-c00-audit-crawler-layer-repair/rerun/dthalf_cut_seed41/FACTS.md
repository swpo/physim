# Evidence pack: wavepin-crawler-layer-cargo-rho (seed 41)

- world: `../../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0243-c31-crawler-layer-repair-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 61 frames x 400 steps x dt 0.0005 = time 12; grid [256, 256]; wall 755s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0243-c31-crawler-layer-repair-claim/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/crawler-layer-repair/replication/runs/dth41c --seeds 41 --frames 60 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.05
- tracks: 1; persistent (alive >= 50% of run): 1; longest 61 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 12.2/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.4248, -0.4487, -0.448, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 30: holes 0, rim-vs-core 0.07, rim-vs-outside 1.10, heterogeneity 0.28; core [1.0, 0.434, 0.437, 0.138, 0.183] rim [0.963, 0.443, 0.428, 0.193, 0.198]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 53.2 (aggregate of 6 individuals; 4/6 membrane-like individually; rim level 0.522)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.98, rim/outside 19.8 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.385)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.89, rim/outside 7.16 (aggregate of 6 individuals; 4/6 membrane-like individually; rim level 0.331)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species), c (cargo)
- membrane-like channels per top track at mid-life: #0 (t=6, R_eq 46.78): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
