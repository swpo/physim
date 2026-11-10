# VERDICT: NO-GO for the scripted smoke test on the lead's Mac. NO-GO for the one-model rollout.

Host-safety audit of `round6/vfport`, 10 Nov 2026. Audited: `round6/vfport` and `round5/agentenv` at
branch head 216eddf37, identical in both folders to 997005f56 (archives compared by me). All three lenses
returned.

## 1. Verdict

Five major findings are confirmed; one is enough for NO-GO. A1 and A2 are reached by following the runbook the
way a Claude session would. A3 to A5 need one step off the runbook, and nothing in the code stops it. No
runbook command was found that starts the incident's cleanup on the Mac. The rollout depends on the
smoke test and has its own findings (B13 to B15).

| evidence label | meaning |
|---|---|
| read | the cited lines were read |
| tripwire | run on the cloud host with every destructive call replaced by a recorder that raises |
| container | run in a throwaway container with no host mount |
| inferred | reasoned, not run: every statement about macOS |

## 2. The incident, and whether it can happen again

A unit test started the item driver as root on the cloud host. The driver took "I am root" to mean "I am in a
grading box"; its cleanup killed every process of uid 1000 and deleted that account's files.

**Cloud host: not by the same route, but the fix is incomplete.** The driver now refuses unless four conditions
hold (`physim2_env/public/_item.py:100-131`). Two lenses called every kill and delete function on the host with
each condition missing in turn: all refused (tripwire). Three gaps remain:

- In any Docker container three of the four conditions come for free: `/.dockerenv` always exists, and the
  package's own commands write the marker and set the variable. With a host folder mounted, the cleanup runs (A4).
- The cleanup removes a directory the uid owns with everything below it, whoever owns it (A5). This is how
  /home/ubuntu went as a whole.
- The incident tool still starts the driver, and its test predictors, as root on a Linux host (B4).

**Mac: for the driver's cleanup, no path found (inferred).** macOS has no `/.dockerenv`, `/proc` or `/run`; the
operator is not root; verifiers starts every box without a host mount (verifiers
`runtimes/docker/__init__.py:196-244`, read) and refuses a host runtime. The danger lies next to the driver: a
first command that can delete another project's Python environment (A1), cleanup by improvisation after an
interrupted run (A2), two scripts that run `kill -9 -1` as the lead (A3), and a hand-started container with a
Mac folder mounted (A4, A5).

## 3. Findings

Paths are relative to `round6/vfport`; "verifiers" is the pinned `verifiers/v1`. R = required change (section 4),
S = same pass.

