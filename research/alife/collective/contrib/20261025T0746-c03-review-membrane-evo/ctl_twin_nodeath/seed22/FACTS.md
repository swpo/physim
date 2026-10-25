# Evidence pack: membrane-evo (seed 22)

- world: `../../twin_nodeath.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 100s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/evo/twin_nodeath.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/evo/twin_nodeath/seed22 --seeds 22 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6897], min area 6 px

## Measurements
- components: final 4, mean 3.6, max 13; occupancy final 0.20
- tracks: 17; persistent (alive >= 50% of run): 4; longest 135 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.38 (1 = constant size)
- enclosures: components with a hole mean 3.47, final 4; holes at thresholds 0.2/0.35/0.5 final [4, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 4, 4], H1 [4, 4, 4]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 5000, default): splits 1, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.7718, None, 0.2503, -0.4116]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.7 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.298)
  - radial K2: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.37 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.23)
  - radial L link: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 2.43 (aggregate of 24 individuals; 2/24 membrane-like individually; rim level 0.397)
  - radial membrane (wall): peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 19.9, rim/outside 1.05 (aggregate of 24 individuals; 4/24 membrane-like individually; rim level 0.19)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=23250, R_eq 16.5, ring): none; #14 (t=23250, R_eq 16.38, ring): none; #15 (t=23250, R_eq 16.04, ring): none; #16 (t=23250, R_eq 16.24, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 24 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
