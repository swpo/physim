"""Scoped transport repair and evidence capture for the installed VF Bash harness.

The model loop, tools, sampling and retry count remain the installed Verifiers
implementations. The campaign omits the generic coding-role preamble so the
task's ordered scientific instructions lead the prompt; tool guidance is in
that task contract. The generated source and diff are archived per run;
no installed dependency is edited. Remove this overlay when upstream fixes the
MCP cleanup path. Fault injection is only exposed by the offline smoke entrypoint.
"""

from __future__ import annotations

import difflib
import hashlib
import importlib.metadata
import json
import re
from pathlib import Path

# Actual sandbox versions from the successful no-charge Docker replay. The
# stock script floats these dependencies on every new container; pin the tested
# transport stack so logging and live inference use the same implementation.
CLIENT_VERSIONS = {
    "openai": "3.7.0",
    "mcp": "1.29.1",
    "httpx": "0.28.1",
    "httpcore": "1.0.9",
    "anyio": "4.15.1",
    "tenacity": "9.1.4",
}


def redact(text):
    text = re.sub(r"(?i)(bearer\s+)[^\s'\"<>]+", r"\1[REDACTED]", text)
    text = re.sub(r"(?i)((?:--api-key|api_key|secret)[= :]+)[^\s'\"<>]+", r"\1[REDACTED]", text)
    return re.sub(r"(https?://[^\s?'\"<>]+)\?[^\s'\"<>]+", r"\1?[REDACTED]", text)


SESSION = '''@asynccontextmanager
async def mcp_session(spec: dict):
    """Keep task-group failures visible to native retries; preserve cancellation."""
    from mcp import ClientSession
    from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client

    answered = False
    try:
        # Pass body exceptions through __aexit__: aclose() would lose the
        # background transport error and leave only its induced cancellation.
        async with AsyncExitStack() as stack:
            http_client = await stack.enter_async_context(
                create_mcp_http_client(
                    headers=spec.get("headers") or None,
                    timeout=httpx.Timeout(spec.get("timeout", MCP_TIMEOUT), connect=5.0),
                )
            )
            http_client.event_hooks.setdefault("request", []).append(_campaign_mcp_request)
            http_client.event_hooks.setdefault("response", []).append(_campaign_mcp_response)
            read, write, *_ = await stack.enter_async_context(
                streamable_http_client(spec["url"], http_client=http_client)
            )
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            yield session
            answered = True
    except Exception:
        _campaign_transport_error(answered)
        if not answered:
            raise
        # Cleanup noise must never replay an already answered tool operation.
'''

LOGGING = """
# Campaign diagnostics: metadata only, never HTTP headers or tool arguments.
import importlib.metadata as _campaign_metadata
import sys as _campaign_sys
import time as _campaign_time
import traceback as _campaign_traceback

_campaign_schema_calls = 0

def _campaign_event(event, **fields):
    print(json.dumps(dict(event=event, utc_seconds=_campaign_time.time(), **fields)),
          file=_campaign_sys.stderr, flush=True)

def _campaign_transport_error(answered):
    _campaign_event("mcp_transport_exception", answered=answered)
    _campaign_traceback.print_exc(file=_campaign_sys.stderr)

async def _campaign_mcp_request(request):
    global _campaign_schema_calls
    method = None
    if request.method == "POST":
        try:
            method = json.loads(request.content).get("method")
        except (ValueError, httpx.RequestNotRead):
            pass
    request.extensions["campaign_started"] = _campaign_time.monotonic()
    request.extensions["campaign_rpc_method"] = method
    _campaign_event("mcp_request", http_method=request.method, rpc_method=method)
    if method == "tools/list":
        _campaign_schema_calls += 1
        if _campaign_schema_calls == CAMPAIGN_OFFLINE_FAULT_AT:
            _campaign_event("offline_injected_schema_failure")
            raise httpx.ConnectError("offline injected MCP schema connection failure", request=request)

async def _campaign_mcp_response(response):
    request = response.request
    _campaign_event("mcp_response", http_method=request.method,
                    rpc_method=request.extensions.get("campaign_rpc_method"),
                    status=response.status_code,
                    elapsed_seconds=_campaign_time.monotonic() - request.extensions["campaign_started"])

_campaign_event("harness_dependencies", versions={name: _campaign_metadata.version(name)
    for name in ("mcp", "httpx", "httpcore", "anyio", "openai", "tenacity")})

"""


