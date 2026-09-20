"""Exercise the stock Bash MCP client with injected local transport failures."""

import asyncio
import importlib.util
import json
from contextlib import asynccontextmanager
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

import httpx
import pytest
import verifiers.v1.harnesses.bash.harness as bash


def stock_program():
    path = Path(bash.__file__).with_name("program.py")
    spec = importlib.util.spec_from_file_location("stock_bash_program_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MCPTransport:
    def __init__(self, fail_schema_once=False):
        self.fail_schema_once = fail_schema_once
        self.executed = 0
        self.methods = []

    async def __call__(self, request):
        if request.method != "POST":
            return httpx.Response(405)
        body = json.loads(request.content)
        method = body["method"]
        self.methods.append(method)
        if "id" not in body:
            return httpx.Response(202)
        if method == "initialize":
            result = dict(
                protocolVersion=body["params"]["protocolVersion"],
                capabilities={"tools": {}},
                serverInfo={"name": "offline", "version": "1"},
            )
        elif method == "tools/call":
            self.executed += 1
            result = {"content": [{"type": "text", "text": "ok"}], "isError": False}
        elif method == "tools/list":
            if self.fail_schema_once:
                self.fail_schema_once = False
                raise httpx.ConnectError("injected schema connection failure", request=request)
            result = {"tools": [{"name": "ping", "inputSchema": {"type": "object"}}]}
        else:
            raise AssertionError(method)
        return httpx.Response(200, json={"jsonrpc": "2.0", "id": body["id"], "result": result})


def client_factory(transport):
    return lambda **kwargs: httpx.AsyncClient(transport=httpx.MockTransport(transport))


def test_stock_schema_transport_failure_escapes_as_cancellation():
    transport = MCPTransport(fail_schema_once=True)
    program = stock_program()

    async def run():
        with patch("mcp.client.streamable_http.create_mcp_http_client", client_factory(transport)):
            with pytest.raises(asyncio.CancelledError):
                await program.call_mcp({"lab": {"url": "http://offline/mcp"}}, {"ping": ("lab", "ping")}, "ping", {})

    asyncio.run(run())
    assert transport.executed == 1
    assert transport.methods.count("tools/list") == 1  # native retry was bypassed


def diagnostics_module():
    path = Path(__file__).resolve().parents[1] / "scripts/physim/campaign_diagnostics.py"
    spec = importlib.util.spec_from_file_location("campaign_diagnostics_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def repaired_program():
    module = ModuleType("instrumented_bash_test")
    source = diagnostics_module().instrument_program(bash.PROGRAM_SOURCE)
    exec(compile(source, "instrumented_bash.py", "exec"), module.__dict__)
    module.wait_exponential_jitter = lambda **kwargs: __import__("tenacity").wait_none()
    return module


def test_schema_failure_retries_before_tool_side_effect():
    transport = MCPTransport(fail_schema_once=True)
    program = repaired_program()

    async def run():
        with patch("mcp.client.streamable_http.create_mcp_http_client", client_factory(transport)):
            result = await program.call_mcp(
                {"lab": {"url": "http://offline/mcp"}}, {"ping": ("lab", "ping")}, "ping", {}
            )
            assert result == "ok"

    asyncio.run(run())
    assert transport.methods.count("initialize") == 2
    assert transport.methods.count("tools/list") == 2
    assert transport.executed == 1


def test_external_cancellation_is_never_retried():
    transport = MCPTransport()
    program = repaired_program()

    async def run():
        started = asyncio.Event()

        async def blocked(request):
            if request.method == "POST" and json.loads(request.content)["method"] == "tools/list":
                started.set()
                await asyncio.Event().wait()
            return await transport(request)

        with patch("mcp.client.streamable_http.create_mcp_http_client", client_factory(blocked)):
            task = asyncio.create_task(
                program.call_mcp(
                    {"lab": {"url": "http://offline/mcp"}},
                    {"ping": ("lab", "ping")},
                    "ping",
                    {},
                )
            )
            await asyncio.wait_for(started.wait(), timeout=5)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

    asyncio.run(run())
    assert transport.methods.count("initialize") == 1
    assert transport.executed == 0


def test_cleanup_failure_after_answer_does_not_replay_tool():
    from mcp.client.streamable_http import streamable_http_client

    transport = MCPTransport()
    program = repaired_program()

    @asynccontextmanager
    async def noisy_cleanup(*args, **kwargs):
        async with streamable_http_client(*args, **kwargs) as values:
            yield values
        raise RuntimeError("injected cleanup noise after response")

    async def run():
        with (
            patch("mcp.client.streamable_http.create_mcp_http_client", client_factory(transport)),
            patch("mcp.client.streamable_http.streamable_http_client", noisy_cleanup),
        ):
            assert (
                await program.call_mcp(
                    {"lab": {"url": "http://offline/mcp"}},
                    {"ping": ("lab", "ping")},
                    "ping",
                    {},
                )
                == "ok"
            )

    asyncio.run(run())
    assert transport.executed == 1


def test_permanent_schema_failure_retains_native_retry_bound():
    transport = MCPTransport()
    program = repaired_program()

    async def failing(request):
        transport.fail_schema_once = True
        return await transport(request)

    async def run():
        with patch("mcp.client.streamable_http.create_mcp_http_client", client_factory(failing)):
            with pytest.raises(ExceptionGroup):
                await program.call_mcp(
                    {"lab": {"url": "http://offline/mcp"}},
                    {"ping": ("lab", "ping")},
                    "ping",
                    {},
                )

    asyncio.run(run())
    assert transport.methods.count("tools/list") == program.MCP_CALL_ATTEMPTS == 6
    assert transport.executed == 0


def test_diagnostics_redact_auth_and_query_secrets():
    value = diagnostics_module().redact(
        "Authorization: Bearer private-token --api-key=private-key http://host/mcp?vf_state_signature=secret-value"
    )
    for secret in ("private-token", "private-key", "secret-value"):
        assert secret not in value


def test_full_harness_error_is_saved_before_native_truncation(tmp_path, monkeypatch):
    from verifiers.v1.harness import Harness

    async def native_check(*args):
        raise RuntimeError("native error still propagates")

    monkeypatch.setattr(bash, "PROGRAM_SOURCE", bash.PROGRAM_SOURCE)
    monkeypatch.setattr(Harness, "_check_result", native_check)
    diagnostics_module().install(tmp_path)
    result = SimpleNamespace(
        stdout="", stderr="root cause first\n" + "x" * 5000 + "\nAuthorization: Bearer private-token"
    )
    with pytest.raises(RuntimeError, match="native error still propagates"):
        asyncio.run(Harness._check_result(None, SimpleNamespace(id="trace"), None, result))
    saved = (tmp_path / "trace.harness.stderr.log").read_text()
    assert saved.startswith("root cause first") and len(saved) > 5000
    assert "private-token" not in saved
    assert json.loads((tmp_path / "manifest.json").read_text())["offline_fault_at"] is None
