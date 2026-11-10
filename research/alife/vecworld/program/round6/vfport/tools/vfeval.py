"""vfeval -- verifiers' `vf-eval`, started so that a scripted run cannot load the operator's model credential.

The console script .venv/bin/vf-eval imports verifiers first, and verifiers reads ~/.prime/config.json while it
is being imported (host-safety audit, round 3, finding M3; physim2_env/_nokey.py has the lines). This file is
the pilot's only way to start vf-eval: it imports physim2_env first, whose first line installs a stand-in for
verifiers' reader of that file, and then calls verifiers' own entry point with the arguments it was given.
It is started by tools/vfrun.py and by nothing else; RUNBOOK_MAC.md never names it in a command.

    python -B tools/vfeval.py @ <config.toml> [vf-eval options]

Without PHYSIM2_MODEL_CREDENTIALS=prime (step 3 only, set by tools/vfrun.py) it refuses to go on unless the
stand-in is in place, and it removes PRIME_API_KEY, PRIME_TEAM_ID and PRIME_INFERENCE_URL from its own
environment, so that neither this process nor a child holds them.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if sys.path and os.path.abspath(sys.path[0] or ".") == HERE:
    sys.path[0] = ROOT                                       # the study folder, not tools/, is this process's first import path
else:
    sys.path.insert(0, ROOT)

from physim2_env import _nokey  # noqa: E402   (imports the package: its first line installs the stand-in)


def main() -> int:
    state = _nokey.install()
    if os.environ.get(_nokey.MODE_ENV) != "prime":
        if state != "stand-in":
            raise SystemExit(f"refused: verifiers' credential reader is {state} in this process; a scripted run starts only "
                             "with the stand-in of physim2_env/_nokey.py in place")
        for name in ("PRIME_API_KEY", "PRIME_TEAM_ID", "PRIME_INFERENCE_URL"):
            os.environ.pop(name, None)
    from verifiers.v1.cli.eval.main import main as vf_eval
    sys.argv[0] = "vf-eval"
    vf_eval()
    return 0


if __name__ == "__main__":
    sys.exit(main())
