"""The PhySim v2 exam as a verifiers taskset: task hooks only; execution is stock verifiers v1.

Run it under the stock isolated grader (`--env.id isolated-verifier`) on a container runtime with the declared
network policy. What happens, and where:

  worker (vf-eval process, trusted)   this module: setup, finalize, the reward; the instance store
  laboratory (host process, trusted)  lab_tools.LabTools, one per rollout, started by verifiers
  agent box (container)               TASK.md, the public physim2 package, an empty submission/; its only ways
                                      out are the model route and the laboratory's URL
  verifier box (fresh container)      the public package again, the frozen submission/, the public driver;
                                      no network; the predictor as an unprivileged user, one item at a time

A task row carries pointers only (instance id, world, config name, the public commitment of the secret): rows
are saved in every trace. Hidden values are read on the worker from the store, by the laboratory and the reward.
"""
from __future__ import annotations

import json
import os
import time

import verifiers.v1 as vf
from pydantic import Field

from . import access as ACCESS
from . import bundle as BUNDLE
from . import grading as GRADING
from . import store as STORE
from .lab_tools import LabTools, LabToolsConfig

WORKDIR = "/workspace"
PROMPT = ("Your task is described in /workspace/TASK.md (the same text follows). Work in /workspace. Finish by "
          "calling lab.submit(\"submission\").\n\n")
MIB = 1 << 20


class Physim2State(vf.State):
    # Host-only: `state` is excluded from saved traces (verifiers/v1/trace.py:412-417).
    access: dict = Field(default_factory=dict)               # socket of the task controller (announce, freeze)
    rollout: str = ""                                        # names this rollout's records in the store
    finalized: bool = False                                  # set by finalize: setup then runs in verifier mode
    collection: dict = Field(default_factory=dict)           # how submission/ was obtained (no file content)


class Physim2TaskConfig(vf.TaskConfig):
    tools: LabToolsConfig = LabToolsConfig()
    single_use: bool = False
    """Sealed exams: refuse an instance whose laboratory was already opened by another rollout (a rerun would
    hand the agent a fresh budget). Pilots and proofs leave it off."""
    item_cleanup: bool = True
    """TEST HOOK. False skips the cleanup between items so that a probe can show what the cleanup prevents;
    such a rollout is marked NOT_AN_EXAM in its trace."""
    grading_seed: int = 0


class Physim2Config(vf.TasksetConfig):
    task: Physim2TaskConfig = Physim2TaskConfig()
    store: str = ""
    """Instance store on the worker (default $PHYSIM2_STORE)."""
    index: str = ""
    """Public index of instances (default <store>/index.json)."""
    instances: list[str] | None = None
    """Instance ids to load (default: every row of the index)."""
    image: str = "physim2-ring:1"
    """The one image of both boxes (docker/Dockerfile.ring)."""


