"""R6 task hooks and MCP tools; execution is stock Verifiers v1.

The agent uses a provided harness in DockerRuntime, driven by SingleAgentEnv/eval.
The trusted MCP tool process keeps the simulator and grader outside that box.
Only observations and submitted workspace files cross the task boundary.
"""
from __future__ import annotations

import asyncio
from functools import wraps
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from types import SimpleNamespace
from typing import Literal

import numpy as np
from pydantic import Field
import verifiers.v1 as vf

from physim.blobround6_explore import ExperimentService
from physim.blobround6_eval import EvaluationError
from physim_r6 import evaluation as E

PROTOCOL = "r6-verifiers-v1-bash-1"
AGENT_IMAGE = "physim-r6-verifiers:20260909"
DEFAULT_OUTPUT = E.HERE / "verifiers_v1" / "artifacts"
DEFAULT_PROMPT = "Investigate the laboratory and submit your executable predictor."


class R6State(vf.State):
    # This state channel is host-only; these fields are never tool arguments.
    container_id: str = ""
    output: str = ""
    submitted: bool = False
    artifact: str | None = None
    checks: list[dict] = Field(default_factory=list)
    experiments: list[dict] = Field(default_factory=list)
    usage: dict = Field(default_factory=dict)
    origin: dict = Field(default_factory=dict)
    infrastructure_error: str | None = None
    exploration_closed: bool = False
    checkpoint: dict = Field(default_factory=dict)


class R6ToolsConfig(vf.ToolsetConfig):
    max_experiments: int = Field(20, ge=1, le=100)
    max_total_tu: float = Field(750, gt=0, le=5000)
    max_validation_attempts: int = Field(8, ge=1, le=32)
    max_submission_attempts: int = Field(8, ge=1, le=32)


class R6TaskConfig(vf.TaskConfig):
    tools: R6ToolsConfig = R6ToolsConfig()
    output_root: Path = DEFAULT_OUTPUT
    agent_image: str = AGENT_IMAGE
    coding_interface: Literal["shell", "ipython"] = "shell"
    setup_timeout: float = Field(180, gt=0, le=900)
    checkpoint_artifact: Path | None = None


class R6Config(vf.TasksetConfig):
    task: R6TaskConfig = R6TaskConfig()
    prompt: str = DEFAULT_PROMPT


def public_prompt(config: R6ToolsConfig, coding_interface: str = "shell") -> str:
    spec = (E.WORKED / "AGENT_SPEC.md").read_text()
    # The authoritative short-run budget is written explicitly below.
    spec = spec.replace("100 experiments", f"{config.max_experiments} experiments")
    spec = spec.replace("5000 integrated time units", f"{config.max_total_tu:g} integrated time units")
    text = f"""Investigate the anonymous laboratory and deliver /workspace/predictor.py.

You have the harness's bash and edit tools for working with files and running Python.
NumPy, SciPy, scikit-learn and Matplotlib are installed. The working directory is
/workspace. Files persist throughout the coding session. Laboratory tools:

- laboratory_experiment(actions, queries): run an independent experiment from the
  prepared start; save full NPZ observations in /observations and return their path.
- laboratory_usage(): inspect the laboratory budget.
- laboratory_validate(): test a snapshot of your predictor against public interface
  examples; return errors to repair. Does not submit or test physical accuracy.
- laboratory_submit(): check and freeze the current predictor and supporting files.
  A failed check leaves the workspace open for repair; a successful submission ends
  exploration. Finish the coding session once submission is accepted.

The experiment budget is {config.max_experiments} experiments and
{config.max_total_tu:g} integrated time units. Each experiment costs its largest
requested timestamp, at most 50 tu. You may validate {config.max_validation_attempts}
times and attempt submission {config.max_submission_attempts} times; neither costs
experiments or simulation time. Save a simple working predictor early, validate it,
then improve it and submit before your coding session ends. If the session ends
with predictor.py written, its final snapshot is collected and checked as well.

Implement predict(actions, queries, n_samples=64, seed=0) at module scope. Return
{{"samples": [array_for_query0, array_for_query1, ...]}}. Each array has shape
(n_samples, len(query["t"]), 12, sensor_slots), where slots are device0=13,
device1=19, global=2. Handle empty query/time lists, different query orders,
different time grids, and the requested member count. The same seed must reproduce
the same result. During prediction /workspace and /observations are read-only;
/tmp is writable. No further laboratory calls are available during prediction.

Read observation metadata and arrays together:
```python
import json
import numpy as np
with np.load(observation_path, allow_pickle=False) as data:
    request = json.loads(data["request"].item())
    observations = [(query, data[f"query{{i}}"].copy())
                    for i, query in enumerate(request["queries"])]
```
Observation arrays have shape (1, times, 12, slots). query0 is the first query
in that file, not a fixed sensor. Align sensor identities and timestamps before
comparing observations from different experiments. There is no separate metadata
JSON file. Do not print whole arrays into the conversation; analyze saved files.

The laboratory tools are your only access to the system. Grading happens after
artifact freeze, on independent realizations and undisclosed action/query programs.
The model receives no hidden equations, fields, sensor locations, or test answers.

{spec}"""
    if coding_interface == "ipython":
        text = text.replace("You have the harness's bash and edit tools for working with files and running Python.",
            "Use the harness's persistent IPython session to analyze data and write files.\n"
            "Use the MCP skill wrappers advertised by the harness for laboratory calls;\n"
            "follow their actual import and calling instructions.")
    return text


