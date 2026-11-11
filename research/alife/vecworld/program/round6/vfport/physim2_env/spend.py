"""The spend stop: every model call of a rollout is admitted, counted and priced inside vf-eval, on the host.

WHERE. verifiers sends every request to the provider through one method of one object in the vf-eval process:
`EvalClient._request` (clients/eval.py:124-164; `get_response`, `relay` and `relay_aux` all end there, and the
client itself never retries: clients/base.py:14-16). A box has no key and no route to the provider; its harness
talks to verifiers' interception server, which calls that client once per real exchange (interception/
server.py:773-800; a retry of the harness's SDK is a new request there, and either replays a finished answer
without a provider call or makes a new one, which is counted like any other). `install()` wraps that one
method. Nothing here is reachable from a box: the meter is a Python object of the vf-eval process.

WHAT, per HTTP attempt to the provider (Meter.admit, before anything is sent):
  1. the run is not stopped, and  counted + (attempts in flight) x worst  <  cap_usd   (else stop `spend_cap`);
  2. the request is one this meter can bound: the chat-completions route, the configured model, `max_tokens`
     present and at most the cap, one choice, text content and function tools only (else stop
     `model_request_refused`; verifiers also serves the Responses and Anthropic routes to a box, and their
     auxiliary routes: none of them passes);
  3. an upper bound on the prompt's tokens is at most max_context_tokens (else stop `max_context_tokens`).
     The bound: the provider's own count of the previous prompt, when this request repeats that prompt's
     messages exactly, plus ONE TOKEN PER BYTE for everything added since (and 16 per message); or one token
     per byte of the whole request when there is no such previous prompt. (A token is at least one byte of
     text in every tokenizer we know of; per-message framing is covered by the JSON's own keys and the 16.)
and after it (Meter.settle):
  4. a reply with complete usage costs what the usage says at the LISTED prices: non-cached prompt tokens at
     the input price, cache reads at the listed cache-read price if the run's record holds one and at the
     input price otherwise, completion tokens (reasoning included) at the output price; the provider's own
     `cost` field is taken instead when it is higher;
  5. anything else costs ONE WORST-CASE CALL: an error status, a timeout, a cut connection, a streamed reply
     without a final usage chunk, usage with a field missing. Never zero.

  worst = max_context_tokens x input price + max_output_tokens x output price     (one call)

THE BOUND. An attempt is sent only while counted + in-flight x worst < cap_usd, and costs at most `worst`
(point 3 bounds its prompt, the provider's `max_tokens` bounds its reply): the counted cost of a run never
exceeds cap_usd + worst, also with requests in parallel. This rests on two things the meter cannot see: that
the provider bills what its usage says, and that it honours `max_tokens` for reasoning as well.

A stop is a stop, not an error: the trace gets its stop condition, the refused request is answered `400
rollout stopped: <condition>` exactly as verifiers answers at max_turns, and finalize and scoring run (ruling
E1). The task's `@vf.stop spend_cap` makes the same check before each turn (taskset.py), so the usual end of a
run at its cap never reaches the wrapper at all.

Every attempt is appended to the file named by $PHYSIM2_SPEND_LOG (set by tools/vfrun.py: a file in the run
folder on the host; counts, prices and words only, never message text).
"""
from __future__ import annotations

import hashlib
import json
import os
import time

from pydantic import BaseModel

MTOK = 1_000_000
LOG_ENV = "PHYSIM2_SPEND_LOG"
PER_MESSAGE = 16
SLACK = 64
METERS: dict = {}                                            # trace id -> Meter, in this vf-eval process only
_INSTALLED = False


class SpendConfig(BaseModel):
    """`[env.taskset.task.spend]`: written by tools/vfrun.py for a model run, never by a rollout config. With
    no `cap_usd` there is no meter, and without a meter no model call leaves this process."""
    model_config = {"extra": "forbid"}
    cap_usd: float | None = None
    max_context_tokens: int | None = None
    max_output_tokens: int | None = None                     # per reply: must equal [sampling] max_tokens
    model: str = ""
    input_usd_per_mtok: float | None = None
    output_usd_per_mtok: float | None = None
    cache_read_usd_per_mtok: float | None = None             # None = not listed: cache reads at the input price
    context_window: int | None = None
    prices_from: str = ""                                    # where and when the prices were read (words)
    billed: bool = True                                      # False for a run against a local stand-in endpoint
    reasoning_effort: str | None = None                      # round 5 (K10): the config's effort; None = "default" (nothing sent)


class Refused(Exception):
    def __init__(self, condition: str, detail: str = ""):
        super().__init__(condition)
        self.condition, self.detail = condition, detail


