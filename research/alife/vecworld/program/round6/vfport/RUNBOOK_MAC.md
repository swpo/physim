# RUNBOOK for the Mac session: PhySim v2 on verifiers
<!-- HOLD-BEGIN: a verdict edits the text between this line and HOLD-END, and nothing else in this file -->
**ON HOLD. Run nothing from this file.** The host-safety audit's round-1 verdict was NO-GO, narrowly: the code
passed, the stop-and-recover text of this file did not (`HOST_SAFETY_AUDIT.md`, "Re-audit, round 1"). This file
was changed to meet the seven remaining changes of that verdict; these changes have not been re-audited. The
hold on steps 0 to 2 is lifted only by a verdict that says GO: it replaces this notice by one that begins
`**GO for steps 0 to 2.**`, and the coordinator's message then gives the 40-character hash of the commit that
holds the replaced notice. Step 3 (a paid model rollout) has a second hold of its own and stays NO-GO until
steps 0 to 2 have passed on the Mac and been reported.
<!-- HOLD-END -->

<!-- PIN-BEGIN -->
**Pin.** This file names no commit to check out: a commit cannot hold its own hash. The commit is the
40-character hash in the coordinator's GO message. The lead checks it out (section C) and gives it to the
session, and the first line that step 0 prints must equal it. The code is identified by the sha256 of
`PIN.sha256`, the list of the sha256 of every file the pilot executes or imports; step 0 recomputes both.
sha256 of `PIN.sha256`: `7aa9bbfc79e7df6421af9a6ec6fa9ef9d507cf2a2583c4c11da2b18ab0f64c19`
<!-- PIN-END -->

What this is: the exact commands to (0) verify the code, (1) install, (2) run the scripted, model-free smoke test
on Docker at $0, (3) run ONE rollout of a cheap model with a stock harness. Evidence: every command of steps 0
to 2 and of step 4 except the image build, and every point of "If a run was interrupted", was rehearsed in the
cloud container (Linux x86_64, Docker 29.9.2, uv 0.11.32) from a fresh clone, each command issued the way a
session issues it, as ONE `sh -c '<text>'` (`results/rehearsal_round2.json`: the literal text and the complete
output of each; the commands are byte for byte the ones below, and the prose around them was corrected
afterwards in the six places that record lists; what could not be rehearsed there is listed at the end of this
file).
**Nothing here has run on a Mac: every statement about macOS and Docker Desktop is inferred.** Step 3 has not
run anywhere.

## A. Rules for the session that follows this file

1. **Two things come from the lead before your first command:** the absolute path of the study folder (it ends
   in `research/alife/vecworld/program/round6/vfport`) and the 40-character commit hash of the coordinator's GO
   message. You follow the copy of this file that is in that study folder. If its first lines say ON HOLD, or
   you were given no hash: stop, run nothing.
2. **One command per call, copied from this file.** The only change you make is to replace the literal text
   `/ABSOLUTE/PATH/TO/vfport` by the path of the study folder, and, in the two commands of "If a run was
   interrupted" that have one, the placeholder `PID_FROM_THE_STATUS_LINE` or `NAME_FROM_THE_STATUS_LINE` by what
   the status command printed. Write the path out in every command. Never put it in a variable, never rely on
   the folder a previous command was in, never type a command from memory.
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
7. **Never, on the Mac:**

   | never | why |
   |---|---|
   | `sudo`; edits of `~/.zshrc`, `~/.zprofile`, `~/.zshenv`; `export` of a variable for later commands | nothing in the pilot needs them; every variable is written on the command that uses it |
   | `docker run` with `-v`, `--mount` or the Docker socket; any other `docker run` by hand for anything in this repository, whatever its options (`--pid`, `--ipc`, `--tmpfs`, `--privileged`, `--volumes-from` included) | the exam's cleanup deletes files of one user id wherever it can see them; a mounted Mac folder would be in sight (the driver refuses when an extra file system is mounted, but do not rely on it). The only `docker run` of the pilot is the image check of step 1, copied from this file |
   | pasting the route's own commands (the `sh -c` lines of `physim2_env/grading.py` and `physim2_env/taskset.py`) into a shell or a container | they change owners and modes and delete as root |
   | `physim2_env/public/_item.py`, `physim2 validate`, or a model's `predict.py`, on the Mac itself | they run submitted code |
   | `agents/*.py`; anything in `redteam/`, in `rehearsal/` or in `../../round5/agentenv` (its `mac/` runbook and compose file included); `tools/check_units.py`, `tools/check_driver.py`, `tools/check_safety.py`, `tools/check_interrupt.py` | attack scripts, the cloud rehearsal's own scripts and development checks for the cloud container; the round-5 compose file mounts host folders into a container that deletes there as root |
   | `pkill`, `killall`, `kill -1`, `kill -9`, a `kill` that is not the stop command of "If a run was interrupted", `docker rm` by filter or with `$(...)`, any `prune`, `vf-eval --clean`, `rm -rf` of anything this file does not spell out | they reach beyond the pilot: other verifiers runs on this Mac (PhySim v1) use the same container names `vf-...` |
   | another `[env.agent.runtime] type`, another harness, another model, a second try after a failure | stop and report instead |
   | `tools/docker_shim` | it is for Linux hosts without IPv6 and cannot work on macOS. If a run fails with `net.ipv6.conf.all.disable_ipv6`: stop and report |