def _container(state: R6State) -> str:
    if not re.fullmatch(r"[0-9a-f]{12,64}", state.container_id):
        raise vf.ToolsetError("missing trusted Docker runtime identity")
    return state.container_id


def _snapshot(state: R6State, target: Path) -> dict:
    # Reuse the existing bounded, regular-file-only artifact transport. This
    # does not create a runtime or run an agent; Verifiers owns that runtime.
    return E.Sandbox.export_workspace(SimpleNamespace(name=_container(state)), target,
                                     excludes=("./.vf-*",))


def _put_observation(state: R6State, path: Path) -> None:
    # No host path or code from the model is accepted. The trusted filename is
    # fixed by the experiment counter. O_NOFOLLOW prevents a workspace symlink
    # from redirecting this write within the agent container.
    script = """import os,sys
p='/observations/'+sys.argv[1]
fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
with os.fdopen(fd,'wb') as f: f.write(sys.stdin.buffer.read())
"""
    E.docker(["exec", "-i", "--user", "0", _container(state), "python", "-c", script, path.name],
             data=path.read_bytes())


def _checkpoint_file(root: Path, name: str, digest: str) -> tuple[str, bytes]:
    """Read only a hashed regular file in a trusted prior artifact manifest."""
    rel = PurePosixPath(name)
    if rel.is_absolute() or not rel.parts or any(p in (".", "..") or p.startswith(".vf-") for p in rel.parts):
        raise vf.TaskError("invalid checkpoint file path")
    path = root.joinpath(*rel.parts)
    if any(root.joinpath(*rel.parts[:i]).is_symlink() for i in range(1, len(rel.parts)+1)) or not path.is_file():
        raise vf.TaskError("checkpoint file is not a regular file")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise vf.TaskError("checkpoint file hash mismatch")
    return str(rel), data


