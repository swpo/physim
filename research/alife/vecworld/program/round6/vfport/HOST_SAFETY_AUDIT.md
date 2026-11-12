# VERDICT (round 5, second pass, 12 Nov 2026): GO for steps 0 to 3 of `RUNBOOK_MAC.md` on the lead's Mac, from the one commit that holds this line: the scripted smoke test (steps 0 to 2) and then, once steps 0 to 2 have passed on the Mac at this commit and the lead has read their report, the model rollouts driven by request files (step 3), each request naming this commit (code of the round-5 second-pass pin 19b6beb836874f9f938c51367849e2442bd6af4e, sha256 of `PIN.sha256` 41da66d69750ce7829112f30c4c22417b0e19df38c34448818dbfac4670f78c8; its commands rehearsed from a fresh clone of it with one paid job from a request, `results/rehearsal_round5.json`, `second_pass`). No finding of blocker or major severity is open in the three audits; the open minors (K16: vf-eval can be made to hold about 3 GiB, not the 0.8 GiB section B says; three untold behaviours of the laboratory tools; four runbook wording points) go to the next pin, and the notice corrects the three that the operator needs now. Scores of this pin may be quoted only on the conditions of that section. It replaces the GO for steps 0 to 2 of round 5, first pass, for 5be2466e307ccc4785278af43279b63a06c3ac9f: start from this commit only. See "Re-audit, round 5, second pass" at the end; sections 1 to 6 and the re-audits of rounds 1 to 5 (first pass) are the earlier verdicts, kept as they were.

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

## Re-audit, round 1

**VERDICT, 10 Nov 2026: NO-GO for the scripted smoke test on the lead's Mac. NO-GO for the one-model rollout.**
The hold in `RUNBOOK_MAC.md` stays; the first line of this file stands.

The NO-GO is narrow. A1, A3, A4 and A5 are closed, and the code re-audit's GO on the code stands. What holds the smoke test is the runbook's
stop-and-recover procedure, the answer to A2. Issued the way a Claude session issues commands, its process listing
shows a line that is not the tool, its stop signal can go to that line and then stops nothing, and it was
rehearsed only in a mode that hides this. The repair is runbook text and one short rehearsal. No file of the
package has to change.

Judged: the branch at 73829e5c6, where the code equals `PIN.sha256` (sha256 `7aa9bbfc…f64c19`, 105 of 105 files,
recomputed by me at the head); since then only `PROGRESS.md` changed. Inputs: the fixer's report, the re-audit of
the code (GO on the code, two new minor gaps) and the re-audit of the runbook (NO-GO as written). What I rely on I
checked myself. Labels as in section 1, and two more:

| evidence label | meaning |
|---|---|
| run | run by me in scratch with stand-ins (`echo`, a sleeping script); no file of the port executed |
| vf-eval | rollouts through `vf-eval` with the scripted harness and no upload; made by the fixer and the code re-auditor, none by me |

"container (mine)" means my own run in named throwaway containers without a host path; nothing of the driver or of
the box scripts ran on the host itself.

### Status of the findings and changes

| finding, change | status | evidence |
|---|---|---|
| A1, change 1 | closed | read: all 27 fenced commands and the 2 inline ones begin with the folder guard (counted by script); uv appears twice, with `--project <absolute path>`, dry run first. run: the guard with `echo` from 6 start folders and 6 wrong targets prints nothing (another checkout of this same folder would pass: the path the lead gives is compared by eye). uv on macOS: inferred. |
| A2, change 2 | **open, narrowed** | Closed: containers are listed by the run label and nothing wider (read: verifiers keeps a caller's `VF_RUN_ID`, `cli/eval/runner.py:138`; container, fixer and re-auditor, 8 of 8: a foreign `vf-other` is absent); vf-eval gets SIGTERM before SIGKILL (`tools/vfrun.py:72-111`, read). Open: N1, N2, N3 below. |
| A3, change 3 | closed | read: the gate is the first statement of the three scripts and stands again before each `kill -9 -1` (`agents/hostile_submission.py:62, 190, 202, 206`; `agents/probe_grading.py:46`; `redteam/agent_rt.py:39, 243, 483, 486`). container (mine): 6 starts in a container without the marker, all `refused:`, a canary process alive, nothing written. tripwire (fixer, re-auditor): 34 starts. |
| A4, changes 4c and 5 | closed as specified | container (mine): the script of `tools/check_driver.py`, 31 of 31; with `--tmpfs /extra` every function refuses and the driver runs nothing. read: `physim2_env/grading.py:49-87`, and the gate stands before every command the package sends into a box (`grading.py:160, 193`; `taskset.py:147, 202`; `access.py:47, 150, 163`; `physim2_script/__init__.py:34`). New minor gaps: N5, N6. The Mac: inferred. |
| A5, changes 4a and 4b | closed | read: no `rmtree` in `_item.py`; unlink or rmdir of listed paths only, never a mount point (`367-391`); an unreadable mount table raises (`169-177`). container (mine): a root-owned file below a directory of the uid survives, with its directories; only the uid's own files go. |
| change 6 (B3, B6 to B9, B12) | closed as text | read: the never-table, the inventory, the store path on each command, `docker info` before each detached start, step 4 as one `&&` chain with the image kept. The inventory holds for the Mac: off Linux verifiers' proxy listens on 127.0.0.1 and no helper container gets a folder (`runtimes/docker/__init__.py:318-321`; on Linux one fresh temp folder goes into a helper, `366-388`). Small mismatches of text: item 6 below. |
| change 7 (B11) | values closed, handover open | run: the sha256 of `PIN.sha256` equals the runbook's; 105 of 105 files match at the head. read: N4. |
| change 8 (B10) | **open, narrowed** | read (`results/rehearsal_round1.json`): steps 0, 1, 2 and 4 and two interruptions ran, from files and not as a session issues them; the image build did not run. |
| change 9 (B13 to B15) | done as text, never run | read: a STOP line and a block of its own, output to a file, a report tool that prints fixed fields and counts (`tools/run_report.py`), caps equal to `configs/qwen_ring_bash.toml`, no `claude_code` or `codex` sentence, the disk limit in the by-hand list. The price fields are blank and the gate is prose. |
| S1 (B1, B2) | closed | read: `_item.py:87, 187-212, 273-300, 515-527, 687`. container (mine): uid 1000, 19999 and 60000 refused; a helper whose identity did not change signals nothing. |
| S2 (B4, B5) | closed, one weakness | not checked by me. Fixer: 66 of 66. Code re-auditor: N8. |
| N1, new | **blocks** | run: see below. |
| N2, new | **blocks** | inferred (macOS). |
| N3, new | **blocks** | read. |
| N4, new | **blocks** | read: `git show 454812a2b:…/RUNBOOK_MAC.md`. |
| N5, new | minor, Linux only | container (mine, the guard only): with `--tmpfs /dev/extra` the guard passes and `/dev/extra` is among the mount points the cleanup walks (`_item.py:158-160`). |
| N6, new | minor, Linux only | read: no condition of the guard looks at namespaces (`_item.py:187-212`). The re-auditor's `--pid=host` run was not repeated. |
| N7, N8, new | minor | read (N7: `agents/hostile_submission.py:45-53, 135`); N8 as reported by the code re-auditor. |

The new problems:

- **N1. The process listing and the stop command.** A session issues every command as `<shell> -c <text>` (seen
  here with bash; zsh on the Mac is inferred). The
  detached commands of 2a and 2b leave a waiting shell whose command line is that whole text, so the pattern of
  runbook lines 221 and 418 lists it next to the real tool, on a line that also holds `tools/prove.py`. "The pid
  at the start of ITS line" (334-339) then has two candidates. Run through this session's own command tool with a
  sleeping stand-in: two lines were listed; SIGTERM to the first left the stand-in running, and no `EXIT` line was
  ever written. Every listed process is the pilot's, so nothing outside the pilot can be hit. But the procedure
  does not do what its text says, and the first status of step 2a already differs from the text, which is a stop
  by rule A.4. The rehearsal ran the commands from files and did not see it.
- **N2. The interpreter.** If uv builds `.venv` on a Homebrew or python.org Python 3.12 (uv uses an installed
  system Python before it downloads its own), that interpreter re-executes as `…/Python.app/Contents/MacOS/Python`.
  No process line then begins with the `.venv` path: the listing shows the waiting shell at most, or nothing,
  while the pilot runs, and points 3 and 6 would remove containers and folders of a run that is still going. `ps`
  without `ww` may also cut long lines.
- **N3. Step 1 has no branch.** The real `uv sync` runs in the foreground. On the Mac the cache is cold (several
  hundred megabytes; the rehearsal's 6.7 s had a warm one), and a session's foreground command is cut after 2 to 10
  minutes (A2). After a cut, "If a run was interrupted" lists nothing, point 6 prints nothing, and the text says to
  go on from `make_instances` with half a `.venv`.
- **N4. The handover of the pin.** The Mac checks out the pinned commit. The runbook inside that commit says ON
  HOLD and "Commit: not named in this copy", while step 0 expects "the pinned commit". Which text the session
  follows and which hash it compares is not defined.
- **N5, N6.** They need a container started by hand with `--tmpfs` below `/dev`, a host tmpfs bound there, or
  `--pid=host`, and the route's commands replayed in it; kill and delete stay limited to one uid in 20000-59999. A
  Mac share is not a memory file system and is refused wherever it is mounted (pure function, code re-auditor).
- **N7.** The box scripts' gate does not look at mounts: in a hand-started container that has the marker and a
  host folder, `./submission` is deleted. **N8.** `tools/check_units.py:57-61, 152-155` imports the package and
  runs `tar` and `chmod -R` on a temp folder before its tripwires are installed.

### What remains before GO for the smoke test

Text and one rehearsal. Change no file that `PIN.sha256` lists: the verdict on the code holds for that hash only,
and a changed package file needs a re-audit of its diff.

1. **Process listing** (lines 221 and 418). Replace the `ps … | grep` part by
   `ps axwwo pid=,command= | grep -E "^ *[0-9]+ /ABSOLUTE/PATH/TO/vfport/\.venv/bin/python"` (line 418 keeps its
   `cut`). The path is now a pattern: section C gets a by-hand check that it holds only letters, digits and
   `/ . _ -`.
   *Test:* the command of 2a issued as one `sh -c '<text>'`: the tool is listed, the waiting shell is not (my
   stand-in run: one line).
2. **Stop command** (line 339). `… && ps -ww -p PID_FROM_THE_STATUS_LINE -o command= | grep -E
   "^/ABSOLUTE/PATH/TO/vfport/\.venv/bin/python" && kill -TERM PID_FROM_THE_STATUS_LINE`.
   *Test:* aimed at the waiting shell's pid it prints nothing and signals nothing (my stand-in run: no match).
3. **Interpreter.** In step 1, after the import check, a command that prints the interpreter's own process line
   (`ps -ww -p <its own pid> -o command=`); expected: it begins with `/ABSOLUTE/PATH/TO/vfport/.venv/bin/python`,
   anything else is a stop. To make it hold, `--managed-python` on both uv commands (uv 0.11.32 has the flag), with
   the dry run's expected lines taken from the rehearsal. After the start of 2a: "`processes:` must show `<pid>
   /…/.venv/bin/python -B tools/prove.py`. If not, and `prove.log` has no `EXIT`: send no signal, wait for `EXIT`,
   stop and report."
4. **Step 1.** The real `uv sync` detached, with a log and an `EXIT` line, in the shape of the image build, with a
   status command. "If a run was interrupted" begins: "This section is for step 2 only. A cut or an unexpected
   output in step 0, 1 or 4: run nothing more, report, stop. Use this section once; at a second interruption do
   points 1 to 5, then stop. A Docker error under `containers:`: stop." In point 6 and in step 4, "If it prints
   nothing: stop and report" replaces "delete nothing and go on" and "nothing was deleted".
5. **Pin handover.** The file names no commit to check out. Rule A.1, section C and step 0 say: the commit is the
   40-character hash in the coordinator's GO message, which the lead gives the session; the first line of step 0
   must equal it; the code is identified by the sha256 of `PIN.sha256`. The hold notice is the only text a verdict
   edits. Step 0 says what a failed comparison prints (a `shasum: WARNING` line and no `PIN-OK`; not `FAILED`).
6. **Text that would trip the stop rule.** What each log shows after a stop (runbook re-auditor: `EXIT 130` after
   a `KeyboardInterrupt` traceback inside a rollout, `EXIT 143` between two rollouts, `EXIT 130` without a
   traceback for `vf-eval` alone; take it from the rehearsal); line 308 (two lines of token counts and `}`); line
   178 (`wc` pads its number on macOS).
7. **Rehearsal in session mode.** A fresh clone in the cloud container; every command issued as ONE `sh -c '<text
   of the fenced command>'` or through a session's command tool, never from a file. At least: step 0; the changed
   commands of step 1; 2a with a status while it runs; one stop by points 1 and 2, first aimed at the waiting
   shell's pid on purpose; one hard kill with points 3 to 6; 2a to its end; a status and a stop during 2c. The
   record holds the literal text of each command and the complete output of every status command.

Same pass, not gating (runbook text):

- The never-table: no `docker run` by hand for anything of this repository, whatever its options (`--pid`, `--ipc`,
  `--tmpfs`, `--privileged`, `--volumes-from` included): N5, N6.
- Step 3: `test -f "$HOME/physim2-pilot-20261110/scratch/LEAD-GO-STEP3" &&` after the guard of the paid command;
  the lead creates that file by hand, and writes the price into its three fields.
- Traces. The lead decided that pilot traces may be uploaded where that helps, never for a sealed exam (roadmap,
  decision 5 additions, 52cbe73a4). As written, step 4 deletes every run folder. If the trace of step 3 is wanted,
  step 4 must copy that run folder out, unread, and only when the report counts 0 hidden values; the upload is
  then the lead's own act. The smoke test needs none of this.

A later pass, with a re-audit of its diff, and before the package runs on any Linux machine other than the cloud
container: N5 (below `/proc`, `/sys`, `/dev` accept the stock mount points only; a stored `--tmpfs /dev/extra`
table and a container check), N6 (the guard requires the box's own process namespace; the re-auditor proposes that
`/proc/1/root` be the same directory as `/`, to be confirmed in a verifiers box), N7, N8.

**The one-model rollout** stays NO-GO. It can be offered to the lead only after a GO for the smoke test and after
the smoke test has passed on the Mac and been reported. Change 9 is in place as text.

### Residual risks, also after a GO

- Nothing has run on macOS or Docker Desktop. Inferred only: the signs of a container and the stock mount table
  there (if they differ, staging stops and damages nothing), the non-Linux branch of verifiers' Docker runtime,
  `ps`, `uv`, how a session ends a command at its limit, that a detached command outlives its call (seen here on
  Linux).
- A vf-eval that is killed outright still leaves its containers and its laboratory process; they are found by
  label and by path and removed by exact name and pid, by the session.
- The tools and the laboratory run on the Mac as the lead. `uv sync` runs an unpinned build backend and writes
  `.venv`, uv's cache and, with `--managed-python`, uv's own Python.
- The image build of step 1 has never run in the runbook's form.
- N5 to N8, on Linux hosts.
- Step 3: an untrusted model is root in a container for an hour, and Docker Desktop's virtual machine is the only
  wall; untested.

By hand, on the Mac, in addition to section 5 and to section C of the runbook:

| check | expected |
|---|---|
| the coordinator's message | GO for steps 0 to 2 with a 40-character commit; `git rev-parse HEAD` equals it; the `RUNBOOK_MAC.md` on disk says GO, not ON HOLD |
| `pwd -P` in the study folder | only letters, digits and `/ . _ -` |
| the session | started in the study folder; no subagents; one command per call |
| power and sleep | plugged in, and the Mac does not sleep for the 45 minutes of steps 1 and 2 (a sleep is an interruption) |
| baseline | `docker ps -a` and `docker images` saved before step 0 and compared after step 4: the four images the runbook names and no container more |
| stop rule | any output that differs from the runbook, any `refused:`, any request for a password: the session stops and reports, and the lead does not repair by hand what the runbook does not name |

Not covered by this round: the same as section 6, and the red team's attacks, `tools/prove.py --worlds 4` and the
gliders rollout on the new code (not rerun by anyone).

## Re-audit, round 2

**VERDICT, 10 Nov 2026: GO for the scripted smoke test on the lead's Mac. The one-model rollout stays NO-GO
until that test has passed on the Mac and been reported; it may then be offered to the lead.**

The GO covers steps 0, 1 and 2 of `RUNBOOK_MAC.md`, its section "If a run was interrupted", and step 4 once the
lead says the pilot is over. It holds for ONE commit: the commit that carries this section and the GO notice at
the top of the runbook. A commit cannot name itself: the coordinator's message gives its 40-character hash, the
lead checks it out, and step 0 compares it. This verdict changed the first line of this file, added this section
and replaced the notice between `HOLD-BEGIN` and `HOLD-END` of the runbook; it changed nothing else.

Judged: the code and the commands of commit `40c697e542a633d0cb1bba5f30b63567c5896097`. Its pinned files are
those of round 1 (sha256 of `PIN.sha256` `7aa9bbfc…f64c19`, 105 of 105 files, recomputed by me at the branch
head). Since 73829e5c6 only texts, `rehearsal/` and `results/` changed; since 40c697e54 only `PROGRESS.md`, this
file and the notice. Inputs: the fixer's report, the re-audit of the code (GO on the code; N5 is wider than
recorded) and the re-audit of the runbook (GO for steps 0 to 2, with prose items). What I rely on I checked at
the head myself; where a row rests on somebody else's run it says whose. Labels as in section 1 and round 1:

| evidence label | meaning in this round |
|---|---|
| read | the cited lines were read by me |
| run | run by me in scratch with stand-ins; no file of the port was executed on the host |
| container (mine) | my own named throwaway containers, no host path, no network, removed on exit |
| tripwire, vf-eval | runs of the fixer and the re-auditors, recorded in `results/`; none by me |
| inferred | reasoned, not run: every statement about macOS and Docker Desktop |

### Status of the findings and changes

Runbook lines are those of the text at 40c697e54. The GO notice is 16 lines longer than the notice it replaced,
so in the commit that holds this section every later line lies 16 lines lower.

