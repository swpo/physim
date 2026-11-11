"""What verifiers' Docker runtime does not do for a box of the pilot, added in place: the box caps, and the
laboratory's bearer on a box's own proxy.

`install()` (called once per vf-eval process, when the taskset module is imported) changes three names of the
module `verifiers.v1.runtimes.docker` and one of `verifiers.v1.runtimes.container`, and nothing else of verifiers:

  cli                   the function through which that module runs `docker ...`. The wrapper edits ONE command,
                        the `docker run` of a box issued by `DockerRuntime.start`, adding the caps of
                        boxcaps.py; every other command passes unchanged (helper containers, exec, inspect).
  DockerRuntime.start   afterwards the started container is read back with `docker inspect` and compared with
                        the caps (boxcaps.check_host_config). A box without them is not used: start() raises,
                        verifiers records a failed boot and removes the container on its normal path.
  EgressProxy           replaced by a subclass that can put one header on the requests it forwards to ONE
                        upstream port of the host's loopback: the laboratory's bearer (bearer.py). A box never
                        sees that header; requests to every other destination pass byte for byte.

  container._communicate   the one function through which verifiers starts a `docker` client (run, exec,
                        inspect, port, build). verifiers lets the client inherit vf-eval's whole environment; in a
                        model run that includes the model key. The wrapper gives the client an environment
                        without any credential-like name and without the PRIME_* names. (Not covered: the
                        synchronous `docker rm --force <its box>` at teardown, runtimes/docker/__init__.py:553-567,
                        which inherits the environment; a `docker` client puts no variable into a container
                        unless it is told to with --env.)
                        Second pass (code audit K4): verifiers reads a client's whole output into memory
                        (`proc.communicate()`), and every `docker exec` into the agent's box carries output the
                        agent can write to (it is root there and can open /proc/<pid>/fd/1 of any process of
                        an exec, the harness's own main program included: runtimes/base.py:228-235). The
                        replacement is verifiers' function with that one call changed: it keeps at most
                        OUTPUT_MAX bytes of each stream, reads and drops the rest, and then raises SandboxError
                        (the caller sees a failed command). Nothing else differs: the same arguments, the same
                        new session, the same SIGKILL of the client's group when the call is cut.

The box's proxy (second pass, K4): verifiers' proxy holds one connection's bytes in a reader that pauses its
socket when it is full. The subclass below reads the request head itself and hands the rest on through a second
reader, RelayBuffer, which now pauses the copying in the same way (at most 2 x RELAY_LIMIT + 64 KiB waiting per
connection), and it serves at most MAX_CONNECTIONS connections of its box at once (a further one is closed
unread). So what one box can make vf-eval hold in its proxy is bounded.

Round 5 (code audit K9, and the channel sweep of README section "What a box can make the host hold"): verifiers'
interception server (the model's route out of the agent's box) accepts a request body of 1 GiB and reads it whole
once the rollout's secret is found, and that secret is on the command line of the chat program in the box. install()
now also sets, before any server starts, three things of verifiers by name and edits no file of it:

  interception.server.MAX_REQUEST_BODY   INTERCEPTION_BODY_MAX (16 MiB); the server reads it at start()
                        (server.py:424) for aiohttp's client_max_size: a larger body is answered 413 after that many
                        bytes. A body is parsed whole into Python objects (measured: up to 25 times its size), so
                        the bound on one request is about 25 x 16 MiB.
  logging               a filter (RepeatLimit) on the interception server's logger and on Python's last-resort
                        handler: each kind of record (logger and message) passes LOG_REPEAT_MAX times in full, then
                        once a minute with the count dropped; every record is cut at LOG_RECORD_MAX characters. A box
                        can make the server log one line per request (an unauthorized one, server.py:588) and aiohttp
                        one traceback per failed request: without the filter the run's log grows with the box's rate.
  the box's proxy       (below) a request to a callback of the host that carries no bearer (the interception server)
                        waits until fewer than CALLBACK_ACTIVE_MAX requests of the same box go there; nothing of it,
                        head or body, is forwarded before. And the body a box sends to a callback is cut after
                        CALLBACK_UPLOAD_MAX bytes (the connection is closed).
So what one box can make vf-eval hold through that route is about CALLBACK_ACTIVE_MAX x 25 x INTERCEPTION_BODY_MAX
(measured through vf-eval: README).

Why in place and not a subclass of DockerRuntime: the worker gate of the host-safety audit (round 1, change 5;
grading.container_gate) accepts a box only if its class is EXACTLY verifiers' DockerRuntime, and that gate
stays as it is. Why the caps are a wrapper at all: verifiers passes --cpus and --memory natively and has no
option for --read-only, --tmpfs or --pids-limit (runtimes/docker/__init__.py:196-244; "disk" is advisory,
runtimes/container.py:38-41).

The caps apply to every box a vf-eval of this package starts: the agent's box (rollout.py:192), the verifier
box (envs/isolated_verifier/env.py:160) and the item boxes (grading.py through provision_runtime), in model
runs and in the scripted reference runs alike: they all go through DockerRuntime.start.
"""
from __future__ import annotations

