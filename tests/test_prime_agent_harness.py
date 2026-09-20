"""Interception, state isolation, and native transport configuration."""

import asyncio
import json
from types import SimpleNamespace

import pytest
from physim_prime_agent import PrimeAgentConfig, PrimeAgentHarness


@pytest.mark.parametrize(
    "transport,api,base",
    [
        ("chat_completions", "openai-completions", "http://proxy:123/v1"),
        ("responses", "openai-responses", "http://proxy:123/v1"),
        ("anthropic_messages", "anthropic-messages", "http://proxy:123"),
    ],
)
def test_native_program_only_has_interception_credentials_and_fresh_home(transport, api, base):
    writes = {}

    async def write(path, data):
        writes[path] = data

    async def run(argv, env):
        return argv, env

    harness = PrimeAgentHarness(
        PrimeAgentConfig(
            id="physim_prime_agent",
            transport=transport,
            context_window=262144,
            max_response_tokens=65536,
            thinking="max",
        )
    )
    trace = SimpleNamespace(id="fresh-rollout", info={})
    argv, env = asyncio.run(
        harness.launch(
            SimpleNamespace(model="test/model"),
            trace,
            SimpleNamespace(write=write, run_program=run),
            "http://proxy:123/v1",
            "interception-only",
            {"laboratory": "http://proxy:456/mcp"},
            SimpleNamespace(system_prompt="Public task", prompt="Begin"),
        )
    )
    home = env["PRIME_AGENT_CODING_AGENT_DIR"]
    assert home.startswith("/workspace/.vf-")
    provider = json.loads(writes[home + "/models.json"])["providers"]["physim"]
    assert provider["baseUrl"] == base and provider["api"] == api
    assert provider["apiKey"] == "PHYSIM_INTERCEPT_KEY"
    assert env["PHYSIM_INTERCEPT_KEY"] == "interception-only"
    assert not any(k in env for k in ("PRIME_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"))
    settings = json.loads(writes[home + "/settings.json"])
    assert settings["mcpServers"]["laboratory"]["url"] == "http://proxy:456/mcp"
    assert all(v == "unlimited" for v in settings["autonomous"].values())
    assert settings["telemetry"]["enabled"] is False
    assert settings["bundledSkills"]["websearch"] is False
    assert argv[0] == "prime-agent" and "--offline" in argv
    assert "--continue" not in argv and "--resume" not in argv
    assert trace.info["prime_agent"]["transport"] == transport
