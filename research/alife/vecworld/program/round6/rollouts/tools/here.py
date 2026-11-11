"""here -- start one tool of the pinned port (../../vfport/tools) in the cloud container, changing nothing in the pinned tree.

    nice -n 10 <venv python> -B rollouts/tools/here.py --run-id LABEL TOOL.py [the tool's own arguments]

TOOL.py is one of TOOLS below. What this wrapper does, and why (first model rollouts of round 6, 11 Nov 2026):

1. THE SESSION ENVIRONMENT. The cloud session holds about 170 variables, two of which the port's tools refuse
   (UV_NATIVE_TLS, DOCKER_HTTPS_PROXY: vfrun.ENV_REFUSE), and three credentials. The cloud rehearsals of the runbook
   issued every command from PATH, HOME, USER, LANG and nothing else (results/rehearsal_round3.json, `how`). This
   wrapper does that in-process: it builds exactly that environment, adds VF_RUN_ID (--run-id) and starts the tool
   in it (execve). No value of the caller's environment is put on a command line, printed or written.
2. THE MODEL KEY, for `vfrun.py ... --model-credentials prime` only (runbook step 3): PRIME_API_KEY and
   PRIME_TEAM_ID are copied from the caller's environment into the new process's ENVIRONMENT (never its argument
   list); tools/vfrun.py then passes them on to vf-eval as its step-3 route does (ENV_PASS_MODEL). For every other
   tool, and for the dry run, they are not copied.
3. THE MACHINE'S CA BUNDLE, for the same command only. This container sits behind a TLS-intercepting proxy.
   verifiers' model client is httpx, which checks certificates against certifi unless SSL_CERT_FILE names another
   bundle; tools/vfrun.py gives vf-eval an allow-list of names (ENV_PASS, tools/vfrun.py line 62) on which
   SSL_CERT_FILE is not, so the first model call would end in CERTIFICATE_VERIFY_FAILED (measured before the
   rollout: rollouts/PROGRESS.md). For that command the wrapper therefore runs tools/vfrun.py's own main() in this
   process after adding the one NAME "SSL_CERT_FILE" to vfrun.ENV_PASS in memory, with SSL_CERT_FILE set to the
   bundle's path (a public file of CA certificates; a path, not a secret). The pinned file is not edited. On a
   machine without such a proxy (the lead's Mac) none of this is needed.

Everything else is the pinned tool, unchanged: its refusals, the disk watchdog, the one stop path, the docker shim.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VFPORT = os.path.normpath(os.path.join(HERE, "..", "..", "vfport"))
TOOLS = ("make_instances.py", "prove.py", "vfrun.py", "run_report.py", "settle.py")
SESSION = ("PATH", "HOME", "USER", "LANG")                   # what the cloud rehearsals gave every command
MODEL = ("PRIME_API_KEY", "PRIME_TEAM_ID")                   # step 3 only, by inheritance
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"                       # this machine's CA bundle (system roots + the proxy's CA)
STAGE = "ROLLOUT_HERE_STAGE"                                 # not a name the port refuses, and not on its allow-list


def main() -> int:
    argv = sys.argv[1:]
    if len(argv) < 3 or argv[0] != "--run-id" or argv[2] not in TOOLS:
        raise SystemExit("usage: here.py --run-id LABEL {" + ",".join(TOOLS) + "} [arguments of the tool]")
    label, tool, rest = argv[1], argv[2], argv[3:]
    model = tool == "vfrun.py" and "--model-credentials" in rest and "--dry-run" not in rest
    if os.environ.get(STAGE) != "2":
        if not os.path.isfile(os.path.join(VFPORT, "tools", tool)) or not os.path.isfile(os.path.join(VFPORT, "PIN.sha256")):
            raise SystemExit("refused: the pinned port is not next to this folder")
        env = {k: os.environ[k] for k in SESSION if k in os.environ}
        env.setdefault("USER", "root")
        env.setdefault("LANG", "C.UTF-8")
        env["VF_RUN_ID"] = label
        if model:
            missing = [k for k in MODEL if not os.environ.get(k)]
            if missing or not os.path.isfile(CA_BUNDLE):
                raise SystemExit("refused: the model rollout needs " + ", ".join(MODEL) + " in the environment and the CA bundle "
                                 "on disk (missing: " + (", ".join(missing) or "the bundle") + "). Nothing was started.")
            env.update({k: os.environ[k] for k in MODEL})
            env["SSL_CERT_FILE"] = CA_BUNDLE
            env[STAGE] = "2"
            os.chdir(VFPORT)
            os.execve(sys.executable, [sys.executable, "-B", os.path.abspath(__file__), *argv], env)
        os.chdir(VFPORT)                                     # as the runbook starts every tool: in the study folder
        os.execve(sys.executable, [sys.executable, "-B", os.path.join("tools", tool), *rest], env)
    # ---- stage 2: the model rollout, in the environment built above ----
    os.environ.pop(STAGE, None)
    sys.path.insert(0, os.path.join(VFPORT, "tools"))
    import vfrun
    if "SSL_CERT_FILE" not in vfrun.ENV_PASS:
        vfrun.ENV_PASS = tuple(vfrun.ENV_PASS) + ("SSL_CERT_FILE",)
    return vfrun.main(rest)


if __name__ == "__main__":
    sys.exit(main())