class Physim2Data(vf.TaskData):
    # Pointers and public declarations only. Never a hidden value: the row is saved in every trace.
    instance_id: str
    world: str
    config_name: str
    secret_commitment: str = Field(pattern=r"^[0-9a-f]{64}$")


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
        # ---- guard 3: no token-like variable may enter a box ----
        harness = getattr(getattr(trace.agent, "config", None), "harness", None)
        names = list(runtime.env) + list(getattr(harness, "env", {}) or {}) + list(getattr(harness, "forward_env", []) or [])
        if STORE.token_like(names):
            raise vf.TaskError("a token-like variable is configured for a box (runtime env, harness env or forward_env)")
        hidden = self._hidden()
        inst = json.load(open(os.path.join(hidden, "instance.json")))
        cfg = BUNDLE.load_config(self.data.config_name)
        if inst["secret_commitment"] != self.data.secret_commitment or inst["world"] != self.data.world \
                or inst["config"] != cfg:
            raise vf.TaskError("the stored instance differs from the task row (commitment, world or config)")
        del inst
        raw, info = BUNDLE.public_bundle(self.data.world, self.data.config_name)
        await runtime.write("/tmp/physim2-workspace.tar", raw)
        r = await runtime.run(["sh", "-c", f"umask 022; mkdir -p {WORKDIR} /etc/physim2 && chmod 755 {WORKDIR} /etc/physim2 && "
                                            f"tar -xf /tmp/physim2-workspace.tar -C {WORKDIR} && rm -f /tmp/physim2-workspace.tar"], {})
        if r.exit_code:
            raise vf.TaskError("could not build the workspace in the box")
        state = trace.state
        if state.finalized:                                  # the verifier box: public files only, no laboratory
            trace.info.setdefault("physim2", {})["verifier_started_unix"] = time.time()
            return
        labs = os.path.join(hidden, "labs")
        if self.config.single_use and os.path.isdir(labs) and os.listdir(labs):
            raise vf.TaskError("this instance was already opened by another rollout (single_use)")
        box = ACCESS.BoxAccess(runtime, list(self.data.artifacts), self.data.artifact_max_bytes, cfg["predictor"]["artifact_mib"])
        self._access[trace.id] = box
        state.access = await box.start()
        state.rollout = trace.id
        trace.info["physim2"] = {
            "instance_id": self.data.instance_id, "world": self.data.world, "config_name": self.data.config_name,
            "secret_commitment": self.data.secret_commitment, "bundle": {k: info[k] for k in ("files", "bytes", "manifest_sha256")},
            "verifiers_version": __import__("verifiers").__version__, "runtime": runtime.config.type,
            "network_restricted": bool(runtime.config.network_restricted)}

    async def finalize(self, trace, runtime):
        """Runs in the agent's box after the harness ended and the laboratory stopped. Collects the submission
        defensively and never raises: whatever the agent did to its box, the rollout stays gradable (hole 3)."""
        state = trace.state
        info = trace.info.setdefault("physim2", {})
        box = self._access.pop(trace.id, None)
        try:
            cfg = BUNDLE.load_config(self.data.config_name)
            frozen = box.frozen if box is not None and box.frozen is not None and box.frozen["ok"] else None
            source = "agent_submission" if frozen is not None else "final_collection"
            if frozen is None:
                frozen = await ACCESS.collect_frozen(runtime, list(self.data.artifacts), self.data.artifact_max_bytes,
                                                     cfg["predictor"]["artifact_mib"])
            # A non-empty mapping makes verifiers skip its own collection (rollout.py:501); None = nothing to restore.
            state.artifacts = {frozen["root"]: frozen["archive"]}
            man = frozen["manifest"]
            state.collection = {"source": source, "ok": frozen["ok"], "error": frozen["error"], "files": len(man["files"]),
                                "bytes": man.get("bytes", 0), "sha256": man.get("sha256")}
        except Exception as e:
            state.artifacts = {f"{WORKDIR}/submission": None}
            state.collection = {"source": "none", "ok": False, "error": f"collection failed ({type(e).__name__})", "files": 0}
        finally:
            state.access = {}
            state.finalized = True
            if box is not None:
                try:
                    await box.close()
                except Exception:
                    pass
        info["submission"] = dict(state.collection)
        info["lab"] = self._lab_usage(state.rollout)
        info["stop_condition"] = trace.stop_condition
        info["agent_box_cpu_s"] = await GRADING.box_cpu_seconds(runtime)

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

    async def stage_verifier(self, trace, runtime):
        """After verifiers restored the frozen submission into the fresh box: trusted staging only."""
        staged = await GRADING.stage(runtime, WORKDIR)
        trace.info.setdefault("physim2", {})["verifier_box"] = {
            "has_predict": staged["has_predict"], "network_restricted": bool(runtime.config.network_restricted),
            "writable_dirs": staged["scan"].get("writable_dirs"), "world_writable_paths_fixed": staged["scan"].get("fixed"),
            "owned_by_predictor_user_before": len(staged["scan"].get("owned_by_user", []))}

    @vf.reward(weight=1)
    async def skill(self, trace, runtime) -> float:
        """Skill on the K-to-O scale: (L(K) - L) / (L(K) - L(O)); K = 0, the oracle = 1. Never raises: any
        failure is scored as K and recorded (memo hole 3)."""
        info = trace.info.setdefault("physim2", {})
        name = trace.state.rollout or trace.id
        t0, c0 = time.time(), time.process_time()
        try:
            hidden = self._hidden()
            if not info.get("verifier_box", {}).get("has_predict"):
                g = GRADING.score_as_k(hidden, name, (trace.state.collection or {}).get("error") or "no predictor")
            else:
                budget = self.data.timeout.scoring
                g = await GRADING.grade(runtime, hidden, name, self._limits(), WORKDIR, seed=self.config.grading_seed,
                                        cleanup=self.config.item_cleanup,
                                        deadline=None if budget is None else t0 + 0.9 * budget)
        except Exception as e:
            info["grading_error"] = type(e).__name__
            try:
                g = GRADING.score_as_k(self._hidden(), name, f"grading error ({type(e).__name__})")
            except Exception:
                g = {"skill_vs_O": 0.0, "n_failed": None, "reason": "grading error and the store is unreadable"}
        g["worker_wall_s"], g["worker_cpu_s"] = time.time() - t0, time.process_time() - c0
        g["verifier_box_cpu_s"] = await GRADING.box_cpu_seconds(runtime)
        if info.get("verifier_started_unix"):
            g["verifier_wall_s"] = time.time() - info["verifier_started_unix"]
        if not self.config.item_cleanup:
            info["NOT_AN_EXAM"] = "cleanup between items was disabled by the operator (test hook)"
        info["grade"] = g
        return float(g["skill_vs_O"])


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
            lim, env = cfg["predictor"], cfg["envelope"]
            text = BUNDLE.task_text(row["world"], row["config_name"])
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
                    resources=vf.TaskResources(cpu=env["cpus"], memory=env["memory_gib"]),
                    timeout=vf.TaskTimeout(setup=900, agent=env["wall_hours"] * 3600.0, finalize=900,
                                           scoring=max(1800.0, cfg["exam"]["n_items"] * (lim["wall_seconds"] + 20.0) + 600.0)),
                ),
                config,
            )
