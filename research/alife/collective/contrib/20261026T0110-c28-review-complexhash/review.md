# Review of 20261026T0115-c30-complex-hash-contests (O finding: zero-sum hash turns over without novelty; correlated feature contest at the neutral rate; transitive freezes)

Written before reading other reviews. The author's run.py and analyze.py unchanged, fresh seed 7, 20000 steps, four rules
(runs/, calibrated_s7.json), plus a labkit run of world.py (rerun/lk; its particle render draws every complex as a large disk and
is not informative, the numbers are what matter here).

Seed 7, neutral-calibrated a* = 417; late windows (t >= 2000):

| rule | significant kinds per window | births per window | per 1000 births | top-kind share (late mean) | mean size at end |
|---|---|---|---|---|---|
| neutral | 29-188 | ~108k | 0.3-1.7 (by construction ~1) | 0.021 | 11.2 |
| zero-sum hash | 2-7 | ~144k | 0.01-0.05 | 0.013 | 13.7 |
| feature | 138-257 | ~76k | 1.8-3.4 | 0.034 | 7.8 |
| transitive | 0-7 | ~2.9k | (frozen) | 0.75 (max 0.89) | 1.08 |

- Zero-sum: complete turnover with 20-100x fewer significant kinds than neutral, as reported (0.01-0.05 per 1000).
- Transitive: one kind holds 75% of complexes on average, size collapses to 1.08, as reported.
- Feature contest: on this seed it sits at or a little above the neutral rate (1.8-3.4 per 1000 vs the claim's 0.6-2;
  neutral windows give 0.3-1.7). Not an above-neutral open-endedness signal of any size, consistent with the finding's reading.

Verdict: Supported. Limits: one fresh seed; I did not check the phenotype-mean measurement (feature sd 0.07).
