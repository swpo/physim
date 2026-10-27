# Judge rubric v2: how the committee scores worlds

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

v2 (24 October 2026) tightens the evidence rules after sprint 1. Each change, with
the counterexample that prompted it, is listed in
[committee/RUBRIC_CHANGES.md](committee/RUBRIC_CHANGES.md).

## Part 1: the ladder

Report the highest rung with **Supported** evidence and qualify it by the rung of
the individuals involved, e.g. `L6[L2]` = reproduction of unstructured individuals
(Gray-Scott spots), `L4b[L3]` = self-propelled membrane-bounded individuals.

| Rung | Name | Evidence that suffices | Typical screens (FACTS.md) | Common false positives |
|---|---|---|---|---|
| L0 | Inert or broken | dies out, goes uniform, blows up, or is a numerical artifact | status, components_final = 0, occupancy -> 1 | |
| L1 | Pattern | persistent nontrivial structure without discrete individuals: stripes, labyrinths, waves, chaos, networks | occupancy high, few long tracks | |
| L2 | Individuals | discrete localized entities, separable from the background, each persisting far longer than it took to form, at bounded size. In colliding populations where tracked identities churn through merges and splits, the requirement is that a body's lifetime between collisions is much longer than its formation time, judged from images | persistent_tracks, area ratio near 1-3, occupancy < ~0.5 | one connected sea; frozen noise islands; a single blob that slowly grows forever |
| L3 | Organized individuals | an inside/outside organization that belongs to the individual and persists with it. It is a boundary layer in a **material** channel that differs from both the interior and the exterior (`radial.png`: rim/core and rim/outside >= 1.5 in the claimed channel), and/or differentiated internal parts arranged consistently. See the L3 rules below | radial boundary scores, holes/enclosures, H1 persistence, tracks.png | a threshold contour around a smooth bump; a channel that is an algebraic function of the body field; renderer colour; one frame only |
| L4 | Autonomy | at least one of: **(a) repair**, where organization recovers after damage to a mature individual; **(b) self-propulsion**, coherent motion >= 3 body lengths with the body plan preserved and no imposed field; **(c) metabolism**, the individual consumes a resource it depends on and keeps a bounded size. See the L4 rules below | damage.png, motion lines, channel totals | drift from a global gradient; growth mistaken for maintenance; regrowth from debris |
| L5 | Interaction | individuals interact in structured, repeatable ways (scattering, binding into composites, consumption or predation, competition for a resource, signalling) that change population dynamics, shown by a matched ablation | per-species counts, merges/splits with survivors | everything merging into one blob; an unmatched control |
| L6 | Reproduction | an individual gives rise to >= 2 individuals of the same kind (the same body plan), repeatedly, without external template injection. See the L6 rules below | persistent_splits, max_generation, merge/split ratio, lineage.png | fragmentation into debris; splits that re-merge; counting the planted founders' first split |
| L7 | Heredity and selection | >= 2 distinguishable kinds that breed true, variation that arises during the run, and differential persistence or growth between kinds carried by births and deaths. See the L7 rules below | per-kind births, deaths, conversions, off-kind daughters | contagion (living individuals converted); kinds assigned at seeding; a mismatched neutral arm |
| L8 | Open-endedness | new kinds keep appearing and replacing old ones over long runs; novelty does not saturate | long-run diversity curves | cycling through a fixed repertoire |

For every rung the candidate claims, and for the rung below it, the judge writes a
gate verdict: **Supported**, **Weak**, **Contradicted** or **Not tested**. Each
verdict names one concrete observation (file, time or track id) and one limitation.
Rungs are usually cumulative but need not be; record weak lower rungs explicitly.

### Gate rules (v2)

**L3, boundaries.**
- The boundary contrast must appear in a dynamically independent channel, one with its own
  production and transport, and an ablation of its source must remove it. A channel that is
  an algebraic function of the order parameter or of the body field (`4phi(1-phi)`,
  `|grad phi|`, a band-pass readout `4s(1-s)` of the body) is a contour by construction:
  cap it at **Weak** unless an ablation shows that the layer does work, such as containing a
  species or changing the individual's behaviour.
- A quasi-equilibrium layer that a self-made, independently transported species forms at the
  interface counts toward the rung. Whether it does work is scored under the mechanism and
  beyond-diffusion modifiers.
- A conditional layer, one set by a local environment rule and lost by the whole population
  when the environment changes, is **Weak** unless it persists through most of each
  individual's life.
- In kernel worlds, boundary features of 1-2 px, far below the kernel radius, must survive a
  >= 1.5x resolution continuation.

**L4a, repair.**
- Damage a **mature, non-dividing** individual and keep an undamaged twin (same seed,
  branched), on >= 2 seeds.
- Erased matter must leave the individual's reach (deleted, or relocated as background). It
  must not be converted into the individual's own resource at the wound.
- Report the actual erased fraction (`--damage F:FRAC:MODE` measures it).
- Repair that is automatic by construction (for example curvature flow) counts for the rung
  and is scored under mechanism.

**L4c, metabolism.**
- Removing a global feed is passed by any open reaction-diffusion spot, so it is not
  sufficient. Require one of:
  - an abrupt resource removal at a fork with the fed twin alongside, showing individuals
    die (not just a population decline), on >= 2 seeds;
  - a local ablation that cuts one individual's supply while its neighbours keep theirs;
  - a per-individual flux budget.
- Run the ablation on the world claimed. When the model makes the dependence true by
  construction (matter buildable only from the resource, a decay term), it counts for the
  rung and is scored under mechanism.
