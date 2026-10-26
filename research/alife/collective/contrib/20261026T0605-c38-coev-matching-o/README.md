# coev-matching (c38): does a coevolving predator-prey world keep making new kinds?

Files: `coev.py` (numba individual-based world, every birth and death logged), `world.py` (labkit wrapper; `pack/` is the
eps=0.08 regime, 2 seeds x 10000 steps), `drive.py` (one long run -> data/<tag>_s<seed>.npz, not imported),
`analyze.py` (o_measure on trait-bin kinds, shadows, twin, figure), `scan.py` (predator persistence screen).

Reproduce one regime: `python drive.py e08 0 200000 '{"eps":0.08}'`, then the twin with p0 = that run's mean_success:
`python drive.py e08N 0 200000 '{"neutral":1,"p0":0.0813}'`, then `python analyze.py e08 0 e08N` (about 1+1+1 min).
Tags: e08 = Gaussian matching with capture floor 0.08; S2 / S4 = prey food uptake x exp(-|trait|^2/(2 S^2));
k1e04 = Cauchy matching 1/(1+d^2/w^2) with floor 0.04; <tag>N = in-world neutral twin (constant capture p0 = the real
run's mean realised success; prey cost kept). Results per run: data/<tag>_s<seed>_o.json, results_table.json, figs/.
