# Evaluation candidate review — 2026-09-13

Start with **m4, xv, and bf**. Together they offer translation and binding,
rotation, and history-dependent motion. Follow with **mv3** for transport and
**ds6_000** for a richer evolved system. This is a prioritization of historical
evidence, not a new simulation campaign or an evaluation certification.

The registry has **22 world records, 19 distinct genomes, and one validated
evaluation bundle**. The records comprise 15 other historical research worlds,
the `p4g2_044` development reference, and six workflow-example harvests. Some
harvests share a genome with an earlier record; record counts are not counts of
independent physical systems. No additional evaluation bundle was created here.

## Initial shortlist

| Priority | World | Why it adds useful coverage | First preparation and prediction test | Main uncertainty |
|---|---|---|---|---|
| First | `m4` (3 fields) | Moving blobs and traveling bonds; a simple physical control for more complex systems. Three historical soup seeds show motion without box-limit flags. | Prepare an isolated traveler and a bonded pair; predict sensor arrivals and recovery after a localized pulse, compared with persistence and constant-velocity extrapolation. | A straight traveler may be too easy. Cases must expose interaction or response to intervention. |
| First | `xv` (6 fields) | Heterodimer rotation and spontaneous choice of handedness. At the packaged reference point, the historical prepared-pair study reports three noisy rotors, a grid check, and a 10,000-tu stable run. | Prepare the bound pair, record the settling history and phase, then predict phase-dependent sensor readings and response to a pulse. Vary phase and orientation across preparations. | Spontaneous launch takes a long warm-up. A 50-tu window covers only part of an orbit; test whether phase and intervention effects are distinguishable from simple local extrapolation. |
| First | `bf` (4 fields) | Motion with a slowly relaxing trail field. The packaged gamma=0.05, tau_b=200, D_b=0, tau=5.7 point matches the historical self-launch reference. | Harvest mature moving states with recorded trail history. Compare pulse response and forecasts from full-state, persistence, and memory-ablated controls. | A 200-tu memory may be subtle in a 50-tu episode. Trail-mediated reader deflection was certified at different parameters; that stronger claim does not automatically transfer to this genome. |
| Next | `mv3` (8 fields) | Engine–cargo interaction, pushing and capture, with meaningful component controls. Packaged mimic coupling eta=0.6 matches the historical transport world. | Intentionally prepare a kicked engine behind cargo and compare engine-only, cargo-only, and coupled transport. Test prediction of contact and transport under the existing source/probe actions. | Random soups sometimes park. The historical multi-cargo delivery used an external coupling-cut controller; autonomous delivery/release is not established by this genome or the current action API. |
| Next | `ds6_000` (8 fields) | Evolved two-species dense tissue with persistent microscopic rearrangement. All three historical assays stopped at 2,500 tu with no box-limit flag. | Harvest mature states from multiple seeds and compare paired pulse/control ensembles; measure intervention signal, spatial correlations, and gain over persistence. | Rich dynamics may be noisy rather than learnable, and may add less diversity beyond the dense-field `p4g2_044` reference. |

Sources: [common three-seed validation](../probes/blobs/l0/complexity/VALIDATION_V2.md),
[rotor study](../probes/blobs/rotor/SUMMARY.md),
[trail-field study](../probes/blobs/bfield/SUMMARY.md),
[transport study](../probes/blobs/machinev3/SUMMARY.md), and the
[exact packaged extraction map](../packages/blobkit/blobkit/data/worlds/_extraction.json).
Evaluation task ideas in the table are proposals; those studies did not test them.

The historical assay's stop reason `static` means its extension criteria did not
fire. It does not mean all local fields or objects stopped moving. Search
interest scores are not evaluation-quality scores, and scores from different
metric versions or horizons should not be ranked together.

## Other registered worlds

- `ds3_014`: valuable later target for staged succession and slow memory. The
  three-seed horizons were 10,000 / 20,000 / 5,000 tu; every run raised a
  box-limit flag. Its interesting epoch must be deliberately harvested. Check
  larger domains and whether a short forecast window captures a meaningful
  transition before spending on a full truth suite.
- `ds3_017`: later target for worm-like ecology and reorganizing tissue. Two of
  three runs raised box-limit flags. Use organism-aware measurements; counting
  thresholded segments as independent organisms was a documented earlier error.
- `pred`: encounters offer a promising predation mechanism, but the common soup
  assays show slow charging, weak mature motion and box-limit flags on all three
  seeds. An intentionally prepared encounter may be more useful than its soup.
- `rail_111_17`: reserve for cross-species binding and sorting. The stage-3 census
  records distinct binding/repelling roles and no replication in 18 encounter
  assays. It needs a preparation and contemporary reproduction of those effects.