def load_checkpoint(artifact: Path) -> tuple[dict, list, list]:
    """Recover public workspace/data only; never copy host state or private origin."""
    artifact = artifact.resolve()
    state_path = artifact.parent / "laboratory_state.json"
    prior = json.loads(state_path.read_text())
    check = next((c for c in prior["checks"] if c["path"] == artifact.name), None)
    if not check or not check.get("validation", {}).get("ok"):
        raise vf.TaskError("checkpoint must be a previously validated artifact")
    manifest = check["snapshot"]["files"]
    files = [_checkpoint_file(artifact, f["path"], f["sha256"]) for f in manifest]
    if "predictor.py" not in {name for name, _ in files}:
        raise vf.TaskError("checkpoint has no predictor.py")
    experiments = prior["experiments"]
    observations = []
    for index, event in enumerate(experiments, 1):
        if event["file"] != f"experiment_{index:03d}.npz":
            raise vf.TaskError("invalid checkpoint observation sequence")
        observations.append(_checkpoint_file(artifact.parent / "observations", event["file"], event["sha256"]))
    if len(experiments) != prior["usage"]["experiments"]:
        raise vf.TaskError("checkpoint experiment accounting mismatch")
    metadata = dict(source_artifact=str(artifact), source_state_sha256=E.file_digest(state_path),
        files=manifest, observations=[dict(file=e["file"], sha256=e["sha256"]) for e in experiments],
        inherited_experiments=len(experiments), inherited_charged_tu=prior["usage"]["charged_tu"],
        exploration_closed=True)
    return metadata, files, observations


def recovery_prompt() -> str:
    return ("\n\nThis is a submission recovery after a framework interruption. Your last "
            "validated predictor and its supporting files are restored in /workspace, "
            "with your collected data in /observations. Exploration is closed: no new "
            "experiments are allowed. Inspect the restored predictor if needed, then "
            "call laboratory_submit to validate and freeze it. No accuracy feedback "
            "has been provided. This recovery inherits the earlier experiment/time usage.")


def _check(state: R6State, config: R6ToolsConfig, *, final: bool) -> dict:
    if state.submitted:
        return dict(ok=True, accepted=True, finalized=True)
    kind = "submit" if final else "validate"
    attempt = 1 + sum(row["kind"] == kind for row in state.checks)
    cap = config.max_submission_attempts if final else config.max_validation_attempts
    if attempt > cap:
        return dict(ok=False, error=f"{kind} attempt limit reached", finalized=False)
    target = Path(state.output) / f"{kind}_{attempt:02d}"
    event = dict(kind=kind, attempt=attempt, path=target.name)
    state.checks.append(event)
    try:
        event["snapshot"] = _snapshot(state, target)
    except E.SandboxError as exc:
        report = dict(ok=False, gate=E.SUBMISSION_GATE_VERSION,
                      failure=dict(stage="artifact", error=str(exc)[-3000:]))
    else:
        # A validator-container startup failure is infrastructure failure, not
        # evidence that the submitted predictor violates the contract.
        report = E.validate_predictor(target, Path(state.output) / "observations")
    event["validation"] = report
    if final and report["ok"]:
        state.submitted = True
        state.artifact = str(target)
    E.dump(Path(state.output) / "laboratory_state.json", state.model_dump(exclude={"artifacts"}))
    return dict(report, finalized=state.submitted, accepted=final and report["ok"])


