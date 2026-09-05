# BLOB2v2r2 — private resource-policy revision

**New cohorts:** `BLOB2v2r2-E1` and `BLOB2v2r2-E2`.
**Legacy cohorts stay frozen:** `BLOB2v2-E1` and `BLOB2v2-E2` retain their
old ceilings, 8-open refusal, generic saturation, and fork-ID spelling.
Never pool the old capped results with the new cohorts.

This patch changes resource policy and its failure handling. It does not
change worlds, seeds, apparatus physics, instance draws, syllabus domains,
reveal rules, truth paths/arrays, or scoring formulas. E1 still uses world
`p4g2_044`, seeds 928–930. E2 still uses `p6g8_033`, seeds 942–944. The
syllabus body is identical; its heading names the new cohort. No truth
build, inference call, rollout, GPU operation, SSH action, or commit ran.

## Why a separate cohort

The [recovery audit](../recovery_20260905/fable_recovery_status.md) found
13 spawn refusals at 400 spawns in E2#942, an 8-open refusal in E2#943,
and long generic-saturation loops in four failed Fable rollouts. Those
limits were experimentally binding, not merely runaway protection.

Both `Blob5TaskConfig` and `BlobToolsetConfig` declare the resource-policy
field. The latter also declares `r5_mode`. They survive JSON and the actual
native `ServerBase.run()` / `VF_CONFIG` entry point before registration,
without a task channel or initialized world state. The task checks that its
cohort and config agree; the tool checks that config and state agree.
Unknown policies fail closed. Do not attach undeclared config attributes
with `model_copy(update=...)` (the acc310e serialization lesson).

## Exact private guards

| Meter | Legacy v2 | New v2r2 |
|---|---:|---:|
| Cumulative fork spawns | 400 | 100,000 |
| Logically open fork handles | 8 | 10,000 |
| Aggregate forward simulation, tu | 100,000 | 10,000,000 |
| Sensor meter, node-tu | 1,000,000 | 1,000,000,000 |
| Actuator meter, commanded cu | 30,000 | 10,000,000 |
| Emission meter, original amp-tu price function | 3,000 | 1,000,000 |
| Persisted operation-log plus emission entries | no separate guard | 1,000,000 |

The last row is a **seventh aggregate safety guard**, not a price on an
experiment. Every persisted operation-log record counts as one entry.
Every persisted emission record also counts as one entry. Thus a fork
read/wait/accepted adjustment adds one, while an injection adds two.
The checks run before metadata growth or physics. Only actual appends
accrue the counter. A zero-window read or rejected first actuator step
adds no history. Fixed fork records have their separate spawn guard.

Zero-amplitude and substep-rounded-zero injections remain accepted and
recorded verbatim. They still count two history entries. No no-op elision,
closed-leaf garbage collection, or change to emission dynamics is used.
Reset does not reduce this cumulative counter or erase ancestor logs.

E2#942 recorded 400 forks, 15,795 sim-tu, 536,360 sensor node-tu,
611.75 adjustment units, and 1,015.6 emission units. The five corresponding
new cumulative ceilings provide about **250x, 633x, 1,864x, 16,347x, and
985x** that observed demand. The old trace did not record log-entry count.
At most two entries can be appended by each world-tool call; its 4,552
recorded environment turns therefore bound that demand by 9,104 entries.
The new million-entry guard has at least about **110x headroom over that
conservative bound**, not a claimed measurement of the old log count.

These are empirical headroom targets, **not a guarantee that limits can
never bind**. They are private meters. No budget, remaining allowance,
price, reward for unused resources, or efficiency instruction is shown to
the agent. There is no per-fork duration ceiling and no automatic ready.
Apparatus amplitude, duration, dilation, and control bounds stay unchanged.

## Logical handles versus resident state

The new cohort has an **8-entry process-wide LRU live-state cache**.
The normal tool-server process belongs to one rollout. A cache miss
reconstructs the original state from the salted fork stream and operation
log. An eviction does not close a logical handle or change its poses,
emissions, historical parent reference, or logical time.

Historical ancestry replay is iterative, not recursive. A branch from an
evicted parent and a surviving child of a reset parent both retain their
original state. Reconstruction uses the parent's recorded spawn step,
not its later operations. Children retain the existing semantics: fresh
independent noise streams, captured device poses, and their own emissions.
Replay work does not accrue logical forward-time or log-entry meters.

The r2 cohort uses opaque **128-bit fork IDs**. The old 32-bit IDs would
have about a 69% birthday-collision probability by 100,000 spawns. The
regression has a real short-hash collision at counters 5,931 and 67,233.
New IDs cannot overwrite an occupied record; legacy IDs are unchanged.
The RNG seed still uses the same nonce and counter, never the ID width.

