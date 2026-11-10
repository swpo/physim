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


class ScriptHarness(vf.Harness[ScriptHarnessConfig]):
    SUPPORTS_MCP = True
    NEEDS_CONTAINER = True
    EXECUTES_CODE = True

    async def setup(self, runtime: vf.Runtime) -> None:
        c = self.config
        if not c.agent_dir or not c.script:
            raise ValueError("physim2-script needs --env.agent.harness.agent-dir and --env.agent.harness.script")
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for nm in sorted(os.listdir(c.agent_dir)):
                p = os.path.join(c.agent_dir, nm)
                if os.path.isfile(p) and not os.path.islink(p) and not nm.endswith(".pyc"):
                    ti = tar.gettarinfo(p, arcname=nm)
                    ti.uid = ti.gid = 0
                    ti.mode = 0o644
                    with open(p, "rb") as f:
                        tar.addfile(ti, f)
        await runtime.write("/tmp/agent.tar", buf.getvalue())
        r = await runtime.run(["sh", "-c", f"mkdir -p {AGENT_HOME} /logs/agent && tar -xf /tmp/agent.tar -C {AGENT_HOME} && rm -f /tmp/agent.tar"], {})
        if r.exit_code:
            raise RuntimeError("could not install the script in the box")

    async def launch(self, ctx, trace, runtime, endpoint, secret, mcp_urls, data) -> vf.ProgramResult:
        c = self.config
        # the address the task controller wrote into the box must be the tool URL verifiers serves to harnesses
        seen = await runtime.run(["cat", ADDRESS_FILE], {})
        written = json.loads(seen.stdout)["url"] if seen.exit_code == 0 and seen.stdout.strip() else None
        route = {"tool_servers": sorted(mcp_urls), "address_file_matches_tool_url": bool(written) and written in mcp_urls.values()}
        trace.info.setdefault("physim2_script", {}).update(route, script=c.script, args=c.args, label=c.label)
        env = {"PHYSIM2_AGENT_HOME": AGENT_HOME, "PYTHONDONTWRITEBYTECODE": "1", **c.resolved_env}
        cmd = shlex.join([c.python, "-B", f"{AGENT_HOME}/{c.script}", *c.args])
        result = await runtime.run_program(["sh", "-c", f"{cmd} > {LOG} 2>&1; rc=$?; tail -c 3000 {LOG}; exit $rc"], env)
        trace.info["physim2_script"].update(exit_code=result.exit_code, log_tail=result.stdout[-1500:])
        return result


__all__ = ["ScriptHarness"]