class LaboratoryTools(vf.Toolset[R6ToolsConfig, R6State]):
    TOOL_PREFIX = "laboratory"

    def __init__(self, config):
        super().__init__(config)
        self.service = None
        self.lock = asyncio.Lock()
        self.state_transaction = asyncio.Lock()

    def _with_state(self, fn):
        wrapped = super()._with_state(fn)

        @wraps(wrapped)
        async def serialized(*args, **kwargs):
            # VF's state channel replaces the full state. Serialize the entire
            # pull/call/push transaction, including under parallel-tool harnesses.
            async with self.state_transaction:
                return await wrapped(*args, **kwargs)
        return serialized

    def _service(self):
        if self.service is None:
            oracle, origin = E.make_origin()
            self.state.origin = origin
            self.service = ExperimentService(oracle, limits=E.LIMITS,
                max_experiments=self.config.max_experiments,
                max_total_tu=self.config.max_total_tu)
        return self.service

    @vf.tool
    async def experiment(self, actions: list[dict], queries: list[dict]) -> str:
        """Run from the prepared start and save NPZ arrays. actions: inject
        {t,kind:'inject',port:0..11,amp:0..3,dur} or adjust
        {t,kind:'adjust',device:0..1,u:[-1..1,-1..1,-1..1]}. queries:
        [{sensor:'device0'|'device1'|'global',t:[strictly increasing times]}].
        All timestamps are absolute, 0..50 tu. Return path, shapes and usage.
        """
        async with self.lock:
            if self.state.submitted:
                return json.dumps(dict(error="predictor already submitted"))
            if self.state.exploration_closed:
                return json.dumps(dict(error="exploration closed for checkpoint recovery", usage=self.state.usage))
            service = self._service()
            try:
                data = await asyncio.to_thread(service.experiment, actions, queries)
            except (ValueError, EvaluationError) as exc:
                self.state.usage = service.usage()
                return json.dumps(dict(error=str(exc), usage=self.state.usage))
            self.state.usage = service.usage()
            path = Path(self.state.output) / "observations" / f"experiment_{self.state.usage['experiments']:03d}.npz"
            request = dict(actions=actions, queries=queries)
            np.savez_compressed(path, request=json.dumps(request),
                **{f"query{i}": a for i, a in enumerate(data["samples"])})
            await asyncio.to_thread(_put_observation, self.state, path)
            arrays = {f"query{i}": list(a.shape) for i, a in enumerate(data["samples"])}
            self.state.experiments.append(dict(request=request, file=path.name,
                                               sha256=E.file_digest(path), arrays=arrays))
            E.dump(Path(self.state.output) / "laboratory_state.json", self.state.model_dump(exclude={"artifacts"}))
            return json.dumps(dict(path="/observations/"+path.name, arrays=arrays, usage=self.state.usage))

    @vf.tool
    async def usage(self) -> str:
        """Return experiment/time budgets and validation/submission attempt counts."""
        return json.dumps(dict(**self.state.usage,
            validation_attempts=sum(c["kind"] == "validate" for c in self.state.checks),
            submission_attempts=sum(c["kind"] == "submit" for c in self.state.checks)))

    @vf.tool
    async def validate(self) -> str:
        """Check a predictor snapshot against public interface cases. No accuracy
        feedback and no experiment cost. Does not submit; repair errors and retry."""
        async with self.lock:
            return json.dumps(await asyncio.to_thread(_check, self.state, self.config, final=False))

    @vf.tool
    async def submit(self) -> str:
        """Validate and freeze predictor.py plus supporting files; success ends
        exploration. Errors leave the workspace open for repairs."""
        async with self.lock:
            return json.dumps(await asyncio.to_thread(_check, self.state, self.config, final=True))


class R6Data(vf.TaskData):
    protocol: str = PROTOCOL