| finding, change | status | evidence |
|---|---|---|
| A1, change 1 | closed | run: all 30 fenced commands begin with the folder guard (the inline one of step 3 too: read); they use no variable but `$HOME` and `$?`, no `$(…)`, no backtick; `uv` occurs in two, both after `cd /` with `--project <absolute path>`, the dry run first (185, 214). The guard with `echo` for 9 wrong targets from 4 start folders printed once: for an empty path started inside the study folder itself, where the shell stays in that folder. uv on macOS: inferred. |
| A2, change 2, and N1 (round-1 changes 1, 2) | closed | run, through my own command tool (`/bin/bash -c … eval …`) on a stand-in folder whose tool only sleeps: the 2a start returned at once; the status (287) listed ONE process line, the tool, while its waiting shell was alive and not listed; the stop command (428) aimed at the waiting shell, and with its placeholder left in, printed nothing and signalled nothing; aimed at the tool it printed the tool's command line, the log ended `EXIT 143`, nothing was left. read: containers are found by the run label only (verifiers `cli/eval/runner.py:138`, `runtimes/docker/__init__.py:102`); the four delete or signal targets of the runbook are literal (428, 451, 466, 578). vf-eval (fixer, `results/rehearsal_round2.json`): five interruptions, two of them a SIGKILL of vf-eval with a box up, each cleared by the runbook's own points. |
| N2, interpreter (round-1 change 3) | closed | read: `--managed-python` on both uv commands; the interpreter prints its own process line and `INTERPRETER-OK` or `INTERPRETER-DIFFERS` (237); the "must show" rule after 2a, 2b, 2c (309-313, 344, 387). run (fixer): a stand-in that re-executes gives `DIFFERS` and an empty listing. On the Mac: inferred; a difference is a stop in step 1. |
| N3, step 1 (round-1 change 4) | closed | read: 181-182, 214-225, 408-414. Record: the detached sync ended `EXIT 0`. |
| N4, pin handover (round-1 change 5) | closed | read: 2-18, 33-36, 136-138, 157-170; this verdict uses it. run: step 0's first two commands in my worktree print the checked-out hash, `0`, the pin hash and `PIN-OK` (Linux). |
| round-1 change 6, text | closed | read: 439-443, 389-391, 158, 177, 206, 590; the record's six prose mismatches are corrected in the text. |
| round-1 change 7 and change 8 (B10), rehearsal | closed, with limits | run: the 30 fenced commands are equal at be2c17ae6 (rehearsed), 40c697e54 and the head, and 23 of them stand in the record byte for byte after undoing its two substitutions (81 commands, each as one `sh -c '<text>'` started in `/`; the 2a start and one status also through the session's own tool). Never issued: the image build and its status (249, 256) and the five commands of step 3. Deviations of the record: `$HOME` in scratch, root, x86_64, the IPv6 shim for 2c, the section used five times. |
| A3, change 3 | closed | read: the gate is the first statement of `agents/hostile_submission.py` (45-62), `agents/probe_grading.py` (29-46), `redteam/agent_rt.py` (22-39) and stands again before the kill (`hostile_submission.py:202`, `agent_rt.py:483`), the mount (`agent_rt.py:243`) and the replacement of `tar` (`agent_rt.py:486`); `redteam/` is outside the pin and unchanged since 73829e5c6 (run: `git diff --stat`). container (mine): 6 starts without the marker (`killall`, `delete`, `no_tar`, the probe, `hostile killall`, `recon`), each `refused:`, a canary process alive, `tar` in place. tripwire (fixer, re-auditor): 34 starts. The Mac has neither sign (inferred). |
| A4, changes 4c and 5 | closed as specified | container (mine): the script of `tools/check_driver.py`, taken out of the source without running the tool's host part, 27 of 27 and, with `--tmpfs /extra`, 4 of 4: every function refuses, the driver on the grading route runs nothing. read: `physim2_env/grading.py:49-87`, `taskset.py:144-148`; verifiers starts a box with no mount option (`runtimes/docker/__init__.py:196-244`) and, off Linux, no helper with a folder (318-321). |
| A5, changes 4a and 4b | closed | read: `_item.py` in full: no `rmtree`; `rmdir` or `unlink` of listed paths, never a mount point (367-391); an unreadable table raises (169-177). container (mine): a root-owned file below a directory of the uid survives, a mount point is not removed, another uid is left alone. |
| change 6 (B3, B6 to B9, B12) | closed | read: the never-table (56-67), the inventory (69-130); the deletes and signals of the code that runs on the Mac itself are the ones the inventory names (run: a search of the tools, the package and the pinned round-5 files; read: `tools/vfrun.py:60-111`, `tools/prove.py:142-156`, `physim2_env/bundle.py:84-92`). Nothing is uploaded: `push = false` in both configs and in `vfrun.py:133`, and `PRIME_RUNS_MODE=disabled` (verifiers `utils/platform.py:68`). No model-written code runs on the Mac: `validate` and `submit` are sent into the box (`physim2_env/lab_tools.py:69-94`). |
| change 7 (B11), pin | closed | run: `sha256sum -c PIN.sha256` 105 of 105 at the head; the sha256 of `PIN.sha256` equals the runbook's line 17. |
| change 9 (B13 to B15), step 3 | in place as text, never run | read: a STOP line and a block of its own (499-521), now behind a file that the lead creates (`LEAD-GO-STEP3`, 511-518); output to a file; `tools/run_report.py` prints flags, numbers and words from fixed lists, never text (37-59, 122-151); caps as in `configs/qwen_ring_bash.toml:26-28`; no `claude_code` or `codex` in the runbook (run: 0 matches); the disk limit in the by-hand list (483). The free dry run returns before any rollout (verifiers `cli/eval/main.py:114-117`). Open, minor: the price fields are blank; the dry run (494) is not behind the lead's file; "writes it here" (507) asks the lead to edit this file. |
| S1, S2 | closed in round 1 | same pinned files. container (mine): uid 1000, 19999 and 60000 refused; a helper whose identity did not change signals nothing. |
| N5, wider (code re-audit, item 5) | confirmed; minor, Linux only | run, the driver's two pure functions cut out of the source (the module was not imported) on the stored and on crafted mount tables: a table shaped like `--ipc=host` (`/dev/shm` with source `tmpfs`), like `-v /dev:/dev` (`devtmpfs` at `/dev`) and like `--tmpfs /dev/extra` passes; a Mac share (`virtiofs`, `fakeowner`, `fuse.grpcfuse`) is refused wherever it is mounted, below `/dev` too. Needs a container started by hand with such an option and the route's commands replayed in it; the runbook forbids every `docker run` by hand (61); verifiers passes no such option (read). On the Mac those options show Docker Desktop's virtual machine, not the Mac (inferred). |
| N6, N7, N8 | open; minor | as in round 1: unchanged code. |
| `rehearsal/` (new, outside the pin) | minor | read: `rehearsal/issue.py:146-154` and `check_round2.py:357` refuse unless `PHYSIM2_DEV_MACHINE=cloud-container` and Linux, so they refuse on the Mac; on the never-list (64). On the cloud host `issue.py` acts for real inside whatever `--inside` names (code re-audit, item 6). |
| runbook re-audit, items 7, 8, 9 | closed by the notice | The three rules of the GO notice: a 60-minute bound for the "must show" branch; the section used once also when a restarted session cannot tell; step 4's image list may lack the two base images (the record's step 4 printed three images, without `alpine:3.22`: read). They change no command and were not rehearsed. |
| runbook re-audit, items 10, 11, 12 | minor; residual | 10: rule A.1 tests for the old notice, not for the new one; section C's "right text" check is the positive one (138). 11: `docker rm -f` (451) trusts the copied name; the name comes from a listing by label, and a name that begins `vf-` cannot be taken for a container id. 12: a stop in step 1 or 4 has no recovery; see the by-hand list. |
| runbook re-audit, item 14 (step 3) | minor; with the offer of step 3 | see change 9 above and "What remains". |

The lead's note on traces: the smoke test uploads nothing and needs no trace; five result files leave the pilot
folder in step 4, and after a stop the scratch folder with its traces is still on the Mac for the lead. For step 3
the runbook copies the trace out only on the lead's request and only when the report counts no hidden value
(559-569); an upload is the lead's own act.

### What remains

**Before the smoke test: nothing in the repository.** The by-hand list below is the lead's.

**The one-model rollout.** Not now. It may be offered to the lead when all of these hold; none needs a commit:

1. Steps 0 to 2 have passed on the Mac with no deviation but the one that step 2b names, and the lead has read
   the report. In it: `failed_new` holds `b_lab_process_dropped_it_after_loading` and nothing else, and the lines
   `control`, `agent box net` and `item box net` show what a box reaches on the Mac. The network cut was measured
   on Linux only; in step 3 it stands between the model and the Mac's own services.
2. The offer states the price bound: the lead reads p_in and p_out from Prime's Models API, the bound is
   `1.5 x p_in + 0.06 x p_out` dollars plus one request, and it binds only if the provider reports usage. The
   lead gives the price in the go message and does not edit the runbook.
3. The lead's go is the file `LEAD-GO-STEP3`, created by the lead by hand, and the words. The dry run before it
   is free and starts nothing (read); it is not behind that file.
4. Docker Desktop's disk limit is below the Mac's free space.

**A later pass, with a re-audit of its diff, not needed for the Mac run:**

- Code, before the package runs on any Linux machine other than the cloud container: N5 as an exact list of
  (mount point, type) with source `shm` for `/dev/shm`, with the `--ipc=host` and `-v /dev:/dev` tables as
  fixtures; N6; N7; N8; `rehearsal/issue.py` refuses unless `--inside` holds a marker file the operator made.
- Runbook body: the notice's three rules written into their places; rule A.1 as "unless its notice begins
  `**GO for steps 0 to 2.**`"; the removal of point 3 with its own label check (runbook re-audit, item 11); after
  line 182 what a stop in step 1 leaves; step 3's dry run behind the lead's file and "states it in the go
  message" for "writes it here".
- Stale after this verdict: `README.md` lines 13 and 81 and `results/summary.json` still say that the runbook is
  on hold; the pinned `tools/check_runbook.py` fails one check, which asks for the listing that round 2 replaced.

### Residual risks, also with this GO

- Nothing has run on macOS or Docker Desktop. Inferred only: zsh as the session's shell and that a detached
  command outlives its call; BSD `ps`, `shasum`, `tail`; uv and its Python there; the signs of a container and
  the stock mount table in Docker Desktop (if they differ, staging refuses and damages nothing); how a session
  ends a command at its limit. Each of these ends in a stop, not in a repair.
- A vf-eval that is killed outright leaves one container and the laboratory process. The session finds them by
  label and by path and removes them by exact name and pid; `docker rm -f` acts on the name it was given.
- The tools and the laboratory run on the Mac as the lead. `uv sync` runs an unpinned build backend and writes
  `.venv` (about 1 GB), uv's cache and uv's own Python; none of it is removed by the pilot.
- Never run in the runbook's form: the image build of step 1 and its status command; the notice's three rules.
- A stop in step 1 or in step 4 has no recovery in the runbook; what is left is removed by the lead.
- N5 to N8 on Linux hosts; the cloud rehearsal's own scripts act for real on the cloud host.
- Step 3: an untrusted model is root in a container for up to an hour. Docker Desktop's virtual machine and
  verifiers' network cut are the walls, and neither is tested on a Mac before step 2b. The laboratory on the Mac
  answers the model's requests. No command of step 3 has run anywhere, the dry run included.

### By hand, on the Mac (the lead)

In addition to section C of the runbook, section 5 above and the list of round 1:

| when | check | expected |
|---|---|---|
| before | the coordinator's GO message; `git rev-parse HEAD`; the first text line of `RUNBOOK_MAC.md` on disk | a 40-character hash; equal to it; it begins `**GO for steps 0 to 2.**` |
| before | the session | started in the study folder, given that path and the hash; no subagents; one command per call; at any deviation it stops and reports, and nobody repairs by hand what the runbook does not name |
| during | the pilot folders in `$HOME` | not opened in Finder: a `.DS_Store` makes step 4's `rmdir` fail after its deletes (a stop, nothing lost) |
| a stop in step 1 | `.venv` in the study folder; `$HOME/physim2-pilot-20261110`; the image `physim2-ring:1`; a running `uv` or `docker build` | the lead removes what exists before any new start: step 0 expects none of the first three |
| staging says `the box is not recognised as a disposable box` | Docker Desktop differs from stock Docker | a finding to report; change no setting to make it pass |
| after step 2 | the report: the "must hold" line of 2a; both lists of 2b; `control`, `agent box net`, `item box net`, `container_evidence` | as the runbook says; these lines decide whether step 3 can be offered |
| after step 4 | `docker ps -a` and `docker images` against the baseline | no container; at most the four images the runbook names. Left on the Mac: `.venv`, uv's cache and Python, `~/.cache/verifiers`, `/tmp/vf-port-*`, the results folder |
| step 3, if offered | the price in the go message; `LEAD-GO-STEP3` made by the lead; the disk limit; the trace | as under "What remains"; the trace is copied only by the runbook's own command, and uploaded only by the lead |

Not covered by this round: the same as section 6 and round 1. By me: no rollout, nothing on macOS, not the red
team's attacks, not `tools/prove.py --worlds 4`, not the gliders rollout.

## Re-audit, round 3

**VERDICT, 10 Nov 2026: GO for the scripted smoke test on the lead's Mac (steps 0, 1 and 2 of
`RUNBOOK_MAC.md`). The one-model rollout stays NO-GO until that test has passed on the Mac and been reported,
and until the three points that step 3 lists as open are settled.**

The GO covers steps 0, 1 and 2, the section "If a run was interrupted", and step 4 once the lead says the pilot
is over. It holds for ONE commit: the commit that carries this section and the GO notice at the top of the
runbook; the coordinator's message gives its 40-character hash, the lead checks it out, and step 0 compares it.
It replaces the round-2 GO, which was suspended when the Mac session reviewed that commit before running it
(three major and eleven minor points) and the coordinator added a disk requirement (D1):
`af767adbdeac3d00906d7a3394421e1bc4d6e486` is not to be run. This verdict replaced the first line of this file
together with the fixer's suspension note above it, added this section, and replaced the notice between
`HOLD-BEGIN` and `HOLD-END` of the runbook. Apart from notes in `PROGRESS.md` it changed nothing else, and no
command.

Why GO although the re-audit of the runbook said "NO-GO as written, narrowly". Its open items are six texts
and one command. The six texts are now in the GO notice (two rules and four corrections, the means round 2 used
for its three rules). The one command, a comparison of `sys.executable` in step 1, answers a gap that is minor:
I could run it here, and it ends in a stop at step 1 (G1 below). The re-audit of the code said GO. No finding
of the Mac review was rejected: the fixer confirmed each before changing anything, and I confirmed M1, M2, M3,
m5 and m9 against the round-2 code and the verifiers source myself.

Judged: the code and the commands of commit `db3ff5a6eacc6a4ccc66374df5ac3fc0051c75e3`. The two re-audits read
`33173af09acb5e91a9e2757cce84cbdf3da42305`; since then only `PROGRESS.md` changed (run: `git diff --stat`).
Pinned files: sha256 of `PIN.sha256` `cd67eb4b…03e4`, equal to the runbook's pin block; 109 of 109 files match
in a clean archive of the head (run). Against the round-2 pin: 91 files identical, 14 changed, 4 added (run).
Inputs: the fixer's report, the re-audit of the code (GO; minor items) and the re-audit of the runbook. What I
rely on I checked at the head myself; where a row rests on somebody else's run it says whose.

| evidence label | meaning in this round |
|---|---|
| read | the cited lines were read by me (verifiers: the pinned checkout, equal to the installed files) |
| run | run by me in scratch: my own scripts over the texts and records, or the interpreter with a one-line program; no file of the port was executed on the host outside tripwires |
| tripwire (mine) | the package imported on the cloud host in a process where `tools/tripwires.py` was installed first; a made-up credential file in a scratch home |
| container (mine) | one named throwaway container (`python:3.12-slim`, no host path, no network, gone afterwards), `tools/vfrun.py` of the pin and stand-in children |
| container, tripwire, vf-eval (fixer, re-auditors) | their runs, recorded in `results/`; no rollout was made by me |
| inferred | reasoned, not run: every statement about macOS and Docker Desktop |

### The Mac review's findings

Runbook lines are those of the text at db3ff5a6e. The GO notice is 37 lines longer than the notice it replaced,
so in the commit that holds this section every later line of the runbook lies 37 lines lower.

