# RUNBOOK for the Mac session: PhySim v2 on verifiers
<!-- HOLD-BEGIN: a verdict edits the text between this line and HOLD-END, and nothing else in this file -->
**ON HOLD. Run nothing from this file.** The round-2 GO for steps 0 to 2 (given for commit
`af767adbdeac3d00906d7a3394421e1bc4d6e486`) is SUSPENDED since 10 Nov 2026: before running anything, the Mac
session reviewed that commit read-only and returned three major and eleven minor points and facts about the
machine (16 GiB free; a Prime credential file in the home folder), and the coordinator added a disk requirement.
Round 3 of fixes changed the code and this file to meet them (`README.md`, section 8.9); **these changes have not
been re-audited.** Do not run af767adb either: its GO is suspended, not replaced, and its code is not the code
this file describes. The hold on steps 0 to 2 is lifted only by a verdict that says GO: it replaces this notice
by one that begins `**GO for steps 0 to 2.**`, and the coordinator's message then gives the 40-character hash of
the commit that holds the replaced notice. Step 3 (a paid model rollout) has a second hold of its own and stays
NO-GO until steps 0 to 2 have passed on the Mac and been reported.
<!-- HOLD-END -->

<!-- PIN-BEGIN -->
**Pin.** This file names no commit to check out: a commit cannot hold its own hash. The commit is the
40-character hash in the coordinator's GO message. The lead checks it out (section C) and gives it to the
session, and the first line that step 0 prints must equal it. The code is identified by the sha256 of
`PIN.sha256`, the list of the sha256 of every file the pilot executes or imports; step 0 recomputes both.
sha256 of `PIN.sha256`: `cd67eb4b8d706acf44c23dce72efd087532b422a5b66179c1cdc92561ffd03e4`
<!-- PIN-END -->

What this is: the exact commands to (0) verify the code, the session and the disk, (1) install, (2) run the scripted,
model-free smoke test on Docker at $0, (3) run ONE rollout of a cheap model with a stock harness. This is the text
of round 3: it answers the read-only review that the Mac session made of the round-2 text before running anything
(three major and eleven minor points) and the coordinator's disk requirement; `README.md`, section 8.9, lists what
changed and why. Evidence: every command of steps 0 to 2 and of step 4 except the image build, and every point of
"If a run was interrupted", was rehearsed in the cloud container (Linux x86_64, Docker 29.9.2, uv 0.11.32) from a
fresh clone, each command issued the way a session issues it, as ONE `sh -c '<text>'`
(`results/rehearsal_round3.json`: the literal text and the complete output of each; what could not be rehearsed
there is listed at the end of this file).
**Nothing here has run on a Mac: every statement about macOS and Docker Desktop is inferred.** Step 3 has not
run anywhere.

## A. Rules for the session that follows this file

1. **Two things come from the lead before your first command:** the absolute path of the study folder, exactly as
   `pwd -P` printed it there (it ends in `research/alife/vecworld/program/round6/vfport`), and the 40-character
   commit hash of the coordinator's GO message. You follow the copy of this file that is in that study folder.
   Unless its notice (the lines after the title) begins `**GO for steps 0 to 2.**`, or if you were given no hash:
   stop, run nothing.
2. **One command per call, copied from this file.** The only change you make is to replace the literal text
   `/ABSOLUTE/PATH/TO/vfport` by the path of the study folder (every occurrence: some commands hold it several times), and,
   in the two commands of "If a run was interrupted" that have one, the placeholder `PID_FROM_THE_STATUS_LINE` or
   `NAME_FROM_THE_STATUS_LINE` by what the status command printed. Write the path out in every command. Never put
   it in a variable, never rely on the folder a previous command was in, never type a command from memory.
3. **Every command starts with the same guard**:
   `cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && ...`
   If the path is wrong, the guard fails and the rest of the line does not run. A command that prints nothing
   where this file says it prints something has not run: stop.
4. **No subagents, no parallel commands.** A subagent starts in another folder. One command at a time.
5. **Stop rule.** If the output differs from what this file says to expect (apart from the one exception named in
   step 2b), or anything asks for a password or for `sudo`, or prints `refused:`, or Docker stops answering:
   **stop and report what you saw. Do not retry, do not repair, do not try another way.** A deviation is a
   result of the pilot, not an obstacle. The only recovery this file has is "If a run was interrupted", and it
   is for step 2 only.
