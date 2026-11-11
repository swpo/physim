"""pin -- the sha256 of every file the Mac pilot executes or imports, in the format `shasum -a 256 -c` reads.

    python -B tools/pin.py --write        writes PIN.sha256 next to the runbook, prints its own sha256 and
                                          writes that hash into the pin block of RUNBOOK_MAC.md
    python -B tools/pin.py --check        recomputes every hash and compares (exit status 1 on any difference)

Host-safety audit, required change 7: RUNBOOK_MAC.md names ONE commit and the sha256 of PIN.sha256; the Mac
checks that commit out detached and runs `shasum -a 256 -c PIN.sha256` before anything else. What is listed
(tracked files only, as `git ls-files` names them; paths relative to the study folder):

  this folder     physim2_env/, physim2_script/, physim2_verifier/ (the env of a model rollout: round 4), tools/,
                  agents/, configs/, docker/ (the two Dockerfiles and, since round 4, everything the image build
                  reads: harness-uv, harness-requirements.txt, ring-requirements.txt), pyproject.toml, uv.lock,
                  .gitignore
  round 5         ../../round5/agentenv/{evaluator,physim2,agents,configs}/ and TASK.md.tmpl: imported, not copied
  the vw library  ../../../vw1/vw/

Not listed: documents and results (README.md, RUNBOOK_MAC.md, PROGRESS.md, HOST_SAFETY_AUDIT.md, results/,
redteam/, rehearsal/) and the development tests (tests/: on the runbook's never-list), which nothing in the
pilot executes. This tool reads files, writes PIN.sha256 and replaces one line
of RUNBOOK_MAC.md; nothing else.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PIN = os.path.join(ROOT, "PIN.sha256")
PATHS = ["physim2_env", "physim2_script", "physim2_verifier", "tools", "agents", "configs", "docker",
         "pyproject.toml", "uv.lock", ".gitignore",
         "../../round5/agentenv/evaluator", "../../round5/agentenv/physim2", "../../round5/agentenv/agents", "../../round5/agentenv/configs",
         "../../round5/agentenv/TASK.md.tmpl", "../../../vw1/vw"]


def tracked() -> list[str]:
    r = subprocess.run(["git", "ls-files", "-z", "--", *PATHS], cwd=ROOT, capture_output=True, check=True)
    names = sorted(n for n in r.stdout.decode().split("\0") if n)
    if not names or any("\n" in n or n.startswith("/") for n in names):
        raise SystemExit("no tracked files found, or a file name this format cannot carry")
    return names


def digest(path: str) -> str:
    h = hashlib.sha256()
    with open(os.path.join(ROOT, path), "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def lines() -> str:
    return "".join(f"{digest(n)}  {n}\n" for n in tracked())


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.write:
        text = lines()
        with open(PIN, "w", newline="\n") as f:
            f.write(text)
        own = hashlib.sha256(text.encode()).hexdigest()
        book = os.path.join(ROOT, "RUNBOOK_MAC.md")
        old = open(book).read()
        new, n = re.subn(r"(sha256 of `PIN\.sha256`: `)[0-9a-zA-Z_]+(`)", lambda m: m.group(1) + own + m.group(2), old)
        if n != 1:
            raise SystemExit("RUNBOOK_MAC.md has no pin block line to carry the hash")
        if new != old:
            with open(book, "w", newline="\n") as f:
                f.write(new)
        print(f"{own}  PIN.sha256   ({text.count(chr(10))} files)")
        return
    want = open(PIN).read()
    bad = []
    listed = {}
    for ln in want.splitlines():
        h, _, name = ln.partition("  ")
        listed[name] = h
    now = {n: digest(n) for n in tracked()}
    bad += [f"changed: {n}" for n in sorted(listed) if n in now and now[n] != listed[n]]
    bad += [f"missing: {n}" for n in sorted(listed) if n not in now]
    bad += [f"not listed: {n}" for n in sorted(now) if n not in listed]
    print(f"{hashlib.sha256(want.encode()).hexdigest()}  PIN.sha256   ({len(listed)} files listed, {len(bad)} differences)")
    for b in bad[:40]:
        print(b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
