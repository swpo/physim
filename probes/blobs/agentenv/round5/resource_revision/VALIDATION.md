# Validation summary — final seven-guard tree

All commands ran from `/Users/spoho/Documents/prime/test/physim` with the
project interpreter. No inference, rollout, truth build, GPU/SSH operation,
or commit ran. The native CLI check parsed configs only.

| Gate | Command | Exit | Process seconds |
|---|---|---:|---:|
| All new resource gates, actual E1 physics, native tool/state/stop/retry | `.venv/bin/python -B environments/physim/tools/test_blob_round5_resources.py --json-out probes/blobs/agentenv/round5/resource_revision/all_gates.json` | 0 | 71.664 |
| Standalone native lifecycle with real zero-charge injection | `.venv/bin/python -B environments/physim/tools/test_blob_round5_resources_native.py` | 0 | 1.542 |
| Frozen v1 server suite | `PYTHONPATH=environments/physim .venv/bin/python -B environments/physim/tools/test_blob_server.py` | 0 | 79.920 |
| Frozen round-2 suite | `PYTHONPATH=environments/physim .venv/bin/python -B environments/physim/tools/test_blob_round2.py` | 0 | 4.228 |
| Frozen v2 suite, final tree | `.venv/bin/python -B environments/physim/tools/test_blob_round5.py --fast` | 0 | 74.910 |

The v1 and round-2 tools were not edited. Their suites ran before the final
r2-only log guard; the final v2 suite and all-resource suite ran after it.
`--fast` skips the extra 300-tu A0 re-simulation. It does not skip the
legacy cap/reveal/surface gates or the check of 51 existing truth-array
hashes. No independent second truth build was supplied or launched.

## Final resource evidence

- 512 spawn/reset cycles, then 64 simultaneously open logical forks.
  576 cumulative spawns; all seven cap-hit counters stay zero.
- Resident peak is eight. The high-demand fixture records 554,240 sensor
  node-tu and 17,000 toy-integrated sim-tu. A separate cheap duration
  preflight extends the same fork beyond 100,000 tu, to 117,005 aggregate
  sim-tu, without a per-fork deadline or forced reveal.
- A 1,101-deep chain reconstructs iteratively after its root is reset.
  1,100 logical forks remain open with resident peak eight and zero hits.
- Warm/cold execution matches byte-for-byte responses, field hashes, RNG,
  poses, emissions, logs, and meters. The real small E1 case includes
  injection, pose changes, an evicted parent, historical branch steps,
  and reset parents with surviving descendants.
- Real resident field-cache peak: 25,165,824 bytes (eight states), excluding
  base cache/shared templates/FFT and reconstruction temporaries.
- A concrete old short-hash collision (counters 5,931 and 67,233) no longer
  overwrites either new-policy fork record; old 32-bit spelling stays.
- Billion-step dense/sparse read requests do not allocate billion-element
  index lists. Adjustment output buffers use the 60,000-number envelope;
  `read=False` still permits long aggregate-allowed experiments.
- All seven tiny guards latch one resource stop before further growth or
  physics. Amp-zero and positive-amplitude substep-rounded-zero injections
  keep accepted logs/emissions verbatim and count two history entries.
- All world tools close after ready. Meters/policy values remain private.
- Native `BlobToolset.inject5` is called through real state GET/PUT with a
  tiny log cap. First no-op injection is retained; the next trips before
  growth; repeated calls remain terminal with one raw cap hit.
- Native next-model requests, streamed and non-streamed, get HTTP 400 with
  zero provider calls. Native finalize preserves an artifact then records
  `ResourceSafetyError`, `ok=false`, explicit resource-truncation info,
  and no science reward. The final-tool/no-next-model case also passes.
- Both native whole-run retry layers are forced to zero even when input
  requests three. Actual agent/episode loops make one attempt, including
  prior ProviderError history. Old tags retain their retry configuration.
- Strict in-process resume keeps terminal r2 resource evidence without
  calling it successful. Server-mode resume is not supported by this fix.

[Machine-readable commands](validation_commands.json) and [final JSON](all_gates.json)
contain the exact results. Earlier stage reports are retained and marked
superseded where needed. [Runner commands](RUNNER_COMMANDS.md) were parsed,
not executed. Root must approve the single short real-runner smoke.
