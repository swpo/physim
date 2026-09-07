# R6 first pass: executable prediction and world-specific physics

**Ready for review. Offline prototype only; not a shipped evaluation.**

For a new session, start with [SESSION_MIGRATION.md](../../../../SESSION_MIGRATION.md).
The separate [absolute-scoring exploration](../round5/resource_revision/absolute_scoring/README.md)
is preserved for provenance, not adopted as the R6 scoring policy.

The agent-facing idea is a code bundle implementing
`predict(actions, queries, n_samples=64, seed=0)`, from one opaque fixed start.
It gets no world history, anchor state or geometry as a prediction argument.
The evaluator uses its privileged view to decide which consequences are worth
checking, without giving the investigator a fixed physics syllabus.

## Review entry points

- [Interface and staged design](../../l0/deepsearch/TRACKA_R6_PREDICTOR.md)
- [Oracle runner design and limits](runner/DESIGN.md)
- [Independent root runner review](RUNNER_REVIEW.md)
- [p4g2_044 / seed928 physics](physics/p4g2_044/PHYSICS.md)
- [p6g8_033 / seed942 physics](physics/p6g8_033/PHYSICS.md)
- [Static evidence validation](first_pass_validation.json)

The dossiers distinguish observed behavior, candidate mechanisms and experiments
not yet run. They are developer/oracle material, not agent-visible inputs. Public
publication for human review requires an explicit exclusion/contamination policy
before these development worlds can support any benchmark claim.

## What is implemented

`environments/physim/physim/blobround6.py` implements a privileged generic oracle
scheduler. The submitted `Predictor` is a structural interface only, not an agent
model supplied by us. Grader truth uses a separate required `truth_seed`.

- Strict absolute-time action/query validation and deterministic event ordering.
- Native source, pose, stepping and sensor math; coherent trajectories across
  query times/devices; passive queries; explicit no-op handling.
- Exact private base checkpoints with fields and RNG state, not f16 frame restarts.
- **31/31 tests passed** independently in worker and root runs: 25 toy/API/state
  tests and six native checks on existing p4g2_044/928.
- Native trajectories in these checks span at most **0.12tu**. They do not verify
  long-horizon accuracy, full old-truth parity, throughput or untrusted-code safety.

A scorer, safe submitted-code runtime, final resource caps and production
exploration integration are not implemented. The R5 state-concurrency defect is
not fixed by adding this isolated module.

## What the physics pass found

### p4g2_044: source-off outcomes, shared feedback and hidden halos

A short u0 pulse can leave different persistent spot outcomes among surrounding
u1 stripes. At the one cached anchor/noise path, positive-segment counts at lag250
are control/amp1/amp2/amp3/amp4 = **5/6/5/7/8**. The source lasts10tu.
Amplitude2 leaves no extra segment but still rearranges the stripe field.
This is evidence against describing this particular series by a monotone final
spot-count response, not a general dose law or tracked organism lineage.

The other candidates are asymmetric negative defects in u2/u3 despite shared
feedback, and a thresholded x7 halo that home probes can nearly miss.

[Matched source fields](physics/p4g2_044/paired_source_fields.png)

### p6g8_033: rearrangement hidden by averages and missed negative cores

In the existing amplitude3, 10tu pulse/control comparison at lag250, the global
u1 mean changes by only about **-0.00014**, while the witness array's RMS u1
change is about **0.79**. These are different reductions of the same paired
field change: large signed local changes can largely cancel in a global mean.
This is one common-noise path, not ensemble uncertainty or proof of chaos.

Four negative u2 cores occupy about1.6% of the domain and drift slowly, while
both home probes see nearly constant background. The gated X9 channel is instead
quiet across all saved late fields at stored precision. Quietness can be a real,
useful control; it should not automatically be discarded as an uninteresting port.

[Matched field differences](physics/p6g8_033/matched_branch_fields.png) ·
[Negative cores, halos and quiet control](physics/p6g8_033/late_polarity_and_quiet_control.png)

Both physics passes used existing full-field caches. No new scientific simulation,
world, seed cohort or truth ensemble was generated. Current-source hashes are not
an immutable build manifest of the original caches. Small effects near f16
rounding and single-path observations have explicit limits in each dossier.

## Design decisions before a test battery

1. **Resolve causal noise pairing.** Current policy A keeps no-op controls on the
   base random stream and reseeds treated continuations. It implements the draft
   convention correctly, but does not reproduce the common-noise paired causal
   experiments above. Choose consistent trial forcing or an explicitly separate
   private pairing method before interpreting treatment-minus-control differences.
2. **Choose observable, reachable phenomena.** Start with compact tests of one
   or two dossier hypotheses, including useful null outcomes and sensor search.
   The proposed experiments are not yet executed. Broad sensitivity search is not
   a substitute for establishing these world-specific phenomena.
3. **Align experiment and evaluation domains.** Existing exploration caps and
   dilation behavior differ from the prototype's proposed evaluation grammar.
   Do not silently present an above-apparatus test as directly learnable in range.
4. **Finish runtime and scoring safeguards.** Exclude privileged material, enforce
   resource/isolation limits, fix transport state integrity, and score joint
   scientific consequences as well as marginal predictions. No universal 0-1
   or exact noise-floor score is claimed by this first pass.

No paid model rollout or new pod has been started. Further scientific simulations
and any evaluation pilot require a scoped next-step review and authorization.

## Reproduce the short checks

From the repository root:

```text
.venv/bin/python environments/physim/tools/test_blob_round6.py --gates toy native --json-out probes/blobs/agentenv/round6/parent_validation.json
.venv/bin/python probes/blobs/agentenv/round6/validate_first_pass.py
```

The second command checks finite JSON, local links, small-source/artifact hashes,
validation consistency and scope statements. It does not rerun the physics
measurements or rehash the large caches. See the dossiers for cache-only plotting
scripts, whose already completed outputs need not be regenerated.

All three workers sent explicit final handoffs. Root checked the key images and
accepted the bounded first pass. The temporary coordination watchdog was removed;
worker sessions were retired. The stop-after-current evaluation policy remains.