## B. What the pilot does to the Mac itself (the whole inventory)

Read from the code that `PIN.sha256` identifies and from verifiers 0.3.2.dev163; the cloud rehearsals saw the
same on Linux.

**Processes on the Mac, as your user.** `uv` (step 1 only); the `docker` client; in step 2 the two tools
(`.venv/bin/python -B tools/prove.py`, `tools/check_probe.py`), each of which starts one `vf-eval` at a time;
`vf-eval` starts one laboratory process per rollout (`.venv/bin/python -m physim2_env.lab_tools`: it simulates the
hidden world and answers the agent's requests) and many short `docker` commands. `tools/prove.py` also runs round
5's own reference agent once on the Mac to build the reference submission C (our code, no submitted code).
Every detached command also leaves one waiting shell, a copy of the shell that issued it, which does nothing but
wait for its tool and then write the `EXIT` line; it ends with the tool.
No predictor, no hostile test agent and no model-written code runs on the Mac: they run in containers only.

**What is signalled or killed on the Mac.**

| who | what | when |
|---|---|---|
| verifiers | the laboratory process it started (its own process group): SIGTERM, then SIGKILL if it has not ended | at the end of every rollout, and when vf-eval is stopped |
| verifiers | a `docker` client command it started itself | only if that command is cut by a timeout |
| `tools/vfrun.py` | the `vf-eval` it started: ONE SIGTERM (vf-eval then removes its containers and stops its laboratory); SIGKILL only if it is still there 120 s later | when a run exceeds an hour, or when the tool itself is stopped |
| you | ONE process of the pilot: SIGTERM to the pid that the status command printed, sent by the stop command, which first checks that the command line of that pid begins with this study folder's `.venv/bin/python` and sends nothing otherwise | only in "If a run was interrupted" |

Nothing sends a signal by name, by user or to "all processes" on the Mac. Inside containers the driver kills the
predictor's processes, and one test agent of step 2b (`harness-killall`) runs `kill -9 -1` in its own box: the box
is a container that verifiers created for it without any Mac folder mounted.

**What is deleted on the Mac.**

| who | what | where |
|---|---|---|
| `uv sync` (step 1) | an existing `.venv` of the study folder would be replaced; the dry run before it must say `Would create`, not `Would replace` | study folder |
| step 1 | nothing: `docker/extra-ca.crt` is created empty only if it does not exist (a file with content is a stop) | study folder |
| `tools/make_instances.py` | `store/<instance>/hidden/examples.npz`, a file it wrote a moment before | store |
| `tools/vfrun.py` | the run folder of an EARLIER call with the same name, only if it holds nothing but vf-eval's own files; happens only when a tool is started again | scratch |
| `tools/prove.py` | `store/<instance>/work/reference_<policy>` for box checks of policies other than C: not reached with the arguments below | store |
| the package (`bundle.py`, `access.py`) and Python's `tempfile` | temporary folders the same process created (`physim2-bundle-*`, `physim2-io-*` under `$TMPDIR`) | temp |
| verifiers | the laboratory's working folder `~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>`, which it created; its `logs/latest` link in a run folder | home, scratch |
| verifiers | the containers it created, `vf-<32 hex>`, by `docker rm --force <that name>`; helper containers started with `--rm` | Docker |
| `docker run --rm` (step 1, and the control of step 2b) | the test container it just started | Docker |
| you, "If a run was interrupted" | a leftover container of this pilot, by its exact name; the two pilot folders | Docker, home |
| you, step 4 | the two pilot folders, after their results were copied out | home |

**What is written and left on the Mac.** uv's own Python 3.12, if uv has none yet: the DRY RUN of step 1
already downloads it (`~/.local/share/uv/python`; 104 MB on disk in the cloud rehearsal); `.venv` in the study
folder (about 1 GB with jax) and uv's cache (`~/.cache/uv`); `docker/extra-ca.crt` (empty; git ignores it);
the folders `$HOME/physim2-pilot-20261110/store` and `.../scratch`, and in step 4
`$HOME/physim2-pilot-20261110-results`; `~/.cache/verifiers/` (created by verifiers); one small file
`/tmp/vf-port-<hex>` per rollout, which verifiers never removes (leave them; do not delete by pattern); only
after a vf-eval was killed outright, two small folders nobody removes: the laboratory's working folder
`~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>` (one log file) and `$TMPDIR/physim2-io-<random>` (one socket);
Docker images `physim2-ring:1` (about 560 MB), `python:3.12-slim`, and `localhost/verifiers-network:1` with `alpine:3.22`,
which verifiers builds itself at the first rollout.

**What listens on the Mac.** Per box, verifiers' proxy and the container's published port, on 127.0.0.1; per
rollout the laboratory, on 127.0.0.1; for the minutes `tools/check_probe.py` runs, one TCP listener on 127.0.0.1
that accepts a connection, records the peer and closes it.

**Network.** `uv sync` downloads from PyPI, one wheel from github.com and, if uv has no Python 3.12 of its own,
that Python from github.com; `docker build` and the first rollout pull `python:3.12-slim` and `alpine:3.22` and
install numpy, scipy and jax from PyPI. Nothing is uploaded: every run is made with `push = false` and
`PRIME_RUNS_MODE=disabled`.

## C. By hand, before the session's first command (the lead)

| check | command | expected |
|---|---|---|
| hold lifted | the coordinator's message | GO for steps 0 to 2, with a 40-character commit hash |
| right code | in the study folder: `git fetch origin claude/fisim-agent-world-research-hepmlz`, then `git checkout --detach <the hash of the GO message>`; `git rev-parse HEAD`; `git status --short` | that hash, all 40 characters; nothing listed |
| right text | the first lines of `RUNBOOK_MAC.md` in the study folder | they begin `**GO for steps 0 to 2.**`, not ON HOLD |
| user | `id -u`; `echo "$HOME"`; `ls "$HOME/physim2-pilot-20261110" "$HOME/physim2-pilot-20261110-results"` | not 0; your own home; no such folders. A current backup of the Mac exists |
| machine | `uname -m` | `arm64` |
| folder | `pwd -P` in the study folder | ends in `research/alife/vecworld/program/round6/vfport` |
| path is plain | `pwd -P \| LC_ALL=C grep -E '^[A-Za-z0-9/._-]+$'` in the study folder | it prints the path again. If it prints nothing, the path holds a space or another character outside letters, digits and `/ . _ -`: move the checkout first (the status and stop commands use the path as a search pattern) |
| the session | started in the study folder; given that path and the hash of the GO message | no subagents; one command per call |
| tools | `command -v uv docker`; `uv --version`; `docker context show`; `docker info` | uv 0.11 or later (it must know `--managed-python`); Docker Desktop's own client and context; it answers. If uv is missing or older: stop and ask, do not install it from inside the session |
| variables | `env \| grep -E '^(PHYSIM2_\|UV_\|VIRTUAL_ENV\|PYTHONPATH\|DOCKER_HOST\|DOCKER_CONTEXT\|VF_RUN_ID\|PRIME_RUNS_MODE)'` | nothing |
| other runs | `docker ps -a --filter label=verifiers.run`; `docker images physim2-ring` | nothing. Save the output of `docker ps -a` and `docker images` as the baseline |
| room | free disk; Docker Desktop: Settings, Resources | 5 GB free; 4 CPUs; the virtual disk limit is BELOW the Mac's free space |
| power | plugged in; no sleep for the 45 minutes of steps 1 and 2 | a sleep is an interruption |
| network | VPN, TLS-intercepting proxy | none (the image build needs a direct connection) |

## 0. Verify the code (seconds)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && git rev-parse HEAD && git status --porcelain -- . ../../round5/agentenv ../../../vw1 | wc -l
```

Expected: two lines. The first is the 40-character hash that the lead gave you from the coordinator's GO
message: compare all 40 characters. The second is `0` (macOS pads the number with spaces). Another hash, or
another number: stop.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && shasum -a 256 PIN.sha256 && shasum -a 256 -c PIN.sha256 > /dev/null && echo PIN-OK
```

Expected: two lines, the hash of the pin block above followed by `PIN.sha256`, then `PIN-OK`. `PIN.sha256` lists
the sha256 of every file the pilot executes or imports (the package, the tools, the agents, the configs, round
5's `agentenv` and the `vw` library). If a listed file was changed or is missing there is no `PIN-OK`; what
appears instead is a line that begins `shasum: WARNING:` (for example `shasum: WARNING: 1 computed checksum did
NOT match`), after a line `shasum: <file>: No such file or directory` for a missing file. No `PIN-OK`, or another
hash in the first line: stop.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}}' | wc -l && docker images -q physim2-ring:1 | wc -l && ls -d "$HOME/physim2-pilot-20261110" "$HOME/physim2-pilot-20261110-results" .venv 2>&1 | grep -c "No such file"
```

Expected: Docker's version, then `0` (no container of this pilot), `0` (no image of that name yet), `3` (neither
pilot folder nor a `.venv` exists); macOS pads the two `wc` numbers with spaces. Anything else: stop.

## 1. Install (about 10 minutes, most of it the image build)

A cut or an unexpected output anywhere in this step: run nothing more, report, stop. Step 1 has no recovery
procedure.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f pyproject.toml && test -f uv.lock && cd / && uv sync --project "/ABSOLUTE/PATH/TO/vfport" --locked --python 3.12 --managed-python --dry-run 2>&1 | grep -E "^Using CPython|project environment|Would (download|install)|error"
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
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && mkdir "$HOME/physim2-pilot-20261110" && mkdir "$HOME/physim2-pilot-20261110/scratch" && (test -e docker/extra-ca.crt || : > docker/extra-ca.crt) && wc -c docker/extra-ca.crt
```