def worst_call_usd(max_context_tokens: int, max_output_tokens: int, p_in: float, p_out: float) -> float:
    return (max_context_tokens * p_in + max_output_tokens * p_out) / MTOK


def _count(x):
    return x if isinstance(x, int) and not isinstance(x, bool) and x >= 0 else None


def reply_cost(usage, prices: dict, worst: float) -> tuple[float, str, dict]:
    """(dollars, basis, the token counts used) for one attempt. `usage` is the provider's usage object in the
    chat-completions shape, or None. Never returns less than the listed prices give; returns `worst` whenever
    the usage is missing or incomplete."""
    if not isinstance(usage, dict):
        return worst, "worst case: no usage reported", {}
    prompt, completion = _count(usage.get("prompt_tokens")), _count(usage.get("completion_tokens"))
    details = usage.get("prompt_tokens_details")
    cached = _count(details.get("cached_tokens")) if isinstance(details, dict) and details.get("cached_tokens") is not None else 0
    if prompt is None or completion is None or cached is None or cached > prompt:
        return worst, "worst case: usage incomplete", {}
    p_in, p_out, p_cache = prices["input"], prices["output"], prices.get("cache_read")
    listed = ((prompt - cached) * p_in + cached * (p_in if p_cache is None else p_cache) + completion * p_out) / MTOK
    tokens = {"prompt_tokens": prompt, "cached_tokens": cached, "completion_tokens": completion}
    out = usage.get("completion_tokens_details")
    if isinstance(out, dict) and _count(out.get("reasoning_tokens")) is not None:
        tokens["reasoning_tokens"] = out["reasoning_tokens"]
    own = usage.get("cost")
    if isinstance(own, (int, float)) and not isinstance(own, bool) and own == own and own > listed:
        return float(own), "usage, the provider's own cost field (higher than the listed prices give)", tokens
    return listed, "usage at the listed prices" + ("" if p_cache is not None or not cached else " (cache reads at the input price)"), tokens


