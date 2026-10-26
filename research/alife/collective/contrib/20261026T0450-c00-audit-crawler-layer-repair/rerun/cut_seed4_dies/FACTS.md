# Evidence pack: wavepin-crawler-layer-cargo-rho (seed 4)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0243-c31-crawler-layer-repair-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 71 frames x 200 steps x dt 0.001 = time 14; grid [256, 256]; wall 494s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0243-c31-crawler-layer-repair-claim/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/crawler-layer-repair/construction/rerun_cut --seeds 4 --frames 70 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 0.8, max 1; occupancy final 0.00
- tracks: 1; persistent (alive >= 50% of run): 1; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 37.66 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 14.1/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 30: holes 0, rim-vs-core 0.48, rim-vs-outside 1.20, heterogeneity 0.27; core [1.0, 0.208, 0.21, 0.149, 0.258] rim [0.961, 0.549, 0.535, 0.214, 0.261]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 5 components >= 12 px at frames [12, 23, 35, 47, 58]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 5 individuals; 0/5 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 44.2 (aggregate of 5 individuals; 3/5 membrane-like individually; rim level 0.432)  MEMBRANE-LIKE
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.68, rim/outside 15.5 (aggregate of 5 individuals; 5/5 membrane-like individually; rim level 0.493)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 11.7 (aggregate of 5 individuals; 3/5 membrane-like individually; rim level 0.501)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside), s (layer species)
- membrane-like channels per top track at mid-life: #0 (t=6, R_eq 46.74): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
