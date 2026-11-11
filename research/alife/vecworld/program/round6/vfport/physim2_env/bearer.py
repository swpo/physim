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


def guard(app, secret: str | None):
    """Wrap an ASGI application: an HTTP request without the bearer is answered `401` here; a WebSocket is
    closed; only `lifespan` passes unconditionally (it carries no request)."""
    async def guarded(scope, receive, send):
        kind = scope.get("type")
        if kind == "lifespan":
            return await app(scope, receive, send)
        if kind != "http":
            if kind == "websocket":
                await send({"type": "websocket.close", "code": 1008})
            return None
        if not authorized(scope.get("headers") or [], secret):
            await send({"type": "http.response.start", "status": 401,
                        "headers": [(b"content-length", b"0"), (b"www-authenticate", REALM), (b"connection", b"close")]})
            await send({"type": "http.response.body", "body": b""})
            return None
        return await app(scope, receive, send)
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