Expected: `0 docker/extra-ca.crt` (macOS pads the number with spaces). `mkdir` fails if a pilot folder exists
already, and nothing after it runs: stop. A number other than 0 means somebody's certificate file is there:
stop.

The real `uv sync` downloads several hundred megabytes on a Mac whose cache is empty, so it runs detached. This
is the only `uv` command that changes anything; no later command uses `uv`.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f pyproject.toml && test -f uv.lock && docker info --format '{{.ServerVersion}}' && { ( nohup uv sync --project "/ABSOLUTE/PATH/TO/vfport" --locked --python 3.12 --managed-python > "$HOME/physim2-pilot-20261110/scratch/sync.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/sync.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once. Status (repeat until the log's last line is `EXIT 0`; any other
`EXIT` line, or a line with `error`: stop; no `EXIT` line after 20 minutes: stop and report, signal nothing):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && tail -n 3 "$HOME/physim2-pilot-20261110/scratch/sync.log"
```

Expected when it is finished: two lines that begin with ` + ` (the last of the installed packages), then
`EXIT 0`.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B -c "import verifiers, numpy, scipy, jax, physim2_env, physim2_script; print(verifiers.__version__, numpy.__version__, scipy.__version__, jax.__version__, physim2_env.__file__)"
```

Expected: `0.3.2.dev163 2.5.4 1.18.1 0.12.0.1 /ABSOLUTE/PATH/TO/vfport/physim2_env/__init__.py` with your path.

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
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( nohup docker build -f docker/Dockerfile.ring -t physim2-ring:1 docker/ > "$HOME/physim2-pilot-20261110/scratch/build.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/build.log" ) > /dev/null 2>&1 < /dev/null & }
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