| id | severity | what could happen, and when | where | status | fix |
|---|---|---|---|---|---|
| A1 | major | The first command, `uv sync --locked --python 3.12`, run from any folder but the study folder, deletes and recreates the `.venv` of the nearest project above it, then ends in a lockfile error that reads as harmless. The `cd` is a separate block with a placeholder, and a Claude session's working directory does not reliably carry from one command to the next. | `RUNBOOK_MAC.md:47-51, 66` | confirmed. Run by me in scratch (uv 0.11.32, from a subfolder of a test project): "Removed virtual environment", my marker file gone, exit 2. uv on macOS inferred. | R1 |
| A2 | major | Steps 2 and 3 run for 10 to 60 minutes; a Claude session's foreground command is cut after 2 to 10. When vf-eval dies by SIGKILL (`vfrun`'s own timeout does that too), its containers (`vf-<hex>`, `sleep infinity`) and possibly a laboratory process stay. The runbook says only "can be started again" and, in step 4, lists containers by the substring `vf-` with "expected: nothing". That listing also shows other verifiers runs on the Mac (PhySim v1). The likely next move, removing what is listed or `pkill python`, destroys the lead's other containers or processes. | `RUNBOOK_MAC.md:103, 216`; `tools/vfrun.py:72-73`; verifiers `runtimes/base.py:102-107`, `runtimes/docker/__init__.py:102, 194` | confirmed (read; the filter was run in throwaway containers by lens 3). What the session does next is inferred. | R2 |
| A3 | major | `agents/hostile_submission.py` and `redteam/agent_rt.py` are meant for the agent's box, and neither checks where it runs. Mode `killall` runs `kill -9 -1` as the caller; other modes delete `/usr/bin/tar` and `./submission`; `recon` mounts a tmpfs over `/mnt`. On the Mac as the lead: every process of the lead is killed. `agents/` must be on the Mac (step 2b uses it inside boxes) and is not on the do-not-run list. | `agents/hostile_submission.py:44-45, 105-110, 164-167, 176`; `redteam/agent_rt.py:39-41, 217, 456-462`; `RUNBOOK_MAC.md:20-22` | confirmed (read). Narrowed for the Mac: the kill is reached only with an importable `physim2` and a live laboratory address (first script) or a writable `/workspace` (second). Both barriers are accidental. | R3 |
| A4 | major | Off the runbook, someone starts a container with a Mac folder mounted (`docker run -v "$PWD":/workspace physim2-ring:1 ...`, the natural way to look at a failing step) and replays the route's commands there, or drives them through a test double whose type says "docker" (the incident's class of mistake). All four guard conditions then hold. Result: SIGKILL to the uid's processes, the wipe on every mount, and root changes to the mounted folder that are keyed to no uid (`tar -xf`, `rm -rf /workspace/submission`, `chown -R`, `chmod -R go-w`). The only worker-side barrier is the string `runtime.config.type`. | `physim2_env/public/_item.py:74-85, 211-254, 469-511`; `physim2_env/taskset.py:198-203`; `physim2_env/grading.py:47-52, 123-131`; `physim2_env/access.py:163-166` | confirmed (container, lens 2: guard ok, 3 processes killed, 5 files removed on two stand-in mounts; a recording fake typed "docker" received every root command). Lines read by me. | R4, R5, R6 |
| A5 | major | Same state as A4. The wipe calls `shutil.rmtree` on every directory the uid owns, so files of any owner below it go too, a mounted host folder included. The uid test does not protect a share. If the mount table cannot be read, the walk falls back to `/`. | `physim2_env/public/_item.py:236-246, 257-271, 219-221` | confirmed (container, lens 2: two root-owned files in a mount below a uid-owned directory were deleted). Lines read by me. | R4 |
| B1 | minor | uid 1000, the one wiped in the incident, is still the driver's default, the agent box's marker and accepted by the guard. The random grading range 20000-59999 holds real accounts on some machines (30001-30032 on the cloud host). Matters only where A4 holds. | `physim2_env/public/_item.py:71, 537`; `physim2_env/taskset.py:202`; `physim2_env/grading.py:57-60` | confirmed (tripwire) | S1 |
| B2 | minor | `kill(-1)` is issued once the three set-id calls return, without checking that the identity changed, and the guard does not require a root caller. Where those calls are stubbed or filtered, the kill hits the caller's own processes. | `physim2_env/public/_item.py:172-184, 194, 399-413` | confirmed (tripwire) | S1 |
| B3 | minor | Outside a box the driver still runs the given `predict.py` as the caller, under resource limits only. A session that "checks a model's submission locally" on the Mac would run model-written code as the lead. | `physim2_env/public/_item.py:377-389, 417-426` | narrowed: only a hand-built `_item.py` command gets there; `validate.py` cannot start from the source tree (`validate.py:28`). | R6, S1 |
| B4 | minor | As root on a Linux host, `check_units.py` starts the driver as a program seven times (it cannot reach the cleanup: line 377 removes the route variable, but its test predictors run as root); with `--package-root` it calls another checkout's kill and wipe functions under a 12-name tripwire list. Cloud host only: it exits on macOS. | `tools/check_units.py:40-43, 276-337, 361-377` | confirmed (read) | S2 |
| B5 | minor | Red-team tools delete `<--scratch>/agents` and run folders without looking inside, and force-remove containers by fixed names. | `redteam/rt_run.py:89, 202-203, 219`; `redteam/nproc_cross_box.sh:9, 52, 55` | confirmed (read) | S2 |
| B6 | minor | The runbook's safety section is not true as written. In every rollout verifiers ends the laboratory's process group on the Mac (SIGTERM, then SIGKILL), deletes `~/.cache/verifiers/runtimes/subprocess/vf-*` and leaves `/tmp/vf-port-*`. Step 1 truncates `docker/extra-ca.crt`. vf-eval's own error message offers `--clean`, which deletes a run folder. A correct run then looks like a deviation. | `RUNBOOK_MAC.md:13-15, 27-41, 67`; verifiers `runtimes/subprocess.py:99, 197-223`, `cli/eval/main.py:72-86` | confirmed (read) | R6 |
| B7 | minor | Step 4: the `rm -rf` is not chained to its check, it deletes the pilot's results together with scratch, and the optional `docker rmi` removes a helper image that other verifiers work shares. | `RUNBOOK_MAC.md:213-217` | confirmed (read) | R6 |
| B8 | minor | `export PHYSIM2_STORE` does not survive between a Claude session's commands; the tempting repair is an edit of the lead's shell profile. The Docker-shim fallback cannot work on macOS: it runs `/usr/bin/docker`, which is absent, or itself for ever. | `RUNBOOK_MAC.md:81, 139-140`; `tools/docker_shim/docker:8-9, 18` | confirmed (read; shim run with stand-ins by lens 3) | R6 |
| B9 | minor | One check must fail on macOS (`b_lab_process_dropped_it_after_loading`: no `/proc`); others were measured on x86 Linux only; with Docker stopped the tools record failed runs as finished. The runbook has no general stop rule, so the session will try to make the expectation hold. | `RUNBOOK_MAC.md:112-120`; `tools/check_probe.py:353`; `physim2_env/store.py:76-82`; `tools/prove.py:134-140` | confirmed (read); macOS inferred | R6 |
| B10 | minor | The runbook's command lines never ran in this form. The cloud run used an environment that already existed and other arguments; `uv sync` and `uv run` would run first on the lead's laptop. | `RUNBOOK_MAC.md:6-9, 66, 96-100`; `README.md:66-83` | confirmed (read) | R8 |
| B11 | minor | The commit is not pinned. The branch head moved twice during the audit, and the Mac would take whatever the head is that day. | `RUNBOOK_MAC.md:3-4` | narrowed: the two audited folders did not change between 997005f56 and 216eddf37. | R7 |
| B12 | minor | The do-not-run list omits `agents/`, a direct `_item.py`, and round 5's older Mac runbook, whose compose file bind-mounts host folders into a container that deletes and chowns there as root. | `RUNBOOK_MAC.md:20-22`; `round5/agentenv/mac/compose.yaml:13-17, 28-30`; `round5/agentenv/run_rollout.py:68-81` | confirmed (read) | R6 |
| B13 | minor, step 3 | The paid run is gated by prose only and sits in one block with the free dry run. The dollar bound holds only if the provider reports usage. The runbook invites `claude_code` or `codex`, harnesses nobody read. | `RUNBOOK_MAC.md:149-176` | confirmed (read) | R9 |
| B14 | minor, step 3 | `--no-rich` prints the examined model's whole transcript into the operator session, which has a shell on the Mac. Check 3 tells it to read that text; check 6 has it read theta and the secret. | `RUNBOOK_MAC.md:157, 186-200`; verifiers `cli/eval/main.py:135-140` | confirmed (read) | R9 |
| B15 | minor, step 3 | Boxes have no disk limit. A model that writes for an hour as root in its box can fill Docker Desktop's disk image, a file on the Mac. | verifiers `runtimes/container.py:38-41`; `RUNBOOK_MAC.md:60` | confirmed (read); macOS inferred | R9 |