import asyncio
import contextlib
import contextvars
import json
import logging
import os
import re
import signal

from . import bearer as BEARER
from . import boxcaps as BOXCAPS

box_caps = BOXCAPS.box_caps                                  # for the statement (ruling E8): the same values the boxes get

_INSTALLED = False
_CAPS: contextvars.ContextVar[dict | None] = contextvars.ContextVar("physim2_box_caps", default=None)
ATTR = "_physim2_box"                                        # on a started runtime: {"caps": ..., "verified": True, ...}
# names a `docker` client of vf-eval does not need: credentials under any usual name, and the Prime account's
NOT_FOR_DOCKER = re.compile(r"(?i)(api[-_]?key|token|secret|passw(or)?d|credential|^PRIME_)")


def docker_client_env(environ=None) -> dict:
    """The environment of a `docker` client that vf-eval starts: vf-eval's own, minus NOT_FOR_DOCKER."""
    environ = os.environ if environ is None else environ
    return {k: v for k, v in environ.items() if not NOT_FOR_DOCKER.search(k)}


# ---- second pass, code audit K4: what a box can make vf-eval hold ----
# The largest output vf-eval reads legitimately from a `docker` client is the collection of submission/: a tar
# archive of at most artifact_mib + 8 MiB (64 + 8 for the ring), read through `head -c` (verifiers
# utils/artifacts.py:180-193). Everything else is small: an item's reply (grading.driver_cmd caps it at
# --max-reply-mib), the validator's report (cut at 1 MiB in the box), inspect, port, the harness's log lines.
OUTPUT_MAX = {"stdout": 96 << 20, "stderr": 4 << 20}
RELAY_LIMIT = 1 << 17                                        # the relay's reader pauses its copy beyond 2 x this
MAX_CONNECTIONS = 64                                         # per box proxy, connections served at once
# ---- round 5, code audit K9 and the channel sweep ----
INTERCEPTION_BODY_MAX = 16 << 20                             # verifiers' interception server: a larger request body is answered 413
CALLBACK_ACTIVE_MAX = 1                                      # per box: requests at once to a host callback without a bearer (they wait)
CALLBACK_UPLOAD_MAX = INTERCEPTION_BODY_MAX + (1 << 20)      # per request to a host callback: body bytes a box can send through
LOG_REPEAT_MAX = 20                                          # records of one kind that pass in full; then one a minute
LOG_REPEAT_EVERY_S = 60.0
LOG_RECORD_MAX = 2000                                        # characters of one record's message
LOG_KINDS_MAX = 256                                          # kinds remembered; beyond, they share one count


async def read_bounded(stream, cap: int) -> tuple[bytes, int]:
    """Read `stream` (an asyncio.StreamReader) to its end. Returns (the first `cap` bytes, the number of bytes
    read and dropped after them). Holds at most `cap` + 64 KiB at any moment."""
    kept, dropped = bytearray(), 0
    while chunk := await stream.read(1 << 16):
        room = cap - len(kept)
        if room > 0:
            kept += chunk[:room]
        dropped += max(0, len(chunk) - max(room, 0))
    return bytes(kept), dropped


class _Gate:
    """The transport the relay reader is given, so that it can say "full": asyncio's StreamReader calls
    pause_reading() when its buffer passes twice its limit and resume_reading() when a read brings it back
    under the limit (asyncio/streams.py, feed_data and _maybe_resume_transport). The pump waits on `open`."""

    def __init__(self):
        self.open = asyncio.Event()
        self.open.set()

    def pause_reading(self):
        self.open.clear()

    def resume_reading(self):
        self.open.set()

    def get_extra_info(self, name, default=None):
        return default