The tools call `vf-eval physim2-env --env.id isolated-verifier` with the Docker runtime and the scripted
harness; they set `push = false`, `PRIME_RUNS_MODE=disabled` and remove `PRIME_API_KEY` from the child's
environment. `VF_RUN_ID=physim2-pilot-20261110` is on every run command: verifiers writes it on every container
it creates as the label `verifiers.run`, and the tools refuse to start without it. The store path is on every
command; nothing depends on a variable set earlier.

**Status command of step 2** (use it after starting 2a, 2b or 2c, and whenever you want to know what runs):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && { tail -n 4 "$HOME/physim2-pilot-20261110/scratch/prove.log" "$HOME/physim2-pilot-20261110/scratch/probe.log" "$HOME/physim2-pilot-20261110/scratch/single.log" 2>/dev/null ; echo "containers:" ; docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' ; echo "processes:" ; ps axww -o pid= -o command= | grep -E "^ *[0-9]+ /ABSOLUTE/PATH/TO/vfport/\.venv/bin/python" ; echo "status done" ; }
```

It prints the last lines of the logs that exist (each under a line `==> <file> <==`), then under `containers:`
the containers of this pilot (`<name> <state>`), under `processes:` the processes of this pilot, and `status
done`. A container line is a box, `vf-<32 hex> Up ...`, or, for a second at a time, a helper that verifiers or
the probe tool started under a two-word name chosen by Docker (cloud rehearsal: `tender_gates Up Less than a
second`); a helper removes itself. A process line is the pid, one space, and the whole command line, which begins with this study folder's
`.venv/bin/python`: the tool (`... -B tools/prove.py ...` or `... -B tools/check_probe.py ...`), its vf-eval
(`... /ABSOLUTE/PATH/TO/vfport/.venv/bin/vf-eval @ ...`), the laboratory (`... -m physim2_env.lab_tools ...`),
and for seconds at a time a helper of the tool (`... tools/make_instances.py ...`, `... reference_agent.py ...`).
The waiting shell of a detached command is not listed. A step is finished when its log ends with an `EXIT` line
and nothing is listed under `containers:` and `processes:`. While a step runs, wait and ask again; start nothing
else. A Docker error under `containers:` (Docker does not answer): stop.

### 2a. One world, three policies, then C once more with one box per exam item (about 10 minutes)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/prove.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/proof" --worlds 1 --prefix mac-ring --policies D,P0,C --box-check C --no-cross-check --out "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" > "$HOME/physim2-pilot-20261110/scratch/prove.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/prove.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once (the tool runs on, detached). Then use the status command, the
first time right away. **Under `processes:` it must show a line `<pid> /ABSOLUTE/PATH/TO/vfport/.venv/bin/python
-B tools/prove.py ...`.** If it does not, and `prove.log` has no `EXIT` line: send no signal and start nothing;
ask for the status every few minutes until `prove.log` ends with an `EXIT` line, then stop and report (the run
cannot be seen from here, so it cannot be stopped from here either). If `prove.log` already ends with an `EXIT`
line other than `EXIT 0`: stop and report.

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
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/check_probe.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/probe" --out "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" > "$HOME/physim2-pilot-20261110/scratch/probe.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/probe.log" ) > /dev/null 2>&1 < /dev/null & }
```

Then the status command; under `processes:` it must show a line `<pid> /ABSOLUTE/PATH/TO/vfport/.venv/bin/python
-B tools/check_probe.py ...` (if not: as in 2a). When `probe.log` ends with `EXIT 0`, the line before it is one
JSON object. Expected on the Mac:

- `"failed_round5": []`
- `"failed_new": ["b_lab_process_dropped_it_after_loading"]`. **This one failure is expected on macOS** and only
  there: the check reads the laboratory process's environment block in `/proc`, which macOS does not have. (On
  Linux the list is empty.)

