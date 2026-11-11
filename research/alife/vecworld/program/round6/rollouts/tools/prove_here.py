"""prove_here -- the pinned ../../vfport/tools/prove.py in the cloud container, with every box capped in memory.

    nice -n 10 <venv python> -B rollouts/tools/prove_here.py --run-id LABEL --box-memory-gb 4 [arguments of prove.py]

Why this exists next to here.py (added for rollout astra_ring_001, 11 Nov 2026): tools/prove.py builds the config
of each scripted reference rollout itself (tools/vfrun.py, run_eval) and has an option for the boxes' CPUs
(--cpu) but none for their memory, so the reference boxes of rollout qwen_ring_001 ran with the task row's own
limit (8 GiB) while this shared machine's rule is 4 GB per box. This wrapper changes no file of the pinned tree.
It does what here.py does for every tool (a new process whose environment is PATH, HOME, USER, LANG and VF_RUN_ID
and nothing else of the session; no credential is copied: the reference policies call no model), then runs
tools/prove.py in that process after wrapping `tomli_w.dump`, the one call through which run_eval writes a
rollout's config: every config whose agent runtime is docker gets `memory = N` (GB) before it is written. The
verifier box and the item boxes take the agent's runtime config, so the cap holds for them as well. The scores
of the reference policies do not depend on it (ridge regressions on a few hundred episodes).
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VFPORT = os.path.normpath(os.path.join(HERE, "..", "..", "vfport"))
SESSION = ("PATH", "HOME", "USER", "LANG")
STAGE = "ROLLOUT_HERE_STAGE"                                 # not a name the port refuses, and not on its allow-list


def main() -> int:
    argv = sys.argv[1:]
    if len(argv) < 4 or argv[0] != "--run-id" or argv[2] != "--box-memory-gb":
        raise SystemExit("usage: prove_here.py --run-id LABEL --box-memory-gb N [arguments of tools/prove.py]")
    label, mem, rest = argv[1], int(argv[3]), argv[4:]
    if not 1 <= mem <= 8:
        raise SystemExit("refused: --box-memory-gb must be a whole number of GB from 1 to 8")
    tool = os.path.join(VFPORT, "tools", "prove.py")
    if os.environ.get(STAGE) != "2":
        if not os.path.isfile(tool) or not os.path.isfile(os.path.join(VFPORT, "PIN.sha256")):
            raise SystemExit("refused: the pinned port is not next to this folder")
        env = {k: os.environ[k] for k in SESSION if k in os.environ}
        env.setdefault("USER", "root")
        env.setdefault("LANG", "C.UTF-8")
        env["VF_RUN_ID"] = label
        env[STAGE] = "2"
        os.chdir(VFPORT)
        os.execve(sys.executable, [sys.executable, "-B", os.path.abspath(__file__), *argv], env)
    os.environ.pop(STAGE, None)
    import tomli_w
    plain_dump = tomli_w.dump

    def dump(obj, fp, **kw):
        runtime = (((obj.get("env") or {}).get("agent") or {}).get("runtime")) if isinstance(obj, dict) else None
        if isinstance(runtime, dict) and runtime.get("type") == "docker":
            runtime["memory"] = mem
        return plain_dump(obj, fp, **kw)

    tomli_w.dump = dump
    sys.argv = [os.path.join("tools", "prove.py"), *rest]
    sys.path.insert(0, os.path.join(VFPORT, "tools"))        # as `python tools/prove.py` would have it
    runpy.run_path(tool, run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
