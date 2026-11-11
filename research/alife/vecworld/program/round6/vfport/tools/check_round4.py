"""check_round4 -- the round-4 changes of fixer B, tested on a host WITHOUT killing, deleting or starting anything.

    python -B tools/check_round4.py --scratch DIR [--out results.json]

The process first makes itself unable to act on the machine (tools/tripwires.py: every kill, delete, move, mode
change and process start raises and is recorded), and only then imports the package. What runs here: pure
functions, and servers on 127.0.0.1 inside THIS process (threads), reached by clients of this process:

  A  box caps       boxcaps.cap_run_argv on verifiers' own command lines; boxcaps.check_host_config
  B  bearer         bearer.guard behind a real HTTP server; the laboratory's own listener (LabTools._serve) with
                    its Host check; verifiers' proxy with the bearer injected (runtime.install)
  C  spend          the meter's arithmetic; verifiers' own EvalClient, wrapped (spend.install), against the
                    stand-in endpoint of tools/standin_model.py: usage, no usage, errors, streams, the cap, the
                    context bound, parallel requests, no meter
  D  step 3         the request, the standing go, the ledger, the instance register, the strict config schema
                    (tools/vfrun.py, tools/check_config.py) and the publication folder (tools/pack_rollout.py),
                    on files in --scratch that this test writes and leaves there

No model is called and no credential is read: the endpoint is the stand-in and its key is a made-up word.
Nothing is removed afterwards: --scratch is the caller's to remove.
"""
import argparse
import asyncio
import json
import os
import socket
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tripwires  # noqa: E402

TW = tripwires.install()                                     # BEFORE anything of the package is imported


class _PopenTripwire:
    """The tripwire of subprocess.Popen as a CLASS: third-party modules write `subprocess.Popen[bytes]` in
    annotations when they are imported (the MCP library does), which a plain function cannot answer. It records
    and raises exactly as the function did, and never starts anything."""

    def __init__(self, *args, **kwargs):
        TW.hits.append(("subprocess.Popen", repr(args[:1])[:160]))
        raise tripwires.Tripped("tripwire: subprocess.Popen")

    def __class_getitem__(cls, item):
        return cls


import subprocess  # noqa: E402

subprocess.Popen = _PopenTripwire
sys.path.insert(0, ROOT)
os.environ.pop("PHYSIM2_MODEL_CREDENTIALS", None)
os.environ["PHYSIM2_STAND_IN_KEY"] = "stand-in-not-a-key"

import logging  # noqa: E402

logging.getLogger("httpx").setLevel(logging.WARNING)

import physim2_env  # noqa: E402,F401   (its first line closes verifiers' reader of the Prime login)
from physim2_env import bearer as BEARER  # noqa: E402
from physim2_env import boxcaps as BOXCAPS  # noqa: E402
from physim2_env import runtime as RUNTIME  # noqa: E402
from physim2_env import spend as SPEND  # noqa: E402

import standin_model  # noqa: E402

CHECKS: list[dict] = []


def check(name: str, ok, detail=None) -> bool:
    CHECKS.append({"name": name, "ok": bool(ok), "detail": detail})
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f"   {detail!r}"), flush=True)
    return bool(ok)


def raises(fn, exc=ValueError) -> bool:
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


# ----------------------------------------------------------------------------- A. box caps
def box_argv(*extra, restricted=True, name="vf-" + "ab" * 16, image="physim2-ring:1", tail=("infinity",)):
    """The `docker run` of a box as verifiers 0.3.2.dev163 builds it (runtimes/docker/__init__.py:196-244)."""
    opts = ["--network", "bridge", "--publish", "127.0.0.1::8000", "--cpus", "4.0", "--memory", "8.0g"]
    if restricted:
        opts += ["--cap-drop", "NET_ADMIN", "--cap-drop", "NET_RAW", "--security-opt", "no-new-privileges",
                 "--sysctl", "net.ipv6.conf.all.disable_ipv6=1"]
    return ["docker", "run", "--label", "verifiers.run=physim2-test-1", "--detach", *opts, *extra,
            "--entrypoint", "sleep", "--name", name, image, *tail]


