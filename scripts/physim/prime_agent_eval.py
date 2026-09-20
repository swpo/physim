"""Run the native Verifiers CLI with diagnostic capture only, no agent-loop patch."""

import argparse
import json
import time
from pathlib import Path

from campaign_diagnostics import redact
from verifiers.v1.cli.eval.main import main as eval_main
from verifiers.v1.clients.eval import EvalClient
from verifiers.v1.harness import Harness


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--diagnostics", type=Path, required=True)
    args, remaining = parser.parse_known_args()
    args.diagnostics.mkdir(parents=True, exist_ok=True)
    original = Harness._check_result
    original_relay = EvalClient.relay

    async def relay(self, dialect, body, session_id=None, headers=None):
        # Save only protocol settings and native usage buckets, never request
        # headers or prompt contents. Streaming is forwarded unchanged.
        reply = await original_relay(self, dialect, body, session_id, headers)
        chunks = reply.chunks
        identity = {
            "time_ns": time.time_ns(),
            "model": body.get("model"),
            "path": dialect.upstream_path,
            "settings": {
                k: body[k]
                for k in (
                    "reasoning",
                    "reasoning_effort",
                    "thinking",
                    "output_config",
                    "max_tokens",
                    "max_output_tokens",
                    "enable_thinking",
                )
                if k in body
            },
        }

        async def captured():
            async for chunk in chunks:
                for line in chunk.decode(errors="replace").splitlines():
                    if line.startswith("data:"):
                        try:
                            event = json.loads(line[5:])
                        except ValueError:
                            continue
                        payload = event.get("message") or event.get("response") or event
                        if payload.get("usage"):
                            with (args.diagnostics / "native-usage.jsonl").open("a") as out:
                                out.write(
                                    json.dumps({**identity, "event": event.get("type"), "usage": payload["usage"]})
                                    + "\n"
                                )
                yield chunk

        reply.chunks = captured()
        return reply

    async def checked(self, trace, runtime, result):
        for stream in ("stdout", "stderr"):
            path = args.diagnostics / f"{trace.id}.harness.{stream}.log"
            path.write_text(redact(getattr(result, stream) or ""))
            path.chmod(0o600)
        return await original(self, trace, runtime, result)

    Harness._check_result = checked
    EvalClient.relay = relay
    eval_main(remaining)


if __name__ == "__main__":
    main()
