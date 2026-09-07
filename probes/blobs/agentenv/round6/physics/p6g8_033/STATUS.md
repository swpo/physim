# p6g8_033 physics reconnaissance — first pass complete

Private evaluator-side coverage for cached seed 942. Not an agent syllabus or
fixed L1–L4 contract design. PHYSICS.md and evidence.json are the main handoff.

## Bounded findings

1. OBSERVED: reorganizing u0/u1 spots and curved ridges with distinct channel
   shadows. HYPOTHESIS: delayed local state matters for recovery and interaction.
2. OBSERVED: four negative u2 cores in the selected late full fields, about 1.6%
   area, with slow drift and broad X4 halos. Both home arrays miss those cores.
   X9 is a useful gated quiet control; f16 zero is not exact physical zero.
3. OBSERVED: native matched u0 pulse branches alter later signed local patterns
   despite small net global-mean change. Control/base parity holds for all 51
   stored branch frames. This is one shared noise path, not an ensemble law.

## Artifacts

- PHYSICS.md: equations, visual observations, 3 candidate phenomena, sensor
  observability, proposed discriminating tests, private query coverage, and gaps.
- evidence.json: claim labels, hashes, provenance, metadata, exclusions, and checks.
- initial_*.png: original full-field montages, actually viewed.
- late_polarity_and_quiet_control.png: corrected explicit late scales. Prefer this
  to the initial degenerate-zero X9 row, whose colorbar artifact is documented.
- matched_branch_fields.png: existing amp3 minus matched control fields, viewed.
- initial_stats.json, offline_checks.json, offline_sensor_observations.npz:
  compact cached-data evidence.
- recon.py, offline_checks.py: read-only analysis scripts, no simulator stepping.

## Execution and limits

Initial plot work took 2.05s. Follow-up checks and plots took 4.83s. Both completed.
The base stored NPY was memory-mapped read-only. No archive was unpacked and no
full trajectory was copied to float32. Thread pools were pinned to one.
No new simulation, seed/world, truth ensemble, model, evaluation, monitor, remote
job, launch-script read, shared-source edit, or commit was performed.
No background analysis remains running. First-pass theory is intentionally
incomplete; all new controlled experiments are proposed, NOT YET TESTED.

## Fixed-t0 R6 clarification

The predictor gets a complete action schedule from t0 and query times, not
histories, anchor inputs, or sensor geometry. The grader can privately select
phases and score slots within returned full device arrays. The inspected R6
prototype reuses A0 layout through B.world_key and B.ROSTER. Its current policy A
keeps no-op sham on the base RNG and reseeds treated continuations. Thus proposed
same-noise experiments need the unresolved root noise-comparison gate; existing
native cached pairing does not certify R6 runner pairing. This clarification was
text/schema and source inspection only, with no new data work or execution.
