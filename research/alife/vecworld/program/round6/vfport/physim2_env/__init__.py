"""physim2_env -- the PhySim v2 exam as a verifiers v1 taskset (`--env.taskset.id physim2-env`).

    vf-eval physim2-env --env.id isolated-verifier --env.agent.runtime.type docker --no-push ...

See README.md of the study folder (program/round6/vfport) for what verifiers supplies and what is ours.
"""
from . import _nokey

_nokey.install()                                             # FIRST: before anything here imports verifiers (see _nokey.py)

from .taskset import Physim2Config, Physim2Data, Physim2State, Physim2Task, Physim2TaskConfig, Physim2Taskset  # noqa: E402

__all__ = ["Physim2Taskset", "Physim2Task", "Physim2Data", "Physim2State", "Physim2Config", "Physim2TaskConfig"]