6. **Long commands run detached** and write a log that ends with a line `EXIT <status>`; you then ask for their
   state with the status command of the step. Never run a long command in the foreground: a session's
   foreground command is cut after a few minutes, and a cut run leaves containers behind. A detached command
   prints one line (Docker's version) and returns at once.
7. **The disk.** The pilot keeps a floor of 8 GiB of free space on the file system of the home folder. Step 0
   checks it, the three starts of step 1 check it, and every tool of step 2 checks it before it starts
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
   | `agents/*.py`; anything in `redteam/`, in `rehearsal/` or in `../../round5/agentenv` (its `mac/` runbook and compose file included); `tools/check_units.py`, `tools/check_driver.py`, `tools/check_safety.py`, `tools/check_interrupt.py`, `tools/check_round3.py` | attack scripts, the cloud rehearsal's own scripts and development checks for the cloud container; the round-5 compose file mounts host folders into a container that deletes there as root |
   | `.venv/bin/vf-eval`, `tools/vfeval.py` or `tools/build_reference.py` by hand | vf-eval is started by `tools/vfrun.py` only: that is where the environment allow-list, the disk floor, the stop path and the stand-in for the model credential are |
   | `pkill`, `killall`, `kill -1`, `kill -9`, a `kill` that is not the stop command of "If a run was interrupted", `docker rm` by filter or with `$(...)`, any `prune`, `vf-eval --clean`, `rm -rf` of anything this file does not spell out, deleting anything to make room | they reach beyond the pilot: other verifiers runs on this Mac (PhySim v1) use the same container names `vf-...`, and a prune removes other projects' images and build cache |
   | opening `~/.prime/config.json`, `~/.docker/config.json` or any other credential file; printing the environment with its values (`env` alone, `printenv`) | steps 0 to 2 need no credential; the step-0 check prints names only |
   | another `[env.agent.runtime] type`, another harness, another model, a second try after a failure | stop and report instead |
   | `tools/docker_shim` | it is for Linux hosts without IPv6 and cannot work on macOS. If a run fails with `net.ipv6.conf.all.disable_ipv6`: stop and report |

## B. What the pilot does to the Mac itself (the whole inventory)

Read from the code that `PIN.sha256` identifies and from verifiers 0.3.2.dev163 (file and line in brackets;
`vf:` is `verifiers/v1/`); the cloud rehearsals saw the same on Linux. What differs on macOS is said in place and
is inferred.

**Processes on the Mac, as your user.** `uv` (step 1 only), which builds this project with the pinned build
backend (`hatchling==1.33.0` and five pinned packages under it: `pyproject.toml`, `uv.lock` `[manifest]`); the
`docker` client; in step 2 one tool at a time (`.venv/bin/python -B tools/prove.py`, `tools/check_probe.py`,
`tools/vfrun.py`), which starts one vf-eval at a time (`.venv/bin/python -B <study>/tools/vfeval.py @ ...`:
verifiers' own entry point, started by our launcher); vf-eval starts one laboratory process per rollout
(`.venv/bin/python -m physim2_env.lab_tools`: it simulates the hidden world and answers the agent's requests),
many short `docker` commands, and through the laboratory's runtime two kinds of short helpers: a Python one-liner
that waits for the laboratory's port (`.venv/bin/python -c ...`, up to 9 minutes if the port never opens) and
`tail` [vf:mcp/launch.py:62-72, 279-287, 355]. `tools/prove.py` and `tools/check_probe.py` also start two helpers
of our own: `tools/make_instances.py` (seconds) and, once, `tools/build_reference.py`, which runs round 5's
reference agent on the Mac to build the reference submission C (our code, no submitted code; the hidden
parameters reach it through a file of mode 0600 in the store, never on a command line).
Every detached command also leaves one waiting shell, a copy of the shell that issued it, which does nothing but
wait for its tool and then write the `EXIT` line; it ends with the tool.
No predictor, no hostile test agent and no model-written code runs on the Mac: they run in containers only.

**What reaches those processes from your session (the environment).** A tool copies nine names from the
environment it was started in, if they are set: `PATH`, `HOME`, `TMPDIR`, `USER`, `LOGNAME`, `LANG`, `LC_ALL`,
`LC_CTYPE`, `TZ`, and the `VF_RUN_ID` of its command. Everything else that vf-eval, the `docker` client and the
laboratory see is set by the tool (`PRIME_RUNS_MODE=disabled`, `PYTHONPATH=<study folder>`, thread and JAX
settings, in step 2b one made-up canary value named `HF_TOKEN`) [`tools/vfrun.py`, `child_env`]. No `DOCKER_*`,
`MCP_*`, `PHYSIM2_*`, `PYTHON*` or credential of the session can get through, and a tool refuses to start
(`refused: the environment of this command holds ...`) when the session has one of the names step 0 looks for.
`PATH` and `HOME` are taken as they are: that is why step 0 has you check, yourself, which `docker` context
answers, and why a tool refuses to start unless that context names a Unix socket of this machine.

**What is signalled or killed on the Mac.** Every target below is a process that the pilot itself started; no
signal is sent by name, by user or to "all processes".

| who sends | to what (who can be the target) | which signal, when |
|---|---|---|
| verifiers, in vf-eval | the laboratory process it started: its process group, which holds that one process [vf:runtimes/subprocess.py:45-53, 197-221, 225-228] | SIGTERM at the end of every rollout and when vf-eval stops; SIGKILL if it has not ended 5 s later |
| verifiers, in vf-eval | the `docker` client command that is under way: the process group of that one client, which holds the client and what it started (a credential helper, a CLI plug-in) [vf:runtimes/container.py:44-65] | SIGKILL, **whenever the call is cut: at every stop of vf-eval** (SIGTERM, Ctrl-C, a failed rollout that cancels the others) and at a time limit inside verifiers. A killed client does not undo what Docker already did: a helper container it started ends by itself and removes itself (`--rm`) |
| verifiers, in vf-eval | the helper it started through the laboratory's runtime: the port probe `python -c ...` or `tail`, its own process group [vf:runtimes/subprocess.py:103-129] | SIGKILL, if the call is cut while the helper runs (same occasions as the row above) |
| verifiers, in vf-eval | `git rev-parse`, started once to find its own version [vf:utils/version.py:23-31] | SIGKILL by Python if it has not answered in 5 s |
| `tools/vfrun.py` | the vf-eval it started (one process) [`stop_child`, `run_child`] | ONE SIGTERM (vf-eval then removes its containers and stops its laboratory); SIGKILL only if it is still there 120 s later. When: a run exceeds its time limit (an hour in 2a and 2b, 90 minutes in 2c), the disk watchdog trips, or the tool itself is stopped or fails. After any of these the tool ends with a status other than 0 (97 disk, 98 stopped or killed, 130 after a stop by signal) and starts nothing further |
| `tools/vfrun.py` | the helper it started, `tools/make_instances.py` or `tools/build_reference.py` (one process) [`run_helper`] | SIGTERM, SIGKILL 20 s later, only when the tool is told to stop while the helper runs |
| `tools/vfrun.py`, `tools/check_probe.py`, `tools/prove.py` | their own `docker context inspect`, `docker info`, `docker run --rm` (the control container of 2b) and `docker version` clients | SIGKILL by Python if the client has not answered in 60 s (120 s for the control) |
| Python, in a tool | the tool itself | after a stop by SIGTERM the tool ends itself with the interrupt signal: the log shows a traceback ending `KeyboardInterrupt` and `EXIT 130` |
| the kernel (Linux only) | the laboratory process, when the vf-eval that started it dies [vf:mcp/server.py:112-118] | SIGKILL. **Not on macOS:** there a laboratory whose vf-eval was killed outright stays until it is stopped ("If a run was interrupted", point 4) |
| you | ONE process of the pilot: the pid that the status command printed, after the stop command has compared that pid's command line with the eight exact beginnings of the pilot's own programs; it sends nothing otherwise | SIGTERM, only in "If a run was interrupted" |

Inside containers the driver kills the predictor's processes, verifiers signals a harness process through
`docker exec`, and one test agent of step 2b (`harness-killall`) runs `kill -9 -1` in its own box: the box is a
container that verifiers created for it without any Mac folder mounted.

**What is deleted on the Mac.**

| who | what | where |
|---|---|---|
| `uv sync` (step 1) | an existing `.venv` of the study folder would be replaced; the dry run before it must say `Would create`, not `Would replace` | study folder |
| step 1 | nothing: `docker/extra-ca.crt` is created empty only if it does not exist (a file with content, or a link, is a stop) | study folder |
| `tools/make_instances.py` | `store/<instance>/hidden/examples.npz`, a file it wrote a moment before | store |
| `tools/vfrun.py` | the run folder of an EARLIER call with the same name, only if it holds nothing but vf-eval's own files; happens only when a tool is started again | scratch |
| `tools/prove.py` | `store/<instance>/work/reference_<policy>` for box checks of policies other than C: not reached with the arguments below | store |
| the package (`bundle.py`, `access.py`) and Python's `tempfile` | temporary folders the same process created (`physim2-bundle-*`, `physim2-io-*` under `$TMPDIR`) | temp |
| verifiers | the laboratory's working folder `~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>`, which it created; its `logs/latest` link in a run folder; at the first rollout an empty temporary folder `vf-network-*` that it made for the build of its helper image | home, scratch, temp |
| verifiers | the containers it created, `vf-<32 hex>`, by `docker rm --force <that name>`; helper containers started with `--rm` | Docker |
| `docker run --rm` (step 1, and the control of step 2b) | the test container it just started | Docker |
| you, "If a run was interrupted" | a leftover container of this pilot, by its exact name and after its label was read back; the two pilot folders | Docker, home |
| you, step 4 | the two pilot folders, after their results were copied out | home |
| the disk watchdog | nothing, ever | |

**What is written and left on the Mac.** uv's own Python 3.12, if uv has none yet: the DRY RUN of step 1
already downloads it (`~/.local/share/uv/python`; 104 MB on disk in the cloud rehearsal); `.venv` in the study
folder (about 1 GB with jax) and uv's cache (`~/.cache/uv`); `docker/extra-ca.crt` (empty; git ignores it);
the folder `$HOME/physim2-pilot-20261110` (mode 0700) with `store` and `scratch`, and in step 4
`$HOME/physim2-pilot-20261110-results`; in the store, next to the hidden instance, one more file with the hidden
parameters, `store/<instance>/work/reference_C.theta.json` (mode 0600; it goes with the store); after a run was
stopped, a small `<run name>.stopped.json` beside the run folder (the reason, in words and numbers);
`~/.cache/verifiers/` (created by verifiers); one small file `/tmp/vf-port-<hex>` per rollout, which verifiers
never removes (leave them; do not delete by pattern); only after a vf-eval was killed outright, two small folders
nobody removes: the laboratory's working folder `~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>` (one log
file) and `$TMPDIR/physim2-io-<random>` (one socket). In Docker Desktop's disk image: the images `physim2-ring:1`
(about 560 MB), `python:3.12-slim`, and `localhost/verifiers-network:1` with `alpine:3.22`, which verifiers builds
itself at the first rollout; and **the build cache of those two builds** (BuildKit; `docker system df` shows it
as "Build Cache"), which nothing in the pilot removes. Docker Desktop's disk image is a file on the Mac that grows
with all of this and does not shrink by itself.

**What listens on the Mac.** All of it for the minutes a run lasts, all on the loopback address or in a folder
of your user.

| what | where | who can connect, and what it needs |
|---|---|---|
| verifiers' interception server, one per vf-eval [vf:interception/server.py:346, 444-447] | TCP 127.0.0.1, a port the system chooses | any process on the Mac and, on Docker Desktop, any container through `host.docker.internal`. Every route needs a per-rollout secret that only vf-eval and the processes it starts hold. Behind it stands the model client: in steps 0 to 2 that is a stand-in without any key (see below) |
| verifiers' proxy, one per box [vf:runtimes/docker/__init__.py:311-321; vf:runtimes/docker/egress.py:160-167, 213-231] | TCP 127.0.0.1, a port the system chooses | the same; it answers only to its own password (given to that box) or to an address that carries a secret of that box |
| the published port of each box [vf:runtimes/docker/__init__.py:196] | TCP 127.0.0.1, a port Docker chooses, forwarded to port 8000 in the box | processes on the Mac; nothing of the pilot listens on port 8000 in a box |
| the laboratory, one per rollout [vf:mcp/server.py:278-283; `physim2_env/lab_tools.py`, last lines: always 127.0.0.1, whatever `MCP_HOST` says] | TCP 127.0.0.1, a port the system chooses | **no secret.** Any process on the Mac and, on Docker Desktop, any running container whose network is not cut can talk to the laboratory through `host.docker.internal:<port>` and spend the rollout's budget. The pilot's own boxes are cut and reach it through the proxy only. Hence the rule of step 2: no other container runs while step 2 runs. A bearer for the laboratory is not built yet; it is a condition for step 3 |
| the task controller, one per rollout [`physim2_env/access.py`, `BoxAccess`] | a Unix socket `$TMPDIR/physim2-io-<random>/io.sock`, in a folder only your user can enter | your user's processes; every request needs a 256-bit secret |
| `tools/check_probe.py`, while it runs | TCP 127.0.0.1, a port the system chooses | anything that can reach the Mac's loopback; it accepts a connection, records the peer and closes it |

On Linux verifiers also makes a Unix socket in a temporary folder that it mounts into a helper container; off
Linux it does not [vf:runtimes/docker/__init__.py:318-321, 348-408].

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
The file on this Mac stays where it is; do not move or open it.

**Network.** `uv sync` downloads from PyPI, one wheel from github.com and, if uv has no Python 3.12 of its own,
that Python from github.com; `docker build` and the first rollout pull `python:3.12-slim` and `alpine:3.22` and
install numpy, scipy and jax from PyPI. Nothing is uploaded: every run is made with `push = false` and
`PRIME_RUNS_MODE=disabled`, and no model is called.

## C. By hand, before the session's first command (the lead)

| check | command | expected |
|---|---|---|
| hold lifted | the coordinator's message | GO for steps 0 to 2, with a 40-character commit hash |
| where the checkout is | directly under your home folder, for example `~/physim`; not under `~/Documents` or `~/Desktop` | those two are synced to iCloud on this Mac: a synced `.venv` of 1 GB and a synced store are not wanted |
| right code | in the study folder: `git fetch origin claude/fisim-agent-world-research-hepmlz`, then `git checkout --detach <the hash of the GO message>`; `git rev-parse HEAD`; `git status --short` | that hash, all 40 characters; nothing listed |
| right text | the first lines of `RUNBOOK_MAC.md` in the study folder | they begin `**GO for steps 0 to 2.**`, not ON HOLD |
| user | `id -u`; `echo "$HOME"`; `ls "$HOME/physim2-pilot-20261110" "$HOME/physim2-pilot-20261110-results"` | not 0; your own home; no such folders. A current backup of the Mac exists |
| machine | `uname -m` | `arm64` |
| folder | `pwd -P` in the study folder | ends in `research/alife/vecworld/program/round6/vfport`. **This output, character for character, is the path you give the session** (step 0 compares it) |
| path is plain | `pwd -P \| LC_ALL=C grep -E '^[A-Za-z0-9/._-]+$'` in the study folder | it prints the path again. If it prints nothing, the path holds a space or another character outside letters, digits and `/ . _ -`: move the checkout first |
| the session | started in the study folder; given that path and the hash of the GO message | no subagents; one command per call |
| tools | `command -v uv docker`; `uv --version`; `docker context show`; `docker info` | uv 0.11 or later (it must know `--managed-python`); Docker Desktop's own client and context `desktop-linux`; it answers. If uv is missing or older: stop and ask, do not install it from inside the session |
| variables | `env \| cut -d= -f1 \| grep -E '^(PHYSIM2_\|UV_\|VIRTUAL_ENV\|PYTHON(PATH\|HOME)\|DOCKER_\|BUILDX_\|VF_\|MCP_HOST\|MCP_PORT\|PRIME_RUNS_MODE)'` | nothing. This is your terminal; the session checks its own environment in step 0 and the tools check theirs |
| other runs | `docker ps -a --filter label=verifiers.run`; `docker ps`; `docker images physim2-ring` | nothing, **and no container of anything else is running** while step 2 runs (see section B, the laboratory). Save the output of `docker ps -a`, `docker images` and `docker system df` as the baseline |
| room | `df -Pk "$HOME"`; Docker Desktop: Settings, Resources | at least 8 GiB free on the Mac (the pilot's floor; steps 1 and 2 use about 3 GiB of it, half in the study folder and uv's cache, half in Docker's disk image); 4 CPUs. Steps 0 to 2 do not ask you to change Docker Desktop's virtual disk limit: nothing untrusted runs, the boxes are small, and the pilot stops itself at the floor. **Step 3 does need your decision about that limit** (see step 3) |
| power | plugged in; no sleep for the 45 minutes of steps 1 and 2 | a sleep is an interruption |
| network | VPN, TLS-intercepting proxy | none (the image build needs a direct connection) |
| credentials | nothing to do | `~/.prime/config.json` may stay; steps 0 to 2 never open it and need no key in the session |
| during the pilot | the pilot folders in `$HOME` | not opened in Finder: a `.DS_Store` makes step 4's `rmdir` fail after its deletes (a stop, nothing lost) |

## 0. Verify the code, the session and the disk (seconds)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && git rev-parse HEAD && pwd -P | grep -Fx "/ABSOLUTE/PATH/TO/vfport" && git status --porcelain -- . ../../round5/agentenv ../../../vw1 && echo "TREE-LISTED"
```

Expected: three lines. The first is the 40-character hash that the lead gave you from the coordinator's GO
message: compare all 40 characters. The second is the path of the study folder, the same text you put into the
command (if it is missing, the path you were given is not the folder's real path: stop). The third is
`TREE-LISTED`. A line between the second and the third names a changed or added file: stop. No `TREE-LISTED`:
stop.

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
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && env | cut -d= -f1 | awk '/^(PHYSIM2_|UV_|VIRTUAL_ENV|PYTHON(PATH|HOME)|DOCKER_|BUILDX_|VF_|MCP_HOST|MCP_PORT|PRIME_RUNS_MODE)/ { bad++ ; print "FOUND " $0 } END { print NR " names, " bad + 0 " refused" }' && docker context show && docker context inspect --format '{{.Endpoints.docker.Host}}'
```

Expected: three lines. `<n> names, 0 refused`, where n is the number of variables of your session (some tens;
`0 names` means the check did not run: stop). Then `desktop-linux`. Then a Unix socket in the home folder,
`unix:///Users/<you>/.docker/run/docker.sock`. A line `FOUND <name>` before the first line (names only are
printed, never values), another context, or an address that is not a `unix://` socket under your home folder
(`tcp://`, `ssh://`, another machine): **stop and report**. Do not unset anything and do not switch the context:
that is the lead's to decide.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}}' && echo "CONTAINERS-LISTED" && docker images -q physim2-ring:1 && echo "IMAGES-LISTED" && test ! -e "$HOME/physim2-pilot-20261110" && test ! -L "$HOME/physim2-pilot-20261110" && test ! -e "$HOME/physim2-pilot-20261110-results" && test ! -L "$HOME/physim2-pilot-20261110-results" && test ! -e .venv && test ! -L .venv && echo "NO-PILOT-FOLDERS"
```

Expected: four lines. Docker's version, `CONTAINERS-LISTED` (no container of this pilot: a name before it is a
stop), `IMAGES-LISTED` (no image `physim2-ring:1` yet: an image id before it is a stop), `NO-PILOT-FOLDERS`
(neither pilot folder nor a `.venv` exists, not even as a link). A missing line: stop.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && df -Pk "$HOME" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) print "DISK-OK " int(free / 1048576) " GiB free" ; else print "refused: " int(free / 1048576) " GiB free on the file system of the home folder, the floor is 8 GiB" }'
```

Expected: `DISK-OK <n> GiB free`, n at least 8. A line that begins `refused:` (rule 7): stop and report; delete
nothing.

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
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && mkdir -m 700 "$HOME/physim2-pilot-20261110" && mkdir "$HOME/physim2-pilot-20261110/scratch" && test ! -L docker/extra-ca.crt && (test -e docker/extra-ca.crt || : > docker/extra-ca.crt) && wc -c docker/extra-ca.crt
```

Expected: `0 docker/extra-ca.crt` (macOS pads the number with spaces). `mkdir` fails if a pilot folder exists
already, and nothing after it runs: stop. A number other than 0 means somebody's certificate file is there:
stop.

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
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && df -Pk "$HOME" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) exit 0 ; print "refused: under 8 GiB free on the file system of the home folder" ; exit 1 }' && docker info --format '{{.ServerVersion}}' && { ( nohup docker build -f docker/Dockerfile.ring -t physim2-ring:1 docker/ > "$HOME/physim2-pilot-20261110/scratch/build.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/build.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once. Status (repeat until the log's last line is `EXIT 0`; any other
`EXIT` line: stop; no `EXIT` line after 30 minutes: stop and report, signal nothing):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && tail -n 2 "$HOME/physim2-pilot-20261110/scratch/build.log"
```

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker run --rm --network none --label verifiers.run=physim2-pilot-20261110 physim2-ring:1 python -c "import numpy, scipy, jax; print(numpy.__version__, scipy.__version__, jax.__version__)"
```

Expected: `2.5.4 1.18.1 0.12.0.1`. This is the ONE image of every box. Do not build
`docker/Dockerfile.network`: verifiers builds its own helper image at the first rollout.

The hidden side lives in a store OUTSIDE the repository. Make one fresh ring instance (a new secret and a new
hidden theta are drawn now; about 15 s):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/make_instances.py --store "$HOME/physim2-pilot-20261110/store" --world ring --config smoke_ring --n 1 --prefix mac-ring
```

Expected: one JSON line with `"instance_id": "mac-ring-w0"`, `"n_items": 64`, `"R": 16` and a
`secret_commitment` (public).

## 2. Scripted smoke test on Docker ($0, no model, no upload; about 35 minutes)

The tools start verifiers' vf-eval (`physim2-env`, `--env.id isolated-verifier`) with the Docker runtime and the
scripted harness; they set `push = false`, `PRIME_RUNS_MODE=disabled` and a stand-in model client, build the
environment of everything they start from the allow-list of section B, and keep the disk floor of rule 7.
`VF_RUN_ID=physim2-pilot-20261110` is on every run command: verifiers writes it on every container it creates as
the label `verifiers.run`, and the tools refuse to start without it. The store path and the disk floor are on
every command; nothing depends on a variable set earlier.

**Before 2a: nothing else runs in Docker.**

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker ps --format '{{.Names}} {{.Image}}' && echo "RUNNING-LISTED"
```

Expected: one line, `RUNNING-LISTED`. A line before it is a running container of somebody (name and image):
**stop and report**; do not stop that container. (On Docker Desktop a running container can reach the
laboratory's port on the Mac, section B; whether to stop it is the lead's decision.)

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

### 2a. One world, three policies, then C once more with one box per exam item (about 10 minutes)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/prove.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/proof" --worlds 1 --prefix mac-ring --policies D,P0,C --box-check C --no-cross-check --disk-floor-gib 8 --out "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" > "$HOME/physim2-pilot-20261110/scratch/prove.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/prove.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once (the tool runs on, detached). Then use the status command, the
first time right away: the "must show" rule.

Expected in `prove.log` when it is finished: lines `D: [..]`, `P0: [..]`, `C: [..]` (one skill per world), a line
`C (one box per item, world 0): ..`, then two JSON lines, the table on the K-to-C scale, for example (cloud
rehearsal) `{"O": 1.0998, "K": 0.0, "D": 0.5175, "P0": 0.8956, "C": 1.0}`, and a line that begins `{"sigma":`, and
last `EXIT 0`. The numbers differ on the Mac: the hidden world is new. Then:

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

What must hold: `all_graded True all_ok True failed_items 0`; ticks `{'D': 392, 'P0': 0, 'C': 0}`; every
`layers` is `{'rlimits': True, 'uid': <a number from 20000 to 59999>, 'cleanup': True}`; `box True 64 0 <seconds
per item box>` (2.7 s in the cloud container: report the Mac's number, it is the price of the default grading
mode); in the table D below P0 below C, O above C (ordering, not values). Anything else: stop and report.

### 2b. The boundary checks and the probes, on their own small instance (37 short rollouts; about 20 minutes)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/check_probe.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/probe" --disk-floor-gib 8 --out "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" > "$HOME/physim2-pilot-20261110/scratch/probe.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/probe.log" ) > /dev/null 2>&1 < /dev/null & }
```

Then the status command and the "must show" rule. When `probe.log` ends with `EXIT 0`, the line before it is one
JSON object. Expected on the Mac:

- `"failed_round5": []`
- `"failed_new": ["b_lab_process_dropped_it_after_loading"]`. **This one failure is expected on macOS** and only
  there: the check reads the laboratory process's environment block in `/proc`, which macOS does not have. (On
  Linux the list is empty.)

Any other name in either list: stop and report the two lists. Several checks were measured on Linux only (the
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

Policy D on `mac-ring-w0` from `configs/scripted_ring.toml`, through the command form of `tools/vfrun.py`: the
way step 3 will start its rollout. It can run once: a second run of the same agent on the same instance is
refused.

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
`"2_item_isolation": "box"`, `"3_lab"."ticks_used": 392`, `"4_submission_source": "agent_submission"`,
`"5_validation_ok": true`, `"5_n_items": 64`, `"5_n_failed": 0`, `"5_item_boxes": 64`,
`"5_infrastructure_failed_items": 0`, and `"total_hits": 0` under `6_hidden_values_in_the_run_folder`.

After step 2: report, and stop. Step 3 needs the lead.

## If a run was interrupted

**This section is for step 2 only** (step 3 uses its points 1 to 5 and 7, as step 3 says). A cut or an
unexpected output in step 0, 1 or 4: run nothing more, report, stop. **Use this section once.** At a second
interruption do points 1 to 5, then stop and report: no reset, no new start. If you cannot tell whether the
section was used before in this pilot (for example after a restart of the session), treat the interruption as
the second one.

Use it when a command of step 2 did not end with `EXIT 0`: the Mac slept, Docker Desktop stopped, a command was
cut, the session was restarted, you were told to stop, a tool ended with `EXIT 97` (the disk floor: points 1 to 5,
then stop and report, whatever the count) or `EXIT 98` (the tool had to stop its vf-eval, or vf-eval was killed).
Do exactly this, in this order, and nothing else. In particular do not start the step again before the end of
this section.

1. **What is still there?** Run the status command of step 2. It lists the pilot's processes and the pilot's
   containers. Nothing of anybody else can be in either list: the processes are the ones whose command line
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
6. **Delete the two pilot folders and start again from the instance** (first interruption only, and never after
   `EXIT 97`). A cut rollout has spent its laboratory budget and its instance cannot be opened again by the same
   agent, so the store is not reusable:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test ! -L "$HOME/physim2-pilot-20261110" && test ! -L "$HOME/physim2-pilot-20261110/store" && test ! -L "$HOME/physim2-pilot-20261110/scratch" && test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch" && mkdir "$HOME/physim2-pilot-20261110/scratch" && echo "pilot folders reset"
   ```

   Expected: `pilot folders reset`. If it prints nothing: stop and report (a pilot folder that is a link is one
   reason; nothing was deleted then). Then continue from the `make_instances` command of step 1, and run step 2
   from its first command. The image and `.venv` stay; the logs of step 1 (`sync.log`, `build.log`) went with the
   scratch folder.
7. Say in the report that a run was interrupted, at which command, and what the status command listed. If
   point 3 or 4 was needed, two small folders of the killed vf-eval stay on the Mac and nothing removes them: the
   laboratory's working folder `~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>` (one log file) and
   `$TMPDIR/physim2-io-<random>` (one socket). Name them in the report and leave them: do not delete by pattern.

## 3. ONE rollout of a cheap model, stock harness (SEPARATE HOLD)

**NO-GO until steps 0 to 2 have passed on this Mac and the lead has read their report.** This is the only step
in which an untrusted model acts: it is root in a container for up to an hour, and Docker Desktop's virtual
machine is the only wall between it and the Mac; that wall was not tested by this study. No command of this step
has run anywhere, the dry run included; round 3 changed how they start (through `tools/vfrun.py`) and did not
rehearse them.

Open before this step can be offered, in addition to the report of steps 0 to 2:

- **The lead's decision about Docker Desktop's disk.** A model can fill its box. Docker Desktop's disk image is a
  file on the Mac that grows up to the limit set under Settings, Resources; on this Mac that limit is far above
  the free space. The pilot's watchdog stops the rollout when the Mac has less than 8 GiB free and deletes
  nothing; it does not give the space back (the image file does not shrink by itself). Lowering the limit below
  the Mac's free space is the sure wall, and it can cost the lead other Docker data: the lead decides, and says
  so in the go message.
- **A bearer for the laboratory.** In step 2 the rule "no other container runs" stands in for it. In step 3 the
  model itself is in a container; its box is cut by verifiers' network policy (measured on Linux, and on the Mac
  by step 2b), and that cut is then the only thing between any container and the laboratory's open port. The
  bearer is to be built and audited before step 3, or the lead accepts this in the go message.
- **The price**, read by the lead from Prime's Models API and given in the go message (below).

Model `qwen/qwen3.5-35b-a3b`, the stock `bash` harness of verifiers, the ring smoke exam, one hidden world, one
hour. `configs/qwen_ring_bash.toml` sets `push = false`, no retries at any level, `max_turns = 40`,
`max_total_tokens = 1500000`, `max_output_tokens = 60000`, and nothing else may be changed.

Model credentials, in this step only: the start command carries `--model-credentials prime`. With it the tool
passes `PRIME_API_KEY` and `PRIME_TEAM_ID` of the session on to vf-eval (and nothing else of the session, as in
step 2), and verifiers may read `~/.prime/config.json`. The laboratory process gets neither.

The lead's go is a file, which the lead creates by hand and the session never creates: an empty file
`$HOME/physim2-pilot-20261110/scratch/LEAD-GO-STEP3`. Neither command below starts anything without it (it then
prints nothing: stop).

Free, calls no model and loads no credential (vf-eval resolves the config, writes it and exits):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f "$HOME/physim2-pilot-20261110/scratch/LEAD-GO-STEP3" && VF_RUN_ID=physim2-pilot-20261110 "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/vfrun.py --config configs/qwen_ring_bash.toml --run-name qwen-dry --out-dir "$HOME/physim2-pilot-20261110/scratch/qwen-dry" --store "$HOME/physim2-pilot-20261110/store" --dry-run > "$HOME/physim2-pilot-20261110/scratch/qwen-dry.log" 2>&1 && echo "DRY-RUN-OK"
```

Expected: `DRY-RUN-OK`.

---

**STOP. THE NEXT COMMAND SPENDS MONEY. Do not run it without the lead's explicit "go" for this command, given
after the smoke test's report.**

Price: the token caps are checked before each model call, so the spend is bounded by 1.5 M tokens in total, of
which at most 60 k are output, plus one request: at most `1.5 x p_in + 0.06 x p_out` dollars for prices p_in and
p_out per million tokens. The price of this model was not available in the cloud container; the lead reads it
from Prime's Models API and states p_in, p_out and the bound in the go message (the lead does not edit this
file). (As an illustration only: at $0.20 in and $0.60 out the bound is $0.34.) The caps count the usage the
provider reports; if it reports none they do not bind, and the bound is then 40 requests and one hour.

It can be run ONCE: `single_use` refuses a second rollout of this model and harness on `mac-ring-w0`.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f "$HOME/physim2-pilot-20261110/scratch/LEAD-GO-STEP3" && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/vfrun.py --config configs/qwen_ring_bash.toml --run-name qwen --out-dir "$HOME/physim2-pilot-20261110/scratch/qwen" --store "$HOME/physim2-pilot-20261110/store" --disk-floor-gib 8 --model-credentials prime > "$HOME/physim2-pilot-20261110/scratch/qwen.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/qwen.log" ) > /dev/null 2>&1 < /dev/null & }
```

---

While it runs (up to an hour, then about 3 minutes of grading), ask for its state with this command only:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && { tail -n 1 "$HOME/physim2-pilot-20261110/scratch/qwen.log" | cut -c 1-12 ; echo "containers:" ; docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' ; echo "processes:" ; ps axww -o pid= -o command= | awk -v p="/ABSOLUTE/PATH/TO/vfport" 'BEGIN { py = p "/.venv/bin/python " } { line = $0 ; sub(/^ *[0-9]+ /, "", line) ; if (index(line, py) != 1) next ; r = substr(line, length(py) + 1) ; k = "OTHER" ; if (index(r, "-B tools/prove.py ") == 1 || index(r, "-B tools/check_probe.py ") == 1 || index(r, "-B tools/vfrun.py ") == 1) k = "TOOL" ; else if (index(r, "-B " p "/tools/vfeval.py @ ") == 1) k = "VF-EVAL" ; else if (index(r, "-m physim2_env.lab_tools") == 1) k = "LAB" ; else if (index(r, "-B " p "/tools/make_instances.py ") == 1 || index(r, "-B tools/make_instances.py ") == 1 || index(r, "-B " p "/tools/build_reference.py ") == 1) k = "HELPER" ; else if (index(r, "-c") == 1) k = "PROBE" ; print k " " substr($0, 1, 160) }' ; echo "free:" ; df -Pk "$HOME" | awk 'NR == 2 { print int($4 / 1048576) " GiB" }' ; echo "status done" ; }
```

**Never display `qwen.log`, `traces.jsonl` or anything under `scratch/qwen/`**: they hold what the model wrote,
and you have a shell on this Mac. (`cut -c 1-12` shows at most the word `EXIT` and a number.) When the first
line reads `EXIT 0`, read the run through the report tool:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/run_report.py --store "$HOME/physim2-pilot-20261110/store" --run-dir "$HOME/physim2-pilot-20261110/scratch/qwen/qwen"
```

Report its output as it is. How to read it:

1. `1_ok` true and `1_reward_present` true. If the reward is missing the rollout is ungraded (for example the
   model killed its own harness): run
   `cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/settle.py --store "$HOME/physim2-pilot-20261110/store" --run-dir "$HOME/physim2-pilot-20261110/scratch/qwen/qwen"`,
   which records it as K. Do NOT run the rollout again.
2. Both `network_restricted` true; `2_single_use` true; `2_item_isolation` is `box`.
3. `3_lab`: `ticks_used` at most 400, `infrastructure_errors` 0. `3_tool_calls_by_name` counts the model's tool
   calls by name (names outside a fixed list are counted as `(other)`): whether it reached the laboratory through
   the tool, from its own Python, or both.
4. `4_submission_source` is `agent_submission` (its submit was accepted) or `final_collection`;
   `4_stop_condition` `frozen` means the task's stop hook ended the rollout right after the submit (that hook has
   never fired before this rollout).
5. `5_validation_ok`, `5_n_failed`, `5_layers` as in step 2, `5_isolation` `box`, `5_item_boxes` 64,
   `5_infrastructure_failed_items` 0, `5_skill_vs_O` equal to the reward.
6. `6_hidden_values_in_the_run_folder`: `total_hits` 0 (the tool counts, without printing them, the secret and
   the first ten characters of each hidden parameter in every file of the run folder).
7. `7_num_input_tokens` and `7_num_output_tokens` against the caps; `7_wall_s`.

If the run is cut, or ends with `EXIT 97` or `EXIT 98`: "If a run was interrupted", points 1 to 5 and 7; do not
delete the folders (the references of step 2 are in them), do not run the rollout again; settle it as in 1.

**The trace of this rollout, only if the lead asks for it.** Step 4 deletes every run folder. The lead decided
that pilot traces may be uploaded where that helps (never for a sealed exam). If the lead wants this one, copy
the run folder out BEFORE step 4, unread, and only when the report tool counts no hidden value in it:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/run_report.py --store "$HOME/physim2-pilot-20261110/store" --run-dir "$HOME/physim2-pilot-20261110/scratch/qwen/qwen" | grep -c '"total_hits": 0' && mkdir "$HOME/physim2-pilot-20261110-trace" && cp -R "$HOME/physim2-pilot-20261110/scratch/qwen/qwen" "$HOME/physim2-pilot-20261110-trace/" && ls "$HOME/physim2-pilot-20261110-trace"
```

Expected: `1`, then `qwen`. If it prints `0` and nothing else, the folder holds a hidden value or has no report:
nothing was copied; stop and report. Do not open the copy. It holds what the model wrote and it names the
operator's account; what happens to it, an upload included, is the lead's own act. The session uploads nothing.

## 4. After the pilot

The store holds theta and the secret of a pilot that must never be reused. Run this step only when the lead says
the pilot is over: it deletes the store that step 3 would need. First run the status command of step 2: nothing
may be listed. Then copy the results out and remove exactly the two folders, in ONE command, so that nothing is
deleted unless every check and every copy before it succeeded:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test ! -L "$HOME/physim2-pilot-20261110" && test ! -L "$HOME/physim2-pilot-20261110/store" && test ! -L "$HOME/physim2-pilot-20261110/scratch" && test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && test -f "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" && test -f "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" && mkdir "$HOME/physim2-pilot-20261110-results" && cp "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" "$HOME/physim2-pilot-20261110/scratch/proof_mac_items.npz" "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" "$HOME/physim2-pilot-20261110/scratch/prove.log" "$HOME/physim2-pilot-20261110/scratch/probe.log" "$HOME/physim2-pilot-20261110-results/" && test -s "$HOME/physim2-pilot-20261110-results/proof_mac.json" && test -s "$HOME/physim2-pilot-20261110-results/probe_mac.json" && rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch" && rmdir "$HOME/physim2-pilot-20261110" && ls "$HOME/physim2-pilot-20261110-results"
```

Expected: the five file names. If it prints nothing: stop and report. The copied files
hold scores, counters and commitments only (`PILOT_NEVER_REUSE_AS_EXAM`); the run folders with their traces are
deleted with the scratch folder (a trace names the operator's account), and after step 3 the output of
`tools/run_report.py` is what leaves the Mac, with the trace folder only if the lead asked for it.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' && echo "CONTAINERS-LISTED" && docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}' && docker system df
```

Expected: `CONTAINERS-LISTED` with no line before it (no container of the pilot), then the images, then Docker's
own table of what its disk holds (images, containers, volumes, build cache). Compare with the baseline of the
by-hand checks: the pilot added `physim2-ring:1`, `localhost/verifiers-network:1` and no container;
`python:3.12-slim` and `alpine:3.22` may or may not be listed (Docker Desktop does not always list the base
images of a build): that is not a deviation. Another new image, or a container of the pilot, is. The pilot also
added build cache (the "Build Cache" row; several hundred megabytes). **Remove none of it yourself.** The helper
image `localhost/verifiers-network:1` is shared with other verifiers work on this Mac and is not this pilot's to
remove; `physim2-ring:1` may be removed by the lead, by hand, when no further run is planned (`docker rmi
physim2-ring:1`); the build cache can only be removed together with that of every other project (`docker builder
prune`), which is the lead's decision and never the session's. The `.venv` stays until the lead removes the
checkout. Left on the Mac besides: uv's cache and Python, `~/.cache/verifiers`, `/tmp/vf-port-*`, the results
folder.

## What the cloud rehearsal could not cover

- macOS and Docker Desktop: nothing. Inferred, not seen: that containers there carry `/.dockerenv` and Docker's
  usual mount table (if not, staging stops with `the box is not recognised as a disposable box` and names the
  mount or the missing sign; nothing is damaged; report it); how `uv` behaves and that the Python it manages
  shows `.venv/bin/python` as its command line (step 1 checks it); that `ps`, `shasum`, `df -Pk`, `tail` and the
  system's `awk` print and accept there what they do on Linux (the two awk programs were run with mawk only; they
  use `index`, `substr`, `length` and `sub`, nothing newer); that `docker context show` says `desktop-linux` and
  the context's address is a socket in the home folder; that the session's shell (zsh) leaves the same waiting
  shell as `sh` and `bash` did; how a Claude session on the Mac ends a command at its limit; that a detached
  command survives the end of the call that started it; that a laboratory outlives a killed vf-eval there.
