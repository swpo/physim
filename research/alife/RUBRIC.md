# Judge rubric v1: how the committee scores worlds

The rubric serves two purposes. It tells researchers what counts as progress, and
it tells the judges how to turn images and measurements into verdicts that can be
compared across very different kinds of dynamics. It deliberately mixes three ingredients:

1. a **ladder of organization** with explicit evidence requirements per rung,
2. **modifiers** for things the ladder cannot see (spontaneity, robustness, numerics,
   novelty, mechanism, use of non-diffusive operators, value as a PhySim world),
3. a holistic **promise** score: the judge's estimate of the value of further work.
   It is not a sum of the other scores.

Do not average these into one number. A world that reproduces but has no
internal structure and a world with beautiful membranes that never divide are
different achievements, and the director funds them for different reasons.

## Part 1: the ladder

Report the highest rung with **Supported** evidence and qualify it by the rung of
the individuals involved, e.g. `L6[L2]` = reproduction of unstructured individuals
(Gray-Scott spots), `L4b[L3]` = self-propelled membrane-bounded individuals.

| Rung | Name | Evidence that suffices | Typical screens (FACTS.md) | Common false positives |
|---|---|---|---|---|
| L0 | Inert or broken | dies out, goes uniform, blows up, or is a numerical artifact | status, components_final = 0, occupancy -> 1 | |
| L1 | Pattern | persistent nontrivial structure without discrete individuals: stripes, labyrinths, waves, chaos, networks | occupancy high, few long tracks | |
| L2 | Individuals | discrete localized entities, separable from the background, each persisting far longer than it took to form (tracked through most of the run), at bounded size | persistent_tracks, area ratio near 1-3, occupancy < ~0.5 | one connected sea; frozen noise islands; a single blob that slowly grows forever |
| L3 | Organized individuals | an inside/outside organization that belongs to the individual and persists with it: a boundary layer that differs from interior *and* exterior (membrane-like), and/or differentiated internal parts arranged consistently | holes/enclosures, H1 persistence, rim_vs_core and rim_vs_outside contrasts, channel profiles, tracks.png | a threshold contour around a smooth bump; renderer colour; noise heterogeneity; one frame only |
| L4 | Autonomy | at least one of: **(a) repair**, where organization recovers after damage (>= 30% erased, `--damage`) and an undamaged control is shown; **(b) self-propulsion**, coherent motion >= 3 body lengths with the shape preserved, not driven by an imposed field; **(c) metabolism**, the individual consumes a resource or flux it depends on (an ablation kills it) and keeps a bounded size | damage packs, motion lines, channel totals | drift from a global gradient; growth mistaken for maintenance |
| L5 | Interaction | individuals interact in structured, repeatable ways (scattering, binding into composites, consumption or predation, competition for a resource, signalling) that change population dynamics | merges/splits with survivors, counts over time, sheet.png | everything merging into one blob; one collision |
| L6 | Reproduction | an individual gives rise to >= 2 individuals of the same kind, repeatedly (>= 2 generations), without external template injection | persistent_splits, max_generation, lineage.png | fragmentation into debris; splits that immediately re-merge; seeded copies |
| L7 | Heredity and selection | >= 2 distinguishable kinds that breed true, variation that arises during the run, and differential persistence or growth between kinds | per-kind counts, lineage by kind | kinds defined by colour assigned at seeding only; drift without selection |
| L8 | Open-endedness | new kinds keep appearing and replacing old ones over long runs; novelty does not saturate | long-run diversity curves | cycling through a fixed repertoire |

For every rung the candidate claims, and for the rung below it, the judge writes a
gate verdict: **Supported**, **Weak**, **Contradicted** or **Not tested**. Each
verdict names one concrete observation (file, time or track id) and one limitation.
Rungs are usually cumulative but need not be; record weak lower rungs explicitly.

## Part 2: modifiers (0-3 each)

| Modifier | 0 | 3 |
|---|---|---|
| Spontaneity | organization is hand-planted in the initial condition and merely survives | arises from random or noisy initial conditions |
| Robustness | one seed, one parameter point | >= 3 seeds and +-10% jitter of the key parameters give the same behaviour |
| Numerical validity | untested, or artifacts visible (grid-aligned shapes, checkerboards, NaNs) | dt halving and a resolution change leave the behaviour qualitatively unchanged; conservation holds where claimed |
| Novelty | a known result (Orbium gliders, Gray-Scott spots, the Particle Lenia ring) | not known in the literature we have (see LITERATURE.md) and not a re-skin of another thread |
| Mechanistic insight | "it just happens" | an ablation identifies the responsible operator and the explanation predicts something |
| Beyond-diffusion leverage | a Laplacian-only model would plainly do the same | a non-diffusive ingredient (nonlocal kernel, advection, conservation, interfaces, particles) demonstrably does work that reaction-diffusion could not |
| PhySim potential | no clear hidden law or level structure for an agent to discover | rich, measurable, multi-level behaviour that would make a good discovery world |

## Part 3: promise (1-10)

The expected scientific value of funding the next sprint of this line, in the
judge's own judgment. Weigh: rung reached and the distance to the next rung, how
much the modifiers say the result can be trusted, how fast the line is moving, and
how much it would teach the other threads. A stuck thread can have a high-rung
candidate and low promise. A new line can have L1 results and high promise.

## Part 4: judging procedure

1. Read the researcher's claims table. Do not read their discussion yet.
2. For each claimed candidate open `sheet.png` **first**, then `tracks.png`,
   `lineage.png`, `timeseries.png`, and only then `FACTS.md` and `metrics.json`.
   Write down what you see before you read the numbers.
3. Calibrate against the control packs in `examples/packs/`:
   Orbium ~ `L4b[L2]` (motile individuals, no organization beyond a body);
   Gray-Scott mitosis ~ `L6[L2]`; Particle Lenia ~ a single `L3` cell (ring boundary,
   core, spokes) with no motility or reproduction; smoothed noise ~ `L0/L1`.
4. Re-run at least one claimed pack (or a new seed) when it costs under ~2 minutes.
   Independent reproduction beats any amount of reading.
5. Write the verdicts, modifiers, promise, and **one** most valuable next experiment.

## Anti-Goodhart rules

- No rung is awarded from metrics alone; every rung needs a visual observation.
- Claims based on chosen frames or a single seed are capped at **Weak** for L3 and above.
- If the initial condition plants the structure, say so; persistence of a planted
  template is weaker than formation, and reproduction of a planted template counts only
  for generations after the first.
- A boundary claim needs contrast in some channel that differs from both inside and
  outside. A contour drawn by the threshold is not a membrane.
- Reproduction claims need lineage across >= 2 generations and offspring of the same
  kind as the parent. Debris does not count.
- Occupancy above ~0.6 usually means a sea, not individuals.
- The researcher's prose is not evidence. Images, packs and reruns are.
- The metric definitions are in `labkit/metrics.py`. If a metric is misleading for a
  world, say so and judge from the images; report the failure so labkit improves.

## Versioning

v1, 24 October 2026. The director may revise the rubric between rounds when a
concrete counterexample shows a rung is mis-specified. The revision is recorded in
`committee/RUBRIC_CHANGES.md` together with the example that prompted it. Earlier
verdicts stand under the version they used.
