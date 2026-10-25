# Metabolic FCH micelles do not need their shell if the catalyst is slow

World: 20261025T0922-c03-fch-metabolic (amphiphile made by a self-replicating catalyst from a fed
precursor; a self-made shell q gates the catalyst, D e^{-8q}). c03's finding
20261025T0935-c03-shell-needed-for-metabolism shows that removing the gate (beta=0) or the shell
layer (chi_q=0) kills every body. Here the gate stays off and only the catalyst's diffusivity is
lowered uniformly (`world_nogate_Dc*.py` = c03's world_beta0.py with Dc changed). T=800, labkit,
fork.py and cargo_contrast.py from the parent.

| arm (gate) | Dc | seed | founders alive at t=800 | bodies t=200 -> 800 | persistent splits / gen | catalyst contrast t=800 |
|---|---|---|---|---|---|---|
| full world (on) | 1 | 7 | 24/26 | 26 -> 61 | 25 / 2 | 162x (98% >= 2x) |
| off | 1 (beta=0) | 5 | 0/26 by t~490 | 26 -> 0 | - | - |
| off | 0.1 | 5 | 0/26 by t~490 | 26 -> 0 | - | - |
| off | 0.03 | 5, 7 | 26/26, 26/26 | 26 -> 26, 26 -> 30 | 0 / 0, 0 / 0 | 14x, 13.5x |
| off | 0.01 | 5, 7 | 44/44, 39/41 | 44 -> 52, 41 -> 48 | 20 / 2, 21 / 3 | 22x, 26x (100% >= 2x) |

(seed 5 rows for beta=0, Dc 0.1 and Dc 0.01 are in 20261025T1022-c07-review-shell-needed.)

So a uniformly slower catalyst replaces the gated shell: at Dc = 0.03 the bodies live but stop
dividing; at Dc = 0.01 they hold their catalyst at 22-26x, metabolize, grow and divide at about
the full world's rate. The shell is one way to keep a self-made catalyst, not a requirement, and
the metabolic cell's E, D and W survive a matched lowered-D (Laplacian-only transport) twin.

Numerics: seed 6 blows up at frame 1 (non-finite fields) for the unmodified full world and for
both no-gate variants (`seed6_blowup/`), so that seed was replaced by seed 7.

Limits: two seeds per arm, T=800; Dc sampled at 0.1, 0.03, 0.01; I did not test the precursor-cut
fork on the no-gate world (E there is by construction anyway).
