"""The PhySim v2 exam as a verifiers taskset: task hooks only; execution is stock verifiers v1.

Run it under the stock isolated grader (`--env.id isolated-verifier`) on a container runtime with the declared
network policy. What happens, and where:

  worker (vf-eval process, trusted)   this module: setup, finalize, the reward; the instance store
  laboratory (host process, trusted)  lab_tools.LabTools, one per rollout, started by verifiers
  agent box (container)               TASK.md, the public physim2 package, submission/ with the null baseline;
                                      its only ways out are the model route and the laboratory's URL
  verifier box (fresh container)      the public package again, the frozen submission/, the public driver;
                                      no network; the predictor as an unprivileged user; here run the three
                                      public validation calls (an invalid predictor falls back to the null policy)
  item boxes (fresh containers)       one per exam item (default), provisioned by the reward through verifiers'
                                      `provision_runtime` with the verifier box's own config and staged the
                                      same way, so that nothing in a box can carry from one item to the next

A task row carries pointers only (instance id, world, config name, the public commitment of the secret): rows
are saved in every trace. Hidden values are read on the worker from the store, by the laboratory and the reward.

Round 4 (the coordinator's rulings E1 to E10, after the first model rollout):

  E1  whatever is in submission/ when the run ends is graded: `finalize` collects it at every ending verifiers
      treats as a stop (submit, turn limit, time limit, token limits, a clean exit), with no attempt cap; for a
      run that FAILED, where verifiers calls no task hook, `recover` hands the env physim2_verifier the last
      checkpoint the task controller took (access.py). The graded copy and a size-capped copy of /workspace go
      to <store>/<instance>/captures/<rollout>/ through capture.py, the one writer of box content.
  E2  the box starts with the null policy in submission/ (bundle.py).
  E3  a failed item is scored with the null policy's forecast, never K (grading.py).
  E4, E8  the statement an agent reads is rendered at setup from the run's resolved config (turns, wall time,
      tokens per reply) and from the limits measured in its box (CPUs, memory, processes); the first message
      carries the same text. `lab.usage()` reports seconds and turns, used and left.
  E10 the trace records whether reasoning was asked for and whether replies carried any.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import math
import os
import time
from typing import Literal

import verifiers.v1 as vf
from pydantic import Field

from . import access as ACCESS
from . import bundle as BUNDLE
from . import capture as CAPTURE
from . import grading as GRADING
from . import profiles as PROFILES
from . import runtime as RUNTIME
from . import spend as SPEND
from . import store as STORE
from .lab_tools import LabTools, LabToolsConfig

# ---- round 4, fixer B: the box caps and the bearer-carrying proxy are put in place before any box can start ----
RUNTIME.install()
SPEND.install()                                              # every model call passes the spend meter, or none is made

WORKDIR = "/workspace"
PROMPT = ("Your task is described in /workspace/TASK.md (the same text follows). Work in /workspace. A working baseline is "
          "already in /workspace/submission; whatever is in that directory when your run ends is graded, so improve it in "
          "place. The limits of your run are in section 4.\n\n")
MIB = 1 << 20
GIB = 1 << 30
# One command, as root in a box nobody else has used yet: what the runtime really set (cgroup v2, then v1).
MEASURE = ("for f in /sys/fs/cgroup/cpu.max /sys/fs/cgroup/memory.max /sys/fs/cgroup/pids.max "
           "/sys/fs/cgroup/cpu/cpu.cfs_quota_us /sys/fs/cgroup/cpu/cpu.cfs_period_us /sys/fs/cgroup/memory/memory.limit_in_bytes "
           "/sys/fs/cgroup/pids/pids.max; do printf '%s=' \"$f\"; (cat \"$f\" 2>/dev/null || echo absent) | head -c 64 | tr '\\n' ' '; echo; done; "
           "printf 'nproc='; (nproc 2>/dev/null || echo absent)")


def parse_box(text: str) -> dict:
    """{"cpus", "memory_gib", "pids"} from MEASURE's output; None where the runtime set no limit. Pure."""
    kv = {}
    for line in str(text).splitlines():
        k, sep, v = line.partition("=")
        if sep:
            kv[k.strip()] = v.strip()

    def num(v):
        try:
            return int(v)
        except (TypeError, ValueError):
            return None
    out = {"cpus": None, "memory_gib": None, "pids": None, "nproc": num(kv.get("nproc"))}
    cpu = (kv.get("/sys/fs/cgroup/cpu.max") or "").split()
    if len(cpu) == 2 and num(cpu[0]) and num(cpu[1]):
        out["cpus"] = round(int(cpu[0]) / int(cpu[1]), 3)
    else:
        q, per = num(kv.get("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")), num(kv.get("/sys/fs/cgroup/cpu/cpu.cfs_period_us"))
        if q and per and q > 0:
            out["cpus"] = round(q / per, 3)
    mem = num(kv.get("/sys/fs/cgroup/memory.max"))
    if mem is None:
        mem = num(kv.get("/sys/fs/cgroup/memory/memory.limit_in_bytes"))
    if mem and 0 < mem < (1 << 50):                          # cgroup v1 writes a huge number for "no limit"
        out["memory_gib"] = round(mem / GIB, 3)
    pids = num(kv.get("/sys/fs/cgroup/pids.max"))
    if pids is None:
        pids = num(kv.get("/sys/fs/cgroup/pids/pids.max"))
    if pids and pids > 0:
        out["pids"] = pids
    return out


