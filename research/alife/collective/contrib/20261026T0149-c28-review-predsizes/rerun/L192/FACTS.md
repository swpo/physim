# Evidence pack: eco-lenia2 (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 301 frames x 40 steps x dt 0.1 = time 1200; grid [192, 192]; wall 861s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py --out /tmp/claude-0/c28ps/L192 --seeds 5 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 45, mean 35.4, max 68; occupancy final 0.18
- tracks: 831; persistent (alive >= 50% of run): 31; longest 207 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.36 (1 = constant size)
- enclosures: components with a hole mean 0.34, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [67, 50, 45], H1 [1, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.158/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 80, default): splits 270, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 2, merges 124, merge/split ratio 0.459, nucleations 168
- channel total drift (end/start - 1): [28.9709, 20.7175, 14.0838, None, None, None, -0.1324]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 571 at frame 199: holes 0, rim-vs-core 0.53, rim-vs-outside 0.98, heterogeneity 0.15; core [1.0, 0.673, 0.539, 0.0, 0.0, 0.0, 0.76] rim [0.895, 1.0, 0.142, 0.0, 0.0, 0.0, 0.784]
  - track 575 at frame 199: holes 0, rim-vs-core 0.43, rim-vs-outside 0.97, heterogeneity 0.15; core [1.0, 0.664, 0.438, 0.0, 0.0, 0.0, 0.758] rim [0.903, 0.987, 0.175, 0.0, 0.0, 0.0, 0.782]
  - track 592 at frame 202: holes 0, rim-vs-core 0.36, rim-vs-outside 0.92, heterogeneity 0.15; core [1.0, 0.736, 0.375, 0.0, 0.0, 0.0, 0.726] rim [0.835, 1.0, 0.196, 0.0, 0.0, 0.0, 0.753]
  - track 744 at frame 222: holes 0, rim-vs-core 0.37, rim-vs-outside 0.93, heterogeneity 0.15; core [1.0, 0.683, 0.333, 0.0, 0.0, 0.0, 0.776] rim [0.843, 0.971, 0.171, 0.0, 0.0, 0.0, 0.799]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 242 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 62 (aggregate of 242 individuals; 1/242 membrane-like individually; rim level 0.951)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.93, rim/outside 11.3 (aggregate of 242 individuals; 195/242 membrane-like individually; rim level 0.937)  MEMBRANE-LIKE
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.451, rim/outside 5.18 (aggregate of 242 individuals; 16/242 membrane-like individually; rim level 0.331)
  - radial B0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.57 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.0215)
  - radial B1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 1.28 (aggregate of 242 individuals; 4/242 membrane-like individually; rim level 0.0224)
  - radial B2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 1.46 (aggregate of 242 individuals; 6/242 membrane-like individually; rim level 0.0238)
  - radial F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.922 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.67)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #571 (t=796, R_eq 6.72): ['A1']; #575 (t=796, R_eq 6.84): ['A1']; #592 (t=808, R_eq 6.96): ['A1']; #744 (t=888, R_eq 6.89): ['A1']
- species `A` (channels ['A0'], own threshold): components final 45, mean 33.8, max 49; tracks 503, persistent 31; splits 169, persistent splits 16 (K=20), max generation 2, merges 73, merge/split 0.432; moving tracks 2
- species `B` (channels ['B0'], own threshold): components final 0, mean 1.8, max 40; tracks 308, persistent 0; splits 94, persistent splits 0 (K=20), max generation 0, merges 40, merge/split 0.426; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