def _dump(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8", "surrogatepass")


# Second pass (code audit K5): the request keys a model call may carry, and nothing else. What the stock bash
# harness sends (verifiers harnesses/utils/core.py:240-286: model, messages, tools, tool_choice, stream,
# stream_options) and what verifiers' chat dialect lays over it from the run's sampling config (dialects/chat.py:
# 399-423, 583-596). A field a provider could bill or route by (plugins, provider, models, transforms, reasoning,
# service_tier, extra_body, audio, prediction, web search, ...) is not among them and refuses the request unsent.
REQUEST_KEYS = frozenset({"model", "messages", "tools", "tool_choice", "parallel_tool_calls", "stream", "stream_options",
                          "max_tokens", "max_completion_tokens", "n", "temperature", "top_p", "top_k", "min_p", "seed", "stop",
                          "frequency_penalty", "presence_penalty", "repetition_penalty", "reasoning_effort"})
STREAM_OPTION_KEYS = frozenset({"include_usage"})


ANY_EFFORT = object()                                        # check_shape's default: the effort is not compared


def check_shape(body, *, model: str, max_output_tokens: int, reasoning_effort=ANY_EFFORT) -> str | None:
    """Why this request cannot be bounded by the meter, or None. Text chat with function tools, one choice, the
    configured model and reply cap, the keys of REQUEST_KEYS only: everything the stock bash harness sends, and
    nothing a provider could bill beyond prompt and completion tokens. With `reasoning_effort` (round 5, K10: the
    meter passes the config's, None for "default") the request's effort must be exactly that: a box that holds the
    rollout's secret cannot ask for an effort the config never set."""
    if not isinstance(body, dict) or not isinstance(body.get("messages"), list) or not body["messages"]:
        return "no messages"
    unknown = sorted(str(k)[:40] for k in body if k not in REQUEST_KEYS)
    if unknown:
        return "a request key the meter does not know: " + ", ".join(unknown[:4])
    so = body.get("stream_options")
    if so is not None and (not isinstance(so, dict) or any(k not in STREAM_OPTION_KEYS for k in so)):
        return "stream_options other than include_usage"
    if body.get("reasoning_effort") is not None and not isinstance(body.get("reasoning_effort"), str):
        return "a reasoning_effort that is not a word"
    if reasoning_effort is not ANY_EFFORT and body.get("reasoning_effort") != reasoning_effort:
        return "a reasoning_effort other than the config's"
    if body.get("model") != model:
        return "another model"
    caps = [body.get(k) for k in ("max_tokens", "max_completion_tokens") if k in body]
    if not caps or any(_count(c) is None or c < 1 or c > max_output_tokens for c in caps):
        return "no reply cap, or one above the run's"
    if "n" in body and not (body["n"] is None or (type(body["n"]) is int and body["n"] == 1)):   # K10: True is not 1 here
        return "more than one choice, or a choice count that is not the integer 1"
    for key in ("plugins", "web_search_options", "audio", "prediction"):
        if body.get(key):
            return f"field {key}"
    if any(m not in ("text",) for m in body.get("modalities") or []):
        return "a modality other than text"
    for tool in body.get("tools") or []:
        if not isinstance(tool, dict) or tool.get("type") != "function":
            return "a tool that is not a function"
    for m in body["messages"]:
        if not isinstance(m, dict):
            return "a message that is not an object"
        c = m.get("content")
        if c is None or isinstance(c, str):
            continue
        if not isinstance(c, list) or any(not isinstance(p, dict) or p.get("type") != "text" or not isinstance(p.get("text"), str) for p in c):
            return "content that is not text"
    return None


def prompt_bound(body: dict, prev: dict | None) -> tuple[int, str]:
    """An upper bound on the prompt tokens of `body`, and how it was made. `prev` is what settle() kept of the
    last reply with usage: the hashes of its request's messages, the hash of everything else in that request
    that enters a prompt, and the provider's prompt-token count."""
    messages = body["messages"]
    sizes = [len(_dump(m)) for m in messages]
    whole = len(_dump({k: v for k, v in body.items() if k != "messages"})) + sum(sizes) + PER_MESSAGE * len(messages) + SLACK
    if prev:
        n = len(prev["hashes"])
        if len(messages) > n and prev["rest"] == _rest_hash(body) and prev["hashes"] == [_hash(m) for m in messages[:n]]:
            chained = prev["prompt_tokens"] + sum(sizes[n:]) + PER_MESSAGE * (len(messages) - n) + SLACK
            if chained <= whole:
                return chained, "the last reply's prompt count plus the bytes added since"
    return whole, "the bytes of the whole request"


def _hash(obj) -> str:
    return hashlib.sha256(_dump(obj)).hexdigest()


def _rest_hash(body: dict) -> str:
    """Every key of the request but the messages (second pass, K5: the chained prompt bound holds only while all
    of them are what they were for the prompt the provider counted)."""
    return _hash({k: v for k, v in body.items() if k != "messages"})


class Meter:
    def __init__(self, *, model: str, cap_usd: float, max_context_tokens: int, max_output_tokens: int, prices: dict,
                 log_path: str | None = None, billed: bool = True, trace=None, clock=time.time, reasoning_effort: str | None = None):
        for name, v in (("cap_usd", cap_usd), ("input price", prices.get("input")), ("output price", prices.get("output"))):
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not v == v or v < 0 or (name == "cap_usd" and v <= 0):
                raise ValueError(f"spend meter: {name} is not a usable number")
        if _count(max_context_tokens) in (None, 0) or _count(max_output_tokens) in (None, 0) or not model:
            raise ValueError("spend meter: the model, max_context_tokens and max_output_tokens are required")
        self.model, self.cap_usd, self.prices = model, float(cap_usd), dict(prices)
        self.max_context_tokens, self.max_output_tokens = max_context_tokens, max_output_tokens
        self.worst = worst_call_usd(max_context_tokens, max_output_tokens, prices["input"], prices["output"])
        self.log_path, self.billed, self.trace, self.clock = log_path, billed, trace, clock
        self.reasoning_effort = reasoning_effort             # K10: the only effort a request may carry (None: none)
        self.counted, self.inflight, self.attempts, self.settled, self.refused = 0.0, 0, 0, 0, 0
        self.log_failures = 0                                # second pass, K5: writes to the spend log that failed
        self.stopped: str | None = None
        self.prev: dict | None = None
        self._log({"event": "meter", "model": model, "cap_usd": self.cap_usd, "max_context_tokens": max_context_tokens,
                   "max_output_tokens": max_output_tokens, "prices_usd_per_mtok": self.prices, "worst_call_usd": self.worst,
                   "bound_on_the_bill_usd": self.cap_usd + self.worst, "billed": billed})

    # ---- the two questions ----
    def reserved(self) -> float:
        return self.counted + self.inflight * self.worst

    def exhausted(self) -> bool:
        return self.stopped is not None or self.reserved() >= self.cap_usd

    # ---- before a request is sent ----
    def admit(self, body, url: str = "/chat/completions") -> dict:
        if self.stopped is not None:
            self._refuse(self.stopped, "the run is stopped")
        if not str(url).split("?")[0].rstrip("/").endswith("/chat/completions"):
            self._refuse("model_request_refused", "not the chat-completions route")
        if self.reserved() >= self.cap_usd:
            self._refuse("spend_cap", f"counted {self.counted:.6f} + {self.inflight} in flight x {self.worst:.6f} >= cap {self.cap_usd:.6f}")
        why = check_shape(body, model=self.model, max_output_tokens=self.max_output_tokens, reasoning_effort=self.reasoning_effort)
        if why:
            self._refuse("model_request_refused", why)
        bound, how = prompt_bound(body, self.prev)
        if bound > self.max_context_tokens:
            self._refuse("max_context_tokens", f"the prompt could hold {bound} tokens ({how}); the cap is {self.max_context_tokens}")
        # the attempt is written to the spend log BEFORE it is sent: the tools close a run's books from that log
        # (an attempt that is "sent" and never "settled" counts one worst case), so a call the log could not hold
        # is not made (second pass, K5)
        if not self._log({"event": "sent", "n": self.attempts + 1, "prompt_bound": bound, "bound_from": how,
                          "in_flight": self.inflight + 1, "counted_usd": self.counted}) and self.log_path:
            self._refuse("spend_log_failed", "the spend log could not be written: no call is sent that the log does not hold")
        self.attempts += 1
        self.inflight += 1
        attempt = {"n": self.attempts, "start": self.clock(), "prompt_bound": bound, "bound_from": how, "open": True,
                   "hashes": [_hash(m) for m in body["messages"]], "rest": _rest_hash(body)}
        return attempt

    def _refuse(self, condition: str, detail: str):
        self.refused += 1
        if self.stopped is None:
            self.stopped = condition
        self._log({"event": "refused", "condition": condition, "detail": detail[:300], "counted_usd": self.counted,
                   "in_flight": self.inflight})
        raise Refused(condition, detail)

    # ---- after it ended, however it ended ----
    def settle(self, attempt: dict, usage, outcome: str) -> float:
        if not attempt.get("open"):
            return 0.0
        attempt["open"] = False
        self.inflight -= 1
        self.settled += 1
        cost, basis, tokens = reply_cost(usage, self.prices, self.worst)
        self.counted += cost
        if tokens:                                           # the next request may chain on this prompt count
            self.prev = {"hashes": attempt["hashes"], "rest": attempt["rest"], "prompt_tokens": tokens["prompt_tokens"]}
        self._log({"event": "settled", "n": attempt["n"], "outcome": outcome[:120], "basis": basis, "usd": cost, **tokens,
                   "over_the_reply_cap": bool(tokens and tokens["completion_tokens"] > self.max_output_tokens),
                   "over_the_prompt_bound": bool(tokens and tokens["prompt_tokens"] > attempt["prompt_bound"]),
                   "seconds": round(self.clock() - attempt["start"], 3), "counted_usd": self.counted, "in_flight": self.inflight})
        return cost

    def summary(self) -> dict:
        return {"model": self.model, "cap_usd": self.cap_usd, "worst_call_usd": self.worst, "bound_on_the_bill_usd": self.cap_usd + self.worst,
                "counted_usd": self.counted, "attempts": self.attempts, "settled": self.settled, "in_flight": self.inflight,
                "refused": self.refused, "stopped": self.stopped, "billed": self.billed, "log_failures": self.log_failures,
                "max_context_tokens": self.max_context_tokens, "max_output_tokens": self.max_output_tokens,
                "prices_usd_per_mtok": self.prices}

    def _log(self, record: dict) -> bool:
        """Append one record to the spend log. False when it could not be written: counted in log_failures,
        said on standard error (vf-eval's log), and carried by the next record that is written."""
        if not self.log_path:
            return False
        try:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(dict(record, time_unix=round(self.clock(), 3),
                                        **({"log_failures_before": self.log_failures} if self.log_failures else {}))) + "\n")
            return True
        except (OSError, ValueError) as e:
            self.log_failures += 1
            import sys
            print(f"physim2 spend meter: the spend log could not be written ({type(e).__name__}); failures so far: "
                  f"{self.log_failures}", file=sys.stderr, flush=True)
            return False


