# RUNBOOK for the Mac session: PhySim v2 on verifiers
<!-- HOLD-BEGIN: a verdict edits the text between this line and HOLD-END, and nothing else in this file -->
**ON HOLD (round 4, 11 Nov 2026). Run nothing from this copy.** The round-3 GO for steps 0 to 2 held for the
commit `08bd5a669867623a476e7446a74612be47001b3b` and for that commit only. The code and this file were changed
in round 4 (the laboratory's bearer, box caps in code, the spend stop, a step 3 that is driven by a request, the
exam rulings E1 to E16), and that round has no verdict yet, so nothing below is released: not steps 0 to 2, not
step 3, not step 4. A new notice replaces this one when the round-4 verdict is written (it will begin
`**GO for steps 0 to 3.**`, or `**GO for steps 0 to 2.**`, or stay a hold); until then a session that reads this
file stops here (rule A.1) and reports.
<!-- HOLD-END -->

<!-- PIN-BEGIN -->
**Pin.** This file names no commit to check out: a commit cannot hold its own hash. The commit is the
40-character hash in the coordinator's GO message. The lead checks it out (section C) and gives it to the
session, and the first line that step 0 prints must equal it. The code is identified by the sha256 of
`PIN.sha256`, the list of the sha256 of every file the pilot executes or imports; step 0 recomputes both.
sha256 of `PIN.sha256`: `cd67eb4b8d706acf44c23dce72efd087532b422a5b66179c1cdc92561ffd03e4`
<!-- PIN-END -->

What this is: the exact commands to (0) verify the code, the session and the disk, (1) install, (2) run the scripted,
model-free smoke test on Docker at $0, (3) run the model rollout that ONE REQUEST FILE describes, as often as
there are requests, one at a time, and (4) clean up. This is the text of round 4. Steps 0 to 2 and step 4 are the
commands of round 3 with the changes that `README.md`, section 8.12, lists (image `physim2-ring:2`, no certificate
file, the exam config `ring_r4`, the null policy in the reference table, two more names in the environment check).
Step 3 is new: it is driven by a request (schema `rollout-job/v1`) and by the tools `tools/check_request.py`,
`tools/vfrun.py --request` and `tools/pack_rollout.py`.
Evidence. Round 3 rehearsed every command of steps 0 to 2 and of step 4 except the image build and its status
command, and every point of "If a run was interrupted" except point 4, in the cloud container (Linux x86_64,
Docker 29.9.2), each as ONE `sh -c '<text>'` (`results/rehearsal_round3.json`). Round 4: the tools of step 3 ran
there end to end through vf-eval against a stand-in for the model endpoint, in capped boxes of image
`physim2-ring:2`, and under tripwires on the host (`results/round4_step3.json`); which commands of this text were
issued as written, and which were not, is listed at the end of this file.
**Nothing here has run on a Mac: every statement about macOS and Docker Desktop is inferred.** No command of
step 3 has called a model from this code.

## A. Rules for the session that follows this file

1. **Two things come from the lead before your first command:** the absolute path of the study folder, exactly as
   `pwd -P` printed it there (it ends in `research/alife/vecworld/program/round6/vfport`), and the 40-character
   commit hash of the coordinator's GO message. You follow the copy of this file that is in that study folder.
   Unless its notice (the lines after the title) begins `**GO for steps 0 to 2.**` or `**GO for steps 0 to 3.**`,
   or if you were given no hash: stop, run nothing. Step 3 runs only under a notice that begins
   `**GO for steps 0 to 3.**`, after steps 0 to 2 have passed on this Mac at this commit.
2. **One command per call, copied from this file.** The only change you make is to replace the literal text
   `/ABSOLUTE/PATH/TO/vfport` by the path of the study folder (every occurrence: some commands hold it several times), and,
   in the two commands of "If a run was interrupted" that have one, the placeholder `PID_FROM_THE_STATUS_LINE` or
   `NAME_FROM_THE_STATUS_LINE` by what the status command printed (a pid is digits only; a name is `vf-` and 32
   hexadecimal digits, or two lower-case words joined by `_`: anything else is not put into a command), and, in step 3, the four placeholders that
   step 3 names (`JOB_ID`, `SOURCE_COMMIT`, `CEILING_USD`, `GO_DATE`). **A step-3 placeholder is replaced only by
   text that you have first read, character by character, against the shape step 3 gives for it** (lower-case
   letters, digits and hyphens; 40 hexadecimal digits; a plain number; a date): text of any other shape is never
   put into a command, because a shell would run it. Write the path out in every command. Never put it in a
   variable, never rely on the folder a previous command was in, never type a command from memory.
3. **Every command starts with the same guard**:
   `cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && ...`
   If the path is wrong, the guard fails and the rest of the line does not run. A command that prints nothing
   where this file says it prints something has not run: stop.
4. **No subagents, no parallel commands.** A subagent starts in another folder. One command at a time.
5. **Stop rule.** If the output differs from what this file says to expect (apart from the one exception named in
   step 2b), or anything asks for a password or for `sudo`, or prints `refused:`, or Docker stops answering:
   **stop and report what you saw. Do not retry, do not repair, do not try another way.** A deviation is a
   result of the pilot, not an obstacle. The only recovery this file has is "If a run was interrupted".
   **After a stop that does not end in point 6 of that section** (a second interruption, `EXIT 97`, a deviation in
   step 1, 2 or 4): leave both pilot folders as they are, the hidden store included, and say in the report that
   they are still there. If both result files exist, step 4 removes them later, on the lead's word. If not,
   step 4 cannot, nothing else in this file may, and they are the lead's to remove, by hand. The folder of
   step 3 (`$HOME/physim2-rollouts`) is never removed by a command of this file.
