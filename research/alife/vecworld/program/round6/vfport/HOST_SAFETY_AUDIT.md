**NOTE of the round-4 second-pass fixer (11 Nov 2026), above the verdict and not part of it:** the GO in the line below holds for commit `8bbab3324ae510990f17be400602e97d4042ef6e` only (sha256 of `PIN.sha256` `776d9a33...fadc`). From commit `841b4a1e1d12afc7cd60b8b184b451d278895b1d` on (the third round-4 pin, `PIN.sha256` `898089fc...108f`) the code carries the second pass's changes for K4, X6 and the minor items, and has no verdict: `RUNBOOK_MAC.md` there says ON HOLD, and so does this note. See `README.md`, section 8.16.

# VERDICT (round 4, 11 Nov 2026): GO for the scripted smoke test on the lead's Mac (steps 0 to 2 of `RUNBOOK_MAC.md`), from the one commit that holds this line (code as judged at c7db465d5fc990aa41d28cfb6cfc36eb34f8b2ed, commands as rehearsed at d9694f3e5b6c92a98c13fb36f02645f01f18728c; sha256 of `PIN.sha256` 776d9a333d545d21abd182879fc311fbb41bd710d024a035b15b48df84f6fadc). NO-GO for step 3, the model rollouts driven by requests: two major findings are open (K4: a model in its box can push an unbounded amount of data into processes on the Mac; X6: the in-box check `validate` reports "as graded" for predictors that fail in grading), and each needs a new pin. It replaces the round-3 GO for 08bd5a669867623a476e7446a74612be47001b3b, which is not to be run any more. See "Re-audit, round 4" at the end; sections 1 to 6 and the re-audits of rounds 1 to 3 are the earlier verdicts, kept as they were.

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