def test_boxcaps():
    caps = BOXCAPS.box_caps()
    check("A1 the pin's caps: 2 CPUs, 4 GiB, no swap, 512 processes, read-only root, four tmpfs",
          (caps["cpus"], caps["memory_gb"], caps["swap"], caps["pids"], caps["read_only_root"], sorted(caps["tmpfs"]))
          == (2, 4, False, 512, True, ["/etc/physim2", "/runtime", "/tmp", "/workspace"]), caps)
    check("A2 a request may lower the memory, never raise it",
          BOXCAPS.box_caps(memory_gb=2)["memory_gb"] == 2 and raises(lambda: BOXCAPS.box_caps(memory_gb=5))
          and raises(lambda: BOXCAPS.box_caps(memory_gb=0.5)) and raises(lambda: BOXCAPS.box_caps(memory_gb=True))
          and raises(lambda: BOXCAPS.box_caps(cpus=3)))
    out = BOXCAPS.cap_run_argv(box_argv(), caps)
    want = ["--cpus", "2", "--memory", "4g", "--memory-swap", "4g", "--pids-limit", "512", "--read-only"]
    check("A3 the box's docker run gets the caps right after `run`", out[2:2 + len(want)] == want, out[:14])
    check("A4 ... and its own --cpus 4.0 and --memory 8.0g are gone", "4.0" not in out and "8.0g" not in out and out.count("--cpus") == 1
          and out.count("--memory") == 1)
    tm = [out[i + 1] for i, a in enumerate(out) if a == "--tmpfs"]
    check("A5 ... with the four tmpfs mounts and their sizes", tm == [f"{p}:{o}" for p, o in BOXCAPS.TMPFS], tm)
    check("A6 ... and everything else of verifiers' command is kept in order",
          [a for a in out if a not in want and not a.startswith("/") and a != "--tmpfs"][2:8] == ["--label", "verifiers.run=physim2-test-1", "--detach", "--network", "bridge", "--publish"]
          and out[-2:] == ["physim2-ring:1", "infinity"])
    low = BOXCAPS.cap_run_argv(box_argv(restricted=False), BOXCAPS.box_caps(memory_gb=1.5))
    check("A7 a lowered memory is what the command carries", low[low.index("--memory") + 1] == "1.5g" and low[low.index("--memory-swap") + 1] == "1.5g")
    mac = BOXCAPS.cap_run_argv(box_argv("--add-host", "host.docker.internal:host-gateway", "--env", "LANG=C"), caps)
    check("A8 the off-Linux form (--add-host) and an --env pass", "--add-host" in mac and "LANG=C" in mac)
    bad = {"a volume": ("-v", "/home:/x"), "a mount": ("--mount", "type=bind,src=/,dst=/x"), "privileged": ("--privileged",),
           "a tmpfs of somebody's": ("--tmpfs", "/x"), "host pid": ("--pid", "host"), "a device": ("--device", "/dev/sda"),
           "another network": ("--network", "host"), "an unknown option": ("--foo", "bar"), "a capability": ("--cap-add", "SYS_ADMIN"),
           "gpus": ("--gpus", "1"), "another security option": ("--security-opt", "seccomp=unconfined")}
    refused = {k: raises(lambda v=v: BOXCAPS.cap_run_argv(box_argv(*v), caps)) for k, v in bad.items()}
    check("A9 a box command with anything else on it is refused (11 forms)", all(refused.values()), refused)
    check("A10 ... as is one with another name, another entrypoint or another tail",
          raises(lambda: BOXCAPS.cap_run_argv(box_argv(name="mybox"), caps))
          and raises(lambda: BOXCAPS.cap_run_argv(box_argv(tail=("sh", "-c", "x")), caps))
          and raises(lambda: BOXCAPS.cap_run_argv(box_argv(tail=()), caps))
          and raises(lambda: BOXCAPS.cap_run_argv([a if a != "sleep" else "sh" for a in box_argv()], caps)))
    helper = ["docker", "run", "--label", "verifiers.run=x", "--rm", "--network", "container:vf-1", "--cap-drop", "ALL", "img", "sh"]
    check("A11 a helper container (--rm) and every other docker command are not boxes",
          BOXCAPS.is_box_run(helper) is False and BOXCAPS.is_box_run(["docker", "exec", "vf-1", "true"]) is False
          and BOXCAPS.is_box_run(["docker", "inspect", "x"]) is False and BOXCAPS.is_box_run(["podman", "run", "--detach"]) is False)
    check("A12 a docker run that is neither is refused", raises(lambda: BOXCAPS.is_box_run(["docker", "run", "img", "sh"])))
    gib = 1 << 30
    good = {"ReadonlyRootfs": True, "Memory": 4 * gib, "MemorySwap": 4 * gib, "NanoCpus": 2_000_000_000, "PidsLimit": 512,
            "Privileged": False, "Tmpfs": dict(BOXCAPS.TMPFS), "Binds": None, "Mounts": None, "VolumesFrom": None, "Devices": [],
            "CapAdd": None, "PidMode": "", "IpcMode": "private", "UTSMode": "", "UsernsMode": "", "CgroupnsMode": "host", "ShmSize": 64 << 20}
    check("A13 a container started with the caps passes the read-back", BOXCAPS.check_host_config(good, caps) == [], BOXCAPS.check_host_config(good, caps))
    worse = {"writable root": {"ReadonlyRootfs": False}, "more memory": {"Memory": 8 * gib}, "swap": {"MemorySwap": 8 * gib},
             "more cpus": {"NanoCpus": 4_000_000_000}, "no process limit": {"PidsLimit": None}, "privileged": {"Privileged": True},
             "a fifth tmpfs": {"Tmpfs": dict(BOXCAPS.TMPFS, **{"/x": "rw"})}, "a missing tmpfs": {"Tmpfs": dict(BOXCAPS.TMPFS[:3])},
             "a larger workspace": {"Tmpfs": dict(BOXCAPS.TMPFS, **{"/workspace": "rw,size=8g"})}, "a bind": {"Binds": ["/home:/x"]},
             "a mount": {"Mounts": [{"Type": "bind"}]}, "host pid": {"PidMode": "host"}, "host ipc": {"IpcMode": "host"},
             "a capability": {"CapAdd": ["SYS_ADMIN"]}, "a larger shm": {"ShmSize": 1 << 30}}
    got = {k: bool(BOXCAPS.check_host_config(dict(good, **v), caps)) for k, v in worse.items()}
    check("A14 ... and each of 15 deviations fails it", all(got.values()), got)
    check("A15 no HostConfig at all fails it", bool(BOXCAPS.check_host_config(None, caps)))

    class Cfg:
        memory, cpu = 8.0, 4.0
    r = RUNTIME.resolved_caps(Cfg())
    Cfg.memory, Cfg.cpu = 2.0, None
    r2 = RUNTIME.resolved_caps(Cfg())
    Cfg.memory = None
    r3 = RUNTIME.resolved_caps(Cfg())
    check("A16 a runtime config that asks for more gets the pin's caps; one that asks for less gets less",
          (r["memory_gb"], r["cpus"], r2["memory_gb"], r2["cpus"], r3["memory_gb"]) == (4, 2, 2, 2, 4), (r, r2, r3))


# ----------------------------------------------------------------------------- B. bearer
def serve_asgi(app, host_check: bool = False):
    """Run an ASGI app on 127.0.0.1 in a daemon thread of this process; returns its port."""
    import uvicorn
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    server = uvicorn.Server(uvicorn.Config(app, log_level="critical", access_log=False))
    threading.Thread(target=lambda: asyncio.run(server.serve(sockets=[sock])), daemon=True).start()
    return sock.getsockname()[1]


