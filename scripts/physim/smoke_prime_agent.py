"""No-charge full Prime Agent / Docker / MCP / grading integration test."""

import argparse
import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from physim.bundles import Bundle
from run_campaign import configuration, dump
from smoke_campaign import BOUNDARY_PROBE, PREDICTOR


def main(root, bundle):
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=False)
    dump(root / "prime_agent.json", {"image": "physim-prime-agent:0.9.5"})
    steps = [
        BOUNDARY_PROBE,
        "print(await mcp.list_tools('laboratory'))",
        "print(await mcp.call_tool('laboratory', 'experiment', "
        + repr({"actions": [], "queries": [{"sensor": s, "t": [0]} for s in ("device0", "device1", "global")]})
        + "))",
        "from pathlib import Path\nPath('/workspace/predictor.py').write_text("
        + repr(PREDICTOR)
        + ")\nprint('written')",
        "print(await mcp.call_tool('laboratory', 'validate', {}))",
        "print(await mcp.call_tool('laboratory', 'submit', {}))",
    ]
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            i = len(requests)
            requests.append(body)
            dump(root / "requests.json", requests)
            delta = {"role": "assistant", "content": "Submitted."}
            reason = "stop"
            if i < len(steps):
                delta = {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "index": 0,
                            "id": f"call_{i}",
                            "type": "function",
                            "function": {"name": "ipython", "arguments": json.dumps({"code": steps[i]})},
                        }
                    ],
                }
                reason = "tool_calls"
            base = {"id": f"offline-{i}", "object": "chat.completion.chunk", "created": 0, "model": body["model"]}
            chunks = [
                dict(base, choices=[{"index": 0, "delta": delta, "finish_reason": None}]),
                dict(
                    base,
                    choices=[{"index": 0, "delta": {}, "finish_reason": reason}],
                    usage={"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20, "cost": 0},
                ),
            ]
            encoded = "".join("data: " + json.dumps(c) + "\n\n" for c in chunks).encode() + b"data: [DONE]\n\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    model = {
        "id": "offline/scripted",
        "specs": {"context_window": 131072, "max_output_tokens": 8192},
        "pricing": {"input_usd_per_mtok": 0, "output_usd_per_mtok": 0},
    }
    config = configuration(root, root, model, bundle.resolve())
    config["client"] = {
        "type": "eval",
        "base_url": f"http://127.0.0.1:{server.server_port}/v1",
        "api_key_var": "PHYSIM_OFFLINE_SMOKE_KEY",
        "headers": {},
    }
    dump(root / "eval.json", config)
    try:
        with (root / "eval.log").open("w") as log:
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("prime_agent_eval.py")),
                    "--diagnostics",
                    str(root / "diagnostics"),
                    "@",
                    str(root / "eval.json"),
                ],
                stdout=log,
                stderr=subprocess.STDOUT,
                env={**os.environ, "PHYSIM_OFFLINE_SMOKE_KEY": "offline-only-no-credential"},
            )
    finally:
        server.shutdown()
        server.server_close()
    traces = list((root / "runs").glob("*/traces.jsonl"))
    if not traces:
        raise RuntimeError(f"No trace; inspect {root}/eval.log (exit {result.returncode})")
    trace = json.loads(traces[0].read_text().splitlines()[-1])["traces"][-1]
    outputs = [m["content"] for r in requests for m in r.get("messages", []) if m["role"] == "tool"]
    report = {
        "ok": trace["ok"],
        "errors": trace.get("errors"),
        "calls": len(requests),
        "info": trace.get("info"),
        "tool_outputs": outputs,
    }
    dump(root / "report.json", report)
    assert trace["ok"], trace.get("errors")
    assert len(requests) == len(steps) + 1
    assert any('"boundary_audit"' in str(x) and "false" not in str(x).lower() for x in outputs)
    expected = json.loads(Bundle(bundle).verified_path("checks.json").read_text())["reference"]["primary_joint_energy"]
    assert abs(trace["info"]["r6"]["primary_joint_energy"] - expected) < 1e-10
    print(json.dumps({"ok": True, "calls": len(requests), "energy": expected, "reported_cost": 0}))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--bundle", type=Path, default=Path("outputs/eval-preparation-20260916/bf/bundle"))
    args = p.parse_args()
    main(args.output, args.bundle)
