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
import contextvars
import json
import os
import re

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

    orig_cli, orig_start, orig_communicate = D.cli, D.DockerRuntime.start, C._communicate

    async def _communicate(*argv, input=None, env=None):
        return await orig_communicate(*argv, input=input, env=docker_client_env() if env is None else env)

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

        def set_bearer(self, port: int, secret: str) -> None:
            if not BEARER.well_formed(secret) or isinstance(port, bool) or not isinstance(port, int) or not 0 < port < 65536:
                raise ValueError("not a bearer or not a port")
            self._bearers[("127.0.0.1", port)] = BEARER.header_value(secret)

        def _bearer_for(self, head: bytes) -> bytes | None:
            path = BEARER.target_path(head)
            if not path.startswith(E._CALLBACK_PREFIX):
                return None
            callback = self._callbacks.get(path[len(E._CALLBACK_PREFIX):].partition("/")[0].partition("?")[0])
            return None if callback is None else self._bearers.get((callback.host, callback.port))

        async def _handle(self, reader, writer):
            if not self._bearers or self.server is None:
                return await super()._handle(reader, writer)
            try:
                head = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), E._HEADER_TIMEOUT)
                value = self._bearer_for(head)
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
            relay = asyncio.StreamReader(limit=1 << 20)
            relay.feed_data(head)

            async def pump():
                try:
                    while chunk := await reader.read(1 << 16):
                        relay.feed_data(chunk)
                except Exception:
                    pass
                finally:
                    relay.feed_eof()
            task = asyncio.create_task(pump())
            try:
                return await super()._handle(relay, writer)
            finally:
                task.cancel()

    C._communicate = _communicate
    D.cli = cli
    D.DockerRuntime.start = start
    D.EgressProxy = BearerEgressProxy
    _INSTALLED = True
    return True