def relay_buffer() -> tuple[asyncio.StreamReader, _Gate]:
    """A StreamReader and the gate through which its feeder sees that it is full (gate.open cleared)."""
    relay, gate = asyncio.StreamReader(limit=RELAY_LIMIT), _Gate()
    relay.set_transport(gate)
    return relay, gate


async def pump(reader, relay, gate, cap: int | None = None, cut=None) -> None:
    """Copy `reader` into `relay` in pieces of 64 KiB, waiting while the relay is full; feed_eof at the end.
    With `cap` (round 5): after `cap` bytes the copy stops, `cut()` is called (it closes the box's connection) and
    the relay ends there: the request reaches its server incomplete and fails."""
    copied = 0
    try:
        while True:
            await gate.open.wait()
            chunk = await reader.read(1 << 16)
            if not chunk:
                break
            if cap is not None and copied + len(chunk) > cap:
                if cut is not None:
                    cut()
                break
            copied += len(chunk)
            relay.feed_data(chunk)
    except Exception:
        pass
    finally:
        relay.feed_eof()


class RepeatLimit(logging.Filter):
    """Round 5: a log record a box can cause once per request passes LOG_REPEAT_MAX times in full; afterwards one
    record of its kind passes every LOG_REPEAT_EVERY_S seconds, saying how many were dropped. Every record that
    passes is cut at LOG_RECORD_MAX characters. A kind is (logger, message template); at most LOG_KINDS_MAX kinds
    are remembered and the rest share one count. Never raises."""

    def __init__(self, clock=None):
        super().__init__()
        import time as _time
        self.clock = clock or _time.monotonic
        self.kinds: dict = {}
        self.dropped_total = 0

    def filter(self, record) -> bool:
        try:
            if getattr(record, "_physim2_limited", False):    # already judged (a logger's filter, then the last resort's)
                return True
            record._physim2_limited = True
            key = (record.name, str(record.msg)[:120])
            if key not in self.kinds and len(self.kinds) >= LOG_KINDS_MAX:
                key = ("*", "*")
            k = self.kinds.setdefault(key, [0, 0, 0.0])       # passed, dropped since the last that passed, time of that one
            now = self.clock()
            if k[0] >= LOG_REPEAT_MAX and now - k[2] < LOG_REPEAT_EVERY_S:
                k[1] += 1
                self.dropped_total += 1
                return False
            text = record.getMessage()
            if k[1]:
                text = f"[{k[1]} more records like this one were dropped] " + text
            if len(text) > LOG_RECORD_MAX:
                text = text[:LOG_RECORD_MAX] + f" [... cut at {LOG_RECORD_MAX} characters]"
            record.msg, record.args = text, ()
            if record.exc_info and k[0] >= LOG_REPEAT_MAX:   # a traceback is printed in full only the first times
                record.exc_info, record.exc_text = None, None
            k[0], k[1], k[2] = k[0] + 1, 0, now
            return True
        except Exception:
            return True


LOG_FILTER = RepeatLimit()
BOX_TRIGGERED_LOGGERS = ("verifiers.v1.interception.server", "aiohttp.server", "aiohttp.web", "aiohttp.access", "aiohttp.internal",
                         "asyncio")


def install_log_limits() -> None:
    """Idempotent: LOG_FILTER on the loggers a box can make write once per request, and on Python's last-resort
    handler (what prints a record of a logger without a handler of its own: aiohttp's, the MCP library's)."""
    for name in BOX_TRIGGERED_LOGGERS:
        lg = logging.getLogger(name)
        if LOG_FILTER not in lg.filters:
            lg.addFilter(LOG_FILTER)
    last = logging.lastResort
    if last is not None and LOG_FILTER not in last.filters:
        last.addFilter(LOG_FILTER)


def resolved_caps(config) -> dict:
    """The caps of the box a runtime config resolves to: its memory and cpu may lower the pin's values, never
    raise them (a config that asks for more, or for nothing, gets the pin's)."""
    mem = BOXCAPS.clamp(getattr(config, "memory", None), BOXCAPS.MEMORY_GB, BOXCAPS.MEMORY_MIN_GB)
    cpu = BOXCAPS.clamp(getattr(config, "cpu", None), BOXCAPS.CPUS, 0.25)
    return BOXCAPS.box_caps(memory_gb=mem, cpus=cpu)


