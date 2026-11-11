"""harness_setup_command -- print, from the pinned verifiers itself, exactly what its stock `bash` harness runs
in a box at set-up, so that the command can be replayed in a throwaway container without any network.

    .venv/bin/python -B tests/harness_setup_command.py OUT_DIR

Nothing of verifiers is executed here beyond importing two modules and reading three of their constants; the
process installs tools/tripwires.py first (nothing can be started, removed or changed). It writes two files into
OUT_DIR (which must exist): `program.py`, the harness's chat program (CHAT_PROGRAM_SOURCE: what set-up writes to
/tmp/vf-scripts/<sha256>.py), and `setup.json`: the shell command of Runtime.prepare_uv_script
(runtimes/base.py:258-292) for that file, the environment it adds, and the sha256.

The replay (tests/harness_setup.sh) then runs that command in `docker run --network none --read-only` and starts
the program's own `--help` with the interpreter the command printed.
"""
import hashlib
import json
import os
import shlex
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
sys.path.insert(0, os.path.dirname(HERE))
import tripwires  # noqa: E402

tw = tripwires.install()
import physim2_env  # noqa: E402,F401   (first: closes verifiers' reader of the model credential)
from verifiers.v1.harnesses.utils.launch import CHAT_PROGRAM, CHAT_PROGRAM_SOURCE  # noqa: E402
from verifiers.v1.runtimes import base as RB  # noqa: E402
from verifiers.v1.runtimes.docker import DockerRuntime  # noqa: E402

out = sys.argv[1]
data = CHAT_PROGRAM_SOURCE.encode()
digest = hashlib.sha256(data).hexdigest()
scripts_dir = DockerRuntime.scripts_dir
path = f"{scripts_dir}/{digest}.py"
tmp = f"{path}.replay.tmp"
# the command of Runtime.prepare_uv_script, character for character (runtimes/base.py:271-277)
command = (f"mv -f {shlex.quote(tmp)} {shlex.quote(path)} "
           f"&& {{ {RB._ENSURE_UV}; }} "
           f"&& uv sync --script {shlex.quote(path)} -q --no-config "
           f"&& uv python find --script {shlex.quote(path)} --no-config")
with open(os.path.join(out, "program.py"), "wb") as f:
    f.write(data)
rec = {"verifiers": __import__("verifiers").__version__, "program_sha256": digest, "program_bytes": len(data),
       "program_metadata": CHAT_PROGRAM, "scripts_dir": scripts_dir, "tmp": tmp, "path": path, "command": command,
       "env_added_by_verifiers": {"UV_OFFLINE": "false"}, "ensure_uv": RB._ENSURE_UV, "tripwire_hits": tw.hits}
with open(os.path.join(out, "setup.json"), "w") as f:
    json.dump(rec, f, indent=1)
print(json.dumps({k: rec[k] for k in ("verifiers", "program_sha256", "program_bytes", "path", "tripwire_hits")}))
