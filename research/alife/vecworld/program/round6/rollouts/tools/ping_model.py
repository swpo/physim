"""ping_model -- ONE tiny paid request to the model, from the same environment vf-eval will have, before an
exam instance is opened for a rollout.

    <venv python> -B rollouts/tools/ping_model.py MODEL_ID OUT.json

Why: `GET /api/v1/models` answers 200 without any credential, so a listed model says nothing about the key. A
rollout whose first model call is refused has still opened (and used up) its instance. This sends one chat
completion with one trivial tool offered and `max_tokens = 16`: a few dozen tokens, well under a hundredth of
a cent, entered in LEDGER.md like any other spend.

The request is made as verifiers' eval client makes it: httpx, `Authorization: Bearer` from PRIME_API_KEY, the
team in `X-Prime-Team-ID`, and of the session's environment only PATH, HOME, USER, LANG plus SSL_CERT_FILE (the
machine's CA bundle): the process re-executes itself in that environment first. The key is read from the
environment inside this process and is never printed, written or put on a command line. OUT.json gets the
HTTP status, the usage the provider reported, the finish reason and the names of the response's fields: no
header, no key, no account identifier.
"""
import json
import os
import sys
import time

CA_BUNDLE = "/root/.ccr/ca-bundle.crt"
STAGE = "ROLLOUT_PING_STAGE"
URL = "https://api.pinference.ai/api/v1/chat/completions"


def main() -> int:
    model, out = sys.argv[1], sys.argv[2]
    if os.environ.get(STAGE) != "2":
        env = {k: os.environ[k] for k in ("PATH", "HOME", "USER", "LANG", "PRIME_API_KEY", "PRIME_TEAM_ID") if k in os.environ}
        env.update({"SSL_CERT_FILE": CA_BUNDLE, STAGE: "2"})
        os.execve(sys.executable, [sys.executable, "-I", "-B", os.path.abspath(__file__), model, out], env)
    import httpx
    headers = {"Authorization": "Bearer " + os.environ["PRIME_API_KEY"], "Content-Type": "application/json"}
    if os.environ.get("PRIME_TEAM_ID"):
        headers["X-Prime-Team-ID"] = os.environ["PRIME_TEAM_ID"]
    body = {"model": model, "max_tokens": 16,
            "messages": [{"role": "user", "content": "Reply with the single word: ok"}],
            "tools": [{"type": "function", "function": {"name": "noop", "description": "does nothing", "parameters": {"type": "object", "properties": {}}}}]}
    t0 = time.time()
    rec = {"model": model, "url": URL, "unix": t0, "environment_names": sorted(k for k in os.environ if k != STAGE)}
    try:
        r = httpx.post(URL, headers=headers, json=body, timeout=httpx.Timeout(connect=5.0, read=120.0, write=30.0, pool=30.0))
        rec.update(http_status=r.status_code, seconds=round(time.time() - t0, 2))
        try:
            d = r.json()
        except ValueError:
            d = None
        if isinstance(d, dict):
            rec["response_fields"] = sorted(d)
            rec["usage"] = d.get("usage")
            ch = (d.get("choices") or [{}])[0]
            rec["finish_reason"] = ch.get("finish_reason")
            msg = ch.get("message") or {}
            rec["message_fields"] = sorted(k for k, v in msg.items() if v not in (None, "", []))
            rec["content_characters"] = len(msg.get("content") or "")
            rec["tool_calls"] = len(msg.get("tool_calls") or [])
            if r.status_code >= 400:
                err = d.get("error") if isinstance(d.get("error"), dict) else {}
                rec["error_type"], rec["error_code"] = err.get("type"), err.get("code")
                rec["error_message_characters"] = len(str(err.get("message") or d.get("detail") or ""))
    except Exception as e:                                   # the class only: an error text could quote a header
        rec.update(http_status=None, exception=type(e).__name__, seconds=round(time.time() - t0, 2))
    with open(out, "w") as f:
        json.dump(rec, f, indent=1)
    print(json.dumps({k: rec.get(k) for k in ("http_status", "exception", "finish_reason", "usage", "seconds", "error_type", "error_code")}))
    return 0 if rec.get("http_status") == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
