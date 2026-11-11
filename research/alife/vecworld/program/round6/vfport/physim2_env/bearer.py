"""The laboratory's bearer: the pure parts, shared by the laboratory process and by vf-eval.

The laboratory listens on 127.0.0.1 of the trusted worker. Until round 4 it answered anybody who could reach
that port (any process of the machine; on Docker Desktop any container that reaches the host's loopback). Now:

  secret      256 bits, drawn in vf-eval at task set-up (new_secret). It travels to the laboratory process over
              verifiers' state channel, inside `trace.state.access` (never saved in a trace, never on a command
              line, in an environment or in a file), and both sides keep it in memory only.
  laboratory  every HTTP request must carry `Authorization: Bearer <secret>` (guard). Anything else gets
              `401` with an empty body before the MCP application sees a byte. The MCP library's DNS-rebinding
              protection is on again, with the laboratory's own `127.0.0.1:<port>` as the only allowed Host
              (lab_tools.LabTools._serve).
  the box     never holds the secret. A box reaches the laboratory through the proxy that verifiers runs FOR
              that box inside vf-eval (`http://<proxy>/.vf-host/<token>/mcp`); that proxy puts the header on
              the requests it forwards to the laboratory's port, and on no others (inject; runtime.py). The
              address file in the box and the harness's MCP url are what they were.
  bounds      (second pass, code audit K4) a request body is read here, counted, and refused with `413` above
              MAX_BODY; at most MAX_ACTIVE requests are served at once (`503` beyond).

Nothing here kills, deletes or starts a process.
"""
from __future__ import annotations

import hmac
import secrets

REALM = b'Bearer realm="physim2-laboratory"'


def new_secret() -> str:
    """A fresh 256-bit secret as 64 hex characters."""
    return secrets.token_hex(32)


def well_formed(secret) -> bool:
    return isinstance(secret, str) and len(secret) == 64 and all(c in "0123456789abcdef" for c in secret)


def header_value(secret: str) -> bytes:
    return b"Bearer " + secret.encode("ascii")


def authorized(headers, secret: str | None) -> bool:
    """Does an ASGI header list carry exactly one Authorization header with this bearer? Constant-time
    comparison. No secret configured means nobody is authorized (the laboratory fails closed)."""
    if not well_formed(secret):
        return False
    got = [v for k, v in headers if k.lower() == b"authorization"]
    return len(got) == 1 and hmac.compare_digest(bytes(got[0]), header_value(secret))


# Round 4, second pass (code audit K4): what one request may make the laboratory hold. The MCP library reads a
# request body whole (mcp/server/streamable_http.py:537, `await request.body()`) and uvicorn sets no limit, so the
# guard reads the body itself, counting, and hands the application at most MAX_BODY bytes. The largest legitimate
# body is an `advance` or `experiment` block of 4096 ticks x 24 inputs written as JSON (about 2 MB); everything
# else is a few hundred bytes. At most MAX_ACTIVE requests are held at once (a box reaches the laboratory only
# through its proxy, which itself takes at most runtime.MAX_CONNECTIONS connections): the laboratory holds at
# most MAX_ACTIVE x MAX_BODY bytes of request bodies, whatever a box sends.
MAX_BODY = 4 << 20
MAX_ACTIVE = 8


def _plain_reply(status: int, extra=()) -> tuple[dict, dict]:
    return ({"type": "http.response.start", "status": status,
             "headers": [(b"content-length", b"0"), *extra, (b"connection", b"close")]},
            {"type": "http.response.body", "body": b""})


def declared_length(headers):
    """The request's Content-Length as an int, None when there is none, -1 when it is not one plain number (or
    there are several)."""
    got = [bytes(v) for k, v in headers if k.lower() == b"content-length"]
    if not got:
        return None
    if len(got) != 1 or not got[0].strip().isdigit() or len(got[0].strip()) > 18:
        return -1
    return int(got[0].strip())


async def read_body(receive, limit: int):
    """(body, None) with the whole request body if it holds at most `limit` bytes, counted as it arrives;
    (None, "too large") as soon as it holds more (the rest is never read); (None, "disconnect") when the client
    went away. Pure ASGI: nothing but `receive` is called."""
    parts, total = [], 0
    while True:
        msg = await receive()
        kind = msg.get("type")
        if kind == "http.disconnect":
            return None, "disconnect"
        if kind != "http.request":
            continue
        chunk = msg.get("body", b"") or b""
        total += len(chunk)
        if total > limit:
            return None, "too large"
        parts.append(chunk)
        if not msg.get("more_body", False):
            return b"".join(parts), None


def guard(app, secret: str | None, *, max_body: int = MAX_BODY, max_active: int = MAX_ACTIVE):
    """Wrap an ASGI application: an HTTP request without the bearer is answered `401` here; a WebSocket is
    closed; only `lifespan` passes unconditionally (it carries no request). An authorized request whose
    Content-Length, or whose body as counted while it is read, passes `max_body` gets `413` before the
    application sees it; while `max_active` requests are being served, a further one gets `503` unread."""
    active = 0

    async def guarded(scope, receive, send):
        nonlocal active
        kind = scope.get("type")
        if kind == "lifespan":
            return await app(scope, receive, send)
        if kind != "http":
            if kind == "websocket":
                await send({"type": "websocket.close", "code": 1008})
            return None
        headers = scope.get("headers") or []
        if not authorized(headers, secret):
            for m in _plain_reply(401, [(b"www-authenticate", REALM)]):
                await send(m)
            return None
        declared = declared_length(headers)
        if declared == -1 or (declared is not None and declared > max_body):
            for m in _plain_reply(413):
                await send(m)
            return None
        if active >= max_active:
            for m in _plain_reply(503, [(b"retry-after", b"1")]):
                await send(m)
            return None
        active += 1
        try:
            body, why = await read_body(receive, max_body)
            if why == "disconnect":
                return None
            if body is None:
                for m in _plain_reply(413):
                    await send(m)
                return None
            delivered = False

            async def replay():
                nonlocal delivered
                if not delivered:
                    delivered = True
                    return {"type": "http.request", "body": body, "more_body": False}
                return await receive()                       # after the body: the disconnect, as the server reports it
            return await app(scope, replay, send)
        finally:
            active -= 1
    return guarded


def inject(head: bytes, value: bytes) -> bytes:
    """`head` is one HTTP/1.1 request head (request line and header lines, ending in the empty line). Returns it
    with every Authorization header removed and `Authorization: <value>` added. Raises ValueError for a head
    that is not one (the caller then forwards nothing)."""
    if not head.endswith(b"\r\n\r\n"):
        raise ValueError("not a complete request head")
    lines = head[:-4].split(b"\r\n")
    if len(lines[0].split(b" ")) != 3:
        raise ValueError("not a request line")
    if b"\r" in value or b"\n" in value:
        raise ValueError("not a header value")
    kept = [lines[0]]
    for line in lines[1:]:
        name, sep, _ = line.partition(b":")
        if not sep or line[:1] in (b" ", b"\t"):             # no folded or nameless lines in a head we rewrite
            raise ValueError("not a header line")
        if name.strip().lower() != b"authorization":
            kept.append(line)
    kept.append(b"Authorization: " + value)
    return b"\r\n".join(kept) + b"\r\n\r\n"


def target_path(head: bytes) -> str:
    """The request target of a request head, or "" when it cannot be read."""
    try:
        return head.split(b"\r\n", 1)[0].split(b" ")[1].decode("ascii")
    except (IndexError, UnicodeDecodeError):
        return ""
