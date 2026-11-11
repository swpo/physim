"""fetch4 -- step 3a of RUNBOOK_MAC.md for a REHEARSAL request: the pinned tools/check_request.py, unchanged on
disk, run with the one constant that says where requests live in the repository changed in memory.

    .venv/bin/python -B rehearsal/fetch4.py --requests-prefix research/.../round6/vfport/rehearsal/round4_jobs/ \
        --fetch --source-commit HEX --job-id ID --pilot DIR

Why: the Mac's runner executes every request that appears under `research/alife/vecworld/program/rollouts/requests/`
on the lab branch. A rehearsal in the cloud container must therefore never commit a file there. Its request is
committed under this folder instead (`rehearsal/round4_jobs/<job_id>.json`), and this wrapper lets the pinned
fetch read it from there. Everything else is the pinned tool: the shape check of the request, the config taken
from `round6/rollouts/configs/` of the same commit, the shared ledger, the three files written into the pilot
folder. The prefix must be a folder of the repository below `research/` that is no `requests/` folder.

Cloud rehearsal only (PHYSIM2_DEV_MACHINE=cloud-container is not asked for here because the runbook's command
carries no such variable; rehearsal/ is on the never-list of RUNBOOK_MAC.md, rule 8, and the Mac's runner fetches
with tools/check_request.py as the runbook says).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2 or argv[0] != "--requests-prefix":
        raise SystemExit("usage: fetch4.py --requests-prefix research/<folder>/ --fetch --source-commit HEX --job-id ID --pilot DIR")
    prefix, rest = argv[1], argv[2:]
    if sys.platform != "linux":
        raise SystemExit("refused: a rehearsal tool of the cloud container; not for the Mac")
    if not re.fullmatch(r"research/[A-Za-z0-9/._-]+/", prefix) or ".." in prefix or "/requests/" in "/" + prefix:
        raise SystemExit("refused: --requests-prefix is a repository folder below research/ that is no `requests/` folder")
    if "--fetch" not in rest:
        raise SystemExit("refused: this wrapper is for the fetch of step 3a only")
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import check_request as CR
    CR.REQUESTS_PREFIX = prefix
    return CR.main(rest)


if __name__ == "__main__":
    sys.exit(main())
