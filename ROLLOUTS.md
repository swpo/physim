# Model rollouts on the user's Mac, requested from cloud sessions

Besides GPU jobs (PROTOCOL.md), the PhySim macbook session runs **model
rollouts**: exam rollouts of a Prime inference model under a pinned, reviewed
version of the vfport exam port. They run on the Mac itself, never on a pod,
one at a time. You ask for one by pushing a JSON file to your own `claude/*`
branch; results and costs appear on the `gpu-jobs` branch under `rollouts/`.
Only the Mac writes `gpu-jobs`: never push to it.

> Status: intake, checks, budget and publication are live. The executor (the
> pinned runbook's step-3 commands) is wired after the round-4 pin review;
> until then an accepted rollout stays `queued` with a message saying so.

## 1. Ask for a rollout

Commit `research/alife/vecworld/program/rollouts/requests/<job_id>.json`
(`rollouts/requests/` at the repository root also works) together with the
config file it names, and push the branch. Requests anywhere else, including
the `gpu-jobs` branch, are ignored. The Mac checks about once a minute.

```json
{
  "schema": "rollout-job/v1",
  "job_id": "r6-pilot-qwen-001",
  "purpose": "round-6 pilot: qwen3.6 on the default exam profile",
  "requester": "fisim agent-world session",
  "pin": "0123456789abcdef0123456789abcdef01234567",
  "pin_sha256": "<64 lowercase hex: sha256 of PIN.sha256 at the pin>",
  "config": "research/alife/vecworld/program/round6/rollouts/configs/pilot-qwen.toml",
  "exam_profile": "default",
  "instance": "pilot-qwen-001",
  "model": "qwen/qwen3.6-35b-a3b",
  "caps": {"max_turns": 200, "max_output_tokens": 8192, "max_context_tokens": 131072,
           "wall_minutes": 90, "box_memory_gb": 2},
  "cap_usd": 20
}
```

Only these fields are accepted; any other field rejects the request. There is
no `env`, `setup`, `run`, `paths` or other executable field: what runs is fixed
by the reviewed pin.

| field | meaning |
|---|---|
| `schema` | always `"rollout-job/v1"` |
| `job_id` | `[a-z0-9][a-z0-9-]{2,47}`, equal to the file name, never reused. GPU jobs and rollouts share one id namespace: an id already used by either is refused (see below). |
| `purpose` | one printable line, at most 300 characters |
| `requester` | optional, one printable line (at most 200) |
| `notes` | optional printable text, at most 4000 characters |
| `pin` | the pinned commit, 40 lowercase hex. It must have been reviewed and approved on the Mac. |
| `pin_sha256` | 64 lowercase hex: the sha256 of `PIN.sha256` at that commit. `(pin, pin_sha256)` must equal the approved entry. |
| `config` | repository path under `research/alife/vecworld/program/round6/rollouts/configs/`, ending in `.toml` or `.json` (no `..`, no wildcards). It is read from the commit that holds the request (your branch tip when the Mac sees it) and must be a regular file of at most 64 KB of UTF-8 text without NUL. Its strict schema check ships with the pin. |
| `exam_profile` | `[a-z0-9][a-z0-9_-]{0,40}` |
| `instance` | `pilot-[a-z0-9-]{3,40}`, never reused: a name any accepted rollout used before is rejected |
| `model` | Prime inference model id, `[a-z0-9][a-z0-9._/-]{2,100}`, e.g. `qwen/qwen3.6-35b-a3b` |
| `caps` | exactly `max_turns` (integer 1-500), `max_output_tokens` (integer 1-262144), `max_context_tokens` (integer 1024-2000000), `wall_minutes` (integer 1-180), `box_memory_gb` (number 0.5-4) |
| `cap_usd` | the most the rollout may cost, above 0 and at most 500 |

A request file is at most 256 KB and immutable once received: a changed file
under the same `job_id` is ignored; use a new id.

Some requests are refused without any record on `gpu-jobs`: a file name that
is not a valid `job_id`, an id that looks like a credential or a local private
value, and an id already used by a GPU job (`jobs/<job_id>/` on `gpu-jobs`) or
by another rollout. If nothing appears under `rollouts/<job_id>/` within a few
minutes, check those cases and push the request again under a new id.

## 2. Acceptance and budget

When the Mac plans a rollout it checks, in this order:

1. the pin: `(pin, pin_sha256)` is approved and not revoked, otherwise **rejected**;
2. the config: size, UTF-8 and NUL now, the pin's own checker once it ships;
3. the instance name has not been used, otherwise **rejected**;
4. the price: the model's listed prices from Prime's model listing
   (`pricing.input_usd_per_mtok`, `pricing.output_usd_per_mtok`, in USD per
   1M tokens; the input price is the higher of the input and cache-write
   prices). A model that is not listed, or lists no positive prices, is
   **rejected**. One maximal call costs
   `one_call_usd = max_context_tokens x p_in + max_output_tokens x p_out`
   (per-token prices); `cap_usd` below that is **rejected**. The rollout's
   bound is `bound_usd = cap_usd + one_call_usd` (the run stops at the cap,
   and one call may already be under way).
5. the budget, separate from the GPU budget: the user's model-rollout total
   (`$500`) covers this Mac's rollouts (each counts its billed amount once
   reconciled, otherwise its `bound_usd` while queued, waiting for approval,
   running or collecting, and after it ends if it ever started) plus the
   coordinator's cloud ledger, `billed_usd_total + reserved_usd_open` of
   `research/alife/vecworld/program/round6/rollouts/ledger.json` on
   `claude/fisim-agent-world-research-hepmlz` (schema `rollout-ledger/v1`).
   If that ledger cannot be read or parsed, nothing is planned: the rollout
   goes back to `received` with a message and is planned again
   automatically, after 5 minutes and then with doubling waits (at most an
   hour).

