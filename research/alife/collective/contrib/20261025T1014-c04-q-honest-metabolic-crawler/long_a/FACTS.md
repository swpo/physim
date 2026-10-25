# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [256, 256]; wall 719s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/long_a --seeds 1 --frames 400 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9969], min area 6 px

## Measurements
- components: final 0, mean 4.0, max 17; occupancy final 0.00
- tracks: 109; persistent (alive >= 50% of run): 0; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.847/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 0.364, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, None, -0.5735]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 131: holes 0, rim-vs-core 0.39, rim-vs-outside 0.39, heterogeneity 0.08; core [0.795, 0.239, 0.009, 0.192] rim [0.421, 0.34, 0.005, 0.21]
  - track 106 at frame 289: holes 0, rim-vs-core 0.41, rim-vs-outside 0.37, heterogeneity 0.08; core [0.828, 0.208, 0.01, 0.133] rim [0.426, 0.288, 0.005, 0.147]
  - track 99 at frame 282: holes 0, rim-vs-core 0.20, rim-vs-outside 0.49, heterogeneity 0.08; core [0.797, 0.238, 0.009, 0.132] rim [0.593, 0.238, 0.007, 0.138]
  - track 18 at frame 104: holes 0, rim-vs-core 0.42, rim-vs-outside 0.35, heterogeneity 0.08; core [0.847, 0.176, 0.011, 0.092] rim [0.428, 0.244, 0.006, 0.104]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [67, 134, 202, 266]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 5.27 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.683)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.9, rim/outside 6 (aggregate of 31 individuals; 27/31 membrane-like individually; rim level 0.241)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 1.53 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.0113)
  - radial n (nutrient): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.96 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.14)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #24 (t=655, R_eq 19.78): ['|P| (actin polarization)']; #106 (t=1445, R_eq 20.3): ['|P| (actin polarization)']; #99 (t=1410, R_eq 20.19): ['|P| (actin polarization)']; #18 (t=520, R_eq 20.82): ['|P| (actin polarization)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