6. **Long commands run detached** and write a log that ends with a line `EXIT <status>`; you then ask for their
   state with the status command of the step. Never run a long command in the foreground: a session's
   foreground command is cut after a few minutes, and a cut run leaves containers behind. A detached command
   prints one line (Docker's version) and returns at once.
7. **The disk.** The pilot keeps a floor of 8 GiB of free space on the file system of the home folder. Step 0
   checks it, the three starts of step 1 check it, and every tool of steps 2 and 3 checks it before it starts
   (`--disk-floor-gib 8` on its command) and every 15 seconds while a rollout runs. Below the floor nothing
   starts, and a running rollout is stopped by its tool (one SIGTERM to its vf-eval, the same path a time limit
   takes); the log then holds a line that begins `refused:` and ends with `EXIT 97`. **When that happens: stop and
   report** (after a stop during a run: points 1 to 5 of "If a run was interrupted", then stop). **You never
   make room:** you delete nothing, clear no cache, remove no image, change no setting. How much room this Mac
   and Docker Desktop get is the lead's decision.
8. **Never, on the Mac:**

   | never | why |
   |---|---|
   | `sudo`; edits of `~/.zshrc`, `~/.zprofile`, `~/.zshenv`; `export` of a variable for later commands; `docker context use`; setting any `DOCKER_*` variable | nothing in the pilot needs them; every variable is written on the command that uses it, and the tools refuse a session that holds one of the names step 0 looks for |
   | `docker run` with `-v`, `--mount` or the Docker socket; any other `docker run` by hand for anything in this repository, whatever its options (`--pid`, `--ipc`, `--tmpfs`, `--privileged`, `--volumes-from` included) | the exam's cleanup deletes files of one user id wherever it can see them; a mounted Mac folder would be in sight (the driver refuses when an extra file system is mounted, but do not rely on it). The only `docker run` of the pilot is the image check of step 1, copied from this file |
   | pasting the route's own commands (the `sh -c` lines of `physim2_env/grading.py` and `physim2_env/taskset.py`) into a shell or a container | they change owners and modes and delete as root |
   | `physim2_env/public/_item.py`, `physim2 validate`, or a model's `predict.py`, on the Mac itself | they run submitted code |
   | `agents/*.py`; anything in `redteam/`, in `rehearsal/` or in `../../round5/agentenv` (its `mac/` runbook and compose file included); `tools/check_units.py`, `tools/check_driver.py`, `tools/check_safety.py`, `tools/check_interrupt.py`, `tools/check_round3.py`, `tools/check_round4.py`, `tools/check_step3.py`, `tools/check_runbook.py`, `tools/make_round4_step3.py`, `tools/standin_model.py`, anything in `tests/`; the option `--stand-in-endpoint` of `tools/vfrun.py` | attack scripts, the cloud rehearsal's own scripts and development checks for the cloud container (some start containers, one starts a listener that plays a model); the round-5 compose file mounts host folders into a container that deletes there as root |
   | `.venv/bin/vf-eval`, `tools/vfeval.py` or `tools/build_reference.py` by hand | vf-eval is started by `tools/vfrun.py` only: that is where the environment allow-list, the disk floor, the stop path, the stand-in for the model credential and, in step 3, the spend stop are |
   | `pkill`, `killall`, `kill -1`, `kill -9`, a `kill` that is not the stop command of "If a run was interrupted", `docker rm` by filter or with `$(...)`, any `prune`, `vf-eval --clean`, `rm -rf` of anything this file does not spell out, deleting anything to make room | they reach beyond the pilot: other verifiers runs on this Mac (PhySim v1) use the same container names `vf-...`, and a prune removes other projects' images and build cache |
   | opening `~/.prime/config.json`, `~/.docker/config.json` or any other credential file; printing the environment with its values (`env` alone, `printenv`); writing a key into a file or onto a command line | steps 0 to 2 need no credential; step 3 takes the key from the environment of its one paid command and nowhere else; the step-0 check prints names only |
   | another `[env.agent.runtime] type`, another harness; a model, a cap or a config that is not the request's; editing a request or a config; a second try of a job after a failure | stop and report instead. A job runs once; a request that is wrong is answered with a report, and the requester writes a new one |
   | creating or changing `LEAD-GO-MODEL-SPEND.json` on your own; displaying `rollout.log`, a `traces.jsonl`, a transcript or anything under `rollouts/<job>/out/` or `publish/` of step 3 | the go for model spend is the lead's word, written down by you only when the lead says it in this session; the run files hold what an examined model wrote, and you have a shell on this Mac |
   | `tools/docker_shim` | it is for Linux hosts without IPv6 and cannot work on macOS. If a run fails with `net.ipv6.conf.all.disable_ipv6`: stop and report |

## B. What the pilot does to the Mac itself (the whole inventory)

Read from the code that `PIN.sha256` identifies and from verifiers 0.3.2.dev163 (file and line in brackets;
`vf:` is `verifiers/v1/`); the cloud runs saw the same on Linux. What differs on macOS is said in place and is
inferred. Where a line holds for step 3 only, it says so; everything else holds for steps 1 to 3.

**Processes on the Mac, as your user.** `uv` (step 1 only), which builds this project with the pinned build
backend (`hatchling==1.33.0` and five pinned packages under it: `pyproject.toml`, `uv.lock` `[manifest]`); the
`docker` client; `git` (step 0, and in step 3 one fetch and reads of three files of one commit); one tool at a
time (`.venv/bin/python -B tools/prove.py`, `tools/check_probe.py`, `tools/vfrun.py`; in step 3 also
`tools/check_request.py`, `tools/run_report.py` and `tools/pack_rollout.py`, which start nothing but `git`), which
starts one vf-eval at a time (`.venv/bin/python -B <study>/tools/vfeval.py @ ...`: verifiers' own entry point,
started by our launcher under `nice -n 10`); vf-eval starts one laboratory process per rollout
(`.venv/bin/python -m physim2_env.lab_tools`: it simulates the hidden world and answers the agent's requests),
many short `docker` commands, and through the laboratory's runtime two kinds of short helpers: a Python one-liner
that waits for the laboratory's port (`.venv/bin/python -c ...`, up to 9 minutes if the port never opens) and
`tail` [vf:mcp/launch.py:62-72, 279-287, 355]. `tools/prove.py` and `tools/check_probe.py` also start two helpers
of our own: `tools/make_instances.py` (seconds; in step 3 it is `tools/vfrun.py --stage instance` that starts it)
and, once per reference table, `tools/build_reference.py`, which runs round 5's reference agent on the Mac to build
the reference submission C (our code, no submitted code; the hidden parameters reach it through a file of mode
0600 in the store, never on a command line). `tools/vfrun.py --stage reference` turns into `tools/prove.py` (the
same process, the same pid, the same log).
Every detached command also leaves one waiting shell, a copy of the shell that issued it, which does nothing but
wait for its tool and then write the `EXIT` line; it ends with the tool.
No predictor, no hostile test agent and no model-written code runs on the Mac: they run in containers only. What
a model wrote is on the Mac as DATA in the run folders and in the store's `captures/`; no tool imports, executes
or evaluates it.

**What reaches those processes from your session (the environment).** A tool copies nine names from the
environment it was started in, if they are set: `PATH`, `HOME`, `TMPDIR`, `USER`, `LOGNAME`, `LANG`, `LC_ALL`,
`LC_CTYPE`, `TZ`, and the `VF_RUN_ID` of its command. Everything else that vf-eval, the `docker` client and the
laboratory see is set by the tool (`PRIME_RUNS_MODE=disabled`, `PYTHONPATH=<study folder>`, thread and JAX
settings, in step 2b one made-up canary value named `HF_TOKEN`; in step 3 the store's path and the path of the
run's spend log) [`tools/vfrun.py`, `child_env`]. No `DOCKER_*`, `MCP_*`, `PHYSIM2_*`, `PYTHON*`, proxy or
certificate setting (`SSL_CERT_FILE` among them) or credential of the session can get through, with ONE exception
in ONE command (next paragraph), and a tool refuses to start (`refused: the environment of this command holds
...`) when the session has one of the names step 0 looks for. `PATH` and `HOME` are taken as they are: that is why
step 0 has you check, yourself, which `docker` context answers, and why a tool refuses to start unless that
context names a Unix socket of this machine. The commands of this file that are not tools (`git`, `docker`,
`shasum`, `df`, the interpreter one-liners of steps 1 and 2) run with the session's whole environment, as any
command of the session does; `DYLD_*` variables are not looked for by anybody.

**The model key (step 3 only): who holds it, and for how long.** Your session's environment holds
`PRIME_API_KEY`, before and after the pilot. Every command of the session inherits it, the tools included, and
no tool reads its value except as listed here:

| process | has the key | for how long | what it does with it |
|---|---|---|---|
| `tools/vfrun.py --stage rollout --model-credentials prime` (the one paid command) | in its environment, like every command | the rollout and its grading | copies `PRIME_API_KEY` and `PRIME_TEAM_ID` into the environment of ONE child, its vf-eval; refuses to start a model run without `PRIME_API_KEY` in its environment (the name is looked for, the value never read). In every other stage and tool the child gets neither |
| that vf-eval | in its environment | from its start to its end: set-up, the agent's wall time (at most 180 minutes), finalize and grading (at most 160 minutes more; then the tool stops it) | verifiers' model client sends it as the `Authorization` header to `https://api.pinference.ai/api/v1` and to nowhere else: the run's config names that address itself, so the Prime login file cannot move it [`tools/vfrun.py`, `PRIME_INFERENCE_URL`; vf:configs/client.py:37-57]. verifiers may read `~/.prime/config.json` for the team id |
| the laboratory | **no**: verifiers starts it without any variable whose name holds `API_KEY` [vf:runtimes/subprocess.py:104, 134, 151]; `PRIME_TEAM_ID` (an account name, not a secret) does reach it, and it drops every token-like name from its own environment after loading (on Linux also from what `/proc` shows; not on macOS) | | |
| `docker` clients of vf-eval | **no**: the pilot starts them without credential-like names and without `PRIME_*` [`physim2_env/runtime.py`, `docker_client_env`]. One exception: the `docker rm --force <its box>` at the end of a box inherits vf-eval's environment for the seconds it runs [vf:runtimes/docker/__init__.py:553-567]; a `docker` client puts no variable into a container unless told to | | |
| a box (the model's, the grader's, a reference policy's) | **no**. A container inherits nothing from the Mac. The harness in the model's box holds a per-rollout secret for verifiers' interception server, with which it asks for model calls; those calls are made by vf-eval, counted and capped (step 3, the spend stop) | | |
| `tools/pack_rollout.py` | in its environment | seconds | reads the VALUE (and those of `HF_TOKEN`, `WANDB_API_KEY` if set) into memory to search the run's files for it, plain and base64; prints and writes file names and counts only |
| the waiting shell of a detached command, `tools/check_request.py`, `tools/run_report.py`, `git`, `docker` started by you | in their environment, as every command of the session | their life | nothing |

The key is never on a command line, never in a file the pilot writes, never in a box. The key scan of
`tools/pack_rollout.py` looks for its value in every file that would be published and in the job folder.

**The box (every container of the pilot: the model's box, the grading boxes, the boxes of the reference
policies).** verifiers creates it; the pilot adds caps to that one `docker run` and reads them back from Docker
before the box is used (a box without them is not used: the rollout fails at boot)
[`physim2_env/boxcaps.py`, `physim2_env/runtime.py`]. No Docker Desktop setting is involved.

| cap | value | what the agent sees when it is hit |
|---|---|---|
| CPUs | 2 (`--cpus 2`) | slower; no error |
| memory | 4 GB, or what the request's `box_memory_gb` lowers it to (1 to 4); no swap (`--memory`, `--memory-swap`) | the kernel kills the largest process of the box: `Killed`, exit status 137; the box goes on |
| processes and threads | 512 (`--pids-limit 512`) | `fork: Resource temporarily unavailable`; Python: `can't start new thread` |
| root file system | read-only (`--read-only`) | `Read-only file system` for any write outside the places below, the home directory `/root` included |
| `/workspace` | 1 GiB, memory-backed (`--tmpfs`) | `No space left on device` |
| `/tmp` (the scratch) | 512 MiB, memory-backed | the same |
| `/dev/shm` | 64 MiB (Docker's default) | the same |
| `/etc/physim2`, `/runtime` | 1 MiB and 16 MiB, memory-backed: the exam's own files | not for the agent |
| network | none of its own: verifiers cuts the box and gives it one proxy on the Mac, through which it reaches the model route and the laboratory and nothing else [vf:runtimes/docker/egress.py] | refused connections |

Everything a box can write is memory and counts against its memory cap: a box that fills `/workspace` and `/tmp`
has 2.4 GB left for its processes. **A box cannot write to Docker's disk**, so a model cannot make Docker
Desktop's disk image grow; that is why this pin asks for no disk setting. Measured from inside a box in the
cloud container (`results/round4_step3.json`, checks K2 to K10). Docker Desktop's virtual machine remains the
wall between a box and the Mac; that wall was not tested by this study.

**What is signalled or killed on the Mac.** Every target below is a process that the pilot itself started; no
signal is sent by name, by user or to "all processes".

| who sends | to what (who can be the target) | which signal, when |
|---|---|---|
| verifiers, in vf-eval | the laboratory process it started: its process group, which holds that one process [vf:runtimes/subprocess.py:45-53, 197-221, 225-228] | SIGTERM at the end of every rollout and when vf-eval stops; SIGKILL if it has not ended 5 s later |
| Python's asyncio, in vf-eval | the same laboratory process | SIGKILL, if the object that stands for it in vf-eval is closed or discarded while the laboratory still runs (the end of vf-eval's event loop after an error, for example) |
| verifiers, in vf-eval | the `docker` client command that is under way: the process group of that one client, which holds the client and what it started (a credential helper, a CLI plug-in) [vf:runtimes/container.py:44-65] | SIGKILL, **whenever the call is cut: at every stop of vf-eval** (SIGTERM, Ctrl-C, a failed rollout that cancels the others), at a time limit inside verifiers, and at a deadline of the pilot's own code around a box command (`physim2_env/grading.py`, `taskset.py`, `access.py`: staging, an item's time limit, the collection of `submission/`). A killed client does not undo what Docker already did: a helper container it started ends by itself and removes itself (`--rm`) |
| Python, in vf-eval | the `docker rm --force <its box>` client that verifiers starts at the end of every box [vf:runtimes/docker/__init__.py:553-567] | SIGKILL by Python if that client has not answered in 30 s; the box then stays and is found by its run label |
| verifiers, in vf-eval | the helper it started through the laboratory's runtime: the port probe `python -c ...` or `tail`, its own process group [vf:runtimes/subprocess.py:103-129] | SIGKILL, if the call is cut while the helper runs (same occasions as the `docker` client row) |
| verifiers, in vf-eval | `git rev-parse`, started once to find its own version [vf:utils/version.py:23-31] | SIGKILL by Python if it has not answered in 5 s |
| `tools/vfrun.py` | the vf-eval it started (one process) [`stop_child`, `run_child`] | ONE SIGTERM, however often the tool itself is told to stop (vf-eval then removes its containers and stops its laboratory); SIGKILL only if it is still there 120 s later. When: a run exceeds its time limit (an hour in 2a and 2b, 90 minutes in 2c; in step 3 the request's wall minutes plus 160 minutes for set-up and grading), the disk watchdog trips, or the tool itself is stopped or fails. Before the signal the tool writes the reason to `<run>.stopped.json`. After any of these the tool ends with a status other than 0 (97 disk, 98 stopped or killed, 130 after a stop by signal) and starts nothing further |
| `tools/vfrun.py` | the helper it started, `tools/make_instances.py` or `tools/build_reference.py` (one process) [`run_helper`] | SIGTERM, SIGKILL 20 s later, only when the tool is told to stop while the helper runs |
| `tools/vfrun.py`, `tools/check_probe.py`, `tools/prove.py`, `tools/check_request.py` | their own `docker context inspect`, `docker info`, `docker run --rm` (the control container of 2b), `docker version` and `git` clients | SIGKILL by Python if the client has not answered in 60 s (120 s for the control, 20 s for `git`), and also when the tool is itself interrupted while it waits for that client |
| Python, in a tool | the tool itself | after a stop by SIGTERM the tool ends itself with the interrupt signal: the log shows a traceback ending `KeyboardInterrupt` and `EXIT 130` |
| the kernel (Linux only) | the laboratory process, when the vf-eval that started it dies [vf:mcp/server.py:112-118] | SIGKILL. **Not on macOS:** there a laboratory whose vf-eval was killed outright stays until it is stopped ("If a run was interrupted", point 4) |
| you | ONE process of the pilot: the pid that the status command printed, after the stop command has compared that pid's command line with the eight exact beginnings of the pilot's own programs; it sends nothing otherwise | SIGTERM, only in "If a run was interrupted" |

**The spend stop, the turn limit, the context limit and the wall time of a model run are not signals.** They end
the agent's part of the rollout inside vf-eval (a stop condition on the trace; the refused model call is answered
`400 rollout stopped: ...`), after which vf-eval collects `submission/`, grades it and exits by itself with
status 0. Nothing on the Mac is killed for them.
Inside containers the driver kills the predictor's processes, verifiers signals a harness process through
`docker exec`, and one test agent of step 2b (`harness-killall`) runs `kill -9 -1` in its own box: the box is a
container that verifiers created for it without any Mac folder mounted.

**What is deleted on the Mac.**

| who | what | where |
|---|---|---|
| `uv sync` (step 1) | an existing `.venv` of the study folder would be replaced; the dry run before it must say `Would create`, not `Would replace` | study folder |
| `tools/make_instances.py` | `store/<instance>/hidden/examples.npz`, a file it wrote a moment before | store |
| `tools/vfrun.py`, command form and `tools/prove.py` (steps 2a to 2c, and the reference stage of step 3) | the run folder of an EARLIER call with the same name, only if it holds nothing but vf-eval's own files; happens only when a tool is started again. The request route's own run folder (`rollouts/<job>/out`) is never replaced: a job that has run files is refused | scratch; `rollouts/<job>/reference` |
| `tools/prove.py` | `store/<instance>/work/reference_<policy>` for box checks of policies other than C: not reached with the arguments of this file | store |
| the package (`bundle.py`, `access.py`) and Python's `tempfile` | temporary folders the same process created (`physim2-bundle-*`, `physim2-io-*` under `$TMPDIR`) | temp |
| verifiers | the laboratory's working folder `~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>`, which it creates under a name drawn at random for that rollout and removes at its end (were a folder of that exact name already there, it would be used and removed all the same: 48 random bits make that a collision nobody can arrange from a box); its `logs/latest` link in a run folder; at the first rollout an empty temporary folder `vf-network-*` that it made for the build of its helper image | home, scratch, temp |
| verifiers | the containers it created, `vf-<32 hex>`, by `docker rm --force <that name>`; helper containers started with `--rm` | Docker |
| `docker run --rm` (step 1, and the control of step 2b) | the test container it just started | Docker |
| you, "If a run was interrupted" | a leftover container of this pilot, by its exact name and after its label was read back; the two pilot folders of steps 1 and 2 (point 6) | Docker, home |
| you, step 4 | the two pilot folders of steps 1 and 2, after their results were copied out | home |
| step 3: `tools/vfrun.py --request`, `tools/check_request.py`, `tools/pack_rollout.py`, `tools/settle.py`, the laboratory, the capture of `submission/` | **nothing.** They create, append and replace in place (next table); a publication folder is created once and never overwritten | |
| the disk watchdog | nothing, ever | |

**What is replaced in place** (a new file written beside the old one and renamed over it, or a file opened for
writing again), all inside the two pilot folders or the folder of step 3:

| who | file |
|---|---|
| the laboratory | `store/<instance>/hidden/labs/<rollout>/state.json` (its budget counters, after every request) |
| the task controller, in vf-eval | `store/<instance>/captures/<rollout>/checkpoint.tar` and `checkpoint.json` (the newest copy of `submission/`) |
| `tools/prove.py`, `tools/check_probe.py` | their state files and the `--out` file in the scratch (`prove_state.json`, `proof_mac.json`, ...) |
| `tools/vfrun.py` | `<run name>.toml` and `<run name>.stopped.json` beside a run folder; in step 3 `rollouts/<job>/status.json`, `dry-run.toml`, `resolved.toml`, `model_entry.json` |
| `tools/check_request.py --fetch` | `shared-ledger.json` of step 3 (the newest copy; a request and a config are created once and never replaced) |
| the store's index | `store/index.json`, rewritten by `tools/make_instances.py` with one row more |

Append-only: `LEDGER.jsonl`, `INSTANCES.jsonl`, `rollouts/<job>/spend.jsonl`, the laboratory's `log.jsonl`, the
two `PILOT_NEVER_REUSE_AS_EXAM.txt`, the logs.

**What is written and left on the Mac.** uv's own Python 3.12, if uv has none yet: the DRY RUN of step 1
already downloads it (`~/.local/share/uv/python`; 104 MB on disk in the cloud rehearsal); `.venv` in the study
folder (about 1 GB with jax) and uv's cache (`~/.cache/uv`);
the folder `$HOME/physim2-pilot-20261110` (mode 0700) with `store` and `scratch`, and in step 4
`$HOME/physim2-pilot-20261110-results`; in the store, next to the hidden instance, one more file with the hidden
parameters, `store/<instance>/work/reference_C.theta.json` (mode 0600; it goes with the store); after a run was
stopped, a small `<run name>.stopped.json` beside the run folder (the reason, in words and numbers);
`~/.cache/verifiers/` (created by verifiers); one small file `/tmp/vf-port-<hex>` per rollout, which verifiers
never removes (leave them; do not delete by pattern); small state files of the `docker` client's builder under
`~/.docker/buildx/` (seen on Linux; inferred for the Mac); only after a vf-eval was killed outright, small
folders nobody removes: the laboratory's working folder `~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>` (one
log file), `$TMPDIR/physim2-io-<random>` (one socket), and possibly `$TMPDIR/physim2-bundle-<random>` (a copy of
the public package, about 1 MB) and an empty `$TMPDIR/vf-network-<random>`. In Docker Desktop's disk image: the
images `physim2-ring:2` (about 620 MB), `python:3.12-slim`, and `localhost/verifiers-network:1` with
`alpine:3.22`, which verifiers builds itself at the first rollout (if an image of that name is already on the
Mac, from other verifiers work, verifiers uses it as it is, and runs it with the right to configure the network
of each box: it is the lead's own image either way); and **the build cache of those two builds** (BuildKit;
`docker system df` shows it as "Build Cache"), which nothing in the pilot removes. Docker Desktop's disk image is
a file on the Mac that grows with all of this and does not shrink by itself. A box adds nothing to it (above).
**Step 3** adds the folder `$HOME/physim2-rollouts` (mode 0700), which no command of this file removes:

| in `$HOME/physim2-rollouts` | what | holds |
|---|---|---|
| `LEAD-GO-MODEL-SPEND.json` | the lead's standing go: a dollar ceiling and a date | written by you on the lead's instruction in the session, and by nobody else |
| `requests/<job>.json`, `configs/<name>.toml`, `shared-ledger.json` | copies of three files of one commit of the repository | data; public |
| `INSTANCES.jsonl`, `LEDGER.jsonl` | every instance name ever used, with its job; per job the reserved bound and, at its end, the counted cost | numbers and names |
| `store/` | the hidden side of every pilot instance (the hidden parameters and the secret; `PILOT_NEVER_REUSE_AS_EXAM`), the laboratory's logs, the grades, and under `captures/` what each run's `submission/` and `/workspace` held (agent-made files: data) | **hidden values; never published as it is** |
| `rollouts/<job>/` | the request and config as run, `status.json`, `reference.json` and the reference runs, `dry-run.toml`, `resolved.toml`, `model_entry.json` (prices as listed at the start), `spend.jsonl` (every model call: counts and dollars), `out/` (vf-eval's run folder: the trace with the model's text), the logs | the model's text; the account's team id in the trace |
| `publish/<job>/` | the publication folder that `tools/pack_rollout.py` builds: what may leave the Mac | checked by the key scan; no hidden value, no machine detail |

**What listens on the Mac.** All of it for the minutes a run lasts, all on the loopback address or in a folder
of your user.

| what | where | who can connect, and what it needs |
|---|---|---|
| verifiers' interception server, one per vf-eval [vf:interception/server.py:346, 444-447] | TCP 127.0.0.1, a port the system chooses | any process on the Mac and, on Docker Desktop, any container through `host.docker.internal`. Every route needs a per-rollout secret that only vf-eval and the harness in that rollout's box hold. Behind it stands the model client: in steps 0 to 2 a stand-in without any key; **in step 3 the client with the key**. Whoever holds the per-rollout secret can ask for model calls, and that is the examined model itself; every such call passes the spend stop (the configured model only, capped per call and in total) |
| verifiers' proxy, one per box [vf:runtimes/docker/__init__.py:311-321; vf:runtimes/docker/egress.py:160-167, 213-231] | TCP 127.0.0.1, a port the system chooses | the same; it answers only to its own password (given to that box) or to an address that carries a secret of that box. For requests of its box to the laboratory, and only for those, it adds the laboratory's bearer [`physim2_env/runtime.py`, `BearerEgressProxy`] |
| the published port of each box [vf:runtimes/docker/__init__.py:196] | TCP 127.0.0.1, a port Docker chooses, forwarded to port 8000 in the box | processes on the Mac; nothing of the pilot listens on port 8000 in a box |
| the laboratory, one per rollout [vf:mcp/server.py:278-283; `physim2_env/lab_tools.py`, `_serve`: always 127.0.0.1, whatever `MCP_HOST` says] | TCP 127.0.0.1, a port the system chooses | **every request needs the rollout's bearer**: 256 random bits drawn in vf-eval at the rollout's set-up, handed to the laboratory over verifiers' own channel to it and to the box's proxy in vf-eval's memory. It is in no environment, on no command line, in no file and in no box; the laboratory's record holds its sha256 only. Without it: `401` and an empty body, before the request reaches the laboratory's code. The DNS-rebinding protection that verifiers turns off is on again: the bearer with another `Host` gets `421`, with a foreign `Origin` `403`. A laboratory that was given no bearer serves nothing. The rule "no other container runs" stays as a second wall |
| the task controller, one per rollout [`physim2_env/access.py`, `BoxAccess`] | a Unix socket `$TMPDIR/physim2-io-<random>/io.sock`, in a folder only your user can enter (the socket's path must stay under 104 bytes on macOS: with the system's default `TMPDIR` it does) | your user's processes; every request needs a 256-bit secret |
| `tools/check_probe.py`, while it runs (step 2b) | TCP 127.0.0.1, a port the system chooses | anything that can reach the Mac's loopback; it accepts a connection, records the peer and closes it |

On Linux verifiers also makes a Unix socket in a temporary folder that it mounts into a helper container; off
Linux it does not [vf:runtimes/docker/__init__.py:318-321, 348-408]. Nothing of the pilot listens on any other
address, and step 3 starts no listener that steps 0 to 2 do not start.

**No model credential in steps 0 to 2.** Two things on the route read the Prime login `~/.prime/config.json`
and the key in it: verifiers, when it is merely imported and again when it builds a model client without a key
in the environment [vf:configs/cli/eval.py:86; vf:configs/client.py:37-57, 93-104; vf:utils/prime.py:9-20]; and
the prime-runs SDK, which vf-eval calls once per run even with uploads off [vf:utils/platform.py:93;
prime_runs/run.py:456; prime_traces/core/config.py:25-32]. The pilot closes both readers before verifiers is
imported, in every process it starts (`physim2_env/_nokey.py`, `tools/vfeval.py`), gives every scripted run a
stand-in client (`base_url = "http://127.0.0.1:9/v1"`, a key variable that is never set) and passes no
`PRIME_API_KEY` on. Shown in the cloud container with a made-up file in a scratch home: the stock route opens the
file and loads its key; the pilot's processes never open it, in the tests and through the whole rehearsal, where
the kernel reported every open of that file (`results/round3_checks.json`, `results/rehearsal_round3.json`).
The file on this Mac stays where it is; do not move or open it. This holds for every command of step 3 as well,
the reference table and the dry run included, except the one paid command; and in a scripted run NO model call
can leave vf-eval at all (without a spend table there is no meter, and without a meter the wrapped client
answers `400` itself: `results/round4_step3.json`, check C37).

**Network.** `uv sync` downloads from PyPI, one wheel from github.com and, if uv has no Python 3.12 of its own,
that Python from github.com; `docker build` pulls `python:3.12-slim`, installs 41 hashed wheels from PyPI and
one Debian package (`binutils`, from `deb.debian.org`, in the build stage); the first rollout makes verifiers
build its helper image (`alpine:3.22` from Docker Hub and Alpine's package mirror). Nothing is uploaded: every
run is made with `push = false` and `PRIME_RUNS_MODE=disabled`, and in steps 0 to 2 no model is called.
**Step 3, at run time:** vf-eval talks to `api.pinference.ai` (the model calls, with the key) and to nothing
else; `tools/vfrun.py` and `tools/check_request.py --prices` each make one `GET
https://api.pinference.ai/api/v1/models` without any credential; `git fetch` talks to the repository's host. A
box talks to verifiers' proxy on the Mac only, and at set-up it downloads nothing (the harness is in the image;
replayed with the network off, fixer A's `tests/harness_setup.sh`). That vf-eval opens no other connection in a
model run is read from the code (the run's config names the inference address; uploads are off) and was NOT
measured at the socket: no model run has been made from this code yet.

## C. By hand, before the session's first command (the lead)

| check | command | expected |
|---|---|---|
| hold lifted | the coordinator's message | GO for steps 0 to 3 (or 0 to 2), with a 40-character commit hash |
| where the checkout is | directly under your home folder, for example `~/physim`; not under `~/Documents` or `~/Desktop` | those two are synced to iCloud on this Mac: a synced `.venv` of 1 GB and a synced store are not wanted |
| right code | in the study folder: `git fetch origin claude/fisim-agent-world-research-hepmlz`, then `git checkout --detach <the hash of the GO message>`; `git rev-parse HEAD`; `git status --short` | that hash, all 40 characters; nothing listed |
| right text | the first lines of `RUNBOOK_MAC.md` in the study folder | they begin `**GO for steps 0 to 3.**` (or `0 to 2`), not ON HOLD |
| user | `id -u`; `echo "$HOME"`; `ls "$HOME/physim2-pilot-20261110" "$HOME/physim2-pilot-20261110-results"` | not 0; your own home; no such folders. A current backup of the Mac exists |
| machine | `uname -m` | `arm64` |
| folder | `pwd -P` in the study folder | ends in `research/alife/vecworld/program/round6/vfport`. **This output, character for character, is the path you give the session** (step 0 compares it) |
| path is plain | `pwd -P \| LC_ALL=C grep -E '^[A-Za-z0-9/._-]+$'` in the study folder | it prints the path again. If it prints nothing, the path holds a space or another character outside letters, digits and `/ . _ -`: move the checkout first |
| the session | started in the study folder; given that path and the hash of the GO message | no subagents; one command per call |
| tools | `command -v uv docker`; `uv --version`; `docker context show`; `docker info` | uv 0.11 or later (it must know `--managed-python`); Docker Desktop's own client and context `desktop-linux`; it answers. If uv is missing or older: stop and ask, do not install it from inside the session |
| variables | `env \| cut -d= -f1 \| grep -E '^(PHYSIM2_\|UV_\|VIRTUAL_ENV\|PYTHON(PATH\|HOME\|EXECUTABLE)\|__PYVENV_LAUNCHER__\|DYLD_\|DOCKER_\|BUILDX_\|VF_\|MCP_HOST\|MCP_PORT\|PRIME_RUNS_MODE)'` | nothing. This is your terminal; the session checks its own environment in step 0 and the tools check theirs |
| other runs | `docker ps -a --filter label=verifiers.run`; `docker ps`; `docker images physim2-ring` | nothing, **and no container of anything else is running** while steps 2 and 3 run (the laboratory now needs a secret, section B; the rule stays as a second wall). Save the output of `docker ps -a`, `docker images` and `docker system df` as the baseline |
| room | `df -Pk "$HOME"`; Docker Desktop: Settings, Resources | at least 11 GiB free on the Mac before step 0: the pilot's floor of 8 GiB plus the about 3 GiB that steps 1 and 2 write (half in the study folder and uv's cache, half in Docker's disk image). With less, a later command refuses or the watchdog stops a run: a stop like any other, nothing is lost and nothing is deleted to make room. The watchdog measures the file system of the home folder only: Docker Desktop's disk image must be on it (the default). 4 CPUs and at least 6 GB of memory for Docker Desktop's virtual machine (a box is capped at 2 CPUs and 4 GB, and the grading boxes come one at a time). No Docker Desktop setting is changed by the pilot or needs to be: a box of this pin cannot write to Docker's disk at all (read-only root, memory-backed scratch; section B) |
| power | plugged in; no sleep for the 45 minutes of steps 1 and 2, nor while a rollout of step 3 runs (up to its wall time plus grading) | a sleep is an interruption |
| network | VPN, TLS-intercepting proxy | none (the image build needs a direct connection) |
| Docker's own settings | `~/.docker/config.json`, read by you, not by the session: a `proxies` section; `docker images localhost/verifiers-network` | no `proxies` section (Docker copies such settings into every container as environment variables, past the pilot's allow-list). If the helper image is listed it comes from your other verifiers work; the pilot uses it as it is, with the right to configure each box's network |
| credentials | for step 3 only: the session's environment holds `PRIME_API_KEY` (and `PRIME_TEAM_ID`, if the account has teams) | `~/.prime/config.json` may stay; steps 0 to 2 never open it and need no key in the session. In step 3 the key reaches one command, by the environment only (section B); the tool refuses a model run whose command has no `PRIME_API_KEY` in its environment |
| during the pilot | the pilot folders in `$HOME` | not opened in Finder: a `.DS_Store` makes step 4's `rmdir` fail after its deletes (a stop, nothing lost) |

## 0. Verify the code, the session and the disk (seconds)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && git rev-parse HEAD && pwd -P | grep -Fx "/ABSOLUTE/PATH/TO/vfport" && git --no-optional-locks status --porcelain --ignored -- . ../../round5/agentenv ../../../vw1 && echo "TREE-LISTED"
```

Expected: three lines. The first is the 40-character hash that the lead gave you from the coordinator's GO
message: compare all 40 characters. The second is the path of the study folder, the same text you put into the
command (if it is missing, the path you were given is not the folder's real path: stop). The third is
`TREE-LISTED`. A line between the second and the third names a changed or added file, or (marked `!!`) a file that
git ignores, such as a bytecode cache or an environment left by an earlier install: stop. No `TREE-LISTED`: stop.
(The command writes nothing, not even git's index.)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && shasum -a 256 PIN.sha256 && shasum -a 256 -c PIN.sha256 > /dev/null && echo PIN-OK
```

Expected: two lines, the hash of the pin block above followed by `PIN.sha256`, then `PIN-OK`. `PIN.sha256` lists
the sha256 of every file the pilot executes or imports (the package, the tools, the agents, the configs, round
5's `agentenv` and the `vw` library). If a listed file was changed or is missing there is no `PIN-OK`; what
appears instead is a line that begins `shasum: WARNING:` (for example `shasum: WARNING: 1 computed checksum did
NOT match`), after a line `shasum: <file>: No such file or directory` for a missing file. No `PIN-OK`, or another
hash in the first line: stop.

Your own environment, and the Docker engine your commands reach (the lead's check in section C looked at the
lead's terminal, not at you):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && env | cut -d= -f1 | awk '/^(PHYSIM2_|UV_|VIRTUAL_ENV|PYTHON(PATH|HOME|EXECUTABLE)|__PYVENV_LAUNCHER__|DYLD_|DOCKER_|BUILDX_|VF_|MCP_HOST|MCP_PORT|PRIME_RUNS_MODE)/ { bad++ ; print "FOUND " $0 } END { print NR " names, " bad + 0 " refused" }' && docker context show && docker context inspect --format '{{.Endpoints.docker.Host}}'
```

Expected: three lines. `<n> names, 0 refused`, where n is the number of variables of your session (some tens;
`0 names` means the check did not run: stop). Then `desktop-linux`. Then a Unix socket in the home folder,
`unix:///Users/<you>/.docker/run/docker.sock`. A line `FOUND <name>` before the first line (names only are
printed, never values), another context, or an address that is not a `unix://` socket under your home folder
(`tcp://`, `ssh://`, another machine): **stop and report**. Do not unset anything and do not switch the context:
that is the lead's to decide. (The listing takes each line of `env` up to its first `=` as a name; a variable
whose VALUE holds a line break adds a line of its own, which can only add a `FOUND` line or raise n, never hide
a name.)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}}' && echo "CONTAINERS-LISTED" && docker images -q physim2-ring:2 && echo "IMAGES-LISTED" && test ! -e "$HOME/physim2-pilot-20261110" && test ! -L "$HOME/physim2-pilot-20261110" && test ! -e "$HOME/physim2-pilot-20261110-results" && test ! -L "$HOME/physim2-pilot-20261110-results" && test ! -e .venv && test ! -L .venv && echo "NO-PILOT-FOLDERS"
```

Expected: four lines. Docker's version, `CONTAINERS-LISTED` (no container of this pilot: a name before it is a
stop), `IMAGES-LISTED` (no image `physim2-ring:2` yet: an image id before it is a stop), `NO-PILOT-FOLDERS`
(neither pilot folder nor a `.venv` exists, not even as a link). A missing line: stop.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && df -Pk "$HOME" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) print "DISK-OK " int(free / 1048576) " GiB free" ; else print "refused: " int(free / 1048576) " GiB free on the file system of the home folder, the floor is 8 GiB" }'
```

Expected: `DISK-OK <n> GiB free`, n at least 8 (the lead made sure of 11 before the session started, section C; with
8 to 10 a later command may refuse, which is a stop like any other). A line that begins `refused:` (rule 7):
stop and report; delete nothing.

## 1. Install (about 10 minutes, most of it the image build)

A cut or an unexpected output anywhere in this step: run nothing more, report, stop. Step 1 has no recovery
procedure; what a stop here leaves behind (a `.venv`, the pilot folder, an image, a running `uv` or
`docker build`) is the lead's to remove before any new start. The dry run, the sync and the image build each begin
with the disk check: below 8 GiB free they print one line `refused: under 8 GiB free ...` and start nothing.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f pyproject.toml && test -f uv.lock && df -Pk "$HOME" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) exit 0 ; print "refused: under 8 GiB free on the file system of the home folder" ; exit 1 }' && cd / && uv sync --project "/ABSOLUTE/PATH/TO/vfport" --locked --python 3.12 --managed-python --dry-run 2>&1 | grep -E "^Using CPython|project environment|Would (download|install)|error"
```

Expected, four lines:

- `Using CPython 3.12.<n>` and nothing after the number (3.12.13 in the cloud rehearsal). A path after it
  (`Using CPython 3.12.<n> interpreter at: ...`) means uv took a Python that is not its own: stop.
- `Would create project environment at: /ABSOLUTE/PATH/TO/vfport/.venv`, exactly, with your path. `Would
  replace` or `Would use`, or any other path: **stop** (finding A1: `uv sync` deletes and recreates the
  environment it names).
- `Would download <n> packages` and `Would install <n> packages` (cloud rehearsal: `Would download 1 package`
  and `Would install 103 packages`; on the Mac the first number is larger, the cache is empty).

An `error` line: stop. This command changes nothing in the study folder. It is not free of effect: if uv has no
Python 3.12 of its own yet, it downloads one now, before it prints anything (cloud rehearsal: 33 MB; it goes to
`~/.local/share/uv/python`), so allow it a minute.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && mkdir -m 700 "$HOME/physim2-pilot-20261110" && mkdir "$HOME/physim2-pilot-20261110/scratch" && echo "PILOT-FOLDER-MADE"
```

