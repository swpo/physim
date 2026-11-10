"""tripwires -- make THIS Python process unable to kill, delete, move, re-own or start anything, and record
every attempt.

    import tripwires                 # first, before the code under test is imported
    tw = tripwires.install()         # every primitive below now records its name and raises Tripped
    ...                              # import and call the code under test
    tw.hits                          # [(name, short repr of the arguments)]: what was attempted
    tw.restore()                     # put the real functions back (needed to remove the test's own temp files)

Why: code of this folder once ran its cleanup on a development host (README section 8). A test that runs on a
host therefore replaces, before it imports anything of the package, every primitive through which such code
could act on the machine. A tripwire never forwards the call. What is NOT covered, and must therefore never be
reached by a host test: writing or truncating a file through open(), ctypes calls into libc, and anything a
compiled extension does on its own.
"""
import os
import pathlib
import shutil
import subprocess
import tempfile


class Tripped(AssertionError):
    """A destructive primitive was reached. Deliberately not an OSError or a RuntimeError: code under test that
    catches those (`except OSError: pass`) cannot swallow it by accident."""


OS_NAMES = [
    # signals and identity
    "kill", "killpg", "setuid", "setgid", "seteuid", "setegid", "setreuid", "setregid", "setresuid", "setresgid", "setgroups",
    "initgroups",
    # removing, moving, truncating
    "remove", "unlink", "rmdir", "removedirs", "rename", "renames", "replace", "truncate", "ftruncate",
    # modes and owners
    "chmod", "fchmod", "lchmod", "chown", "fchown", "lchown", "chroot",
    # new processes
    "system", "popen", "fork", "forkpty", "posix_spawn", "posix_spawnp",
    "execl", "execle", "execlp", "execlpe", "execv", "execve", "execvp", "execvpe",
    "spawnl", "spawnle", "spawnlp", "spawnlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe",
]
SHUTIL_NAMES = ["rmtree", "move", "chown"]
SUBPROCESS_NAMES = ["run", "Popen", "call", "check_call", "check_output", "getoutput", "getstatusoutput"]
PATH_NAMES = ["unlink", "rmdir", "rename", "replace", "chmod", "lchmod"]


class Tripwires:
    def __init__(self):
        self.hits: list[tuple[str, str]] = []
        self.saved: dict = {}
        self.names: list[str] = []

    def _wire(self, owner, attr, label):
        if not hasattr(owner, attr):
            return
        self.saved[(owner, attr)] = getattr(owner, attr)
        hits = self.hits

        def trip(*args, **kw):
            hits.append((label, repr(args[:3])[:160]))
            raise Tripped("tripwire: " + label)
        trip.__name__ = f"tripwire_{attr}"
        setattr(owner, attr, trip)
        self.names.append(label)

    def install(self):
        tempfile.gettempdir()                                # the standard library probes the temp directory once (create, unlink): now
        for nm in OS_NAMES:
            self._wire(os, nm, f"os.{nm}")
        for nm in SHUTIL_NAMES:
            self._wire(shutil, nm, f"shutil.{nm}")
        for nm in SUBPROCESS_NAMES:
            self._wire(subprocess, nm, f"subprocess.{nm}")
        for nm in PATH_NAMES:
            self._wire(pathlib.Path, nm, f"pathlib.Path.{nm}")
        return self

    def real(self, owner, attr):
        """The real function behind a tripwire, for the TEST's own bookkeeping (never handed to code under test)."""
        return self.saved[(owner, attr)]

    def restore(self):
        for (owner, attr), fn in self.saved.items():
            setattr(owner, attr, fn)
        self.saved.clear()

    def take(self):
        """The hits since the last call, and forget them."""
        got = list(self.hits)
        self.hits.clear()
        return got


def install() -> Tripwires:
    return Tripwires().install()
