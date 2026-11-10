# RUNBOOK for the Mac session: PhySim v2 on verifiers

**ON HOLD. Run nothing from this file.** An independent host-safety audit returned NO-GO on 10 Nov 2026
(`HOST_SAFETY_AUDIT.md`). The code and this file were changed to meet its nine required changes; a re-audit has
not been made. The hold on steps 0 to 2 is lifted only by a message from the coordinator that says the re-audit
returned GO and names the commit of the pin block below. Step 3 (a paid model rollout) has a second hold of its
own and stays NO-GO until steps 0 to 2 have passed on the Mac and been reported.

<!-- PIN-BEGIN -->
**Pin.** Commit: `454812a2bc497e5c5e7e38109dd7121fcc57c1cf` (this is the copy of the file at the head of the
branch; the copy inside that commit is identical outside this block, where it says that a commit cannot name its
own hash).
sha256 of `PIN.sha256`: `7aa9bbfc79e7df6421af9a6ec6fa9ef9d507cf2a2583c4c11da2b18ab0f64c19`
<!-- PIN-END -->

What this is: the exact commands to (0) verify the code, (1) install, (2) run the scripted, model-free smoke test
on Docker at $0, (3) run ONE rollout of a cheap model with a stock harness. Evidence: steps 0 to 2 and step 4
were rehearsed in the cloud container (Linux x86_64, Docker 29.9.2) from a fresh clone, with two deliberate
interruptions (`results/rehearsal_round1.json`; what could not be rehearsed there is listed at the end of this
file).
**Nothing here has run on a Mac: every statement about macOS and Docker Desktop is inferred.** Step 3 has not
run anywhere.

## A. Rules for the session that follows this file

1. **One command per call, copied from this file.** The only change you make is to replace the literal text
   `/ABSOLUTE/PATH/TO/vfport` by the absolute path of the study folder, the one the lead gives you (it ends in
   `research/alife/vecworld/program/round6/vfport`). Write that path out in every command. Never put it in a
   variable, never rely on the folder a previous command was in, never type a command from memory.
2. **Every command starts with the same guard**:
   `cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && ...`
   If the path is wrong, the guard fails and the rest of the line does not run. A command that prints nothing
   where this file says it prints something has not run: stop.
3. **No subagents, no parallel commands.** A subagent starts in another folder. One command at a time.
4. **Stop rule.** If the output differs from what this file says to expect (apart from the one exception named in
   step 2b), or anything asks for a password or for `sudo`, or prints `refused:`, or Docker stops answering:
   **stop and report what you saw. Do not retry, do not repair, do not try another way.** A deviation is a
   result of the pilot, not an obstacle.
5. **Long commands run detached** and write a log; you then ask for their status with the status command of the
   step. Never run a long command in the foreground: a session's foreground command is cut after a few minutes,
   and a cut run leaves containers behind.
6. **Never, on the Mac:**

   | never | why |
   |---|---|
   | `sudo`; edits of `~/.zshrc`, `~/.zprofile`, `~/.zshenv`; `export` of a variable for later commands | nothing in the pilot needs them; every variable is written on the command that uses it |
   | `docker run` with `-v`, `--mount` or the Docker socket, for anything in this repository | the exam's cleanup deletes files of one user id wherever it can see them; a mounted Mac folder would be in sight (the driver now refuses when any extra file system is mounted, but do not rely on it) |
   | pasting the route's own commands (the `sh -c` lines of `physim2_env/grading.py` and `physim2_env/taskset.py`) into a shell or a container | they change owners and modes and delete as root |
   | `physim2_env/public/_item.py`, `physim2 validate`, or a model's `predict.py`, on the Mac itself | they run submitted code |
   | `agents/*.py`; anything in `redteam/` or in `../../round5/agentenv` (its `mac/` runbook and compose file included); `tools/check_units.py`, `tools/check_driver.py`, `tools/check_safety.py`, `tools/check_interrupt.py` | attack scripts and development checks for the cloud container; the round-5 compose file mounts host folders into a container that deletes there as root |
   | `pkill`, `killall`, `kill -1`, `docker rm` by filter or with `$(...)`, any `prune`, `vf-eval --clean`, `rm -rf` of anything this file does not spell out | they reach beyond the pilot: other verifiers runs on this Mac (PhySim v1) use the same container names `vf-...` |
   | another `[env.agent.runtime] type`, another harness, another model, a second try after a failure | stop and report instead |
   | `tools/docker_shim` | it is for Linux hosts without IPv6 and cannot work on macOS. If a run fails with `net.ipv6.conf.all.disable_ipv6`: stop and report |