- Consumption, not presence. When the resource acts on the body in any way besides being
  consumed (a written drift toward it, a field or gradient it shapes, a surface it provides),
  removing the resource does not show that the body depends on consuming it. The control must
  then switch off the consumption, or what the body gains from it, with the resource left in
  place (for example, eating kept but no product made, or uptake set to zero around one body),
  and show the individuals die while the fed twin persists. Precedent: predators held on their
  prey by a written drift survived with digestion off (20261027T1515-c00-audit-digestion-ecology).
- Optional supply threshold. A reviewer may also ask for constant-supply holds that bracket the
  death threshold, each reached both by an abrupt step and by a slow ramp, on >= 2 seeds. A
  body that dies after a cut but survives a slow ramp to the same supply is reacting to the
  shock, not living on the supply, and fails the rung. Report the death supply from the holds,
  not from a ramp (20261027T1755-c00-cips-supply-threshold). This control does not settle
  by-construction questions: open-feed spots also die below a supply threshold.

**L5, interaction.**
- The control must be matched: same grid, duration and seeds, with >= 2 seeds.
- Report the sign of the effect on each partner. An effect whose sign flips under a matched
  control is not established.
- Oscillation claims ("cycles") need peak spacing across >= 3 seeds and a grid-size check
  before they are called limit cycles rather than demographic noise.

**L6, reproduction.**
- Count generations after the founders: from planted founders, Supported needs
  max_generation >= 3, because the founders' own first split does not count. From founders
  formed from noise, >= 2 suffices.
- Report the merge/split ratio. When merges exceed 50% of splits the genealogy is
  reticulate, and confidence is capped at medium.
- Lineage must be merge-aware. A daughter counts only if it stays separate and does not
  re-merge with its sibling. For propagules, the daughter must also reach a set fraction of
  parent size.
- Show strips of randomly chosen births at the deepest generation claimed.
- "Same kind" means the same body plan, not the same instantaneous shape.

**L7, heredity and selection.**
- Kinds may change only at mutation or birth. Report conversions of intact individuals per
  mutation event. A sweep carried by converting living individuals is contagion: it is L5
  evidence (infection), not L7.
- Variation must arise during the run. Kinds assigned at seeding test heredity, not
  selection.
- The neutral arm must share the ancestor's baseline fitness, ideally as an identical-event
  twin (the same mutation events replayed with no fitness effect).
- Report per-kind births, deaths, mutation flips and off-kind daughters.
- Selection that happens only during colonization, with 0 deaths, caps confidence at low.

## Part 2: modifiers (0-3 each)

| Modifier | 0 | 3 |
|---|---|---|
| Spontaneity | organization is hand-planted in the initial condition and merely survives | arises from random or noisy initial conditions |
| Robustness | one seed, one parameter point | >= 3 seeds and +-10% jitter of the key parameters give the same behaviour |
| Numerical validity | untested, or artifacts visible (grid-aligned shapes, checkerboards, NaNs) | the behaviour is unchanged under dt/2 **and** a resolution change; conservation holds where claimed. For reintegration-tracking transport (Flow-Lenia), dt/2 at fixed spread is not a convergence test: change resolution with kernels and flow scaled |
| Novelty | a known result (Orbium gliders, Gray-Scott spots, the Particle Lenia ring, Chan's planted creatures) | not known in the literature we have (see LITERATURE.md) and not a re-skin of another thread |
| Mechanistic insight | "it just happens" | an ablation identifies the responsible operator and the explanation predicts something |
| Beyond-diffusion leverage | a Laplacian-only model would plainly do the same | a **matched Laplacian-only control** (the non-diffusive operator replaced by linear diffusion with comparable rates) fails where the world succeeds. Without that control, score at most 1 |
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
   `radial.png`, `lineage.png`, `timeseries.png` and `damage.png` if present. Only then
   read `FACTS.md` and `metrics.json`. Write down what you see before you read the numbers.
3. Calibrate against the control packs in `examples/packs/`:
   Orbium ~ `L4b[L2]` (motile individuals, no organization beyond a body);
   Gray-Scott mitosis ~ `L6[L2]`; Particle Lenia ~ a single `L3` cell (ring boundary,
   core, spokes) with no motility or reproduction; smoothed noise ~ `L0/L1`.
4. Re-run at least one claimed pack (or a new seed) when it costs under a few minutes.
   Use `PYTHONDONTWRITEBYTECODE=1` and write only to scratch directories. Independent
   reproduction beats any amount of reading. Matched controls beat unmatched ones.
5. Write the verdicts, modifiers, promise, and **one** most valuable next experiment.

## Anti-Goodhart rules

- No rung is awarded from metrics alone; every rung needs a visual observation.
- Claims based on chosen frames or a single seed are capped at **Weak** for L3 and above.
- If the initial condition plants the structure, say so; persistence of a planted
  template is weaker than formation, and reproduction of a planted template counts only
  for generations after the first.
- A boundary claim needs contrast in a material channel that differs from both inside
  and outside. A contour drawn by the threshold, or by a function of the body field, is
  not a membrane.
- Reproduction claims need a merge-aware lineage across the required generations and
  offspring of the same kind as the parent. Debris does not count.
- Occupancy above ~0.6 usually means a sea, not individuals.
- The researcher's prose is not evidence. Images, packs and reruns are.
- The metric definitions are in `labkit/metrics.py`. If a metric is misleading for a
  world, say so and judge from the images; report the failure so labkit improves.

## Versioning

v1, 24 October 2026; v2, 24 October 2026 after sprint 1. The director may revise the
rubric between rounds when a concrete counterexample shows a rung is mis-specified. The
revision is recorded in `committee/RUBRIC_CHANGES.md` together with the example that
prompted it. Earlier verdicts stand under the version they used.
