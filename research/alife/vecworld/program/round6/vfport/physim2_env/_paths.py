"""Where the kept round-5 code lives. physim2_env reuses agentenv BY IMPORT (no copy): the hidden-side modules
(evaluator.instance, evaluator.lab_service.LabService, evaluator.grader.table, evaluator.acceptance,
evaluator.build_workspace), the public package physim2 (world modules, predict_runner.py), TASK.md.tmpl, the
reference agents and the configs. Set PHYSIM2_AGENTENV to use a checkout elsewhere."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "public")


def agentenv_root() -> str:
    p = os.environ.get("PHYSIM2_AGENTENV") or os.path.join(HERE, "..", "..", "..", "round5", "agentenv")
    p = os.path.abspath(p)
    if not os.path.isfile(os.path.join(p, "evaluator", "instance.py")):
        raise RuntimeError(f"agentenv not found at {p}: install physim2_env from a checkout of the physim repository "
                           "(editable install) or set PHYSIM2_AGENTENV")
    return p


def use_agentenv() -> str:
    """Put agentenv on sys.path (once) and return its root."""
    root = agentenv_root()
    if root not in sys.path:
        sys.path.insert(0, root)
    os.environ.setdefault("JAX_PLATFORMS", "cpu")
    return root


def config_path(name: str) -> str:
    return os.path.join(agentenv_root(), "configs", f"{name}.json")
