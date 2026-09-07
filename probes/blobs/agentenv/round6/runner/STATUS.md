# R6 runner Phase 1 — complete

The approved isolated runner task is complete. Parent handoff sent after reading
the completed result. No native gate was rerun during final documentation.

## Deliverables

- `environments/physim/physim/blobround6.py`: validated absolute-time oracle scheduler, structural submitted `Predictor` protocol, and private exact native-state/checkpoint support.
- `environments/physim/tools/test_blob_round6.py`: 25 toy/API/checkpoint tests and six bounded native tests.
- `probes/blobs/agentenv/round6/runner/DESIGN.md`: exact grammar, event/noise rules, required seed separation, limits, native-state policy, and R5 compatibility matrix.
- `probes/blobs/agentenv/round6/runner/validation.json`: authoritative combined results.
- `probes/blobs/agentenv/round6/runner/toy_validation.json`: preliminary toy-only results; superseded by the combined result.

## Result

**31/31 passed; zero failures, errors, or skips.**

```text
.venv/bin/python environments/physim/tools/test_blob_round6.py --gates toy native --json-out probes/blobs/agentenv/round6/runner/validation.json
```

- Suite: 0.5228532501 s; whole process including imports: 1.4957175422 s.
- Peak RSS: 328,597,504 bytes (about 329 MB / 313.4 MiB).
- Native case: existing E1 `p4g2_044`, seed928. Maximum six dt substeps per trajectory (0.12tu).
- Native initialization: 0.0140672503 s; original f32 fields preserved.
- Project `.venv/bin/python`; NumPy 2.5.2; OpenMP/OpenBLAS/MKL each pinned to one thread.

## Important boundaries

- Submitted API: `predict(actions, queries, n_samples=64, seed=0)` -> `{"samples": [...]}`. Only a structural protocol is declared here, not an implemented submitted model or sandbox.
- Privileged API: `OracleRunner.sample_truth(actions, queries, n_samples=64, *, truth_seed)`; `truth_seed` is REQUIRED and grader-owned. There is no public `seed` alias.
- Policy A: base stream before first effective field/apparatus change; switch once per member; no-op commands and queries do not reseed. No actions means base replay.
- Accepted times use dt=0.02 with 1e-9tu representation tolerance. Adjust occupies 5tu and changes pose at its start. Injection sources use half-open intervals at fixed emitter home.
- Simultaneous starts, same-kind overlaps, and invalid shapes/keys/ranges are rejected. Cross-kind overlap with distinct start times is supported.
- Prototype amp [0,3], dur (0,50], and truth/core dilation clipping are NOT current exploration parity (R5 tools cap amp at 1 and reject bound-striking dilation).
- Exact private base checkpoints only. No f16 frames or arbitrary external checkpoints are accepted as exact native state.

## Open gates / not done

Full old-truth parity is **UNRUN**. Only semantically matched native base, R5
member-state/source primitive, and pose-helper parity were tested. R5 L1/L2 and
long no-action truth semantics are not blanket matches; see DESIGN matrix.

Final horizon/member/output/action/query/CPU budgets are not frozen or enforced
as resource limits. This library is **not safe for untrusted requests**. No
scorer, untrusted-code runtime, production transport/exploration integration,
late-time physics validation, long replay, ensemble battery, new worlds/seeds,
truth regeneration, model/eval/remote work, or commits were added.

R5/production/shared code and uncommitted `absolute_scoring/` were left untouched.
