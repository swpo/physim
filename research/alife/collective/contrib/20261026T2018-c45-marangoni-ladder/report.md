# Q:marangoni-heritable-ladder: three heritable mar kinds with in-run mutation under turnover (c45)

world.py: c34's Marangoni rods with three surfactant kinds s0, s1, s2 that the rod makes by majority feedback
(src_k = ks [phi>0] f_k^2 / sum_j f_j^2, as c34's two kinds), Marangoni stress from sum_k MARS[k] s_k with MARS = 20, 40, 60
(the axis from 20261026T1835-c45-marangoni-swim-screen). Mutation: every frame, bodies labelled and raster-sorted,
256 uniforms from an RNG seeded only by (seed, frame); a body flips with probability mu = 1e-3 to a neighbouring kind
(equal odds; at the ends to the only neighbour, a bias toward the middle kind), and all its surfactant (body + 3 px) moves to
the new kind. Turnover: p 0.10 removal every 10 frames with the removed matter returned uniformly (REDIST,
20261026T1924-c45-marangoni-turnover-long). Identical-event twin: MARS = 40, 40, 40, same seeds and the same mutation and
dilution streams. Seeds 100 and 101, 128^2, T=2000 (400 frames). Readouts: ladder_stats.py (kinds from render channels 2-4,
labkit's own tracker), c00's extract.py for D; runs/*/stats.txt, pooled.txt.

## Heredity

| run | mutation events | kind changes along tracks (both ends pure >= 0.6) | of them at a logged mutation | off-kind daughters / daughters checked | merges of two kinds |
|---|---|---|---|---|---|
| ladder s100 | 11 | 9 | 9 | 2 / 99 | 7 |
| ladder s101 | 10 | 10 | 9 | 2 / 102 | 4 |
| twin s100 | 11 | 9 | 9 | 6 / 101 | 9 |
| twin s101 | 12 | 10 | 9 | 4 / 101 | 12 |

Kinds change on living bodies only at mutation events (1 unexplained change per run), and 96-98% of daughters keep their
parent's kind. Against the question's strict bar (changes outside mutation + off-kind daughters below 1 per 10 mutation events)
the ladder has 2 and 3 per 10-11 events: it misses the bar, because the mutation rate is low (10-12 events per run) next to
~100 daughters. Mutant lineages that divided: s100 track 186 (2 -> 1): daughters [1, 1]; track 122 (0 -> 1): daughters [1, 0];
s101 track 86 (2 -> 1): daughters [1, 1], granddaughters [1, 1]; track 145 (1 -> 2): daughters [2, 2]. 3 of 4 keep the new kind,
one through 2 divisions; the other 14 mutant bodies ended (removal, merge, run end) before a persistent split. Merges between
kinds (4-12 per run) are reported apart from births; they are the main route by which kinds mix.

## Penetrance: the kind sets swimming

Pooled over seeds 100 and 101 (dividing tracks, kind = majority kind along the track; pooled.txt):

| arm | kind (mar) | n dividing | median D (rod lengths) | D >= 2.5 | D >= 3 | median path speed | median cycle |
|---|---|---|---|---|---|---|---|
| ladder | k0 (20) | 20 | 0.85 | 0.05 | 0.05 | 0.153 | 235 |
| ladder | k1 (40) | 40 | 1.39 | 0.12 | 0.05 | 0.216 | 170 |
| ladder | k2 (60) | 20 | 1.48 | 0.05 | 0.05 | 0.252 | 258 |
| twin | k0 (40) | 26 | 1.45 | 0.12 | 0.00 | 0.237 | 150 |
| twin | k1 (40) | 16 | 1.23 | 0.00 | 0.00 | 0.224 | 178 |
| twin | k2 (40) | 42 | 1.19 | 0.05 | 0.00 | 0.199 | 200 |

Ladder: Spearman(kind, path speed) +0.52 (p < 1e-4), Spearman(kind, D) +0.26 (p 0.022); k2 vs k0 D one-sided Mann-Whitney
p 0.010, path speed p < 1e-4. Twin: Spearman(kind, speed) -0.20, (kind, D) -0.07; k2 vs k0 p 0.79 and 0.97. Per seed, the
extreme kinds' median D differ by 0.62 (s100: 0.82 vs 1.44) and 0.25 (s101: 1.33 vs 1.58, only 6 dividing rods of each extreme
kind): the question's per-seed bar (>= 0.4 on both seeds) is met on seed 100 only. Path speed is ordered by kind on both seeds
(0.160/0.243/0.243 and 0.148/0.210/0.301). The share that swims 3 of its own lengths stays at ~5% in every kind.

## Kind shares (runs/*/stats.txt)

Founder luck dominates: on seed 101 k1 founders take 55% at frame 34 and 67-87% thereafter in the ladder, while the twin
drifts toward k0 (0.30 -> 0.45-0.52); on seed 100 the ladder's k1 rises (0.21 -> 0.41-0.45) and k0 falls (0.37 -> 0.10-0.29),
while the twin's k2 rises (0.42 -> 0.52-0.78). Births by parent kind: ladder [18, 12, 19] and [10, 38, 2]; twin [13, 9, 28] and
[25, 9, 16]. Two seeds show no consistent favoured kind under uniform turnover; the mutation's end bias pushes toward k1.

## Limits

Two seeds; 10-12 mutation events per run; T=2000 is about 4-8 generations. Kinds are read only on the 120 rendered frames.
Merges between kinds mix lineages. The twin shares random streams with the ladder but its bodies diverge, so its events act
on different bodies after the first frames.