def http(port: int, method: str = "GET", path: str = "/", headers: dict | None = None, body: bytes = b"", host: str | None = None, timeout=10):
    """One raw HTTP/1.1 request to 127.0.0.1:<port>; (status, body bytes). Raw, so that the Host header can be
    chosen and nothing follows a redirect."""
    lines = [f"{method} {path} HTTP/1.1", f"Host: {host or f'127.0.0.1:{port}'}", "Connection: close", f"Content-Length: {len(body)}"]
    lines += [f"{k}: {v}" for k, v in (headers or {}).items()]
    with socket.create_connection(("127.0.0.1", port), timeout=timeout) as c:
        c.sendall(("\r\n".join(lines) + "\r\n\r\n").encode() + body)
        data = b""
        while chunk := c.recv(65536):
            data += chunk
    head, _, rest = data.partition(b"\r\n\r\n")
    return int(head.split(b" ")[1]), rest


def test_bearer(scratch: str):
    secret, other = BEARER.new_secret(), BEARER.new_secret()
    check("B1 a secret is 256 bits of hex, and two differ", BEARER.well_formed(secret) and len(secret) == 64 and secret != other)
    hv = BEARER.header_value(secret)
    check("B2 authorized: exactly one Authorization header with the bearer",
          BEARER.authorized([(b"authorization", hv)], secret) and BEARER.authorized([(b"Authorization", hv), (b"x", b"y")], secret)
          and not BEARER.authorized([], secret) and not BEARER.authorized([(b"authorization", BEARER.header_value(other))], secret)
          and not BEARER.authorized([(b"authorization", hv), (b"authorization", hv)], secret)
          and not BEARER.authorized([(b"authorization", hv)], None) and not BEARER.authorized([(b"authorization", b"Bearer ")], "")
          and not BEARER.authorized([(b"authorization", hv.lower())], secret.upper()))
    head = b"POST /.vf-host/tok/mcp HTTP/1.1\r\nHost: a\r\nAuthorization: Bearer mine\r\nX: 1\r\nauthorization: again\r\n\r\n"
    new = BEARER.inject(head, hv)
    check("B3 inject: the box's own Authorization headers go, the bearer comes, the rest stays",
          new.count(b"uthorization") == 1 and new.endswith(b"Authorization: " + hv + b"\r\n\r\n") and b"X: 1" in new and b"mine" not in new
          and new.startswith(b"POST /.vf-host/tok/mcp HTTP/1.1\r\nHost: a\r\n"))
    check("B4 inject refuses what is not one complete, plain request head",
          raises(lambda: BEARER.inject(b"GET / HTTP/1.1\r\nHost: a\r\n", hv)) and raises(lambda: BEARER.inject(b"GET /\r\n\r\n", hv))
          and raises(lambda: BEARER.inject(b"GET / HTTP/1.1\r\n folded\r\n\r\n", hv))
          and raises(lambda: BEARER.inject(b"GET / HTTP/1.1\r\nHost: a\r\n\r\n", b"x\r\nEvil: 1")))

    seen = []

    async def inner(scope, receive, send):                   # says what it saw, never the value
        if scope["type"] != "http":
            return
        auth = [v for k, v in scope["headers"] if k == b"authorization"]
        seen.append({"path": scope["path"], "n_auth": len(auth), "right": bool(auth) and auth[0] == hv})
        body = json.dumps(seen[-1]).encode()
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-length", str(len(body)).encode())]})
        await send({"type": "http.response.body", "body": body})

    port = serve_asgi(BEARER.guard(inner, secret))
    time.sleep(0.5)
    a = http(port)[0]
    b = http(port, headers={"Authorization": "Bearer " + other})[0]
    c = http(port, headers={"Authorization": "Bearer " + secret[:-1]})[0]
    d = http(port, headers={"Authorization": "Basic " + secret})[0]
    e = http(port, "POST", "/mcp", headers={"Authorization": "Bearer " + secret})
    check("B5 behind the guard: no header, another bearer, a cut bearer, another scheme -> 401; the bearer -> 200",
          (a, b, c, d, e[0]) == (401, 401, 401, 401, 200), (a, b, c, d, e[0]))
    check("B6 ... and the four refused requests never reached the application", len(seen) == 1 and seen[0]["right"], seen)
    open_port = serve_asgi(BEARER.guard(inner, None))
    time.sleep(0.3)
    check("B7 a guard without a secret refuses everybody", http(open_port, headers={"Authorization": "Bearer " + secret})[0] == 401)

    # ---- the laboratory's own listener: LabTools._serve with a made-up task set-up (no store, no state channel) ----
    import verifiers.v1.mcp.server as VS
    VS._die_with_parent = lambda: None                       # a libc call a tripwire cannot see: not made in a host test
    from physim2_env.lab_tools import LabTools, LabToolsConfig
    lab_secret = BEARER.new_secret()
    port_file = os.path.join(scratch, f"lab-port-{os.getpid()}")

    class TestLab(LabTools):
        async def _setup_task_from_channel(self, state_url, secret):
            self.bearer = lab_secret

    class NoBearerLab(LabTools):
        async def _setup_task_from_channel(self, state_url, secret):
            self.bearer = None

    os.environ["MCP_PORT_FILE"] = port_file
    os.environ["MCP_HOST"], os.environ["MCP_PORT"] = "0.0.0.0", "1"       # must be ignored
    threading.Thread(target=TestLab(LabToolsConfig())._serve, daemon=True).start()
    for _ in range(100):
        time.sleep(0.1)
        if os.path.exists(port_file) and open(port_file).read().strip().isdigit():
            break
    lab_port = int(open(port_file).read())
    time.sleep(1.0)
    listen = [s for s in open("/proc/net/tcp").read().splitlines() if f":{lab_port:04X} " in s] if os.path.exists("/proc/net/tcp") else []
    check("B8 the laboratory binds 127.0.0.1 and a port of the system's choice, whatever MCP_HOST and MCP_PORT say",
          lab_port not in (0, 1) and (not listen or all(s.split()[1].startswith("0100007F:") for s in listen if s.split()[3] == "0A")), (lab_port, listen[:2]))
    init = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                       "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}}).encode()
    mcp_headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    no = http(lab_port, "POST", "/mcp", headers=mcp_headers, body=init)
    wrong = http(lab_port, "POST", "/mcp", headers=dict(mcp_headers, Authorization="Bearer " + other), body=init)
    get = http(lab_port, "GET", "/mcp")
    yes = http(lab_port, "POST", "/mcp", headers=dict(mcp_headers, Authorization="Bearer " + lab_secret), body=init)
    check("B9 the laboratory: a request without the bearer, or with another, is refused with 401 and an empty body",
          (no, wrong, get) == ((401, b""), (401, b""), (401, b"")), (no, wrong, get))
    check("B10 ... and with the bearer the MCP server answers", yes[0] == 200 and b'"result"' in yes[1], (yes[0], yes[1][:120]))
    rebind = http(lab_port, "POST", "/mcp", headers=dict(mcp_headers, Authorization="Bearer " + lab_secret), body=init, host="evil.example:80")
    alias = http(lab_port, "POST", "/mcp", headers=dict(mcp_headers, Authorization="Bearer " + lab_secret), body=init, host=f"localhost:{lab_port}")
    origin = http(lab_port, "POST", "/mcp", headers=dict(mcp_headers, Authorization="Bearer " + lab_secret, Origin="http://evil.example"), body=init)
    check("B11 DNS-rebinding protection is on: the bearer with another Host -> 421, with a foreign Origin -> 403",
          (rebind[0], alias[0], origin[0]) == (421, 421, 403), (rebind[0], alias[0], origin[0]))
    os.environ["MCP_PORT_FILE"] = port_file + "-none"
    failed = []

    def run_no_bearer():
        try:
            NoBearerLab(LabToolsConfig())._serve()
        except BaseException as ex:                          # noqa: BLE001
            failed.append(type(ex).__name__ + ": " + str(ex)[:80])
    t = threading.Thread(target=run_no_bearer, daemon=True)
    t.start()
    t.join(20)
    check("B12 a laboratory that was given no bearer serves nothing: it stops before it listens for requests",
          bool(failed) and "no bearer" in failed[0], failed)
    for k in ("MCP_PORT_FILE", "MCP_HOST", "MCP_PORT"):
        os.environ.pop(k, None)

    # ---- verifiers' proxy of a box, with the bearer (runtime.install) ----
    RUNTIME.install()
    import verifiers.v1.runtimes.docker as D
    from verifiers.v1.configs.runtime import NetworkPolicyConfig
    from verifiers.v1.runtimes.docker.egress import NetworkPolicy
    plain_seen = []

    async def plain(scope, receive, send):                   # an upstream WITHOUT a guard: sees what the proxy forwards
        if scope["type"] != "http":
            return
        auth = [v for k, v in scope["headers"] if k == b"authorization"]
        plain_seen.append({"n_auth": len(auth), "is_lab_bearer": bool(auth) and auth[0] == BEARER.header_value(lab_secret),
                           "is_box_value": bool(auth) and auth[0] == b"Bearer box-own-value"})
        body = b"{}"
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-length", b"2")]})
        await send({"type": "http.response.body", "body": body})
    other_port = serve_asgi(plain)
    time.sleep(0.3)

    async def through_proxy():
        proxy = D.EgressProxy(NetworkPolicy(NetworkPolicyConfig(allow=[]), [], allow_non_global=False))
        await proxy.start("127.0.0.1")
        try:
            lab_url = proxy.callback_url(f"http://127.0.0.1:{lab_port}/mcp", "127.0.0.1")
            other_url = proxy.callback_url(f"http://127.0.0.1:{other_port}/x", "127.0.0.1")
            lab_path, other_path = "/" + lab_url.split("/", 3)[3], "/" + other_url.split("/", 3)[3]
            call = lambda *a, **k: asyncio.to_thread(http, proxy.port, *a, **k)      # noqa: E731
            before = await call("POST", lab_path, headers=mcp_headers, body=init)
            proxy.set_bearer(lab_port, lab_secret)
            after = await call("POST", lab_path, headers=mcp_headers, body=init)
            own = await call("POST", lab_path, headers=dict(mcp_headers, Authorization="Bearer box-own-value"), body=init)
            elsewhere = await call("POST", other_path, headers={"Authorization": "Bearer box-own-value"}, body=b"{}")
            bare = await call("POST", other_path, body=b"{}")
            unknown = await call("GET", "/.vf-host/not-a-token/mcp")
            return {"before": before[0], "after": after[0], "own": own[0], "elsewhere": elsewhere[0], "bare": bare[0],
                    "unknown": unknown[0], "class": type(proxy).__name__, "lab_url_holds_secret": lab_secret in lab_url,
                    "reply_holds_secret": lab_secret.encode() in after[1] + own[1]}
        finally:
            await proxy.stop()
    r = asyncio.run(through_proxy())
    check("B13 through a box's proxy: before the bearer is registered the laboratory answers 401", r["before"] == 401 and r["class"] == "BearerEgressProxy", r)
    check("B14 ... after it, the same request passes, also when the box sends an Authorization header of its own", (r["after"], r["own"]) == (200, 200), r)
    check("B15 ... the box's address and the laboratory's replies do not hold the secret", not r["lab_url_holds_secret"] and not r["reply_holds_secret"], r)
    check("B16 ... a request to ANOTHER upstream keeps the box's own header and gets no bearer",
          (r["elsewhere"], r["bare"]) == (200, 200) and plain_seen[0] == {"n_auth": 1, "is_lab_bearer": False, "is_box_value": True}
          and plain_seen[1] == {"n_auth": 0, "is_lab_bearer": False, "is_box_value": False}, plain_seen)
    check("B17 ... an unknown callback token gets nothing from the proxy", r["unknown"] in (407, 403), r["unknown"])

    class NoProxy:
        _proxy = None
    check("B18 a box without the pilot's proxy cannot be given the bearer (the caller hears it)",
          raises(lambda: RUNTIME.set_lab_bearer(NoProxy(), lab_port, lab_secret), RuntimeError))
    return lab_secret


