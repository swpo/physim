"""No model credential in a scripted run (host-safety audit, round 3, finding M3).

verifiers reads the operator's Prime login, `~/.prime/config.json`, in three places: when its eval config class
is DEFINED (the default client is built at import: configs/cli/eval.py:86 -> configs/client.py:41), when any
client config with the default key variable is validated (client.py:37-57), and when a model client is made
without a key in the environment (client.py:93-104, clients/eval.py:67). All three go through one function,
`verifiers.v1.utils.prime.load_prime_config`. A scripted rollout calls no model, so it has no use for that file,
and the file holds a key that can spend money.

`install()` therefore puts a stand-in for that one module into `sys.modules` BEFORE verifiers is imported: its
`load_prime_config` returns `{}` and opens nothing. It is called from the first line of `physim2_env/__init__.py`
(every tool and the laboratory process import the package before verifiers) and from tools/vfeval.py (the one
way the pilot starts vf-eval). The stand-in is skipped in exactly one case: the variable PHYSIM2_MODEL_CREDENTIALS
is "prime" (set by `tools/vfrun.py --model-credentials prime`, step 3 of RUNBOOK_MAC.md, and by nothing else)
AND the process is not a tool server (verifiers starts those with VF_CONFIG: the laboratory never needs a key).
"""
import logging
import os
import sys
import types

NAME = "verifiers.v1.utils.prime"
MODE_ENV = "PHYSIM2_MODEL_CREDENTIALS"


def real_wanted() -> bool:
    return os.environ.get(MODE_ENV) == "prime" and "VF_CONFIG" not in os.environ


def state() -> str:
    """"stand-in", "real", or "not imported yet"."""
    mod = sys.modules.get(NAME)
    if mod is None:
        return "not imported yet"
    return "stand-in" if getattr(mod, "PHYSIM2_STAND_IN", False) else "real"


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
    return state()