Refuted, or not to be relied on:

- A runbook command starting the driver or a uid-wide kill on the Mac host: no scenario found (read).
- A model's shell on the Mac after switching step 3 to `subprocess`: refused three times before any model call
  (verifiers `utils/compile.py:107-112`, `envs/isolated_verifier/env.py:82-87`; `physim2_env/taskset.py:145-146`).
- Not to rely on: "Mac uids are below the guard's floor" (directory accounts are not); "no `/proc`, no wipe"
  (`wipe_user` falls back to `/`).

## 4. Required changes before GO

No test may kill or delete on a host: use recorders that raise, or the `tools/check_driver.py` container.

1. **Working directory (A1).** Every runbook command starts with
   `cd "<absolute study folder>" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py &&`. Run the sync
   with `--dry-run` first; stop unless it names that folder's `.venv`. No subagents.
   *Test:* from a wrong folder, the guarded line with `echo` in place of uv prints nothing.
2. **Interruption (A2).** `VF_RUN_ID=physim2-pilot-20261110` before every run command; it becomes the container
   label `verifiers.run`. Long commands run detached with a log. An "if interrupted" section: list by that
   label; remove by exact name; stop the laboratory by pid (`pgrep -fl physim2_env.lab_tools`); delete the two
   pilot folders; restart from `make_instances`. Step 4 lists by label. `vfrun.run_eval` sends SIGTERM before
   SIGKILL.
   *Test:* a stub for vf-eval records SIGTERM under `timeout=1`; in the cloud container a foreign `vf-other` is
   absent from the label listing.
