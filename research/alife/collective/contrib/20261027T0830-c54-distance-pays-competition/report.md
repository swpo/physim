# Q:marangoni-distance-pays, loop 2 (c54): does birth-site depletion favour the faster heritable kind? Competition assay

Loop 1 (20261027T0725-c54-distance-pays-loop1) found that a depletion disc opened at every split site makes 40-55% of dividing
Marangoni rods swim 3 of their own lengths, but as a response of the ancestral mar-40 kind: mutants rarely reached division, so
the heritable trait had no variance to be selected. This loop gives it variance directly.

**World** (world.py = loop 1's world plus FOUNDER=-2): founders of the mar-40 (k1) and mar-60 (k2) kinds, laid as random 16 px
blocks of initial surfactant noise (each nucleating body takes one kind by the rods' own majority-feedback copying), mutation off.
Not a challenge design (the challenge needs one ancestral kind); it measures selection on the trait in each environment.
Arms, fresh seeds 610 and 611, 128^2, T=2000: **cdep** (depletion R 20, -0.7, 200 t, plus sink discs, ladder), **cdeptwin**
(same, MARS 40/40/40, so k2 is a neutral label with the same start), **cE** (sink discs only, ladder), **cEtwin**. Selection on
mar 60 in an environment = its share in the ladder arm minus the label's share in that environment's twin. comp.py, comp.txt.

## Results

| seed | arm | mar-60 share t<500 | t>=1000 | end | k1 dividers: M pass, median D | k2 dividers: M pass, median D |
|---|---|---|---|---|---|---|
| 610 | cdep | 0.75 | **0.51** | 0.40 | 1/5, 2.12 | 6/9, 3.57 |
| 610 | cdeptwin | 0.81 | 0.86 | 0.75 | 1/1, 3.53 | 7/14, 2.87 |
| 610 | cE | 0.80 | 0.66 | 0.46 | 2/7, 0.92 | 3/14, 1.23 |
| 610 | cEtwin | 0.80 | 0.81 | 0.80 | 1/3, 2.16 | 3/15, 1.47 |
| 611 | cdep | 0.11 | 0.00 | 0.00 | 5/17, 2.27 | - |
| 611 | cdeptwin | 0.11 | 0.00 | 0.00 | 8/11, 3.62 | - |
| 611 | cE | 0.10 | 0.21 | 0.15 | 2/13, 1.88 | 3/7, 2.62 |
| 611 | cEtwin | 0.10 | 0.00 | 0.00 | 1/17, 1.54 | - |

Selection on mar 60 (ladder minus twin, t >= 1000 / end): seed 610 depletion **-0.35 / -0.35**, sink discs only -0.15 / -0.34;
seed 611 depletion 0 / 0 (mar 60 lost by t 500 in both arms), sink discs only +0.21 / +0.15.

- The block founders do not give an even start: the rods' majority copying during nucleation turns 50/50 blocks into 75-81%
  mar 60 on seed 610 and 10-11% on seed 611 (same draw in all four arms of a seed).
- **Depletion does not favour mar 60.** On seed 610 (the only seed where both kinds persist under depletion) mar 60 falls
  steadily from 0.75 to 0.40 under depletion while its neutral twin label stays at 0.75-0.86; on seed 611 mar 60 is lost under
  depletion in the ladder and in the twin alike. With sink discs only, mar 60 falls on 610 and rises on 611.
- Mar-60 dividing rods do swim farther per cycle under depletion (seed 610: 6/9 pass, median D 3.57, vs mar 40 1/5, 2.12), so
  the kind that carries the capability more often is the one that loses. Per-kind bookkeeping (out/cdep_s610.txt): persistent
  splits k1/k2 7/13, vanishings 5/15, merges of two different kinds 7 (1 in the twin). So mar-60 bodies die (dissolve) more per
  split under depletion, and cross-kind merges are 7x as frequent; this loop does not separate which costs more.
- Drift and the direct effect of the environment are absorbed by the twins: the neutral label holds its share under depletion
  (seed 610), so the decline is a trait effect.

## Reading

Together with loop 1: the depletion rule makes distance per cycle pay at the level of the individual (rods that leave grow;
passing share 40-55%), yet the heritable trait that raises distance per cycle, a stronger Marangoni coefficient, is not
favoured and on one seed is clearly disfavoured. Stronger Marangoni stress costs something here that outweighs the escape
benefit: mar-60 bodies dissolve more often (15 vanishings per 13 splits against 5 per 7). A candidate reason, untested: a
stronger tangential stress elongates and thins a rod (median D is higher but bodies are smaller), so in a lowered supply it
crosses the dissolution threshold sooner. Distance pays, but the trait that buys distance is not cheap in this world.

## Limits

Two seeds, one of which (611) is uninformative under depletion because mar 60 was lost by t 500 in both arms. 9-18 bodies.
Founders are not balanced by the block draw; a balanced start would need a field-level placement (e.g. alternating halves).
Kinds are read from rendered frames only (purity >= 0.6). The death and merge counts per kind are single-seed. Mutation off
(this is a selection assay, not a challenge design). Grid-scale ripples around high-surfactant mar-60 bodies (loop 1's limit)
were not tested and could bear on mar-60 survival.
