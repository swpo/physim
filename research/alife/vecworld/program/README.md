# PhySim v2: supervenient worlds research program (started 7 Nov 2026)

A world is a level-0 evolution network F0 (hidden weights, explicit noise) plus a coarse-graining Φ to level 1 (and
possibly further levels). The agent observes level k > 0 and acts on level 0 through a constrained input port.
Library: `../vw1/vw`; worked example: the Flow-Lenia gliders world (`../vw1/port`, results in `../vw1/fresh`).

| track | question | memo |
|---|---|---|
| 1, more worlds | how to get more worlds: design from motivating examples, search over level-0 families, and learned coarse-grainings whose inductive biases define Φ | `track1/DESIGN.md` (with the closed-form pooling pilot P0) |
| 2, the exam | what the agent predicts, what is hidden, how interaction is limited, how predictions are scored, how it runs as an environment | `track2/EXAM.md` (with the KL check on the ring toy) |
| inventory | which existing worlds can become level 0, with measured costs, invariants and input costs | `inventory/WORLDS.md` |
| review | cross-reading of the three memos against each other and the gliders results | `CRITIQUE.md` |

Track 1 framing (the lead, 7 Nov 2026, speculative and open-ended): choosing an inductive bias (model structure,
objective) and training autoencoders on level-0 dynamics yields emergent coarse variables, such as local conservation
laws, that depend on the bias; which bias is right almost certainly depends on the level-0 theory. World research may
then look like: hand-design level 0, then iterate on the autoencoder's biases to obtain the higher levels instead of
designing those by hand too. The working plan is to map (level-0 theory x inductive bias) to what emerges, judged by
closure, non-triviality, seed stability, agreement with hand designs and closure under the agent's inputs. The first
cell of that map is the learned level-2 prototype on the gliders block view (`track1/learned_phi2`).

`lit/` holds the earlier literature reviews these build on. `cover/` holds the "PhySim v2 / supervenience" cover
(stack concept; liberties listed in `make_cover.py`).

Headline positions so far:
- Hidden set: the level-0 weights, a secret (at least 128 bits) behind all real-world noise, and the exam instances
  until grading. Nothing fitted to the hidden world leaves the evaluator (for example a Φ trained on its data).
  Permutations can be dropped once the semantics are public.
- Interaction: for inputs that enter as a shift before Gaussian noise, the information cost in nats is half the
  noise-whitened squared norm, so the information budget picks the norm. Inputs must enter where the noise is.
- Scoring: oracle-normalised fair energy skill over declared (level, horizon) cells; variogram score secondary.
  The designer's level-1 ceiling is a lower bound, so rewards must not be clipped at it.
- Pooling: a reconstruction autoencoder picks the wrong feature in a mass-conserving world; a long-horizon closure
  objective with a local, translation-equivariant encoder recovers block sums.