3. **Box scripts (A3).** First lines of `agents/hostile_submission.py`, `agents/probe_grading.py`,
   `redteam/agent_rt.py`: exit unless `/.dockerenv` exists and `/etc/physim2/predictor_uid` is a root-owned
   regular file. Repeat before each `kill -9 -1`.
   *Test:* `runpy.run_path` under recorders, every mode: SystemExit, empty recorder; the `harness-killall`
   rollout still passes.
4. **Driver (A4, A5).** (a) `wipe_user`: no `rmtree`; unlink and `rmdir` only the paths `owned_by` listed,
   deepest first, never a mount point. (b) `mount_points` raises when the table is unreadable. (c) Fifth guard
   condition: refuse on any mount outside an allow-list (overlay `/`; below `/proc`, `/sys`, `/dev`; the three
   `/etc` file mounts).
   *Test:* the pure function on stored mount tables; in the `check_driver.py` container a root-owned canary
   below a uid-owned directory survives, `--tmpfs /extra` makes everything refuse, the 19 existing checks pass.
5. **Worker gate (A4).** `grading.require_container` requires a real verifiers container runtime, not borrowed.
   *Test:* recording fakes typed "docker" and "subprocess" receive zero commands from `stage`, `run_request`,
   `_public_files`, `BoxAccess.check`.
6. **Runbook text (B3, B6 to B9, B12).** A true inventory of what is killed, deleted and written on the Mac.
   The store path on each command. "Stop and report" replaces the shim. A `docker info` gate per step.
   Step 4 chained with `&&`, results copied out first, the shared image kept. The known macOS exception; any
   other deviation is a stop. The "never" table of section 5.
   *Test:* review against section 3.
7. **Pin (B11).** The runbook names one commit and the sha256 of package and tool files; the Mac checks it out
   detached and compares.
8. **Rehearse (B10).** The rewritten steps 0 to 2, once in the cloud container from a fresh clone, with one
   deliberate interruption.
9. **Step 3 only (B13 to B15).** The paid command alone under a STOP line with the price; output to a file; a
   script printing fixed fields and hit counts, never message text; no `claude_code`/`codex` sentence; Docker
   Desktop's disk limit below the free space. NO-GO until the smoke test has passed on the Mac.

Changes 3 to 5 need a re-audit of their diff. Same pass, not gating:

| id | change |
|---|---|
| S1 | `_item.py`: uid floor 20000 with an upper bound, `--uid` required, the agent box's marker from the reserved range; verify the identity after the set-id calls and before `kill(-1)`; the guard requires a root caller; no predictor outside a box without an explicit flag |
| S2 | `check_units.py` never starts the driver as root and skips its unguarded-code block; red-team tools stop deleting unchecked paths and fixed container names |

## 5. Residual risks after those changes

- The guard still rests on Docker conventions; in a long-lived container the uid's files can still be wiped.
- A vf-eval killed with SIGKILL still leaves containers, now findable by label.
- The laboratory runs on the Mac as the lead; verifiers signals only process groups it started.
- In step 3 an untrusted model is root in a container for an hour; Docker Desktop's VM is the only wall,
  untested.
- `uv sync` runs an unpinned build backend on the Mac and replaces `./.venv` in the study folder.

By hand before the first command:

| check | command | expected |
|---|---|---|
| hold lifted, right code | `git rev-parse HEAD`; `git status --short`; the hashes of change 7 | the commit the runbook names; clean; equal |
| user | `id -u`; `echo "$HOME"`; `ls "$HOME/physim2-pilot-20261110"` | not 0, no sudo; own home; no such folder. A current backup of the Mac exists. |
| machine | `uname -m` | `arm64` (no Intel Mac) |
| folder | `pwd` | ends in `round6/vfport`; the Claude session is rooted there |
| tools | `command -v uv docker`; `docker context show`; `docker info` | Docker Desktop's own client and context; answers. If uv is missing: stop and ask. |
| variables | `env \| grep -E '^(PHYSIM2_\|UV_PROJECT_ENVIRONMENT\|PYTHONPATH\|DOCKER_HOST\|DOCKER_CONTEXT\|VF_RUN_ID\|PRIME_RUNS_MODE)'` | nothing |
| other runs | `docker ps -a --filter label=verifiers.run`; `docker images physim2-ring` | nothing. Save `docker ps -a` and `docker images` as the baseline. |
| room | free disk; Docker Desktop's disk limit and CPUs | 5 GB free; limit below the free space; 4 CPUs |
| network | VPN, TLS-intercepting proxy | none |

Never, on the Mac:

| never | why |
|---|---|
| `sudo`; edits of `~/.zshrc`, `~/.zprofile`, `~/.zshenv` | nothing in the pilot needs them (B8) |
| `docker run` with `-v`, `--mount` or the Docker socket, for anything in this repository | A4, A5 |
| pasting the route's commands (the `sh -c` lines of `grading.py` and `taskset.py`) into a shell | A4 |
| `_item.py`, `physim2 validate` or a model's `predict.py` on the Mac itself | B3 |
| `agents/*.py`; anything in `redteam/` or `round5/agentenv` (its `mac/` runbook and compose file included); `tools/check_units.py`, `tools/check_driver.py` | A3, B12 |
| `pkill`, `killall`, `docker rm` by filter or `$(...)`, any `prune`, `vf-eval --clean` | A2, B6 |
| another `[env.agent.runtime] type`, another harness, a second try after a failure | stop and report instead (B9, B13) |

## 6. What this audit did not cover

- Nothing ran on macOS or Docker Desktop. Inferred only: that containers there show `/.dockerenv` (if not,
  grading stops); how a shared folder reports owners; how a Claude session ends a command at its limit; uv on
  macOS.
- No vf-eval rollout was run; interruption behaviour is read from code.
- Not audited: network isolation, credentials, the Prime runtime, the `claude_code` and `codex` harnesses, the
  incident's pre-fix code.
- Checked by me: `_item.py` and `RUNBOOK_MAC.md` in full, every line cited for A1 to A5, the uv run of A1, the
  commit comparison, the imported `vw` library. The lenses' tripwire and container runs were not repeated; two
  lenses made them independently and agree.