Any other name in either list: stop and report the two lists. Several checks were measured on Linux only (the
network cut and its control `c_*`, the per-item channels `a2_*`, `agent_sees_only_its_own_processes`); if one of
them differs on Docker Desktop, that is a finding to report, not something to make pass. Then, for the report:

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
the uncut control container reaches a listener on the Mac (`control`), and what a box can reach.

### 2c. One scripted rollout without the tools (about 4 minutes)

Policy D on `mac-ring-w0` through `vf-eval` directly, as step 3 will call it. It can run once: a second run of
the same agent on the same instance is refused.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 PHYSIM2_STORE="$HOME/physim2-pilot-20261110/store" PRIME_RUNS_MODE=disabled PYTHONDONTWRITEBYTECODE=1 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/vf-eval" @ configs/scripted_ring.toml --no-rich --run.name single-d -o "$HOME/physim2-pilot-20261110/scratch/single" > "$HOME/physim2-pilot-20261110/scratch/single.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/single.log" ) > /dev/null 2>&1 < /dev/null & }
```

Then the status command; under `processes:` it must show a line `<pid> /ABSOLUTE/PATH/TO/vfport/.venv/bin/python
/ABSOLUTE/PATH/TO/vfport/.venv/bin/vf-eval @ configs/scripted_ring.toml ...` (if not: as in 2a, with
`single.log`). Repeat it until `single.log` ends with `EXIT 0`. The status shows the last four lines of that
log: at the end these are the end of the trace that vf-eval prints with `--no-rich` (two lines of token counts
and a closing `}`) and `EXIT 0`. Do not open `single.log` or `traces.jsonl` beyond that: in step 3 the same
files hold the examined model's text, and step 3 has a status command of its own that shows the `EXIT` line
only. Read a run only through the report tool, which prints fixed fields and counts:

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
interruption do points 1 to 5, then stop and report: no reset, no new start.

Use it when a command of step 2 did not end with `EXIT 0`: the Mac slept, Docker Desktop stopped, a command was
cut, the session was restarted, you were told to stop. Do exactly this, in this order, and nothing else. In
particular do not start the step again before the end of this section.

1. **What is still there?** Run the status command of step 2. It lists the pilot's processes and the pilot's
   containers. Nothing of anybody else can be in either list: the processes are the ones whose command line
   begins with this study folder's own `.venv/bin/python`, the containers the ones that carry this pilot's run
   label. (Do not list by the name `vf-`: other verifiers runs on this Mac use the same names. Do not look for
   the pilot with another `ps` or `pgrep` command: a search for the folder's name also finds the waiting shell
   of a detached command, and a signal to that shell stops nothing and loses the `EXIT` line.) If Docker prints
   an error under `containers:`: stop and report; remove nothing.
2. **A tool or a vf-eval of the pilot is still running** (a line with `-B tools/prove.py`, `-B
   tools/check_probe.py` or `.venv/bin/vf-eval`): tell it to stop, once, by the pid at the start of its line.
   Take the tool's pid if a tool is listed, otherwise vf-eval's:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && ps -ww -p PID_FROM_THE_STATUS_LINE -o command= | grep -E "^/ABSOLUTE/PATH/TO/vfport/\.venv/bin/python" && kill -TERM PID_FROM_THE_STATUS_LINE
   ```

   It prints the command line of the process it then signals (the same text as on the status line, without the
   pid). **If it prints nothing, no signal was sent**: that pid is not, or no longer, a process of this study
   folder's interpreter. Then run the status command once more; if a tool or a vf-eval is still listed, stop
   and report.
   The tool passes the signal on; vf-eval removes its containers and stops its laboratory itself (2 to 4 seconds
   in the cloud rehearsals; allow two minutes). Ask for the status again until no process and no container is
   listed. The log of the stopped command then ends in one of three ways, all of them expected here:

   | stopped | the log ends with |
   |---|---|
   | a tool, inside a rollout | a Python traceback whose last line is `KeyboardInterrupt`, then `EXIT 130` |
   | a tool, between two rollouts or before the first (no vf-eval was listed) | `EXIT 143`, no traceback; the shell may put one line of its own before it (`Terminated` in the cloud rehearsal) |
   | the vf-eval of 2c | lines of vf-eval's own log (one of them says `WARNING interrupted`), then `EXIT 130`; no traceback |

   Send the signal once; never `kill -9`, never a second pid in the same command.