Expected: `PILOT-FOLDER-MADE`. `mkdir` fails if a pilot folder exists already, and nothing after it runs: stop.
(The build of this pin reads no certificate file: the step that made `docker/extra-ca.crt` is gone.)

The real `uv sync` downloads several hundred megabytes on a Mac whose cache is empty, so it runs detached. This
is the only `uv` command that changes anything; no later command uses `uv`. It builds this project with the
pinned build backend; a `pyproject.toml` whose pins differ from `uv.lock` makes it fail (`--locked`).

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f pyproject.toml && test -f uv.lock && df -Pk "$HOME" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) exit 0 ; print "refused: under 8 GiB free on the file system of the home folder" ; exit 1 }' && docker info --format '{{.ServerVersion}}' && { ( nohup uv sync --project "/ABSOLUTE/PATH/TO/vfport" --locked --python 3.12 --managed-python > "$HOME/physim2-pilot-20261110/scratch/sync.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/sync.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once. Status (repeat until the log's last line is `EXIT 0`; any other
`EXIT` line, or a line with `error`: stop; no `EXIT` line after 20 minutes: stop and report, signal nothing):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && tail -n 3 "$HOME/physim2-pilot-20261110/scratch/sync.log"
```

Expected when it is finished: two lines that begin with ` + ` (the last of the installed packages), then
`EXIT 0`.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B -c "import physim2_env, physim2_script, verifiers, numpy, scipy, jax; print(verifiers.__version__, numpy.__version__, scipy.__version__, jax.__version__, physim2_env.__file__, physim2_env._nokey.state())"
```

