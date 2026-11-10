"""physim2 -- the agent-facing package of a PhySim-v2 exam.

    import physim2
    W = physim2.load_world()        # the public world: law, coarse-grainings, prior, programs, simulator
    lab = physim2.Lab()             # the real (hidden) world, within tick and nats budgets

Everything in this package is public. The hidden parameters and the noise secret live in the Lab
process only.
"""
from .labclient import Lab, LabError  # noqa: F401


def load_world():
    """The public world module of this exam (see its docstring and TASK.md)."""
    import importlib
    import json
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    f = os.path.join(here, "world.json")
    name = json.load(open(f))["world"] if os.path.exists(f) else os.environ.get("PHYSIM2_WORLD", "ring")
    return importlib.import_module(f".world_{name}", __name__)
