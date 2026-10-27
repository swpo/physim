# Q:marangoni-swimmer-spread, loop 3 (c50): a supply only movers reach (food flashes)

Loops 1-2 (20261027T0000-c50-marangoni-spread-loop1, 20261027T0105-c50-marangoni-spread-loop2) found that growing sink discs
select the faster kind without selecting distance per cycle. Loop 3 adds a supply that should reward travel: **food flashes**.
world.py = the loop-1 world plus a second Poisson stream (seeded only by the run seed) of patches of radius 12 px that open for
100 t, one per 25 t (about 13% of the domain open at a time); inside an open patch the chemostat rate is 5x (kfood 5), same
target, so patches speed growth but do not nucleate droplets. Sink discs, ladder, founders (all mar 40), mutation as before.
Arms: E (MARS 20/40/60) and the identical-event twin (MARS 40/40/40), fresh seeds 502 and 503, 128^2, T=2000.
Readouts as before (an.sh: extract.py, spread_stats.py, fate_kind.py); out/, trait_food.png.

| arm | trait mean t 1000 / 1600 / 2000 | bodies min / end | M passers (rod lengths, rear tip) | sqrt-area passers | escape share | D gradient | persistent splits k0/k1/k2 |
|---|---|---|---|---|---|---|---|
| E+food s502 | 45.0 / 55.4 / **60.0** | 4 / 8 | **0 of 10** | 6 of 10 | 0.66 | -0.29 [-1.04, +0.13] | 0/13/11 |
| twin+food s502 | 44.0 / 48.0 / 46.7 | 5 / 6 | 2 of 20 | 12 of 20 | 0.64 | -0.03 [-0.19, +0.62] | 1/21/7 |
| E+food s503 | 37.1 / 42.5 / 36.0 | 5 / 5 | 1 of 13 | 10 of 13 | 0.62 | -0.04 [-0.29, +0.29] | 5/8/8 |
| twin+food s503 | 40.0 / 37.8 / 20.0 | 2 / 2 | 1 of 11 | 6 of 11 | 0.65 | +0.48 [-0.08, +1.13] | 2/10/5 |

## What it shows

1. **Food flashes do not reward distance per cycle.** The M-gate share stays at 0-10% in both arms on both seeds, and the
   selection gradient on D is not positive in E (-0.29, -0.04).
2. **They reward speed, and speed shortens the cycle.** In E (both seeds pooled) the mar-60 kind's dividing rods swim at a
   median path speed of 0.38 against 0.24 (mar 40) and 0.20 (mar 20), but divide after 125 t against 235 t and 210 t, so
   their distance per cycle (median D 1.80) is no larger than mar 40's (2.00); speed vs cycle Spearman -0.39 (p 0.06, n 23).
   On seed 502 the mar-60 kind goes to fixation in E (trait mean 60, 8 of 8 bodies; 11 of 24 births from mar-60 parents)
   while the twin's label sits at 47. On seed 503 no kind wins in E (36 at the end) and the twin falls to 2 bodies.
3. **Populations are smaller, not larger**: the patches did not lift the body count (min 2-5, end 2-8 against 4-25 in loops
   1-2), so single lineages decide every curve.
4. Heredity bookkeeping holds: 0-1 changes outside logged mutations per run (1 of 54 in total), 2-3 off-kind daughters per 33-58.

## Reading

Across three environments (slow discs, fast discs, food flashes), what pays is swimming fast, and in this world a faster rod
that finds more supply also divides sooner: distance per cycle, the quantity the challenge's M gate counts, is conserved or
falls. The challenge's capability will not spread by selecting the Marangoni coefficient alone unless the environment rewards
travel without rewarding growth: for example a supply that a rod can use only after it has moved (food that appears at a
distance from where it was born), or a division threshold that a body can reach only by collecting several patches.
Loop 4 adds the matched no-food runs on seeds 502 and 503 and two more paired seeds of the plain design, so that the trait-mean
comparison (E above the twin on seeds 500 and 501) can be judged on four paired seeds.

## Limits

Two seeds; 10-20 dividing tracks per arm; no no-food run on these seeds yet (loop 4). The patch edges are sharp: the explicit
food term on the spectral grid shows faint ringing in the surfactant channels near patch edges (sheet at t=605, t=1830),
which may affect rods sitting on an edge. The twin shares random streams but not bodies.