class Physim2State(vf.State):
    # Host-only: `state` is excluded from saved traces (verifiers/v1/trace.py:412-417).
    access: dict = Field(default_factory=dict)               # socket of the task controller (announce, check, freeze)
    rollout: str = ""                                        # names this rollout's records in the store
    uid: int = 0                                             # the predictor's uid in this rollout's grading boxes
    finalized: bool = False                                  # set by finalize: setup then runs in verifier mode
    collection: dict = Field(default_factory=dict)           # how submission/ was obtained (no file content)
    task_md: str = ""                                        # the statement of THIS run, as written into its boxes


class LimitsConfig(vf.BaseConfig):
    """What a run is promised and held to, beyond what verifiers' own agent config says (turns, wall time and
    tokens per reply are read from that config at setup). tools/vfrun.py fills these from a rollout config."""
    box_cpus: float | None = Field(None, gt=0, le=64)
    """CPU cores of every box (default: the profile's). Becomes the task's resource request; a runtime config
    that names another number wins, and the statement always shows what was measured in the box."""
    box_memory_gb: float | None = Field(None, gt=0, le=64)
    """Memory of every box in GB (default: the profile's)."""
    max_context_tokens: int | None = Field(None, ge=1024)
    """Disclosed in the statement. Enforced on the worker by the spend stop, not here."""
    cap_usd: float | None = Field(None, gt=0)
    """Disclosed in the statement. Enforced on the worker by the spend stop, not here."""


class Physim2TaskConfig(vf.TaskConfig):
    tools: LabToolsConfig = LabToolsConfig()
    single_use: bool = True
    """Refuse an instance that the SAME agent already opened (a rerun would hand it a fresh laboratory budget;
    round 5 refused a reused rollout name, run_rollout.py:66-67). The agent is named by `agent_key`. Every
    opening is recorded in the store whatever this flag says."""
    agent_key: str = ""
    """Who is examined, for `single_use` (default: "<model>|<harness id>" of the rollout). Reference policies run
    by the evaluator on the same instance get distinct keys (tools/vfrun.py: the run name)."""
    item_isolation: Literal["box", "shared"] = "box"
    """"box": every exam item runs in a fresh container of its own (nothing in a box survives to the next item).
    "shared": all items in the one verifier box with the driver's cleanup between them: cheaper, for pilots and
    reference tables; timestamps, the process-id counter and kernel counters of the box survive that cleanup, so
    a rollout graded this way is marked `between_item_state: possible` in its trace."""
    item_boxes_parallel: int = Field(1, ge=1, le=16)
    """With item_isolation "box": how many item boxes may exist at once."""
    box_env_allow: list[str] = Field(default_factory=list)
    """Extra variable NAMES the operator may pass into a box (harness env, forward_env, verifier env) besides
    BOX_ENV_ALLOW. Anything else is refused at setup: a box is no place for a credential, whatever its name."""
    item_cleanup: bool = True
    """TEST HOOK. False skips the cleanup between items so that a probe can show what the cleanup prevents;
    such a rollout is marked NOT_AN_EXAM in its trace."""
    stock_collection: bool = False
    """TEST HOOK. True leaves the collection of submission/ to verifiers' default (collect after finalize), to
    show which agent actions then end a rollout without a grade; marked NOT_AN_EXAM in the trace."""
    grading_seed: int = 0
    limits: LimitsConfig = LimitsConfig()
    checkpoint_seconds: float = Field(30.0, ge=0, le=600)
    """How often the task controller looks whether submission/ changed and keeps a frozen copy (it also looks
    before every model call). 0 turns the timer off. The copy is what a FAILED run is graded on (ruling E1)."""
    spend: SPEND.SpendConfig = SPEND.SpendConfig()
    """Round 4, fixer B. The model's listed prices and the caps of the spend stop (physim2_env/spend.py), written
    by tools/vfrun.py for a model run. Empty in a scripted run: then no model call can leave vf-eval."""


class Physim2Config(vf.TasksetConfig):
    task: Physim2TaskConfig = Physim2TaskConfig()
    store: str = ""
    """Instance store on the worker (default $PHYSIM2_STORE)."""
    index: str = ""
    """Public index of instances (default <store>/index.json)."""
    instances: list[str] | None = None
    """Instance ids to load (default: every row of the index)."""
    image: str = "physim2-ring:2"
    """The one image of both boxes (docker/Dockerfile.ring)."""


class Physim2Data(vf.TaskData):
    # Pointers and public declarations only. Never a hidden value: the row is saved in every trace.
    instance_id: str
    world: str
    config_name: str
    secret_commitment: str = Field(pattern=r"^[0-9a-f]{64}$")


