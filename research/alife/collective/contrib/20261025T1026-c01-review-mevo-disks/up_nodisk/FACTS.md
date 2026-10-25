# Evidence pack: membrane-evo-up (seed 24)

- world: `../world_up_nodisk.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1026-c01-review-mevo-disks/world_up_nodisk.py --out collective/contrib/20261025T1026-c01-review-mevo-disks/up_nodisk --seeds 24 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6833], min area 6 px

## Measurements
- components: final 4, mean 3.6, max 17; occupancy final 0.24
- tracks: 22; persistent (alive >= 50% of run): 4; longest 135 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.95 (1 = constant size)
- enclosures: components with a hole mean 3.12, final 4; holes at thresholds 0.2/0.35/0.5 final [4, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 4, 4], H1 [4, 4, 4]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 5000, default): splits 1, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5981, None, 0.4314, -0.3236]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 3.18 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.303)
  - radial K2: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.41 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.184)
  - radial L link: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 1.63 (aggregate of 24 individuals; 4/24 membrane-like individually; rim level 0.371)
  - radial membrane (wall): peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 14.4, rim/outside 0.688 (aggregate of 24 individuals; 6/24 membrane-like individually; rim level 0.153)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=23250, R_eq 15.59, ring): none; #18 (t=23250, R_eq 19.27, ring): none; #19 (t=23250, R_eq 17.71, ring): none; #20 (t=23250, R_eq 15.46, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 24 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
