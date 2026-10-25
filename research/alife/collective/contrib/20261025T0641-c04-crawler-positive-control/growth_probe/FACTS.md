# Evidence pack: crawler (seed 0)

- world: `../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [256, 256]; wall 146s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/gr2 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 1.00
- tracks: 1; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 36.39 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 1.02/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [33.6343, -0.9999, None, -0.213]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.25, rim-vs-outside 0.83, heterogeneity 0.13; core [0.982, 0.135, 0.209, 0.699] rim [0.894, 0.372, 0.19, 0.716]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 96.8 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.969)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.77, rim/outside 23.7 (aggregate of 6 individuals; 3/6 membrane-like individually; rim level 0.235)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 43.7 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.427)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.672 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.627)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #0 (t=250, R_eq 80.11): ['|P| (actin polarization)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 4 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