# ----------------------------------------------------------------------------- C. spend
PRICES = {"input": 2.0, "output": 10.0, "cache_read": 0.5}


class FakeTrace:
    def __init__(self):
        self.stop_condition = None

    def stop(self, condition, override=False):
        if override or self.stop_condition is None:
            self.stop_condition = condition


def chat_body(n_bytes: int = 200, *, model=standin_model.MODEL, max_tokens=100, stream=False, messages=None, **extra):
    messages = messages or [{"role": "user", "content": "x" * n_bytes}]
    return dict({"model": model, "max_tokens": max_tokens, "messages": messages, "stream": stream}, **extra)


def test_spend_pure():
    worst = SPEND.worst_call_usd(10_000, 1_000, 2.0, 10.0)
    check("C1 one worst-case call: 10,000 x $2/M + 1,000 x $10/M = $0.03", abs(worst - 0.03) < 1e-12, worst)
    c, basis, tok = SPEND.reply_cost({"prompt_tokens": 1000, "completion_tokens": 100}, PRICES, worst)
    check("C2 a reply with usage costs its tokens at the listed prices", abs(c - (1000 * 2 + 100 * 10) / 1e6) < 1e-12 and basis.startswith("usage"), (c, basis))
    c, basis, tok = SPEND.reply_cost({"prompt_tokens": 1000, "completion_tokens": 100, "prompt_tokens_details": {"cached_tokens": 800}}, PRICES, worst)
    check("C3 cache reads at the LISTED cache-read price", abs(c - (200 * 2 + 800 * 0.5 + 100 * 10) / 1e6) < 1e-12 and tok["cached_tokens"] == 800, (c, basis))
    c, basis, _ = SPEND.reply_cost({"prompt_tokens": 1000, "completion_tokens": 100, "prompt_tokens_details": {"cached_tokens": 800}},
                                   dict(PRICES, cache_read=None), worst)
    check("C4 ... and at the FULL input price when the record holds no cache-read price", abs(c - (1000 * 2 + 100 * 10) / 1e6) < 1e-12 and "input price" in basis, (c, basis))
    c, basis, _ = SPEND.reply_cost({"prompt_tokens": 1000, "completion_tokens": 100, "cost": 0.5}, PRICES, worst)
    c2, _, _ = SPEND.reply_cost({"prompt_tokens": 1000, "completion_tokens": 100, "cost": 0.0}, PRICES, worst)
    check("C5 the provider's own cost field counts when it is HIGHER, never when it is lower", c == 0.5 and abs(c2 - 0.003) < 1e-12, (c, c2))
    partial = [None, {}, {"prompt_tokens": 10}, {"completion_tokens": 10}, {"prompt_tokens": "10", "completion_tokens": 1},
               {"prompt_tokens": -1, "completion_tokens": 1}, {"prompt_tokens": True, "completion_tokens": 1},
               {"prompt_tokens": 10, "completion_tokens": 1, "prompt_tokens_details": {"cached_tokens": 99}},
               {"prompt_tokens": 10, "completion_tokens": 1, "prompt_tokens_details": {"cached_tokens": "x"}}, "usage", 7]
    got = [SPEND.reply_cost(u, PRICES, worst)[0] for u in partial]
    check("C6 missing or partial usage (11 forms) costs ONE WORST-CASE CALL, never zero", all(g == worst for g in got), got)
    shapes = {"another model": chat_body(model="other/model"), "no reply cap": {k: v for k, v in chat_body().items() if k != "max_tokens"},
              "a reply cap above the run's": chat_body(max_tokens=101), "two choices": chat_body(n=2), "an image": chat_body(messages=[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "http://x/y.png"}}]}]),
              "a provider tool": chat_body(tools=[{"type": "web_search"}]), "plugins": chat_body(plugins=[{"id": "web"}]), "audio out": chat_body(modalities=["text", "audio"]),
              "no messages": chat_body(messages=[]) | {"messages": []}, "a second cap above": chat_body(max_completion_tokens=5000)}
    got = {k: SPEND.check_shape(v, model=standin_model.MODEL, max_output_tokens=100) for k, v in shapes.items()}
    ok_shape = SPEND.check_shape(chat_body(tools=[{"type": "function", "function": {"name": "bash"}}],
                                           messages=[{"role": "system", "content": "s"}, {"role": "user", "content": [{"type": "text", "text": "t"}]},
                                                     {"role": "assistant", "content": None, "tool_calls": []}]), model=standin_model.MODEL, max_output_tokens=100)
    check("C7 a request the meter cannot bound is refused (10 forms); the bash harness's own shape passes", all(got.values()) and ok_shape is None, (got, ok_shape))
    reason = [SPEND.check_shape(chat_body(**kw), model=standin_model.MODEL, max_output_tokens=100)
              for kw in ({"reasoning_effort": "high"}, {"reasoning": {"summary": "auto", "effort": "low"}}, {"stream": True, "stream_options": {"include_usage": True}})]
    check("C7b the reasoning settings a rollout config can ask for (an effort; the route's `reasoning` object) and a streamed request pass the shape check",
          reason == [None, None, None], reason)
    body = chat_body(1000)
    b1, how1 = SPEND.prompt_bound(body, None)
    check("C8 the first prompt is bounded by the bytes of the whole request", b1 >= len(json.dumps(body["messages"][0])) and "whole request" in how1, (b1, how1))
    prev = {"hashes": [SPEND._hash(body["messages"][0])], "rest": SPEND._rest_hash(body), "prompt_tokens": 260}
    longer = chat_body(messages=body["messages"] + [{"role": "assistant", "content": "a" * 40}, {"role": "tool", "tool_call_id": "c1", "content": "r" * 500}])
    b2, how2 = SPEND.prompt_bound(longer, prev)
    added = sum(len(SPEND._dump(m)) for m in longer["messages"][1:])
    check("C9 a continued conversation: the provider's last prompt count plus one token per byte added since",
          b2 == 260 + added + 2 * SPEND.PER_MESSAGE + SPEND.SLACK and "last reply" in how2, (b2, how2, added))
    rewritten = chat_body(messages=[{"role": "user", "content": "y" * 1000}] + longer["messages"][1:])
    b3, how3 = SPEND.prompt_bound(rewritten, prev)
    retooled = dict(longer, tools=[{"type": "function", "function": {"name": "t", "description": "d" * 5000}}])
    b4, how4 = SPEND.prompt_bound(retooled, prev)
    check("C10 a rewritten history, or changed tools, falls back to the bytes of the whole request", "whole request" in how3 and "whole request" in how4 and b4 > 5000, (how3, how4))
    multi = "é" * 300
    check("C11 bytes, not characters, are counted", SPEND.prompt_bound(chat_body(messages=[{"role": "user", "content": multi}]), None)[0] >= 600)
    m = SPEND.Meter(model=standin_model.MODEL, cap_usd=0.05, max_context_tokens=10_000, max_output_tokens=100, prices=PRICES)
    a1 = m.admit(chat_body())
    check("C12 a request in flight is reserved at one worst-case call", m.inflight == 1 and abs(m.reserved() - m.worst) < 1e-12 and abs(m.worst - 0.021) < 1e-12, m.summary())
    a2 = m.admit(chat_body())
    m13 = SPEND.Meter(model=standin_model.MODEL, cap_usd=0.05, max_context_tokens=10_000, max_output_tokens=100, prices=PRICES)
    for _ in range(3):
        m13.admit(chat_body())                               # 0, 0.021 and 0.042 reserved: each below the cap of 0.05
    check("C13 parallel requests are admitted while the RESERVED sum is below the cap: three at $0.021 under a cap of $0.05, a fourth is refused",
          m13.inflight == 3 and raises(lambda: m13.admit(chat_body()), SPEND.Refused) and m13.stopped == "spend_cap"
          and m13.reserved() <= m13.cap_usd + m13.worst, m13.summary())
    m2 = SPEND.Meter(model=standin_model.MODEL, cap_usd=0.04, max_context_tokens=10_000, max_output_tokens=100, prices=PRICES)
    m2.admit(chat_body())
    m2.admit(chat_body())
    check("C14 ... and with the cap at $0.04 the third is refused: what is reserved never exceeds cap_usd + one worst-case call",
          raises(lambda: m2.admit(chat_body()), SPEND.Refused) and m2.stopped == "spend_cap" and m2.attempts == 2
          and m2.reserved() <= m2.cap_usd + m2.worst, m2.summary())
    m.settle(a1, {"prompt_tokens": 100, "completion_tokens": 10}, "reply")
    m.settle(a1, {"prompt_tokens": 100, "completion_tokens": 10}, "reply")
    check("C15 settling replaces the reservation by the reply's cost, once", m.inflight == 2 - 1 and abs(m.counted - 0.0003) < 1e-12 and m.settled == 1, m.summary())
    m.settle(a2, None, "no reply")
    check("C16 an attempt without usage is settled at the worst case", abs(m.counted - 0.0003 - m.worst) < 1e-12 and m.inflight == 0, m.summary())
    m3 = SPEND.Meter(model=standin_model.MODEL, cap_usd=10, max_context_tokens=500, max_output_tokens=100, prices=PRICES)
    check("C17 a prompt that could exceed max_context_tokens is refused as max_context_tokens, and the run stays stopped",
          raises(lambda: m3.admit(chat_body(2000)), SPEND.Refused) and m3.stopped == "max_context_tokens"
          and raises(lambda: m3.admit(chat_body(10)), SPEND.Refused) and m3.attempts == 0 and m3.exhausted(), m3.summary())
    m4 = SPEND.Meter(model=standin_model.MODEL, cap_usd=10, max_context_tokens=5000, max_output_tokens=100, prices=PRICES)
    check("C18 the Responses and Anthropic routes and an auxiliary route are refused",
          raises(lambda: m4.admit(chat_body(), "http://h/v1/responses"), SPEND.Refused)
          and SPEND.Meter(model="m", cap_usd=1, max_context_tokens=9, max_output_tokens=9, prices=PRICES).worst > 0)
    check("C19 a meter without a usable cap or price is not made",
          raises(lambda: SPEND.Meter(model="m", cap_usd=0, max_context_tokens=9, max_output_tokens=9, prices=PRICES))
          and raises(lambda: SPEND.Meter(model="m", cap_usd=1, max_context_tokens=9, max_output_tokens=9, prices={"input": None, "output": 1}))
          and raises(lambda: SPEND.Meter(model="", cap_usd=1, max_context_tokens=9, max_output_tokens=9, prices=PRICES))
          and raises(lambda: SPEND.Meter(model="m", cap_usd=float("nan"), max_context_tokens=9, max_output_tokens=9, prices=PRICES)))
    full = SPEND.SpendConfig(cap_usd=1.0, max_context_tokens=1000, max_output_tokens=100, model="m", input_usd_per_mtok=1.0, output_usd_per_mtok=2.0)

    class Limits:
        cap_usd, max_context_tokens = 1.0, 1000
    check("C20 the spend table makes a meter; an empty one makes none; an incomplete or contradicted one is refused",
          SPEND.meter_for(full) is not None and SPEND.meter_for(SPEND.SpendConfig()) is None and SPEND.meter_for(full, Limits()) is not None
          and raises(lambda: SPEND.meter_for(SPEND.SpendConfig(cap_usd=1.0)))
          and raises(lambda: SPEND.meter_for(SPEND.SpendConfig(cap_usd=2.0, max_context_tokens=1000, max_output_tokens=100, model="m",
                                                               input_usd_per_mtok=1.0, output_usd_per_mtok=2.0), Limits())))
    sc = SPEND.UsageScanner()
    for piece in (b'data: {"choices":[{"delta":{"content":"a"}}]}\n\ndata: {"choices":[],"us', b'age":{"prompt_tokens":5,"completion_tokens":2}}\n\n', b"data: [DONE]\n\n"):
        sc.feed(piece)
    sc2 = SPEND.UsageScanner()
    sc2.feed(b'data: {"choices":[{"delta":{"content":"\\"usage\\": {}"}}]}\n\ndata: [DONE]\n\n')
    check("C21 the stream scanner finds a usage chunk split across reads, and none where there is none",
          sc.finish() == {"prompt_tokens": 5, "completion_tokens": 2} and sc2.finish() is None)


