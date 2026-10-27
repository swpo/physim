# Review of 20261026T1700-c43-cips-consumer#c1 (c54), fresh seeds 54 and 55

Re-runs: rerun/seed54, rerun/seed55 (world defaults, --frames 120 --lineage-k 5), consumer-free twin twin_nocons/seed54
(pred_on 0), prey-removal fork efork_t3000/seed54 (tcut 3000). consumer_only.py segments the consumer channel q alone (q > 0.5,
min 6 px) and runs labkit's tracker on it; strips.py draws random persistent consumer-only splits (strips_s54.png).

| | seed 54 | seed 55 |
|---|---|---|
| composite (prey+consumer matter) persistent splits / max generation | 93 / 10 | 88 / 9 |
| consumer-only bodies (mean t >= 2000) | 30.8 | 27.8 |
| consumer-only persistent splits / max generation | 27 / 2 | 25 / 3 |
| consumer bodies touching a prey droplet (c_a > 0.5 within 2 px) | 300 / 314 (96%) | 269 / 290 (93%) |
| consumer-free twin: prey persistent splits / generation / prey bodies at end | 7 / 1 / 73 | - |
| prey with consumers: persistent splits / generation / bodies at end | 68 / 9 / 31 | - |
| prey removed at t=3000: consumer bodies t 3000 -> 3100 (fed twin) | 34 -> 0 (37) | - |

**S** yes: unstructured start (sheet t=0), consumers and prey appear by t=500.
**X** yes: against the matched consumer-free twin the prey go from a frozen emulsion (7 persistent splits, 73 bodies) to a dividing
population with fewer bodies (68 splits, 31 bodies); the consumer's sign is set by the fork below. One matched seed of mine.
**E** yes for the fork test: removing the prey dissolves every consumer body within 100 t (max q 1.02 -> 0.15 -> 0.08, the bath
level) while the fed twin keeps 37-41. Caveat: the fork removes the surface the consumer sits on as well as its food.
**I** not supported for the consumer as an individual: 93-96% of consumer bodies lie on a prey droplet as a band on its edge, the
few free consumer dots fade within a few hundred t (strips rows 1-2, t 2400-2600), and the claim's own limits name this. The
prey+consumer composite is the individual I see; the consumer is a self-assembled part of it.
**D** not supported for the consumer as such: the numbers pass labkit's gate (25-27 persistent consumer-only splits, generation
2-3, no re-merges), but every split I drew is a consumer band carried apart by its prey droplet pinching (strips_s54.png rows 1, 2,
4); it is division of the composite, which the consumer drives (the twin's prey hardly divide).

Verdict **Weak**: S, X and E reproduce on fresh seeds; I and D hold for the prey-consumer composite rather than for a consumer
individual, so C:ecology-with-reproduction's "populations that reproduce and eat" is met only if the composite is taken as one
kind that eats its own substrate, which is not the claim's statement.
