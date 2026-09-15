"""Experiments and prediction evaluation for prepared physical worlds.

The base package has no model-client or historical research-tree dependency.
Historical tasksets remain source-checkout compatibility imports only.
"""
from importlib import import_module

__version__ = "0.12.0"
__all__ = ["Bundle", "BundleError", "ExperimentService", "OracleRunner"]
_PUBLIC = {
    "Bundle": ("physim.bundles", "Bundle"),
    "BundleError": ("physim.bundles", "BundleError"),
    "ExperimentService": ("physim.blobround6_explore", "ExperimentService"),
    "OracleRunner": ("physim.blobround6", "OracleRunner"),
}
_LEGACY = {"PhysimConfig", "PhysimData", "PhysimEnv", "PhysimEnvConfig", "PhysimTask", "PhysimTaskset"}


def __getattr__(name):
    if name in _PUBLIC:
        module, attribute = _PUBLIC[name]
        return getattr(import_module(module), attribute)
    if name in _LEGACY:
        try:
            return getattr(import_module("physim.taskset"), name)
        except ModuleNotFoundError as exc:
            if exc.name == "physim.taskset":
                raise ImportError("Historical tasksets are source-checkout only; use physim_r6 for the supported native task") from exc
            raise
    raise AttributeError(name)