Expected: `0.3.2.dev163 2.5.4 1.18.1 0.12.0.1 /ABSOLUTE/PATH/TO/vfport/physim2_env/__init__.py stand-in` with your
path. The last word says that verifiers' reader of the Prime login is closed in this process (section B); any
other last word: stop.

The status and stop commands of step 2 find the pilot's processes by the path of this interpreter. Check that
the interpreter shows that path as its own command line:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B -c "import os, subprocess; line = subprocess.run(['ps', '-ww', '-p', str(os.getpid()), '-o', 'command='], capture_output=True, text=True).stdout.strip(); print(line[:160]); print('INTERPRETER-OK' if line.startswith('/ABSOLUTE/PATH/TO/vfport/.venv/bin/python -B -c ') else 'INTERPRETER-DIFFERS')"
```

Expected: two lines. The first is the interpreter's own command line, cut at 160 characters: it begins
`/ABSOLUTE/PATH/TO/vfport/.venv/bin/python` with your path and goes on with ` -B -c import os, subprocess; ...`
as far as the 160 characters reach. The second is `INTERPRETER-OK`. If the second line is `INTERPRETER-DIFFERS`
(the first then shows another program, for example a `Python.app` of a Python that is not uv's own): **stop**.
Nothing after this step could find or stop the pilot's processes.

The image build takes minutes, so it runs detached:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && df -Pk "$HOME" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) exit 0 ; print "refused: under 8 GiB free on the file system of the home folder" ; exit 1 }' && docker info --format '{{.ServerVersion}}' && { ( nohup docker build -f docker/Dockerfile.ring -t physim2-ring:2 docker/ > "$HOME/physim2-pilot-20261110/scratch/build.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/build.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once. Status (repeat until the log's last line is `EXIT 0`; any other
`EXIT` line: stop; no `EXIT` line after 30 minutes: stop and report, signal nothing):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && tail -n 2 "$HOME/physim2-pilot-20261110/scratch/build.log"
```

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker run --rm --network none --label verifiers.run=physim2-pilot-20261110 physim2-ring:2 python -c "import numpy, scipy, jax; print(numpy.__version__, scipy.__version__, jax.__version__)"
```

Expected: `2.5.4 1.18.1 0.12.0.1`. This is the ONE image of every box: the agent's, the grader's and the reference
policies'. It also holds, preinstalled from hashed pins, the program of verifiers' stock `bash` harness and its 35
packages (`docker/harness-requirements.txt`), so that a box downloads nothing when a rollout starts; the build
is the only moment anything of the image comes from the network (`python:3.12-slim`, 41 wheels from PyPI, each
checked against its sha256, and `binutils` from Debian's mirror in the build stage). Do not build
`docker/Dockerfile.network`: verifiers builds its own helper image at the first rollout.

The hidden side lives in a store OUTSIDE the repository. Make one fresh ring instance (a new secret and a new
hidden theta are drawn now; about 15 s):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/make_instances.py --store "$HOME/physim2-pilot-20261110/store" --world ring --config ring_r4 --n 1 --prefix mac-ring
```

Expected: one JSON line with `"instance_id": "mac-ring-w0"`, `"n_items": 64`, `"R": 16` and a
`secret_commitment` (public). `ring_r4` is the exam config of the profile `ring`, the one step 3 uses (64 items,
256 samples per item, a laboratory of 400 ticks in which starting an episode costs 17).

## 2. Scripted smoke test on Docker ($0, no model, no upload; about 35 minutes)

The tools start verifiers' vf-eval (`physim2-env`, `--env.id isolated-verifier`) with the Docker runtime and the
scripted harness; they set `push = false`, `PRIME_RUNS_MODE=disabled` and a stand-in model client, build the
environment of everything they start from the allow-list of section B, and keep the disk floor of rule 7.
`VF_RUN_ID=physim2-pilot-20261110` is on every run command: verifiers writes it on every container it creates as
the label `verifiers.run`, and the tools refuse to start without it. The store path and the disk floor are on
every command; nothing depends on a variable set earlier.

**Before 2a, again before 2b, and again before 2c: nothing else runs in Docker.**

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker ps --format '{{.Names}} {{.Image}}' && echo "RUNNING-LISTED"
```

Expected: one line, `RUNNING-LISTED`. A line before it is a running container of somebody (name and image):
**stop and report**; do not stop that container. Run this command three times in step 2: before 2a, before 2b
and before 2c; and in step 3 where step 3 says so. (On Docker Desktop a running container can reach the Mac's
loopback, where the pilot's listeners are; each of them needs a secret now, section B, and this rule is the
second wall. Whether to stop a foreign container is the lead's decision.)

**Status command of step 2** (use it after starting 2a, 2b or 2c, and whenever you want to know what runs):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && { tail -n 4 "$HOME/physim2-pilot-20261110/scratch/prove.log" "$HOME/physim2-pilot-20261110/scratch/probe.log" "$HOME/physim2-pilot-20261110/scratch/single.log" 2>/dev/null | cut -c 1-200 ; echo "containers:" ; docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' ; echo "processes:" ; ps axww -o pid= -o command= | awk -v p="/ABSOLUTE/PATH/TO/vfport" 'BEGIN { py = p "/.venv/bin/python " } { line = $0 ; sub(/^ *[0-9]+ /, "", line) ; if (index(line, py) != 1) next ; r = substr(line, length(py) + 1) ; k = "OTHER" ; if (index(r, "-B tools/prove.py ") == 1 || index(r, "-B tools/check_probe.py ") == 1 || index(r, "-B tools/vfrun.py ") == 1) k = "TOOL" ; else if (index(r, "-B " p "/tools/vfeval.py @ ") == 1) k = "VF-EVAL" ; else if (index(r, "-m physim2_env.lab_tools") == 1) k = "LAB" ; else if (index(r, "-B " p "/tools/make_instances.py ") == 1 || index(r, "-B tools/make_instances.py ") == 1 || index(r, "-B " p "/tools/build_reference.py ") == 1) k = "HELPER" ; else if (index(r, "-c") == 1) k = "PROBE" ; print k " " substr($0, 1, 160) }' ; echo "free:" ; df -Pk "$HOME" | awk 'NR == 2 { print int($4 / 1048576) " GiB" }' ; echo "status done" ; }
```