| finding | status | evidence |
|---|---|---|
| M1, the session's environment | closed | read: `tools/vfrun.py:62-72` (nine names pass; the refuse pattern), `87-102`, `116-134` (a child's environment is built from nothing), `137-161` (the Docker context must name a Unix socket); every tool makes the check before it imports the package (`prove.py:41`, `check_probe.py:44`, `make_instances.py:20`, `settle.py:54`, `vfrun.py:404`); `physim2_env/lab_tools.py:174-176`; runbook 250 (a command the session runs itself, the same list), 106-114. The finding was right: at 40c697e54 `child_env` copied everything but one name (read). container (mine): of 28 made-up session names (every `DOCKER_*`, `MCP_*` and `PHYSIM2_*` one, `PYTHONPATH`, keys, proxies) none reaches a child; a child gets 18 names, 10 from the pass list and the run label, 8 set by the tool; the dirty session is refused, 15 names listed, no value printed. vf-eval (fixer, record entries 3 and 4): `6 names, 0 refused`; with `DOCKER_HOST` and `PYTHONPATH` two `FOUND` lines and `tcp://…` as the address. Left open, minor: G1. |
| M2, the signal table | closed by the GO notice, point 3 | read, verifiers `v1/` searched for every kill, group kill, signal and every process start with a time limit: the ten rows of runbook 119-130 match `runtimes/container.py:44-65`, `runtimes/subprocess.py:45-53, 103-129, 197-228`, `utils/version.py:23-31`, `mcp/server.py:112-118` and `tools/vfrun.py:200-215, 264-284`. One sender was missing, as the runbook re-audit found: `runtimes/docker/__init__.py:553-567`, the teardown of every box (`runtimes/base.py:180-195`), starts `docker rm --force <box>` with a limit of 30 s, and Python kills that client at the limit. Python does the same when the waiting process is itself interrupted (CPython 3.12.13 `Lib/subprocess.py:549-568`, read): also in the notice. Not on the route of steps 0 to 2: `runtimes/container.py:136-173` (only through `open_process`, which only the ACP harness calls, `acp/__init__.py:242`), `serve/pool.py`, the package build of `mcp/launch.py:173` (the laboratory runs in the subprocess runtime: `launch.py:335-337`). |
| M3, listeners and the Prime key | closed | read: `physim2_env/_nokey.py:71-91`, `physim2_env/__init__.py:7-9`, `tools/vfeval.py:25-38`, `tools/vfrun.py:75-77, 325, 369-387`, `configs/scripted_ring.toml:12-15`. verifiers reads the file through one function (`utils/prime.py:9-20`; callers `configs/client.py:41, 103`, `runtimes/prime.py:150`, `interception/tunnel/prime.py:36`), the prime-runs SDK through `prime_traces/core/config.py:22-39`. tripwire (mine): the package first gives `stand-in`, key `EMPTY` for the stand-in and for the default client, an empty prime-runs configuration, an exit from `ensure_prime_auth`, and 0 opens and 0 stats of the made-up file with 195 modules of verifiers, the package and the Prime SDKs loaded (vf-eval's entry point, the Docker runtime, the interception server, the laboratory module among them); control, verifiers' client module alone: the file is opened. Both re-auditors: the same with their own traces. vf-eval (fixer): the kernel reported 0 events on the made-up file through 45 rollouts and 3 for the stock import. Listeners: runbook 169-182 names six; read by me `interception/server.py:346, 444-447`, `mcp/server.py:278-283`; the others as the runbook re-audit read them. |
| m1, theta in the status | closed | read: `tools/prove.py:54-74`, `tools/build_reference.py:23-50`; runbook 399 (process lines cut at 160 characters, log lines at 200). container (code re-auditor): the builder's command line and environment hold the path of the 0600 file, not the values. |
| m2, the patterns | closed | read: runbook 399, 560: comparisons with `index()`, letter for letter, against eight beginnings; no pattern is left. vf-eval (fixer, entries 27, 28): the stop command aimed at the waiting shell printed nothing and ended with status 1. |
| m3, a linked pilot folder | closed | read: runbook 261, 605, 735: `test ! -L` on the pilot folder, on `store` and on `scratch` before each `rm -rf`. |
| m4, an orphaned helper | closed; not seen live | read: `tools/vfrun.py:264-284`; runbook 591 and the word `HELPER`. container (code re-auditor): the helper stops with its tool. |
| m5, the laboratory on macOS | closed; macOS inferred | read: verifiers `mcp/server.py:112-118` (the kernel's help is asked for on Linux only); `tools/vfrun.py:299-314`; runbook 129, 591-597. container (mine): a child that dies of SIGKILL ends the tool with status 98 and the line "may be left". vf-eval (fixer, entry 39): `EXIT 98`. Point 4 has never met a live case. |
| m6, the removal | closed | read: runbook 584 (the label is read back before `docker rm -f`). vf-eval (fixer, entries 40 to 43): an unknown name and a container with another label were not removed, the pilot's box was. |
| m7, the laboratory's open port | rule in place, widened by the notice (point 1); bearer deferred to before step 3 | read: runbook 177, 216, 386-394, 633-636. The check command ran three times in the rehearsal, each time before 2a (entries 18, 33, 57); before 2b and 2c it is new. |
| m8, the proxy check | closed; Linux | read: `agents/probe_grading.py:113-134, 180`, `tools/check_probe.py:384`. vf-eval (fixer): `HTTP 403` eight times, 0 hits on the listener. |
| m9, the build backend | closed for versions | read: `pyproject.toml:17-31`, `uv.lock:9-17` (`hatchling==1.33.0` and five packages under it). uv records no hashes for build requirements. |
| m10, the build cache | closed | read: runbook 163-167, 744-758. |
| m11, counts | closed | read: runbook 226, 250, 261: sentinels (`TREE-LISTED`, `CONTAINERS-LISTED`, `IMAGES-LISTED`, `NO-PILOT-FOLDERS`), no count. |
| D1, the disk | closed | read: `tools/vfrun.py:80-84, 164-185, 218-261, 287-314`; the floor is on every start (`prove.py:119-125`, `check_probe.py:113-118`, `vfrun.py:410-422`), and inside the pin vf-eval is started by `vfrun.run_eval` and `vfrun.main` only; the watchdog path holds no delete (the one delete of the file is `clear_run_dir`, an earlier run folder of the same name). Runbook 61-68, 217, 269, 283, 313, 350, 399 (`free:`), 627-632. container (mine): below the floor nothing starts (status 97); a trip sends ONE SIGTERM (the child counted one), status 97, the record written, no file removed (tree compared before and after); a child that ignores SIGTERM gets SIGKILL only after the grace period; the time limit takes the same path (status 98). vf-eval (fixer, entries 6, 8, 20, 47 to 52): the refusal at 8 GiB and a trip that removed the box and stopped the laboratory. Limits: residual risks, the disk. |

### Rounds 1 and 2: nothing reopened

| earlier finding | status | evidence |
|---|---|---|
| A1, working directory | closed | run: all 33 fenced commands begin with the folder guard; they use no variable but `$HOME` and `$?`, no `$(…)`, no backtick. `uv` stands in two (283, 313), both with `--project <absolute path>`, the dry run first: the round-2 text with the disk check in front. |
| A2, N1 to N3, interruption | closed | The status and stop commands are new in round 3 and were rehearsed as a session issues them (`results/rehearsal_round3.json`: 65 commands, each one `sh -c '<text>'`): two interruptions (a stop by the stop command, a vf-eval killed outright), each cleared by the runbook's own points, and two watchdog cases (a refusal before the start, a stop of a running rollout), after which the status listed nothing. run: 11 of the 33 commands are byte for byte the round-2 ones, the interpreter check (338) among them; 22 are new or changed in round 3 (the detached sync, 313, by the disk check in front). |
| A3, A4, A5, S1, S2 | closed | run: byte-identical to the round-2 pin are the driver `_item.py`, `grading.py`, `taskset.py`, `access.py`, `bundle.py`, `store.py`, `agents/hostile_submission.py`, `physim2_script/__init__.py`, `tools/tripwires.py`, `tools/run_report.py`. `agents/probe_grading.py` changed in its opening text and inside the report script it sends into the box; its gate is untouched (read: the diff). |
| N4, pin handover | closed | used by this verdict as in round 2. |
| the three rules of the round-2 notice | now in the body | read: 427, 538-540, 750. |
| change 9, step 3 | in place as text, never run | read: both commands, the dry run too, stand behind `LEAD-GO-STEP3` (654, 674); the price comes in the go message (664-669); `tools/vfrun.py:380-386` refuses a model config without `--model-credentials`. |
| the rehearsal | closed, with limits | run: the 33 fenced commands are equal, block for block, at the rehearsed commit 00947b226 and at the head; each of the 65 recorded commands equals one of them after undoing the recorded substitutions; 26 were issued. Never issued: the image build and its status (350, 357) and the five commands of step 3 (654, 674, 682, 690, 720). After the rehearsal only prose changed: four places of the body (421-423, 588-590, 596-597, 780-784) and the six points of the notice. Deviations of the record: `$HOME` pointed into scratch, root, x86_64, the floor lowered to 0.5 GiB wherever a command had to run (1.8 GiB free there), the Docker context `default`, and the rehearsal went on after `EXIT 97`. |

### The re-auditors' open items, and what is new

| item | status | evidence |
|---|---|---|
| runbook re-audit 2: one row of the signal table | closed by the notice, point 3 | see M2. |
| runbook re-audit 5: the Docker check before 2a only | closed by the notice, point 1 | see m7. |
| runbook re-audit 6: section C asks for 8 GiB | closed by the notice, point 5 | the floor is 8 GiB and steps 1 and 2 write about 3. This Mac had 16 at its review. |
| runbook re-audit 7: `~/.docker/buildx/` | closed by the notice, point 4 | as the re-audit saw it on Linux; inferred for the Mac. |
| runbook re-audit 11: the folders after a stop | closed by the notice, point 2 | read: point 6 runs only at a first interruption and never after `EXIT 97` (600-611); step 4 needs both result files (735). |
| runbook re-audit 12: the opening lines | closed by the notice, point 6 | read: 27-28 against 780-784. |
| G1 (runbook re-audit 10, code re-audit 1): `PYTHONEXECUTABLE`, `__PYVENV_LAUNCHER__` | minor; residual; by hand | Both re-audits call it macOS-only and inferred. It is neither. read: CPython 3.12 takes both variables on every POSIX system (`Modules/getpath.c:901-902`, v3.12.13) and uses them for `sys.executable` AND for the search for the environment (`Modules/getpath.py:302-320, 349`). run (the port's interpreter with a one-line program): with either variable set, `sys.executable` is the variable's value, `sys.prefix` leaves the environment (here `/usr`), and a package of the environment is not found (`ModuleNotFoundError`). A session that holds one of them therefore fails step 1's import check, before step 2: a stop (on the Mac: inferred from the same code). It passes only if the interpreter then finds the same four package versions elsewhere (the value points into another environment that has them, or the user's own site-packages do); the tool's vf-eval and laboratory would then run under the interpreter the variable names and the status command would not list them (the tool stays listed and stoppable; containers are found by label). Not closed: step 0 and `ENV_REFUSE` do not name the two. The proposed comparison of `sys.executable` in step 1 would stand after the import check, which already stops the likely case. |
| runbook re-audit 15: no command to wait | minor; residual | the session waits by asking for the status again; it issues no `sleep` of its own. |
| code re-audit 4: a vf-eval that ends with 130 after a SIGTERM from outside the tool counts as ended | minor | read: `vfrun.py:304`. Off the runbook's path, which signals the tool first; `prove.py` then stops for lack of an episode. |
| code re-audit 5: four limits of the watchdog | minor | read: `vfrun.py:255-257` (a stop of the tool during the grace period sends a second SIGTERM and loses the record), `307-310` (no "may be left" after a SIGKILL; the words `SIGTERM, then SIGKILL` are in the line: container, mine), a failing `statvfs` ends the tool with status 1 after the stop path ran, and `uv sync`, `docker build` and the helpers are checked before they start, not while they run. |
| code re-audit 7: `rehearsal/issue3.py` accepts `HOME` | minor; cloud host only | outside the pin, refuses off Linux, on the Mac's never-list (as the code re-audit read it; not checked by me). |
| new, by me | nothing of major severity | Python's kill of a client when its caller is interrupted (in the notice, point 3); the watchdog's reach in step 3 (below); stale texts (below). |

### What remains

**Before the smoke test: nothing in the repository.** The by-hand list below is the lead's.

**The one-model rollout.** Not now. It may be offered to the lead when all of these hold:

1. Steps 0 to 2 have passed on the Mac with no deviation but the one that step 2b names, and the lead has read
   the report: `failed_new` holds `b_lab_process_dropped_it_after_loading` and nothing else, and the lines
   `control`, `agent box net`, `item box net` and `proxy_loopback_names` show what a box reaches on the Mac.
2. The lead has decided about Docker Desktop's disk and says so in the go message (see "By hand").
3. The laboratory has a bearer, built and audited, or the lead accepts in the go message that the network cut
   of the box is the only thing between a container and the laboratory's port.
4. The go message states the price bound, and the lead has created `LEAD-GO-STEP3` by hand.
5. The two start commands of step 3 are new in round 3. The runbook re-audit read them (its item 14); they
   have run nowhere. Before the offer the free dry run is rehearsed in the cloud container: it calls no model
   and loads no credential.

**A later pass, with a rehearsal and a re-audit of its diff; not needed for steps 0 to 2:**

- Runbook body: the six points of the notice written into their places. G1: both names in step 0's pattern and
  in `ENV_REFUSE` (`tools/vfrun.py:67`, a pinned file, so a new pin); it can be rehearsed on Linux. A command to
  wait.
- Code: status 130 and 143 of vf-eval treated as a stop (`vfrun.py:304`); no second SIGTERM and no lost record
  in the grace period (`255-257`); "may be left" in the disk message; a record when `statvfs` fails;
  `rehearsal/issue3.py` refuses `HOME` and `PATH`.
- Before step 3: the bearer; a size limit for what a box can write, if the lead does not lower Docker Desktop's
  limit (verifiers has none: `runtimes/container.py:38-41`).
- Still open from rounds 1 and 2, Linux hosts only: N5 to N8.
- Stale after this verdict: `README.md` (lines 14 and 99-100) and `results/summary.json`
  (`host_safety.round_3_of_fixes.status`) still say that the runbook is on hold.

### Residual risks, also with this GO

- **Nothing has run on macOS or Docker Desktop.** Inferred only: zsh as the session's shell and that a detached
  command outlives its call; BSD `ps`, `awk`, `df -Pk`, `cut`, `nohup`, `shasum`; uv 0.12.8 on the Mac against
  0.11.32 in the rehearsal (the wording of the dry run may differ); the Docker context and its socket; the signs
  of a container and the mount table in Docker Desktop; that a laboratory outlives a killed vf-eval there. Each
  of these ends in a stop, not in a repair.
- **The session's environment.** G1. `PATH` and `HOME` reach every process as they are: another `docker` binary
  or another local engine is caught only by step 0's context lines and by the lead's `command -v`. Other
  `PYTHON*`, `DYLD_*` and proxy names reach the tool's own process, not its children.
- **The disk.** The watchdog is a brake, not a wall. It looks every 15 s and stops a rollout; `uv sync`, the
  image build and the helpers are checked before they start only. It frees nothing: after a trip the Mac is
  still near the floor. With 16 GiB free, about 3 GiB written and a disk that is 97% full, a trip in steps 1 or
  2 cannot be excluded on this Mac; it is a clean stop, and what step 1 left is then the lead's to remove.
- **A vf-eval that is killed outright** leaves its box and, on macOS, its laboratory; the session finds them by
  label and by exact command line and removes them by exact name and pid. Two small folders stay.
- **The laboratory's port has no secret** in steps 0 to 2. Another process on the Mac, or a container that
  reaches the Mac's loopback, could spend a rollout's budget: a risk to the pilot's result, not to the Mac. The
  rule: nothing else runs in Docker.
- **As the lead.** The tools and the laboratory run on the Mac as the lead. `uv sync` runs a build backend
  whose versions are pinned but not hashed, and writes `.venv` (about 1 GB), uv's cache and uv's own Python;
  the pilot removes none of it. The `docker` client reads its own configuration in the home folder and may ask
  its credential helper when it pulls the two public base images (inferred; no model credential is involved).
- **Never run in the runbook's form:** the image build and its status command; point 4 of "If a run was
  interrupted"; the rule for a second interruption; a stop of a vf-eval by its own pid; `EXIT 143`; a `HELPER`
  line; the Docker check before 2b and 2c; every command of step 3.
- **Step 3.** An untrusted model is root in a container for up to an hour; Docker Desktop's virtual machine and
  verifiers' network cut are the walls, neither tested on a Mac before step 2b. The disk and the bearer are
  open (above).
- **Linux hosts:** N5 to N8; the cloud rehearsal's own scripts act for real on the cloud host.

### By hand (the lead, and the Mac session before its first command)

In addition to section C of the runbook and to the lists of rounds 1 and 2:

| when | check | expected |
|---|---|---|
| before | the coordinator's GO message; `git rev-parse HEAD`; the first text line of `RUNBOOK_MAC.md` on disk | a 40-character hash; equal to it; it begins `**GO for steps 0 to 2.**` and names round 3. Not `af767adb…` |
| before | G1: in the terminal that starts the session, `env \| cut -d= -f1 \| grep -E '^(PYTHONEXECUTABLE\|__PYVENV_LAUNCHER__)$'`; the Mac session, which listed the names of its own environment in its review, says the same for these two | nothing. If the session holds one: do not start; report |
| before | the disk, steps 0 to 2: `df -Pk "$HOME"` | at least 11 GiB available (the notice, point 5); 16 at the review. Nothing else that writes much runs for the 45 minutes (downloads, backups, sync). Docker Desktop's limit need not change for these steps |
| before | the checkout | directly under the home folder, not opened in Finder: a `.DS_Store` is an untracked file, and step 0 then stops |
| during | Docker | no other container for the whole of step 2; the session checks before 2a, 2b and 2c, and the lead starts none in between |
| the floor trips (`refused:`, `EXIT 97`) | the session stops and reports; nobody deletes anything to go on | the lead decides whether to free space and start again; after a stop in step 1 the lead first removes `.venv`, the pilot folder and the image, as round 2's list says |
| any stop that does not end in point 6 | `$HOME/physim2-pilot-20261110`, the hidden store in it | still there (the notice, point 2). If both result files exist, step 4 removes it on the lead's word; if not, the lead removes it by hand |
| after step 2 | the report: the "must hold" line of 2a; both lists of 2b; `control`, `agent box net` with `proxy_loopback_names`, `item box net`, `container_evidence` | as the runbook says; these lines decide whether step 3 can be offered |
| step 3, the disk: the lead's decision, in the go message | The facts: 16 GiB free at the review; Docker Desktop's disk image can grow to its limit, far above that (apparent size about 460 GiB). The watchdog looks every 15 s and then gives vf-eval up to 120 s to remove the box (`tools/vfrun.py:56, 82`); it does not give space back. That is enough against slow growth. A model that writes as fast as the disk allows can use 8 GiB between two looks, so the Mac's disk can be full before the rollout is stopped (inferred from the code; not measured) | one of: (a) lower Docker Desktop's limit to below the free space less the floor: the sure wall; Docker Desktop may then discard its disk image with the lead's other images, containers and volumes (inferred: read Docker's own warning first); (b) leave the limit and accept the watchdog as the only brake for this one hour. The session changes no Docker setting and deletes nothing |
| step 3, the rest | the bearer or its acceptance; the price; `LEAD-GO-STEP3` made by the lead; the trace | as under "What remains"; the trace is copied only by the runbook's own command and uploaded only by the lead |

Not covered by this round: the same as section 6 and rounds 1 and 2. By me: no rollout, nothing on macOS. I did
not rerun `tools/check_round3.py`, `tools/check_interrupt.py` and `tools/check_runbook.py` (the code re-auditor
did: 48 of 48, 8 of 8, 46 of 46), nor `tools/check_safety.py`, the red team's attacks, `tools/prove.py
--worlds 4` or the gliders rollout. Of the changed check tools (pinned, on the Mac's never-list) I read the
opening texts and searched the added lines for calls that kill or delete: they stand in scripts that are sent
into containers and in the harness that starts them. The code re-audit read that diff in full.

## Re-audit, round 4

**VERDICT, 11 Nov 2026: GO for the scripted smoke test on the lead's Mac (steps 0, 1 and 2 of
`RUNBOOK_MAC.md`). NO-GO for step 3, the model rollouts driven by request files: two findings of major severity
are open (K4 and X6 below). Each needs a change of a pinned file, so a new pin, a re-audit of its diff and a
rehearsal of what changed.**

The GO covers steps 0, 1 and 2, the section "If a run was interrupted" as it applies to step 2, and step 4 once
the lead says the pilot is over. It holds for ONE commit: the commit that carries this section and the GO notice
at the top of the runbook; the coordinator's message gives its 40-character hash, the lead checks it out, and
step 0 compares it. It replaces the round-3 GO: `08bd5a669867623a476e7446a74612be47001b3b` is not to be run any
more. This verdict replaced the first line of this file, added this section, and replaced the notice between
`HOLD-BEGIN` and `HOLD-END` of the runbook (GO for steps 0 to 2, NO-GO for step 3 in words, three corrections of
wording); it changed nothing else and no command. Neither file is listed in `PIN.sha256` (run: 0 matches).

Judged: the code of the second round-4 pin, `c7db465d5fc990aa41d28cfb6cfc36eb34f8b2ed` (sha256 of `PIN.sha256`
`776d9a33…fadc`, equal to the runbook's pin block; 135 of 135 files match at the branch head: run), and the
commands as rehearsed from a fresh clone of the first round-4 pin, `d9694f3e5b6c92a98c13fb36f02645f01f18728c`.
Between the rehearsed and the judged commit: the 41 fenced commands and the 2 inline commands are byte for byte
the same (run: my script); the prose changed in six places (the opening paragraph, section B's network paragraph, 3.1,
3g, 3h, the closing section), and so did the pin block, the block of facts and the example config (the removed
key `reasoning_summary`); five pinned files changed
(`rollout_config.py`, `check_config.py`, `check_round4_step3.py`, `run_report.py`, the example config), of which
steps 0 to 2 use one, `run_report.py` (one field of 2c's report: the turn count; read). After `c7db465d5` only
`results/`, `rehearsal/`, this file and the notice changed in the three folders the pilot uses (run: `git diff
--stat`). Inputs: the integrator's report and three audits: code (GO for steps 0 to 2, NO-GO for step 3), runbook
(GO for steps 0 to 3, minor items) and exam integrity (one major, scores quotable on conditions). What I rely on
I checked at the head myself; where a row rests on somebody else's run it says whose.

| evidence label | meaning in this round |
|---|---|
| read | the cited lines were read by me (verifiers: the pinned checkout; mcp 2.0.0, starlette 1.10.0, uvicorn 0.54.0: the versions of `uv.lock`, read in an installed copy of them) |
| run | run by me: scripts over texts and records, `sha256sum`, `git`, and one key scan (a Python process that read the values from its environment and printed file names and counts only); no file of the port was executed |
| tripwire, container, vf-eval (integrator, fixers, auditors) | their runs, recorded in `results/`; none by me |
| inferred | reasoned, not run: every statement about macOS and Docker Desktop |

### What changed since 08bd5a66

| area | change | where (pinned unless said) | checked by me |
|---|---|---|---|
| the laboratory | a 256-bit bearer per rollout, in vf-eval's memory only; `401` without it before the application; DNS-rebinding protection on (Host `127.0.0.1:<port>` only); the box's proxy adds the header for laboratory requests | `physim2_env/bearer.py`, `lab_tools.py`, `runtime.py`, `access.py` | read |
| the boxes | caps added to every box and read back from the engine before use: 2 CPUs, at most 4 GB without swap, 512 processes, read-only root, memory-backed `/workspace` 1 GiB, `/tmp` 512 MiB, `/etc/physim2`, `/runtime`; a config can only lower memory | `boxcaps.py`, `runtime.py` | read (the code audit read and the fixers measured the rest) |
| the image | `physim2-ring:2`: verifiers' `bash` harness preinstalled from hashed pins, so a box downloads nothing at set-up; the scientific wheels hashed (`ring-requirements.txt` says the aarch64 compile gives the same file) | `docker/` (now pinned) | read |
| the driver guard | the four memory file systems of a capped box are accepted mount points | `public/_item.py` (+9 lines) | read: see K1 |
| the spend stop | one counted client in vf-eval; worst-case counting of missing usage, errors and streams without usage; mandatory `max_context_tokens`; the provider's cost field when higher; the lead's standing go `LEAD-GO-MODEL-SPEND.json` and one ceiling over this Mac's ledger and the program's shared ledger | `spend.py`, `tools/vfrun.py`, `tools/check_request.py` | read |
| step 3 | request route `rollout-job/v1` (stages instance, reference, dry-run, rollout, close), strict config schema, publication folder with key scan and manifest | `tools/check_request.py`, `tools/vfrun.py`, `tools/pack_rollout.py`, `rollout_config.py`, `tools/check_config.py`, `profiles.py` | read |
| the exam | rulings E1 to E15 (list in the report to the coordinator; E16 not done); profile `ring` with exam config `ring_r4` (64 items, 256 samples, reset 17 ticks) | `taskset.py`, `grading.py`, `access.py`, `capture.py`, `bundle.py`, `TASK.md.tmpl`, `public/`, `agents/keep_baseline.py` | read in part (X1 to X11) |
| the session's environment | refused names now include `PYTHONEXECUTABLE`, `__PYVENV_LAUNCHER__` and `DYLD_*` (step 0 and every tool); the nine names a child inherits are unchanged and do not include `SSL_CERT_FILE` | `tools/vfrun.py:74, 82-84`; runbook step 0 | read |
| the runbook | 43 commands (35 in round 3), 20 of them byte for byte round 3's; every one starts with the folder guard; no `$(...)`, no backtick, no variable but `$HOME` and `$?`; the destructive targets are round 3's four (one pid after its command line was compared, one container by exact name after its label was read back, the two pilot subfolders after link checks, in point 6 and step 4) | `RUNBOOK_MAC.md` (not pinned) | run (script) |
| the pin | 135 files (109): `docker/`, `physim2_verifier/` and the new tools added | `PIN.sha256` | run |

Every kill, delete, move or mode change added since 08bd5a66 outside `tests/`, `rehearsal/` and `results/` stands
in a box script behind the marker gate (`agents/probe_caps.py`, `public/validate.py`), in a command sent into a
box (`taskset.py`), in the image build, in a development check on the Mac's never-list, in `tools/vfrun.py`'s stop
of its own child, or replaces a file inside the pilot folder (`access.py`, `vfrun.py`) (run: a search of the diff
for 15 primitives; read: each hit).

### The code audit (K1 to K8)

| item | severity | status | evidence (mine unless said) |
|---|---|---|---|
| K1 the driver guard accepts any tmpfs at `/workspace`, `/tmp`, `/etc/physim2`, `/runtime` | minor, Linux hosts only | open; same class as N5 | read (`_item.py:95, 169-171`): a host tmpfs bound there by a hand-started Linux container passes (round 3 refused it). A Mac folder is never a tmpfs and is refused wherever it is mounted; every `docker run` by hand is on the never-list (inferred for the Mac). Not a reopening of A4/A5 (below). Fix: require the box's own `size=` option |
| K2 capture: directories not counted; a tar error in mid-file leaves an unlisted partial file | minor | open | auditor's container run (22 hostile archives, nothing outside the destination); not repeated |
| K3 the bearer | none | closed | read: `bearer.py` in full, `lab_tools.py:254-262` |
| **K4 a box can push unbounded data into processes on the Mac** | **major, step 3** | **open: blocks step 3** | read: the laboratory's `check` runs `physim2.validate` from `/workspace` (`access.py:86-89, 355`), which the agent, root in its box, can rewrite; verifiers reads that command's whole output into vf-eval's memory (`runtime.py:96-99` delegates to `vf:runtimes/container.py:44-63`, `proc.communicate()` at line 59), for up to `check_timeout` (`access.py:175`); a request to the laboratory with the bearer is read whole (`mcp/server/streamable_http.py:537`, `await request.body()`; uvicorn sets no body limit); the proxy's pump feeds every chunk into an unbounded buffer (`runtime.py:167-178`). The box caps bound what a box holds, not what it sends. Fix: cap the validator's output in the box (`... \| head -c 1048576`), refuse request bodies above a limit in `bearer.guard` (Content-Length and counted bytes), bound the relay buffer; a test for each |
| K5 spend stop: `check_shape` is a deny-list; the chained prompt bound ignores non-message fields outside `_rest_hash`; failed spend-log writes are silent | minor, step 3 | open | read (`spend.py:119-172`). Effect if a provider honours such a field: one call can cost more than "one worst-case call" (up to the model's window instead of `max_context_tokens`), or be routed elsewhere; the provider's cost field still counts when higher. Fix: an allow-list of request keys; every non-message key in the hash |
| K6 strict config schema | none | closed | read (`rollout_config.py`, `check_config.py`); the block of facts equals `check_request.py --facts` (code auditor, tripwire) |
| K7 the model key | none | closed | read (`vfrun.py`: `ENV_PASS`, the model names only with `--model-credentials`); run: 0 hits for the values of `PRIME_API_KEY`, `HF_TOKEN`, `WANDB_API_KEY` (plain and base64 at three alignments) in 274 files of `round6/rollouts` and `round6/vfport`. Minor: `pack_rollout.py`'s base64 needle has one alignment |
| K8 the pin | none | closed | run (135/135; both edited files outside it); every file that runs on the Mac is listed (`docker/`, `physim2_verifier/`, tools, agents, configs, `uv.lock`); `tests/` and `rehearsal/` are not, and are on the never-list |

### The runbook audit (T1 to T18)

| item | severity | status |
|---|---|---|
| T1 no accidental start of a model from steps 0 to 2 | none | closed (read: the command form refuses a config that is not scripted; the rollout stage needs a request, the go file, `--model-credentials prime`) |
| T2 "the tools check the last three themselves" (3, opening) | minor, step 3 | open: no tool checks that steps 0 to 2 passed |
| T3 the go file: placeholders inside double quotes; the session writes the file on the lead's word, where an earlier decision had the lead make it by hand | minor, step 3 | open; the lead confirms the procedure before step 3 |
| T4 "no single call can cost more than the worst case" holds at the listed prices only | minor, step 3 | open (with K5) |
| T5 3b's "the bound you computed yourself": no command computes it | minor, step 3 | open |
| T6 refusals print `refused:` and exit 2 | none | closed |
| T7 status commands print no key and no hidden value | none | closed |
| T8 point 8 asks to read the log's last lines, which 3f forbids | minor, step 3 | open |
| T9 `close` checks the pin first: a cut job must be closed at its own commit | minor, step 3 | open (read: `vfrun.py:645, 652`) |
| T10 `EXIT 97` in step 3: two readings, both safe | minor, step 3 | open |
| T11 3f's "wall time plus 160 minutes" equals the tool's own deadline (`GRADING_ALLOWANCE_S`, `vfrun.py:468, 777`) | minor, step 3 | open |
| T12 an interrupted pack (`publish/<job>` without `MANIFEST.json`) | minor, step 3 | open |
| T13 the Mac runner's protocol is checkable from the block of facts | none; one mismatch | closed; minor: the runner accepts requests from more places than 3a reads (ends in a refusal at 3a) |
| T14 section B: "`DYLD_*` not looked for" is false; `git rev-parse` missing from the key table | minor | the first is corrected by the notice (point 1); the second is step 3, open |
| T15 "If a run was interrupted" on paper, per phase | none | closed for step 2; step 3's cases as listed by the auditor |
| T16 the rehearsal record against the text | none | closed; I repeated the comparison of commands (above) |
| T17 macOS differences end in a stop (`Error: No such object`, zsh `noclobber`, `chpwd` output, `nohup` notice, the session's sandbox) | minor | point 3 of the notice for the first; the rest residual |
| T18 the Mac review's minor findings | | see below |

### The exam-integrity audit (X1 to X11)

| item | severity | status |
|---|---|---|
| X1 E1, the end of the run: graded on the last checkpoint after a failed run (at most 30 s or one model call old), while the statement says "at the moment your run ends" | minor (wording) | open |
| X2 E2, the baseline | none | closed (records: an untouched box scores as the null policy, below K) |
| X3 E3, fallback and arithmetic | none; two notes | closed: the round-5 cross-check gives identical scores for six predictors (largest difference 0.0) at the profile `ring_r4` (`results/round4_exam.json`, entries 41 to 46 of `proof.checks`: read); no grading file changed after that proof (run: `git diff --stat 9dafd57df c7db465d5`). Notes: the reason word of a fallback comes from the predictor's stderr; `not_a_grade` scores 0.0 |
| X4 E4 to E7 | none | closed (read: `TASK.md.tmpl:9, 49, 77, 94-100`, `bundle.py:190-230`, `public/labclient.py:22, 46, 125`; E7: Lab and exam both `build_world(inst["theta"])`, `round5/agentenv/evaluator/instance.py:107`, `lab_service.py:52`) |
| X5 E8: the card's envelope and per-item memory are fixed numbers while a config may lower the box; `/dev/shm` and the 256-process item limit undisclosed | minor | open (read: `round5/agentenv/evaluator/lab_service.py:93`) |
| **X6 E9: `validate` says "as graded" for predictors that fail in grading** | **major (exam integrity), step 3** | **open: blocks step 3.** read (`public/validate.py:58-75, 175-238`, the copy at 206, `/workspace` closed at 218): the check copies the agent's own `physim2/` (added files included; `package_changes` looks at manifest entries only) and closes `/workspace` only, so a predictor that reads `/tmp`, `/dev/shm` or an added `physim2/` file passes here and fails every item in grading (all 64 then fall back to the null policy). Auditor's container run: `ok: true, as_graded: true` for two such predictors. Fix: copy `physim2/` from the manifest entries only and fail on a mismatch; close `/tmp` and `/dev/shm` to other users during the check; both cases into `check_round4` |
| X7 gaming the grader | minor residual | jointly chosen samples still gain about 0.4% at 256 samples (about one standard error) |
| X8 leaks in the box | none | closed |
| X9 no `--max-reply-mib` on `driver_cmd` (default 64 MiB per item) | minor | open (read: `_item.py:694`) |
| X10 the caps from the agent's side | none | closed apart from X5 |
| X11 what qwen_ring_002 showed; three changes before the next rollouts (X6; E16; `python -m physim2.validate` forwarded to `lab.validate`) | | recommendations |

### The Mac review's minor findings (identifiers only)

Status as fixer B reported it and as the runbook audit read the text; spot-checked by me where marked.

| status | findings |
|---|---|
| closed in code | CRED-5 (the bearer: read), SIG-3, G1 (both names refused: read), NEWC-1, RB-8 (`--ignored`, `--no-optional-locks`: read), RB-3/R3-4, INV-9 (`--no-cross-check` kept: read), DOCK-3/INV-4/INV-2 |
| closed in text | SIG-2 (read), INV-7 (read), DEL-2 (read), DEL-3/INV-6 (read), the apt and apk mirrors (read), RB-7, INV-5 (read), INV-8 (read), RB-1, RB-2 (runbook audit; fixer B had deferred it), RB-9, CRED-1 (read) |
| accepted with reason, in text | DEL-1 (read), DOCK-5 (read), R3-3 |
| closed in part | R3-8; R3-7 (`DYLD_*` refused; the stale sentence is point 1 of the notice); INV-3/R3-9 (disclosed); DOCK-1/RB-4/R3-1/RB-5 (the tools refuse a context that is not a local Unix socket) |
| open, minor | CRED-2 (git's and docker's credential helpers are not in section B); DOCK-4 (mitigated: a box carries no extra mount; the guard is unchanged; said in `README.md` only) |
| deferred | CRED-4/CMD-14 (build backend pinned by version, not hash); RB-6 (needs the Mac); CMD-5, SIG-1, R3-2, R3-5, INV-1 (the appendix gives no text); the list "not covered by anyone" |

### Rounds 1 to 3: nothing reopened

| earlier finding | status | evidence |
|---|---|---|
| A1 working directory | closed | run: 43 of 43 commands begin with the folder guard; `uv` in two commands, both with `--project <absolute path>`, the dry run first |
| A2, N1 to N3, interruption | closed | the status and stop commands are round 3's with the same matching; rehearsed again as `sh -c` lines (record: one stop by the stop command, `EXIT 130`, a reset; a watchdog trip, `EXIT 97`; in step 3 a SIGKILL of tool and vf-eval cleared by points 1, 3, 5 and 8) |
| A3 box scripts | closed | the new box script `agents/probe_caps.py` deletes only its own one-byte file behind the marker gate (code audit, read; the hit read by me) |
| A4, A5 driver | closed for the Mac; narrowed on Linux | `_item.py` changed in the allow-list only (K1): a Mac share is still refused wherever it is mounted; no `rmtree`, unlink and rmdir of listed paths only (unchanged lines). K1 joins N5 as a Linux-host residual |
| S1, S2, N4 | closed | unchanged; N4 used by this verdict |
| N5 to N8 | open, minor, Linux hosts only | unchanged, plus K1 |
| M1 to M3, m1 to m11, D1 (round 3) | closed | `ENV_PASS` unchanged, `ENV_REFUSE` wider (read); `_nokey` and the stand-in client unchanged for scripted runs; the watchdog on every start (record: `EXIT 97`) |
| G1 | closed | read: step 0's pattern and `ENV_REFUSE` hold both names |
| change 9 (step 3) | replaced | by the request route of round 4; NO-GO in this round (K4, X6) |

### The Mac runner's protocol: can the pin meet it?

Yes, as far as a program can check it (runbook audit T13; read by me): the request keys and shapes, the strict
config schema with its forbidden fields, the profile `ring` with 64 items, the scripted policies of the reference
table (`null`, `D`, `P0`, `PM`, `S`, `C`), the stages, the publication files and the 20 MB / 50 MB limits stand in
the block of facts between markers, which `tools/check_request.py --facts` prints; the crash clean-up is point 8
of "If a run was interrupted" with stage `close`; `SSL_CERT_FILE` is not on the tools' allow-list; the key
reaches vf-eval by the environment only. What this pin cannot give the runner is a rollout: the route is in
place, but step 3 is not released (K4, X6), so no request should name this commit.

### What remains before GO for steps 0 to 3

1. **K4** (major): a byte cap on the validator's output inside the box; a body limit in `bearer.guard`; a bounded
   relay buffer in `runtime.py`; one test each (a box that writes without end must not grow vf-eval or the
   laboratory beyond a fixed bound).
2. **X6** (major): `validate` copies `physim2/` from the manifest entries only and fails on any difference;
   `/tmp` and `/dev/shm` are closed to other users for the check; the two predictors of the exam audit fail the
   check; `check_round4` gains both cases.
3. Same pin, minor: K1 (`size=` on the four tmpfs mounts), K2, K5 (allow-list of request keys; all non-message
   keys in the hash; a failed spend-log write is not silent), X1 (one clause in §4), X5 (card rendered from the
   run; `/dev/shm` and 256 processes disclosed), X9 (`--max-reply-mib 1`).
4. Runbook text of step 3: T2, T3, T4, T5, T8, T9, T10, T11, T12, the `git rev-parse` row of T14, the request
   source of T13; and step 0 should say what a `.venv` and an image `physim2-ring:2` left by this pin's steps 1
   and 2 mean (today both are a stop).
5. A new pin, a re-audit of its diff, a rehearsal of every changed command and of one model job from a request
   (at least to the first model call, with the new caps exercised by a box that floods), and a verdict.

### Scores from this pin

Not quotable without conditions. The exam audit found one fault that can make a run's score misleading (X6: an
agent trapped by the false "as graded" scores the null policy on all 64 items), and the top of the scale is
unknown until ruling E16's two reference rows exist (the strong model scored above C on the ring). A score of
this code may be quoted only with its `n_failed` and fallback reasons, with `infrastructure_failed_items` = 0,
without `grading error` or `not_a_grade`, and, for a run whose items failed for `validation failed`, only after
its detail was read for the X6 trap; and not as a measure of how hard the ring is. qwen_ring_002 (0.786, no
failed item, no fallback; code of `d9694f3e5`, whose grading files equal this pin's) meets these conditions.

### Residual risks, also with this GO

- **Nothing has run on macOS or Docker Desktop** (inferred only, each ending in a stop rather than a repair):
  zsh as the session's shell and a detached command outliving its call; BSD `ps`, `awk`, `df -Pk`, `shasum`;
  uv's managed Python and its command line; that Docker Desktop applies `--read-only`, `--tmpfs`, `--memory`,
  `--pids-limit` and `--cpus` as the Linux engine does (the caps are read back and a box without them is not
  used); the signs of a container and the mount table there; that a laboratory outlives a killed vf-eval.
- **Never run in the runbook's form:** the image build of step 1 and its status command (built in the cloud with
  two proxy arguments the Mac does not use); step 4; point 4 of "If a run was interrupted"; the rule for a second
  interruption; a stop of a vf-eval by its own pid.
- **As the lead:** the tools and the laboratory run on the Mac as the lead; `uv sync` runs a build backend pinned
  by version, not hash (CRED-4); the `docker` client may ask its credential helper when it pulls the base image
  (CRED-2).
- **The disk:** the watchdog is a brake, not a wall; `uv sync` and the image build are checked before they start
  only.
- **Linux hosts:** N5 to N8 and K1; the cloud rehearsal's own scripts act for real on the cloud host.
- **Step 3, when a later pin releases it:** an untrusted model is root in a capped box for up to 180 minutes;
  Docker Desktop's virtual machine and verifiers' network cut are the walls (2b measures the cut on the Mac);
  the spend stop rests on the provider's usage and was seen to stop a run only against the stand-in endpoint
  (`results/round4_step3.json`, R11, R14); the ledger ceiling was seen to refuse under tripwires (D19 to D19c) and
  to block the next job while a cut job's row was open (rehearsal).

### By hand (the lead, and the Mac session before its first command)

In addition to section C of the runbook and the lists of rounds 1 to 3:

| when | check | expected |
|---|---|---|
| before | the coordinator's GO message; `git rev-parse HEAD`; the first text line of `RUNBOOK_MAC.md` on disk | a 40-character hash; equal to it; it begins `**GO for steps 0 to 2.**` and names round 4. Not `08bd5a66…` |
| before | nothing of round 3 on the Mac: `ls "$HOME/physim2-pilot-20261110"`, `docker images physim2-ring`, `.venv` in the study folder | none (section C and step 0 expect none) |
| before | Docker Desktop: 4 CPUs and at least 6 GB for its virtual machine; at least 11 GiB free on the home folder's file system | as section C says; nothing changed by the pilot |
| after step 2b | the report: both lists of `probe.log`; `staging` with `box_limits`; `control`; `agent box net` with `proxy_loopback_names`; `item box net` | `failed_new` holds `b_lab_process_dropped_it_after_loading` only; `box_limits` shows the caps; these lines are what a later step-3 GO rests on (the network cut and the caps on Docker Desktop) |
| after the pilot | before the next pin's step 0 | step 4 on the lead's word; then the lead removes `.venv` (or uses a fresh checkout) and the image `physim2-ring:2` by hand, unless the next runbook says otherwise |
| step 3 | | not from this commit. The next pin's verdict says what it needs (above) |

Not covered by this round: the same as section 6 and rounds 1 to 3. By me: no rollout, no container, nothing on
macOS; I did not rerun the check tools (`check_runbook.py` reads the notice's first line only for `GO for steps 0
to 2.` or `0 to 3.`: read, lines 297-300), `tools/check_step3.py` or the exam proof, and I did not repeat the
auditors' container runs (capture, E9). The Mac review's text was read; no detail of the lead's machine is
written here.

## Re-audit, round 4, second pass

**VERDICT, 11 Nov 2026: GO for the scripted smoke test on the lead's Mac (steps 0, 1 and 2 of
`RUNBOOK_MAC.md`). NO-GO for step 3, the model rollouts driven by request files: two findings of major severity
are open (K9 of the code audit and X13 of the exam audit, below). Each needs a change of a pinned file, so a new
pin, a re-audit of its diff, a flood case through vf-eval and a verdict. Scores of this pin may be quoted only on
the conditions under "Scores from this pin".**

The GO covers steps 0, 1 and 2, the section "If a run was interrupted" as it applies to step 2, and step 4 once
the lead says the pilot is over. It holds for ONE commit: the commit that carries this section and the GO notice
at the top of the runbook; the coordinator's message gives its 40-character hash, the lead checks it out, and
step 0 compares it. It replaces the GO of round 4's first pass (`8bbab3324ae510990f17be400602e97d4042ef6e`) and
the round-3 GO (`08bd5a669867623a476e7446a74612be47001b3b`): steps 0 to 2 are started from this commit only. A
smoke test that already passed at `8bbab3324` stays a result; it does not count for a later pin, whose step 0
stops on what another commit's steps 1 and 2 left. This verdict replaced the first line of this file together
with the fixer's note above it, added this section, and replaced the notice between `HOLD-BEGIN` and `HOLD-END`
of the runbook (GO for steps 0 to 2; NO-GO for step 3 in words; one paragraph for the lead); it changed nothing
else and no command. Neither file is listed in `PIN.sha256` (run: 0 matches). The new notice is 21 lines longer
than the hold it replaced: runbook lines cited below are those of `ebf1e993c`; in the commit that holds this
section every line after the notice lies 21 lines lower.

Why the two answers differ. Steps 0 to 2: the code audit found no new host hazard and nothing that weakens a
guard; the commands are byte for byte the rehearsed ones; the scripted parts of the new code ran through vf-eval
in the cloud container (the fixer's `check_step3` caps, route and flood parts, and the reference stage of the
rehearsal job `qwen-ring-003`, which is `tools/prove.py` with six scripted policies and 64 item boxes); and
neither open major is reachable without a model (K9 needs a box that reads the harness's secret and posts to the
interception server; in steps 0 to 2 every box runs our own scripted agents). Step 3: the brief's rule is that no
item of major severity may be open in any audit, and two are. The runbook audit's GO for steps 0 to 3 (on three
text conditions) is outweighed by K9 and X13.

Judged: the code of the third round-4 pin, `841b4a1e1d12afc7cd60b8b184b451d278895b1d` (sha256 of `PIN.sha256`
`898089fc…108f`, equal to the runbook's pin block; 136 of 136 files match at the branch head: run). After
`841b4a1e1` the three folders the pilot uses changed in `results/`, `rehearsal/`, `README.md`, the runbook's prose
(three places, no command), the fixer's note in this file and nothing pinned; after the audited head `ebf1e993c`
only `round6/foundrylong/` and a request of that study under `gpu/requests/` changed (run: `git diff --stat`,
`--name-only`). Commands: 41 fenced and 2 inline; byte for byte those of the first pass's GO commit `8bbab3324`
except the go command of 3.0 (its placeholders now in single quotes), and equal at the pin and at the head (run: my
script). Those of steps 0 to 2 were rehearsed as `sh -c` lines at `d9694f3e5` (round 4); step 0 and the uv
commands of step 1 again from a fresh clone of `841b4a1e1` (`results/rehearsal_round4.json`, `second_pass`).
Inputs: the second-pass fixer's report and three audits of `841b4a1e1`/`ebf1e993c`: code (steps 0 to 2 GO, step 3
NO-GO on K9), runbook (GO for steps 0 to 3 if three texts are added), exam integrity (one major for rollouts, one
for reading scores). What I rely on I checked at the head myself; where a row rests on somebody else's run it
says whose.

| evidence label | meaning in this round |
|---|---|
| read | the cited lines were read by me (verifiers: the pinned checkout `verifiers/v1`, written `vf:`) |
| run | run by me: scripts over texts and records, `sha256sum -c`, `git`, `grep`, and one key scan (a Python process that read the values from its environment and printed file names and counts only); no file of the port was executed |
| tripwire, container, vf-eval (fixer, auditors) | their runs, recorded in `results/` or in their reports; none by me |
| inferred | reasoned, not run: every statement about macOS and Docker Desktop |

### What changed since 08bd5a66

| area | change | pass | where (pinned unless said) | checked by me |
|---|---|---|---|---|
| the laboratory | a 256-bit bearer per rollout, in vf-eval's memory only; `401` before the application without it; DNS-rebinding protection on; the box's proxy adds it to laboratory requests | first | `bearer.py`, `lab_tools.py`, `runtime.py`, `access.py` | read (round 4) |
| what a box can make the Mac hold (K4) | vf-eval keeps at most 96 MiB of standard output and 4 MiB of standard error of any `docker` client, drops the rest and fails the command; the in-box check's report is cut at 1 MiB in the box; the laboratory reads a body itself, at most 4 MiB (`413`), at most 8 requests at once (`503`); the box's proxy serves at most 64 connections and pauses its relay beyond 2 x 128 KiB. Not bounded: verifiers' interception server (K9) | second | `runtime.py` (`OUTPUT_MAX`, `read_bounded`, `_communicate`, `MAX_CONNECTIONS`), `bearer.py`, `access.py` | read (`runtime.py:75-100, 178-210`; `bearer.py:54-60, 101-133`) |
| the boxes | 2 CPUs, at most 4 GB without swap, 512 processes, read-only root, memory-backed `/workspace` 1 GiB, `/tmp` 512 MiB, `/etc/physim2`, `/runtime`; read back from the engine before use; a config can only lower memory | first | `boxcaps.py`, `runtime.py` | read (round 4) |
| the image | `physim2-ring:2`: verifiers' `bash` harness preinstalled from hashed pins, so a box downloads nothing at set-up | first | `docker/` | read (round 4) |
| the driver guard | the four memory file systems of a capped box are accepted mount points (first pass), and only with the box's own `size=` (second pass, K1) | both | `public/_item.py` | read (the second pass's diff adds a refusal and removes none) |
| the spend stop | one counted client in vf-eval; worst-case counting of missing usage, errors and streams without usage; mandatory `max_context_tokens`; the provider's cost field when higher; the lead's standing go file; one ceiling over this Mac's ledger and the shared ledger (first pass). Request keys an allow-list, every non-message key in the chained prompt bound, no call before its `sent` record is in the spend log, a failed write stops the run (second pass, K5) | both | `spend.py`, `tools/vfrun.py`, `tools/check_request.py` | read (`spend.py:119-150, 240-242`) |
| step 3 | request route `rollout-job/v1` (stages instance, reference, dry-run, rollout, close), strict config schema, publication folder with key scan and manifest | first | `tools/check_request.py`, `tools/vfrun.py`, `tools/pack_rollout.py`, `rollout_config.py`, `tools/check_config.py`, `profiles.py` | read (round 4) |
| the capture of `submission/` | the one writer of box content on the Mac: the archive held whole in memory, read once, a decision per entry, caps on files and bytes; directories counted and a broken-off file listed (second pass, K2) | both | `capture.py` | not repeated (code auditor's container run, 15 hostile archives) |
| the exam | rulings E1 to E15 (E16 not done): whatever is in `submission/` when the run ends is graded; the box starts with the null baseline; a failed item is scored as the null policy, never K; the statement renders every limit of the run; the Lab log in `/workspace`; `ring_r4` (256 samples per item, an episode start costs 17 ticks). Second pass: X1 (what is graded after an error), X5 (the card and the statement carry the measured envelope and per-item limits), X6 (`lab.validate` from the manifest's files, scratch places closed), X9 (an item's reply capped at 1 MiB) | both | `taskset.py`, `grading.py`, `access.py`, `bundle.py`, `TASK.md.tmpl`, `public/`, `agents/keep_baseline.py`, `physim2_verifier/` | read in part (X13, X15, X16 below; the rest by the exam auditor) |
| the session's environment | refused names include `PYTHONEXECUTABLE`, `__PYVENV_LAUNCHER__`, `DYLD_*`; nine names pass to a child, not `SSL_CERT_FILE` | first | `tools/vfrun.py:82-84` | read |
| the runbook | 43 commands (round 3: 35), each with the folder guard; no `$(...)`, no backtick, no variable but `$HOME` and `$?`; destructive targets as in round 3; second pass: the go command's quotes, step-3 text T2 to T14, "step 0 again at the same commit" | both | `RUNBOOK_MAC.md` (not pinned) | run (script) |
| the pin | 109 files, then 135, now 136 (`agents/probe_flood.py` added) | both | `PIN.sha256` | run |

A search of the second pass's diff (`c7db465d5..841b4a1e1`, `physim2_env/` and `tools/vfrun.py`) for calls that
kill, delete, move or change modes found five lines: `runtime.py:202`, `os.killpg` of the session of a `docker`
client the same function started with `start_new_session` (verifiers' `vf:runtimes/container.py` does the same);
two `os.chmod` and one `shutil.copyfile` in `public/validate.py`, which runs in the box only, behind its gate; and
a docstring (run: the search; read: each line). The code auditor searched the same diff for 15 primitives and
read the gate of `agents/probe_flood.py` (30-43).

### The code audit, second pass (K1 to K10)

| item | severity | status | evidence (mine unless said) |
|---|---|---|---|
| K1 driver guard and tmpfs sizes | minor, Linux hosts | closed | read: `_item.py:93-99, 138-141, 172-179`; the size comes from the mount's own options; a refusal added. Fixer: `check_driver` 33 of 33 (containers) |
| K2 capture | minor | closed | code auditor's container run (15 hostile archives: links, devices, FIFOs, traversal, 30,000 entries, a 10 GiB PAX size, a cut archive): every file written regular, inside the destination, within the caps; not repeated |
| K3 the bearer | none | closed | unchanged since `c7db465d5` apart from the body and request caps (auditor: `git diff`) |
| K4 four ways out of a box | major (first pass) | closed for those four | read (table above); vf-eval (fixer, `check_step3` flood 14 of 14): a box pushed about 0.9 GB, vf-eval 517 to 616 MiB, the laboratory 427 MiB |
| K5 request keys | minor | closed, with K10 | read `spend.py:119-150, 240-242`; tripwire (fixer, E13 to E15); the paid job's 24 requests passed the allow-list (record) |
| K6 strict config schema | none | closed | unchanged (auditor: `git diff`) |
| K7 the model key | none; one minor | key closed; the base64 needle of `tools/pack_rollout.py:79` has one alignment: open, minor | run: 0 hits for the values of `PRIME_API_KEY`, `HF_TOKEN`, `WANDB_API_KEY` (plain, base64 and URL-safe base64 at three alignments) in 296 files of `round6/rollouts` and `round6/vfport` at the head, `qwen_ring_003` included |
| K8 the pin | none | closed | run: 136 of 136; every file of `vfport` that runs on the Mac is listed (auditor; the unlisted `round5/agentenv` files are imported by nothing in the pilot) |
| **K9 verifiers' interception server takes 1 GiB per request** | **major, step 3** | **open: blocks step 3** | read: `vf:interception/server.py:78` (`MAX_REQUEST_BODY = 1024**3`), `424` (`client_max_size`), `586-591` (the secret is looked up, then the whole body is read); `vf:harnesses/utils/launch.py:54` (`--api-key={secret}` on the chat program's command line in the box, where root can read `/proc/<pid>/cmdline`); `runtime.py:84` (64 connections per box) and the relay, which paces but does not cap a body; no override anywhere in `physim2_env/` and no flood case aimed at this route in `agents/probe_flood.py` (run: `grep`). So a box can make vf-eval hold about 64 GiB, and runbook line 195 ("some hundreds of MiB at most, whatever it sends") is false. Code auditor, under tripwires: an aiohttp 3.14.5 app with the same limit and order grew by 1,151 MiB for two concurrent 384 MiB posts. Not reachable in steps 0 to 2 |
| K10 `reasoning_effort` any word; `n=True` passes | minor, step 3 | open | read `spend.py:142-149`. A box holding the secret can ask for an effort the config never set; the bound then rests on the provider counting reasoning within `max_tokens` (runbook 3.2, point 8) |

### The runbook audit, second pass (T19 to T25)

| item | severity | status |
|---|---|---|
| T2 to T12, T13 (request source), T14 (`git rev-parse` row), step 0 at the same commit | minor, step 3 | closed in text (read: runbook 155, 409-418, 802-812, 857-865, 880-883, 1076-1078, 1141-1149, 1204-1207; fixer: `check_runbook` 51 of 51) |
| runbook audit items 1, 2, 3, 11: pin, no accidental start, price bound and refusals, the rehearsal record | none | closed (auditor; the commands I compared myself: run) |
| T19 (item 4) nothing checks the pinned files before each job: `check_pin` hashes `PIN.sha256` and compares HEAD only | minor, step 3 | open (read `tools/check_request.py:149-156`): before each job, the first two commands of step 0 |
| T20 (item 5) 3b and the STOP line refer to "what the runner's protocol lets you start without asking" and give no number | minor, step 3 | open |
| T21 (item 6) `EXIT 2` means a refusal OR vf-eval's own status 2 after the bound was reserved | minor, step 3 | open (read `tools/vfrun.py:770-806`: the tool returns vf-eval's status); 3f should go on with 3g and 3h in both cases |
| T22 (item 7) the publication files, the size limits and the crash clean-up are not in the block of facts; the code allows 20 MiB and 50 MiB, the text and the runner say MB | minor, step 3 | open. This corrects the first pass's section "The Mac runner's protocol", which said they stand in that block: they stand in 3h's table and in point 8 (read) |
| T23 (item 8) the runner's published intake (a fifth cap, `notes`, optional `requester`, memory down to 0.5) differs from the pin | minor | open; each difference is refused at 3a or 3b (auditor, read) |
| T24 (item 9) `PRIME_API_KEY` set but empty: verifiers takes the key from `~/.prime/config.json` | minor, step 3 | open (auditor read `resolve_api_key`; not checked by me) |
| T25 (item 10) 3d's "points 1 to 5, 7" should add "(point 8 does not apply)" | minor, wording | open |
| item 12, macOS | | inferred by the auditor; each difference ends in a stop |

### The exam-integrity audit, second pass (X12 to X19)

| item | severity | status |
|---|---|---|
| X1, X5, X9 | minor (first pass) | closed (read in part: `bundle.py:218-262`; exam auditor and fixer: `exam_pure` 25 of 25) |
| X6 `validate` as graded | major (first pass) | closed for `/workspace`, `/tmp`, `/dev/shm` and files added to `physim2/` (exam auditor, read; fixer: `exam_units` part 6 in a container, flood F8 through vf-eval); residue X16 |
| E1, E2, E3, E5 to E7, E9 | none | sound (exam auditor). E3 recomputed by the auditor from `results/proof_ring_items.npz` (S 0.89834, D 0.19197, P0 0.84842) and qwen_ring_003's `grades.json` (-0.029243, the null row); failing on purpose gains nothing; grading changed only in the reply cap since the round-5 cross-check |
| X7 jointly chosen samples | minor residual | about 0.4% at 256 samples |
| X12 (item 1) the comment at `access.py:66` still says "scored as K" | minor, wording | open (read) |
| **X13 (item 4) one command of the `bash` tool can hold the agent for up to an hour; the statement does not say so** | **major for rollouts** | **open: blocks step 3.** read: `vf:harnesses/utils/core.py:160-166` (`subprocess.run(..., timeout=3600)`); the limits section of the statement (`bundle.py:218-262`) says the run "ends at once, in the middle of whatever is running", not that a command holds the agent until it returns; `../rollouts/qwen_ring_003/`: turn 24 at t = 165 s ran `python learn_params.py`, no later turn, stop condition `agent_timeout` at 900 s (`transcript.md`, `status.json`). That run lost 735 of its 900 s and scored the baseline; its score measures the wait, not the model. Fix: one rendered line in section 4 (a command blocks until it returns, up to the harness's limit; use `timeout` or a background job writing a progress file) |
| X14 (item 5) a failed write of `/workspace/lab_log.jsonl` is silent | minor | open |
| X15 (item 7) "write to `/workspace`, `/tmp`, `/dev/shm` and nowhere else" is false for root: `/etc/physim2` and `/runtime` are writable | minor | open (read `bundle.py:265`) |
| X16 (item 8) `SCRATCH_PLACES` leaves out `/runtime` and `/etc/physim2`; a predictor reading a file put there passes `lab.validate` as graded and fails every item | minor | open (read `public/validate.py:122`) |
| X17 (item 10) the context stop counts one token per byte added since the last reply, so a run can end before `context_tokens_left` says | minor | open; to be disclosed |
| **X18 (item 11) what a score means** | **major for reading scores, not for the Mac** | open: on qwen_ring_003's instance P0 scores 0.896 and C 0.927 (read: `RESULT.md`); the auditor finds that instance outside the program's own bars (sigma 0.033 against at least 0.15; rho 0.83 against at most 0.7) and qwen_ring_002's outside the rho bar (0.826); E16 is not done |
| X19 (item 12) qwen_ring_002 read end to end | | recommendations: X13 first, then X18 with E16, then X16 and a pointer from `python -m physim2.validate` to `lab.validate` |

### The Mac review's minor findings (identifiers only)

Statuses as the runbook audit read the text at `ebf1e993c` (no change since the first pass); spot-checked by me in
the runbook where marked (read).

| status | findings |
|---|---|
| closed | CRED-5 (read), SIG-2 (read), SIG-3, G1 (read: `tools/vfrun.py:82`), NEWC-1, RB-1 (read), RB-2 (read), RB-3/R3-4, RB-7 (read), RB-8 (read), RB-9 (read), INV-2, INV-4, INV-5 (read), INV-7 (read), INV-8 (read), INV-9 (read), DOCK-3 (read), DEL-2 (read), DEL-3/INV-6 (read), the apt and apk mirrors (read), CRED-1 (read) |
| accepted with a reason, in the text | DEL-1 (a 48-bit name collision; read), DOCK-5 (the helper image is the lead's own either way; read), R3-3 |
| closed in part | R3-7, R3-8, INV-3/R3-9, DOCK-1/RB-4/R3-1/RB-5 |
| open, minor | CRED-2 (git's and Docker Desktop's credential helpers are not named in section B; read: no mention) |
| mitigated | DOCK-4 (a box carries no extra mount; the guard is unchanged) |
| deferred | CRED-4/CMD-14 (build backend pinned by version, not hash), RB-6 (needs the Mac), CMD-5, SIG-1, R3-2, R3-5, INV-1 (the appendix gives no text); the list "not covered by anyone" |

### Rounds 1 to 4: nothing reopened

| earlier finding | status | evidence |
|---|---|---|
| A1 working directory | closed | run: 43 of 43 commands begin with the folder guard; no `$(...)`, no backtick, no variable but `$HOME` and `$?`; `uv` in two commands, both with `--project <absolute path>`, the dry run first |
| A2, N1 to N3, interruption | closed | run: the status and stop commands are byte for byte the first pass's, rehearsed in round 4 (`EXIT 130` and a reset; `EXIT 97`; a SIGKILL of tool and vf-eval cleared by points 1, 3, 5 and 8) |
| A3 box scripts | closed | the new box script `agents/probe_flood.py` stands behind the marker gate (code auditor, read: 30-43) and under `agents/*.py` on the never-list (read) |
| A4, A5 driver | closed | `_item.py`: one refusal added (K1); no `rmtree`; unlink and rmdir of listed paths only, unchanged (read: the diff) |
| S1, S2, N4 | closed | unchanged; N4 used by this verdict |
| N5 to N8 | open, minor, Linux hosts only | unchanged; K1, their sibling, is closed |
| M1 to M3, m1 to m11, D1, G1 | closed | `tools/vfrun.py` changed in one argument since `c7db465d5` (read: the diff); `ENV_PASS` and the watchdog unchanged |
| K3, K6, K8; the first pass's K4 and X6 | closed | above |

### The Mac runner's protocol: can the pin meet it?

Yes for every point but the rollout itself (runbook audit item 7; read by me): the request keys and shapes, the
strict config schema with its forbidden fields, the profile `ring` with 64 items, the scripted policies of the
reference table (`null`, `D`, `P0`, `PM`, `S`, `C`) and the stages stand in the block of facts that
`tools/check_request.py --facts` prints; the publication files are 3h's table and the crash clean-up is point 8
with stage `close` (prose, not that block: T22); `SSL_CERT_FILE` is not on the tools' allow-list; the key reaches
vf-eval by the environment only. Since the second pass the spend stop refuses, unsent, any request key outside its
allow-list (`reasoning`, `provider`, `models`, `service_tier` among them). Step 3 is not released (K9, X13), so no
request should name this commit.

### What remains before GO for steps 0 to 3

1. **K9** (major): bound what one rollout can make vf-eval hold through verifiers' interception server: a body
   limit far below 1 GiB, set before the server starts (the code auditor's proposal: 32 MiB through
   `vf:interception/server.py`'s module attribute, read at `start()`), and a limit on concurrent requests of one
   rollout before any body is read; a flood case (1 GiB, with the secret taken from the chat program's command
   line) in `agents/probe_flood.py` and `tools/check_step3.py`, a check in `tools/check_round4.py`, the row in
   section B and line 195 corrected.
2. **X13** (major for rollouts): section 4 of the statement says, rendered from the harness's limit, that a
   command holds the agent until it returns (up to 3,600 s, longer than the run), and how to avoid it.
3. A new pin with 1 and 2, a re-audit of its diff, the K9 flood case run through vf-eval, one model job from a
   request, and a verdict.
4. Runbook text of step 3: T19, T20, T21 (the runbook audit's conditions for its GO); recommended T22 to T25 and
   CRED-2.
5. Same pin, minor: K7 (three alignments), K10 (`reasoning_effort` equal to the config's, `type(n) is int`), X12,
   X14 to X17.
6. For reading scores, not gating: X18 (quote next to P0, S and C with sigma and rho; E16's two rows).

### Scores from this pin

Not quotable without conditions. X18 can make a score misleading on its own, and X13 can make a score a measure of
a blocked command rather than of prediction. A score of this pin may be quoted only with its `n_failed` and
fallback reasons; with `infrastructure_failed_items` = 0 and no `grading error`, `not_a_grade` or `not run`;
next to P0, S and C of the same instance and the instance's sigma and rho; with the run's stop condition and the
time its last command took; and not as a measure of how hard the ring is. qwen_ring_003 (-0.029, the baseline)
measures the wait of X13, not the model.

### Residual risks, also with this GO

- **Nothing has run on macOS or Docker Desktop** (inferred only, each ending in a stop rather than a repair):
  zsh and a detached command outliving its call; BSD `ps`, `awk`, `df -Pk`, `shasum`; uv's managed Python and its
  command line; that Docker Desktop applies the box caps as the Linux engine does (they are read back and a box
  without them is not used); the signs of a container and the mount table there; that a laboratory outlives a
  killed vf-eval.
- **Step 2 at this code.** 2b (`tools/check_probe.py`) and 2c have not run at `841b4a1e1` anywhere; 2a's tool ran
  there as the reference stage of `qwen-ring-003`. The guard now also needs each box tmpfs's size as the kernel
  prints it (`size=1048576k`, ...); Docker Desktop runs a Linux kernel, inferred to print the same. If it does
  not, item boxes are refused, 2a's "must hold" line fails, and that is a stop.
- **Never run in the runbook's form:** the image build of step 1 and its status command; step 4; point 4 of "If
  a run was interrupted"; the rule for a second interruption; a stop of a vf-eval by its own pid.
- **As the lead:** the tools and the laboratory run on the Mac as the lead; `uv sync` runs a build backend pinned
  by version, not hash (CRED-4); `git` and the `docker` client may start their credential helpers (CRED-2).
- **The disk:** the watchdog is a brake, not a wall; `uv sync` and the image build are checked before they start
  only.
- **Linux hosts:** N5 to N8; the cloud rehearsal's own scripts act for real on the cloud host.
- **Step 3, when a later pin releases it:** an untrusted model is root in a capped box for up to 180 minutes;
  Docker Desktop's virtual machine and verifiers' network cut are the walls (2b measures the cut on the Mac); a
  box can keep a core of the Mac busy while vf-eval reads and drops what it sends; the spend stop rests on the
  provider's usage and was seen to stop a run only against the stand-in endpoint (`results/round4_step3.json`,
  R11, R14); the ledger ceiling was seen to refuse under tripwires (D19 to D19c) and to block the next job while a
  cut job's row was open (rehearsal).

### By hand (the lead, and the Mac session before its first command)

In addition to section C of the runbook and the lists of rounds 1 to 4:

| when | check | expected |
|---|---|---|
| before | the coordinator's GO message; `git rev-parse HEAD`; the first text line of `RUNBOOK_MAC.md` on disk | a 40-character hash; equal to it; it begins `**GO for steps 0 to 2.**` and names round 4, second pass. Not `8bbab3324…`, not `08bd5a66…` |
| before | what another commit's steps 1 and 2 left: `ls "$HOME/physim2-pilot-20261110"`, `docker images physim2-ring`, `.venv` in the study folder | none. If steps 1 and 2 ran at `8bbab3324`: step 4 there on the lead's word, then the `.venv` (or a fresh checkout) and the image by hand |
| before | Docker Desktop: 4 CPUs and at least 6 GB; at least 11 GiB free on the home folder's file system | as section C says; nothing changed by the pilot |
| after 2a | the "must hold" line: every `layers` is `{'rlimits': True, 'uid': ..., 'cleanup': True}`, and `box True 64 0` | the driver guard accepted the capped boxes, tmpfs sizes included, on Docker Desktop; anything else: stop |
| after 2b | both lists of `probe.log`; `staging` with `box_limits`; `control`; `agent box net` with `proxy_loopback_names`; `item box net` | `failed_new` holds `b_lab_process_dropped_it_after_loading` only. This is the first 2b at this code anywhere: a difference is a finding to report, not something to make pass |
| step 3 | | not from this commit; no `LEAD-GO-MODEL-SPEND.json`. The next pin's verdict says what it needs (above) |

Not covered by this round: the same as section 6 and rounds 1 to 4. By me: no rollout, no container, nothing on
macOS; I did not rerun the check tools, `tools/check_step3.py` or the exam proof, nor the auditors' container and
tripwire runs (capture, the aiohttp body test, JAX in an item box). The Mac review's text was read; no detail of
the lead's machine is written here.

## Re-audit, round 5

**VERDICT, 12 Nov 2026 (round 5, first pass): GO for the scripted smoke test on the lead's Mac (steps 0, 1 and 2
of `RUNBOOK_MAC.md`) from the one commit that holds this section. NO-GO for step 3, the model rollouts driven by
request files: five findings of major severity are open, three of the class "what a box can make a process on the
Mac hold" (K11 to K13) and two of the class "what the agent is told is not what happens" (X20, X21). Each needs a
change of a pinned file, so a new pin, a re-audit of its diff, the new flood cases through vf-eval and a verdict.
Scores of this pin are not to be quoted (see "Scores from this pin").**

The GO covers steps 0, 1 and 2, the section "If a run was interrupted" as it applies to step 2, and step 4 once
the lead says the pilot is over. It holds for ONE commit: the commit that carries this section and the GO notice
at the top of the runbook; the coordinator's message gives its 40-character hash, the lead checks it out in a
fresh checkout for this round (runbook section C), and step 0 compares it. It replaces the GO of round 4, second
pass, for `0697487eb4b9d9bcf4f5753543c0786141b99094`: steps 0 to 2 are started from this commit only. A smoke test
that passed at `0697487eb` stays a result; it does not count for this pin. This verdict replaced the first line of
this file, added this section, and replaced the notice between `HOLD-BEGIN` and `HOLD-END` of the runbook (GO for
steps 0 to 2; NO-GO for step 3 in words; one paragraph for the lead); it changed nothing else and no command
(run: the diff touches no line that begins with the folder guard and no fence). Neither file is listed in
`PIN.sha256` (run: 0 matches). The notice is 23 lines longer than the hold it replaced: runbook lines cited below
are those of `ad499d1a1`; in the commit that holds this section every line after the notice lies 23 lines lower.

Why the two answers differ. Steps 0 to 2: the code audit found no new host hazard and nothing that weakens a guard
of rounds 1 to 4; the runbook audit found the pin block, the facts block, the 43 guarded commands and the four
destructive targets in order; the scripted parts of the new code ran through vf-eval in the cloud container (the
fixer's `check_step3` route and `flood5`, 40 of 40, and the reference stage of the rehearsal job `qwen-ring-004`);
and none of the five open majors is reachable without a model (K11 needs a request written in absolute form to
the interception server, K12 a validator that writes past its `head -c`, K13 a box that writes to its PID 1's
output; in steps 0 to 2 every box runs the port's own scripted agents, and I read that none of them does any of
this: `agents/probe_grading.py:116-130` sends absolute-form requests only for `/` of the loopback names, a few
bytes each). Step 3: the brief's rule is that no item of blocker or major severity may be open in any audit, and
five are. The runbook audit's GO for steps 0 to 3 is a verdict on the runbook alone and is outweighed by them.

Did this round close the two classes, as the brief asked? No. The fixer enumerated both (25 box-to-host channels,
README 8.17; 11 disclosures) and fixed what the enumeration found, and the audits again found new members of each
class: two channels the table does not list (the box's container log; the request target in absolute form, which
the new gate reads differently from verifiers' proxy) and one listed channel whose bound is on the bytes kept, not
on what parsing them costs (K12); and two endings or numbers the statement gets wrong (X20, X21). This is the third
round in a row with that pattern (K4, K9, K11 to K13; X6, X13, X20 and X21).

Judged: the code of the round-5 pin, `c48eb6dc28b31f798a8c75f3b9612c8895570278` (sha256 of `PIN.sha256`
`025a9da6e724f5f907b05497603ced013a78c531ded70affd82b0c8f1d004eed`, equal to the runbook's pin block; 136 of 136
files match at the branch head `ad499d1a1`: run, `sha256sum -c`). After the pin the commits `727622574` and
`ad499d1a1` changed `README.md` (14 lines), the runbook's prose (11 lines, no command), `rehearsal/round5_jobs/`
and `results/rehearsal_round5.json`, and nothing pinned (run: `git diff --stat c48eb6dc2 ad499d1a1`). Inputs: the
fixer's report and three audits of `c48eb6dc2`/`ad499d1a1`: code and channels (GO for steps 0 to 2, NO-GO for step
3 on three new majors), runbook as the Mac's operator (GO for steps 0 to 3 on the runbook alone, two minor wording
points), what the agent is told (NO-GO for model rollouts on two new majors). What I rely on I checked at the head
myself; where a row rests on somebody else's run it says whose.

| evidence label | meaning in this round |
|---|---|
| read | the cited lines were read by me at `ad499d1a1` (verifiers: the pinned checkout `verifiers/v1` at `a24f5e21`, written `vf:`) |
| run | run by me: `sha256sum -c`, `git`, `grep`, scripts over texts, and one key scan (a Python process that read the values from its environment and printed file names and counts only); no file of the port was executed |
| tripwire, container, vf-eval (fixer, auditors) | their runs, recorded in `results/` or in their reports; none by me |
| inferred | reasoned, not run: every statement about macOS and Docker Desktop |

### What changed since 0697487eb

| area | change | where (pinned unless said) | checked by me |
|---|---|---|---|
| verifiers' interception server (K9) | body limit 16 MiB, set through the module attribute before any server starts (the checkout is not edited) | `physim2_env/runtime.py:108, 273` | read |
| the box's proxy (K9) | a request to a host callback without a bearer (the interception server) waits, before anything of it is forwarded, until no other request of the same box goes there; what it sends there is cut after 17 MiB | `runtime.py:109-110, 361-430` (`_callback_of`, `_handle_one`), `pump` | read: holds for origin-form targets only (K11) |
| logs (K9) | a filter caps the repeated per-request log lines a box can cause, in vf-eval and in the laboratory; the laboratory's log keeps at most 20,000 lines with every text cut at 500 characters, and a failed write is counted | `runtime.py:178-230`, `lab_tools.py:40-83` | read (definitions); the counts are the fixer's `flood5` (3,000 unauthorized requests, 20 lines) |
| the task statement (X13 and the sweep) | one command holds the agent up to 3,600 s, parsed from the harness's source, and how to avoid it; the output cut; the context bound (X17); `/etc/physim2` and `/runtime` writable (X15); the laboratory's 4 MiB and 8 at once | `bundle.py:82-102, 270-300`, `TASK.md.tmpl` | read in part; rendered by the told auditor |
| `lab.validate` (X16) and others | `SCRATCH_PLACES` adds `/etc/physim2` and `/runtime`; `python -m physim2.validate` points to `lab.validate`; a failed laboratory-log write is reported (X14); docstring (X12) | `public/validate.py:125`, `public/labclient.py`, `access.py` | read (`validate.py:120-125`); the rest by the told and code auditors |
| the spend stop (K10, T24) | only the config's `reasoning_effort` is admitted, and `n` only as the integer 1; an empty key is refused | `spend.py:76, 127-149`, `tools/vfrun.py:551-553` | read |
| the key scan (K7) | base64 and URL-safe base64 at all three alignments | `tools/pack_rollout.py` | not repeated (code auditor: the arithmetic is right); my own scan uses the same needles |
| tests | `check_round4` part F (F1 to F10), `check_step3` part `flood5` with `agents/probe_flood.py --interception` (1 GiB with the secret read from the command line), `exam_pure`, `exam_units` | `tools/`, `tests/`, `agents/` | not rerun by me (fixer; the code auditor reran `check_round4`, 151 of 151, under tripwires) |
| the runbook (not pinned) | this round's names (`physim2-ring:3`, `$HOME/physim2-pilot-r5`, a fresh checkout), "at least" for Docker Desktop's resources, `command grep`, a refusal when uv takes a Python not its own, section B rows for the interception server and the logs (line 195's false "some hundreds of MiB" replaced), T19 to T25, CRED-2, the facts block's `publication` and `after_a_crash` | `RUNBOOK_MAC.md` | run: no command changed after the pin; the 43 commands, the guards and the destructive targets are the runbook auditor's script |
| the pin | 136 files; 24 entries changed, none added or removed | `PIN.sha256` | run |
| rehearsal and model job (not pinned) | every command changed beyond names issued from a fresh sparse clone of the pin; the job `qwen-ring-004` packed with its ledger rows | `results/rehearsal_round5.json`, `round6/rollouts/qwen_ring_004/`, `ledger.json`, `LEDGER.md` | read; key scan run (below) |

### The code and channel audit, round 5 (K11 to K15)

| item | severity | status | evidence |
|---|---|---|---|
| **K11 the per-box gate and the upload cut are bypassed by the form of the request target** | **major (blocker for step 3)** | open. `_callback_of` takes the raw second word of the request line and requires it to start with `/.vf-host/` (`runtime.py:361-366`, `bearer.py:176-181`); verifiers' proxy routes by `urlsplit(target).path` (`vf:runtimes/docker/egress.py:203-213`), which also accepts `POST http://h:p/.vf-host/T/...` and `//x/.vf-host/T/...`. Such a request gets no gate and no cut, while the egress still delivers it. The server's 16 MiB still holds, so the bound falls back to 64 connections x 16 MiB x the parse factor, about 25 to 37 GiB (inferred). One request per connection (`egress.py:433-434`), so keep-alive is no further way round | read (both sides); tripwire (code auditor, the pin's proxy class: 5 absolute-form and 5 `//` requests reached the upstream at once, a 40 MiB absolute-form body arrived whole, `callback_stats` unchanged). F4, F6 and `flood5` send origin form only |
| **K12 a box-written report and listing are parsed whole in vf-eval** | **major** | open. `clean_report` runs `strip()`, `splitlines()` and `json.loads` on the exec's whole output (`access.py:99-104`); the `head -c` cut in the box (`access.py:96`) is the box's own and root can write past it (`access.py:91-94` says so); vf-eval keeps up to 96 MiB (`runtime.py:104`). `capture.parse_listing` splits all lines before its `[:4000]` (`capture.py:227`) | read; measured by the code auditor (18 to 36 times the input, about 1.8 to 3.5 GiB per `lab.validate`, one at a time, as often as the agent likes; listing 19 times) |
| **K13 the box's container log has no size limit** | **major** | open. No `--log-driver` in the box's run line (`boxcaps.py:127-130`); PID 1 is `sleep infinity`; a box writing to `/proc/1/fd/1` fills the daemon's json-file log for up to the run's wall time. On the Mac that is the disk of Docker Desktop's virtual machine and its disk image on the Mac's volume, which the disk watchdog does not watch (inferred). Not among the 25 channels of README 8.17 | read (`boxcaps.py`); container (code auditor: 3 MB through `/proc/1/fd/1` became 3.0 MB of log, `LogConfig` `{"Type":"json-file","Config":{}}`) |
| K14 the parse factor is a measurement, not a bound | minor | open: README row 2 and runbook section B say about 25 times (0.4 GiB); nested JSON measured 36 times (about 0.6 to 0.7 GiB) | measured by the code auditor; not repeated |
| K15 the laboratory's memory is not stated | minor | open: 8 requests of 4 MiB at once, each parsed and waiting on the service lock, about 1.2 GiB in the laboratory (inferred); README row 11 does not say so | read (`bearer.py:59-60`) |
| the rest of the sweep (`RepeatLimit`, `BoundedLog`, the other interception routes, the tar extraction) | | sound | code auditor (read) |
| kill, delete, move and mode changes in the diff | | sound: the `SCRATCH_PLACES` chmods run in the box only and put the modes back; `exam_units` acts under `/runtime` and `/etc/physim2` behind `refuse_outside_a_container`; `flood5` stops only its own stand-in child by its `Popen` object; `issue5.py`'s `rm -rf` names the literal r5 folders (step 4's command, issued only in the rehearsal) | code auditor (read); I read `validate.py:115-125` |

### The runbook audit, round 5 (T19 to T25, CRED-2, T26, T27)

| item | severity | status | evidence |
|---|---|---|---|
| pin block, facts block | | pass: the pin block is `sha256(PIN.sha256)`; `check_request.facts_text()` equals the facts block (tripwire, runbook auditor) | run (pin block, by me) |
| folder guard, shell syntax, destructive targets | | pass: 43 commands (41 fenced, 2 inline), identical at the pin and the head, each with the guard, no `$(`, no backtick, no variable but `$HOME` and `$?`; the destructive targets are round 3's four (`kill -TERM` after the command-line comparison, `docker rm -f` after the label read back, `rm -rf` of `store` and `scratch` after the link checks, step 4's `rm -rf` and `rmdir`) | runbook auditor's script; run by me: no command line changed after the pin or in this verdict |
| rehearsal record | | pass: 27 commands changed since `0697487eb`; the 13 issued include the only two that changed beyond names (0d and step 1's dry run); the 14 others changed in names only. Not issued: the image build (tried; it failed behind the cloud's proxy, so `physim2-ring:3` there is a tag of round 4's image, no baked file changed), step 2's commands, step 4, points 3, 6 and 8 of "If a run was interrupted" | runbook auditor (script); I read `not_rehearsed` |
| T19, T20, T21, T22, T23, T24, T25, CRED-2 | | closed: T20's $50 matches `roadmap/DECISIONS.md` and is applied to `bound_usd`; T21: a refusal returns 2 before anything is reserved and the `ended` row is written in a `finally`; T24 read by me (`vfrun.py:551-553`) | runbook auditor (read) |
| T26 (wording of T19, l. 1092-1094) | minor | open: the paragraph does not say that at the same commit the first command prints exactly one line `!! research/alife/vecworld/program/round6/vfport/.venv/`; read literally, an operator stops there (safe, but it blocks a job). The auditor's replacement text is in its report | runbook auditor (read) |
| T27 (wording of 3a and CRED-2, l. 1101-1102) | minor | open: in a `--filter=blob:none` clone (which section C suggests) the second command of 3a fetches three files' contents from the host and may start the credential helper; "changes nothing / reads that commit's objects" is not exact; with an SSH remote it refuses with a misleading message (a stop) | runbook auditor (read) |
| conditions | | requests name the GO commit, not `c48eb6dc2` (`check_pin` compares HEAD); a later change to a pinned file needs new names; step 3 needs a notice that begins `**GO for steps 0 to 3.**` | runbook auditor; agreed |

### The audit of what the agent is told, round 5 (X13, X20 to X24)

| item | severity | status | evidence |
|---|---|---|---|
| X13 one command holds the agent up to 3,600 s | | closed by telling: the rendered statement gives 3,600 s parsed from `vf:harnesses/utils/core.py:166` and how to avoid it (`timeout`, a background job writing to a file). The harness has no parameter, so the hold itself remains (residual) | told auditor (rendered, read); read by me (`bundle.py:82-102`); vf-eval transcript of `qwen-ring-004`: every training command under its own `timeout`, longest wait 219 s |
| **X20 a reply that calls no tool ends the run** | **major** | open. `vf:harnesses/utils/core.py:380-381` returns on a reply without tool calls, recorded as `agent_completed`; with compaction off, a reply cut at the token limit before its tool call ends the run the same way. The statement says "`lab.submit` only ends the run early" (`TASK.md.tmpl:106`) and that a cut reply "loses the tool call it was writing" (`bundle.py:290`) | read by me (both); vf-eval transcript (told auditor): `qwen-ring-002` ended `agent_completed` at turn 143 on a text-only reply |
| **X21 `lab.usage()` reports the context without cache reads** | **major** | open. `access.py:232` adds `Usage.prompt_tokens`, which excludes cache reads (`vf:types.py`, `Usage`: "`prompt_tokens` excludes cache reads"); the statement calls the number "your last turn, as the provider counted it". The context stop itself counts the provider's raw count (`spend.py:99-106, 276`, told auditor) | read by me (`access.py:228-235`, `vf:types.py`); the trace of `qwen-ring-004` shows `context_tokens_used: 622` and `471` (run: grep), against a prompt of 11,504 tokens at turn 10 (told auditor); the job's ledger row counts 1,666,429 cache-read tokens in all |
| X22 spend wording | minor | open: the meter charges the provider's cost when higher and one worst-case call for an error or a reply without usage (`spend.py:24-28, 108-110`); the statement says only "at your model's listed prices"; `lab.usage()` reports no spend left | told auditor (read) |
| X23 per-item limits apply to each process | minor | open: `RLIMIT_CPU` and `RLIMIT_AS` are inherited per process (`_item.py:563-567`), the total `cpu_s` is recorded, not enforced; a predictor with several processes gets about 120 CPU-seconds against the 30 it is told (inferred); the memory limit is address space; the 256 MiB file-size limit is not told. Small gain on the ring | told auditor (read) |
| X24 a submission over 64 MiB at the end voids every item | minor | open: it fails the freeze rules and the last good checkpoint is not used (`_rules.py:96-97`, `taskset.py:459-463`); the statement gives 64 MiB only as a limit | told auditor (read) |
| the other limits (output cut, turns, wall time, context bound, box, laboratory, `lab.validate`, reset, grading) | | pass: the rendered text matches the code; `qwen-ring-004`: 24.3 s elapsed + 1,055.7 s left = 1,080 s | told auditor (rendered, read, transcript) |
| raising the score without better prediction | | no new route (residuals: jointly chosen sample sets about 0.4%; X23) | told auditor (read, inferred) |
| X18 what a score means (round 4) | major for reading scores, not for the Mac | open: `qwen-ring-004`'s instance has sigma 0.109 and rho 0.924, outside the program's bars | told auditor; fixer's report |

### Round 4's "remaining" list

| item | status |
|---|---|
| K9 | not closed: bounded for origin-form targets (read), bypassed by absolute-form and `//` targets (K11); the flood case runs through vf-eval (`flood5`, 40 of 40, fixer) but only in origin form |
| X13 | closed by telling (above) |
| a new pin, re-audit, flood case through vf-eval, one model job from a request, a new verdict | done for `c48eb6dc2`: this section; `qwen-ring-004` ran end to end from a request (fixer; record read) |
| T19 to T21 | closed (T26 is a wording point of T19) |
| K7, K10, X12, X14 to X17, T22 to T25, CRED-2 | closed (K10 and T24 read by me; the rest by the auditors) |

### Rounds 1 to 4: nothing reopened

`_item.py`, `grading.py`, `boxcaps.py`, `store.py` and `bearer.py` are not in this round's diff (run: `git diff
--stat 0697487eb ad499d1a1`): the driver guard, the mount allow-list, the wipe and the box caps read back are as
audited. `ENV_PASS` and the disk watchdog are unchanged (code auditor, read). K4's walls (64 connections per box,
the relay pause, 96 MiB and 4 MiB kept of a client's output, the laboratory's 4 MiB and 8 at once) still apply to
every request, absolute form included: `_handle` counts connections before reading a head, and every request goes
through `relay_buffer` (read: `runtime.py:372-430`). Bearer injection is unchanged for origin-form targets; an
absolute-form request to the laboratory gets no bearer and is refused (code auditor, read). The spend stop is
stricter (K10). K9 was never closed, so K11 does not reopen it; it keeps it open.

### Spend, ledger and the key

The rehearsal job `qwen-ring-004` (`qwen/qwen3.6-35b-a3b`, ring, 60 turns, 18 minutes, `cap_usd` 1.0, from the
request `rehearsal/round5_jobs/qwen-ring-004.json`, never under `requests/`): bound $1.0193, counted $0.2026 by the
spend stop over 60 model calls, none refused; stopped at the turn limit after 790 s of 1,080; 0.316 of the oracle
with no failed item; the ledger's running sum after it $3.6576 (read: `LEDGER.md` row 8, `status.json`). The spend
stop has been seen to stop a run only against the stand-in endpoint (R11, R14) and the ledger ceiling to refuse
under tripwires (D19 to D19c); this round adds no new evidence of either against the provider. Key: my scan of the
321 files under `round6/rollouts/` and `round6/vfport/` at `ad499d1a1` (the key's plain value and its base64 and
URL-safe base64 forms at three alignments, three secrets present in the environment) found no file with a hit
(run).

### What remains before GO for steps 0 to 3

All in one new pin with names of its own (for example `physim2-ring:4` and `$HOME/physim2-pilot-r6`, or what the
coordinator rules); every changed command rehearsed byte for byte.

1. K11: in `_callback_of`, find the callback as `egress.py` does (`urlsplit(target).path`, method not `CONNECT`),
   or forward nothing for a target that does not begin with exactly one `/`; add absolute-form and `//` cases to
   `check_round4` F4 and F6 and to `flood5` (through vf-eval).
2. K12: refuse box text longer than `REPORT_MAX` + 64 KiB before any split in `clean_report`, and cut the listing's
   text before `splitlines` in `parse_listing`; a flood case where the validator writes past `head -c` through
   `/proc`, through vf-eval, with vf-eval's peak memory recorded.
3. K13: `--log-driver none` in `cap_run_argv`, read back in `check_host_config` (verifiers never calls `docker
   logs`: code auditor, read); a case in `check_step3` that writes to `/proc/1/fd/1` and shows no log grows; a row
   in README 8.17 and runbook section B.
4. X20: the statement says that a reply without a tool call ends the run at once, and so does a reply cut at the
   token limit before its tool call; correct `TASK.md.tmpl:106` and `bundle.py:290`; a check that parses
   `vf:harnesses/utils/core.py` for this, as `harness_constants` does for the other numbers.
5. X21: `access.py:232` adds `cached_input_tokens or 0`; one check in `check_round4`.
6. Told limits equal to the actual (the brief's rule; minor, one sentence each): X22 (what the meter charges;
   optionally `usd_left` in `lab.usage()`), X23 ("per process", the 256 MiB file limit; or fail an item whose
   `cpu_s` exceeds the limit), X24 (what a submission over 64 MiB at the end does).
7. Text for the lead (not pinned unless README): K14 (about 40 times, about 0.7 GiB per request, README row 2 and
   runbook section B), K15 (the laboratory's about 1.2 GiB, README row 11 and section B), T26 and T27 (the runbook
   auditor's replacement texts).
8. Re-audit of the new diff (both classes, with the absolute-form, report and log cases), and one model job from a
   request at the new pin (the proxy's routing and the box's run line change; a short job like `qwen-ring-004`,
   about $0.20, shows an ordinary run passes) or a reasoned waiver by the next verdict; then a verdict.

For the coordinator, not a condition: enumerating channels and disclosures has not converged in three rounds. One
wall per class would end the pattern: for the first, a memory watchdog in vf-eval like the disk watchdog (stop the
rollout above a resident size); for the second, a check that parses every place where verifiers' harness and
rollout end a run and requires the statement to name each. Both are small; whether they fit "no new features" is
the lead's call.

### Scores from this pin

Not to be quoted. Two majors of the told class (X20, X21) change how a run can end and what the agent knows about
its context, so a score of this pin does not measure what it is meant to, and `qwen-ring-004`'s instance is outside
the program's bars (X18). Its 0.316 is a rehearsal record, not a result. For a later pin that closes X20 and X21, a
score may be quoted only with: the number of failed items and why each fell back; zero infrastructure failures; P0,
S and C of the same instance with its sigma and rho inside the program's bars; the stop condition (a run that ended
by `agent_completed` before the agent said it was done, or by the context stop, flagged as such); never as a
measure of how hard the ring is.

### Residual risks, also with this GO

- Nothing has run on macOS or Docker Desktop at this pin; all of it is inferred, and each known failure there ends
  in a stop: zsh and BSD tools, uv's managed Python (the guard line), Docker Desktop applying the box caps (read
  back; a box without them is not used), the tmpfs sizes the driver guard expects (`size=1048576k`), a laboratory
  outliving a killed vf-eval.
- Not rehearsed in the runbook's form at this pin: the image build of step 1 (tried; it failed behind the cloud's
  proxy; on the Mac it builds `physim2-ring:3` from the same files as round 4's image), step 2's commands, step 4,
  points 3, 6 and 8 of "If a run was interrupted", the second-interruption rule, stopping a vf-eval by its own pid.
  They differ from round 4's in names only (runbook auditor, script).
- Step 2b has not run at this code anywhere; its two lists decide a stop.
- K13 also applies to steps 0 to 2 in principle, but only the port's own scripted agents run there; their logs are
  small (inferred from the agents' code).
- As the lead: the tools and the laboratory run as the lead's user; uv's build backend is pinned by version, not by
  hash (CRED-4); git and the docker client may start their credential helpers (CRED-2; T27).
- Disk: the watchdog is a brake on the home volume, not a wall, and does not see Docker Desktop's disk image.
- File descriptors: two per proxied connection; the macOS soft limit is inferred; running out fails the run.
- Step 3, once a later pin releases it: an untrusted model is root in a capped box for up to 180 minutes; X13's hold
  remains for an agent that ignores the text; the spend stop has been seen to stop a run only against the stand-in.

### By hand (the lead, and the Mac session before its first command)

- Before step 0: a fresh checkout at a path named for the round (section C); `git rev-parse HEAD` equals the hash
  of the coordinator's GO message; the third line of the runbook begins `**GO for steps 0 to 2.**` and names round
  5, first pass; step 0's pin line prints `025a9da6e724f5f907b05497603ced013a78c531ded70affd82b0c8f1d004eed` and
  `PIN-OK`, and `shasum -c` passes for 136 files.
- Docker Desktop: at least 4 CPUs and at least 6 GB; at least 11 GiB free on the Mac (section C). No container of
  anything else running during step 2. Report `docker info --format '{{.LoggingDriver}}'` (read only; it tells the
  next round what K13's fix replaces).
- Leftovers of round 4 (`physim2-ring:2`, `$HOME/physim2-pilot-20261110`) are listed by step 0 as harmless and stay
  until the lead removes them.
- Step 1: the guard line shows `Using CPython 3.12.<n>` with nothing after the number; after step 1, grep the
  installed `mcp` for `MCP_`-prefixed environment reads (coordinator's ruling).
- After 2a: every `layers` entry is `{'rlimits': True, 'uid': n, 'cleanup': True}` and the line reads `box True 64
  0`. After 2b: `failed_new` holds only `b_lab_process_dropped_it_after_loading`. Report `box_limits`, `control`,
  the agent box's net with `proxy_loopback_names`, and the item box's net (the first 2b at this code anywhere).
- No command of section 3, 3.0 included, and no `LEAD-GO-MODEL-SPEND.json` from this commit.

Not covered by this pass: by me, no rollout, no container, nothing on macOS; I did not rerun the check tools,
`check_step3` or the auditors' tripwire and container runs; K11 to K13, X20 and X21 I confirmed by reading the
cited lines on both sides, not by running them. No detail of the lead's machine is written here.

## Re-audit, round 5, second pass

**VERDICT, 12 Nov 2026 (round 5, second pass): GO for steps 0 to 3 of `RUNBOOK_MAC.md` from the one commit that
holds this section: steps 0, 1 and 2 (the scripted smoke test) and then step 3, the model rollouts driven by request
files, once steps 0 to 2 have passed on the lead's Mac at this commit and the lead has read their report. No
finding of blocker or major severity is open in any of the three audits, nothing closed in rounds 1 to 4 is
reopened, and each condition of the brief holds (table below). One new finding of the class "what a box can make a
process on the Mac hold" (K16) and the new findings of the class "what the agent is told" are minor and stay open
for the next pin; the operator's memory figure that K16 makes wrong, and two runbook wording points that bear on
the key and on reading the logs, are corrected in the notice. Scores of this pin may be quoted, only on the
conditions in "Scores from this pin".**

The GO covers steps 0, 1 and 2, step 3 for as many requests as the lead writes, the section "If a run was
interrupted", and step 4 once the lead says the pilot is over. It holds for ONE commit: the commit that carries this
section and the GO notice at the top of the runbook; the coordinator's message gives its 40-character hash, the
lead checks it out in a fresh checkout for this round (`~/physim-r6` or similar, runbook section C), and step 0
compares it. Requests name this commit as `source_commit`, not the pin `19b6beb83`: `check_pin` compares `HEAD`
(`tools/check_request.py:154-160`; runbook auditor, read), so a request naming the pin is refused at 3b. Steps 0 to
2 run again on the Mac at this commit before any step 3: this pin's names are new (`physim2-ring:4`,
`$HOME/physim2-pilot-r6`), and step 2b has not run at this code anywhere. It replaces the GO for steps 0 to 2 of
round 5, first pass, for `5be2466e307ccc4785278af43279b63a06c3ac9f`. This verdict replaced the first line of this
file, added this section, and replaced the notice between `HOLD-BEGIN` and `HOLD-END` of the runbook (GO for steps
0 to 3; three corrections of wording; one paragraph for the lead); it changed nothing else and no command (run: the
diff of the runbook holds no fence and no line with the folder guard). Neither file is listed in `PIN.sha256` (run:
0 matches). The notice is 26 lines longer than the hold it replaced: runbook lines cited below are those of
`73cafdc30`; in the commit that holds this section every line after the notice lies 26 lines lower.

Did this round close the two classes, as the brief asked? At the severity the brief's rule counts, yes, for the
first time in four rounds: the second-pass audits found no new major of either class. Every way out of a box into
a process on the Mac now has a wall that was run against a flood (table below), and the one new member, K16, is the
cost of handling bytes that already pass a wall (a multiplier on the 96 MiB a `docker` client may carry), a few
GiB in total, not a channel without a bound. On the told side, every number the statement gives equals the code
(told auditor, rendered and read), and the three new points are behaviours it does not mention that cost a
plausible run little. New findings have not stopped; they have dropped from major to minor. The coordinator's
round-5 suggestion of one wall per class (a memory watchdog in vf-eval; a check that parses every place where
verifiers ends a run) is still the way to end the pattern; it is not a condition.

Judged: the code of the round-5 second-pass pin, `19b6beb836874f9f938c51367849e2442bd6af4e` (sha256 of
`PIN.sha256` `41da66d69750ce7829112f30c4c22417b0e19df38c34448818dbfac4670f78c8`, equal to the runbook's pin block;
136 of 136 files match at the branch head `73cafdc30`: run, `sha256sum -c`). After the pin the commits `664d68c6c`,
`acc568056` and `73cafdc30` changed `README.md`, the runbook's prose, `rehearsal/round5_jobs/`,
`results/rehearsal_round5.json` and `round6/rollouts/` (the job and its ledger rows), and no pinned file (run: `git
diff --name-only 19b6beb83 73cafdc30` against the pin list). Inputs: the fixer's report and three audits of
`19b6beb83`/`73cafdc30`: code and channels (port5code2: GO for steps 0 to 3 on the code, one new minor), runbook as
the Mac's operator (port5book2: GO for steps 0 to 3 on the runbook, four minor wording points), what the agent is
told (port5told2: GO for model rollouts, three new minors; scores only on conditions). What I rely on I checked at
the head myself; where a row rests on somebody else's run it says whose.

| evidence label | meaning in this pass |
|---|---|
| read | the cited lines were read by me at `73cafdc30` (verifiers: the pinned checkout `verifiers/v1` at `a24f5e21`, written `vf:`) |
| run | run by me: `sha256sum -c`, `git`, `grep`/`awk` over texts, one `sh -c` line with `command grep` on `printf` input, and one key scan (a Python process that read the values from its environment and printed file names and counts only); no file of the port was executed |
| tripwire, container, vf-eval (fixer, auditors) | their runs, recorded in `results/` or in their reports; none by me |
| inferred | reasoned, not run: every statement about macOS and Docker Desktop |

### The brief's conditions for GO for steps 0 to 3

| condition | holds | evidence |
|---|---|---|
| no open item of blocker or major severity | yes | code audit: K11 to K13 sound, K16 minor; runbook audit: four minor wording points; told audit: three minors, and X18 "major for reading scores, not for running", which governs quoting (below), as in rounds 4 and 5 |
| nothing closed in rounds 1 to 4 reopened | yes | run: `git diff --stat 0697487eb 73cafdc30` touches none of `public/_item.py` (the driver guard), `grading.py`, `bearer.py`, `store.py`, `rollout_config.py`, `tools/tripwires.py`, `tools/check_config.py`; the diff of `tools/vfrun.py` only adds refusals (an empty key, an effort not the config's) and a name; code auditor (read): mount allow-list, `SpendConfig` `extra="forbid"`, `ENV_PASS`, the key scan's needles |
| every box-to-host channel bounded and tested | yes (K16: the total of one bounded channel is misstated, corrected in the notice) | walls and their floods: 96 MiB and 4 MiB kept per `docker` client (round 4, second pass, vf-eval); the interception server's 16 MiB body, one request of a box at a time and the 17 MiB cut, now in origin, absolute and `//` form (tripwire F4b, F6; vf-eval G10: 8 + 8 requests of 15 MiB, at most 1 at the server); the report refused past 1 MiB + 64 KiB and the listing cut before splitting (tripwire F11, F12; vf-eval G11: 90 MiB of short lines refused, vf-eval peak 936 MiB for the whole rollout); `--log-driver none` read back (tripwire A3, A14; vf-eval G12: 66 boxes, no log path, `docker logs` refused); the laboratory's 4 MiB and 8 at once (round 4); the log filters (vf-eval G6). Read by me: `runtime.py:365-383` against `vf:runtimes/docker/egress.py:194-213` (same h11 parse, method, `urlsplit` path, token partition; one request per connection, `Connection: close` upstream), `access.py:99-108, 281`, `capture.py:218, 227-232`, `boxcaps.py:134, 151-152` |
| every told limit equal to the actual | yes for the agent; for the operator after the notice's correction | told auditor: the statement rendered at the head under tripwires is byte-equal (18,360 bytes) to the one in `qwen_ring_005/transcript.md`, and each number matches its code. Read by me: `TASK.md.tmpl:11, 102-107, 148-163`, `bundle.py:102-117, 415` (X20 parsed from `vf:harnesses/utils/core.py:380`), `access.py:240-245` (X21). The operator's figure in section B ("96 MiB + 4 MiB of one `docker` client") is low by K16; the notice gives about 3 GiB in vf-eval and 1.2 GiB in the laboratory |
| the runbook rehearsed in its final wording, or wording-only changes after it listed | yes, with the exceptions listed | run: the fenced commands are byte-identical at `19b6beb83` and `73cafdc30` (41, each with the folder guard; 2 inline, runbook auditor). Issued from a fresh sparse clone of the pin (rehearsal record, `second_pass`): 0a to 0e, 1a to 1e, 1g, 1h, "Before 2a", 3.0, 3a to 3h with one paid job, then 0a, 0b, 0d. Not issued at this pin: the image build and its status, 2a to 2c, step 4, the points of "If a run was interrupted" (names only since round 4's rehearsal; point 3's `command grep -Fx` since round 5's first pass, never issued in that form). For point 3, run by me in `sh` (dash): `command grep -Fx physim2-pilot-r6` prints the label and returns 0 on exactly that line, returns 1 on another, and bypasses a shell function named `grep`. After the rehearsal, wording only: the notice (its three corrections) and this file. Steps 2a to 2c run on the Mac before any step 3, so a failure there stops before a model acts |
| the key in no box, log or published file | yes | run: my scan of all 345 files under `round6/vfport/` and `round6/rollouts/` at `73cafdc30` (the values of `PRIME_API_KEY`, `HF_TOKEN`, `WANDB_API_KEY` from my environment; plain, base64 and URL-safe base64 at three alignments; 12 distinct needles): no file with a hit, `qwen_ring_005`'s transcript, redacted trace, lab log and submission included. vf-eval at this pin (fixer, `check_step3` part `route`, 43 of 43 with `flood5`): R17 to R19 (the laboratory's bearer on no command line or environment; no credential-like name and no 64-hex string of the run in the box). The child environment allow-list is unchanged (above) |
| the spend stop and the ledger ceiling shown to work | yes, against the stand-in endpoint; with the provider, counted but never stopping | vf-eval at this pin (fixer, part `route`): R11 (four calls pass the cap, the fifth is never sent, stop condition `spend_cap`), R13 (counted cost within cap + one call; the ledger's reservation and closing rows), R14 (graded after the stop). Tripwires, round 4: D19 to D19c (the ceiling, one total over a shared ledger); `check_ceiling` is unchanged since (run: the diff of `check_request.py` adds only the publication facts). Rehearsal 3b at this pin passed against the ledger; `qwen-ring-005` counted $0.0978 of a $0.5193 bound over 40 calls, none refused (read: `RESULT.md`, `usage.json`). The provider's bill was not read |
| one model job from a request, end to end | yes | `qwen-ring-005`, from the request `rehearsal/round5_jobs/qwen-ring-005.json` (never under `requests/`), through 3a to 3h from a fresh clone of the pin: instance, reference, dry run, rollout, grading of 64 items, pack, ledger row 9 (read: the rehearsal record, `RESULT.md`, `LEDGER.md`) |
| every file that runs on the Mac inside the pin | yes | run: 136 of 136 files match; every `.py`, `.toml`, lock and Dockerfile path that a runbook command names is in `PIN.sha256` (the other names in the text are verifiers' files cited as evidence, placeholders, an example config inside the request schema, and the rehearsal's own helper `rehearsal/fetch4.py`, which the Mac does not run); the tracked files of the study folder outside the pin are `tests/`, `redteam/` and `PROGRESS.md`, which no runbook command runs; no pinned file changed after `19b6beb83` |

### What changed since 0697487eb

| area | change | where (pinned unless said) | checked by me |
|---|---|---|---|
| verifiers' interception server (K9, round 5 first pass) | body limit 16 MiB through the module attribute before any server starts; one request of a box at a time reaches it; a body is cut after 17 MiB | `physim2_env/runtime.py:108-110, 273, 400-445` | read (round 5, first pass, and again) |
| the route of a request (K11, second pass) | the box's proxy finds the callback exactly as verifiers' proxy routes it (h11, not `CONNECT`, the path of `urlsplit(target)`), so absolute-form and `//` targets meet the same gate and cut; a count of each form | `runtime.py:356, 365-383, 424-426` | read, against `vf:egress.py:194-213` |
| box text parsed in vf-eval (K12, second pass) | the validator's report is refused past `REPORT_MAX` + 64 KiB before any strip, split or parse; the listing is cut to 400,000 bytes before splitting; the fingerprint is cut before stripping | `access.py:99-108, 281`, `capture.py:218, 227-232` | read |
| the box's container log (K13, second pass) | `--log-driver none` on every box, read back after start; a box without it is refused | `boxcaps.py:131-134, 151-152` | read |
| logs (round 5, first pass) | `RepeatLimit` on the interception server's logger and the last-resort handler; the laboratory's `BoundedLog` | `runtime.py`, `lab_tools.py` | read in round 5, first pass |
| the spend stop (K10, T24) | only the config's `reasoning_effort`, and `n` only as the integer 1; an empty key refused | `spend.py`, `tools/vfrun.py` | read (diff) |
| `lab.usage()` (X21) | the context count adds the provider's cache reads | `access.py:240-245` | read; `qwen-ring-005`: 11,918, 12,669, 13,410, 16,671 |
| the task statement (X13, X15 to X17; X20, X22 to X24) | the 3,600 s hold of one command and how to avoid it; a reply without a tool call ends the run, and so does one cut at the token limit before its tool call (parsed from verifiers, refused if absent); what the meter charges; per-process item limits and the 256 MiB file limit; a submission over 64 MiB at the end gives every item the baseline | `TASK.md.tmpl`, `bundle.py:102-117, 310-342, 415` | read in part; rendered by the told auditor |
| names (process) | `physim2-ring:4` (a tag of the same image; no baked file changed), `$HOME/physim2-pilot-r6`, a fresh checkout such as `~/physim-r6`; step 0 lists earlier pins' leftovers as harmless | configs, tools, runbook | runbook auditor (run) |
| runbook (not pinned) | section B rows for the interception server, the logs and the container log; K14's factor about 40 and K15's 1.2 GiB; T19 to T27, CRED-2; this round's names | `RUNBOOK_MAC.md` | run: fenced commands identical at pin and head |
| tests | `check_round4` 155 (A3, A14, F4b, F6, F11 to F13 new), `exam_pure` 40, `check_step3` `route` + `flood5` 43 (G10 to G12 new), `exam_units` 103, `check_round3` host 30 | `tools/`, `tests/`, `agents/probe_flood.py` | not rerun by me (fixer; the code auditor reran `check_round4`, 155 of 155, under tripwires) |
| the pin | 136 files | `PIN.sha256` | run |
| rehearsal and model jobs (not pinned) | `qwen-ring-004` (first pass) and `qwen-ring-005` (second pass) from requests, from fresh clones; ledger rows 8 and 9, running sum $3.7554 | `results/rehearsal_round5.json`, `round6/rollouts/` | read; key scan run |

### The code and channel audit, round 5, second pass (port5code2)

| item | severity | status | evidence |
|---|---|---|---|
| 1. K11, request targets in absolute form or starting with `//` | | closed | read (both sides, above); tripwire F4b, F6 (auditor's rerun); vf-eval G10 (fixer) |
| 2. K12, box text parsed whole | | closed for parsing | read; tripwire F11, F12 (auditor's rerun); vf-eval G11. The other parses of box text run in grading boxes, where the predictor is another uid (auditor, read) |
| 3. K13, the box's container log | | closed | read; throwaway container (auditor): with `--read-only`, `/etc/hosts`, `/etc/resolv.conf`, `/etc/hostname` are mounted read-only; vf-eval G12 |
| 4. K9, body limit and gate | | closed | read: `server.py:424` takes the 16 MiB; the port registers no request stops, so the path that keeps a refused prompt in the trace (`vf:interception/server.py:729-738`) is never taken (auditor, read) |
| 5. the laboratory | | sound | `stateless_http`, `json_response`; 4 MiB and 8 at once, about 1.2 GiB (inferred; K15) |
| 6. capture of `submission/` and the workspace | | sound | tripwire (auditor): 96 MiB of header-only entries cost `capture.extract` 97 MiB |
| 7. logs | | sound | read (auditor) |
| 8. rounds 1 to 4 | | nothing reopened | above; the pin verified (auditor and me) |
| 9. **K16, each `docker` client's output becomes text of up to 4 times its size** | minor | open, next pin. Read by me: `vf:runtimes/container.py:71-74` decodes stdout and stderr with `errors="replace"`; the port's `_communicate` (`runtime.py:281-313`) keeps at most 96 MiB and 4 MiB and returns bytes, and verifiers' `cli` then decodes them, so one astral character in 96 MiB of ASCII gives a 384 MiB string; `vf:harness.py:181` strips it once more when the harness's command exits non-zero. Three clients can carry box-written output at once: the harness's command, a checkpoint (`access.py:274-281`, under `_lock`) and the in-box check (`access.py:380`, not under `_lock`; one at a time, since the laboratory serves `check` under `LabService.lock`, `round5/agentenv/evaluator/lab_service.py:60, 200`, read). Measured (auditor, tripwires): one client +963 MiB peak. Inferred: about 2.5 to 3 GiB in vf-eval with one interception request, about 4 GiB with the laboratory, against about 0.8 GiB told in runbook section B and README row 13 | the notice corrects the figure for the operator. Fix for the next pin: wrap `C.cli` in `install()` so a decoded client keeps at most a few MiB, or correct section B and README |
| 10. kills, deletes and mode changes in the diff | | sound | `rehearsal/issue5.py`, `issue6.py` behind the cloud-only guard with the literal `rm -rf`; `tests/exam_units.py` refuses outside a container; `check_step3` stops only its own stand-in child (auditor, read) |
| 11. residuals | minor | not new | `/v1/models` is passed to Prime with the lead's key at the box's rate, unmetered, one at a time (`vf:interception/server.py:935-968`); connection churn through Docker Desktop's network process; macOS's 256-descriptor soft limit (README row 24) |

### The runbook audit, round 5, second pass (port5book2)

| item | severity | status | evidence |
|---|---|---|---|
| 1. pin block | | pass | run (me too): line 17 = sha256 of `PIN.sha256`; 136 files; nothing pinned changed after `19b6beb83` |
| 2. facts block | | pass | lines 982-1018 equal `check_request.facts_text()` byte for byte (4,425 bytes; tripwires, 65 installed, 0 hits) |
| 3. command shape | | pass | 43 commands (41 fenced, 2 inline), identical at pin and head (run, me too), each with the folder guard, no `$(`, no backtick, no variable but `$HOME` and `$?` |
| 4. destructive targets | | pass | round 3's four (`kill -TERM` line 777, `docker rm -f` 801, `rm -rf` of `store` and `scratch` 823, step 4's 1290) |
| 5. rehearsal coverage | minor | open in the record's wording; covered here | point 3's `command grep -Fx` was issued in neither pass while line 1379 says "names only"; fails safe (no match, nothing removed); run by me in `sh` (above). The auditor's replacement for lines 1378-1379 goes into the next text |
| 6. T19 to T21 | | closed | lines 1094-1099; $50 at 1139-1141 and 1189 (= `DECISIONS.md:152`); 1205-1208 |
| 7. T22 to T25, CRED-2 | | closed | read (auditor) |
| 8. T26 | | closed in the text | the single `.venv` line seen after steps 1 and 3; after 2b and 2c inferred, and an extra line is a stop (residual) |
| 9. T27 | | closed | lines 1105-1111, 217-218, 380; `git_show` passes only `PATH` and `HOME`, 20 s per file |
| 10. status headers in 3d and 3f | minor | corrected in the notice | `cut -c 1-12` cuts both headers to `==> /Users/x`; the notice says the order (`reference.log`, then `rollout.log`) |
| 11. 3h's key scan without the key | minor | corrected in the notice | `pack_rollout.py:71-77, 497-503` (read by me): the needles come from its own environment, the record lists them (`credentials_from_the_environment`), and the line printed says only `clean`; the notice: 3h only in a session started with the key, else stop; the lead checks the needle list before anything is handed on |
| 12. stale "this pin" (lines 39-40, 1334-1335, 1349) | wording | open, next text | the auditor's replacements are in its report; they change no instruction |
| 13. the text read literally on macOS (zsh, BSD tools) | | pass, inferred | only `test`, `printf`, `tail`, `cut`, `ps -o`, `df -Pk`, `shasum`, `awk`; `command grep` bypasses a session's function or alias |
| 14. spend | | pass | 3b and the STOP line check bound = cap + one worst-case call, at most $50; the ceiling counts the shared ledger ($3.7554 of the cloud rehearsals) |
| conditions | | agreed | requests name the GO commit; steps 0 to 2 again on the Mac at it; the image build as written and 2b have not run at this pin anywhere, and a failure there is a stop |

### The audit of what the agent is told, round 5, second pass (port5told2)

| item | severity | status | evidence |
|---|---|---|---|
| 1 to 8. turns (40), wall clock (15 min), one reply (8,192 tokens; no tool call ends the run), one command (3,600 s; 20,000 bytes), context stop (100,000 + 16 per message + 64), spend ($0.5), what is graded at each ending, box and item limits | | pass | rendered at the head under tripwires, byte-equal to `qwen_ring_005`'s statement; each against its code (auditor, read). X20 and X21 read by me (above) |
| 9. `lab_call` replies longer than 20,000 bytes are cut, and the tool writes no `lab_log.jsonl` | minor | open, next pin | both told, in separate places; about 150 ticks fill 20,000 bytes (inferred). One sentence in section 3 (use `physim2.Lab` for long replies) |
| 10. a `lab_call` that meets HTTP 503 six times ends the run as an error | minor | open, next pin | `vf:mcp.py:11, 66-69`, not caught in `core.py:392` (auditor, read); needs 8 laboratory calls held open about 15 s, implausible with 400 ticks of budget. One clause in section 3 |
| 11. `lab.validate` and `lab.submit` can hold the agent about 300 s | minor | open, next pin | `access.py:191` (3 x 60 + 120 s; read by me); the statement says the check runs the predictor on the public examples under the item limits (`TASK.md.tmpl:150-151`), not how long it can take. One clause in section 6 |
| 12. raising the score without better prediction | | no new route | auditor (read, inferred) |
| 13. jointly chosen sample sets; per-process CPU limit | minor | residual | about 0.011 skill on job 005's instance (inferred), more than its S-C gap (0.003) |
| 14. quoting scores (X18) | major for reading scores, not for running | conditions below | jobs 004 (sigma 0.109, rho 0.924) and 005 (0.035, 0.896) are outside the program's bars |

### Round 5 first pass's "remaining" list

| item | status |
|---|---|
| K11 | closed (above) |
| K12 | closed (above) |
| K13 | closed (above) |
| X20 | closed: the statement says it in rule 2 and section 4, rendered from the parsed loop; `qwen-ring-005` ended at the turn limit, no reply ended it without a tool call |
| X21 | closed: read; the four readings of job 005 include the cache reads |
| X22, X23, X24 | closed by telling (told auditor, rendered) |
| K14, K15 | closed in the text (about 40 times, 0.7 GiB per request; about 1.2 GiB in the laboratory); K16 shows that section B's sum is still low, corrected in the notice |
| T26, T27 | closed in the text (runbook auditor) |
| a new pin with names of its own, a re-audit of its diff, the floods through vf-eval, one model job from a request, a verdict | done: `19b6beb83`; three audits; G10 to G12; `qwen-ring-005`; this section |

### Spend, ledger and the key

The rehearsal job `qwen-ring-005` (`qwen/qwen3.6-35b-a3b`, ring, 40 turns, 15 minutes, `cap_usd` 0.5, from the
request `rehearsal/round5_jobs/qwen-ring-005.json`): bound $0.5193, counted $0.0978 over 40 model calls, none
refused; stopped at the turn limit after 367 s of 900; all 64 items fell back to the null policy's forecast,
because the agent's own predictor raised on the first public example (a `jax.vmap` `ValueError`) and the agent
never called `lab.validate`; skill 0.006, no infrastructure failure; the box's log driver `none`, read by hand
(read: `RESULT.md`, the rehearsal record). The ledger's running sum after it is $3.7554 (read: `LEDGER.md` row 9).
The key: my scan found no hit in 345 files (above).

### Scores from this pin

May be quoted, only with all of these beside the number:
- the number of items that fell back to the null forecast and why each did;
- zero infrastructure failures in the run;
- P0, S and C of the same instance, and the instance's sigma and rho inside the program's bars (jobs 004 and 005
  are outside, so neither score is a result; they are rehearsal records);
- the stop condition, flagged when the run ended by `agent_completed` (a reply without a tool call) or by the
  context stop;
- no ranking of two scores closer than about 0.015 skill (jointly chosen sample sets can gain about 0.011);
- never as a measure of how hard the ring is.

### Residual risks, also with this GO

- Nothing has run on macOS or Docker Desktop at this pin; all of it is inferred, and each known failure there ends
  in a stop: zsh and BSD tools, uv's managed Python (the guard line), Docker Desktop applying the box caps and the
  `none` log driver (read back; a box without them is not used), the tmpfs sizes the driver guard expects, a
  laboratory outliving a killed vf-eval. Docker Desktop's virtual machine is the wall between a box and the Mac and
  was not tested by this study.
- Not rehearsed in the runbook's form at this pin: the image build of step 1 and its status (on the Mac it builds
  `physim2-ring:4` from the same files as round 4's image), steps 2a to 2c, step 4, the points of "If a run was
  interrupted" (point 3 with `command grep`), the second-interruption rule, stopping a vf-eval by its own pid.
- Step 2b has not run at this code anywhere; its two lists decide a stop.
- Step 3: an untrusted model is root in a capped box for up to 180 minutes. What a box can make vf-eval hold is
  about 3 GiB at worst and the laboratory about 1.2 GiB (K16, inferred), for seconds; a box can keep a Mac core
  busy while vf-eval reads and drops what it sends. X13's hold remains for an agent that ignores the text. The
  spend stop has been seen to stop a run only against the stand-in endpoint; with the provider it has counted, and
  the lead's ceiling and the runner's bill are the other walls. `/v1/models` is passed to Prime with the lead's key,
  unmetered, one request at a time.
- 3h's key scan looks only for the values in its own environment (the notice's rule).
- As the lead: the tools and the laboratory run as the lead's user; uv's build backend is pinned by version, not by
  hash (CRED-4); git and the docker client may start their credential helpers (CRED-2, T27).
- Disk: the watchdog is a brake on the home volume, not a wall, and does not see Docker Desktop's disk image (a box
  can no longer write there: K13).
- File descriptors: two per proxied connection; the macOS soft limit is inferred; running out fails the run.
- The told minors 9 to 11 and K16 stay until the next pin; that pin needs names of its own.

### By hand (the lead, and the Mac session)

- Before step 0: a fresh checkout at a path named for the round (section C); `git rev-parse HEAD` equals the hash
  of the coordinator's GO message; the third line of the runbook begins `**GO for steps 0 to 3.**` and names round
  5, second pass; step 0's pin line prints `41da66d69750ce7829112f30c4c22417b0e19df38c34448818dbfac4670f78c8` and
  `PIN-OK`, and `shasum -c` passes for 136 files. Earlier pins' leftovers (`physim2-ring:2`, `physim2-ring:3`,
  `$HOME/physim2-pilot-20261110`, `$HOME/physim2-pilot-r5`) are listed as harmless and stay until the lead removes
  them.
- Docker Desktop: at least 4 CPUs and at least 6 GB; at least 11 GiB free on the Mac's disk; and, for step 3, about
  4 GiB of the Mac's memory free beside Docker Desktop's (K16). No container of anything else running during steps
  2 and 3.
- Step 1: the guard line shows `Using CPython 3.12.<n>` with nothing after the number; the image built is
  `physim2-ring:4` (the first build of it as written anywhere); after step 1, grep the installed `mcp` for
  `MCP_`-prefixed environment reads (the coordinator's ruling).
- After 2a: every `layers` entry is `{'rlimits': True, 'uid': n, 'cleanup': True}` and the line reads `box True 64
  0`. After 2b: `failed_new` holds only `b_lab_process_dropped_it_after_loading`. Report `box_limits`, `control`,
  the agent box's net with `proxy_loopback_names`, and the item box's net (the first 2b at this code anywhere).
- Before each job: the first two commands of step 0 (T19; the one `.venv` line is expected); the request names
  this commit, its caps are what the lead wrote, and 3b's bound is at most the lead's auto-approval limit ($50).
- During a job: 3d and 3f by the order of the `==>` lines (`reference.log`, then `rollout.log`); a cut job is
  closed by point 8 and packed in a session that holds the key.
- After each job: 3h prints `"key_scan": "clean"` and `"complete": true`; before the folder is handed on, the lead
  checks that `key_scan.json` lists `PRIME_API_KEY` under `credentials_from_the_environment`; the job's ledger row
  is closed; vf-eval and the laboratory are gone from the status command's process list.

Not covered by this pass: by me, no rollout, no container, nothing on macOS; I did not rerun the check tools,
`check_step3` or the auditors' tripwire and container runs; K11 to K13, K16, X20 and X21 I confirmed by reading the
cited lines on both sides, not by running them. No detail of the lead's machine is written here.