BOX_ENV_ALLOW = {"PHYSIM2_AGENT_HOME", "PHYSIM2_PROBE_PATHS", "PYTHONDONTWRITEBYTECODE", "PYTHONUNBUFFERED",
                 "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "JAX_PLATFORMS", "XLA_FLAGS",
                 "LANG", "LC_ALL", "TZ", "TERM"}


def reasoning_record(trace) -> dict:
    """Ruling E10: was the model's reasoning on, and at what effort, as far as the request and the replies show.
    `requested_effort` is what this run's config asked for (None: nothing was sent, the provider's default
    applies); the counts come from the replies saved on the trace. Numbers and fixed words only."""
    acfg = getattr(getattr(trace, "agent", None), "config", None)
    sampling = getattr(acfg, "sampling", None)
    effort = getattr(sampling, "reasoning_effort", None)
    replies = with_text = with_state = with_tokens = 0
    tokens = None
    for node in getattr(trace, "nodes", None) or []:
        if not getattr(node, "sampled", False):
            continue
        replies += 1
        msg = getattr(node, "message", None)
        if getattr(msg, "reasoning_content", None):
            with_text += 1
        if getattr(msg, "provider_state", None):
            with_state += 1
        n = getattr(getattr(node, "usage", None), "reasoning_tokens", None)
        if isinstance(n, int) and not isinstance(n, bool):
            tokens = (tokens or 0) + n
            with_tokens += 1 if n > 0 else 0
    seen = bool(with_text or with_state or with_tokens)
    return {"requested_effort": effort if isinstance(effort, str) and effort.isalnum() and len(effort) <= 16 else None,
            "replies": replies, "replies_with_reasoning_text": with_text, "replies_with_reasoning_state": with_state,
            "replies_with_reasoning_tokens": with_tokens, "reasoning_tokens": tokens,
            "reasoning_seen_in_replies": seen if replies else None,
            "reasoning_tokens_reported": tokens is not None}


def agent_identity(trace, configured: str = "") -> str:
    if configured:
        return configured
    cfg = getattr(getattr(trace, "agent", None), "config", None)
    harness = getattr(getattr(cfg, "harness", None), "id", None)
    return f"{getattr(cfg, 'model', None) or 'model?'}|{harness or 'harness?'}"


