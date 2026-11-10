"""No model credential in a scripted run (host-safety audit, round 3, finding M3).

Two readers of the operator's Prime login, `~/.prime/config.json`, are on the route of a scripted rollout:

1. verifiers itself, in three places: when its eval config class is DEFINED (the default client is built at
   import: configs/cli/eval.py:86 -> configs/client.py:41), when any client config with the default key variable
   is validated (client.py:37-57), and when a model client is made without a key in the environment
   (client.py:93-104, clients/eval.py:67). All three go through `verifiers.v1.utils.prime.load_prime_config`.
2. the prime-runs SDK, which vf-eval calls once per run even when nothing is uploaded: `prime_runs.init(mode=
   "disabled")` builds a `Config`, and `prime_traces.core.config.Config._load_config` reads the file and its key
   (verifiers utils/platform.py:93 -> prime_runs/run.py:456 -> prime_traces/core/config.py:25-32). Found in round
   3 by tracing a rollout; the Mac session's review had named the first reader only.

A scripted rollout calls no model and uploads nothing, so it has no use for that file, and the file holds a key
that can spend money. `install()` therefore closes both readers BEFORE verifiers is imported: it puts a stand-in
for the module of (1) into `sys.modules` (its `load_prime_config` returns `{}`), and replaces the one method of
(2) by one that sets an empty configuration; neither opens anything. It is called from the first line of
`physim2_env/__init__.py` (every tool and the laboratory process import the package before verifiers) and from
tools/vfeval.py (the one way the pilot starts vf-eval). It does nothing in exactly one case: the variable
PHYSIM2_MODEL_CREDENTIALS is "prime" (set by `tools/vfrun.py --model-credentials prime`, step 3 of
RUNBOOK_MAC.md, and by nothing else) AND the process is not a tool server (verifiers starts those with
VF_CONFIG: the laboratory never needs a key).

Two more modules of the environment can read the file, `prime_sandboxes.core.config` and
`prime_tunnel.core.config`; verifiers reaches them only through its Prime runtime and its tunnel, which a Docker
rollout does not use, and `ensure_prime_auth` of the stand-in stops both before they start.
"""
import logging
import os
import sys
import types

NAME = "verifiers.v1.utils.prime"
TRACES = "prime_traces.core.config"
MODE_ENV = "PHYSIM2_MODEL_CREDENTIALS"


def real_wanted() -> bool:
    return os.environ.get(MODE_ENV) == "prime" and "VF_CONFIG" not in os.environ


def state() -> str:
    """"stand-in" (both readers closed), "real", "real (prime_traces)", or "not imported yet"."""
    mod = sys.modules.get(NAME)
    if mod is None:
        return "not imported yet"
    if not getattr(mod, "PHYSIM2_STAND_IN", False):
        return "real"
    traces = sys.modules.get(TRACES)
    if traces is not None and not getattr(traces.Config, "PHYSIM2_STAND_IN", False):
        return "real (prime_traces)"
    return "stand-in"


def _close_prime_traces() -> None:
    """Reader 2: `Config()` of prime_traces (and of prime_runs, its subclass) no longer opens the file."""
    try:
        import importlib
        mod = importlib.import_module(TRACES)
    except ImportError:                                      # not installed: nothing to close
        return
    if getattr(mod.Config, "PHYSIM2_STAND_IN", False):
        return

    def _load_config(self) -> None:
        self.config = {}
    mod.Config._load_config = _load_config
    mod.Config.PHYSIM2_STAND_IN = True


def install() -> str:
    """Make sure that this process cannot read ~/.prime/config.json through verifiers (see the module text).
    Returns state() afterwards. If the real module was imported already, nothing is changed and "real" is
    returned: the caller decides whether that is acceptable (tools/vfeval.py refuses)."""
    if NAME in sys.modules or real_wanted():
        return state()
    mod = types.ModuleType(NAME)
    mod.__doc__ = "stand-in installed by physim2_env._nokey: a scripted run loads no model credential"
    mod.PHYSIM2_STAND_IN = True
    mod.logger = logging.getLogger(NAME)

    def load_prime_config() -> dict:
        return {}

    def ensure_prime_auth() -> None:
        raise SystemExit("refused: this process was started without model credentials (physim2_env._nokey); "
                         "a Prime runtime or tunnel is not part of a scripted run")
    mod.load_prime_config, mod.ensure_prime_auth = load_prime_config, ensure_prime_auth
    sys.modules[NAME] = mod
    _close_prime_traces()
    return state()