## B. What the pilot does to the Mac itself (the whole inventory)

Read from the code of the pinned commit and of verifiers 0.3.2.dev163; the cloud rehearsal saw the same on Linux.

**Processes on the Mac, as your user.** `uv` (step 1 only); the `docker` client; in step 2 the two tools
(`.venv/bin/python -B tools/prove.py`, `tools/check_probe.py`), each of which starts one `vf-eval` at a time;
`vf-eval` starts one laboratory process per rollout (`.venv/bin/python -m physim2_env.lab_tools`: it simulates the
hidden world and answers the agent's requests) and many short `docker` commands. `tools/prove.py` also runs round
5's own reference agent once on the Mac to build the reference submission C (our code, no submitted code).
No predictor, no hostile test agent and no model-written code runs on the Mac: they run in containers only.

**What is signalled or killed on the Mac.**

| who | what | when |
|---|---|---|
| verifiers | the laboratory process it started (its own process group): SIGTERM, then SIGKILL if it has not ended | at the end of every rollout, and when vf-eval is stopped |
| verifiers | a `docker` client command it started itself | only if that command is cut by a timeout |
| `tools/vfrun.py` | the `vf-eval` it started: ONE SIGTERM (vf-eval then removes its containers and stops its laboratory); SIGKILL only if it is still there 120 s later | when a run exceeds an hour, or when the tool itself is stopped |
| you | a process of the pilot, by the exact pid that the status command printed | only in "If a run was interrupted" |

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
| you, step 4 | the two pilot folders, after their results were copied out | home |

**What is written and left on the Mac.** `.venv` in the study folder (about 1 GB with jax), uv's cache and, if
absent, uv's own Python 3.12 (`~/.cache/uv`, `~/.local/share/uv`); `docker/extra-ca.crt` (empty; git ignores it);
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

**Network.** `uv sync` downloads from PyPI and one wheel from github.com; `docker build` and the first rollout
pull `python:3.12-slim` and `alpine:3.22` and install numpy, scipy and jax from PyPI. Nothing is uploaded: every
run is made with `push = false` and `PRIME_RUNS_MODE=disabled`.

## C. By hand, before the session's first command (the lead)

| check | command | expected |
|---|---|---|
| hold lifted | the coordinator's message | GO for steps 0 to 2, naming the commit of the pin block |
| right code | in the study folder: `git fetch origin claude/fisim-agent-world-research-hepmlz`, then `git checkout --detach <that commit>`; `git rev-parse HEAD`; `git status --short` | the pinned commit; nothing listed |
| user | `id -u`; `echo "$HOME"`; `ls "$HOME/physim2-pilot-20261110" "$HOME/physim2-pilot-20261110-results"` | not 0; your own home; no such folders. A current backup of the Mac exists |
| machine | `uname -m` | `arm64` |
| folder | `pwd -P` in the study folder | ends in `research/alife/vecworld/program/round6/vfport`; give this path to the session, which must be started in this folder |
| tools | `command -v uv docker`; `docker context show`; `docker info` | Docker Desktop's own client and context; it answers. If uv is missing: stop and ask, do not install it from inside the session |
| variables | `env \| grep -E '^(PHYSIM2_\|UV_\|VIRTUAL_ENV\|PYTHONPATH\|DOCKER_HOST\|DOCKER_CONTEXT\|VF_RUN_ID\|PRIME_RUNS_MODE)'` | nothing |
| other runs | `docker ps -a --filter label=verifiers.run`; `docker images physim2-ring` | nothing. Save the output of `docker ps -a` and `docker images` as the baseline |
| room | free disk; Docker Desktop: Settings, Resources | 5 GB free; 4 CPUs; the virtual disk limit is BELOW the Mac's free space |
| network | VPN, TLS-intercepting proxy | none (the image build needs a direct connection) |

## 0. Verify the code (seconds)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && git rev-parse HEAD && git status --porcelain -- . ../../round5/agentenv ../../../vw1 | wc -l
```

Expected: two lines, the pinned commit and `0` (macOS pads the number with spaces).

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && shasum -a 256 PIN.sha256 && shasum -a 256 -c PIN.sha256 > /dev/null && echo PIN-OK
```

Expected: the hash of the pin block followed by `PIN.sha256`, then `PIN-OK`. `PIN.sha256` lists the sha256 of
every file the pilot executes or imports (the package, the tools, the agents, the configs, round 5's `agentenv`
and the `vw` library); a changed or missing file prints `FAILED` lines and no `PIN-OK`: stop.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}}' | wc -l && docker images -q physim2-ring:1 | wc -l && ls -d "$HOME/physim2-pilot-20261110" "$HOME/physim2-pilot-20261110-results" .venv 2>&1 | grep -c "No such file"
```

Expected: Docker's version, then `0` (no container of this pilot), `0` (no image of that name yet), `3` (neither
pilot folder nor a `.venv` exists). Anything else: stop.

## 1. Install (about 10 minutes, most of it the image build)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f pyproject.toml && test -f uv.lock && cd / && uv sync --project "/ABSOLUTE/PATH/TO/vfport" --locked --python 3.12 --dry-run 2>&1 | grep -E "project environment|Would (download|install)|error"
```