def meter_for(spend: SpendConfig, limits=None, *, trace=None, log_path: str | None = None) -> Meter | None:
    """The meter of a model run, or None for a run without a spend table (a scripted run: no model call can
    leave the process then). `limits` is the task's limits table when the taskset has one (fixer A's
    `env.taskset.task.limits`); where both name a cap they must agree."""
    cap, ctx = spend.cap_usd, spend.max_context_tokens
    for name in ("cap_usd", "max_context_tokens"):
        other = getattr(limits, name, None) if limits is not None else None
        mine = cap if name == "cap_usd" else ctx
        if other is not None and mine is not None and float(other) != float(mine):
            raise ValueError(f"the limits table and the spend table disagree on {name}")
        if mine is None and other is not None:
            cap, ctx = (other, ctx) if name == "cap_usd" else (cap, other)
    if cap is None and spend.input_usd_per_mtok is None:
        return None
    if None in (cap, ctx, spend.max_output_tokens, spend.input_usd_per_mtok, spend.output_usd_per_mtok) or not spend.model:
        raise ValueError("an incomplete spend table: a model run needs cap_usd, max_context_tokens, max_output_tokens, the model "
                         "and its listed input and output prices")
    return Meter(model=spend.model, cap_usd=cap, max_context_tokens=int(ctx), max_output_tokens=int(spend.max_output_tokens),
                 prices={"input": spend.input_usd_per_mtok, "output": spend.output_usd_per_mtok, "cache_read": spend.cache_read_usd_per_mtok},
                 log_path=log_path if log_path is not None else os.environ.get(LOG_ENV) or None, billed=spend.billed, trace=trace,
                 reasoning_effort=spend.reasoning_effort)