The real E1 regression measured eight resident field arrays totaling
**25,165,824 bytes** (8 × 3,145,728). This is a live-state-cache measurement,
**not a bound on total RSS**. Shared templates, the base-record cache,
FFT temporaries, and a constant number of reconstruction temporaries also
use memory. The million-entry and spawn guards bound retained history
counts, but large histories still make state transport and replay costly.
Closed leaves remain stored; there is no claim of tested throughput at
10,000 open handles or 100,000 spawns. See [review notes](REVIEW.md).

One buffered tool reply also has a transport envelope. `probe_read` uses
lazy indexing before its existing 60,000-number check. New-cohort
`probe_adjust(read=True)` applies the same check before simulation.
`read=False` retains the full aggregate-allowed actuator/simulation span.
This is a per-response memory guard, not an experiment-duration limit.

## Terminal safety failures, not science scores

On a new-policy guard trip:

1. The tool records the raw cap hit and a private resource-stop latch:
   policy, meter, current use, requested amount, limit, and turn.
2. It returns a normal terminal JSON response without revealing values.
   It must not raise here: native MCP only pushes changed state after a
   normal tool return. All later world/ready/submit/status calls return the
   terminal response without further world work, growth, or cap hits.
3. `Blob5Task.resource_safety_stop` is a native `@vf.stop`. Before the next
   model request it returns true. Native interception returns HTTP 400 and
   does not call a provider. State PUT itself does not interrupt a running
   harness program; an already-running script can still receive terminal
   tool responses until its next model request or program exit.
4. Finalize collects artifacts and stores telemetry, then raises the
   distinct `ResourceSafetyError` **outside** the artifact-error handler.
   Native close records `ok=false` and skips both task and harness scoring.
   This also covers a terminal tool call followed by program exit without
   another model request. Offline score and direct skill calls are guarded.

Private `trace.info.physim` includes `difficulty`, `resource_policy`
(id/caps/cache/stop policy), `resource_truncated=true`, `resource_stop`,
`score_status="not_scored_resource_limit"`, raw meters/cap hits, cache
telemetry, time-to-ready, and collected workspace. Telemetry is refreshed
before model turns because provider errors need not run finalize and native
trace serialization excludes `trace.state`. The log counter is also a
`meter_log_entries` metric. No forced reveal or scientific reward occurs.

**Native limits:** `Trace.is_truncated` is read-only and recognizes only
built-in token/turn stop names, not this custom resource stop. It therefore
remains false; the explicit private resource-truncation field is required.
A trace with no reward has a structural `Trace.reward == 0` convenience
value. That is **not a scored zero**. Aggregate only scored, valid traces
within one resource-policy cohort; retain resource failures separately.

There is no intrinsic non-retryable error flag in this verifiers version.
The new `PhysimEnvConfig` therefore enforces **both whole-agent and
whole-episode `max_retries=0`**, even if a caller requests more. It also
serializes exact `ResourceSafetyError` exclusions. Exclusions alone are not
enough: the native episode predicate can retry an older ProviderError in
the history of a later resource failure. Per-call SDK transient retries
are separate and unchanged. Legacy configs keep their requested policy.

In-process `PhysimEnv.complete` keeps a strictly identified r2 resource
failure on resume without changing its `ok=false` verdict or absent reward.
Other failures and old cohorts retain normal resume behavior. **Do not use
`--server --resume`**: that installed path omits `env.complete`.

## Validation and launch handoff

- [Exact commands and durations](validation_commands.json)
- [Final resource gate report](all_gates.json), [log](all_gates.log)
- [Native lifecycle evidence](native_lifecycle.log)
- [Native parse-only CLI validation](native_cli_validation.json)
- [Runner commands and acceptance checks](RUNNER_COMMANDS.md)

The synthetic gates exceed 400 resets and 8 logical-open forks, cover a
1,101-deep chain, all seven true safety trips, no-op metadata accounting,
large-response preflight, private surfaces, and post-ready closure. The
real small E1 case compares warm and cold responses, field hashes, RNG,
poses, emissions, and logs. The native gate uses the real injection tool
through state GET/PUT, real HTTP stop dispatch, native finalize/error and
retry loops, and retained artifacts, without a provider or truth build.
The unchanged legacy suites cover v1, round 2, and v2 (`--fast` omits only
the extra 300-tu replay; all 51 existing truth-array hashes are checked).

No real-runner smoke or paid cohort is authorized by this document. The
root must review the runner path and approve a single short smoke before
any fresh full Fable cohort. Do not resume the old capped scores into r2.