Expected, first line, exactly: `Would create project environment at: /ABSOLUTE/PATH/TO/vfport/.venv` with your
path. Then `Would download ...` and `Would install ...` lines. If the first line says `Would replace` or `Would
use`, or names any other path, or an `error` line appears: **stop** (finding A1: `uv sync` deletes and recreates
the environment it names). Nothing was changed by this command.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f pyproject.toml && test -f uv.lock && uv sync --project "/ABSOLUTE/PATH/TO/vfport" --locked --python 3.12 2>&1 | tail -n 3
```

Expected: three lines that begin with ` + ` (the last of the installed packages); no line with `error`. This is
the only `uv` command that changes anything; no later command uses `uv`.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B -c "import verifiers, numpy, scipy, jax, physim2_env, physim2_script; print(verifiers.__version__, numpy.__version__, scipy.__version__, jax.__version__, physim2_env.__file__)"
```

Expected: `0.3.2.dev163 2.5.4 1.18.1 0.12.0.1 /ABSOLUTE/PATH/TO/vfport/physim2_env/__init__.py` with your path.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && mkdir "$HOME/physim2-pilot-20261110" && mkdir "$HOME/physim2-pilot-20261110/scratch" && (test -e docker/extra-ca.crt || : > docker/extra-ca.crt) && wc -c docker/extra-ca.crt
```

Expected: `0 docker/extra-ca.crt`. (`mkdir` fails if a pilot folder exists already, and nothing after it runs:
stop. A number other than 0 means somebody's certificate file is there: stop.)

The image build takes minutes, so it runs detached:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( nohup docker build -f docker/Dockerfile.ring -t physim2-ring:1 docker/ > "$HOME/physim2-pilot-20261110/scratch/build.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/build.log" ) > /dev/null 2>&1 < /dev/null & }
```