It prints the last lines of the logs that exist (each under a line `==> <file> <==`, each line cut at 200
characters), then under `containers:` the containers of this pilot (`<name> <state>`), under `processes:` the
processes of this pilot, under `free:` the free space of the home folder's file system in GiB, and `status
done`. A container line is a box, `vf-<32 hex> Up ...`, or, for a second at a time, a helper that verifiers or
the probe tool started under a two-word name chosen by Docker (cloud rehearsal: `tender_gates Up Less than a
second`); a helper removes itself. A process line is a word, the pid, and the command line cut at 160
characters. The word says what the process is; it is found by comparing the command line, letter for letter,
with this study folder's `.venv/bin/python` followed by the program's own name:

| word | the command line continues with | what it is |
|---|---|---|
| `TOOL` | `-B tools/prove.py `, `-B tools/check_probe.py ` or `-B tools/vfrun.py ` | the tool you started |
| `VF-EVAL` | `-B /ABSOLUTE/PATH/TO/vfport/tools/vfeval.py @ ` | the tool's vf-eval |
| `LAB` | `-m physim2_env.lab_tools` | the laboratory of the rollout under way |
| `HELPER` | `-B /ABSOLUTE/PATH/TO/vfport/tools/make_instances.py `, `-B tools/make_instances.py ` or `-B /ABSOLUTE/PATH/TO/vfport/tools/build_reference.py ` | a helper of the tool, for seconds (a minute for the reference submission) |
| `PROBE` | `-c` | verifiers' wait for the laboratory's port, for a second; it ends by itself |
| `OTHER` | anything else | not expected: stop and report the line |

The waiting shell of a detached command is not listed, nor is any process of another checkout. A step is finished
when its log ends with an `EXIT` line and nothing is listed under `containers:` and `processes:` (a `PROBE` line
left by an interrupted run does not count: it goes away by itself). While a step runs, wait and ask again; start
nothing else. A Docker error under `containers:` (Docker does not answer): stop.

**The "must show" rule.** Right after you started 2a, 2b or 2c, the status must show a `TOOL` line. If it does
not, and the log of that step has no `EXIT` line: send no signal and start nothing; ask for the status every few
minutes until the log ends with an `EXIT` line or 60 minutes have passed since the start, whichever comes first;
then stop and report (the run cannot be seen from here, so it cannot be stopped from here either). If the log
already ends with an `EXIT` line other than `EXIT 0`: stop and report. `EXIT 97` with a line `refused:` before it
is the disk floor (rule 7).

### 2a. One world, four policies, then C once more with one box per exam item (about 12 minutes)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/prove.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/proof" --world ring --config ring_r4 --worlds 1 --prefix mac-ring --policies null,D,P0,C --box-check C --no-cross-check --disk-floor-gib 8 --out "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" > "$HOME/physim2-pilot-20261110/scratch/prove.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/prove.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once (the tool runs on, detached). Then use the status command, the
first time right away: the "must show" rule.

Expected in `prove.log` when it is finished: lines `null: [..]`, `D: [..]`, `P0: [..]`, `C: [..]` (one skill per
world), a line `C (one box per item, world 0): ..`, then two JSON lines, the table on the K-to-C scale, for
example (cloud container, another hidden world) `{"O": 1.16, "K": 0.0, "null": -0.075, "D": 0.445, "P0": 0.759,
"C": 1.0}`, and a line that begins `{"sigma":`, and last `EXIT 0`. The numbers differ on the Mac: the hidden world
is new. `null` is the baseline predictor every box starts with (the public prior, no laboratory data): it is
what a failed item is scored as, and it lies near K, a little below or above. Then:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B -c "
import json
p = json.load(open('$HOME/physim2-pilot-20261110/scratch/proof_mac.json'))
r = p['per_world'][0]['rollouts']; b = p['one_box_per_item_check_world_0']['C']
print('all_graded', p['all_graded'], 'all_ok', p['all_ok'], 'failed_items', p['n_failed_items_total'])
print('ticks', {k: r[k]['lab_ticks_used'] for k in r})
print('layers', {k: r[k]['grade']['layers'] for k in r})
print('box', b['identical_per_item_scores'], b['grade']['item_boxes'], b['grade']['infrastructure_failed_items'], round(b['grade']['item_box_wall_s_mean'], 2))
print('table', {k: round(v['vs_C'], 3) for k, v in p['pooled']['policies'].items() if v['vs_C'] is not None})
"
```

What must hold: `all_graded True all_ok True failed_items 0`; ticks `{'null': 0, 'D': 390, 'P0': 0, 'C': 0}`; every
`layers` is `{'rlimits': True, 'uid': <a number from 20000 to 59999>, 'cleanup': True}`; `box True 64 0 <seconds
per item box>` (2.7 s in the cloud container: report the Mac's number, it is the price of the default grading
mode; with 256 samples per item it is higher than round 3's); in the table null below D below P0 below C, O
above C (ordering, not values). Anything else: stop and report.

### 2b. The boundary checks and the probes, on their own small instance (37 short rollouts; about 25 minutes)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/check_probe.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/probe" --disk-floor-gib 8 --out "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" > "$HOME/physim2-pilot-20261110/scratch/probe.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/probe.log" ) > /dev/null 2>&1 < /dev/null & }
```

Then the status command and the "must show" rule. When `probe.log` ends with `EXIT 0`, the line before it is one
JSON object. Expected on the Mac:

- `"failed_round5": []`
- `"failed_new": ["b_lab_process_dropped_it_after_loading"]`. **This one failure is expected on macOS** and only
  there: the check reads the laboratory process's environment block in `/proc`, which macOS does not have. (On
  Linux the list is empty.)

Any other name in either list: stop and report the two lists. (The checks were brought in line with round 4:
a rollout whose every item fails scores exactly what the null policy scores, never K; five of the hostile test
agents begin by replacing `/usr/bin/tar` or by writing under `/logs`, and now end right there with `Read-only file
system`, which is what the check `d_tar_replacement_and_junk_outside_the_writable_places_are_stopped_by_the_read_only_root`
expects; a box carries one directory less between items.) Several checks were measured on Linux only (the
network cut and its control `c_*`, among them the new `c_agent_box_proxy_refuses_the_workers_own_loopback_names`;
the per-item channels `a2_*`; `agent_sees_only_its_own_processes`); if one of them differs on Docker Desktop,
that is a finding to report, not something to make pass. Then, for the report:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B -c "
import json
p = json.load(open('$HOME/physim2-pilot-20261110/scratch/probe_mac.json'))
e = p['evidence']
print('round5', p['n_reproduced'], 'of', p['n_checks_round5'], p['failed_round5'], 'new', p['n_passed_new'], 'of', p['n_checks_new'], p['failed_new'])
print('staging', {k: e['verifier_box_staging'][k] for k in ('container_evidence', 'world_writable_paths_fixed', 'box_limits', 'predictor_uid')})
print('control', e['c_control'], e['c_listener_hits'])
print('agent box net', e['c_agent_box_net'])
print('item box net', e['c_verifier_box_net_all_items'])
print('lab env', {k: e['b_lab_process'][k] for k in ('token_values_left_in_environ', 'token_like_names_left_in_os_environ')})
c = e['a2_channels_one_box_per_item']
print('channels', c['mark_was_read'], c['dirs_touched_after_staging'], c['lo_rx_packets'], c['pid_step'])
print('kill in box', e['h_harness_dies']['killall']['first'], 'wall_s', round(p['wall_s']))
"
```

Report these lines as they are. They answer what only the Mac can answer: what told the driver it was inside a
container (`container_evidence`; in the cloud container `/.dockerenv` and the control group of pid 1), whether
the uncut control container reaches a listener on the Mac (`control`), and what a box can reach: in
`agent box net`, `proxy_loopback_names` shows what the box's proxy answered when it was asked, with the box's
own password, for the Mac's loopback under four names (expected `HTTP 403` eight times).

### 2c. One scripted rollout from a config file (about 4 minutes)

Policy D on `mac-ring-w0` from `configs/scripted_ring.toml`, through the command form of `tools/vfrun.py`. (A
model rollout is NOT started this way: the command form refuses every config that is not scripted; step 3 has
its own route.) It can run once: a second run of the same agent on the same instance is refused.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/vfrun.py --config configs/scripted_ring.toml --run-name single-d --out-dir "$HOME/physim2-pilot-20261110/scratch/single" --store "$HOME/physim2-pilot-20261110/store" --disk-floor-gib 8 > "$HOME/physim2-pilot-20261110/scratch/single.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/single.log" ) > /dev/null 2>&1 < /dev/null & }
```

Then the status command and the "must show" rule (the `TOOL` line reads `... -B tools/vfrun.py --config
configs/scripted_ring.toml ...`). Repeat it until `single.log` ends with `EXIT 0`. The status shows the last four
lines of that log: at the end these are the end of the trace that vf-eval prints (two lines of token counts and
a closing `}`) and `EXIT 0`. Do not open `single.log` or `traces.jsonl` beyond that: in step 3 the same files
hold the examined model's text, and step 3 has a status command of its own that shows the `EXIT` line only. Read
a run only through the report tool, which prints fixed fields and counts:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/run_report.py --store "$HOME/physim2-pilot-20261110/store" --run-dir "$HOME/physim2-pilot-20261110/scratch/single/single-d"
```

Expected: `"1_ok": true`, `"1_reward_present": true`, both `network_restricted` true, `"2_single_use": true`,
`"2_item_isolation": "box"`, `"3_lab"."ticks_used": 390`, `"4_submission_source": "agent_submission"`,
`"5_validation_ok": true`, `"5_n_items": 64`, `"5_n_failed": 0`, `"5_item_boxes": 64`,
`"5_infrastructure_failed_items": 0`, and `"total_hits": 0` under `6_hidden_values_in_the_run_folder`.

After step 2: report. Step 3 needs a notice that covers it (rule A.1), the lead's standing go and a request.

## If a run was interrupted

**This section is for steps 2 and 3.** A cut or an unexpected output in step 0, 1 or 4: run nothing more,
report, stop. **In step 2, use this section once.** At a second interruption of step 2 do points 1 to 5, then
stop and report: no reset, no new start. If you cannot tell whether the section was used before in this pilot
(for example after a restart of the session), treat the interruption as
the second one. **In step 3, use it once per job:** points 1 to 5, then 7 and 8, never point 6; the job is not
run again, whatever happened, and the next request waits until point 8 is done.

Use it when a detached command of step 2 or step 3 did not end with `EXIT 0`: the Mac slept, Docker Desktop stopped, a command was
cut, the session was restarted, you were told to stop, a tool ended with `EXIT 97` (the disk floor: points 1 to 5,
then stop and report, whatever the count) or `EXIT 98` (the tool had to stop its vf-eval, or vf-eval was killed).
Do exactly this, in this order, and nothing else. In particular do not start the step again before the end of
this section.

1. **What is still there?** Run the status command of step 2 (in step 3: the status command of step 3; both list
   the same processes and containers, they differ in the logs they show). It lists the pilot's processes and the
   pilot's containers. Nothing of anybody else can be in either list: the processes are the ones whose command line
   is, letter for letter, this study folder's own `.venv/bin/python` followed by one of the pilot's programs,
   the containers the ones that carry this pilot's run label. (Do not list by the name `vf-`: other verifiers
   runs on this Mac use the same names. Do not look for the pilot with another `ps` or `pgrep` command: a search
   for the folder's name also finds the waiting shell of a detached command, and a signal to that shell stops
   nothing and loses the `EXIT` line.) If Docker prints an error under `containers:`, or a line says `OTHER`:
   stop and report; remove nothing.
2. **A `TOOL` or a `VF-EVAL` line is listed:** tell it to stop, once, by the pid on its line. Take the pid of
   the `TOOL` line if there is one, otherwise of the `VF-EVAL` line:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && ps -ww -p PID_FROM_THE_STATUS_LINE -o command= | awk -v p="/ABSOLUTE/PATH/TO/vfport" 'BEGIN { py = p "/.venv/bin/python " } { r = (index($0, py) == 1) ? substr($0, length(py) + 1) : "" ; if (index(r, "-B tools/prove.py ") == 1 || index(r, "-B tools/check_probe.py ") == 1 || index(r, "-B tools/vfrun.py ") == 1 || index(r, "-B " p "/tools/vfeval.py @ ") == 1 || index(r, "-m physim2_env.lab_tools") == 1 || index(r, "-B " p "/tools/make_instances.py ") == 1 || index(r, "-B tools/make_instances.py ") == 1 || index(r, "-B " p "/tools/build_reference.py ") == 1) { ok = 1 ; print substr($0, 1, 160) } } END { exit !ok }' && kill -TERM PID_FROM_THE_STATUS_LINE
   ```

   It prints the command line of the process it then signals (the same text as on the status line, without the
   word and the pid). **If it prints nothing, no signal was sent**: that pid is not, or no longer, one of the
   pilot's programs. Then run the status command once more; if a `TOOL` or a `VF-EVAL` is still listed, stop
   and report.
   The tool passes the signal on to its vf-eval, or to its helper; vf-eval removes its containers and stops its
   laboratory itself (2 to 4 seconds in the cloud rehearsals; allow two minutes). Ask for the status again until
   no process and no container is listed. The log of the stopped command then ends in one of these ways, all of
   them expected here:

   | stopped | the log ends with |
   |---|---|
   | a tool, inside a rollout or while a helper ran | a Python traceback whose last line is `KeyboardInterrupt`, then `EXIT 130` |
   | a tool, between two rollouts or before the first (no `VF-EVAL` and no `HELPER` was listed) | `EXIT 143`, no traceback; the shell may put one line of its own before it (`Terminated` in the cloud rehearsal) |
   | a vf-eval, by its own pid (no `TOOL` was listed) | nothing more: its tool is gone, so nobody writes into that log |

   Send the signal once; never `kill -9`, never a second pid in the same command.
3. **Containers of the pilot are still listed and no `VF-EVAL` is** (vf-eval was killed before it could clean up;
   the tool's log then ends with a line `refused to go on: vf-eval died of signal 9. ...` and `EXIT 98`): remove
   each one by its exact name, one command per container, the name copied from the status output:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker inspect --format '{{index .Config.Labels "verifiers.run"}}' NAME_FROM_THE_STATUS_LINE | grep -Fx physim2-pilot-20261110 && docker rm -f NAME_FROM_THE_STATUS_LINE
   ```

   It prints two lines: `physim2-pilot-20261110`, the run label that Docker has on record for that name, and then
   the name. **If it prints nothing, or one line that begins `error:`, nothing was removed**: no container of
   that exact name carries this pilot's label (cloud rehearsal: nothing for a container with another label,
   `error: no such object: <name>` for a name no container has). Stop and report.
