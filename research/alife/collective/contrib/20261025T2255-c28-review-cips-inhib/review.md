# Review of 20261025T2130-c23-cips-inhibitor-arrest (finding: a catalysis-made inhibitor arrests CIPS coarsening; no division)

Written before reading other reviews. The claimed world.py unchanged; inhibitor arm `WORLD_P={"DI":0.1,"dI":0.01,"kI":0.2,"KI":0.5}`
(the finding's p_c/p_c1 parameters), matched twin `{"kI":0}`; fresh seeds 5 and 6, 128^2, run twice as long as the
claim (600 frames, t = 6000); dt/2 (`"dt":0.05`, spf 200, t = 3000) on seed 5 for both arms.

Body counts (labkit components):

| run | max | t=1500 | t=3000 | t=4500 | t=6000 | merges | splits |
|---|---|---|---|---|---|---|---|
| inhibitor s5 | 43 | 40 | 37 | 35 | 33 | 11 | 0 |
| inhibitor s6 | 44 | 41 | 34 | 32 | 30 | 10 | 0 |
| no inhibitor s5 | 73 | 55 | 47 | 40 | 35 | 40 | 0 |
| no inhibitor s6 | 78 | 53 | 45 | 40 | 34 | 42 | 0 |
| inhibitor s5, dt/2 | 43 | 40 | 37 | | | 7 | 0 |
| no inhibitor s5, dt/2 | 74 | 55 | 47 | | | 29 | 0 |

What replicates: the inhibitor delays nucleation, starts the population lower (43-44 vs 73-78), cuts merges about
4x, and no droplet ever splits (0 splits in all runs; sheet rerun/inh/seed6 shows round droplets that never elongate
past a cap). dt/2 gives the same counts to the unit.

What does not: the count is not flat from t~1500. From t=1500 to 3000 it falls 40 -> 37 and 41 -> 34 (seed 6 falls
17%, as fast as the twins' 15%). It keeps falling to t=6000 (-18% and -27% from t=1500) by dissolution of small
droplets (few merges; the sheet shows small droplets fading), and the twins (-36%) almost catch up: 33/30 vs 35/34
bodies at t=6000. So the inhibitor slows coarsening and changes its route (ripening instead of merging), but on my
seeds it does not arrest it at a fixed size within the time I ran.

Verdict: Weak. The negative part (no division with a conserved enzyme) is supported; the arrest is not reproduced.
