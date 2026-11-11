"""ping_stream -- TWO small paid requests to the model, made the way the stock `bash` harness makes them, before
an exam instance is opened for a rollout of a model that has not been through this route yet.

    <venv python> -B rollouts/tools/ping_stream.py MODEL_ID OUT.json [MAX_TOKENS]

Why, beyond ping_model.py (one plain request): three things decide whether a rollout of a REASONING model lives
or dies, and none of them was exercised by the first rollout (a model without reasoning):

  1. USAGE IN A STREAM. The harness asks for a stream with `stream_options = {"include_usage": true}`; verifiers'
     turn and token caps count the usage the provider reports in that stream. A provider that reported none for
     this model would leave the token caps without effect (the spend bound of the rollout rests on them).
  2. THE SECOND TURN. The harness appends the streamed assistant message as it stands (tool calls, and whatever
     reasoning fields the provider streamed: `reasoning`, `reasoning_content`, `reasoning_details`) and sends it
     back with the tool's result. A provider that refuses its own reasoning fields on the way back would end the
     rollout at its second model call, after the instance was opened and used up.
  3. WHAT `max_tokens` COVERS. For a model whose reasoning is mandatory the per-reply cap covers reasoning and
     answer together; the record shows the reasoning tokens of each reply and its finish reason.

Request 1: a system line, a user line asking for one call of the `bash` tool, the harness's own tool definitions
(`bash`, `edit`); request 2: the same conversation plus the assistant message and a made-up tool result. Both
are read with the harness's own stream reader (verifiers.v1.harnesses.utils.core._read_chat_completion), so the
message that goes back is the one the harness would send. Nothing is run: the tool result is a constant.

Like ping_model.py: the process re-executes itself with PATH, HOME, USER, LANG, the two model variables and
SSL_CERT_FILE only; the key is read from the environment inside this process and is never printed, written or
put on a command line. OUT.json gets status, usage numbers, finish reasons, field NAMES and lengths: no header,
no key, no account identifier, no text of the model. Cost: at most 2 x MAX_TOKENS output tokens (default 2048
each) and a few hundred input tokens; entered in LEDGER.md like any other spend.
"""
import asyncio
import json
import os
import sys
import time

CA_BUNDLE = "/root/.ccr/ca-bundle.crt"
STAGE = "ROLLOUT_PING_STAGE"
BASE_URL = "https://api.pinference.ai/api/v1"


def usage_numbers(usage) -> dict | None:
    if usage is None:
        return None
    d = usage.model_dump() if hasattr(usage, "model_dump") else dict(usage)
    out = {}
    for k, v in d.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            out[k] = v
        elif isinstance(v, dict):
            out[k] = {kk: vv for kk, vv in v.items() if isinstance(vv, (int, float)) and not isinstance(vv, bool)}
    return out


async def one(client, core, model, messages, tools, max_tokens) -> tuple[dict, dict | None]:
    t0 = time.time()
    rec = {"n_messages_sent": len(messages)}
    try:
        raw = await client.chat.completions.create(model=model, messages=messages, tools=tools, max_tokens=max_tokens,
                                                   stream=True, stream_options={"include_usage": True})
        completion = await core._read_chat_completion(raw)
    except Exception as e:                                   # the class and the status only: a text could quote a header
        rec.update(ok=False, exception=type(e).__name__, http_status=getattr(e, "status_code", None),
                   error_code=getattr(e, "code", None), error_type=getattr(e, "type", None),
                   error_message_characters=len(str(getattr(e, "message", "") or "")), seconds=round(time.time() - t0, 2))
        return rec, None
    choice = completion.choices[0]
    msg = choice.message.model_dump(exclude_none=True)
    rec.update(ok=True, seconds=round(time.time() - t0, 2), finish_reason=choice.finish_reason, usage=usage_numbers(completion.usage),
               message_fields=sorted(k for k, v in msg.items() if v not in (None, "", [])),
               content_characters=len(msg.get("content") or ""),
               tool_calls=[{"name": c["function"]["name"], "arguments_characters": len(c["function"].get("arguments") or "")}
                           for c in msg.get("tool_calls") or []],
               reasoning_fields={k: (len(msg[k]) if isinstance(msg[k], (str, list)) else 1)
                                 for k in ("reasoning", "reasoning_content", "reasoning_details") if msg.get(k)})
    return rec, msg


async def run(model: str, max_tokens: int) -> dict:
    import httpx
    from openai import AsyncOpenAI, DefaultAsyncHttpxClient
    from verifiers.v1.harnesses.utils import core
    headers = {"X-Prime-Team-ID": os.environ["PRIME_TEAM_ID"]} if os.environ.get("PRIME_TEAM_ID") else None
    client = AsyncOpenAI(base_url=BASE_URL, api_key=os.environ["PRIME_API_KEY"], default_headers=headers, max_retries=0,
                         timeout=httpx.Timeout(300.0, connect=5.0), http_client=DefaultAsyncHttpxClient(verify=CA_BUNDLE))
    tools = [core.BASH_TOOL, core.EDIT_TOOL]
    messages = [{"role": "system", "content": "You are a coding agent. You have access to a bash tool for running shell commands. "
                                              "You also have an edit tool for single-occurrence string replacement in a file."},
                {"role": "user", "content": "Call the bash tool exactly once with the command `echo ok`. After you see its "
                                            "result, reply with the single word: done"}]
    out = {"model": model, "base_url": BASE_URL, "unix": time.time(), "max_tokens_per_reply": max_tokens,
           "as_the_harness_sends_it": "chat.completions, stream=true, stream_options.include_usage=true, tools=[bash, edit]",
           "environment_names": sorted(k for k in os.environ if k != STAGE)}
    r1, msg = await one(client, core, model, messages, tools, max_tokens)
    out["request_1"] = r1
    if msg is not None and msg.get("tool_calls"):
        messages.append(msg)
        for c in msg["tool_calls"]:
            messages.append({"role": "tool", "tool_call_id": c["id"], "content": "ok\n", "name": c["function"]["name"]})
        r2, _ = await one(client, core, model, messages, tools, max_tokens)
        out["request_2"] = r2
    else:
        out["request_2"] = {"ok": None, "skipped": "request 1 returned no tool call"}
    await client.close()
    return out


def main() -> int:
    model, out = sys.argv[1], sys.argv[2]
    max_tokens = int(sys.argv[3]) if len(sys.argv) > 3 else 2048
    if not 16 <= max_tokens <= 8192:
        raise SystemExit("refused: MAX_TOKENS must be from 16 to 8192")
    if os.environ.get(STAGE) != "2":
        env = {k: os.environ[k] for k in ("PATH", "HOME", "USER", "LANG", "PRIME_API_KEY", "PRIME_TEAM_ID") if k in os.environ}
        env.update({"SSL_CERT_FILE": CA_BUNDLE, STAGE: "2"})
        os.execve(sys.executable, [sys.executable, "-I", "-B", os.path.abspath(__file__), *sys.argv[1:]], env)
    rec = asyncio.run(run(model, max_tokens))
    with open(out, "w") as f:
        json.dump(rec, f, indent=1)
    brief = {k: {kk: rec[k].get(kk) for kk in ("ok", "exception", "http_status", "finish_reason", "usage", "seconds", "tool_calls",
                                               "reasoning_fields", "message_fields", "content_characters")}
             for k in ("request_1", "request_2")}
    print(json.dumps(brief, indent=1))
    return 0 if rec["request_1"].get("ok") and rec["request_2"].get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