4. **A `LAB` or a `HELPER` line is still listed and no `VF-EVAL` and no `TOOL` is:** stop it by its pid with the
   stop command of point 2. Neither holds state worth keeping. On Linux a laboratory that has lost its vf-eval
   ends by itself at once; **on macOS it does not (inferred: verifiers asks the kernel for that on Linux
   only), so expect to need this point after a vf-eval was killed outright.** If the stop command prints
   nothing, nothing was signalled and the process is gone already; go on with point 5. A `PROBE` line needs
   nothing: it ends by itself within nine minutes (cloud rehearsal: the probe of a killed vf-eval was listed for
   four minutes, through the reset and the next start, and then was gone).
5. Run the status command again. Expected now: no process line (a `PROBE` line may remain for some minutes), no
   container line. If something else of the pilot is still listed after two minutes: stop and report.
6. **Step 2 only: delete the two pilot folders and start again from the instance** (first interruption only, and
   never after `EXIT 97`; the command refuses below the disk floor). A cut rollout has spent its laboratory budget and its instance cannot be opened again by the same
   agent, so the store is not reusable:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && df -Pk "$HOME" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) exit 0 ; print "refused: under 8 GiB free on the file system of the home folder" ; exit 1 }' && test ! -L "$HOME/physim2-pilot-20261110" && test ! -L "$HOME/physim2-pilot-20261110/store" && test ! -L "$HOME/physim2-pilot-20261110/scratch" && test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch" && mkdir "$HOME/physim2-pilot-20261110/scratch" && echo "pilot folders reset"
   ```

   Expected: `pilot folders reset`. If it prints nothing: stop and report (a pilot folder that is a link is one
   reason; nothing was deleted then). Then continue from the `make_instances` command of step 1, and run step 2
   from its first command. The image and `.venv` stay; the logs of step 1 (`sync.log`, `build.log`) went with the
   scratch folder.
7. Say in the report that a run was interrupted, at which command, and what the status command listed. If
   point 3 or 4 was needed, small folders of the killed vf-eval stay on the Mac and nothing removes them: the
   laboratory's working folder `~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>` (one log file),
   `$TMPDIR/physim2-io-<random>` (one socket; nothing listens on it any more), and possibly
   `$TMPDIR/physim2-bundle-<random>` and an empty `$TMPDIR/vf-network-<random>`. Name them in the report and leave
   them: do not delete by pattern. A `docker` client that a killed vf-eval had started may live on for seconds
   outside the status listing; it ends by itself.
8. **Step 3 only: what a crash in the middle of a model rollout leaves behind, and the clean-up.** After points 1
   to 5 nothing of the job runs any more. What is left, and what happens to it:

   | left behind | where | what to do |
   |---|---|---|
   | containers (the model's box, a grading box, a helper) | Docker, under the run label | point 3, each by its exact name. None may remain |
   | the laboratory process (macOS: it outlives a killed vf-eval), a port probe | the Mac | point 4. The laboratory's port closes with it; its bearer was only ever in memory |
   | the interception server and the box's proxy | inside vf-eval | gone with vf-eval; nothing to do |
   | the task controller's socket and the small temporary folders of point 7 | `$TMPDIR`, `~/.cache/verifiers` | leave them (point 7) |
   | a half-written store: `store/<instance>/captures/<rollout>/checkpoint.tar` (and a `*.tmp` beside it), `hidden/labs/<rollout>/` with the laboratory's budget as spent, `hidden/opened/<hash>.json` (the instance is used: this agent can never open it again), no `final/` folder and no grade | the folder of step 3 | leave it. Nothing reads a half-written file as if it were whole: a later tool takes the last complete checkpoint or none |
   | the job folder: `out/` with or without a trace, `spend.jsonl` (possibly a call that was sent and never settled), `rollout.stopped.json`, `status.json` | the folder of step 3 | leave it; `tools/pack_rollout.py` reads it as it is |
   | the ledger: the job's `reserved` row, and its `ended` row unless the TOOL itself was killed | `LEDGER.jsonl` | if the tool wrote `ended` (the log's last lines show a JSON line with `"ended"` before the `EXIT` line): nothing. If not, the job counts at its whole bound and blocks every later job until you close it (next command) |
   | the instance name and the job id | `INSTANCES.jsonl`, `LEDGER.jsonl` | used, for ever. The job is never run again; a new attempt is a new request with a new job id and a new instance name |
   | the key | nowhere: it was in the environment of the tool and of vf-eval, which are gone | nothing |

   Close the job's books (this starts nothing and spends nothing; it refuses while the job's tool, a laboratory of
   its instance or a container of the run label is still there, and when the ledger has nothing open for the job):

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && VF_RUN_ID=physim2-pilot-20261110 "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/vfrun.py --request "$HOME/physim2-rollouts/requests/JOB_ID.json" --pilot "$HOME/physim2-rollouts" --stage close --disk-floor-gib 8
   ```

   Expected: one JSON line, `{"stage": "close", "job_id": "<the job>", "status": "cut", "counted_usd": <dollars>,
   "count_complete": <true or false>}`, or one line `refused: nothing to close: the ledger holds no open row for
   this job` when the tool had closed the books itself. Any other `refused:` line: stop and report. The counted
   cost is what the run's spend log holds, with ONE WORST-CASE CALL for every call that was sent and never
   settled; with `"count_complete": false` this folder's ledger goes on counting the job at its whole bound against
   the lead's ceiling (the safe side; no tool lowers it afterwards), and the runner records what Prime billed in
   its own table. Then build the publication folder of the cut run (step 3h: the same
   command; it packs what is there and lists what is missing) and report. An interrupted model rollout is recorded
   as cut; its last checkpoint of `submission/` stays in the store, ungraded.

## 3. Model rollouts, one request at a time (SEPARATE GO)

**Not released by a notice that says "steps 0 to 2".** Step 3 runs only when ALL of this holds: the notice of this
file begins `**GO for steps 0 to 3.**`; steps 0 to 2 have passed on this Mac at this commit and the lead has read
their report; the lead's standing go for model spend exists (3.0); a request names this commit (3.1). The tools
check the last three themselves and refuse otherwise; nothing in steps 0 to 2 can start a model run: their
commands carry no request, and `tools/vfrun.py` starts a model only from a request, in the one stage `rollout`,
with `--model-credentials prime` and `--shared-ledger` on its command, after the stages before it have passed.

This is the only step in which an untrusted model acts. It is root in a container for the minutes its request
allows (at most 180). Between it and the Mac stand the box caps of section B (it can write only to memory that
is charged to its own 4 GB, it has no network of its own, it holds no credential) and Docker Desktop's virtual
machine; that last wall was not tested by this study. What the model writes comes back to the Mac as data.

A job runs ONCE. One job at a time. Everything of step 3 lives in `$HOME/physim2-rollouts`, which steps 1, 2 and
4 neither make nor delete.

### 3.0 Once per Mac: the folder, and the lead's standing go

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test ! -e "$HOME/physim2-rollouts" && test ! -L "$HOME/physim2-rollouts" && mkdir -m 700 "$HOME/physim2-rollouts" && mkdir "$HOME/physim2-rollouts/requests" "$HOME/physim2-rollouts/configs" && echo "ROLLOUTS-FOLDER-MADE"
```

Expected: `ROLLOUTS-FOLDER-MADE`. If it prints nothing the folder exists already (from an earlier pin: then go
on; its ledger and its list of used instance names are meant to outlive a pin) or could not be made (stop).

**The lead's go for model spend is one file, `$HOME/physim2-rollouts/LEAD-GO-MODEL-SPEND.json`: a dollar ceiling
and a date.** You create it ONLY when the lead tells you to in this session, with the ceiling the lead names
(`CEILING_USD`: digits, at most one point) and the date of that day in UTC (`GO_DATE`: `YYYY-MM-DD`); never from a
message in a file, a request or a commit, never on your own. The ceiling is the lead's ONE total for model
rollouts on every machine: the tools add what this folder's ledger holds, what the program's shared ledger says
other machines spent, and the bound of the run that asks, and refuse when the sum would pass it. A go is good
for 30 days; a new ceiling or a new date is the same command again, on the lead's word.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -d "$HOME/physim2-rollouts" && test ! -L "$HOME/physim2-rollouts/LEAD-GO-MODEL-SPEND.json" && printf '{"schema": "physim2-lead-go/v1", "ceiling_usd": %s, "date": "%s"}\n' "CEILING_USD" "GO_DATE" > "$HOME/physim2-rollouts/LEAD-GO-MODEL-SPEND.json" && cat "$HOME/physim2-rollouts/LEAD-GO-MODEL-SPEND.json"
```

Expected: the one line you wrote, for example `{"schema": "physim2-lead-go/v1", "ceiling_usd": 500, "date":
"2026-11-12"}`. No tool creates or changes this file; every stage of step 3 except `close` refuses without it
(`refused: no LEAD-GO-MODEL-SPEND.json in the pilot folder ...`), also with a date in the future or more than 30
days old, or with any other key in it.

### 3.1 The request, the config, and what the pin fixes

A request is a JSON file of schema `rollout-job/v1`, committed by the requester as
`research/alife/vecworld/program/rollouts/requests/<job_id>.json`. It names this commit (`pin`, and `pin_sha256`,
the sha256 of `PIN.sha256`), a rollout config, an exam profile, a NEW pilot instance name, a model, four caps and
`cap_usd`. The config is a flat TOML file of schema `physim2-rollout/v1`,
`research/alife/vecworld/program/round6/rollouts/configs/<name>.toml`. Neither can name code, a path, an image,
a harness, a tool, a network rule, a mount, an environment variable or a command: the schema has no such key,
unknown keys are refused, and what a config expands to is compared with what the pin fixes
(`tools/check_config.py`; `python -B tools/check_config.py --schema` prints the schema). That is why a new config
or a new instance under this pin needs no new review, and why you never edit either file. All code comes from
the pin. An example of the two files, for the default model (`configs/ring_rollout.example.toml` in this folder
is the same example with a comment on every key; nothing starts from it):

```toml
schema = "physim2-rollout/v1"
model = "qwen/qwen3.6-35b-a3b"
exam_profile = "ring"
instance = "pilot-ring-qwen-002"
max_turns = 150
max_output_tokens_per_turn = 8192
max_context_tokens = 200000
wall_minutes = 60
box_memory_gb = 4
cap_usd = 1.0
reasoning_effort = "default"
reasoning_summary = "default"
push = false
```

```json
{"schema": "rollout-job/v1", "job_id": "qwen-ring-002", "purpose": "second mechanics rollout on the ring profile",
 "requester": "coordinator", "pin": "<the 40 characters of this commit>", "pin_sha256": "<sha256 of PIN.sha256>",
 "config": "research/alife/vecworld/program/round6/rollouts/configs/qwen_ring_002.toml",
 "exam_profile": "ring", "instance": "pilot-ring-qwen-002", "model": "qwen/qwen3.6-35b-a3b",
 "caps": {"max_turns": 150, "max_output_tokens": 8192, "wall_minutes": 60, "box_memory_gb": 4}, "cap_usd": 1.0}
```

The request repeats what the config says, and the tools refuse when the two differ. What a program can check,
as data (`python -B tools/check_request.py --facts` prints exactly this object, and `tools/check_runbook.py`
fails when this block and the code differ): the request's keys and shapes; every key a config may hold, with
type, range and default; what the pin fixes for every model rollout (the harness is the image's preinstalled
`bash` harness; no retries anywhere; `push = false`); the fields that may appear nowhere; the exam profiles
with their item counts; the scripted policies of the reference table; the stages in their order.

