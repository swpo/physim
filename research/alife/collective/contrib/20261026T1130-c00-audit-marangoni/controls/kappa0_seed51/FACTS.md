# Evidence pack: active-nematic-marangoni-kappa0 (seed 51)

- world: `../../variants/active-nematic-marangoni-kappa0.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 487s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni/variants/active-nematic-marangoni-kappa0.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni/controls/kappa0_seed51 --seeds 51 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8407, 0.5767], min area 6 px

## Measurements
- components: final 31, mean 23.3, max 32; occupancy final 0.09
- tracks: 120; persistent (alive >= 50% of run): 11; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.291/time; max body lengths 9.5
- replication (lineage window K = 20 frames = time 100, default): splits 45, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 4, merges 21, merge/split ratio 0.467, nucleations 8
- channel total drift (end/start - 1): [-0.5063, -0.4035, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 124: holes 0, rim-vs-core 0.60, rim-vs-outside 0.34, heterogeneity 0.17; core [0.97, 0.598, 0.341, 0.898] rim [0.77, 0.417, 0.879, 0.853]
  - track 45 at frame 136: holes 0, rim-vs-core 0.45, rim-vs-outside 0.41, heterogeneity 0.15; core [0.93, 0.806, 0.416, 0.853] rim [0.759, 0.562, 0.756, 0.83]
  - track 47 at frame 136: holes 0, rim-vs-core 0.61, rim-vs-outside 0.32, heterogeneity 0.16; core [0.956, 0.516, 0.393, 0.917] rim [0.754, 0.327, 0.933, 0.874]
  - track 65 at frame 151: holes 0, rim-vs-core 0.51, rim-vs-outside 0.37, heterogeneity 0.14; core [0.94, 0.865, 0.37, 0.88] rim [0.751, 0.573, 0.748, 0.845]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.777, rim/outside 4.53 (aggregate of 155 individuals; 1/155 membrane-like individually; rim level 0.695)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 8.81 (aggregate of 155 individuals; 14/155 membrane-like individually; rim level 0.527)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.22 (aggregate of 155 individuals; 77/155 membrane-like individually; rim level 0.58)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 1.26 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.767)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=620, R_eq 4.26): none; #45 (t=680, R_eq 3.99): none; #47 (t=680, R_eq 4.51): ['order |Q|']; #65 (t=755, R_eq 3.87): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
