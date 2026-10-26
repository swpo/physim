# coevbits (c38): predator-prey particles with 20-bit matching genotypes

Fork of 20261026T0605-c38-coev-matching-o/coev.py: the 2-D trait becomes a 20-bit genotype (mutation flips each bit with
prob u = 0.003 at birth); capture success exp(-h^2/w^2), h = Hamming distance between the predator's and the prey's
genotype, w = 10 bits. Kinds = exact genotypes. Everything else (food, energy, division, pursuit) is unchanged.

Twins: `neutral=1` capture = constant p0 (the real run's realised mean success); `neutral=2` (shuffled twin) each attack
uses the genotype of a random living predator instead of the attacker's own, so prey-side selection and the spread of
success are kept but a predator's own genotype has no effect.

Reproduce (about 1 min per run; analysis 2-5 min):
    python drivebits.py b10 0 200000 '{"w":10}'
    python drivebits.py b10N 0 200000 '{"w":10,"neutral":1,"p0":<mean_success of data/b10_s0.json>}'
    python drivebits.py b10S 0 200000 '{"w":10,"neutral":2}'
    BWF=0.1 python twincal.py b10 b10N 0     # a* = 99.9th pct of the twin's early activity; late = windows >= 2
    BWF=0.1 python analyze.py b10 0 b10N     # RB shadows (NSH, LC env vars); BWF=0.1 makes kinds exact genotypes
    python bitsfig.py b10 0 b10N; python sumfig.py
Long run: MAXLOG=8000000 python drivebits.py b10L 0 700000 '{"w":10}' (and its b10LN twin).
`pack/` is a labkit run of world.py (seeds 0, 1; 10000 steps): spatial ecology only.