<!-- STEP3-FACTS-BEGIN -->
```json
{
 "request": {"schema": "rollout-job/v1", "keys": ["schema", "job_id", "purpose", "requester", "pin", "pin_sha256", "config", "exam_profile", "instance", "model", "caps", "cap_usd"], "caps_keys": ["max_turns", "max_output_tokens", "wall_minutes", "box_memory_gb"], "job_id": "^[a-z0-9][a-z0-9-]{2,62}$", "instance": "^pilot-[a-z0-9-]{3,40}$", "pin": "^[0-9a-f]{40}$", "pin_sha256": "^[0-9a-f]{64}$", "max_bytes": 16384, "file": "research/alife/vecworld/program/rollouts/requests/<job_id>.json", "wall_minutes_max": 180, "box_memory_gb_max": 4},
 "config": {
  "schema": "physim2-rollout/v1",
  "config_folder": "research/alife/vecworld/program/round6/rollouts/configs/",
  "file_name": "^[a-z0-9][a-z0-9._-]{0,79}\\.toml$",
  "max_bytes": 16384,
  "keys": {
   "schema": {"type": "str", "required": true, "default": null, "one_of": ["physim2-rollout/v1"]},
   "model": {"type": "str", "required": false, "default": "qwen/qwen3.6-35b-a3b", "pattern": "^[a-z0-9][a-z0-9._-]{0,63}/[A-Za-z0-9][A-Za-z0-9._:-]{0,95}$"},
   "exam_profile": {"type": "str", "required": false, "default": "ring", "one_of": ["ring"]},
   "instance": {"type": "str", "required": true, "default": null, "pattern": "^pilot-[a-z0-9-]{3,40}$"},
   "max_turns": {"type": "int", "required": false, "default": 150, "range": [1, 400]},
   "max_output_tokens_per_turn": {"type": "int", "required": false, "default": 8192, "range": [256, 32768]},
   "max_context_tokens": {"type": "int", "required": true, "default": null, "range": [8192, 2000000]},
   "wall_minutes": {"type": "int", "required": false, "default": 60, "range": [5, 180]},
   "box_memory_gb": {"type": "int or float", "required": false, "default": 4, "range": [1, 4]},
   "cap_usd": {"type": "int or float", "required": true, "default": null, "range": [0.01, 500]},
   "reasoning_effort": {"type": "str", "required": false, "default": "default", "one_of": ["default", "none", "minimal", "low", "medium", "high", "xhigh", "max"]},
   "reasoning_summary": {"type": "str", "required": false, "default": "default", "one_of": ["default", "auto", "detailed"]},
   "push": {"type": "bool", "required": false, "default": false, "one_of": [false]}
  },
  "fixed_by_the_pin": {"env": "physim2-verifier", "taskset": "physim2-env", "harness": {"id": "bash", "edit": true, "search": false}, "runtime": "docker", "num_rollouts": 1, "max_concurrent": 1, "retries": 0, "push": false},
  "forbidden_fields": ["agent_dir", "allow", "api_key_var", "args", "base_url", "block", "box_env_allow", "client", "collect", "collect_dir", "collect_tree", "colocated", "command", "compaction", "disk", "endpoints", "entrypoint", "env", "extra_body", "forward_env", "gpu", "headers", "index", "judges", "mount", "mounts", "network", "network_allow", "output_dir", "python", "script", "skills", "store", "system_prompt", "tools", "toolsets", "url", "volume", "volumes", "workdir"],
  "exam_profiles": [
   {"profile": "ring", "world": "ring", "exam_config": "ring_r4", "items": 64, "samples_per_item": 256, "lab_ticks": 400, "reset_cost_ticks": 17, "image": "physim2-ring:2", "box_cpus": 2, "box_memory_gb": 4, "max_turns": 150, "wall_minutes": 60, "reference_policies": ["null", "D", "P0", "PM", "S", "C"]}
  ]
 },
 "reference_table": {"tool": "tools/prove.py", "policies_by_profile": {"ring": ["null", "D", "P0", "PM", "S", "C"]}, "scale": "K = 0 (climatology) and O = 1 (oracle) come from the frozen exam, not from a rollout"},
 "stages": ["instance", "reference", "dry-run", "rollout", "close"],
 "then": "tools/pack_rollout.py",
 "pilot_folder": {"go": "LEAD-GO-MODEL-SPEND.json", "go_schema": "physim2-lead-go/v1", "go_max_age_days": 30, "ledger": "LEDGER.jsonl", "instances": "INSTANCES.jsonl", "shared_ledger": "shared-ledger.json", "shared_ledger_schema": "rollout-ledger/v1", "shared_ledger_source": "research/alife/vecworld/program/round6/rollouts/ledger.json"},
 "prices_from": "https://api.pinference.ai/api/v1/models"
}
```
<!-- STEP3-FACTS-END -->

The scripted policies of the reference table (`tools/prove.py`, at $0, on the job's own instance, in boxes with
the same caps as the model's): `null` is the baseline predictor that every box starts with, left untouched (the
public prior, no laboratory data; `agents/keep_baseline.py`); `D`, `P0`, `PM` and `S` are round 5's reference
agent with that policy (`../../round5/agentenv/agents/reference_agent.py`: fit to laboratory data only; the prior
alone; the prior mean; a posterior sample); `C` is the reference submission built on the Mac from the hidden
parameters by `tools/build_reference.py` and installed by `agents/install_prebuilt.py`. K (climatology, 0) and O
(the oracle, 1) come from the frozen exam itself.

### 3.2 The bill: what bounds it

A model run has a spend stop inside vf-eval, on the Mac (`physim2_env/spend.py`). Before the run the tool reads
the model's listed prices and context window from Prime's public model list (one GET, no credential), saves
that entry in the job folder (`model_entry.json`) and prints, for the request's caps:

    one worst-case call  =  max_context_tokens x input price  +  max_output_tokens x output price
    bound on the bill    =  cap_usd  +  one worst-case call
    crude bound          =  max_turns x (context window x input price  +  max_output_tokens x output price)

**A request is accepted only if `cap_usd` is at least one worst-case call. The bound on the bill is `cap_usd`
plus one worst-case call**: a call is sent only while what was counted so far (plus one worst case for every
call still under way) is below `cap_usd`, and no single call can cost more than the worst case, because its
prompt is bounded before it is sent and its reply by the provider's own limit. The crude bound is what the
turn cap alone would allow without the spend stop; it is printed for comparison and is not what the tools
reserve. (Round 3's text bounded the bill by the token caps of the config, `1.5 x p_in + 0.06 x p_out`. That
was wrong: those caps count each fed-in token once, while the provider bills the whole conversation again at
every turn. The first rollout's caps saw 18,759 input tokens; 758,132 were billed.)

For the default config above, at the prices listed on 11 Nov 2026 ($0.11 in, $1.01 out, $0.099 cache read per
million tokens; window 262,144): one worst-case call = 200,000 x 0.11/M + 8,192 x 1.01/M = **$0.0303**; bound on
the bill = 1.00 + 0.0303 = **$1.0303**; crude bound = 150 x (262,144 x 0.11/M + 8,192 x 1.01/M) = $5.57. The tool
computes all three afresh from the prices of the day. For a model at $10 in and $50 out with a window of
1,050,000 the same caps give $2.41 for one call and a crude bound of $1,636: for such a model `max_context_tokens`
is what keeps one call affordable.

How the count is made (each line has its test in `results/round4_step3.json`):

1. Every HTTP attempt to the provider is counted, where verifiers sends it: one method of one object in vf-eval
   (`EvalClient._request`). verifiers' client never retries by itself [vf:clients/base.py:14-16], the run's
   config allows no retry at any level, and a retry by the harness in the box is a new request, counted like any
   other (C22 to C27).
2. A reply with complete usage costs its tokens at the LISTED prices; the provider's own cost field counts
   instead when it is higher. A reply with missing or partial usage, a streamed reply without a final usage
   chunk, an error reply, a timeout or a cut connection counts as ONE WORST-CASE CALL, never as zero (C2, C5,
   C6, C25 to C30).
3. Cache reads are counted at the full input price unless the saved model entry lists a cache-read price. Where
   the entry lists a cache-write price above the input price, prompt tokens are counted at that price (C3, C4,
   D15b).
4. `max_context_tokens` is enforced: before a call is sent its prompt is bounded from above (the provider's own
   count of the previous prompt plus one token per byte of everything added since, or one token per byte of the
   whole request); a call that could exceed the cap is not sent and the run ends with the stop condition
   `max_context_tokens` (C8 to C11, C17, C34, C35). The strict schema makes the key mandatory and the tool
   refuses a value above the model's window (D2, D15).
5. The counter and the stop are objects of vf-eval on the Mac; nothing in a box can reach them. A box's only
   way to a model is verifiers' interception server, which calls that one counted client; a request for another
   model, another route, more than one choice, a reply cap above the run's, or anything but text and function
   tools is refused unsent; a scripted run has no meter and can send nothing (C7, C18, C36 to C39).
6. `max_turns` stays a cap of its own, and it, the wall time, the reply cap, the context cap and the spend cap
   are all stated to the agent in its task statement, rendered from the run's config.
7. When a stop is reached (`spend_cap`, `max_context_tokens`, the turn limit, the wall time) the run ENDS, it is
   not killed: vf-eval collects what is in `submission/` at that moment and grades it (R11, R14).
8. The tool reserves the bound in `LEDGER.jsonl` before the run and writes the counted cost after it, and every
   call with its tokens, its dollars and their basis into `rollouts/<job>/spend.jsonl`, which the publication
   folder carries as `usage.json`. The runner reconciles the counted cost with Prime's billing afterwards and
   accepts no further request if billing exceeds the count by more than 10 percent plus $0.05. What the count
   rests on and cannot see: that the provider bills what its usage says, and that it holds a reply, reasoning
   included, to the limit it was sent.

### 3.3 One job: the commands, in order

`JOB_ID` is the job id: the request file's name without `.json`. **Read it first**: 3 to 63 characters, lower-case
letters, digits and hyphens only, starting with a letter or digit. `SOURCE_COMMIT` is the 40 hexadecimal digits
that the first command prints. Anything else: stop (rule A.2).

**3a. Bring the job's three files** (the request, the config it names, the program's shared ledger), as data,
out of one commit of the repository's branch. The first command talks to the repository's host and changes
nothing in the checked-out files; the second reads that commit's objects and writes three files:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && git fetch origin claude/fisim-agent-world-research-hepmlz && git rev-parse FETCH_HEAD
```

Expected, last line: 40 hexadecimal digits (`SOURCE_COMMIT`).

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/check_request.py --fetch --source-commit SOURCE_COMMIT --job-id JOB_ID --pilot "$HOME/physim2-rollouts"
```

Expected: one JSON line with `"job_id"`, `"source_commit"`, and under `"request"`, `"config"` and
`"shared_ledger"` each file's name, size and sha256, and `"request_says"`. A line `refused:`: stop and report
(no request of that name in the commit; a request of another shape; a request or config of that name already in
the folder with other content: neither is ever replaced).

**3b. Check the request** (starts nothing; one GET for the prices, without a credential):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/check_request.py --request "$HOME/physim2-rollouts/requests/JOB_ID.json" --pilot "$HOME/physim2-rollouts" --shared-ledger "$HOME/physim2-rollouts/shared-ledger.json" --prices
```

Expected: one JSON line. What must hold before you go on: `"pin"` is this commit and the hash of the pin block;
under `"instance"` all three are `null`/`false` (a new name); `"go"` shows the lead's ceiling and date;
`"bounds"` shows `worst_call_usd`, `bound_usd` and `crude_bound_usd`; `"ceiling"` shows the ledger's sum, what
other machines spent and `after_this_run_at_most_usd`. Compare `bound_usd` with the bound you computed yourself
from Prime's list, and with what the runner's protocol lets you start without asking. A line `refused:` (another
pin; an unknown key; a cap below one worst-case call; a context cap above the model's window; an instance name
the store has seen; the ceiling) is the answer to the requester: report it; do not edit the request.

**3c. Make the instance** (seconds; from here on the instance name is used, whatever happens next):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && VF_RUN_ID=physim2-pilot-20261110 "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/vfrun.py --request "$HOME/physim2-rollouts/requests/JOB_ID.json" --pilot "$HOME/physim2-rollouts" --stage instance --disk-floor-gib 8
```

Expected: `{"stage": "instance", "job_id": "<the job>", "instance": "<its name>", "made": true}`.