def instrument_program(source, *, inject_schema_failure_at=None):
    start = source.index("@asynccontextmanager\nasync def mcp_session(")
    end = source.index("\n\nasync def with_retry(", start)
    old = source[start:end]
    if "with suppress(Exception):\n            await stack.aclose()" not in old:
        raise RuntimeError("Installed MCP cleanup changed; review/remove campaign overlay before running")
    prefetch = "async with mcp_session(servers[server_name]) as session:\n            return await session.call_tool(raw, arguments)"
    if source.count(prefetch) != 1:
        raise RuntimeError("Installed MCP dispatch changed; review the campaign overlay")
    patched = source[:start] + SESSION + source[end:]
    patched = patched.replace(
        prefetch,
        "async with mcp_session(servers[server_name]) as session:\n"
        "            await session.list_tools()  # cache schema before any side effect\n"
        "            return await session.call_tool(raw, arguments)",
    )
    dependencies = '# dependencies = ["openai", "mcp>=1.24.0,<2", "httpx", "tenacity"]'
    if patched.count(dependencies) != 1:
        raise RuntimeError("Installed Bash dependencies changed; review the pinned transport stack")
    patched = patched.replace(
        dependencies,
        "# dependencies = "
        + json.dumps(
            [f"{name}=={version}" for name, version in CLIENT_VERSIONS.items()],
        ),
    )
    # Insert after imports and before executable harness definitions. Actual
    # resolved versions are also logged in the sandbox.
    marker = 'SERPER_URL = "https://google.serper.dev/search"'
    if patched.count(marker) != 1:
        raise RuntimeError("Installed Bash program layout changed")
    return patched.replace(marker, f"CAMPAIGN_OFFLINE_FAULT_AT = {inject_schema_failure_at!r}\n" + LOGGING + marker)


def install(directory, *, inject_schema_failure_at=None):
    import verifiers.v1.harnesses.bash.harness as bash
    from verifiers.v1.harness import Harness

    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    framing = dict(bash=bash.BASH_SYSTEM_PROMPT, edit=bash.EDIT_SYSTEM_PROMPT)
    # Scoped to this campaign entrypoint; never edit installed Verifiers files.
    # The task contract already describes these tools under Limits and runtime.
    bash.BASH_SYSTEM_PROMPT = ""
    bash.EDIT_SYSTEM_PROMPT = ""
    original = bash.PROGRAM_SOURCE
    modified = instrument_program(original, inject_schema_failure_at=inject_schema_failure_at)
    (directory / "bash-original.py").write_text(original)
    (directory / "bash-instrumented.py").write_text(modified)
    (directory / "bash.patch").write_text(
        "".join(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                modified.splitlines(keepends=True),
                fromfile="verifiers/bash/program.py",
                tofile="campaign/bash/program.py",
            )
        )
    )
    (directory / "manifest.json").write_text(
        json.dumps(
            dict(
                verifiers=importlib.metadata.version("verifiers"),
                original_sha256=hashlib.sha256(original.encode()).hexdigest(),
                instrumented_sha256=hashlib.sha256(modified.encode()).hexdigest(),
                offline_fault_at=inject_schema_failure_at,
                client_versions=CLIENT_VERSIONS,
                system_framing=dict(original=framing, campaign=dict(bash="", edit="")),
                behavior="Native Bash harness with MCP exception propagation and schema prefetch; native retry count unchanged.",
            ),
            indent=2,
        )
        + "\n"
    )
    original_check = Harness._check_result

    async def checked(self, trace, runtime, result):
        name = re.sub(r"[^a-zA-Z0-9_-]", "_", str(trace.id))
        for stream in ("stdout", "stderr"):
            path = directory / f"{name}.harness.{stream}.log"
            with path.open("a") as output:
                output.write(redact(getattr(result, stream) or ""))
            path.chmod(0o600)
        return await original_check(self, trace, runtime, result)

    bash.PROGRAM_SOURCE = modified
    Harness._check_result = checked


def main():
    import argparse
    from urllib.parse import urlsplit

    from verifiers.v1.cli.eval.main import main as eval_main

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--diagnostics", type=Path, required=True)
    parser.add_argument("--inject-schema-failure-at", type=int)
    args, remaining = parser.parse_known_args()
    if args.inject_schema_failure_at is not None:
        if args.inject_schema_failure_at < 1 or len(remaining) != 2 or remaining[0] != "@":
            parser.error("Fault injection requires one unmodified offline config")
        config = json.loads(Path(remaining[1]).read_text())
        if config["model"] != "offline/scripted" or urlsplit(config["client"]["base_url"]).hostname != "127.0.0.1":
            parser.error("Fault injection is restricted to the local scripted-model smoke")
    install(args.diagnostics, inject_schema_failure_at=args.inject_schema_failure_at)
    eval_main(remaining)


if __name__ == "__main__":
    main()