def caps_of(runtime) -> dict | None:
    """What install()'s start wrapper recorded for a started box, or None."""
    return getattr(runtime, ATTR, None)


def set_lab_bearer(runtime, port: int, secret: str) -> None:
    """Tell the proxy of THIS box to authorize its requests to the laboratory at 127.0.0.1:<port>. Raises if the
    box has no proxy of ours (install() was not called before the box started): the laboratory would then
    answer the box with 401, which is the safe failure, and the caller reports it."""
    proxy = getattr(runtime, "_proxy", None)
    if proxy is None or not hasattr(proxy, "set_bearer"):
        raise RuntimeError("the box's proxy cannot carry the laboratory's bearer (physim2_env.runtime.install() did not run "
                           "before the box was started)")
    proxy.set_bearer(port, secret)


def install() -> bool:
    """Idempotent. Returns True when this call made the changes."""
    global _INSTALLED
    if _INSTALLED:
        return False
    import verifiers.v1.runtimes.docker as D
    from verifiers.v1.errors import SandboxError
    from verifiers.v1.runtimes.docker import egress as E

    import verifiers.v1.runtimes.container as C
    from verifiers.v1.utils.aio import run_shielded

    import verifiers.v1.interception.server as IS
    IS.MAX_REQUEST_BODY = INTERCEPTION_BODY_MAX                 # round 5, K9: read by InterceptionServer.start() (server.py:424)
    install_log_limits()

    orig_cli, orig_start = D.cli, D.DockerRuntime.start

    async def _communicate(*argv, input=None, env=None):
        """verifiers' container._communicate (runtimes/container.py:44-63) with two changes: the client's
        environment (docker_client_env), and bounded reading of its output instead of proc.communicate()."""
        proc = await asyncio.create_subprocess_exec(
            *argv, env=docker_client_env() if env is None else env,
            stdin=asyncio.subprocess.PIPE if input is not None else asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, start_new_session=True)

        async def feed():
            if input is None:
                return
            try:
                proc.stdin.write(input)
                await proc.stdin.drain()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                proc.stdin.close()
        try:
            _, (stdout, lost_out), (stderr, lost_err) = await asyncio.gather(
                feed(), read_bounded(proc.stdout, OUTPUT_MAX["stdout"]), read_bounded(proc.stderr, OUTPUT_MAX["stderr"]))
            await proc.wait()
        except BaseException:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(proc.pid, signal.SIGKILL)
            await run_shielded(asyncio.gather(read_bounded(proc.stdout, 0), read_bounded(proc.stderr, 0), proc.wait(),
                                              return_exceptions=True))
            raise
        if lost_out or lost_err:
            raise SandboxError(f"refused: a `{' '.join(str(a) for a in argv[:2])}` client wrote more than the pilot reads "
                               f"({lost_out} bytes of standard output and {lost_err} of standard error past "
                               f"{OUTPUT_MAX['stdout']} and {OUTPUT_MAX['stderr']}); its output was dropped")
        return proc.returncode or 0, stdout, stderr

    async def cli(*argv, input=None, env=None):
        caps = _CAPS.get()
        if caps is not None and argv[:2] == ("docker", "run"):
            try:
                if BOXCAPS.is_box_run(argv):
                    argv = tuple(BOXCAPS.cap_run_argv(argv, caps))
            except ValueError as e:                          # a command the caps were not written for: no box
                raise SandboxError(str(e)) from None
        return await orig_cli(*argv, input=input, env=env)

    async def start(self):
        if self.engine != "docker" or getattr(self, "_host", None) is not None:
            raise SandboxError("refused: the pilot's boxes are local Docker containers (no Podman, no nested engine)")
        caps = resolved_caps(self.config)
        token = _CAPS.set(caps)
        try:
            await orig_start(self)
        finally:
            _CAPS.reset(token)
        shown = await orig_cli("docker", "inspect", "--format", "{{json .HostConfig}}", str(self._container))
        try:
            host_config = json.loads(shown.stdout) if shown.exit_code == 0 else None
        except ValueError:
            host_config = None
        why = ["`docker inspect` gave no HostConfig"] if host_config is None else BOXCAPS.check_host_config(host_config, caps)
        if why:
            raise SandboxError("refused: the box was started without the pilot's caps (" + "; ".join(why[:6]) + ")")
        setattr(self, ATTR, {"caps": caps, "verified": True, "container": str(self._container)})

    class BearerEgressProxy(E.EgressProxy):
        """verifiers' proxy of one box, plus: requests whose callback leads to a port registered with
        set_bearer() are forwarded with `Authorization: <that bearer>` (any Authorization header of the box's
        own is dropped). The head of every request is read here once and handed on to verifiers' handler
        through a second stream; the body follows unchanged."""

        def __init__(self, policy):
            super().__init__(policy)
            self._bearers: dict[tuple[str, int], bytes] = {}
            self._active = 0                                 # connections being served now (MAX_CONNECTIONS)
            self.refused_connections = 0
            self._gates: dict[tuple[str, int], asyncio.Semaphore] = {}   # round 5: per callback without a bearer
            self.callback_stats = {"waited": 0, "most_at_once": 0, "cut_uploads": 0}
            self._callback_active = 0

        def set_bearer(self, port: int, secret: str) -> None:
            if not BEARER.well_formed(secret) or isinstance(port, bool) or not isinstance(port, int) or not 0 < port < 65536:
                raise ValueError("not a bearer or not a port")
            self._bearers[("127.0.0.1", port)] = BEARER.header_value(secret)

        def _callback_of(self, head: bytes):
            """The host callback a request head is addressed to (verifiers' _Callback), or None."""
            path = BEARER.target_path(head)
            if not path.startswith(E._CALLBACK_PREFIX):
                return None
            return self._callbacks.get(path[len(E._CALLBACK_PREFIX):].partition("/")[0].partition("?")[0])

        def _bearer_for(self, head: bytes) -> bytes | None:
            callback = self._callback_of(head)
            return None if callback is None else self._bearers.get((callback.host, callback.port))

        async def _handle(self, reader, writer):
            if self._active >= MAX_CONNECTIONS:              # K4: a box gets at most this many connections served at once
                self.refused_connections += 1
                writer.close()
                return None
            self._active += 1
            try:
                return await self._handle_one(reader, writer)
            finally:
                self._active -= 1

        async def _handle_one(self, reader, writer):
            if self.server is None:
                return await super()._handle(reader, writer)
            try:                                             # round 5: every request's head is read here, bearer or not
                head = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), E._HEADER_TIMEOUT)
                callback = self._callback_of(head)
                value = None if callback is None else self._bearers.get((callback.host, callback.port))
                if value is not None:
                    head = BEARER.inject(head, value)
            except Exception:                                # no head, or one we will not rewrite: forward nothing
                try:
                    writer.write(b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
                    await asyncio.wait_for(writer.drain(), 10)
                except Exception:
                    pass
                writer.close()
                return None
            # round 5 (K9): a request to a callback that has no bearer (verifiers' interception server) waits here,
            # before anything of it is forwarded, until fewer than CALLBACK_ACTIVE_MAX of this box's go there; and
            # what it sends there is cut after CALLBACK_UPLOAD_MAX bytes. (The laboratory, the callback with a
            # bearer, bounds its own requests: bearer.py.)
            sem = None
            if callback is not None and value is None:
                key = (callback.host, callback.port)
                sem = self._gates.get(key)
                if sem is None:
                    sem = self._gates[key] = asyncio.Semaphore(CALLBACK_ACTIVE_MAX)
                if sem.locked():
                    self.callback_stats["waited"] += 1
                await sem.acquire()
                self._callback_active += 1
                self.callback_stats["most_at_once"] = max(self.callback_stats["most_at_once"], self._callback_active)
            try:
                relay, gate = relay_buffer()                 # K4: the copy waits while this holds 2 x RELAY_LIMIT
                relay.feed_data(head)

                def cut():
                    self.callback_stats["cut_uploads"] += 1
                    writer.close()
                task = asyncio.create_task(pump(reader, relay, gate, CALLBACK_UPLOAD_MAX if callback is not None else None, cut))
                try:
                    return await super()._handle(relay, writer)
                finally:
                    task.cancel()
            finally:
                if sem is not None:
                    self._callback_active -= 1
                    sem.release()

    C._communicate = _communicate
    D.cli = cli
    D.DockerRuntime.start = start
    D.EgressProxy = BearerEgressProxy
    _INSTALLED = True
    return True
