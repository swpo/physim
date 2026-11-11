"""redact_values -- replace the operator's ACCOUNT IDENTIFIERS, by value, in files that are about to be committed.

    <venv python> -B rollouts/tools/redact_values.py PATH [PATH ...]

The safety net behind extract.py's removal by field name: tools/scan_key.py exits with status 2 when a file still
holds the value of PRIME_TEAM_ID or of `user_id`, `user_name`, `team_id` of ~/.prime/config.json (a trace names
the operator's account in places no field name announces). This tool replaces each such value with
`[removed: account identifier]` in place and prints file names and counts only. It never touches a credential:
if scan_key finds a KEY (status 1), nothing is redacted and nothing is committed; that is a blocker to report.
Only files under the paths given are changed; run it on copies made for the repository, never on a run folder.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_key import files, needles  # noqa: E402

MARK = b"[removed: account identifier]"


def main() -> int:
    cred, ident = needles()
    out = {}
    for f in files(sys.argv[1:]):
        with open(f, "rb") as h:
            data = h.read()
        if any(v in data for v in cred.values()):
            print(json.dumps({"refused": "a credential is in " + f + "; nothing was changed"}))
            return 1
        n = 0
        for v in ident.values():
            n += data.count(v)
            data = data.replace(v, MARK)
        if n:
            with open(f, "wb") as h:
                h.write(data)
            out[f] = n
    print(json.dumps({"identifier_values_replaced": out, "total": sum(out.values())}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
