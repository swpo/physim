# Evidence pack: active-nematic-marangoni (seed 2)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 421s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0505-c34-nematic-marangoni/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8414, 0.5692], min area 6 px

## Measurements
- components: final 31, mean 23.1, max 31; occupancy final 0.09
- tracks: 98; persistent (alive >= 50% of run): 11; longest 178 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.68 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.249/time; max body lengths 14.2
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.316, nucleations 10
- channel total drift (end/start - 1): [-0.5106, -0.4179, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 113: holes 0, rim-vs-core 0.71, rim-vs-outside 0.33, heterogeneity 0.24; core [0.951, 0.643, 0.422, 0.437] rim [0.742, 0.404, 0.903, 0.015]
  - track 12 at frame 113: holes 0, rim-vs-core 0.65, rim-vs-outside 0.34, heterogeneity 0.20; core [0.922, 0.744, 0.457, 0.426] rim [0.751, 0.495, 0.861, 0.016]
  - track 30 at frame 128: holes 0, rim-vs-core 0.66, rim-vs-outside 0.32, heterogeneity 0.22; core [0.944, 0.793, 0.404, 0.392] rim [0.749, 0.505, 0.818, 0.01]
  - track 70 at frame 156: holes 0, rim-vs-core 0.65, rim-vs-outside 0.43, heterogeneity 0.24; core [0.951, 0.881, 0.388, 0.504] rim [0.789, 0.594, 0.768, 0.099]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 153 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.68 (aggregate of 153 individuals; 0/153 membrane-like individually; rim level 0.72)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 9.37 (aggregate of 153 individuals; 6/153 membrane-like individually; rim level 0.556)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 3.25 (aggregate of 153 individuals; 66/153 membrane-like individually; rim level 0.592)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.502, rim/outside 2.27 (aggregate of 153 individuals; 13/153 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=565, R_eq 4.18): ['order |Q|']; #12 (t=565, R_eq 4.75): ['cargo c']; #30 (t=640, R_eq 3.91): none; #70 (t=780, R_eq 3.78): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