- `engine_10748`: useful component/control for `mv3`; avoid counting engine-only
  transport as another independent difficulty axis without additional evidence.
- `s2_128_26`: parked, plateau-bonded cargo is useful as a component/control.
  The packaged genome retains another activator that did not nucleate in the
  historical cargo study; apparatus design must account for all fields.
- `m0`: static calibration/control. `coex`: mostly inert coexistence; lower
  priority for a first challenging forecast suite.
- `g0_jit_11`, `s2_118_41`: retain as research seeds. Neither received a detailed
  standalone evaluation-suitability review in this pass.
- `small-mass-search/*`: six demonstrations of generation, metrics, lineage,
  and harvesting. Their short-run mass objective makes no evaluation-quality
  claim; exclude them from the candidate shortlist by default.
- `p4g2_044`: retain as the validated local development reference. Its dense
  background matters; the V3 audit corrected an earlier sparse-rotor description.
  It is openly documented and does not establish unfamiliar-world generalization.

Further sources: [stage-3 census](../probes/blobs/l0/stage3/CENSUS.md),
[V3 interpretation audit](../probes/blobs/l0/complexity/VALIDATION_V3.md),
[champion mechanisms and corrections](../docs/archive/blobs/searching-equation-space.html),
and [reference reproduction checks](../handoff/generation_refactor/STATUS.md).

## Preparation and evaluation gates

1. **Support the physical profile.** The shared Blobkit simulator accepts these
   genomes, but the installed V1 bundle loader explicitly requires four
   activators, eight channels, twelve ports and a fixed numerical profile.
   Broaden that validated contract before attempting to load the smaller worlds.
   In particular, `bf` has a zero-diffusion channel, while V1 currently requires
   positive channel diffusion. Do not pad genomes with dummy fields to fit V1.
2. **Make the preparation reproducible.** Record exact warm-up, kicks, initial
   fields, time origin, noise policy, code and numerical profile. Mature behavior
   is often more useful than a fresh random soup. Use several independently
   prepared starts; separate development preparations from future held-out ones.
3. **Check observability and intervention signal.** Choose probes, emitter
   placement and actions that reveal the intended dynamics. Compare no-action
   and pulse runs with paired seeds during diagnosis, then use independent
   realizations for truth. Start with the current 50-tu contract; change it only
   if the measured timescales justify a separately versioned suite.
4. **Demonstrate predictive value.** Compare native independent-noise forecasts
   with persistence, simple motion extrapolation, and mechanism-specific
   ablations. A visually interesting world is insufficient if all controls tie,
   persistence already solves it, or the response is dominated by noise. Record
   uncertainty across preparations and score groups; set acceptance thresholds
   before the final validation campaign.
5. **Package and reproduce.** Bind world, preparation, apparatus, suite, truth,
   and validation evidence by immutable identities; rerun through the installed
   environment. Only then label that particular preparation/suite validated.

Loader evidence: [bundle validation](../environments/physim/physim/bundles.py)
and [episode contract](../environments/physim/physim/blobround6.py).
No new physics claims, predictor scores, simulations, or GPU rentals were made
in this review.

## How the registry distinguishes them

`curation.json` adds review metadata keyed by the **immutable world-record ID**.
The catalog exporter merges it into each row as `curation`. Updating a priority
or interpretation does not change a genome, source record, recipe or bundle ID.

- **Role:** `research-candidate`, `evaluation-reference`, `demonstration`, or
  `unclassified`. This describes intended use.
- **Evaluation stage:** `genome-only`, `prepared`, or `validated`. Here,
  `genome-only` means no linked current evaluation preparation; historical
  characterization can still be extensive. `prepared` requires exact physical
  world and preparation identities. `validated` additionally requires a suite,
  bundle and evidence. It describes the linked preparation/suite, not every
  possible use of the genome.
- **Review priority:** `first`, `next`, `later`, `control`, `reference`,
  `example`, or `unreviewed`. This is a revisable judgment, not a search metric.
- **Evidence and next check:** each reviewed row cites archived evidence and
  identifies what remains to establish a useful evaluation task.

Provenance completeness stays separate in the source/recipe records: a world
can have incomplete original search history and a fully reproducible present
evaluation bundle. Publication and exposure also stay separate: the current
reference is locally verified, pending publication, and for development use.
Labels do not bypass the environment's bundle validation.

The exporter verifies evidence artifacts and rejects unknown world IDs, unknown
evidence, invalid labels and unsupported readiness claims. New records default
to unclassified/genome-only/unreviewed. The raw `blobkit registry` catalog stays
general-purpose; the Physim exporter adds these project-specific judgments.
