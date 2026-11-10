"""physim2-script -- a scripted, model-free harness: run ONE script inside the agent's box.

    --env.agent.harness.id physim2-script
    --env.agent.harness.agent-dir /abs/path/to/agents      host directory, copied to /opt/agent in the box
    --env.agent.harness.script reference_agent.py          a file of that directory
    --env.agent.harness.args '["--policy", "S", "--sizes", "{...}"]'

The script runs where a model's shell commands would run: in the box, in the task's working directory, after
the network cut, with the tool servers up. It is given NOTHING a model's own script would not find: no
laboratory address in its environment (physim2.Lab() reads /etc/physim2/lab.json, which the task controller
wrote), no credential. The harness only checks that the address written into the box is the tool URL verifiers
handed to it, and keeps the script's output in the box (/logs/agent/script.log). No model call is made.
"""
from __future__ import annotations

import io
import json
import os
import shlex
import tarfile

import verifiers.v1 as vf

AGENT_HOME = "/opt/agent"
LOG = "/logs/agent/script.log"
ADDRESS_FILE = "/etc/physim2/lab.json"


class ScriptHarnessConfig(vf.HarnessConfig):
    agent_dir: str = ""
    """Host directory with the script and its helper modules (regular files, top level only)."""
    script: str = ""
    args: list[str] = []
    python: str = "python3"
    label: str = ""
    """Free text recorded with the harness config on the trace (e.g. the policy name)."""
    collect: list[str] = []
    """Files the script leaves in the working directory that the operator wants back (reports, logs)."""
    collect_dir: str = ""
    """Host directory for them: <collect_dir>/<trace id>/<file>. They are the script's own notes, at most 4 MiB each."""
    collect_tree: str = ""
    """A directory of the working directory to copy out as well (regular top-level files only, at most 16 MiB
    each): <collect_dir>/<trace id>/<name>_copy/. For the operator's own cross-checks of reference agents."""


def fill(text: str, data) -> str:
    """Per-task substitution in agent_dir and args: {idx} and {instance_id} of the task row."""
    return text.replace("{idx}", str(data.idx)).replace("{instance_id}", str(getattr(data, "instance_id", data.id)))


class ScriptHarness(vf.Harness[ScriptHarnessConfig]):
    SUPPORTS_MCP = True
    NEEDS_CONTAINER = True
    EXECUTES_CODE = True

    async def setup(self, runtime: vf.Runtime) -> None:
        c = self.config
        if not c.agent_dir or not c.script:
            raise ValueError("physim2-script needs --env.agent.harness.agent-dir and --env.agent.harness.script")
        r = await runtime.run(["mkdir", "-p", AGENT_HOME, "/logs/agent"], {})
        if r.exit_code:
            raise RuntimeError("could not prepare the box for the script")

    async def install(self, runtime: vf.Runtime, agent_dir: str) -> None:
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for nm in sorted(os.listdir(agent_dir)):
                p = os.path.join(agent_dir, nm)
                if os.path.isfile(p) and not os.path.islink(p) and not nm.endswith(".pyc"):
                    ti = tar.gettarinfo(p, arcname=nm)
                    ti.uid = ti.gid = 0
                    ti.mode = 0o644
                    with open(p, "rb") as f:
                        tar.addfile(ti, f)
        await runtime.write("/tmp/agent.tar", buf.getvalue())
        r = await runtime.run(["sh", "-c", f"tar -xf /tmp/agent.tar -C {AGENT_HOME} && rm -f /tmp/agent.tar"], {})
        if r.exit_code:
            raise RuntimeError("could not install the script in the box")

    async def launch(self, ctx, trace, runtime, endpoint, secret, mcp_urls, data) -> vf.ProgramResult:
        c = self.config
        await self.install(runtime, fill(c.agent_dir, data))
        args = [fill(a, data) for a in c.args]
        # the address the task controller wrote into the box must be the tool URL verifiers serves to harnesses
        seen = await runtime.run(["cat", ADDRESS_FILE], {})
        written = json.loads(seen.stdout)["url"] if seen.exit_code == 0 and seen.stdout.strip() else None
        info = trace.info.setdefault("physim2_script", {})
        info.update(tool_servers=sorted(mcp_urls), address_file_matches_tool_url=bool(written) and written in mcp_urls.values(),
                    script=c.script, label=c.label)
        env = {"PHYSIM2_AGENT_HOME": AGENT_HOME, "PYTHONDONTWRITEBYTECODE": "1", **c.resolved_env}
        cmd = shlex.join([c.python, "-B", f"{AGENT_HOME}/{c.script}", *args])
        result = await runtime.run_program(["sh", "-c", f"{cmd} > {LOG} 2>&1; rc=$?; tail -c 3000 {LOG}; exit $rc"], env)
        info.update(exit_code=result.exit_code, log_tail=result.stdout[-1500:])
        if c.collect and c.collect_dir:
            out = os.path.join(c.collect_dir, trace.id)
            os.makedirs(out, exist_ok=True)
            got = []
            for nm in [*c.collect, LOG]:
                try:
                    blob = await runtime.read(nm, max_bytes=4 << 20)
                except Exception:
                    continue
                with open(os.path.join(out, os.path.basename(nm)), "wb") as f:
                    f.write(blob)
                got.append(os.path.basename(nm))
            if c.collect_tree:
                ls = await runtime.run(["sh", "-c", f"cd {shlex.quote(c.collect_tree)} && find . -maxdepth 1 -type f | cut -c3-"], {})
                tree = os.path.join(out, os.path.basename(c.collect_tree.rstrip("/")) + "_copy")
                os.makedirs(tree, exist_ok=True)
                for nm in [n for n in ls.stdout.splitlines() if n and "/" not in n][:64]:
                    try:
                        blob = await runtime.read(f"{c.collect_tree}/{nm}", max_bytes=16 << 20)
                    except Exception:
                        continue
                    with open(os.path.join(tree, nm), "wb") as f:
                        f.write(blob)
                got.append(os.path.basename(tree) + "/")
            info["collected"] = got
        return result


__all__ = ["ScriptHarness"]