Status (repeat until the log's last line is `EXIT 0`; any other `EXIT` line: stop):

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && tail -n 2 "$HOME/physim2-pilot-20261110/scratch/build.log"
```

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker run --rm --network none --label verifiers.run=physim2-pilot-20261110 physim2-ring:1 python -c "import numpy, scipy, jax; print(numpy.__version__, scipy.__version__, jax.__version__)"
```

Expected: `2.5.4 1.18.1 0.12.0.1`. This is the ONE image of every box. Do not build
`docker/Dockerfile.network`: verifiers builds its own helper image at the first rollout.

The hidden side lives in a store OUTSIDE the repository. Make one fresh ring instance (a new secret and a new
hidden theta are drawn now; about 10 s):

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
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && { tail -n 4 "$HOME/physim2-pilot-20261110/scratch/prove.log" "$HOME/physim2-pilot-20261110/scratch/probe.log" "$HOME/physim2-pilot-20261110/scratch/single.log" 2>/dev/null ; echo "containers:" ; docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' ; echo "processes:" ; ps axo pid=,command= | grep "/ABSOLUTE/PATH/TO/vfport/.venv/bin/[p]ython" ; echo "status done" ; }
```

It prints the last lines of the logs that exist (each under a line `==> <file> <==`), then under `containers:`
the containers of this pilot, under `processes:` the processes of this pilot (the tool, its vf-eval, the
laboratory; each line starts with the pid and goes on with the whole command), and `status done`. A step is finished when its log ends with an `EXIT` line and nothing is listed under
`containers:` and `processes:`. While a step runs, wait and ask again; start nothing else.

### 2a. One world, three policies, then C once more with one box per exam item (about 10 minutes)

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/prove.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/proof" --worlds 1 --prefix mac-ring --policies D,P0,C --box-check C --no-cross-check --out "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" > "$HOME/physim2-pilot-20261110/scratch/prove.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/prove.log" ) > /dev/null 2>&1 < /dev/null & }
```

It prints Docker's version and returns at once (the tool runs on, detached). Then use the status command.
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

Then the status command. When `probe.log` ends with `EXIT 0`, the line before it is one JSON object. Expected
on the Mac:

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

Then the status command until `single.log` ends with `EXIT 0` (it shows the last four lines of that log: here the
end of the trace that vf-eval prints with `--no-rich`, three lines of token counts). Do not open `single.log` or
`traces.jsonl` beyond that: in step 3 the same files hold the examined model's text, and step 3 has a status
command of its own that shows the `EXIT` line only. Read a run only through the report tool, which prints fixed
fields and counts:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && "/ABSOLUTE/PATH/TO/vfport/.venv/bin/python" -B tools/run_report.py --store "$HOME/physim2-pilot-20261110/store" --run-dir "$HOME/physim2-pilot-20261110/scratch/single/single-d"
```

Expected: `"1_ok": true`, `"1_reward_present": true`, both `network_restricted` true, `"2_single_use": true`,
`"2_item_isolation": "box"`, `"3_lab"."ticks_used": 392`, `"4_submission_source": "agent_submission"`,
`"5_validation_ok": true`, `"5_n_items": 64`, `"5_n_failed": 0`, `"5_item_boxes": 64`,
`"5_infrastructure_failed_items": 0`, and `"total_hits": 0` under `6_hidden_values_in_the_run_folder`.

After step 2: report, and stop. Step 3 needs the lead.

## If a run was interrupted

Use this whenever a step did not end with `EXIT 0`: the Mac slept, Docker Desktop stopped, a command was cut,
the session was restarted, you were told to stop. Do exactly this, in this order, and nothing else. In
particular do not start the step again before the end of this section.

1. **What is still there?** Run the status command of step 2. It lists the pilot's processes and the pilot's
   containers. Nothing of anybody else can be in either list: the processes are the ones whose command starts
   with this study folder's own `.venv/bin/python`, the containers the ones that carry this pilot's run label.
   (Do not list by the name `vf-`: other verifiers runs on this Mac use the same names.)
2. **A tool or a vf-eval of the pilot is still running** (a line with `tools/prove.py`, `tools/check_probe.py` or
   `.venv/bin/vf-eval`): tell it to stop, once, by the pid at the start of ITS line. Take the tool's pid if a
   tool is listed, otherwise vf-eval's:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && kill -TERM PID_FROM_THE_STATUS_LINE
   ```

   The tool passes the signal on; vf-eval removes its containers and stops its laboratory itself (4 seconds in
   the cloud rehearsal; allow two minutes). The tool's log then ends with a Python traceback whose last line is
   `KeyboardInterrupt`, and `EXIT 130`. Ask for the status again until those lines are gone. Send the signal
   once; never `kill -9`, never a second process in the same command.
3. **Containers of the pilot are still listed and no vf-eval of the pilot is running** (vf-eval was killed before
   it could clean up; the tool's log then ends with `EXIT 1`): remove each one by its exact name, one command per
   container, the name copied from the status output:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker rm -f NAME_FROM_THE_STATUS_LINE
   ```

4. **A laboratory process is still listed** (a line ending in `-m physim2_env.lab_tools`) **and no vf-eval is**:
   stop it by its pid with the `kill -TERM` command of point 2. It holds no state worth keeping.
5. Run the status command again. Expected now: no process line, no container line. If something of the pilot
   is still listed after two minutes: stop and report.
6. **Delete the two pilot folders and start again from the instance.** A cut rollout has spent its laboratory
   budget and its instance cannot be opened again by the same agent, so the store is not reusable:

   ```sh
   cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch" && mkdir "$HOME/physim2-pilot-20261110/scratch" && echo "pilot folders reset"
   ```

   Expected: `pilot folders reset`. (If the interruption came before `make_instances`, the store does not exist
   and this prints nothing: then delete nothing and go on.) Then continue from the `make_instances` command of
   step 1, and run step 2 from 2a. The image and `.venv` stay.
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

It can be run ONCE: `single_use` refuses a second rollout of this model and harness on `mac-ring-w0`.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker info --format '{{.ServerVersion}}' && { ( VF_RUN_ID=physim2-pilot-20261110 PHYSIM2_STORE="$HOME/physim2-pilot-20261110/store" PRIME_RUNS_MODE=disabled PYTHONDONTWRITEBYTECODE=1 nohup "/ABSOLUTE/PATH/TO/vfport/.venv/bin/vf-eval" @ configs/qwen_ring_bash.toml --no-rich --run.name qwen -o "$HOME/physim2-pilot-20261110/scratch/qwen" > "$HOME/physim2-pilot-20261110/scratch/qwen.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/physim2-pilot-20261110/scratch/qwen.log" ) > /dev/null 2>&1 < /dev/null & }
```

---

While it runs (up to an hour, then about 3 minutes of grading), ask for its state with this command only:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && { tail -n 1 "$HOME/physim2-pilot-20261110/scratch/qwen.log" | cut -c 1-12 ; echo "containers:" ; docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' ; echo "processes:" ; ps axo pid=,command= | grep "/ABSOLUTE/PATH/TO/vfport/.venv/bin/[p]ython" | cut -c 1-160 ; echo "status done" ; }
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

## 4. After the pilot

The store holds theta and the secret of a pilot that must never be reused. First run the status command of step
2: nothing may be listed. Then copy the results out and remove exactly the two folders, in ONE command, so that
nothing is deleted unless every check and every copy before it succeeded:

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && test -f "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" && test -f "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" && mkdir "$HOME/physim2-pilot-20261110-results" && cp "$HOME/physim2-pilot-20261110/scratch/proof_mac.json" "$HOME/physim2-pilot-20261110/scratch/proof_mac_items.npz" "$HOME/physim2-pilot-20261110/scratch/probe_mac.json" "$HOME/physim2-pilot-20261110/scratch/prove.log" "$HOME/physim2-pilot-20261110/scratch/probe.log" "$HOME/physim2-pilot-20261110-results/" && test -s "$HOME/physim2-pilot-20261110-results/proof_mac.json" && test -s "$HOME/physim2-pilot-20261110-results/probe_mac.json" && rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch" && rmdir "$HOME/physim2-pilot-20261110" && ls "$HOME/physim2-pilot-20261110-results"
```

Expected: the five file names. If it prints nothing, nothing was deleted: stop and report. The copied files
hold scores, counters and commitments only (`PILOT_NEVER_REUSE_AS_EXAM`); the run folders with their traces are
deleted with the scratch folder (a trace names the operator's account), and after step 3 the output of
`tools/run_report.py` is what leaves the Mac.

```sh
cd "/ABSOLUTE/PATH/TO/vfport" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' | wc -l && docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}'
```

Expected: `0`, then the images. Compare `docker ps -a` and `docker images` with the baseline of the by-hand
checks: the pilot added `physim2-ring:1`, `python:3.12-slim`, `localhost/verifiers-network:1` and `alpine:3.22`
and no container. Keep the images: `localhost/verifiers-network:1` is shared with other verifiers work on this
Mac and is not this pilot's to remove; `physim2-ring:1` may be removed by the lead, by hand, when no further run
is planned (`docker rmi physim2-ring:1`). The `.venv` stays until the lead removes the checkout.

## What the cloud rehearsal could not cover

- macOS and Docker Desktop: nothing. Inferred, not seen: that containers there carry `/.dockerenv` and Docker's
  usual mount table (if not, staging stops with `the box is not recognised as a disposable box` and names the
  mount or the missing sign; nothing is damaged; report it), how `uv` behaves, how a Claude session on the Mac
  ends a command at its limit, that a detached command survives the end of the call that started it.
- The image build of step 1: the cloud machine sits behind a TLS-intercepting proxy and already had the shared
  image `physim2-ring:1`, at which step 0 says stop; the rehearsal went on with that image and did not run the
  build command (`results/rehearsal_round1.json`, deviations).
- Step 2c as written: the cloud machine's kernel has no IPv6, so a direct `vf-eval` needs `tools/docker_shim` first
  on PATH there (the tools of 2a and 2b add it themselves on such Linux hosts); the rehearsal added it to that
  one command. This does not apply to macOS, where the shim must not be used.
- The by-hand checks: the cloud session is root, on x86_64, with `UV_NATIVE_TLS` set.
- Step 3: never run.
