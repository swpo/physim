# Evidence pack: active-nematic-marangoni (seed 3)

- world: `../../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [192, 192]; wall 470s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/rods_converge/behav/dt0.05_n192 --seeds 3 4 --frames 120 --spf 100 --dt 0.05 --size 192 192 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8268, 0.6262], min area 6 px

## Measurements
- components: final 24, mean 11.1, max 24; occupancy final 0.09
- tracks: 51; persistent (alive >= 50% of run): 3; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.48 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 24, 21], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.496/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.087, nucleations 3
- channel total drift (end/start - 1): [-0.5037, -0.3265, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 66: holes 0, rim-vs-core 0.85, rim-vs-outside 0.45, heterogeneity 0.25; core [0.97, 0.77, 0.334, 0.696] rim [0.772, 0.481, 0.782, 0.063]
  - track 15 at frame 89: holes 0, rim-vs-core 0.88, rim-vs-outside 0.44, heterogeneity 0.26; core [0.97, 0.738, 0.339, 0.669] rim [0.759, 0.456, 0.843, 0.038]
  - track 18 at frame 90: holes 0, rim-vs-core 0.78, rim-vs-outside 0.42, heterogeneity 0.24; core [0.95, 0.707, 0.398, 0.636] rim [0.761, 0.492, 0.826, 0.05]
  - track 23 at frame 98: holes 0, rim-vs-core 0.82, rim-vs-outside 0.23, heterogeneity 0.26; core [0.922, 0.846, 0.448, 0.507] rim [0.693, 0.496, 0.94, 0.005]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 4.87 (aggregate of 79 individuals; 1/79 membrane-like individually; rim level 0.694)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 8.98 (aggregate of 79 individuals; 8/79 membrane-like individually; rim level 0.572)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.3 (aggregate of 79 individuals; 38/79 membrane-like individually; rim level 0.562)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.486, rim/outside 4.8 (aggregate of 79 individuals; 13/79 membrane-like individually; rim level 0.204)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=330, R_eq 7): none; #15 (t=445, R_eq 7.14): ['surfactant s']; #18 (t=450, R_eq 6.84): ['cargo c']; #23 (t=490, R_eq 5.5): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 79 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
