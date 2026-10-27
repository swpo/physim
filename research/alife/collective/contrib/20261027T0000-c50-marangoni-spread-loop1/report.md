# Q:marangoni-swimmer-spread, loop 1 (c50): one fresh seed, four arms

**World** (world.py): c45's three-kind Marangoni ladder (20261026T2018-c45-marangoni-ladder: surfactant kinds s0/s1/s2 with
Marangoni coefficients 20/40/60, made by the rods with majority feedback, in-run mutation between neighbouring kinds that
moves a body's surfactant to the new kind) in c45's dense sink-disc environment (20261026T2123-c45-marangoni-sink-escape-dense:
growing discs that lower the chemostat target, one per 50 t, R 24, 0.08 px/t). Changes: all founders of the middle kind
(initial surfactant noise only in s1), mutation 2.5e-3 per body per frame (about 10% per median cycle), no random dilution
(the discs are the turnover). Unstructured start (sheet frame t=0). 128^2, T=2000, seed 500 (fresh).

**Arms** (same seed, so the same initial field, disc stream and mutation uniforms): **E** (escape: discs only lower the supply);
**C** (no-escape: bodies whose centroid lies within R of a disc's centre when it opens are removed); **twin** (E with
MARS 40/40/40: kind labels with no effect, the identical-event twin); **off** (E with MARS 0/0/0: drive off).

Readouts: c00's extract.py (dividing tracks, D in own rod lengths), spread_stats.py (kinds from render channels 2-4, trait mean,
kind shares, births/merges/conversions/off-kind daughters, the M gate with the rear-tip test, cohorts, descendants),
fate_kind.py (c45's fate.py plus the caught body's kind). Outputs in out/.

## Pre-registered trait: mean ladder value (20/40/60) of living bodies (trait_s500.png)

| arm | t 200 | t 600 | t 1000 | t 1400 | t 1800 | t 2000 | bodies at t 1400 / 2000 |
|---|---|---|---|---|---|---|---|
| E | 36.9 | 38.8 | 38.6 | 42.1 | 43.1 | 45.7 | 19 / 7 |
| C | 37.5 | 38.0 | 36.9 | 41.4 | 40.0 | 60 (1 body) | 9 / 1 |
| twin | 36.9 | 38.8 | 34.3 | 35.0 | 36.4 | 36.7 | 24 / 6 |
| off | 36.4 | 38.6 | 35.0 | 35.7 | 31.4 | 40.0 | 10 / 5 |

In E the mar-60 kind appears by mutation at t~700 and holds 20-33% of bodies from t 1300 to the end; in the twin the k2 label
stays at 0-8% and k0 rises instead (the k1 -> k0 mutations); in off k2 never establishes. In C the population collapses
to one body at t~1850 (the removal arm loses the removed matter; 29 bodies removed), so its late trait mean is one body.

## The capability: dividing rods that swim 3 of their own lengths (rear tip >= 2/3 of net)

| arm | dividing tracks | pass (rod lengths) | pass (sqrt area) | median D | persistent splits |
|---|---|---|---|---|---|
| E | 17 | 1 of 17 | 10 of 17 | 1.62 | 31 |
| C | 14 | 0 of 14 | 7 of 14 | 1.50 | 25 |
| twin | 17 | 2 of 17 | 11 of 17 | 1.73 | 32 |
| off | 18 | 0 of 18 | 2 of 18 | 0.60 | 23 |

The passing share does **not** rise in E: 1 of 17, born at frames 114-170, and no passer in any later cohort (out/E_s500.txt);
the twin has 2 of 17. The k2 rods that spread in E are not passers (0 dividing k2 rods; the k2 bodies alive late had not
divided yet or did not divide twice). Drive-off makes no passers (0 of 18) and moves little (median D 0.60).

## Escape and kinds

Bodies inside a disc's final radius one frame after it opened (fate_kind.py): E 44 caught, 25 escape (0.57; c45: 0.53-0.56);
by kind k0 0/3, k1 23/35, k2 1/2. Twin 45 caught, 32 escape (0.71), its k0 label 6/10. Off 28 caught, 7 escape (0.25).
Selection gradient of relative descendants on standardized D (c45's regression, n 17 per arm): E +0.001 [-0.19, +0.40],
twin +0.12 [-0.08, +0.52], C -0.07 [-0.55, +0.15], off -0.23 [-1.08, -0.09].

## Heredity bookkeeping (out/*_s500.txt)

| arm | mutation events | kind changes along tracks / at a mutation | persistent splits by parent kind k0/k1/k2 | off-kind daughters | merges of two kinds |
|---|---|---|---|---|---|
| E | 14 | 14 / 14 | 3/26/2 | 1 of 62 | 5 |
| C | 8 | 6 / 6 | 1/22/1 | 3 of 48 | 2 |
| twin | 15 | 14 / 14 | 8/21/1 | 1 of 59 | 10 |
| off | 7 | 6 / 6 | 2/20/0 | 2 of 44 | 2 |

No conversions outside mutation events. E had 6 k1 -> k2 mutations against 3 in the twin (the streams are shared but the
bodies diverge), so part of E's k2 rise is mutation supply, not selection.

## Against the loop's bar

The question's bar: on every seed, the trait mean and the late passing share rise more in E than in C and in the twin.
Seed 500: **trait mean yes** (E +5.7 at the end, +2 to +6 from t 1400; twin -3.3; C cannot be read after its collapse),
**passing share no** (E 1/17 with none late, twin 2/17, C 0/14). The loop does not pass.

## Reading

The dense-disc environment again favours the faster kind as a body (k1 escapes 23/35, k0 0/3), and the trait mean drifts up
in E only, but distance per cycle is still not rewarded (D gradient +0.00), and the kind that rises (mar 60) does not swim 3
of its lengths between birth and division any more often than mar 40. Escaping a disc is about speed while caught; passing the
M gate is about distance per cycle, which longer cycles inflate and the discs truncate. So this environment can select
the trait without selecting the capability. Next loop (per the question's own instruction): find an environment that rewards
distance before adding seeds; first screen: discs that grow twice as fast (disc_v 0.16), at 1 per 50 t and 1 per 100 t.

## Limits

One seed, small populations (6-25 bodies; all arms fall in the last 300 t, where the shared disc stream clusters), 1-2
passers per arm. C is not population-matched to E: removal destroys matter, so C collapses. Kinds are read only on the 120
rendered frames. The twin shares random streams but its bodies diverge after the first frames.