class Physim2Task(vf.Task[Physim2Data, Physim2State, Physim2TaskConfig]):
    NEEDS_CONTAINER = True

    def __init__(self, data, config=None):
        super().__init__(data, config)
        self._access: dict[str, ACCESS.BoxAccess] = {}

    @property
    def key(self):
        return f"{self.data.instance_id}:{self.data.secret_commitment[:16]}"

    # ---- guard 1 (memo hole 4; v1 taskset.py:453-454): the laboratory stays in its trusted host process ----
    @classmethod
    def toolsets(cls, config):
        t = config.tools
        if t.colocated or t.runtime.type != "subprocess" or t.url:
            raise ValueError("the PhySim laboratory must run in its trusted host process: no colocated placement, "
                             "no sandbox runtime, no external url")
        return [LabTools(t)]

    def runtime_env(self):
        return {}                                            # nothing of the worker's environment enters a box

    def _hidden(self) -> str:
        return STORE.hidden_dir(STORE.store_root(self.config.tools.store), self.data.instance_id)

    def _limits(self) -> dict:
        return BUNDLE.load_config(self.data.config_name)["predictor"]

    async def setup(self, trace, runtime):
        # ---- guard 2 (v1 taskset.py:461-462): a container with framework-only network, or nothing ----
        if runtime.config.type not in ("docker", "prime") or not runtime.config.network_restricted:
            raise vf.TaskError("PhySim v2 requires a Docker or Prime runtime with framework-only network access")
        gate = GRADING.container_gate(runtime)               # the real runtime object, provisioned by verifiers for this run
        if gate:
            raise vf.TaskError("PhySim v2 runs only in a box that verifiers itself provisioned: " + "; ".join(gate))
        # ---- round 4, fixer B: a Docker box must carry the pilot's caps, read back from the engine at its start ----
        capped = RUNTIME.caps_of(runtime)
        if runtime.config.type == "docker" and not (capped and capped.get("verified")):
            raise vf.TaskError("PhySim v2 runs only in a box started with the pilot's caps (physim2_env/runtime.py)")
        # ---- guard 3: only allow-listed variable names may be configured for a box (a credential under any
        #      name, GITHUB_PAT or HF_KEY as much as HF_TOKEN, has no business in one) ----
        harness = getattr(getattr(trace.agent, "config", None), "harness", None)
        names = list(runtime.env) + list(getattr(harness, "env", {}) or {}) + list(getattr(harness, "forward_env", []) or [])
        allow = BOX_ENV_ALLOW | set(self.config.box_env_allow)
        refused = sorted(n for n in set(names) if n not in allow or STORE.token_like([n]))
        if refused:
            raise vf.TaskError(f"{len(refused)} variable(s) configured for a box are not on the allow-list (runtime env, harness "
                               "env or forward_env); see Physim2TaskConfig.box_env_allow")
        hidden = self._hidden()
        inst = json.load(open(os.path.join(hidden, "instance.json")))
        cfg = BUNDLE.load_config(self.data.config_name)
        if inst["secret_commitment"] != self.data.secret_commitment or inst["world"] != self.data.world \
                or inst["config"] != cfg:
            raise vf.TaskError("the stored instance differs from the task row (commitment, world or config)")
        del inst
        state = trace.state
        info = await self._public_files(runtime, state.uid if state.finalized else None, state.task_md if state.finalized else None)
        if state.finalized:                                  # the verifier box: public files only, no laboratory
            trace.info.setdefault("physim2", {})["verifier_started_unix"] = time.time()
            trace.info["physim2"]["verifier_box_caps"] = (capped or {}).get("caps")
            return
        # ---- the statement of THIS run (rulings E4, E8), before the instance is opened: what the run's resolved
        #      config says and what the runtime really set in this box. It replaces the bundle's TASK.md and the
        #      first message, so the limits an agent reads are the limits that bind. ----
        run = await self._run_facts(trace, runtime, harness)
        state.task_md = BUNDLE.statement(self.data.world, self.data.config_name, run)
        await runtime.write(f"{WORKDIR}/TASK.md", state.task_md.encode())
        r = await runtime.run(["sh", "-c", f"chown 0:0 {WORKDIR}/TASK.md && chmod 644 {WORKDIR}/TASK.md"], {})
        if r.exit_code:
            raise vf.TaskError("could not write the task statement into the box")
        trace.task.data = trace.task.data.model_copy(update={"prompt": PROMPT + state.task_md})
        # ---- single use: one laboratory budget per agent and instance (memo hole 3) ----
        key = agent_identity(trace, self.config.agent_key)
        opened = os.path.join(hidden, "opened")
        os.makedirs(opened, exist_ok=True)
        marker = os.path.join(opened, hashlib.sha256(key.encode()).hexdigest()[:32] + ".json")
        try:
            fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            if self.config.single_use:
                raise vf.TaskError("this instance was already opened by this agent (single_use): a rerun would hand it "
                                   "a fresh laboratory budget") from None
        else:
            with os.fdopen(fd, "w") as f:
                json.dump({"agent_key": key, "first_rollout": trace.id, "time": time.time()}, f)
        box = ACCESS.BoxAccess(runtime, list(self.data.artifacts), self.data.artifact_max_bytes, cfg["predictor"]["artifact_mib"],
                               WORKDIR, cfg["predictor"], trace=trace, max_turns=run["max_turns"], wall_s=60.0 * run["wall_minutes"],
                               capture_dir=self._captures(trace.id), checkpoint_s=self.config.checkpoint_seconds)
        self._access[trace.id] = box
        # the first checkpoint is the baseline itself, known without asking the box: a run that fails before
        # anything else could be copied is graded on what its box started with
        base = ACCESS.frozen_files(BUNDLE.baseline_files(self.data.world, self.data.config_name), f"{WORKDIR}/submission",
                                   cfg["predictor"]["artifact_mib"])
        if base["ok"]:
            box.keep(base, "the baseline at setup")
        state.access = await box.start()
        state.rollout = trace.id
        # ---- round 4, fixer B: the spend meter of a model run (None in a scripted run) ----
        try:
            meter = SPEND.meter_for(self.config.spend, getattr(self.config, "limits", None), trace=trace)
        except ValueError as e:
            raise vf.TaskError(str(e)) from None
        if meter is not None:
            SPEND.METERS[trace.id] = meter
        trace.info["physim2"] = {
            "instance_id": self.data.instance_id, "world": self.data.world, "config_name": self.data.config_name,
            "secret_commitment": self.data.secret_commitment, "bundle": {k: info[k] for k in ("files", "bytes", "manifest_sha256")},
            "baseline": info["baseline"], "limits": dict(run, statement_sha256=hashlib.sha256(state.task_md.encode()).hexdigest()),
            "verifiers_version": __import__("verifiers").__version__, "runtime": runtime.config.type,
            "network_restricted": bool(runtime.config.network_restricted), "single_use": bool(self.config.single_use),
            "agent_key": key, "item_isolation": self.config.item_isolation,
            "box_caps": (capped or {}).get("caps"), "lab_bearer_required": True}

    def _captures(self, rollout: str) -> str:
        """The run's own folder of the store, outside hidden/: <store>/<instance>/captures/<rollout>."""
        return os.path.join(STORE.store_root(self.config.tools.store), self.data.instance_id, "captures", STORE.safe_name(rollout))

    async def _run_facts(self, trace, runtime, harness) -> dict:
        """The limits of this run, for its statement and its record: turns, wall time and tokens per reply from
        the seat's resolved config (the values verifiers enforces), context and spend from the task config (the
        values the worker's spend stop enforces), and the box as measured in it."""
        acfg = getattr(trace.agent, "config", None)
        rollout_s = getattr(getattr(acfg, "timeout", None), "rollout", None) or self.data.timeout.agent
        sampling = getattr(acfg, "sampling", None)
        declared = BUNDLE.default_run(self.data.world, self.data.config_name, self.config.limits.model_dump())
        scripted = getattr(harness, "id", None) == "physim2-script"      # a script takes no turns and writes no replies
        run = {"max_turns": getattr(acfg, "max_turns", None),
               "wall_minutes": round(float(rollout_s) / 60.0, 3) if rollout_s else declared["wall_minutes"],
               "max_output_tokens_per_turn": None if scripted else getattr(sampling, "max_tokens", None),
               "max_context_tokens": self.config.limits.max_context_tokens, "cap_usd": self.config.limits.cap_usd,
               "cpus": getattr(runtime.config, "cpu", None), "memory_gib": getattr(runtime.config, "memory", None),
               "pids": None, "scratch_gib": None, "lab_counts_turns": True, "measured": False,
               "harness": str(getattr(harness, "id", None) or "?")[:40]}
        try:
            r = await runtime.run(["sh", "-c", MEASURE], {})
            box = parse_box(r.stdout) if r.exit_code == 0 else None
        except Exception:
            box = None
        if box is not None:
            configured = {"cpus": run["cpus"], "memory_gb": run["memory_gib"]}
            run.update(cpus=box["cpus"], memory_gib=box["memory_gib"], pids=box["pids"], measured=True, nproc=box["nproc"],
                       configured=configured)
        return run

    async def _public_files(self, runtime, uid: int | None = None, task_md: str | None = None) -> dict:
        """TASK.md, the public physim2 package and submission/ with the null baseline into a box (any of the
        three kinds), and the marker of a prepared box: /etc/physim2/predictor_uid. In the agent's box, where only
        the agent's own validation uses it, the number is drawn here from the reserved range (never 1000, the
        first account of most machines); the grading boxes get the rollout's uid, here and again at staging.
        `task_md`: the run's own statement, for the grading boxes (the agent's box gets it in setup). In a grading
        box verifiers then replaces submission/ with the frozen copy."""
        GRADING.require_container(runtime)
        uid = int(uid) if uid else GRADING.new_uid()
        raw, info = BUNDLE.public_bundle(self.data.world, self.data.config_name)
        await runtime.write("/tmp/physim2-workspace.tar", raw)
        r = await runtime.run(["sh", "-c", f"umask 022; mkdir -p {WORKDIR} {GRADING.BOX_DIR} && chmod 755 {WORKDIR} {GRADING.BOX_DIR} && "
                                            f"echo {uid} > {GRADING.BOX_DIR}/predictor_uid && chmod 644 {GRADING.BOX_DIR}/predictor_uid && "
                                            f"tar -xf /tmp/physim2-workspace.tar -C {WORKDIR} && rm -f /tmp/physim2-workspace.tar"], {})
        if r.exit_code:
            raise vf.TaskError("could not build the workspace in the box")
        if task_md:
            await runtime.write(f"{WORKDIR}/TASK.md", task_md.encode())
        return info

    async def finalize(self, trace, runtime):
        """Runs in the agent's box after the harness ended and the laboratory stopped, at every ending that
        verifiers treats as a stop: an accepted submit, the turn limit, the time limit, a token limit, a clean
        exit. Collects the submission defensively and never raises: whatever the agent did to its box, the
        rollout stays gradable (hole 3). What is collected is what is graded (ruling E1): the copy an accepted
        submit froze, else submission/ as it is NOW, with no cap on attempts."""
        state = trace.state
        info = trace.info.setdefault("physim2", {})
        box = self._access.pop(trace.id, None)
        frozen = None
        try:
            if self.config.stock_collection:
                info["NOT_AN_EXAM"] = "the defensive collection was disabled by the operator (test hook)"
                raise LookupError("stock collection")
            cfg = BUNDLE.load_config(self.data.config_name)
            if box is not None:
                box._closed = True                           # no further checkpoint beside the final collection
            frozen = box.frozen if box is not None and box.frozen is not None and box.frozen["ok"] else None
            source = "agent_submission" if frozen is not None else "final_collection"
            if frozen is None:
                frozen = await ACCESS.collect_frozen(runtime, list(self.data.artifacts), self.data.artifact_max_bytes,
                                                     cfg["predictor"]["artifact_mib"])
            if frozen["archive"] is not None:
                # verifiers' own check of what it will restore (utils/artifacts.py:208-290), HERE, inside the try:
                # an archive it would refuse later, after finalize, would end the rollout without a grade
                try:
                    from verifiers.v1.utils.artifacts import _validate_restore
                    _validate_restore(frozen["root"], frozen["archive"])
                except Exception as e:
                    frozen = dict(frozen, archive=None, ok=False, error=f"the frozen archive did not pass the restore check ({type(e).__name__})")
            # A non-empty mapping makes verifiers skip its own collection (rollout.py:501); None = nothing to restore.
            state.artifacts = {frozen["root"]: frozen["archive"]}
            man = frozen["manifest"]
            state.collection = {"source": source, "ok": frozen["ok"], "error": frozen["error"], "files": len(man["files"]),
                                "bytes": man.get("bytes", 0), "sha256": man.get("sha256")}
        except LookupError:
            state.collection = {"source": "verifiers_default", "ok": None, "error": None, "files": None}
        except Exception as e:
            state.artifacts = {f"{WORKDIR}/submission": None}
            state.collection = {"source": "none", "ok": False, "error": f"collection failed ({type(e).__name__})", "files": 0}
        # ---- for the record (never for the grade): the graded copy and a size-capped copy of /workspace ----
        try:
            info["capture"] = await self._record(trace, runtime, frozen)
        except Exception as e:
            info["capture"] = {"error": type(e).__name__}
        finally:
            state.access = {}
            state.finalized = True
            if box is not None:
                info["checkpoints"] = dict(box.checkpoints)
                try:
                    await box.close()
                except Exception:
                    pass
        info["submission"] = dict(state.collection)
        info["lab"] = self._lab_usage(state.rollout)
        meter = SPEND.METERS.pop(trace.id, None)             # round 4, fixer B: what the run cost, as counted on the host
        if meter is not None:
            info["spend"] = meter.summary()
        info["stop_condition"] = trace.stop_condition
        info["ended"] = self._ending(trace, info["lab"])
        info["reasoning"] = reasoning_record(trace)
        # read by a command inside the agent's box, where the agent is root: informational, NOT a trusted meter
        info["agent_box_cpu_s_unverified"] = await GRADING.box_cpu_seconds(runtime)
        state.uid = GRADING.new_uid()

    @staticmethod
    def _ending(trace, lab: dict) -> str:
        """How the run ended, in one of a few fixed words (the graded copy is the same in every case: what was
        in submission/ at that moment)."""
        stop = trace.stop_condition
        if lab.get("submitted"):
            return "submit"
        if stop == "max_turns":
            return "turn limit"
        if isinstance(stop, str) and "timeout" in stop:
            return "time limit"
        if stop in ("max_input_tokens", "max_output_tokens", "max_total_tokens"):
            return "token limit"
        if stop == "agent_completed":
            return "the agent stopped"
        return "stopped" if stop else "ended"

    async def _record(self, trace, runtime, frozen) -> dict:
        """Write the graded copy of submission/ and a size-capped copy and listing of the working directory into
        the run's folder of the store, through capture.extract (regular files only, sanitised names, 20 MiB and
        2000 files per copy, nothing outside the folder). Returns counts for the trace; names stay in the store."""
        root = os.path.join(self._captures(trace.id), "final")
        os.makedirs(os.path.dirname(root), mode=0o700, exist_ok=True)
        os.mkdir(root, 0o700)                                # once per run: a second finalize of the same run writes nothing
        out = {"folder": f"captures/{STORE.safe_name(trace.id)}/final"}
        man = CAPTURE.extract(frozen["archive"] if frozen else None, f"{WORKDIR}/submission", os.path.join(root, "submission"))
        man["graded_manifest_sha256"] = ((frozen or {}).get("manifest") or {}).get("sha256")
        with open(os.path.join(root, "submission.json"), "w") as f:
            json.dump(man, f, indent=1)
        out["submission"] = {k: man[k] for k in ("n_files", "bytes", "n_skipped", "complete", "archive")}
        ws = {"archive": "none"}
        raw, listing = None, None
        try:
            GRADING.require_container(runtime)
            path = f"/tmp/physim2-capture-{os.urandom(8).hex()}.tar"
            async with asyncio.timeout(120):
                r = await runtime.run(["sh", "-c", CAPTURE.workspace_command(WORKDIR, path)], {})
                if r.exit_code == 0:
                    raw = await runtime.read(path, max_bytes=CAPTURE.MAX_BYTES + (1 << 20))
                r = await runtime.run(["sh", "-c", CAPTURE.listing_command(WORKDIR)], {})
                listing = CAPTURE.parse_listing(r.stdout or "")
        except Exception as e:
            ws["error"] = type(e).__name__
        man = CAPTURE.extract(raw, "", os.path.join(root, "workspace"))
        with open(os.path.join(root, "workspace.json"), "w") as f:
            json.dump(dict(man, listing=listing), f, indent=1)
        out["workspace"] = dict(ws, **{k: man[k] for k in ("n_files", "bytes", "n_skipped", "complete", "archive")},
                                listed=None if listing is None else listing["n"])
        return out

    def recover(self, trace) -> dict | None:
        """For a run that FAILED (verifiers called neither finalize nor a collection): put the last checkpoint
        of submission/ on the trace's state as if finalize had collected it, so that the isolated grader can
        grade it. Returns the collection record, or None when the run never opened this instance. Called by the
        env physim2_verifier only; reads the worker's own store, never a box."""
        state = trace.state
        if not state.rollout or state.finalized:
            return None
        info = trace.info.setdefault("physim2", {})
        cfg = BUNDLE.load_config(self.data.config_name)
        got = ACCESS.read_checkpoint(self._captures(state.rollout), cfg["predictor"]["artifact_mib"])
        root = f"{WORKDIR}/submission"
        if got is None:
            state.artifacts = {root: None}
            state.collection = {"source": "none", "ok": False, "error": "no copy of submission/ was taken before the run failed", "files": 0}
        else:
            state.artifacts = {got["root"]: got["archive"]}
            man = got["manifest"]
            state.collection = {"source": "checkpoint", "ok": True, "error": None, "files": len(man["files"]), "bytes": man.get("bytes", 0),
                                "sha256": man.get("sha256"), "checkpoint": got["meta"]}
            try:
                folder = os.path.join(self._captures(state.rollout), "final")
                os.mkdir(folder, 0o700)
                rec = CAPTURE.extract(got["archive"], root, os.path.join(folder, "submission"))
                rec["graded_manifest_sha256"] = man.get("sha256")
                with open(os.path.join(folder, "submission.json"), "w") as f:
                    json.dump(rec, f, indent=1)
                info["capture"] = {"folder": f"captures/{STORE.safe_name(state.rollout)}/final",
                                   "submission": {k: rec[k] for k in ("n_files", "bytes", "n_skipped", "complete", "archive")},
                                   "workspace": {"archive": "none", "error": "the box was gone"}}
            except Exception as e:
                info["capture"] = {"error": type(e).__name__}
        state.access, state.finalized, state.uid = {}, True, GRADING.new_uid()
        info["submission"] = dict(state.collection)
        info["lab"] = self._lab_usage(state.rollout)
        info["stop_condition"] = trace.stop_condition
        info["ended"] = "failed run"
        info["reasoning"] = reasoning_record(trace)
        return dict(state.collection)

    def _lab_usage(self, rollout: str) -> dict:
        """Counters of the laboratory of this rollout (its process has stopped; its records are on the worker)."""
        try:
            d = os.path.join(self._hidden(), "labs", rollout)
            s = json.load(open(os.path.join(d, "state.json")))
            n_infra = sum(1 for line in open(os.path.join(d, "log.jsonl")) if '"kind": "infrastructure"' in line)
            return {"ticks_used": s["ticks_used"], "resets": s["resets"], "total_nats": s["total_nats"], "episodes": s["episodes"],
                    "requests": s["state"]["requests"], "rejected": s["state"]["rejected"], "validations": s["state"]["validations"],
                    "submissions": s["state"]["submissions"], "submitted": s["state"]["submitted"], "infrastructure_errors": n_infra}
        except Exception:
            return {"opened": False}

    @vf.stop
    async def frozen(self, trace: vf.Trace) -> bool:
        """End a model rollout once the agent has submitted: its graded copy is frozen and the laboratory is
        closed, so further turns can change nothing. (Checked before each model call; a scripted run has none.)
        Otherwise, before the model is called again: let the task controller keep a frozen copy of submission/
        if it changed. If the call that follows breaks the run, that copy is what is graded (ruling E1)."""
        try:
            f = os.path.join(self._hidden(), "labs", trace.state.rollout, "state.json")
            if bool(trace.state.rollout) and bool(json.load(open(f))["state"]["submitted"]):
                return True
        except Exception:
            pass
        box = self._access.get(trace.id)
        if box is not None:
            await box.checkpoint("before a model call")      # never raises
        return False

    @vf.stop
    async def spend_cap(self, trace: vf.Trace) -> bool:
        """Round 4, fixer B. End a model rollout when its counted cost, plus one worst-case call for every
        request still in flight, has reached cap_usd (physim2_env/spend.py). Checked before each model call, as
        `frozen` is; a stop, so finalize and scoring still run."""
        meter = SPEND.METERS.get(trace.id)
        return meter is not None and meter.exhausted()

    async def stage_verifier(self, trace, runtime):
        """After verifiers restored the frozen submission into the fresh box: trusted staging only."""
        if not trace.state.uid:
            trace.state.uid = GRADING.new_uid()
        staged = await GRADING.stage(runtime, WORKDIR, trace.state.uid)
        trace.info.setdefault("physim2", {})["verifier_box"] = {
            "has_predict": staged["has_predict"], "network_restricted": bool(runtime.config.network_restricted),
            "writable_dirs": staged["scan"].get("writable_dirs"), "world_writable_paths_fixed": staged["scan"].get("fixed"),
            "owned_by_predictor_user_before": len(staged["scan"].get("owned_by_user", [])),
            "predictor_uid": trace.state.uid, "box_limits": staged["scan"].get("box_limits"),
            "container_evidence": staged["scan"].get("container_evidence")}

    @vf.reward(weight=1)
    async def skill(self, trace, runtime) -> float:
        """Skill on the K-to-O scale: (L(K) - L) / (L(K) - L(O)); K = 0, the oracle = 1. Never raises: an item
        without a valid forecast is scored with the null policy's forecast (ruling E3) and the reason is recorded
        (memo hole 3)."""
        info = trace.info.setdefault("physim2", {})
        name = trace.state.rollout or trace.id
        t0, c0 = time.time(), time.process_time()
        fb = None
        try:
            hidden = self._hidden()
            fb = GRADING.fallback(hidden, self.data.world, self.data.config_name, self._limits()["n_samples"], self.config.grading_seed)
            if "verifier_box" not in info:                   # stage_verifier never ran: this is not the isolated grader
                info["grading_error"] = "NotIsolatedVerifier"
                g = GRADING.score_as_null(hidden, name, "grading error", fb,
                                          detail="the reward ran outside the isolated grader (use --env.id isolated-verifier)")
            elif not info["verifier_box"].get("has_predict"):
                col = trace.state.collection or {}
                g = GRADING.score_as_null(hidden, name, "no predict.py" if col.get("files") else "no submission", fb,
                                          detail=col.get("error") or "no predictor")
            else:
                budget = self.data.timeout.scoring
                uid, prepare = trace.state.uid, None
                if self.config.item_isolation == "box" and self.config.item_cleanup:
                    artifacts = dict(trace.state.artifacts)

                    async def prepare(rt):                   # what verifiers and stage_verifier did for the verifier box
                        await self._public_files(rt, uid)
                        await vf.restore(rt, artifacts)
                        if not (await GRADING.stage(rt, WORKDIR, uid))["has_predict"]:
                            raise RuntimeError("the predictor did not reach the item box")
                else:
                    info["between_item_state"] = "possible: all items ran in one box (item_isolation = shared)"
                g = await GRADING.grade(runtime, hidden, name, self._limits(), WORKDIR, uid=uid, fb=fb,
                                        examples=BUNDLE.public_examples(self.data.world, self.data.config_name),
                                        seed=self.config.grading_seed, cleanup=self.config.item_cleanup,
                                        deadline=None if budget is None else t0 + 0.9 * budget,
                                        prepare=prepare, parallel=self.config.item_boxes_parallel)
        except Exception as e:
            info["grading_error"] = type(e).__name__
            try:
                if fb is None:
                    fb = GRADING.fallback(self._hidden(), self.data.world, self.data.config_name, self._limits()["n_samples"],
                                          self.config.grading_seed)
                g = GRADING.score_as_null(self._hidden(), name, "grading error", fb, detail=f"grading error ({type(e).__name__})")
            except Exception:
                # no grade could be made at all (the store or the null policy is unreadable): 0.0 is a placeholder
                # for verifiers, NOT a score; `not_a_grade` says so and tools/run_report.py shows it
                g = {"skill_vs_O": 0.0, "n_failed": None, "reason": "grading error", "not_a_grade": True}
        g["worker_wall_s"], g["worker_cpu_s"] = time.time() - t0, time.process_time() - c0
        g["verifier_box_cpu_s"] = await GRADING.box_cpu_seconds(runtime)
        if info.get("verifier_started_unix"):
            g["verifier_wall_s"] = time.time() - info["verifier_started_unix"]
        if not self.config.item_cleanup:
            info["NOT_AN_EXAM"] = "cleanup between items was disabled by the operator (test hook)"
        skill = g.get("skill_vs_O")
        if not isinstance(skill, (int, float)) or not math.isfinite(skill):   # never a reward that is not a number
            g["skill_not_finite"], g["skill_vs_O"], skill = repr(skill), 0.0, 0.0
        info["grade"] = g
        return float(skill)