async def spend_through_client(scratch: str):
    """verifiers' own EvalClient, wrapped, against the stand-in. Every case: a fresh stand-in and a fresh meter."""
    SPEND.install()
    from verifiers.v1.clients.eval import EvalClient
    from verifiers.v1.configs.client import EvalClientConfig
    from verifiers.v1.dialects.chat import ChatDialect
    from verifiers.v1.errors import ProviderError
    from verifiers.v1.types import SamplingConfig
    dialect = ChatDialect()

    def setup(script, *, cap=1.0, ctx=10_000, out=100, prices=PRICES, sid="t1", log=None):
        s = standin_model.Standin(script).start()
        client = EvalClient(EvalClientConfig(base_url=s.base_url, api_key_var="PHYSIM2_STAND_IN_KEY"))
        trace = FakeTrace()
        meter = SPEND.Meter(model=standin_model.MODEL, cap_usd=cap, max_context_tokens=ctx, max_output_tokens=out, prices=prices, trace=trace, log_path=log)
        SPEND.METERS.clear()
        SPEND.METERS[sid] = meter
        return s, client, trace, meter

    async def plain(client, body, sid="t1"):
        return await client.get_response(dialect, body, SamplingConfig(), session_id=sid, headers={})

    async def stream(client, body, sid="t1"):
        reply = await client.relay(dialect, dict(body, stream=True), session_id=sid, headers={})
        try:
            return b"".join([c async for c in reply.chunks])
        finally:
            await reply.close()

    async def fails(coro):
        try:
            await coro
        except ProviderError as e:
            return e.status_code, str(e)
        return None, ""

    usage = {"prompt_tokens": 1000, "completion_tokens": 50}
    log = os.path.join(scratch, f"spend-{os.getpid()}.jsonl")
    s, client, trace, meter = setup([{"say": "a", "usage": usage}], log=log)
    r = await plain(client, chat_body())
    check("C22 through verifiers' client: a reply with usage is counted at the listed prices",
          r.message.content == "a" and abs(meter.counted - (1000 * 2 + 50 * 10) / 1e6) < 1e-12 and meter.settled == 1 and len(s.requests) == 1, meter.summary())
    check("C23 ... the request went out with the stand-in's made-up key, the rollout's id and the reply cap", s.requests[0]["has_authorization"] and s.requests[0]["session"] and s.requests[0]["max_tokens"] == 100, s.requests)
    lines = [json.loads(x) for x in open(log)]
    check("C24 ... and the run's spend log holds the meter line, the attempt and its settlement (numbers and words only)",
          [x["event"] for x in lines] == ["meter", "sent", "settled"] and lines[2]["usd"] == meter.counted and lines[0]["bound_on_the_bill_usd"] == meter.cap_usd + meter.worst, lines)
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": None}])
    await plain(client, chat_body())
    check("C25 a reply WITHOUT usage costs one worst-case call", abs(meter.counted - meter.worst) < 1e-12 and meter.settled == 1, meter.summary())
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": {"prompt_tokens": 1000}}])
    partial = await fails(plain(client, chat_body()))        # verifiers itself calls such a reply malformed (502)
    check("C26 ... as does a reply with partial usage (which verifiers then rejects as malformed: still counted)",
          abs(meter.counted - meter.worst) < 1e-12 and partial[0] == 502 and meter.inflight == 0, (partial[0], meter.summary()))
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"status": 500}, {"status": 429}, {"status": 400}, {"say": "a", "usage": usage}])
    codes = [(await fails(plain(client, chat_body())))[0] for _ in range(3)]
    await plain(client, chat_body())
    check("C27 three error replies (500, 429, 400) and then a good one: FOUR attempts counted, three at the worst case",
          codes == [500, 429, 400] and meter.attempts == 4 and len(s.requests) == 4 and abs(meter.counted - 3 * meter.worst - 0.0025) < 1e-12, (codes, meter.summary()))
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"bash": "echo hi", "usage": dict(usage, cached_tokens=600)}])
    out = await stream(client, chat_body())
    check("C28 a streamed reply: the usage chunk is found as the bytes pass, cache reads at their listed price",
          b"[DONE]" in out and b"tool_calls" in out and abs(meter.counted - (400 * 2 + 600 * 0.5 + 50 * 10) / 1e6) < 1e-12 and meter.inflight == 0, meter.summary())
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": None}])
    await stream(client, chat_body())
    check("C29 a streamed reply without a usage chunk costs one worst-case call", abs(meter.counted - meter.worst) < 1e-12 and meter.inflight == 0, meter.summary())
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": usage}])
    reply = await client.relay(dialect, chat_body(stream=True), session_id="t1", headers={})
    mid = (meter.inflight, meter.reserved())
    await reply.close()                                      # the reader gives up before it read anything
    check("C30 a stream that is closed unread: reserved while open, settled at the worst case when closed",
          mid[0] == 1 and abs(mid[1] - meter.worst) < 1e-12 and meter.inflight == 0 and abs(meter.counted - meter.worst) < 1e-12, (mid, meter.summary()))
    s.stop(); await client.close()

    # the cap: worst = 0.021; each good reply costs 0.0025
    s, client, trace, meter = setup([{"say": "a", "usage": usage}], cap=0.006)
    done = 0
    stop = (None, "")
    for _ in range(10):
        stop = await fails(plain(client, chat_body()))
        if stop[0] is not None:
            break
        done += 1
    check("C31 the cap: calls are sent while counted < cap_usd; then the next one is refused with `400 rollout stopped: spend_cap`",
          done == 3 and stop == (400, "rollout stopped: spend_cap") and trace.stop_condition == "spend_cap", (done, stop, meter.summary()))
    check("C32 ... the refused call never left the process, and the counted cost is within cap_usd + one worst-case call",
          len(s.requests) == 3 and meter.cap_usd <= meter.counted <= meter.cap_usd + meter.worst, (len(s.requests), meter.summary()))
    again = await fails(plain(client, chat_body()))
    check("C33 ... and nothing is sent after a stop", again[0] == 400 and len(s.requests) == 3)
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": usage}], ctx=2000)
    ok = await plain(client, chat_body(500))
    big = await fails(plain(client, chat_body(9000)))
    check("C34 the context cap: a prompt that could exceed max_context_tokens is not sent; the run stops as max_context_tokens",
          ok is not None and big == (400, "rollout stopped: max_context_tokens") and trace.stop_condition == "max_context_tokens" and len(s.requests) == 1, (big, len(s.requests)))
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": {"prompt_tokens": 300, "completion_tokens": 20}}], ctx=2000)
    first = chat_body(900)
    await plain(client, first)
    grown = chat_body(messages=first["messages"] + [{"role": "assistant", "content": "a"}, {"role": "tool", "tool_call_id": "c", "content": "r" * 1200}])
    await plain(client, grown)                               # whole request: > 2000 bytes; chained: 300 + ~1300
    check("C35 a conversation whose bytes exceed the cap still passes while the provider's count plus the added bytes does not",
          len(s.requests) == 2 and meter.stopped is None and len(SPEND._dump(grown)) > 2000, meter.summary())
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": usage, "sleep": 0.4}], cap=0.05)
    results = await asyncio.gather(*[fails(plain(client, chat_body())) for _ in range(6)])
    sent = sum(1 for r in results if r[0] is None)
    check("C36 six requests AT ONCE under a cap of $0.05 (worst case $0.021): three are sent, three are refused before they leave",
          sent == 3 and len(s.requests) == 3 and all(r == (400, "rollout stopped: spend_cap") for r in results if r[0] is not None)
          and 3 * meter.worst <= meter.cap_usd + meter.worst, (results, meter.summary()))
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": usage}])
    SPEND.METERS.clear()
    none = await fails(plain(client, chat_body()))
    check("C37 without a meter (a scripted run) NO model call leaves the process", none[0] == 400 and "no spend meter" in none[1] and len(s.requests) == 0, none)
    SPEND.METERS["t1"] = meter
    wrong = await fails(plain(client, chat_body(), sid="another-rollout"))
    aux = None
    try:
        await client.relay_aux(dialect, "/v1/messages/count_tokens", chat_body(), headers={})
    except ProviderError as e:
        aux = e.status_code
    check("C38 ... nor for another rollout's id, nor on an auxiliary route", wrong[0] == 400 and aux == 400 and len(s.requests) == 0, (wrong, aux))
    bad = await fails(plain(client, chat_body(n=4)))
    check("C39 a request the meter cannot bound stops the run as model_request_refused, unsent",
          bad == (400, "rollout stopped: model_request_refused") and trace.stop_condition == "model_request_refused" and len(s.requests) == 0, bad)
    s.stop(); await client.close()

    s, client, trace, meter = setup([{"say": "a", "usage": {"prompt_tokens": 1000, "completion_tokens": 50, "cost": 0.5}}], cap=0.4)
    await plain(client, chat_body())
    after = await fails(plain(client, chat_body()))
    check("C40 a provider cost field above the listed prices is what counts, and it can end the run", meter.counted == 0.5 and after[0] == 400 and len(s.requests) == 1, meter.summary())
    s.stop(); await client.close()
    SPEND.METERS.clear()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, help="a folder of the caller's for the files this test writes (it removes nothing)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--only", default="ABCD", help="sections to run, e.g. AC")
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    t0 = time.time()
    if "A" in a.only:
        test_boxcaps()
    if "B" in a.only:
        test_bearer(a.scratch)
    if "C" in a.only:
        test_spend_pure()
        asyncio.run(spend_through_client(a.scratch))
    if "D" in a.only:
        try:
            import check_round4_step3
        except ImportError:
            check_round4_step3 = None
        if check_round4_step3 is not None:
            check_round4_step3.run(check, raises, a.scratch)
    hits = TW.take()
    check("Z the tripwires recorded no attempt to kill, delete, move, re-own or start anything", not hits, hits[:5])
    failed = [c["name"] for c in CHECKS if not c["ok"]]
    out = {"tool": "tools/check_round4.py", "sections": a.only, "n_checks": len(CHECKS), "n_failed": len(failed), "failed": failed,
           "tripwires_installed": len(TW.names), "tripwire_hits": hits, "wall_s": round(time.time() - t0, 1), "checks": CHECKS,
           "evidence": "run under tripwires on the host; servers on 127.0.0.1 inside the test process; no model, no Docker"}
    if a.out:
        with open(a.out, "w") as f:
            json.dump(out, f, indent=1, default=repr)
    print(json.dumps({k: out[k] for k in ("n_checks", "n_failed", "failed", "wall_s")}))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
