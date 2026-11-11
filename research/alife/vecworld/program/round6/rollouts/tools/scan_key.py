"""scan_key -- count, without ever printing them, the operator's credentials and account identifiers in files.

    <venv python> -B rollouts/tools/scan_key.py PATH [PATH ...]

Run before every commit of this folder, on everything that is to be committed. The needles are read inside this
process and are never printed, logged or written:

  credentials   the values of PRIME_API_KEY, HF_TOKEN and WANDB_API_KEY in this process's environment, and
                `api_key` of ~/.prime/config.json if it is not empty; each also in its base64 form
  identifiers   the value of PRIME_TEAM_ID, and `user_id`, `user_name`, `team_id` of ~/.prime/config.json
                (not secrets, but they name the operator's account and do not belong in a public repository)

Output: one JSON object with file names and counts only. Exit status 1 if any credential is found (a blocker:
nothing is committed), 2 if only identifiers are found (redact them, then scan again), 0 otherwise.
"""
import base64
import json
import os
import sys


def needles() -> tuple[dict, dict]:
    cred, ident = {}, {}
    for name in ("PRIME_API_KEY", "HF_TOKEN", "WANDB_API_KEY"):
        v = os.environ.get(name, "")
        if len(v) >= 8:
            cred[name] = v.encode()
            cred[name + " (base64)"] = base64.b64encode(v.encode()).rstrip(b"=")
    v = os.environ.get("PRIME_TEAM_ID", "")
    if len(v) >= 6:
        ident["PRIME_TEAM_ID"] = v.encode()
    try:
        with open(os.path.expanduser("~/.prime/config.json")) as f:
            cfg = json.load(f)
    except (OSError, ValueError):
        cfg = {}
    v = cfg.get("api_key") or ""
    if len(v) >= 8:
        cred["~/.prime api_key"] = v.encode()
    for k in ("user_id", "user_name", "team_id"):
        v = cfg.get(k) or ""
        if isinstance(v, str) and len(v) >= 6:
            ident["~/.prime " + k] = v.encode()
    return cred, ident


def files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        for root, _, names in os.walk(p):
            for n in sorted(names):
                yield os.path.join(root, n)


def main() -> int:
    cred, ident = needles()
    out = {"needles": {"credentials": sorted(cred), "identifiers": sorted(ident)}, "files_scanned": 0, "bytes_scanned": 0,
           "credential_hits": {}, "identifier_hits": {}}
    for f in files(sys.argv[1:]):
        try:
            with open(f, "rb") as h:
                data = h.read()
        except OSError:
            continue
        out["files_scanned"] += 1
        out["bytes_scanned"] += len(data)
        for name, v in cred.items():
            n = data.count(v)
            if n:
                out["credential_hits"].setdefault(f, {})[name] = n
        for name, v in ident.items():
            n = data.count(v)
            if n:
                out["identifier_hits"].setdefault(f, {})[name] = n
    out["total_credential_hits"] = sum(n for d in out["credential_hits"].values() for n in d.values())
    out["total_identifier_hits"] = sum(n for d in out["identifier_hits"].values() for n in d.values())
    print(json.dumps(out, indent=1))
    return 1 if out["total_credential_hits"] else 2 if out["total_identifier_hits"] else 0


if __name__ == "__main__":
    sys.exit(main())
