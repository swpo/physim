"""standin_model -- a local stand-in for the model endpoint, for tests of the spend stop and of the request route.

It calls no model and costs nothing. It listens on 127.0.0.1 only, answers the two routes verifiers uses
(`POST /v1/chat/completions`, streamed or not, and `GET /v1/models` in the shape of Prime's listing) and plays a
SCRIPT: a JSON list of steps, one per request, the last step repeated for ever. A step:

    {"say": "text"}                              an assistant message, finish_reason "stop"
    {"bash": "echo hi"}                          one call of the harness's `bash` tool
    {"tool": "lab_call", "arguments": {...}}     one call of any other tool
    "usage": {"prompt_tokens": 1200, "completion_tokens": 40, "cached_tokens": 1000, "cost": 0.01}
                                                 what the reply reports; "usage": null reports none; left out, the
                                                 stand-in counts one token per four bytes of the request
    "status": 500                                an error reply instead (no usage)
    "sleep": 2.0                                 seconds before the answer

As a program (the vf-eval tests): it prints one JSON line {"pid", "port", "base_url"} and serves until it gets
SIGTERM. The test that started it stops it by that exact pid.

    python -B tools/standin_model.py --script steps.json [--port 0] [--model standin/echo-1] [--log requests.jsonl]

As a module (tools/check_round4.py): `Standin(script).start()` serves from a thread of the caller's process.
"""
from __future__ import annotations

import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODEL = "standin/echo-1"
PRICING = {"input_usd_per_mtok": 2.0, "output_usd_per_mtok": 10.0, "cache_read_usd_per_mtok": 0.5, "cache_write_usd_per_mtok": None}
CONTEXT_WINDOW = 100_000


def model_entry(model: str = MODEL, pricing: dict | None = None, context_window: int = CONTEXT_WINDOW) -> dict:
    return {"id": model, "object": "model", "name": "stand-in", "context_length": context_window, "context_window": context_window,
            "max_output_tokens": 4096, "pricing": dict(PRICING if pricing is None else pricing)}