class UsageScanner:
    """Finds the usage object in a chat-completions event stream as its bytes pass (`data: {...}` lines; the
    last one that carries a usage object wins). Keeps at most one incomplete line."""

    def __init__(self):
        self.usage = None
        self._tail = b""

    def feed(self, chunk: bytes) -> None:
        data = self._tail + chunk
        lines = data.split(b"\n")
        self._tail = lines.pop()[-(1 << 20):]
        for line in lines:
            line = line.strip()
            if not line.startswith(b"data:") or b'"usage"' not in line:
                continue
            try:
                event = json.loads(line[5:])
            except ValueError:
                continue
            if isinstance(event, dict) and isinstance(event.get("usage"), dict):
                self.usage = event["usage"]

    def finish(self):
        if self._tail:
            self.feed(b"\n")
        return self.usage


def usage_of_json(content: bytes):
    try:
        reply = json.loads(content)
    except ValueError:
        return None
    return reply.get("usage") if isinstance(reply, dict) and isinstance(reply.get("usage"), dict) else None


class _Counted:
    """A streamed provider response as verifiers reads it (headers, aiter_bytes, aclose), settled when it is
    closed: with the usage that passed, or as a worst-case call when none did."""

    def __init__(self, response, meter: Meter, attempt: dict):
        self._response, self._meter, self._attempt, self._scan = response, meter, attempt, UsageScanner()
        self.headers, self.status_code = response.headers, response.status_code

    async def aiter_bytes(self, *args, **kwargs):
        async for chunk in self._response.aiter_bytes(*args, **kwargs):
            self._scan.feed(chunk)
            yield chunk

    async def aclose(self):
        try:
            await self._response.aclose()
        finally:
            usage = self._scan.finish()
            self._meter.settle(self._attempt, usage, "stream" if usage is not None else "stream without a usage chunk")

    def __getattr__(self, name):
        return getattr(self._response, name)


def install() -> bool:
    """Wrap verifiers' one route to the provider. Idempotent; returns True when this call did it."""
    global _INSTALLED
    if _INSTALLED:
        return False
    from verifiers.v1.clients.client import SESSION_ID_HEADER
    from verifiers.v1.clients.eval import EvalClient
    from verifiers.v1.errors import model_error

    original = EvalClient._request

    async def _request(self, url, body, headers, *, stream=False):
        meter = METERS.get(headers.get(SESSION_ID_HEADER) or "")
        if meter is None:                                    # a scripted run, an auxiliary route, an unknown rollout
            raise model_error("rollout stopped: no spend meter for this model call", status_code=400)
        try:
            attempt = meter.admit(body, url)
        except Refused as r:
            if meter.trace is not None:
                meter.trace.stop(r.condition)
            raise model_error(f"rollout stopped: {r.condition}", status_code=400) from None
        try:
            response = await original(self, url, body, headers, stream=stream)
        except BaseException as e:                           # an error status, a timeout, a cut connection, a cancellation
            meter.settle(attempt, None, f"no reply: {type(e).__name__} status {getattr(e, 'status_code', None)}")
            raise
        if stream:
            return _Counted(response, meter, attempt)
        usage = usage_of_json(response.content)
        meter.settle(attempt, usage, "reply" if usage is not None else "reply without usage")
        return response

    EvalClient._request = _request
    _INSTALLED = True
    return True