Outcome: a bound past the remaining total waits in `needs_approval` (the
user's $500 total would be exceeded, and the message says by how much); a
bound above the auto-approval limit ($50) waits in `needs_approval`;
otherwise `queued`. The user's approval covers the bound it was given for and,
past the total, the overrun the message showed: if the bound grows or the
total ends up exceeded by more, the rollout asks again. The plan (listed price
fields and units, `one_call_usd`, `bound_usd`, the committed amounts,
`remaining_usd`, `total_overrun_usd`) is in `status.json` under `plan`. If the
model listing cannot be reached, the rollout goes back to `received` and is
planned again automatically the same way. A queued rollout is planned once
more right before it starts, so it starts only against the budget, prices and
reviewed pins of that moment (it may then wait in `needs_approval` again).

The bill of a finished rollout is compared with the tool's own count. If it is
more than 10% + $0.05 above that count, above the rollout's bound, or above
$0.05 for a rollout that ran without a count, the Mac stops planning further
rollouts until the user has looked at it. Rollouts waiting in `received`
meanwhile are planned once the block is cleared.

## 3. Follow it

```
git fetch origin gpu-jobs
git show origin/gpu-jobs:rollouts/<job_id>/status.json
git show origin/gpu-jobs:rollouts/ledger.json
```

`state` moves through `received -> queued (or needs_approval) -> running ->
collecting` and ends in `done | failed | timeout | cancelled | rejected |
infra_error`. Before a rollout starts it can also go back: `needs_approval`
or `queued` to `received` while the model listing or the coordinator ledger
cannot be read (planned again automatically), and `queued` to
`needs_approval` when it is planned again before its start. `infra_error`
after `running` also means the Mac's executor process ended without
finishing the rollout; its bound stays counted until its bill is reconciled.

- `rollouts/<job_id>/status.json`: state, message, history, the plan, the
  review summary. Once the rollout ran: `counted_usd`, the tool's own cost
  count, and after reconciliation `billed_usd`, `reconciled`,
  `reconcile_history` (and `operator_counted_usd` when the Mac's operator
  supplied a count the tool did not store).
- `rollouts/<job_id>/request.json`: your request as accepted, where it came
  from, and the config file's commit, blob and sha256.
- `rollouts/<job_id>/review.md`: the Mac's review of your request, when there
  is one (`status.json` then carries `review: {file, summary, at, sha256}`).
- `rollouts/<job_id>/manifest.json`: every file the rollout produced, with
  bytes, sha256, `in_git`, and a `reason` when it is not in git.
- `rollouts/<job_id>/out/...`: the outputs, within 50 MB per rollout, 20 MB per
  file and 2000 files.
- `rollouts/ledger.json` (schema `mac-rollout-ledger/v1`): `updated_utc`,
  `billed_usd_total`, `reserved_usd_open` and one row per rollout that was
  ever accepted (queued or waiting for approval), also after it ended: `job_id`,
  `state`, `model`, `instance`, `requester_branch`, `bound_usd`, `billed_usd`
  (once reconciled), `reconciled`, `budget_counted_usd` and `finished_at`.
  `budget_counted_usd` is what the row counts against the budget: its bound
  until reconciled, then its bill, and 0 if it ended before it started. It is
  not the tool's own count (`counted_usd` in `status.json`). Read this file for
  this Mac's share of the budget. `LEDGER.md` has the same as a table under
  "Model rollouts".

Every published file is scanned for credentials first: the Mac's Prime API
key and local private values (as raw bytes, base64 and UTF-16), and common
token shapes such as `sk-`, `pit_`, `hf_`, `ghp_`, `github_pat_`, `AKIA`,
`Bearer <token>` (any case), `x-api-key`/`api_key` assignments, and private-key
blocks (PEM, OpenSSH, PGP). An output with a hit stays on the Mac: the manifest
lists it with `in_git: false` and `reason: "key-scan"` (or
`key-scan-unavailable` when the scan could not run). Compressed and archive
outputs (gzip, zip and `.npz`, bzip2, xz, zstd, 7z, lz4, zlib, tar) cannot be
scanned and also stay on the Mac (`reason: "key-scan-unscannable"`, with their
`format`): write results uncompressed if you want them in git. (Formats that
compress parts of themselves, such as PNG text chunks or PDF streams, are
scanned as raw bytes only.) If
`status.json`, `request.json` or `manifest.json` itself has a hit, a stand-in
`{"job_id", "kind", "state", "withheld": "key-scan", "note"}` is published in
its place. Nothing of a match is ever published. Ask the user or the Mac
session for files that stayed on the Mac. Wallet balances are never published.

## 4. Cancel

Push an empty `<job_id>.cancel` next to the request, on the same branch (a
cancel anywhere else is ignored). A rollout that has not started is cancelled
at once; a running one is stopped by the runner. A run whose executor process
has ended ends in `infra_error`.
