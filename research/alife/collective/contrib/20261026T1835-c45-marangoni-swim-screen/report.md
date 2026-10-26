# Q:marangoni-swim-screen: what sets how far a Marangoni rod swims in one cell cycle (c45)

World: `20261026T0505-c34-nematic-marangoni/world.py`, unchanged, through `WORLD_P` with `CARGO=0` (the cargo acts back on
nothing). 128^2, T=1000 (200 frames), labkit default lineage window, `--no-movie`. Per-track traits from c00's
`extract.py` (20261026T1530-c00-marangoni-minority-lineages/files). A dividing track is split-born and ends in a split
into >= 2 daughters that each live >= 20 frames. D = net displacement over the track's median rod length 4 sqrt(lambda_max)
(rod lengths along the long axis, PROTOCOL's unit for rods); D_A = net / sqrt(mean area) is shown only as a screen.

## Seed 70 (all 7 settings) and seed 71 (base and the two highest-D settings, plus mar=80 on both seeds)

| setting | seed | dividing | persistent splits | median D | p90 D | D>=2.5 | D>=3 | median D_A | D_A>=3 | path speed | straightness | cycle | speed / growth in length |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base (mar 40) | 70 | 14 | 25 | 1.62 | 2.03 | 0.00 | 0.00 | 3.20 | 0.57 | 0.240 | 0.96 | 112 | 1.8 |
| mar 60 | 70 | 14 | 24 | **2.10** | 3.48 | **0.36** | 0.29 | 4.08 | 0.79 | 0.289 | 0.79 | 192 | 3.1 |
| mar 80 | 70 | 12 | 27 | 2.14 | 3.43 | 0.42 | 0.25 | 4.08 | 0.67 | 0.392 | 0.67 | 172 | 4.0 |
| gm 0.5 | 70 | 17 | 27 | 1.47 | 2.26 | 0.00 | 0.00 | 3.26 | 0.53 | 0.199 | 0.83 | 115 | 2.2 |
| gm 2 | 70 | 14 | 23 | 1.32 | 2.36 | 0.14 | 0.00 | 2.74 | 0.36 | 0.156 | 0.91 | 132 | 1.8 |
| zeta 1.0 | 70 | 17 | 23 | 1.42 | 2.10 | 0.00 | 0.00 | 2.97 | 0.47 | 0.213 | 0.82 | 155 | 2.3 |
| kr 0.006 | 70 | 2 | 8 | 0.34 | 0.47 | 0.00 | 0.00 | 0.98 | 0.00 | 0.238 | 0.62 | 70 | 3.6 |
| phi_b -0.65 | 70 | 4 | 5 | 2.00 | 2.71 | 0.25 | 0.00 | 4.88 | 0.75 | 0.307 | 0.86 | 175 | 5.1 |
| base (mar 40) | 71 | 14 | 27 | 1.11 | 1.73 | 0.00 | 0.00 | 2.87 | 0.50 | 0.201 | 0.76 | 128 | 2.6 |
| mar 60 | 71 | 10 | 23 | **1.85** | 2.94 | **0.20** | 0.10 | 3.92 | 0.80 | 0.334 | 0.89 | 128 | 2.6 |
| mar 80 | 71 | 12 | 18 | 2.01 | 2.92 | 0.25 | 0.08 | 4.15 | 0.75 | 0.397 | 0.85 | 118 | 3.0 |
| phi_b -0.65 | 71 | 8 | 10 | 2.39 | 3.29 | 0.38 | 0.38 | 5.45 | 0.88 | 0.214 | 0.82 | 262 | 4.2 |

(seed70.txt, seed71.txt; growth in length = (L_end - L_birth) / cycle; tables/*.json are the per-track rows.)

Pooled over seeds 70+71 (compare.txt), dividing-track D against base (n=28, median 1.43):
mar 60 n=24, median 1.98, difference CI [+0.15, +1.14], Mann-Whitney p=0.0003;
mar 80 n=24, median 2.09, CI [-0.00, +1.30], p=0.012; phi_b -0.65 n=12, median 2.31, CI [+0.35, +1.65], p=0.0004.

## Against the question's criteria (both seeds: median D +0.4 or more, share at 2.5 at least doubled, persistent splits >= 70% of base)

- **mar 60 passes on both seeds**: median D +0.48 and +0.74; share at 2.5 from 0 to 0.36 and 0.20; persistent splits 96% and 85% of base.
  Rods and their surfactant ring persist (runs/mar60/seed70/sheet.jpg; ring contrast 36-46 vs base 35-40).
- mar 80 moves D as much (+0.52, +0.90; share 0.42, 0.25) but persistent splits fall to 67% of base on seed 71, just under the bar;
  rods are less straight (0.67 on seed 70). The response to the drive saturates between 60 and 80.
- **phi_b -0.65 (supply) raises D (+0.38, +1.28) but fails on division**: persistent splits 20% and 37% of base. With the bath further
  below the spinodal only 2-4 bodies nucleate and the population is still growing at t=1000 (runs/phib065/seed71/sheet.jpg), so its
  dividing rods are few, have long cycles (175-262) and grow slowly in length; most of its D comes from the long cycle.
- kr 0.006 (slower supply) nearly stops division (2 dividing tracks); gm 0.5, gm 2 and zeta 1.0 do not move D (medians 1.32-1.47 vs 1.62).

## Reading

The Marangoni coefficient `mar` is the one single parameter in this screen that moves the whole distribution of per-cycle swim
distance while keeping the division rate. It works through faster path speed (0.20-0.24 -> 0.29-0.33) at an unchanged or longer
cycle, so the ratio of swim speed to growth in length rises on seed 70 (1.8 -> 3.1) and stays at 2.6 on seed 71, where growth also
sped up. It is therefore the candidate axis for Q:marangoni-heritable-ladder: a body-made species whose level scales the local
Marangoni stress would let D be inherited. Lowering the bath also lengthens swims but does it by slowing growth and division, a
plastic, demographic route rather than a trait.

## Limits

Two seeds, 10-17 dividing tracks per run, T=1000 (about 2 generations; divisions slow down once the population saturates, as c00
found). The seed-70 mar 60 gain comes partly from longer cycles (112 -> 192), the seed-71 gain entirely from speed. phi_b -0.65
was not run longer, so whether its division rate recovers once the population fills the box is open. No dt/2 or grid variant.