3. **Containers of the pilot are still listed and no vf-eval of the pilot is running** (vf-eval was killed before
   it could clean up; the tool's log then ends with `EXIT 1`): remove each one by its exact name, one command per
   container, the name copied from the status output:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker rm -f NAME_FROM_THE_STATUS_LINE
   ```

   It prints that name.
4. **A laboratory process is still listed** (a line with `-m physim2_env.lab_tools`) **and no vf-eval is**:
   stop it by its pid with the stop command of point 2. It holds no state worth keeping. A laboratory that has
   lost its vf-eval may also end by itself within seconds: if the stop command prints nothing here, nothing was
   signalled and the laboratory is gone already; go on with point 5.
5. Run the status command again. Expected now: no process line, no container line. If something of the pilot
   is still listed after two minutes: stop and report.
6. **Delete the two pilot folders and start again from the instance** (first interruption only). A cut rollout
   has spent its laboratory budget and its instance cannot be opened again by the same agent, so the store is
   not reusable:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch" && mkdir "$HOME/physim2-pilot-20261110/scratch" && echo "pilot folders reset"
   ```

   Expected: `pilot folders reset`. If it prints nothing: stop and report. Then continue from the
   `make_instances` command of step 1, and run step 2 from 2a. The image and `.venv` stay; the logs of step 1
   (`sync.log`, `build.log`) went with the scratch folder.
7. Say in the report that a run was interrupted, at which command, and what the status command listed. If
   point 3 or 4 was needed, two small folders of the killed vf-eval stay on the Mac and nothing removes them: the
   laboratory's working folder `~/.cache/verifiers/runtimes/subprocess/vf-<12 hex>` (one log file) and
   `$TMPDIR/physim2-io-<random>` (one socket). Name them in the report and leave them: do not delete by pattern.

## 3. ONE rollout of a cheap model, stock harness (SEPARATE HOLD)

**NO-GO until steps 0 to 2 have passed on this Mac and the lead has read their report.** This is the only step
in which an untrusted model acts: it is root in a container for up to an hour, and Docker Desktop's virtual
machine is the only wall between it and the Mac; that wall was not tested by this study.

By hand first (the lead): Docker Desktop's virtual disk limit is below the Mac's free disk space (a model can
fill its box; it must hit that limit, not fill the Mac's disk); Prime inference credentials are in the
environment of the session, as for the PhySim v1 rollouts.

Model `qwen/qwen3.5-35b-a3b`, the stock `bash` harness of verifiers, the ring smoke exam, one hidden world, one
hour. `configs/qwen_ring_bash.toml` sets `push = false`, no retries at any level, `max_turns = 40`,
`max_total_tokens = 1500000`, `max_output_tokens = 60000`, and nothing else may be changed.

Free, calls no model (resolves the config only):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && VF_RUN_ID=physim2-pilot-20261110 PHYSIM2_STORE="$HOME/physim2-pilot-20261110/store" PRIME_RUNS_MODE=disabled PYTHONDONTWRITEBYTECODE=1 "/ABSOLUTE/PATH/TO/vfport/.venv/bin/vf-eval" @ configs/qwen_ring_bash.toml --dry-run --run.name qwen-dry -o "$HOME/physim2-pilot-20261110/scratch/qwen-dry" > "$HOME/physim2-pilot-20261110/scratch/qwen-dry.log" 2>&1 ; echo "EXIT $?"
```

Expected: `EXIT 0`.

---

**STOP. THE NEXT COMMAND SPENDS MONEY. Do not run it without the lead's explicit "go" for this command, given
after the smoke test's report.**

Price: the token caps are checked before each model call, so the spend is bounded by 1.5 M tokens in total, of
which at most 60 k are output, plus one request: at most `1.5 x p_in + 0.06 x p_out` dollars for prices p_in and
p_out per million tokens. The price of this model was not available in the cloud container; the lead reads it
from Prime's Models API and writes it here before saying go: p_in = ______, p_out = ______, bound = ______. (As
an illustration only: at $0.20 in and $0.60 out the bound is $0.34.) The caps count the usage the provider
reports; if it reports none they do not bind, and the bound is then 40 requests and one hour.

The lead's go is also a file, which the lead creates by hand and the session never creates: an empty file
`$HOME/physim2-pilot-20261110/scratch/LEAD-GO-STEP3`. The command below starts nothing without it (it then prints
nothing: stop).

It can be run ONCE: `single_use` refuses a second rollout of this model and harness on `mac-ring-w0`.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f "$HOME/physim2-pilot-20261110/scratch/LEAD-GO-STEP3" && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 PHYSIM2_STORE="$HOME/physim2-pilot-20261110/store" PRIME_RUNS_MODE=disabled PYTHONDONTWRITEBYTECODE=1 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/vf-eval" @ configs/qwen_ring_bash.toml --no-rich --run.name qwen -o "$HOME/physim2-pilot-20261110/scratch/qwen" > "$HOME/physim2-pilot-20261110/scratch/qwen.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/qwen.log" ) > /dev/null 2>&1 < /dev/null & }
```

---

While it runs (up to an hour, then about 3 minutes of grading), ask for its state with this command only:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && { tail -n 1 "$HOME/physim2-pilot-20261110/scratch/qwen.log" | cut -c 1-12 ; echo "containers:" ; docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' ; echo "processes:" ; ps axww -o pid= -o command= | grep -E "^ *[0-9]+ /ABSOLUTE/PATH/TO/vfport/\.venv/bin/python" | cut -c 1-160 ; echo "status done" ; }
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

If the run is cut: "If a run was interrupted", points 1 to 5 and 7; do not delete the folders (the references of
step 2 are in them), do not run the rollout again; settle it as in 1.

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

The store holds theta and the secret of a pilot that must never be reused. First run the status command of step
2: nothing may be listed. Then copy the results out and remove exactly the two folders, in ONE command, so that
nothing is deleted unless every check and every copy before it succeeded:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && test -f "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" && test -f "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" && mkdir "$HOME/physim2-pilot-20261110-results" && cp "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" "$HOME/physim2-pilot-20261110/scratch/proof_mac_items.npz" "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" "$HOME/physim2-pilot-20261110/scratch/prove.log" "$HOME/physim2-pilot-20261110/scratch/probe.log" "$HOME/physim2-pilot-20261110-results/" && test -s "$HOME/physim2-pilot-20261110-results/proof_mac.json" && test -s "$HOME/physim2-pilot-20261110-results/probe_mac.json" && rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch" && rmdir "$HOME/physim2-pilot-20261110" && ls "$HOME/physim2-pilot-20261110-results"
```

Expected: the five file names. If it prints nothing: stop and report. The copied files
hold scores, counters and commitments only (`PILOT_NEVER_REUSE_AS_EXAM`); the run folders with their traces are
deleted with the scratch folder (a trace names the operator's account), and after step 3 the output of
`tools/run_report.py` is what leaves the Mac, with the trace folder only if the lead asked for it.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' | wc -l && docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}'
```

Expected: `0` (macOS pads it with spaces), then the images. Compare `docker ps -a` and `docker images` with the
baseline of the by-hand checks: the pilot added `physim2-ring:1`, `python:3.12-slim`,
`localhost/verifiers-network:1` and `alpine:3.22` and no container. Keep the images: the helper image
`localhost/verifiers-network:1` is shared with other verifiers work on this Mac and is not this pilot's to remove;
`physim2-ring:1` may be removed by the lead, by hand, when no further run is planned (`docker rmi
physim2-ring:1`). The `.venv` stays until the lead removes the checkout.

## What the cloud rehearsal could not cover

- macOS and Docker Desktop: nothing. Inferred, not seen: that containers there carry `/.dockerenv` and Docker's
  usual mount table (if not, staging stops with `the box is not recognised as a disposable box` and names the
  mount or the missing sign; nothing is damaged; report it); how `uv` behaves and that the Python it manages
  shows `.venv/bin/python` as its command line (step 1 checks it); that `ps` and `shasum` print there what they
  print on Linux; that the session's shell (zsh) leaves the same waiting shell as `sh` and `bash` did; how a
  Claude session on the Mac ends a command at its limit; that a detached command survives the end of the call
  that started it.
- The image build of step 1: the cloud machine sits behind a TLS-intercepting proxy and already had the shared
  image `physim2-ring:1`, at which step 0 says stop; the rehearsals went on with that image and did not run the
  build command or its status command.
- Step 2c as written: the cloud machine's kernel has no IPv6, so a direct `vf-eval` needs `tools/docker_shim` first
  on PATH there (the tools of 2a and 2b add it themselves on such Linux hosts); the rehearsal put it on the PATH
  of that one call. This does not apply to macOS, where the shim must not be used.
- The by-hand checks: the cloud session is root, on x86_64, with `UV_NATIVE_TLS` set; `$HOME` was replaced by a
  folder of the rehearsal, and uv's own Python went to a folder of the rehearsal.
- "If a run was interrupted": every point was rehearsed, the section five times, each time as a first
  interruption. Its rule for a second interruption (points 1 to 5, then stop) was not exercised as a rule; nor
  was the "must show" rule of 2a in its failing branch with the real tool (with a stand-in interpreter only).
- Step 3, its file gate and the copy of its trace: never run (their gates were run with stand-ins).