class Standin:
    def __init__(self, script: list[dict], *, model: str = MODEL, pricing: dict | None = None, context_window: int = CONTEXT_WINDOW,
                 port: int = 0, log: str | None = None):
        self.script, self.model, self.pricing, self.context_window, self.log = list(script), model, pricing, context_window, log
        self.requests: list[dict] = []                       # what arrived: counts and header names only
        self.lock = threading.Lock()
        outer = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *args):
                pass

            def _send(self, status: int, body: bytes, content_type: str = "application/json"):
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if self.path.rstrip("/").endswith("/models"):
                    return self._send(200, json.dumps({"object": "list", "data": [model_entry(outer.model, outer.pricing, outer.context_window)]}).encode())
                return self._send(404, b"{}")

            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                try:
                    body = json.loads(raw)
                except ValueError:
                    body = {}
                with outer.lock:
                    n = len(outer.requests)
                    step = outer.script[min(n, len(outer.script) - 1)] if outer.script else {"say": "done"}
                    record = {"n": n + 1, "path": self.path, "bytes": len(raw), "stream": bool(body.get("stream")),
                              "messages": len(body.get("messages") or []), "max_tokens": body.get("max_tokens"),
                              "model": body.get("model"), "has_authorization": "authorization" in {k.lower() for k in self.headers},
                              "session": bool(self.headers.get("X-Session-ID")), "time_unix": time.time()}
                    outer.requests.append(record)
                    if outer.log:
                        with open(outer.log, "a") as f:
                            f.write(json.dumps(record) + "\n")
                if step.get("sleep"):
                    time.sleep(float(step["sleep"]))
                if not self.path.endswith("/chat/completions"):
                    return self._send(404, b'{"error": {"message": "the stand-in serves chat completions only"}}')
                if step.get("status", 200) != 200:
                    return self._send(int(step["status"]), json.dumps({"error": {"message": "stand-in error", "type": "server_error"}}).encode())
                message, finish = outer.message(step, n)
                usage = outer.usage(step, len(raw), message)
                ident = f"standin-{n + 1}"
                if not body.get("stream"):
                    reply = {"id": ident, "object": "chat.completion", "created": int(time.time()), "model": outer.model,
                             "choices": [{"index": 0, "message": message, "finish_reason": finish}]}
                    if usage is not None:
                        reply["usage"] = usage
                    return self._send(200, json.dumps(reply).encode())
                base = {"id": ident, "object": "chat.completion.chunk", "created": int(time.time()), "model": outer.model}
                delta = {"role": "assistant", "content": message.get("content") or ""}
                if message.get("tool_calls"):
                    delta["tool_calls"] = [dict(c, index=i) for i, c in enumerate(message["tool_calls"])]
                events = [dict(base, choices=[{"index": 0, "delta": delta, "finish_reason": None}]),
                          dict(base, choices=[{"index": 0, "delta": {}, "finish_reason": finish}])]
                if usage is not None:
                    events.append(dict(base, choices=[], usage=usage))
                out = b"".join(b"data: " + json.dumps(e).encode() + b"\n\n" for e in events) + b"data: [DONE]\n\n"
                return self._send(200, out, "text/event-stream")

        self.server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        self.server.daemon_threads = True
        self.port = self.server.server_address[1]
        self.base_url = f"http://127.0.0.1:{self.port}/v1"
        self.thread: threading.Thread | None = None

    def message(self, step: dict, n: int) -> tuple[dict, str]:
        if "bash" in step or "tool" in step:
            name = "bash" if "bash" in step else step["tool"]
            args = {"command": step["bash"]} if "bash" in step else step.get("arguments") or {}
            return ({"role": "assistant", "content": step.get("say") or "",
                     "tool_calls": [{"id": f"call_{n + 1}", "type": "function",
                                     "function": {"name": name, "arguments": json.dumps(args)}}]}, "tool_calls")
        return {"role": "assistant", "content": step.get("say", "done")}, "stop"

    def usage(self, step: dict, request_bytes: int, message: dict):
        if "usage" in step:
            u = step["usage"]
            if u is None:
                return None
            out = {k: v for k, v in u.items() if k not in ("cached_tokens", "reasoning_tokens")}
            if "cached_tokens" in u:
                out["prompt_tokens_details"] = {"cached_tokens": u["cached_tokens"]}
            if "reasoning_tokens" in u:
                out["completion_tokens_details"] = {"reasoning_tokens": u["reasoning_tokens"]}
            if "prompt_tokens" in out and "completion_tokens" in out:
                out.setdefault("total_tokens", out["prompt_tokens"] + out["completion_tokens"])
            return out
        prompt, completion = max(1, request_bytes // 4), max(1, len(json.dumps(message)) // 4)
        return {"prompt_tokens": prompt, "completion_tokens": completion, "total_tokens": prompt + completion}

    def start(self) -> "Standin":
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        self.thread.start()
        return self

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()


def main(argv=None) -> int:
    import argparse
    import os
    import signal
    ap = argparse.ArgumentParser(description="a local stand-in for the model endpoint (tests only; no model, no cost)")
    ap.add_argument("--script", required=True, help="JSON file: the list of steps")
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--context-window", type=int, default=CONTEXT_WINDOW)
    ap.add_argument("--log", default=None, help="append one JSON line per request (counts only)")
    a = ap.parse_args(argv)
    with open(a.script) as f:
        script = json.load(f)
    s = Standin(script, model=a.model, port=a.port, log=a.log, context_window=a.context_window)
    signal.signal(signal.SIGTERM, lambda *_: threading.Thread(target=s.server.shutdown, daemon=True).start())
    print(json.dumps({"pid": os.getpid(), "port": s.port, "base_url": s.base_url, "model": a.model}), flush=True)
    try:
        s.server.serve_forever(poll_interval=0.1)
    finally:
        s.server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