**3d. The reference table** (about 10 minutes; $0; scripted policies only). First the command under "Before 2a"
(expected: `RUNNING-LISTED` alone). Then:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/vfrun.py --request "$HOME/physim2-rollouts/requests/JOB_ID.json" --pilot "$HOME/physim2-rollouts" --stage reference --disk-floor-gib 8 > "$HOME/physim2-rollouts/rollouts/JOB_ID/reference.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-rollouts/rollouts/JOB_ID/reference.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once. **Status command of step 3** (use it now, right away: the "must
show" rule of step 2 holds here too, with a `TOOL` line that reads `... -B tools/vfrun.py --request ...` for a
moment and then `... -B tools/prove.py ...`; and use it while the rollout of 3f runs):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && { tail -n 1 "$HOME/physim2-rollouts/rollouts/JOB_ID/reference.log" "$HOME/physim2-rollouts/rollouts/JOB_ID/rollout.log" 2>/dev/null | cut -c 1-12 ; echo "containers:" ; docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' ; echo "processes:" ; ps axww -o pid= -o command= | awk -v p="/ABSOLUTE/PATH/TO/vfport" 'BEGIN { py = p "/.venv/bin/python " } { line = $0 ; sub(/^ *[0-9]+ /, "", line) ; if (index(line, py) != 1) next ; r = substr(line, length(py) + 1) ; k = "OTHER" ; if (index(r, "-B tools/prove.py ") == 1 || index(r, "-B tools/check_probe.py ") == 1 || index(r, "-B tools/vfrun.py ") == 1) k = "TOOL" ; else if (index(r, "-B " p "/tools/vfeval.py @ ") == 1) k = "VF-EVAL" ; else if (index(r, "-m physim2_env.lab_tools") == 1) k = "LAB" ; else if (index(r, "-B " p "/tools/make_instances.py ") == 1 || index(r, "-B tools/make_instances.py ") == 1 || index(r, "-B " p "/tools/build_reference.py ") == 1) k = "HELPER" ; else if (index(r, "-c") == 1) k = "PROBE" ; print k " " substr($0, 1, 160) }' ; echo "free:" ; df -Pk "$HOME" | awk 'NR == 2 { print int($4 / 1048576) " GiB" }' ; echo "status done" ; }
```

It prints, for each of the two logs that exists, a line that begins `==>` (the start of the file's name) and the
first 12 characters of the log's last line (nothing, while the log is empty); then the pilot's containers, the
pilot's processes and the free space, as the status command of step 2 does. The stage is finished when the line under `reference.log` reads `EXIT 0` and nothing is listed under
`containers:` and `processes:`. Any other `EXIT`: "If a run was interrupted" (points 1 to 5, 7), then stop and
report; the job is not continued.

**3e. The dry run** (free; no model is called, no credential is passed or loaded; vf-eval resolves the run's
config, writes it and exits):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && VF_RUN_ID=physim2-pilot-20261110 "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/vfrun.py --request "$HOME/physim2-rollouts/requests/JOB_ID.json" --pilot "$HOME/physim2-rollouts" --stage dry-run --shared-ledger "$HOME/physim2-rollouts/shared-ledger.json" --disk-floor-gib 8
```

Expected: a JSON line with the model's listed prices, `one_worst_case_call_usd`, `cap_usd`,
`bound_on_the_bill_usd`, `crude_bound_without_the_spend_stop_usd`, `ledger_sum_usd`, `spent_elsewhere_usd` and
`ceiling_usd`, then a line of vf-eval that ends `wrote config to ...`. A line `refused:`: stop and report.

---

**STOP. THE NEXT COMMAND SPENDS MONEY, up to `bound_on_the_bill_usd` of the dry run's line.** It runs only for a
job whose check (3b), instance (3c), reference table (3d) and dry run (3e) have passed, under the lead's
standing go, within what the runner's protocol lets you start without asking the lead. First the command under
"Before 2a" once more (expected: `RUNNING-LISTED` alone).

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f "$HOME/physim2-rollouts/LEAD-GO-MODEL-SPEND.json" && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/vfrun.py --request "$HOME/physim2-rollouts/requests/JOB_ID.json" --pilot "$HOME/physim2-rollouts" --stage rollout --shared-ledger "$HOME/physim2-rollouts/shared-ledger.json" --disk-floor-gib 8 --model-credentials prime > "$HOME/physim2-rollouts/rollouts/JOB_ID/rollout.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-rollouts/rollouts/JOB_ID/rollout.log" ) > /dev/null 2>&1 < /dev/null & }
```

---

**3f. While it runs** (set-up, the agent's wall time, then grading: 64 items, each in a fresh box), ask for its
state with the status command of step 3 only. **Never display `rollout.log`, a `traces.jsonl`, or anything under
`rollouts/JOB_ID/out/`**: they hold what the model wrote. (`cut -c 1-12` shows at most the word `EXIT` and a
number.) The run is over when the line under `rollout.log` reads `EXIT 0` and nothing is listed under
`containers:` and `processes:`. `EXIT 0` means vf-eval ended by itself, whichever way the agent's part ended (its
submit, the turn limit, the wall time, the spend stop, the context limit, an error of the agent): each of these
is graded. `EXIT 2` with nothing running: the tool refused before anything started (the last lines of the log
are the tool's own `refused:` line; the status command does not show it: report "refused at the rollout stage"
and stop). `EXIT 1` or another small number with nothing running: vf-eval ended by itself and reported a failure;
go on with 3g and 3h, which show what happened, and say so in the report. `EXIT 97`, `EXIT 98`, `EXIT 130`,
`EXIT 137` or `EXIT 143` (the tool itself was killed or stopped from outside), any `EXIT` line while a container
or a process is still listed, or no `EXIT` line when the wall time plus 160 minutes have passed: "If a run was
interrupted", points 1 to 5, 7 and 8.
In every case: do not run the job again.

**3g. Read the run through the report tool** (fixed fields and counts; no text of the model):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/run_report.py --store "$HOME/physim2-rollouts/store" --run-dir "$HOME/physim2-rollouts/rollouts/JOB_ID/out/JOB_ID"
```

Report its output as it is. A run without a reward (vf-eval was cut before it could grade) is settled as the
null policy, never as K and never by a second run:
`cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/settle.py --store "$HOME/physim2-rollouts/store" --run-dir "$HOME/physim2-rollouts/rollouts/JOB_ID/out/JOB_ID"`.

**3h. The key scan and the publication folder** (also for a cut run):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/pack_rollout.py --request "$HOME/physim2-rollouts/requests/JOB_ID.json" --pilot "$HOME/physim2-rollouts"
```

Expected: one JSON line, `{"files": <n>, "total_bytes": <bytes>, "left_out": [], "missing": [], "key_scan":
"clean", "complete": true}`. The tool builds `$HOME/physim2-rollouts/publish/JOB_ID/` (it must not exist; it is
never overwritten):

| file | what |
|---|---|
| `status.json` | what ran and how it ended: stages, stop condition, error types, the reward, the laboratory's counters, the box caps as read back, the limits, the ledger rows, what is missing |
| `transcript.md` | the whole conversation, readable: every message, tool call and tool result, as data in fences |
| `trace.redacted.jsonl` | the saved trace with credential-like fields removed by name |
| `lab_log.jsonl` | the laboratory's log: one line per request (operation, verdict, ticks, nats, time) |
| `grades.json` | per exam item: failed or not, the fallback reason, the energy score per cell, CPU seconds |
| `reference.json` | the reference table of the scripted policies on the same instance |
| `usage.json` | every HTTP attempt to the provider as counted (tokens, dollars, basis), the total, the prices as listed at the start, the bounds |
| `submission/`, `submission.json` | the frozen submission that was graded, and its manifest |
| `request.json`, `config.toml`, `resolved.toml`, `model_entry.json` | what was asked for and what it resolved to |
| `key_scan.json` | the key scan: file names and counts only |
| `PILOT_NEVER_REUSE_AS_EXAM.txt`, `MANIFEST.json` | the pilot marker; sha256 and size of every file, and what was left out and why |

Before anything is written every candidate file is searched for the VALUES of `PRIME_API_KEY`, `HF_TOKEN` and
`WANDB_API_KEY` of this command's environment (plain and base64), for generic credential shapes (bearer tokens,
private keys, well-known key prefixes) and for the instance's secret and hidden parameters; a file with a hit is
LEFT OUT, stays in the pilot folder, and is listed in `MANIFEST.json` and `key_scan.json` by name and count, never
by value. Machine details (the home folder, the pilot folder, the study folder, the host name, the team id) are
replaced by value in every text file. At most 20 MB per file and 50 MB in all; what does not fit is left out and
listed. `"key_scan"` other than `"clean"` (the command then ends with status 3), a non-empty `left_out` or
`missing`, or `"complete": false`: report the line as it is; publish only what the folder holds.

**What leaves the Mac is this folder and nothing else of step 3**: the runner publishes it under
`rollouts/<job_id>/` on its results branch, by its own protocol, together with its own record of the bound it
reserved and of what Prime billed. The store, the job folder, the ledger and the go file stay on the Mac. The
session uploads nothing else. Then the next request may start at 3a.

## 4. After the pilot

The store of steps 1 and 2 holds theta and the secret of a smoke-test instance that must never be reused. Run this
step only when the lead says so. It removes the two folders that steps 1 and 2 made and nothing of step 3:
`$HOME/physim2-rollouts` (the ledger, the list of used instance names, the hidden side of every pilot instance,
the run folders, the publication folders) stays, through later pins as well, until the lead removes it by hand
when the program has no further use for it. First run the status command of step 2: nothing may be listed. Then copy the results out and remove exactly the two folders, in ONE command, so that nothing is
deleted unless every check and every copy before it succeeded:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test ! -L "$HOME/physim2-pilot-20261110" && test ! -L "$HOME/physim2-pilot-20261110/store" && test ! -L "$HOME/physim2-pilot-20261110/scratch" && test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && test -f "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" && test -f "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" && mkdir "$HOME/physim2-pilot-20261110-results" && cp "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" "$HOME/physim2-pilot-20261110/scratch/proof_mac_items.npz" "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" "$HOME/physim2-pilot-20261110/scratch/prove.log" "$HOME/physim2-pilot-20261110/scratch/probe.log" "$HOME/physim2-pilot-20261110-results/" && test -s "$HOME/physim2-pilot-20261110-results/proof_mac.json" && test -s "$HOME/physim2-pilot-20261110-results/probe_mac.json" && rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch" && rmdir "$HOME/physim2-pilot-20261110" && ls "$HOME/physim2-pilot-20261110-results"
```

Expected: the five file names. If it prints nothing: stop and report. The copied files
hold scores, counters and commitments only (`PILOT_NEVER_REUSE_AS_EXAM`); the run folders of step 2 with their
traces are deleted with the scratch folder. Of step 3, what leaves the Mac is each job's publication folder
(step 3h) and nothing else.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' && echo "CONTAINERS-LISTED" && docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}' && docker system df
```

Expected: `CONTAINERS-LISTED` with no line before it (no container of the pilot), then the images, then Docker's
own table of what its disk holds (images, containers, volumes, build cache). Compare with the baseline of the
by-hand checks: the pilot added `physim2-ring:2`, `localhost/verifiers-network:1` (unless it was there) and no container;
`python:3.12-slim` and `alpine:3.22` may or may not be listed (Docker Desktop does not always list the base
images of a build): that is not a deviation. Another new image, or a container of the pilot, is. The pilot also
added build cache (the "Build Cache" row; several hundred megabytes). **Remove none of it yourself.** The helper
image `localhost/verifiers-network:1` is shared with other verifiers work on this Mac and is not this pilot's to
remove; `physim2-ring:2` is needed by every rollout of step 3 and may be removed by the lead, by hand, when no
further run is planned at this pin (`docker rmi physim2-ring:2`); the build cache can only be removed together with that of every other project (`docker builder
prune`), which is the lead's decision and never the session's. The `.venv` stays until the lead removes the
checkout. Left on the Mac besides: uv's cache and Python, `~/.cache/verifiers`, `/tmp/vf-port-*`, the results
folder.

## What the cloud container could not cover, and what was not rehearsed as written

- macOS and Docker Desktop: nothing. Inferred, not seen: that containers there carry `/.dockerenv` and Docker's
  usual mount table (if not, staging stops with `the box is not recognised as a disposable box` and names the
  mount or the missing sign; nothing is damaged; report it); **that Docker Desktop applies `--read-only`,
  `--tmpfs`, `--memory`, `--pids-limit` and `--cpus` to a box as the Linux engine does** (the pilot reads the caps
  back from the engine before a box is used and refuses a box without them; what a box then sees was measured on
  Linux only) and that its mount table then shows the four tmpfs mounts the in-box guard allows; how `uv` behaves
  and that the Python it manages shows `.venv/bin/python` as its command line (step 1 checks it); that `ps`,
  `shasum`, `df -Pk`, `tail`, `printf` and the system's `awk` print and accept there what they do on Linux (the awk
  programs were run with mawk only; they use `index`, `substr`, `length` and `sub`, nothing newer); that `docker
  context show` says `desktop-linux` and the context's address is a socket in the home folder; that the session's
  shell (zsh) leaves the same waiting shell as `sh` and `bash` did; how a Claude session on the Mac ends a command
  at its limit; that a detached command survives the end of the call that started it, and the end of the session
  (it shares the issuing shell's process group; survival was seen on Linux only); that a laboratory outlives a
  killed vf-eval there; what the app does at a session's end, and what a session's own start-up hook writes or
  fetches; uv's behaviour beyond the two commands of step 1; Docker Desktop's own helper containers, telemetry and
  disk-image limit.
- **A model.** No command of this pin has called one. The spend stop, the context cap, the request route and the
  publication folder ran against a stand-in endpoint on the loopback of the cloud container, which answers with
  made-up usage (`tools/standin_model.py`; `results/round4_step3.json`). Not seen with a real provider: the
  usage fields of Prime's replies as this code reads them (their shape was read from the two saved traces of the
  first rollouts and from the model list); that the explicit `[client]` table of a billed run (the inference
  address, the key's variable) behaves like verifiers' default, which the first two rollouts used; that vf-eval
  opens no connection other than to the inference host; the `reasoning` object of the config key
  `reasoning_summary` (nobody has sent it). The one command with `--model-credentials prime` was never issued.
- The image build of step 1: built in the cloud container behind its TLS-intercepting proxy with two build
  arguments that the Mac does not use; the command of step 1 as written was not run.
- Steps 0 to 2 as text of this round: the commands that changed since round 3 (the tree check with `--ignored`,
  the environment check with three more names, the pilot-folder command without the certificate file, the image
  tag, `make_instances` and `prove.py` with `ring_r4` and the null policy, the reset command with its disk gate)
  were not issued as `sh -c` lines in this round. Step 2b's tool was run at this code with the box caps and
  image 2 (`results/round4_step3.json`: 34 and 66 checks, both lists of failures empty on Linux, 27 minutes on a
  loaded machine), not as its `sh -c` line; step 2c was not rerun (it needs `configs/scripted_ring.toml` to name
  image 2); the numbers quoted for 2a are from the same tool run by profile on another hidden world.
- Step 3 as text: the stages `instance`, `reference`, `dry-run`, `rollout` (against the stand-in), `close` (its
  refusal) and `tools/pack_rollout.py` ran as tools in the cloud container with a scratch folder as the pilot
  folder; `tools/check_request.py --fetch` ran on a scratch repository (no file was ever committed under
  `rollouts/requests/`); the shell lines of 3.0 and 3a to 3h were not issued as written, the paid one least of
  all. A crash in the middle of a model rollout was not produced: stage `close` and the rule "one rollout at a
  time" were tested under tripwires with made-up process and container listings.
- The by-hand checks and three expectations of step 0: the cloud session is root, on x86_64, behind a proxy;
  its Docker context is `default` on `unix:///var/run/docker.sock`; the machine has 2.5 GiB free for everyone, so
  `8` was replaced by a lower floor wherever a tool carried it.
- "If a run was interrupted": points 1, 2, 3, 5 and 6 were rehearsed in round 3, each as part of a first
  interruption. Point 4 did not arise on Linux. Point 8 is new and was not rehearsed (above). The rule for a
  second interruption, the stop of a vf-eval by its own pid and the 60-minute bound of the "must show" rule were
  not exercised.
