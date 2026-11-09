# GPU jobs on Prime, requested from cloud sessions

Cloud sessions cannot open outbound SSH, so they cannot drive Prime pods
themselves. The **PhySim macbook session** (a Claude Code session on the user's
Mac) runs GPU jobs for them. You ask for a job by pushing a JSON file to your own
`claude/*` branch; the Mac rents a pod, runs it, terminates it, and publishes the
results and cost to the `gpu-jobs` branch of `swpo/physim`. Only the Mac writes
`gpu-jobs`: never push to it.

## 1. Ask for a job

Commit a request file and push it, together with the code it needs, to your
working branch (any `claude/*` branch of `swpo/physim`). Put it in
`research/alife/vecworld/program/gpu/requests/<job_id>.json` (`gpu/requests/` at
the repository root also works). Requests anywhere else, including the `gpu-jobs`
branch, are ignored. The Mac checks for new requests about once a minute.

```json
{
  "schema": "gpu-job/v1",
  "job_id": "vw1-bench-001",
  "purpose": "gliders throughput, GPU-vs-CPU agreement, one conv training step",
  "paths": ["research/alife/vecworld/vw1"],
  "gpu": {"types": ["H100_80GB", "A100_80GB"], "count": 1, "spot": false},
  "max_hours": 1.0,
  "cap_usd": 15,
  "setup": [
    "curl -LsSf https://astral.sh/uv/install.sh | sh",
    "export PATH=$HOME/.local/bin:$PATH",
    "uv venv -q -p 3.12 $GPUJOB_DIR/.venv && . $GPUJOB_DIR/.venv/bin/activate",
    "uv pip install -q 'jax[cuda12]==0.12.0.1' numpy==2.5.4"
  ],
  "run": "python research/alife/vecworld/vw1/port/bench_gpu.py --out $OUT",
  "env": {"XLA_PYTHON_CLIENT_PREALLOCATE": "false"}
}
```

| field | meaning |
|---|---|
| `schema` | always `"gpu-job/v1"` |
| `job_id` | `[a-z0-9][a-z0-9-]{2,47}`, equal to the file name, never reused |
| `purpose` | one printable line (at most 300 characters) for the ledger |
| `ref` | optional full commit SHA to run. Omit it to use the commit that holds the request (usually what you want). A given `ref` must be reachable from a `claude/*` branch on origin, and every entry of `paths` must exist in it; otherwise the request is rejected. |
| `paths` | repository paths to upload (`git archive` of those paths at `ref`; at most 300 MB). They are unpacked under `src/` on the pod, keeping their repository paths. |
| `gpu.types` | Prime GPU type names in order of preference: `H100_80GB`, `H200_141GB`, `A100_80GB`, `A100_40GB`, `L40S_48GB`, `RTX6000Ada_48GB`, `RTX_PRO_6000B_96GB`, `A10_24GB`, `V100_16GB`. The cheapest available offer of the first type that has stock is used. |
| `gpu.count` | 1-8 (default 1) |
| `gpu.spot` | allow spot instances (default false). Use only if the job checkpoints, because spot pods can be preempted. |
| `image` | Prime image (default `ubuntu_22_cuda_12`, which has the NVIDIA driver and CUDA 12; JAX/PyTorch come from `setup`) |
| `disk_gb` | optional disk size |
| `max_hours` | longest the job may run (0.05-24) |
| `cap_usd` | the most this job may cost. It must cover `rate x (max_hours + 0.25)`. The pod is terminated before the cap is reached. |
| `setup` | shell lines run once in `src/` (bash, `-e -o pipefail`). Environment changes such as `PATH` or an activated venv carry over to `run`. |
| `run` | shell lines run in `src/` after setup |
| `env` | non-secret environment variables. Secrets (`*TOKEN*`, `*API_KEY*`, `*SECRET*`, `*PASSWORD*`) are refused: no credentials ever go to pods. |
| `git_outputs_max_mb` | how much of `$OUT` to put back into git (default and maximum 50 MB; at most 20 MB per file and 2000 files) |
| `notes`, `requester` | printable text (`requester` one line) |

On the pod these are set: `$OUT` (write results here), `$GPUJOB_DIR` (the job
directory), `$GPUJOB_ID`. If you write `$OUT/progress.txt`, its tail shows up in
the 15-minute heartbeats. Pods have internet access (pip, Hugging Face, GitHub).
The pod is deleted afterwards. Only regular files under `$OUT` (no symlinks, at
most `collect_max_mb`, 2000 MB, in total) and the job's top-level logs come back;
everything else in `$GPUJOB_DIR`, such as a venv or `src/`, is lost.

## 2. Follow it

Everything is published on the `gpu-jobs` branch:

```
git fetch origin gpu-jobs
git show origin/gpu-jobs:jobs/<job_id>/status.json
git show origin/gpu-jobs:LEDGER.md
```

`status.json` holds `state`, which moves through
`received -> queued (or needs_approval) -> provisioning -> running -> collecting`
and ends in one of `done | failed | timeout | cancelled | rejected | infra_error`.
A job whose GPU types are momentarily out of stock stays `queued` (or
`needs_approval`) and is retried; only budget and validation problems reject.
It also holds `message`, the pod and its rate, cost so far, deadlines, and log
tails (refreshed every 15 minutes while the job runs). When the job finishes the
Mac also sends a cross-session message to the requesting session when it can
identify it.

Results:
- `jobs/<job_id>/out/...` holds your `$OUT` files, within the git limits.
- `jobs/<job_id>/logs/` holds `setup.log`, `run.log`, `job.log`, `sysinfo.txt`
  (nvidia-smi and the OS) and the exit codes, each truncated to its last 1 MB.
- `jobs/<job_id>/manifest.json` lists every collected file with its size and
  SHA-256, including files that stayed on the Mac (`in_git: false`), and any file
  that was skipped (links, files past the size cap, names git cannot store
  safely). Ask the user or the Mac session for files that stayed on the Mac.
- `jobs/<job_id>/review.md` holds the Mac's code review of your job, when there
  is one, and `status.json` then carries `review: {file, summary, at, sha256}`
  (for example `"summary": "1 major, 4 minor; fine to run"`). It can appear in
  any state, often before the job starts, and a newer review replaces the older
  one. Read it when `review.sha256` changes; fixes it asks for usually go into
  your next request.

## 3. Cancel

Push an empty file `<job_id>.cancel` next to the request, on the same branch
(a cancel anywhere else is ignored). It works in every state before the job ends,
including while the pod is still being provisioned. The Mac sees it within about
2 minutes, stops the job, collects what exists, and terminates the pod.

## Budget and approval

- The GPU campaign cap is $1,000 in total, counted from Prime's billed amounts
  (or rate x time until Prime reports them). Running and queued jobs reserve
  their full `cap_usd`.
- Jobs with `cap_usd` up to the auto-approval limit (currently $25) start
  without asking. Larger caps wait in `needs_approval` until the user approves
  them on the Mac.
- At most 2 pods run at the same time. Extra jobs wait in `queued`.

## Tips

- Batch many short runs into one job. Every job pays roughly 3-10 minutes of
  provisioning plus the time setup takes.
- Pin versions in `setup` and print them in `run`.
- Make `run` exit non-zero on failure. The job's state is taken from the exit code.
- Keep `$OUT` small (summaries, JSON, PNG). If you checkpoint, write checkpoints
  under `$OUT` only if you need them back.
- Test the code path on CPU in your own session first, so GPU time is not spent
  on import errors.

## How it works (for auditing)

The runner is `handoff/gpu_jobs_20261107/gpujobs.py` on the Mac; its state and
its bare mailbox repository live in `~/Library/Application Support/gpujobs`. It
never runs request content on the Mac: `setup` and `run` are written into scripts
that only run on the pod, and all local commands use argument lists. Only commits
reachable from origin's `claude/*` branches are uploaded.

Each pod is named `gpujob-<job_id>-a<n>`, recorded before it is created, and
terminated in a `finally` block that sends its deletes first; a create whose
result never came back is found again by that name, and a pod of an earlier
attempt that appears late is terminated while the job runs. Each job has a hard
deadline (first create request plus the time its `cap_usd` buys at the higher of
the offer's rate and the price Prime reports for the pod); setup, collection and
termination are bounded by it, and outputs are unpacked only after the pod is
gone. Before the first pod is created, a detached guard process must be running:
it terminates the job's pods if the runner dies or the hard deadline passes, and
a manual `sweep` applies the same rule. Termination is confirmed pod by pod with
the provider; a pod the provider still lists as live is deleted again. While the
guard runs it keeps the Mac from idle-sleeping (`caffeinate -i`); a closed lid
or a forced sleep still stops it, and a running pod then keeps billing until the
Mac wakes.

The runner builds every commit on `gpu-jobs` from its own records with git
plumbing, without checking the branch out. Anything else committed there (other
files, symlinks, submodules, git control names) is dropped, and a job's files are
rewritten whenever that job is published. Output names that git refuses or could
take for `.git` on some filesystem (for example `.git.`, `GIT~1`, names with `:`)
are skipped and listed in the manifest. If git or GitHub refuses a job's outputs
or logs (for example push protection on a secret-looking string), its
`status.json`, `request.json` and `manifest.json` are still published, without
them, and say why. Wallet balances, the Prime team id, local paths and pod
addresses are kept off the branch.
