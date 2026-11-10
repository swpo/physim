"""build_reference -- build the reference submission C without the hidden parameters on any command line.

Policy C (the designer's ceiling) is trained on simulations at the TRUE parameters of the hidden world. Round 5's
agents/reference_agent.py takes them as `--theta v1,v2,...`; started as a process of its own, that argument is
readable in the process list for as long as it runs, and RUNBOOK_MAC.md's status command prints the process
list (host-safety audit, round 3, finding m1). This helper is what tools/prove.py starts instead:

    python -B tools/build_reference.py --theta-file <store>/<instance>/work/reference_C.theta.json \
        --script <agentenv>/agents/reference_agent.py -- --policy C --sizes '{...}' --seed 0 --no-submit --out DIR

It reads the parameters from the file (a regular file of this user, mode 0600, inside the store), then runs the
script IN THIS PROCESS with `--theta` added to the argument list in memory only. The command line of this
process holds a path, never a value. It starts no process and removes nothing.
"""
import argparse
import json
import os
import runpy
import stat
import sys


def read_theta(path: str) -> list[float]:
    st = os.lstat(path)
    if not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) & 0o077:
        raise SystemExit("refused: the theta file must be a regular file of this user with mode 0600")
    with open(path) as f:
        theta = json.load(f)["theta"]
    if not isinstance(theta, list) or not theta or not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in theta):
        raise SystemExit("refused: the theta file holds no list of numbers")
    return [float(v) for v in theta]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta-file", required=True)
    ap.add_argument("--script", required=True, help="agentenv's agents/reference_agent.py")
    ap.add_argument("rest", nargs=argparse.REMAINDER, help="-- then the script's own arguments, without --theta")
    a = ap.parse_args()
    rest = a.rest[1:] if a.rest[:1] == ["--"] else a.rest
    if any(x == "--theta" or x.startswith("--theta=") for x in rest):
        raise SystemExit("refused: --theta on the command line is what this helper exists to avoid")
    script = os.path.abspath(a.script)
    if os.path.basename(script) != "reference_agent.py" or not os.path.isfile(script):
        raise SystemExit("refused: --script must be agentenv's agents/reference_agent.py")
    theta = read_theta(a.theta_file)
    sys.argv = [script, *rest, "--theta", ",".join(repr(v) for v in theta)]
    sys.path[0] = os.path.dirname(script)                    # as if the script had been started itself
    del theta
    runpy.run_path(script, run_name="__main__")


if __name__ == "__main__":
    main()