- The image build of step 1: the cloud machine sits behind a TLS-intercepting proxy and already had the shared
  image `physim2-ring:1`, at which step 0 says stop; the rehearsals went on with that image and did not run the
  build command or its status command. Its disk check was run in the two other commands that carry it.
- The by-hand checks and three expectations of step 0: the cloud session is root, on x86_64, behind a proxy;
  its Docker context is `default` on `unix:///var/run/docker.sock`; the home folder of the rehearsal was a folder
  of its scratch (given to every command as the variable `HOME`, so the commands ran byte for byte), with uv's
  cache and uv's own Python pointed elsewhere for the two uv commands; the machine has 2 GiB free for everyone,
  so `8` was replaced by a lower floor in the commands that carry it, except where the refusal itself was
  rehearsed.
- "If a run was interrupted": points 1, 2, 3, 5 and 6 were rehearsed, each as part of a first interruption (a stop
  by the stop command, a vf-eval killed outright, a stop by the disk watchdog). Point 4 did not arise: on Linux
  the laboratory dies with its vf-eval, and no helper happened to be running at a stop; its stop command is the
  one of point 2. The rule for a second interruption (points 1 to 5, then stop), the stop of a vf-eval by its own
  pid and the 60-minute bound of the "must show" rule were not exercised.
- Step 3, its file gate, its dry run and the copy of its trace: never run. Its two start commands are new in
  round 3 and were not issued; `tools/vfrun.py --model-credentials prime` was run with a stand-in for vf-eval in
  a throwaway container only (`results/round3_checks.json`).