class R6Task(vf.Task[R6Data, R6State, R6TaskConfig]):
    @classmethod
    def toolsets(cls, config):
        if config.tools.colocated or config.tools.runtime.type != "subprocess" or config.tools.url:
            raise ValueError("R6 laboratory tools must run in their trusted host process")
        return [LaboratoryTools(config.tools)]

    async def setup(self, trace, runtime):
        if runtime.config.type != "docker" or not runtime.config.network_restricted:
            raise vf.TaskError("R6 requires the Verifiers Docker runtime with framework-only network access")
        state = trace.state
        state.container_id = runtime.info.id
        output = self.config.output_root.resolve() / trace.id
        output.mkdir(parents=True, exist_ok=False)
        (output / "observations").mkdir()
        state.output = str(output)
        state.usage = dict(experiments=0, max_experiments=self.config.tools.max_experiments,
                           charged_tu=0, max_total_tu=self.config.tools.max_total_tu)
        result = await runtime.run(["mkdir", "-p", "/workspace", "/observations"], {})
        if result.exit_code:
            raise vf.TaskError("could not initialize laboratory workspace")
        await runtime.write("/workspace/AGENT_SPEC.md", public_prompt(self.config.tools, self.config.coding_interface).encode())
        if self.config.checkpoint_artifact is not None:
            metadata, files, observations = await asyncio.to_thread(load_checkpoint, self.config.checkpoint_artifact)
            state.checkpoint = metadata
            state.exploration_closed = True
            state.usage.update(experiments=metadata["inherited_experiments"],
                               charged_tu=metadata["inherited_charged_tu"], exploration_closed=True)
            for name, data in files:
                result = await runtime.run(["mkdir", "-p", str(PurePosixPath("/workspace", name).parent)], {})
                if result.exit_code:
                    raise vf.TaskError("could not restore checkpoint directory")
                await runtime.write("/workspace/" + name, data)
            for name, data in observations:
                path = output / "observations" / name
                path.write_bytes(data)
                await asyncio.to_thread(_put_observation, state, path)
            E.dump(output / "laboratory_state.json", state.model_dump(exclude={"artifacts"}))
        trace.info["r6"] = dict(protocol=self.data.protocol, artifact_directory=str(output),
            verifiers_version=__import__("verifiers").__version__,
            gate=E.SUBMISSION_GATE_VERSION, checkpoint=state.checkpoint)

    @vf.stop
    async def submitted(self, trace) -> bool:
        # This installed ACP adapter reports an externally stopped RLM prompt
        # as a harness error. Let RLM return its final answer naturally; submit
        # has already frozen the artifact and disabled further experiments.
        return trace.state.submitted and self.config.coding_interface == "shell"

    async def finalize(self, trace, runtime):
        state = trace.state
        if not state.output:
            return
        # Stock VF ends naturally on final text or a configured limit. The task
        # collects the last executable artifact, without another model call.
        if not state.submitted:
            report = await asyncio.to_thread(_check, state, self.config.tools, final=True)
            trace.info["r6"]["final_collection"] = report
        E.dump(Path(state.output) / "laboratory_state.json", state.model_dump(exclude={"artifacts"}))

    @vf.reward(weight=1)
    async def prediction_reward(self, trace) -> float:
        state = trace.state
        info = trace.info.setdefault("r6", {})
        if not state.submitted:
            attempted = any(c.get("snapshot") for c in state.checks)
            info["score_kind"] = "infinity" if attempted else "nan"
            info["score_reason"] = "invalid_predictor" if attempted else "no_predictor"
            if not attempted:
                raise vf.TaskError("No executable predictor was delivered; retry with an appropriate Verifiers limit or harness")
            return 0.0
        grade = await asyncio.to_thread(E.grade, Path(state.artifact), Path(state.output)/"observations", Path(state.output), members=64)
        info["grade"] = grade
        score = grade["primary_joint_energy"]
        info["score_kind"] = "finite" if score is not None else "infinity"
        info["primary_joint_energy"] = score
        # Preserve the lower-is-better scientific score. VF rewards are larger
        # is better; this monotone transform is explicit and recorded.
        info["reward_mapping"] = "1 / (1 + primary_joint_energy); invalid contract -> 0"
        return 1 / (1 + score) if score is not None else 0.0


class R6Taskset(vf.Taskset[R6Task, R6Config]):
    DEFAULT_HARNESS = "bash"

    def load(self):
        protocol = PROTOCOL if self.config.task.coding_interface == "shell" else "r6-verifiers-v1-ipython-1"
        if self.config.prompt != DEFAULT_PROMPT:
            protocol += "-prompt-" + hashlib.sha256(self.config.prompt.encode()).hexdigest()[:12]
        system_prompt = public_prompt(self.config.task.tools, self.config.task.coding_interface)
        if self.config.task.checkpoint_artifact is not None:
            protocol += "-checkpoint-" + hashlib.sha256(str(self.config.task.checkpoint_artifact.resolve()).encode()).hexdigest()[:12]
            system_prompt += recovery_prompt()
        yield R6Task(R6Data(idx=0, name="r6-prepared-laboratory",
            protocol=protocol,
            prompt=self.config.prompt,
            system_prompt=system_prompt,
            image=self.config.task.agent_image,
            workdir="/workspace", network_allow=[],
            resources=vf.TaskResources(cpu=1, memory=1),
            timeout=vf.TaskTimeout(setup=self.config.task.setup_timeout, agent=1800, finalize=180, scoring=900)), self.config.task)


if __name__ == "__main__":
    LaboratoryTools.run()