class Physim2Taskset(vf.Taskset[Physim2Task, Physim2Config]):
    DEFAULT_HARNESS = "bash"

    def load(self):
        root = STORE.store_root(self.config.store)
        rows = STORE.read_index(root, self.config.index)
        if self.config.instances is not None:
            by = {r["instance_id"]: r for r in rows}
            rows = [by[i] for i in self.config.instances]
        for row in rows:
            config = self.config.task.model_copy(deep=True)
            config.tools.store = root
            cfg = BUNDLE.load_config(row["config_name"])
            lim = cfg["predictor"]
            # what a statement says before a run exists: the profile's defaults and the declared limits (setup
            # renders the run's own). The box caps become the task's resource request.
            run = BUNDLE.default_run(row["world"], row["config_name"], config.limits.model_dump())
            text = BUNDLE.statement(row["world"], row["config_name"], run)
            yield Physim2Task(
                Physim2Data(
                    id=row["instance_id"], name=f"physim2-{row['world']}-{row['config_name']}",
                    instance_id=row["instance_id"], world=row["world"], config_name=row["config_name"],
                    secret_commitment=row["secret_commitment"],
                    prompt=PROMPT + text,
                    image=self.config.image, workdir=WORKDIR,
                    network_allow=[],                        # framework routes only, in both boxes
                    artifacts=[vf.Artifact(source="submission", required=False)],
                    artifact_max_bytes=int(lim["artifact_mib"] + 8) * MIB,   # transport; the 64 MiB cap is on file bytes
                    resources=vf.TaskResources(cpu=run["cpus"], memory=run["memory_gib"]),
                    timeout=vf.TaskTimeout(setup=900, agent=run["wall_minutes"] * 60.0, finalize=900,
                                           scoring=max(1800.0, (cfg["exam"]["n_items"] + 3) * (lim["wall_seconds"] + 40.0) + 600.0)),
                ),
                config,
            )
